#!/usr/bin/env python3
"""Repair legacy malformed Spanish YAML while preserving publication text.

A small set of historical review records were written with prose that was not
properly YAML-quoted.  The publication translation is still recoverable.  This
tool rebuilds only malformed records from their English source record and the
Spanish `translation.text`, removes orphaned footnote markers, and marks the
record for a fresh source-grounded review.

Valid records are never touched.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES_ROOT = ROOT / "translation_es"
EN_ROOT = ROOT / "translation"


def clean_controls(value: str) -> str:
    return "".join(ch for ch in value if ch in "\n\t" or ord(ch) >= 32)


def extract_translation_text(raw: str) -> str:
    lines = raw.splitlines()
    start = next((i for i, line in enumerate(lines) if line == "translation:"), None)
    if start is None:
        raise ValueError("top-level translation block missing")
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line and not line.startswith(" "):
            break
        if not line.startswith("  text:"):
            continue
        value = line.split(":", 1)[1].strip()
        continuation: list[str] = []
        for following in lines[i + 1 :]:
            if following.startswith("    "):
                continuation.append(following.strip())
            else:
                break
        if continuation and (value in {"|", ">", "|-", ">-"} or not value):
            value = " ".join(continuation)
        try:
            parsed = yaml.safe_load(f"value: {clean_controls(value)}\n")
            text = str((parsed or {}).get("value") or "")
        except Exception:
            text = clean_controls(value)
            pairs = [("‘", "’"), ("“", "”"), ("'", "'"), ('"', '"')]
            for left, right in pairs:
                if text.startswith(left) and text.endswith(right) and len(text) >= 2:
                    text = text[1:-1]
                    break
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            raise ValueError("translation.text empty")
        return text
    raise ValueError("translation.text missing")


def load_english(path: pathlib.Path) -> dict[str, Any]:
    relative = path.relative_to(ES_ROOT)
    source_path = EN_ROOT / relative
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid English source record: {source_path}")
    return data


def repaired_record(path: pathlib.Path, raw: str) -> dict[str, Any]:
    english = load_english(path)
    text = extract_translation_text(raw)
    # The malformed review prose may have made its footnote objects
    # unrecoverable. Avoid publishing orphaned anchors; the fresh reviewer can
    # restore only the notes that are genuinely needed.
    text = re.sub(r"\[[a-z]\]", "", text)
    en_translation = english.get("translation") or {}
    return {
        "id": english.get("id"),
        "reference": english.get("reference"),
        "language": {
            "code": "es",
            "name": "Spanish",
            "variant": "neutral Latin American",
        },
        "source": english.get("source") or {},
        "base_translation": {
            "language": "en",
            "yaml_path": str((EN_ROOT / path.relative_to(ES_ROOT)).relative_to(ROOT)),
            "text": en_translation.get("text"),
        },
        "translation": {
            "language": "es",
            "text": text,
            "philosophy": "optimal-equivalence",
        },
        "source_grounding": {"english_pob_role": "consult_only"},
        "repair_pass": {
            "reason": "legacy_review_yaml_was_malformed",
            "original_file_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "publication_text_preserved": True,
            "footnotes_require_fresh_review": True,
        },
        "status": "spanish_needs_review",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    invalid: list[pathlib.Path] = []
    failures: list[tuple[pathlib.Path, str]] = []
    for path in sorted(ES_ROOT.rglob("*.yaml")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        try:
            yaml.safe_load(raw)
            continue
        except Exception:
            invalid.append(path)
        try:
            record = repaired_record(path, raw)
            if args.apply:
                path.write_text(
                    yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=1000),
                    encoding="utf-8",
                )
        except Exception as exc:  # noqa: BLE001
            failures.append((path, str(exc)))
    print(f"invalid={len(invalid)} repaired={len(invalid) - len(failures)} failures={len(failures)} apply={args.apply}")
    for path, error in failures:
        print(f"FAILED {path.relative_to(ROOT)}: {error}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
