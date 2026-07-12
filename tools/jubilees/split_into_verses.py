#!/usr/bin/env python3
"""split_into_verses.py — derive per-verse Jubilees YAMLs from chapter YAMLs.

Also normalizes chapter translation text when it was accidentally stored as a
stringified Python/JSON list of verse strings.
"""
from __future__ import annotations

import ast
import pathlib
import re
from typing import Any

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
BOOK_ROOT = REPO_ROOT / "translation" / "extra_canonical" / "jubilees"
BOOK_CODE = "JUB"
BOOK_NAME = "Jubilees"
VERSE_RE = re.compile(r"(?m)^\s*(\d+)\.\s+")


def normalize_chapter_text(text: str) -> str:
    raw = text.strip()
    if raw.startswith("[") and raw.endswith("]"):
        try:
            data = ast.literal_eval(raw)
            if isinstance(data, list) and all(isinstance(x, str) for x in data):
                return "\n".join(x.strip() for x in data if x.strip())
        except Exception:
            pass
    return raw


def parse_verses(text: str) -> dict[int, str]:
    text = normalize_chapter_text(text)
    matches = list(VERSE_RE.finditer(text))
    out: dict[int, str] = {}
    for i, m in enumerate(matches):
        verse = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[verse] = text[start:end].strip()
    return out


def marker_matches(marker: Any, chapter: int, verse: int) -> bool:
    s = str(marker)
    return s == str(verse) or s == f"{chapter}:{verse}"


def footnote_matches_verse(fn: dict[str, Any], chapter: int, verse: int, verse_text: str) -> bool:
    """Return whether a chapter-level footnote belongs on this verse.

    Legacy Jubilees drafts used verse-reference markers such as ``[12:14]``.
    Normalized reader records use compact labels such as ``[a]``. Supporting
    both keeps this splitter safe to rerun after marker normalization.
    """
    marker = str(fn.get("marker") or "").strip()
    anchor_ref = str(fn.get("anchor_ref") or "").strip()
    return bool(marker) and (
        marker_matches(anchor_ref, chapter, verse)
        or marker_matches(marker, chapter, verse)
        or f"[{marker}]" in verse_text
    )


def ensure_footnote_markers(text: str, footnotes: list[dict[str, Any]]) -> str:
    """Add missing inline markers for verse-level reader exports."""
    out = text
    for fn in footnotes:
        marker = str(fn.get("marker") or "").strip()
        if not marker or f"[{marker}]" in out:
            continue
        for terminator in [", ", ". ", "; "]:
            idx = out.find(terminator)
            if idx > 0:
                out = out[:idx] + f"[{marker}]" + out[idx:]
                break
        else:
            out = out[:-1] + f"[{marker}]." if out.endswith(".") else out + f"[{marker}]"
    return out


def split_chapter(path: pathlib.Path) -> int:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    chapter = int(path.stem)

    source_rows = {
        int(row["verse"]): row
        for row in (doc.get("source", {}).get("rows") or [])
        if isinstance(row, dict) and int(row.get("verse", 0)) >= 1
    }
    translation_text = normalize_chapter_text(str((doc.get("translation") or {}).get("text", "") or ""))
    translation_verses = parse_verses(translation_text)
    if not translation_verses:
        raise ValueError(f"{path}: no verse markers found in translation text")

    ordered_source_rows = [source_rows[key] for key in sorted(source_rows)]
    ordered_translation_verses = sorted(translation_verses)
    chapter_source_text = "\n".join(
        f"{row['verse']}. {row.get('geez', '').strip()}"
        for row in ordered_source_rows
        if str(row.get('geez') or '').strip()
    )

    # Normalize chapter YAML text and publish the source rows through the common
    # source.text provenance field used by reader surfaces.
    doc["translation"]["text"] = translation_text
    doc["source"]["text"] = chapter_source_text
    doc["source"]["text_scope"] = "chapter_source_rows"
    path.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    out_dir = BOOK_ROOT / f"{chapter:03d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    footnotes = (doc.get("translation") or {}).get("footnotes", []) or []
    written = 0
    for verse_num in ordered_translation_verses:
        source_row = source_rows.get(verse_num, {})
        if (
            not str(source_row.get("geez") or "").strip()
            and len(ordered_source_rows) == len(ordered_translation_verses)
        ):
            source_row = ordered_source_rows[ordered_translation_verses.index(verse_num)]
        verse_text = translation_verses[verse_num]
        verse_footnotes = [
            fn for fn in footnotes
            if isinstance(fn, dict) and footnote_matches_verse(fn, chapter, verse_num, verse_text)
        ]
        verse_text = ensure_footnote_markers(verse_text, verse_footnotes)
        record: dict[str, Any] = {
            "id": f"{BOOK_CODE}.{chapter}.{verse_num}",
            "reference": f"{BOOK_NAME} {chapter}:{verse_num}",
            "unit": "verse",
            "book": BOOK_NAME,
            "source": {
                "edition": doc["source"].get("edition"),
                "language": doc["source"].get("language"),
                "text": source_row.get("geez") or chapter_source_text,
                "text_scope": (
                    "source_row"
                    if source_row.get("geez")
                    else "parent_chapter_source_rows"
                ),
                "source_row_verse": source_row.get("verse"),
                "pages": doc["source"].get("pages", []),
                "validation_modes": doc["source"].get("validation_modes", []),
            },
            "translation": {
                "text": verse_text,
                "philosophy": (doc.get("translation") or {}).get("philosophy"),
            },
            "note": (
                f"Derived mechanically from the chapter-level reviewed draft at "
                f"translation/extra_canonical/jubilees/{chapter:03d}.yaml "
                f"by tools/jubilees/split_into_verses.py. The chapter-level YAML remains "
                f"the authoritative draft/review record; these verse YAMLs exist for reader surfaces "
                f"and per-verse linking."
            ),
            "ai_draft_provenance": doc.get("ai_draft", {}),
            "ai_draft_chapter_review_passes": doc.get("review_passes", []),
        }
        if verse_footnotes:
            record["translation"]["footnotes"] = verse_footnotes
        out_path = out_dir / f"{verse_num:03d}.yaml"
        out_path.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False), encoding="utf-8")
        written += 1
    return written


def main() -> int:
    total = 0
    for path in sorted(BOOK_ROOT.glob("[0-9][0-9][0-9].yaml")):
        written = split_chapter(path)
        total += written
        print(f"wrote {path.stem}: {written} verses ({total} cumulative)", flush=True)
    print(f"total verses written: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
