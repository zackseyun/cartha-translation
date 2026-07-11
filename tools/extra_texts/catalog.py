"""Shared registry loader for catalog-backed early Christian texts.

The catalog is intentionally data-only.  Translation, status, and export tools
read the same ordered entries so adding a work does not require copying its
code, title, slug, and layout into several Python registries.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Iterable


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "sources" / "early_christian_texts" / "catalog.json"
CATALOG_GROUPS = (
    "nag_hammadi_order",
    "early_christian_apocrypha_order",
    "apostolic_fathers_completion_order",
)
SUMMARY_CORPORA = frozenset(
    {"gnostic", "early_christian_apocrypha", "patristic"}
)
READER_LAYOUTS = frozenset({"flat"})
UNITS = frozenset({"chapter", "editorial_section", "fragment"})


class CatalogError(ValueError):
    """Raised when the shared catalog violates a cross-tool invariant."""


def load_catalog(path: pathlib.Path | str | None = None) -> dict[str, Any]:
    resolved = pathlib.Path(path) if path is not None else CATALOG_PATH
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 2:
        raise CatalogError(
            f"Unsupported early-Christian-text catalog schema: "
            f"{payload.get('schema_version')!r}"
        )
    return payload


def load_entries(path: pathlib.Path | str | None = None) -> list[dict[str, Any]]:
    """Return every catalog entry in reader order, annotated with its group."""
    catalog = load_catalog(path)
    entries: list[dict[str, Any]] = []
    for group in CATALOG_GROUPS:
        rows = catalog.get(group)
        if not isinstance(rows, list):
            raise CatalogError(f"Catalog group {group!r} must be an array")
        for row in rows:
            if not isinstance(row, dict):
                raise CatalogError(f"Catalog group {group!r} contains a non-object")
            entry = dict(row)
            entry["catalog_group"] = group
            entries.append(entry)
    validate_unique_ids_and_codes(entries)
    return entries


def validate_unique_ids_and_codes(
    entries: Iterable[dict[str, Any]] | None = None,
) -> None:
    rows = list(entries) if entries is not None else load_entries()
    for field in ("id", "code", "title"):
        values = [str(row.get(field, "")).strip() for row in rows]
        missing = [index + 1 for index, value in enumerate(values) if not value]
        if missing:
            raise CatalogError(f"Catalog entries missing {field}: {missing}")
        duplicates = sorted({value for value in values if values.count(value) > 1})
        if duplicates:
            raise CatalogError(f"Duplicate catalog {field} values: {duplicates}")


def entry_by_id(text_id: str) -> dict[str, Any]:
    for entry in load_entries():
        if entry["id"] == text_id:
            return entry
    raise KeyError(text_id)


def published_entries() -> list[dict[str, Any]]:
    return [entry for entry in load_entries() if entry.get("publish") is True]


def flat_export_entries() -> list[dict[str, Any]]:
    return [
        entry
        for entry in published_entries()
        if entry.get("reader_layout") == "flat"
    ]


def resolve_repo_path(value: str) -> pathlib.Path:
    path = pathlib.Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def manifest_path(entry: dict[str, Any]) -> pathlib.Path:
    value = str(entry.get("source_manifest", "")).strip()
    if not value:
        raise CatalogError(f"Catalog entry {entry.get('id')!r} has no source_manifest")
    return resolve_repo_path(value)


def load_manifest(entry: dict[str, Any]) -> dict[str, Any]:
    path = manifest_path(entry)
    if not path.is_file():
        raise CatalogError(
            f"Published catalog entry {entry.get('id')!r} is missing {path}"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("text_id") != entry.get("id"):
        raise CatalogError(
            f"Manifest identity mismatch for {entry.get('id')!r}: "
            f"{payload.get('text_id')!r}"
        )
    return payload


def expected_units(entry: dict[str, Any]) -> int:
    value = load_manifest(entry).get("expected_units")
    if not isinstance(value, int) or value < 1:
        raise CatalogError(
            f"Manifest for {entry.get('id')!r} has invalid expected_units: {value!r}"
        )
    return value
