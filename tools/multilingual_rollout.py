#!/usr/bin/env python3
"""Choose and run the next bounded multilingual Azure rollout wave."""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from typing import Any

from multilingual_pipeline import BLOCK_ROOT, ROOT, load_config, source_relatives


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


def language_state(code: str) -> dict[str, Any]:
    source = set(source_relatives())
    target_root = ROOT / f"translation_{code}"
    all_target = relative_files(target_root)
    target = all_target & source
    reviewed = reviewed_files(target_root) & source
    pending_review = sorted(target - reviewed - blocked_files(code, "review"))
    pending_draft = sorted(source - target - blocked_files(code, "draft"))
    return {
        "code": code,
        "source": len(source),
        "files": len(target),
        "reviewed": len(reviewed),
        "non_publication_records": len(all_target - source),
        "pending_review": len(pending_review),
        "pending_draft": len(pending_draft),
        "blocked_review": len(blocked_files(code, "review")),
        "blocked_draft": len(blocked_files(code, "draft")),
    }


def choose_next() -> tuple[str, str, dict[str, Any]] | None:
    config = load_config()
    ordered = ["es", "ko"] + [
        code for code, spec in config["languages"].items() if spec.get("status") == "pilot"
    ]
    for code in ordered:
        state = language_state(code)
        if state["pending_review"]:
            return code, "review", state
        if state["pending_draft"]:
            return code, "both", state
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit-records", type=int, default=500)
    parser.add_argument("--concurrency", type=int, default=32)
    args = parser.parse_args()

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

    selection = choose_next()
    if selection is None:
        print("All configured multilingual draft and review stages are complete.")
        return 0
    code, stage, state = selection
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
    ]
    print(" ".join(command))
    if args.dry_run:
        return 0
    return subprocess.run(command, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
