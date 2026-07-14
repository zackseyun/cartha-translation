#!/usr/bin/env python3
"""Coordinate fair, bounded multilingual draft and review epochs."""
from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import datetime as dt
import fcntl
import json
import os
import pathlib
import subprocess
import sys
from typing import Any

from multilingual_pipeline import (
    ROOT,
    azure_key,
    load_config,
    rollout_order,
    source_relatives,
)
from multilingual_rollout import LOCK_ROOT, language_state


COORDINATOR_LOCK = LOCK_ROOT / "coordinator.lock"


class CoordinatorBusy(RuntimeError):
    """Raised when another process already owns the global coordinator."""


@contextlib.contextmanager
def coordinator_lock():
    """Allow only one process to schedule multilingual lanes at a time."""
    COORDINATOR_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with COORDINATOR_LOCK.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CoordinatorBusy("multilingual rollout coordinator is already active") from exc
        handle.seek(0)
        handle.truncate()
        handle.write(f"pid={os.getpid()}\n")
        handle.flush()
        try:
            yield COORDINATOR_LOCK
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def rollout_codes(requested: list[str], config: dict[str, Any]) -> list[str]:
    """Return unique lanes in explicit or product-priority order."""
    known = config["languages"]
    values = requested or [
        code
        for code in rollout_order(config)
        if code != "en"
        and known[code].get("status") in {"pilot", "existing_revision"}
    ]
    codes: list[str] = []
    for code in values:
        if code not in known or code == "en":
            raise ValueError(f"unknown target language: {code}")
        if code not in codes:
            codes.append(code)
    return codes


def choose_tasks(
    codes: list[str], workers: int, *, stage: str, cursor: int,
    source: set[str],
) -> tuple[list[dict[str, Any]], int]:
    """Choose one lane per language, rotating priority to prevent starvation."""
    if workers < 1 or stage not in {"draft", "review"}:
        raise ValueError("workers must be positive and stage must be draft or review")
    if not codes:
        return [], 0

    states: dict[str, dict[str, Any]] = {}

    def state_for(code: str) -> dict[str, Any]:
        if code not in states:
            states[code] = language_state(code, source=source)
        return states[code]

    # Keep the highest unfinished readership-priority lane in every epoch.
    # Lower lanes rotate so they progress in parallel without starving the
    # primary language the user asked us to finish first.
    tasks: list[dict[str, Any]] = []
    primary_code: str | None = None
    for priority_index, code in enumerate(codes):
        state = state_for(code)
        if state[f"pending_{stage}"]:
            primary_code = code
            tasks.append(
                {
                    "code": code,
                    "stage": stage,
                    "state": state,
                    "priority_index": priority_index,
                    "primary": True,
                }
            )
            break

    scanned = 0
    while scanned < len(codes) and len(tasks) < workers:
        priority_index = (cursor + scanned) % len(codes)
        code = codes[priority_index]
        scanned += 1
        if code == primary_code:
            continue
        state = state_for(code)
        if state[f"pending_{stage}"]:
            tasks.append(
                {
                    "code": code,
                    "stage": stage,
                    "state": state,
                    "priority_index": priority_index,
                    "primary": False,
                }
            )
    return tasks, (cursor + scanned) % len(codes)


