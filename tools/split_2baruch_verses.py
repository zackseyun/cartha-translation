#!/usr/bin/env python3
"""split_2baruch_verses.py

Replace the synthetic single-verse mirror files in 2_baruch/ with proper
per-verse YAML files, one file per verse number found in the chapter text.

The chapter-level flat YAMLs (2_baruch/NNN.yaml) and their current
single-verse mirrors (2_baruch/NNN/001.yaml) have inline verse numbers like:
    1 verse one text
    2 verse two text
This script splits them into 2_baruch/NNN/001.yaml, 002.yaml, etc.

The *mirror* file (NNN/001.yaml) is used as source because revision passes
may have already improved its wording relative to the flat NNN.yaml.

Usage:
  python3 tools/split_2baruch_verses.py --dry-run
  python3 tools/split_2baruch_verses.py
  python3 tools/split_2baruch_verses.py --chapter 1   # single chapter
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from copy import deepcopy

from ruamel.yaml import YAML

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK_DIR = REPO_ROOT / "translation" / "extra_canonical" / "2_baruch"
BOOK_NAME = "2 Baruch"
BOOK_CODE = "2BA"

_VERSE_BOUNDARY = re.compile(r"(?:^|\n+)(\d+)\.?\s+", re.MULTILINE)

_JSON_ENGLISH = re.compile(
    r'"english_text"\s*:\s*"(.*?)(?:"\s*,\s*"(?:translation_philosophy|lexical|notes|'
    r'source|theological))',
    re.DOTALL,
)


def _extract_from_corrupt_json(text: str) -> str | None:
    """Extract english_text from a truncated submit_2baruch_chapter_draft JSON blob."""
    m = _JSON_ENGLISH.search(text)
    if not m:
        return None
    raw = m.group(1)
    # Unescape JSON string escapes
    raw = raw.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
    return raw.strip()


def split_text(text: str, chapter: int = 0) -> list[tuple[int, str]]:
    """Return list of (verse_num, verse_text) by splitting on inline verse numbers."""
    # Handle corrupted JSON drafts first
    if "submit_2baruch_chapter_draft" in text or '"english_text"' in text:
        extracted = _extract_from_corrupt_json(text)
        if extracted:
            text = extracted
    text = text.strip()

    # Strip leading chapter-number header (e.g. "54 The Prayer of Baruch…")
    # — the drafter sometimes emits the chapter number as a label, not a verse number.
    if chapter:
        leading = re.match(rf"^{chapter}\.?\s+", text)
        if leading:
            text = text[leading.end():].strip()

    matches = list(_VERSE_BOUNDARY.finditer(text))
    if not matches:
        return [(1, text)]

    # Build a dict so duplicate verse numbers are resolved with "last wins".
    # Some chapters have duplicate drafts; the final occurrence is authoritative.
    verse_dict: dict[int, str] = {}
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        verse_dict[int(m.group(1))] = text[start:end].strip()

    return sorted(verse_dict.items())
    return verses


def build_verse_record(
    chapter: int,
    verse_num: int,
    verse_text: str,
    source_record: dict,
    is_first: bool,
) -> dict:
    src = deepcopy(source_record.get("source") or {})
    src["verse"] = verse_num
    src.pop("verse_count", None)
    # Only carry full Syriac source text on verse 1 (chapter-level, not per-verse)
    if not is_first:
        src.pop("text", None)
        src.pop("note", None)

    rec: dict = {
        "id": f"{BOOK_CODE}.{chapter}.{verse_num}",
        "reference": f"{BOOK_NAME} {chapter}:{verse_num}",
        "unit": "verse",
        "book": BOOK_NAME,
        "source": src,
        "translation": {
            "text": verse_text,
            "philosophy": (source_record.get("translation") or {}).get("philosophy"),
        },
        "status": source_record.get("status", "ai_draft"),
    }

    # Carry provenance fields only on verse 1
    if is_first:
        for key in ("lexical_decisions", "theological_decisions", "footnotes",
                    "ai_draft", "ai_draft_provenance", "revision_pass", "revisions"):
            if key in source_record:
                rec[key] = source_record[key]

    return rec


def process_chapter(ch: int, dry_run: bool, yaml_rt: YAML) -> int:
    """Return number of verse files written (0 if chapter already split or skipped)."""
    chapter_dir = BOOK_DIR / f"{ch:03d}"
    mirror_path = chapter_dir / "001.yaml"
    if not mirror_path.exists():
        return 0

    raw = mirror_path.read_text(encoding="utf-8")
    record = yaml_rt.load(raw)
    if not isinstance(record, dict):
        return 0

    # Skip chapters that have already been split into multiple verses
    # (identified by lacking the synthetic mirror note AND having correct verse files)
    note = str(record.get("note") or "")
    existing_verse_files = [f for f in chapter_dir.glob("*.yaml")]
    if "Synthetic single-verse mirror" not in note and len(existing_verse_files) > 1:
        return 0

    text = (record.get("translation") or {}).get("text") or ""
    verses = split_text(text.strip(), chapter=ch)

    if dry_run:
        print(f"  ch{ch:03d}: {len(verses)} verses → " +
              ", ".join(f"v{v}" for v, _ in verses))
        return len(verses)

    # Write per-verse files
    written_paths = set()
    for i, (vnum, vtext) in enumerate(verses):
        rec = build_verse_record(ch, vnum, vtext, record, is_first=(i == 0))
        out_path = chapter_dir / f"{vnum:03d}.yaml"
        with out_path.open("w", encoding="utf-8") as fh:
            yaml_rt.dump(rec, fh)
        written_paths.add(out_path)

    # If the split didn't produce a 001.yaml (e.g. chapter starts at v7),
    # remove the stale synthetic mirror.
    old_mirror = chapter_dir / "001.yaml"
    if old_mirror not in written_paths and old_mirror.exists():
        old_mirror.unlink()

    return len(verses)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--chapter", type=int, default=None)
    args = ap.parse_args()

    yaml_rt = YAML()
    yaml_rt.preserve_quotes = True
    yaml_rt.width = 4096

    chapters = [args.chapter] if args.chapter else range(1, 88)
    total_split = already_done = 0

    for ch in chapters:
        n = process_chapter(ch, dry_run=args.dry_run, yaml_rt=yaml_rt)
        if n > 1:
            total_split += 1
        elif n == 1:
            already_done += 1

    label = "would split" if args.dry_run else "split"
    print(f"\n{label}: {total_split} chapters (multi-verse); {already_done} single-verse (skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
