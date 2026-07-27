#!/usr/bin/env python3
"""Fail when a canonical POB verse is missing from a derived translation.

The derived trees may intentionally differ under ``extra_canonical`` while that
catalog is still being translated. The Bible canon scopes (OT, NT, and
deuterocanon) must mirror the base POB so newly added source verses cannot be
silently omitted from SPOB, Spanish POB, or Korean POB.
"""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE_ROOT = "translation"
DERIVED_ROOTS = {
    "simplified": "translation_simplified",
    "spanish": "translation_es",
    "korean": "translation_ko",
}
CANONICAL_SCOPES = ("ot", "nt", "deuterocanon")


def relative_yaml_paths(root: pathlib.Path) -> set[str]:
    paths: set[str] = set()
    for scope in CANONICAL_SCOPES:
        scope_root = root / scope
        if not scope_root.exists():
            continue
        paths.update(
            path.relative_to(root).as_posix()
            for path in scope_root.rglob("*.yaml")
            if path.is_file()
        )
    return paths


def build_report(repo_root: pathlib.Path = REPO_ROOT) -> dict[str, Any]:
    base = relative_yaml_paths(repo_root / BASE_ROOT)
    derived: dict[str, Any] = {}
    for name, directory in DERIVED_ROOTS.items():
        present = relative_yaml_paths(repo_root / directory)
        derived[name] = {
            "directory": directory,
            "present": len(present),
            "missing_count": len(base - present),
            "missing": sorted(base - present),
            "extra_count": len(present - base),
            "extra": sorted(present - base),
        }
    return {
        "scopes": list(CANONICAL_SCOPES),
        "base_records": len(base),
        "derived": derived,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=REPO_ROOT,
        help="Repository root (defaults to the current checkout)",
    )
    parser.add_argument("--json", action="store_true", help="Print the full JSON report")
    args = parser.parse_args()

    report = build_report(args.root.resolve())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            "canonical derived coverage "
            f"(base={report['base_records']}, scopes={','.join(report['scopes'])})"
        )
        for name, result in report["derived"].items():
            print(
                f"  {name}: present={result['present']} "
                f"missing={result['missing_count']} extra={result['extra_count']}"
            )
            for path in result["missing"][:20]:
                print(f"    MISSING {path}")
            if result["missing_count"] > 20:
                print(f"    ... and {result['missing_count'] - 20} more")

    return 1 if any(
        result["missing_count"] for result in report["derived"].values()
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
