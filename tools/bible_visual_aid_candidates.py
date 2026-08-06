#!/usr/bin/env python3
"""Build an editorial queue of verses that may benefit from a visual aid.

This script does not generate or publish images. It cheaply scans every verse
record, explains why each candidate was selected, and emits a reviewable JSONL
queue. Approved queue rows are intended to be rendered with Codex Image Gen
and then published through the versioned ``/bible-visual-aids/`` CDN catalog.

Policy (docs/BIBLE_VISUAL_AIDS.md): aids show the stage, not the play. A verse
qualifies through the setting, object, route, or practice it assumes — never
through its narrative action, and never through symbolic-vision imagery, so
neither is a scoring signal here.

Example:
    python tools/bible_visual_aid_candidates.py \
      --translation-root translation \
      --out /tmp/bible-visual-aid-candidates.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


@dataclass(frozen=True)
class VisualSignal:
    category: str
    weight: int
    pattern: re.Pattern[str]
    reason: str


def _signal(category: str, weight: int, words: str, reason: str) -> VisualSignal:
    terms = [re.escape(word.strip()) for word in words.split("|") if word.strip()]
    return VisualSignal(
        category=category,
        weight=weight,
        pattern=re.compile(r"\b(?:" + "|".join(terms) + r")\b", re.IGNORECASE),
        reason=reason,
    )


SIGNALS = (
    _signal(
        "architecture",
        3,
        "temple|tabernacle|portico|colonnade|gate|courtyard|court|palace|synagogue|"
        "tower|wall|fortress|house|roof|upper room|tomb|altar|tent|city",
        "A built place or spatial arrangement may be unfamiliar to modern readers.",
    ),
    _signal(
        "geography",
        3,
        "mountain|mount|valley|river|sea|wilderness|desert|island|lake|brook|spring|"
        "Jordan|Jerusalem|Galilee|Judea|Samaria|Egypt|Babylon",
        "Geography or travel context could be clarified by a reconstruction or map.",
    ),
    _signal(
        "material_culture",
        3,
        "denarius|talent|shekel|ephah|cubit|bath|omer|scroll|lampstand|censer|"
        "millstone|winepress|yoke|sling|scepter|seal|phylactery|sandal|loom|"
        "chariot|jar|amphora|mat|sackcloth|armor|breastplate",
        "An ancient object, unit, or practice is easier to understand visually.",
    ),
    _signal(
        "nature",
        2,
        "cedar|fig tree|fig|vineyard|vine|olive tree|mustard seed|lily|hyssop|"
        "locust|camel|lion|eagle|serpent|sheep|goat|dove|raven|fish|storm|"
        "earthquake|rainbow|cloud|fire|hail|dew",
        "A plant, animal, landscape, or natural phenomenon carries concrete meaning.",
    ),
    _signal(
        "diagram",
        3,
        "length|width|height|measured|measurement|dimensions|boundary|tribal allotment|"
        "north side|south side|east side|west side",
        "Measurements or relative positions may be clearer as a diagram.",
    ),
)


def _translation_text(payload: dict) -> str:
    translation = payload.get("translation")
    if isinstance(translation, dict):
        return str(translation.get("text") or "").strip()
    return ""


def _footnote_text(payload: dict) -> tuple[str, bool]:
    translation = payload.get("translation")
    if not isinstance(translation, dict):
        return "", False
    footnotes = translation.get("footnotes") or []
    texts: list[str] = []
    has_cultural_note = False
    for note in footnotes:
        if not isinstance(note, dict):
            continue
        texts.append(str(note.get("text") or ""))
        has_cultural_note = has_cultural_note or note.get("reason") in {
            "cultural_note",
            "historical_context",
            "geographical_note",
        }
    return " ".join(texts), has_cultural_note


def score_verse(payload: dict) -> dict | None:
    """Return an explainable candidate row, or ``None`` below threshold."""
    verse_id = str(payload.get("id") or "").strip()
    reference = str(payload.get("reference") or verse_id).strip()
    verse_text = _translation_text(payload)
    if not verse_id or not verse_text:
        return None

    footnotes, has_cultural_note = _footnote_text(payload)
    searchable = f"{verse_text} {footnotes}"
    category_scores: dict[str, int] = {}
    reasons: list[str] = []
    for signal in SIGNALS:
        matches = signal.pattern.findall(searchable)
        if not matches:
            continue
        # Repeated concrete details increase confidence, but cap each family so
        # a single verbose verse cannot crowd out the rest of the canon.
        contribution = min(signal.weight + len(matches) - 1, signal.weight + 2)
        category_scores[signal.category] = contribution
        reasons.append(signal.reason)

    if has_cultural_note:
        category_scores["cultural_context"] = 3
        reasons.append("The translation record already flags cultural or historical context.")

    if not category_scores:
        return None
    ranked = sorted(category_scores.items(), key=lambda item: (-item[1], item[0]))
    primary_category, primary_score = ranked[0]
    total_score = min(10, primary_score + max(0, len(ranked) - 1))
    if total_score < 3:
        return None

    prompt = (
        f"Annotated reference visual for {reference}; do not depict the events of the "
        f"passage happening — show the {primary_category.replace('_', ' ')} it assumes "
        "as it would appear on an ordinary day. "
        "Style: matte realistic historical-reconstruction painting, natural daylight, "
        "neutral documentary tone; no cinematic lighting, glow, or halo. "
        "People: small anonymous figures for scale only — no identifiable individuals, "
        "no Bible characters, no divine or angelic beings; preserve human dignity. "
        "Annotations: 3-5 short labeled callouts (dark rounded chips, white text, thin "
        "leader lines) naming places, parts, or functions with exact spelling; no other "
        "text or watermark. "
        "Use historically and geographically plausible details and distinguish "
        "reconstruction from certainty."
    )
    return {
        "candidate_id": verse_id.lower().replace(".", "-"),
        "verse_id": verse_id,
        "reference": reference,
        "verse_text": verse_text,
        "category": primary_category,
        "score": total_score,
        "signals": [category for category, _ in ranked],
        "reasons": list(dict.fromkeys(reasons)),
        "status": "needs_editorial_review",
        "suggested_prompt": prompt,
    }


def iter_candidates(root: Path) -> Iterable[dict]:
    for path in sorted(root.rglob("*.yaml")):
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(payload, dict):
            continue
        candidate = score_verse(payload)
        if candidate is None:
            continue
        candidate["source_record"] = path.as_posix()
        yield candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--translation-root", type=Path, default=Path("translation"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--minimum-score", type=int, default=3)
    parser.add_argument("--book", help="Optional canonical book code prefix, e.g. ACT")
    args = parser.parse_args()

    rows = [
        row
        for row in iter_candidates(args.translation_root)
        if row["score"] >= args.minimum_score
        and (not args.book or row["verse_id"].split(".", 1)[0] == args.book.upper())
    ]
    rows.sort(key=lambda row: (-row["score"], row["verse_id"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    print(json.dumps({"candidate_count": len(rows), "output": str(args.out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
