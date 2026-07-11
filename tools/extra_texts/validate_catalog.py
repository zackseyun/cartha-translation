#!/usr/bin/env python3
"""Validate the shared early-Christian-text catalog and published artifacts."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from catalog import (  # noqa: E402
    CATALOG_PATH,
    REPO_ROOT,
    SUMMARY_CORPORA,
    UNITS,
    load_catalog,
    load_entries,
    load_manifest,
    manifest_path,
)

CATALOG_SCHEMA = REPO_ROOT / "schema" / "early_christian_texts_catalog.schema.json"
SECTION_SCHEMA = REPO_ROOT / "schema" / "extra_canonical_section.schema.json"


def _validator(path: pathlib.Path) -> Draft202012Validator:
    return Draft202012Validator(json.loads(path.read_text(encoding="utf-8")))


def _schema_errors(validator: Draft202012Validator, value: Any, label: str) -> list[str]:
    return [
        f"{label}: {'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def validate_published_entry(
    entry: dict[str, Any], section_validator: Draft202012Validator
) -> list[str]:
    errors: list[str] = []
    text_id = entry["id"]
    try:
        manifest = load_manifest(entry)
    except Exception as exc:
        return [str(exc)]

    if manifest.get("title") != entry["title"]:
        errors.append(f"{text_id}: manifest title does not match catalog")
    if manifest.get("unit") != entry["unit"]:
        errors.append(f"{text_id}: manifest unit does not match catalog")

    manifest_dir = manifest_path(entry).parent
    sections_path = manifest_dir / "sections.json"
    if not sections_path.is_file():
        errors.append(f"{text_id}: missing {sections_path}")
        return errors
    sections = json.loads(sections_path.read_text(encoding="utf-8"))
    expected = manifest.get("expected_units")
    if expected != len(sections):
        errors.append(
            f"{text_id}: expected_units={expected!r}, sections={len(sections)}"
        )

    translation_dir = REPO_ROOT / "translation" / "extra_canonical" / text_id
    files = sorted(translation_dir.glob("*.yaml")) if translation_dir.is_dir() else []
    expected_names = [f"{index:03d}.yaml" for index in range(1, len(files) + 1)]
    actual_names = [path.name for path in files]
    if actual_names != expected_names:
        errors.append(f"{text_id}: YAML units are not contiguous: {actual_names}")
    if expected != len(files):
        errors.append(f"{text_id}: expected_units={expected!r}, YAML files={len(files)}")

    for index, path in enumerate(files, start=1):
        record = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        errors.extend(_schema_errors(section_validator, record, str(path.relative_to(REPO_ROOT))))
        expected_id = f"{entry['code']}.{index:03d}"
        if record.get("id") != expected_id:
            errors.append(f"{text_id}: {path.name} id is not {expected_id}")
        if record.get("book") != entry["title"]:
            errors.append(f"{text_id}: {path.name} book does not match catalog title")
        if record.get("unit") != entry["unit"]:
            errors.append(f"{text_id}: {path.name} unit does not match catalog")
        nav = record.get("reader_navigation") or {}
        if nav.get("authoritative_division") is not False:
            errors.append(f"{text_id}: {path.name} marks editorial navigation authoritative")
        source = record.get("source") or {}
        if not str(source.get("english_witness", "")).strip():
            errors.append(f"{text_id}: {path.name} does not retain its English witness")
        if record.get("source_language_review") != "pending":
            errors.append(f"{text_id}: {path.name} must retain source-language review gate")
        review = record.get("grounding_review") or {}
        if review.get("verdict") not in {"accept", "revise"}:
            errors.append(f"{text_id}: {path.name} has no grounding review verdict")
    return errors


def validate_catalog(catalog_path: pathlib.Path = CATALOG_PATH) -> list[str]:
    errors: list[str] = []
    payload = load_catalog(catalog_path)
    errors.extend(_schema_errors(_validator(CATALOG_SCHEMA), payload, str(catalog_path)))
    try:
        entries = load_entries(catalog_path)
    except Exception as exc:
        return errors + [str(exc)]

    if len(entries) != 25:
        errors.append(f"catalog must contain 25 works; found {len(entries)}")
    for entry in entries:
        if entry.get("summary_corpus") not in SUMMARY_CORPORA:
            errors.append(f"{entry['id']}: unsupported summary_corpus")
        if entry.get("unit") not in UNITS:
            errors.append(f"{entry['id']}: unsupported unit")
        expected_manifest = (
            f"sources/early_christian_texts/{entry['id']}/manifest.json"
        )
        if entry.get("source_manifest") != expected_manifest:
            errors.append(f"{entry['id']}: source_manifest must be {expected_manifest}")

    section_validator = _validator(SECTION_SCHEMA)
    for entry in entries:
        if entry.get("publish") is not True or entry.get("reader_layout") != "flat":
            continue
        errors.extend(validate_published_entry(entry, section_validator))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all",
        action="store_true",
        help="Compatibility flag: validate all catalog rows and all published artifacts.",
    )
    parser.add_argument("--catalog", type=pathlib.Path, default=CATALOG_PATH)
    args = parser.parse_args()
    errors = validate_catalog(args.catalog)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Validated 25 catalog entries and all published catalog artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
