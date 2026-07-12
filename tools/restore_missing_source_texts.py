#!/usr/bin/env python3
"""Audit and deterministically restore missing ``source.text`` fields.

The corpus has several intentionally richer source shapes (Coptic normalized
text, page OCR, Ge'ez rows, and derived reader verses).  Reader provenance
pages, however, consume the common ``source.text`` field.  This tool bridges
those already-published source artifacts into that common field without
inventing source-language content or rewriting the rest of each YAML record.

Run without flags to audit.  Pass ``--write`` to apply all recoverable repairs.
"""
from __future__ import annotations

import argparse
import pathlib
import re
from dataclasses import dataclass
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
TRANSLATION_ROOT = ROOT / "translation"
NULL_SCALARS = {"", "''", '""', "null", "~"}
BLOCK_SCALARS = {"|", "|-", "|+", ">", ">-", ">+"}


@dataclass(frozen=True)
class Recovery:
    text: str
    scope: str
    source_row_verse: int | None = None


def source_block(lines: list[str]) -> tuple[int, int, list[str]] | None:
    start = next((i for i, line in enumerate(lines) if line == "source:"), None)
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i] and not lines[i][0].isspace():
            end = i
            break
    return start, end, lines[start + 1 : end]


def has_source_text(path: pathlib.Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    block = source_block(lines)
    if block is None:
        return False
    _, _, body = block
    for index, line in enumerate(body):
        match = re.match(r"^  text:\s*(.*)$", line)
        if not match:
            continue
        scalar = match.group(1).strip()
        if scalar not in NULL_SCALARS and scalar not in BLOCK_SCALARS:
            return True
        if scalar in BLOCK_SCALARS:
            for continuation in body[index + 1 :]:
                if re.match(r"^  [A-Za-z0-9_]+:", continuation):
                    break
                if continuation.strip():
                    return True
        return False
    return False


def load_record(path: pathlib.Path) -> dict[str, Any]:
    record = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(record, dict):
        raise ValueError(f"{path}: YAML root is not a mapping")
    return record


def nonempty(value: Any) -> str:
    return str(value or "").strip()


def page_text(source: dict[str, Any]) -> str:
    pages = source.get("primary_page_texts") or []
    return "\n\n".join(
        nonempty(page.get("text"))
        for page in pages
        if isinstance(page, dict) and nonempty(page.get("text"))
    ).strip()


def row_text(row: dict[str, Any]) -> str:
    for key in ("geez", "greek", "syriac", "source_text", "text"):
        value = nonempty(row.get(key))
        if value:
            return value
    return ""


def combined_rows(source: dict[str, Any]) -> str:
    rows = [row for row in (source.get("rows") or []) if isinstance(row, dict)]
    rendered = []
    for row in rows:
        text = row_text(row)
        if not text:
            continue
        label = row.get("verse")
        rendered.append(f"{label}. {text}" if label is not None else text)
    return "\n".join(rendered).strip()


def parent_path(path: pathlib.Path) -> pathlib.Path | None:
    if not path.parent.name.isdigit():
        return None
    candidate = path.parent.parent / f"{path.parent.name}.yaml"
    return candidate if candidate.exists() else None


def recover_from_parent_rows(
    path: pathlib.Path,
    parent_source: dict[str, Any],
) -> Recovery | None:
    rows = [
        row
        for row in (parent_source.get("rows") or [])
        if isinstance(row, dict) and row_text(row)
    ]
    if not rows:
        return None
    verse = int(path.stem)
    exact = next((row for row in rows if int(row.get("verse") or -1) == verse), None)
    if exact is not None:
        return Recovery(row_text(exact), "source_row", int(exact.get("verse")))

    siblings = sorted(
        child for child in path.parent.glob("*.yaml") if child.stem.isdigit()
    )
    ordered_rows = sorted(rows, key=lambda row: int(row.get("verse") or 0))
    if len(siblings) == len(ordered_rows) and path in siblings:
        mapped = ordered_rows[siblings.index(path)]
        return Recovery(
            row_text(mapped),
            "positionally_aligned_source_row",
            int(mapped.get("verse")),
        )
    return None


def recover(path: pathlib.Path, record: dict[str, Any]) -> Recovery | None:
    source = record.get("source") or {}
    if not isinstance(source, dict):
        return None

    witness = nonempty(source.get("english_witness"))
    if witness:
        return Recovery(witness, "public_domain_english_witness")

    normalized_coptic = nonempty(source.get("coptic_norm"))
    if normalized_coptic:
        return Recovery(normalized_coptic, "normalized_source_language_text")

    coptic_excerpt = nonempty(source.get("approx_ocr_excerpt"))
    if coptic_excerpt:
        return Recovery(coptic_excerpt, "aligned_source_language_ocr_excerpt")

    pages = page_text(source)
    if pages:
        return Recovery(pages, "source_page_ocr_for_editorial_section")

    rows = combined_rows(source)
    if rows:
        return Recovery(rows, "chapter_source_rows")

    parent = parent_path(path)
    if parent is None:
        return None
    parent_record = load_record(parent)
    parent_source = parent_record.get("source") or {}
    if not isinstance(parent_source, dict):
        return None

    row_recovery = recover_from_parent_rows(path, parent_source)
    if row_recovery is not None:
        return row_recovery

    text = nonempty(parent_source.get("text")) or combined_rows(parent_source)
    if not text:
        return None
    book = nonempty(record.get("book"))
    scope = {
        "Shepherd of Hermas": "parent_section_source",
        "2 Baruch": "parent_chapter_bucket_source",
        "1 Clement": "parent_chapter_source",
    }.get(book, "related_parent_record_source")
    return Recovery(text, scope)


def yaml_block(value: str, scope: str, source_row_verse: int | None) -> list[str]:
    lines = ["  text: |-"]
    lines.extend(f"    {line}" if line else "" for line in value.splitlines())
    lines.append(f"  text_scope: {scope}")
    if source_row_verse is not None:
        lines.append(f"  source_row_verse: {source_row_verse}")
    return lines


def write_recovery(path: pathlib.Path, recovery: Recovery) -> None:
    original = path.read_text(encoding="utf-8")
    trailing_newline = original.endswith("\n")
    lines = original.splitlines()
    block = source_block(lines)
    if block is None:
        raise ValueError(f"{path}: missing source mapping")
    start, end, _ = block
    text_index = next(
        (i for i in range(start + 1, end) if re.match(r"^  text:", lines[i])),
        None,
    )
    replacement = yaml_block(
        recovery.text,
        recovery.scope,
        recovery.source_row_verse,
    )
    if text_index is None:
        lines[start + 1 : start + 1] = replacement
    else:
        scalar_end = text_index + 1
        scalar = lines[text_index].split(":", 1)[1].strip()
        if scalar in BLOCK_SCALARS:
            while scalar_end < end and not re.match(
                r"^  [A-Za-z0-9_]+:", lines[scalar_end]
            ):
                scalar_end += 1
        lines[text_index:scalar_end] = replacement
    rendered = "\n".join(lines) + ("\n" if trailing_newline else "")
    path.write_text(rendered, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="apply recoverable repairs")
    args = parser.parse_args()

    paths = sorted(TRANSLATION_ROOT.rglob("*.yaml"))
    missing = [path for path in paths if not has_source_text(path)]
    recoverable: list[tuple[pathlib.Path, Recovery]] = []
    unrecoverable: list[pathlib.Path] = []
    scopes: dict[str, int] = {}
    for path in missing:
        recovery = recover(path, load_record(path))
        if recovery is None or not recovery.text.strip():
            unrecoverable.append(path)
            continue
        recoverable.append((path, recovery))
        scopes[recovery.scope] = scopes.get(recovery.scope, 0) + 1

    if args.write:
        for path, recovery in recoverable:
            write_recovery(path, recovery)

    print(f"records={len(paths)} missing={len(missing)} recoverable={len(recoverable)} unrecoverable={len(unrecoverable)}")
    for scope, count in sorted(scopes.items()):
        print(f"  {scope}: {count}")
    for path in unrecoverable[:50]:
        print(f"UNRECOVERABLE {path.relative_to(ROOT)}")

    if args.write:
        remaining = [path for path in paths if not has_source_text(path)]
        print(f"restored={len(recoverable)} remaining={len(remaining)}")
        return 1 if remaining else 0
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
