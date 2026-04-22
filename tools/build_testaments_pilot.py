#!/usr/bin/env python3
"""build_testaments_pilot.py — normalize one Testament pilot into chapter files.

This takes a raw OCR page range for a single Testament source witness, extracts
only the BODY block from each page, concatenates the result, and then uses
`tools/testaments_twelve_patriarchs.py` to split the material into chapter
files under:

    sources/testaments_twelve_patriarchs/transcribed/normalized/<slug>/chNN.txt

It is intentionally lightweight and pilot-oriented. The first target is Reuben
from Charles 1908 Greek pages 66-79.
"""
from __future__ import annotations

import argparse
import pathlib
import re
from typing import Iterable

import testaments_twelve_patriarchs as t12p


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "sources" / "testaments_twelve_patriarchs" / "transcribed" / "raw"
NORMALIZED_DIR = REPO_ROOT / "sources" / "testaments_twelve_patriarchs" / "transcribed" / "normalized"


def parse_pages(spec: str) -> list[int]:
    pages: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if end < start:
                raise ValueError(f"Descending page range: {chunk}")
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(chunk))
    return sorted(dict.fromkeys(pages))


def raw_page_file(prefix: str, page: int) -> pathlib.Path:
    return RAW_DIR / f"{prefix}_p{page:04d}.txt"


def build_combined_text(prefix: str, pages: list[int]) -> str:
    chunks: list[str] = []
    missing: list[int] = []
    for page in pages:
        path = raw_page_file(prefix, page)
        if not path.exists():
            missing.append(page)
            continue
        page_text = path.read_text(encoding="utf-8")
        body = t12p.extract_body(page_text)
        if body.strip():
            chunks.append(body.strip())
    if missing:
        raise FileNotFoundError(f"Missing raw OCR files for pages: {missing}")
    return "\n".join(chunks).strip()


def write_chapter_files(
    *,
    testament_slug: str,
    pages: list[int],
    source_label: str,
    prefix: str,
) -> tuple[list[pathlib.Path], list[str]]:
    combined = build_combined_text(prefix, pages)
    chapters, warnings = t12p.parse_testament_text(testament_slug, combined)
    out_paths: list[pathlib.Path] = []
    out_dir = NORMALIZED_DIR / testament_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    for chapter in chapters:
        path = out_dir / f"ch{chapter.chapter:02d}.txt"
        payload = (
            f"# testament: {testament_slug}\n"
            f"# chapter: {chapter.chapter}\n"
            f"# source_pages: {','.join(str(p) for p in pages)}\n"
            f"# source_prefix: {prefix}\n"
            f"# source_edition: {source_label}\n"
            f"# normalization: pilot chapter split from raw OCR; verify against source before drafting full-book production.\n\n"
            f"{chapter.text}\n"
        )
        path.write_text(payload, encoding="utf-8")
        out_paths.append(path)

    return out_paths, warnings


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--testament", required=True, choices=sorted(t12p.TESTAMENT_BY_SLUG))
    parser.add_argument("--pages", required=True, help="Page spec, e.g. 66-79")
    parser.add_argument("--prefix", required=True, help="Raw OCR stem prefix, e.g. t12p_charles1908gk")
    parser.add_argument("--source-label", required=True, help="Human-readable source label")
    args = parser.parse_args(list(argv) if argv is not None else None)

    pages = parse_pages(args.pages)
    out_paths, warnings = write_chapter_files(
        testament_slug=args.testament,
        pages=pages,
        source_label=args.source_label,
        prefix=args.prefix,
    )

    print(f"Wrote {len(out_paths)} chapter file(s) for {args.testament}:")
    for path in out_paths:
        print(f"- {path.relative_to(REPO_ROOT)}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
