#!/usr/bin/env python3
"""parse_violet_witnesses.py — parse Violet 1910 raw OCR into per-witness blocks.

Violet 1910 vol. 1 presents 4 Ezra with 2-3 parallel columns per page,
each column carrying a different witness (Latin, Syriac, Ethiopic,
Arabic Ewald, Arabic Gildemeister, Armenian, Georgian) either in the
original language (Latin) or in Violet's Latin/German translation
(oriental witnesses). Column headers identify the witness and its
chapter:verse range in the form:

  Lat. Cap. IV 15-18
  Arab. Ew. III 24-28
  Arab. Gild. III 24-28
  Armen. III 24-28

This parser walks the raw OCR files at
  sources/2esdras/raw_ocr/violet1910-vol1/*.txt
extracts per-column witness blocks with their identified verse ranges,
and writes a structured index at
  sources/2esdras/violet_witness_index.json

The output is NOT per-verse yet — it's per-column with the verse range
parsed. Per-verse splitting is a second pass once OCR coverage is
confirmed for the chapter.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
RAW_OCR_DIR = REPO_ROOT / "sources" / "2esdras" / "raw_ocr" / "violet1910-vol1"
OUT_PATH = REPO_ROOT / "sources" / "2esdras" / "violet_witness_index.json"

COLUMN_RE = re.compile(r"^\[COLUMN\s+(\d+)(?::\s*([A-Z]+))?\]\s*$")
HEADER_RUN_RE = re.compile(r"^\[(RUNNING HEAD|INTRODUCTION|APPARATUS|MARGINALIA|BLANK)\]")
# First line after [COLUMN N: LANG] often reads something like
#   "Lat. Cap. IV 15-18"     or
#   "Arab. Ew. III 24-28"    or
#   "Armen. III 24-28"       or
#   "Syr. III 24-28"         or
#   "Aeth. III 24-28"
WITNESS_REF_RE = re.compile(
    r"^(?P<tag>Lat\.|Arab\.\s+Ew\.|Arab\.\s+Gild\.|Armen\.?|Syr\.?|Aeth\.?|Georg\.?|Kopt\.?)\s+"
    r"(?:Cap\.\s+)?"
    r"(?P<ch>[IVXLCDM]+|\d+)\s+"
    r"(?P<vs>\d+)(?:\s*[\-\u2013\u2014]\s*(?P<ve>\d+))?\s*$"
)

WITNESS_TAG_NORMALIZE = {
    "Lat.": "latin",
    "Arab. Ew.": "arabic_ewald",
    "Arab. Gild.": "arabic_gildemeister",
    "Armen.": "armenian",
    "Armen": "armenian",
    "Syr.": "syriac",
    "Syr": "syriac",
    "Aeth.": "ethiopic",
    "Aeth": "ethiopic",
    "Georg.": "georgian",
    "Georg": "georgian",
    "Kopt.": "coptic",
    "Kopt": "coptic",
}

ROMAN_MAP = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}


def roman_to_int(s: str) -> int | None:
    s = s.strip().upper()
    if not s:
        return None
    # if it's already digits, return int
    if s.isdigit():
        return int(s)
    # roman numeral
    try:
        total = 0
        prev = 0
        for ch in reversed(s):
            val = ROMAN_MAP.get(ch)
            if val is None:
                return None
            if val < prev:
                total -= val
            else:
                total += val
                prev = val
        return total
    except Exception:
        return None


@dataclass
class ColumnBlock:
    page: int
    column_index: int
    witness_label: str      # raw label e.g. "ARABIC" or "LATIN"
    witness: str | None     # normalized e.g. "arabic_ewald" / None if unparsable
    chapter: int | None
    verse_start: int | None
    verse_end: int | None
    raw_ref_line: str | None
    text_lines: list[str]

    def text(self) -> str:
        return "\n".join(self.text_lines).strip()

    def verse_range_label(self) -> str:
        if self.chapter is None:
            return "unknown"
        if self.verse_end is None or self.verse_end == self.verse_start:
            return f"{self.chapter}:{self.verse_start}"
        return f"{self.chapter}:{self.verse_start}-{self.verse_end}"


def parse_page(page_path: pathlib.Path, page: int) -> list[ColumnBlock]:
    """Parse one Violet OCR page into a list of column blocks."""
    blocks: list[ColumnBlock] = []
    current: ColumnBlock | None = None
    saw_ref = False

    for raw_line in page_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        # Column header
        m_col = COLUMN_RE.match(line)
        if m_col:
            if current is not None:
                blocks.append(current)
            col_idx = int(m_col.group(1))
            label = (m_col.group(2) or "").upper() or "UNKNOWN"
            current = ColumnBlock(
                page=page,
                column_index=col_idx,
                witness_label=label,
                witness=None,
                chapter=None,
                verse_start=None,
                verse_end=None,
                raw_ref_line=None,
                text_lines=[],
            )
            saw_ref = False
            continue

        # Non-body markers close the current column if any
        m_header_run = HEADER_RUN_RE.match(line)
        if m_header_run:
            if current is not None:
                blocks.append(current)
                current = None
            saw_ref = False
            continue

        # Within a column, the first non-empty line matching the
        # witness-reference pattern sets witness/verse-range.
        if current is not None and not saw_ref and stripped:
            m_ref = WITNESS_REF_RE.match(stripped)
            if m_ref:
                saw_ref = True
                current.raw_ref_line = stripped
                tag = m_ref.group("tag").strip()
                current.witness = WITNESS_TAG_NORMALIZE.get(tag, None)
                ch = roman_to_int(m_ref.group("ch"))
                current.chapter = ch
                current.verse_start = int(m_ref.group("vs"))
                ve = m_ref.group("ve")
                current.verse_end = int(ve) if ve else None
                continue

        # Otherwise, if inside a column, collect as text
        if current is not None:
            current.text_lines.append(line)

    if current is not None:
        blocks.append(current)

    return blocks


def build_index() -> dict[str, Any]:
    if not RAW_OCR_DIR.is_dir():
        raise SystemExit(f"{RAW_OCR_DIR} missing -- run ocr_pipeline.py first")

    pages: list[dict[str, Any]] = []
    all_blocks: list[ColumnBlock] = []
    page_paths = sorted(
        p for p in RAW_OCR_DIR.iterdir()
        if p.is_file() and p.suffix == ".txt" and p.name.startswith("violet1910-vol1_p")
    )
    for p in page_paths:
        m = re.match(r"violet1910-vol1_p(\d{4})\.txt$", p.name)
        if not m:
            continue
        page_num = int(m.group(1))
        blocks = parse_page(p, page_num)
        all_blocks.extend(blocks)
        pages.append({
            "page": page_num,
            "block_count": len(blocks),
            "blocks": [
                {
                    "column_index": b.column_index,
                    "witness_label": b.witness_label,
                    "witness": b.witness,
                    "chapter": b.chapter,
                    "verse_start": b.verse_start,
                    "verse_end": b.verse_end,
                    "raw_ref_line": b.raw_ref_line,
                    "text_chars": len(b.text()),
                    "text_preview": b.text()[:120],
                }
                for b in blocks
            ],
        })

    # Per-chapter per-witness index
    by_chapter: dict[int, dict[str, list[dict[str, Any]]]] = {}
    for b in all_blocks:
        if b.chapter is None or b.witness is None:
            continue
        by_chapter.setdefault(b.chapter, {}).setdefault(b.witness, []).append({
            "page": b.page,
            "column_index": b.column_index,
            "verse_start": b.verse_start,
            "verse_end": b.verse_end,
            "text": b.text(),
        })

    summary = {
        "pages_parsed": len(pages),
        "blocks_total": len(all_blocks),
        "blocks_with_witness_ref": sum(1 for b in all_blocks if b.witness is not None),
        "by_chapter_witness_counts": {
            str(ch): {w: len(rows) for w, rows in ws.items()}
            for ch, ws in sorted(by_chapter.items())
        },
    }

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "sources/2esdras/raw_ocr/violet1910-vol1",
        "summary": summary,
        "pages": pages,
        "by_chapter": {
            str(ch): {w: rows for w, rows in ws.items()}
            for ch, ws in sorted(by_chapter.items())
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args()

    index = build_index()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  pages: {index['summary']['pages_parsed']}")
    print(f"  blocks total: {index['summary']['blocks_total']}")
    print(f"  blocks with witness ref: {index['summary']['blocks_with_witness_ref']}")
    if args.print_summary:
        print("  by chapter/witness:")
        for ch, ws in index["summary"]["by_chapter_witness_counts"].items():
            print(f"    ch {ch}: {ws}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
