#!/usr/bin/env python3
"""Run isolated multilingual rollout lanes within one global concurrency budget."""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
from typing import Any

from multilingual_pipeline import ROOT, azure_key, load_config, rollout_order
from multilingual_rollout import language_state


def choose_tasks(requested: list[str], workers: int) -> list[dict[str, Any]]:
    config = load_config()
    known = config["languages"]
    codes = requested or [
        code
        for code in rollout_order(config)
        if code != "en"
        and known[code].get("status") in {"pilot", "existing_revision"}
    ]
    tasks: list[dict[str, Any]] = []
    for code in codes:
        if code not in known or code == "en":
            raise ValueError(f"unknown target language: {code}")
        state = language_state(code)
        if state["pending_review"]:
            stage = "review"
        elif state["pending_draft"]:
            stage = "both"
        else:
            continue
        tasks.append({"code": code, "stage": stage, "state": state})
        if not requested and len(tasks) >= workers:
            break
    return tasks


def lane_concurrency(total: int, lanes: int) -> int:
    if total < 1 or lanes < 1:
        raise ValueError("concurrency and lanes must be positive")
    return max(1, total // lanes)


def run_task(
    task: dict[str, Any], *, limit_records: int, concurrency: int,
    log_dir: pathlib.Path, env: dict[str, str], dry_run: bool,
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
    ]
    result = {
        "code": code,
        "stage": stage,
        "concurrency": concurrency,
        "command": command,
    }
    if dry_run:
        return {**result, "status": "dry_run", "returncode": 0}

    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = log_dir / f"{code}-{stage}-{stamp}.log"
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


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--languages", nargs="*", default=[])
    value.add_argument("--workers", type=int, default=4)
    value.add_argument("--limit-records", type=int, default=500)
    value.add_argument("--total-concurrency", type=int, default=512)
    value.add_argument(
        "--log-dir",
        type=pathlib.Path,
        default=pathlib.Path("/tmp/cartha-multilingual-parallel"),
    )
    value.add_argument("--dry-run", action="store_true")
    return value


def main() -> int:
    args = parser().parse_args()
    if args.workers < 1 or args.limit_records < 1 or args.total_concurrency < 1:
        raise SystemExit("workers, limit-records, and total-concurrency must be positive")
    try:
        tasks = choose_tasks(args.languages, args.workers)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if not tasks:
        print(json.dumps({"status": "complete", "tasks": []}, indent=2))
        return 0

    lanes = min(args.workers, len(tasks))
    concurrency = lane_concurrency(args.total_concurrency, lanes)
    env = os.environ.copy()
    if not args.dry_run:
        env["AZURE_OPENAI_API_KEY"] = azure_key()
    print(
        json.dumps(
            {
                "status": "starting",
                "lanes": lanes,
                "lane_concurrency": concurrency,
                "limit_records_per_language": args.limit_records,
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
                limit_records=args.limit_records,
                concurrency=concurrency,
                log_dir=args.log_dir,
                env=env,
                dry_run=args.dry_run,
            )
            for task in tasks
        ]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    results.sort(key=lambda item: item["code"])
    print(json.dumps({"status": "finished", "results": results}, indent=2))
    return 1 if any(item["status"] == "failed" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
