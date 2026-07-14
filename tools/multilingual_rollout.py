#!/usr/bin/env python3
"""Choose and run the next bounded multilingual Azure rollout wave."""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import json
import os
import pathlib
import subprocess
import sys
from typing import Any

from multilingual_pipeline import (
    BLOCK_ROOT,
    ROOT,
    load_config,
    rollout_order,
    source_relatives,
)


LOCK_ROOT = pathlib.Path(
    os.environ.get("CARTHA_MULTILINGUAL_LOCK_DIR", "/tmp/cartha-multilingual-rollout-locks")
)


class LanguageBusy(RuntimeError):
    """Raised when another rollout already owns a language lane."""


@contextlib.contextmanager
def language_lock(code: str):
    """Hold an advisory cross-process lock for one target language."""
    LOCK_ROOT.mkdir(parents=True, exist_ok=True)
    path = LOCK_ROOT / f"{code}.lock"
    with path.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise LanguageBusy(f"rollout already active for language: {code}") from exc
        handle.seek(0)
        handle.truncate()
        handle.write(f"pid={os.getpid()}\n")
        handle.flush()
        try:
            yield path
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def relative_files(root: pathlib.Path) -> set[str]:
    if not root.exists():
        return set()
    return {str(path.relative_to(root)) for path in root.rglob("*.yaml")}


def reviewed_files(root: pathlib.Path) -> set[str]:
    if not root.exists():
        return set()
    probe = subprocess.run(
        ["rg", "-l", "^review_pass:", str(root), "--glob", "*.yaml"],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        str(pathlib.Path(line).relative_to(root))
        for line in probe.stdout.splitlines()
        if line.strip()
    }


def blocked_files(code: str, stage: str) -> set[str]:
    root = BLOCK_ROOT / code / stage
    return relative_files(root)


def language_state(code: str, source: set[str] | None = None) -> dict[str, Any]:
    source = source if source is not None else set(source_relatives())
    target_root = ROOT / f"translation_{code}"
    all_target = relative_files(target_root)
    target = all_target & source
    reviewed = reviewed_files(target_root) & source
    blocked_review = blocked_files(code, "review")
    blocked_draft = blocked_files(code, "draft")
    pending_review = target - reviewed - blocked_review
    pending_draft = source - target - blocked_draft
    return {
        "code": code,
        "source": len(source),
        "files": len(target),
        "reviewed": len(reviewed),
        "non_publication_records": len(all_target - source),
        "pending_review": len(pending_review),
        "pending_draft": len(pending_draft),
        "blocked_review": len(blocked_review),
        "blocked_draft": len(blocked_draft),
    }


def choose_next() -> tuple[str, str, dict[str, Any]] | None:
    config = load_config()
    ordered = [
        code for code in rollout_order(config)
        if code != "en"
        and config["languages"][code].get("status") in {"pilot", "existing_revision"}
    ]
    for code in ordered:
        state = language_state(code)
        if state["pending_review"]:
            return code, "review", state
        if state["pending_draft"]:
            return code, "draft", state
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    config = load_config()
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit-records", type=int, default=500)
    parser.add_argument("--concurrency", type=int, default=32)
    parser.add_argument(
        "--language",
        help="Run a known language directly instead of rescanning earlier rollout priorities.",
    )
    parser.add_argument(
        "--stage",
        choices=("draft", "review", "both"),
        help="Run a known stage directly; requires --language.",
    )
    parser.add_argument(
        "--draft-deployment",
        default=str(config["draft_deployment"]),
        help="Explicit comma-separated draft deployment pool.",
    )
    parser.add_argument(
        "--review-deployment",
        default=str(config["review_deployment"]),
        help="Explicit comma-separated review deployment pool.",
    )
    args = parser.parse_args()

    if args.stage and not args.language:
        parser.error("--stage requires --language")

    if args.status:
        config = load_config()
        print(
            json.dumps(
                [language_state(code) for code in config["languages"] if code != "en"],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.language and args.stage:
        config = load_config()
        if args.language not in config["languages"] or args.language == "en":
            parser.error(f"unknown target language: {args.language}")
        code, stage = args.language, args.stage
        state = {"directed": True}
    else:
        selection = choose_next()
        if selection is None:
            print("All configured multilingual draft and review stages are complete.")
            return 0
        code, stage, state = selection
    try:
        with language_lock(code):
            print(json.dumps({"selected_language": code, "stage": stage, "state": state}, indent=2))
            command = [
                sys.executable,
                str(ROOT / "tools" / "multilingual_pipeline.py"),
                "wave",
                "--language",
                code,
                "--stage",
                stage,
                "--pending-only",
                "--limit-records",
                str(args.limit_records),
                "--concurrency",
                str(args.concurrency),
                "--draft-deployment",
                args.draft_deployment,
                "--review-deployment",
                args.review_deployment,
            ]
            print(" ".join(command))
            if args.dry_run:
                return 0
            return subprocess.run(command, cwd=ROOT, check=False).returncode
    except LanguageBusy as exc:
        print(json.dumps({"selected_language": code, "status": "busy", "message": str(exc)}))
        return 75


if __name__ == "__main__":
    raise SystemExit(main())