def lane_concurrency(total: int, lanes: int) -> int:
    if total < 1 or lanes < 1:
        raise ValueError("concurrency and lanes must be positive")
    return max(1, total // lanes)


def lane_concurrencies(total: int, lanes: int) -> list[int]:
    """Give the highest-priority lane half the budget and share the rest."""
    if total < 1 or lanes < 1 or lanes > total:
        raise ValueError("concurrency must cover every active lane")
    if lanes == 1:
        return [total]
    primary = max(1, total // 2)
    remaining = total - primary
    base, extra = divmod(remaining, lanes - 1)
    values = [primary]
    values.extend(base + (1 if index < extra else 0) for index in range(lanes - 1))
    return values


def run_task(
    task: dict[str, Any], *, epoch: int, limit_records: int, concurrency: int,
    draft_deployment: str, review_deployment: str, log_dir: pathlib.Path,
    env: dict[str, str], dry_run: bool,
) -> dict[str, Any]:
    code = task["code"]
    stage = task["stage"]
    command = [
        sys.executable,
        str(ROOT / "tools" / "multilingual_rollout.py"),
        "--language",
        code,
        "--stage",
        stage,
        "--limit-records",
        str(limit_records),
        "--concurrency",
        str(concurrency),
        "--draft-deployment",
        draft_deployment,
        "--review-deployment",
        review_deployment,
    ]
    result = {
        "epoch": epoch,
        "code": code,
        "stage": stage,
        "concurrency": concurrency,
        "command": command,
    }
    if dry_run:
        return {**result, "status": "dry_run", "returncode": 0}

    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = log_dir / f"{code}-{stage}-e{epoch}-{stamp}.log"
    with log_path.open("w", encoding="utf-8") as log:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
    status = "busy" if completed.returncode == 75 else (
        "complete" if completed.returncode == 0 else "failed"
    )
    return {
        **result,
        "status": status,
        "returncode": completed.returncode,
        "log": str(log_path),
    }


def run_epoch(
    tasks: list[dict[str, Any]], *, epoch: int, stage: str, workers: int,
    total_concurrency: int, limit_records: int, draft_deployment: str,
    review_deployment: str, log_dir: pathlib.Path, env: dict[str, str],
    dry_run: bool,
) -> list[dict[str, Any]]:
    """Run one stage only, within its aggregate concurrency budget."""
    lanes = min(workers, len(tasks), total_concurrency)
    tasks = tasks[:lanes]
    concurrency_by_lane = lane_concurrencies(total_concurrency, lanes)
    print(
        json.dumps(
            {
                "status": "epoch_starting",
                "epoch": epoch,
                "stage": stage,
                "lanes": lanes,
                "lane_concurrency": {
                    task["code"]: concurrency_by_lane[index]
                    for index, task in enumerate(tasks)
                },
                "total_concurrency_budget": total_concurrency,
                "limit_records_per_language": limit_records,
                "languages": [task["code"] for task in tasks],
            },
            indent=2,
        )
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=lanes) as pool:
        futures = [
            pool.submit(
                run_task,
                task,
                epoch=epoch,
                limit_records=limit_records,
                concurrency=concurrency_by_lane[index],
                draft_deployment=draft_deployment,
                review_deployment=review_deployment,
                log_dir=log_dir,
                env=env,
                dry_run=dry_run,
            )
            for index, task in enumerate(tasks)
        ]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    results.sort(key=lambda item: item["code"])
    print(
        json.dumps(
            {"status": "epoch_finished", "epoch": epoch, "stage": stage, "results": results},
            indent=2,
        )
    )
    return results


def parser() -> argparse.ArgumentParser:
    config = load_config()
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--languages", nargs="*", default=[])
    value.add_argument("--workers", type=int, default=4)
    value.add_argument("--epochs", type=int, default=4)
    value.add_argument("--limit-records", type=int, default=500)
    value.add_argument("--draft-total-concurrency", type=int, default=32)
    value.add_argument("--review-total-concurrency", type=int, default=64)
    value.add_argument(
        "--total-concurrency",
        type=int,
        help=argparse.SUPPRESS,
    )
    value.add_argument(
        "--draft-deployment",
        "--draft-pool",
        dest="draft_deployment",
        default=str(config["draft_deployment"]),
        help="Explicit comma-separated draft deployment pool.",
    )
    value.add_argument(
        "--review-deployment",
        "--review-pool",
        dest="review_deployment",
        default=str(config["review_deployment"]),
        help="Explicit comma-separated review deployment pool.",
    )
    value.add_argument(
        "--log-dir",
        type=pathlib.Path,
        default=pathlib.Path("/tmp/cartha-multilingual-parallel"),
    )
    value.add_argument("--dry-run", action="store_true")
    return value


def coordinate(args: argparse.Namespace) -> int:
    if args.total_concurrency is not None:
        args.draft_total_concurrency = args.total_concurrency
        args.review_total_concurrency = args.total_concurrency
    if any(
        value < 1
        for value in (
            args.workers,
            args.epochs,
            args.limit_records,
            args.draft_total_concurrency,
            args.review_total_concurrency,
        )
    ):
        raise SystemExit(
            "workers, epochs, limit-records, and stage concurrency budgets must be positive"
        )

    config = load_config()
    try:
        codes = rollout_codes(args.languages, config)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    source = set(source_relatives())
    env = os.environ.copy()
    if not args.dry_run:
        env["AZURE_OPENAI_API_KEY"] = azure_key()

    cursors = {"draft": 0, "review": 0}
    all_results: list[dict[str, Any]] = []
    completed = False
    for epoch in range(1, args.epochs + 1):
        scheduled = 0
        for stage, budget in (
            ("draft", args.draft_total_concurrency),
            ("review", args.review_total_concurrency),
        ):
            tasks, cursors[stage] = choose_tasks(
                codes,
                args.workers,
                stage=stage,
                cursor=cursors[stage],
                source=source,
            )
            if not tasks:
                continue
            scheduled += len(tasks)
            results = run_epoch(
                tasks,
                epoch=epoch,
                stage=stage,
                workers=args.workers,
                total_concurrency=budget,
                limit_records=args.limit_records,
                draft_deployment=args.draft_deployment,
                review_deployment=args.review_deployment,
                log_dir=args.log_dir,
                env=env,
                dry_run=args.dry_run,
            )
            all_results.extend(results)
            if any(item["status"] == "failed" for item in results):
                print(json.dumps({"status": "failed", "results": all_results}, indent=2))
                return 1
        if not scheduled:
            completed = True
            break

    print(
        json.dumps(
            {
                "status": "complete" if completed else "epoch_limit_reached",
                "epochs": epoch,
                "results": all_results,
            },
            indent=2,
        )
    )
    return 0


def main() -> int:
    args = parser().parse_args()
    try:
        with coordinator_lock():
            return coordinate(args)
    except CoordinatorBusy as exc:
        print(json.dumps({"status": "busy", "message": str(exc)}))
        return 75


if __name__ == "__main__":
    raise SystemExit(main())
