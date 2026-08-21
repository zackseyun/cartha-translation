#!/usr/bin/env python3
"""Audit every published Bible visual-aid placement against its anchor text.

The image catalog is placement-based: one source asset may be valid at its
primary verse and misleading at a reused verse.  This audit therefore joins
every catalog row to the currently published Scripture text, checks reader-copy
and literary-form safeguards, and optionally requires a manual disposition for
every live placement.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from tools.bible_visual_aid_map import CANON_66
except ModuleNotFoundError:  # direct ``python tools/...py`` execution
    from bible_visual_aid_map import CANON_66


FORBIDDEN_READER_COPY = re.compile(
    r"\b(?:diagram lane|map lane|no people|flagged for editorial|"
    r"editorial care|published|generation prompt)\b|\*\*",
    re.IGNORECASE,
)
INTERPRETIVE_COPY = re.compile(
    r"\b(?:parable|compare[sd]?|comparison|metaphor|image|imagery|"
    r"prophetic|vision|physical picture|symbol|warning|nonliteral|schematic|timeline)\b",
    re.IGNORECASE,
)
PARABLE_TEXT = re.compile(r"\bparable\b", re.IGNORECASE)
SIMILE_TEXT = re.compile(
    r"\b(?:I|you|he|she|they|we|the kingdom|the person|the one) "
    r"(?:am|are|is|was|will be|shall be) like\b",
    re.IGNORECASE,
)
VISION_TEXT = re.compile(r"\b(?:vision|visions|I saw|I looked,? and behold)\b", re.IGNORECASE)


def literary_risks(verse_text: str, caption: str) -> list[str]:
    risks: list[str] = []
    if PARABLE_TEXT.search(verse_text) and "parable" not in caption.lower():
        risks.append("parable_not_identified")
    if SIMILE_TEXT.search(verse_text) and not INTERPRETIVE_COPY.search(caption):
        risks.append("comparison_not_identified")
    if VISION_TEXT.search(verse_text) and not INTERPRETIVE_COPY.search(caption):
        risks.append("vision_not_identified")
    return risks


def load_scripture(books_root: Path) -> dict[tuple[str, int, int], str]:
    text: dict[tuple[str, int, int], str] = {}
    for slug, name in CANON_66.items():
        path = books_root / f"{slug}.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_text())
        for chapter in payload.get("chapters", []):
            cnum = int(chapter["chapter"])
            for verse in chapter.get("verses", []):
                text[(name, cnum, int(verse["verse"]))] = str(verse["text"])
    return text


def audit(
    catalog_root: Path,
    books_root: Path,
    ledger_path: Path | None = None,
) -> dict:
    scripture = load_scripture(books_root)
    ledger = {}
    if ledger_path and ledger_path.exists():
        ledger = {row["id"]: row for row in json.loads(ledger_path.read_text())}

    rows = []
    seen_anchors: set[tuple[str, int, int]] = set()
    failures = []
    for path in sorted((catalog_root / "books").glob("*.json")):
        payload = json.loads(path.read_text())
        for entry in payload.get("aids", []):
            anchor = (entry["book"], entry["chapter"], entry["verse_start"])
            if anchor in seen_anchors:
                failures.append({"id": entry["id"], "risk": "verse_anchor_collision"})
            seen_anchors.add(anchor)
            verse_text = " ".join(
                scripture.get((entry["book"], entry["chapter"], verse), "")
                for verse in range(entry["verse_start"], entry["verse_end"] + 1)
            ).strip()
            risks = []
            if not verse_text:
                risks.append("missing_scripture_text")
            if FORBIDDEN_READER_COPY.search(entry.get("caption", "")):
                risks.append("production_language_in_reader_copy")
            risks.extend(literary_risks(verse_text, entry.get("caption", "")))
            disposition = ledger.get(entry["id"])
            if ledger_path and not disposition:
                risks.append("missing_manual_disposition")
            if disposition and disposition.get("disposition") not in {"pass", "corrected"}:
                risks.append("invalid_live_disposition")
            row = {
                "id": entry["id"], "reference": entry["reference"],
                "title": entry["title"], "verse_text": verse_text,
                "caption": entry["caption"], "risks": sorted(set(risks)),
                "manual_disposition": disposition,
            }
            rows.append(row)
            failures.extend({"id": entry["id"], "risk": risk} for risk in row["risks"])
    return {
        "placements": len(rows), "manual_dispositions": len(ledger),
        "failures": failures, "rows": rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog-root", required=True, type=Path)
    ap.add_argument("--books-root", required=True, type=Path)
    ap.add_argument("--ledger", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    result = audit(args.catalog_root, args.books_root, args.ledger)
    if args.out:
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: result[k] for k in ("placements", "manual_dispositions", "failures")}, indent=2))
    return 1 if result["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
