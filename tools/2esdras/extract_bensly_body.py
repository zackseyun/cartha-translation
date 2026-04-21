#!/usr/bin/env python3
"""extract_bensly_body.py — strip BODY sections from Bensly raw OCR.

Input:
  sources/2esdras/raw_ocr/bensly1895/bensly1895_pNNNN.txt

Output:
  sources/2esdras/latin/intermediate/bensly1895_body_pages/pNNNN.txt
  sources/2esdras/latin/intermediate/bensly1895_body_main_text.txt

This is the bridge between:
  1. page-level OCR dumps with apparatus and headers, and
  2. the later cleaned chapter files consumed by latin_bensly.py

It does *not* attempt final verse segmentation. It simply extracts the
main body text page by page and concatenates it into one cleaner Latin
working text for the human / script cleanup pass.
"""
from __future__ import annotations

import pathlib
import re


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
RAW_DIR = REPO_ROOT / "sources" / "2esdras" / "raw_ocr" / "bensly1895"
OUT_DIR = REPO_ROOT / "sources" / "2esdras" / "latin" / "intermediate" / "bensly1895_body_pages"
COMBINED_PATH = REPO_ROOT / "sources" / "2esdras" / "latin" / "intermediate" / "bensly1895_body_main_text.txt"

PAGE_RE = re.compile(r"bensly1895_p(\d{4})\.txt$")


def extract_body(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_body = False
    for line in lines:
        stripped = line.strip()
        if stripped == "[BODY]":
            in_body = True
            continue
        if stripped.startswith("[") and stripped.endswith("]") and stripped != "[BODY]":
            if in_body:
                break
        if in_body:
            out.append(line.rstrip())
    return "\n".join(out).strip()


def iter_raw_pages() -> list[tuple[int, pathlib.Path]]:
    items: list[tuple[int, pathlib.Path]] = []
    if not RAW_DIR.exists():
        return items
    for path in sorted(RAW_DIR.glob("bensly1895_p*.txt")):
        m = PAGE_RE.fullmatch(path.name)
        if not m:
            continue
        items.append((int(m.group(1)), path))
    return items


def main() -> int:
    pages = iter_raw_pages()
    if not pages:
        print(f"no raw OCR pages found in {RAW_DIR}")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    COMBINED_PATH.parent.mkdir(parents=True, exist_ok=True)

    combined_chunks: list[str] = []
    count = 0
    for page_num, path in pages:
        body = extract_body(path.read_text(encoding="utf-8"))
        if not body:
            print(f"warning: no [BODY] section found in {path.name}")
            continue
        out_path = OUT_DIR / f"p{page_num:04d}.txt"
        out_path.write_text(body + "\n", encoding="utf-8")
        combined_chunks.append(f"=== PAGE {page_num} ===\n{body}")
        count += 1

    COMBINED_PATH.write_text("\n\n".join(combined_chunks) + "\n", encoding="utf-8")
    print(f"wrote {count} page body files to {OUT_DIR}")
    print(f"wrote combined body text to {COMBINED_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
