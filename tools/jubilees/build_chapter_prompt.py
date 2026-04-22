#!/usr/bin/env python3
"""build_chapter_prompt.py — assemble one Jubilees chapter drafting prompt."""
from __future__ import annotations

import json
import pathlib
import subprocess
from dataclasses import dataclass
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
JUBILEES_ROOT = REPO_ROOT / "sources" / "jubilees"
CORPUS_PATH = JUBILEES_ROOT / "ethiopic" / "corpus" / "JUBILEES.vertex.jsonl"
DOCTRINE_PATH = REPO_ROOT / "DOCTRINE.md"
PHILOSOPHY_PATH = REPO_ROOT / "PHILOSOPHY.md"

from multi_witness import CONSULT_REGISTRY  # noqa: E402


@dataclass
class ChapterPromptBundle:
    chapter: int
    reference: str
    prompt: str
    source_payload: dict[str, Any]
    zone1_sources_at_draft: list[str]
    zone2_consults_known: list[str]
    source_warnings: list[str]


def _git_head_short() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def _snapshot_label(label: str) -> str:
    return f"{label} @{_git_head_short()}"


def _load_excerpt(path: pathlib.Path, keep_sections: set[str]) -> str:
    if not path.exists():
        return f"({path.name} not found)"
    lines = path.read_text(encoding="utf-8").splitlines()
    keeping = False
    out: list[str] = []
    for line in lines:
        if line.startswith("## "):
            keeping = line.strip() in keep_sections
        if keeping:
            out.append(line)
    return "\n".join(out).strip() or f"({path.name} excerpt empty)"


def doctrine_excerpt() -> str:
    return _load_excerpt(
        DOCTRINE_PATH,
        {"## Translation philosophy", "## Contested terms"},
    )


def philosophy_excerpt() -> str:
    return _load_excerpt(
        PHILOSOPHY_PATH,
        {"## What we are translating", '## What "transparent" actually means here'},
    )


def load_chapter_rows(chapter: int) -> list[dict[str, Any]]:
    rows = []
    for line in CORPUS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if obj.get("chapter") == chapter:
            rows.append(obj)
    rows.sort(key=lambda r: (int(r.get("verse", 0)), len(str(r.get("geez", "")))))
    return rows


def build_source_payload(chapter: int) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    rows = load_chapter_rows(chapter)
    if not rows:
        raise FileNotFoundError(f"No Jubilees corpus rows found for chapter {chapter}")

    verse_rows = [r for r in rows if int(r.get("verse", 0)) >= 1]
    source_pages = sorted({p for r in rows for p in (r.get("chapter_source_pages") or [])})
    validations = sorted({str(r.get("validation") or "") for r in rows})
    if any(v in {"vertex_chapter_split", "vertex_targeted_refinement"} for v in validations):
        warnings.append(
            "This chapter includes Verse-extraction rows derived from Vertex-assisted segmentation. "
            "Treat the Ge'ez wording as primary, but keep an eye out for local segmentation oddities."
        )
    return (
        {
            "edition": "charles_1895",
            "language": "Geez",
            "chapter": chapter,
            "verse_count": len(verse_rows),
            "source_pages": source_pages,
            "rows": [
                {"verse": int(r["verse"]), "geez": r["geez"]}
                for r in verse_rows
            ],
            "validation_modes": validations,
        },
        warnings,
    )


JUBILEES_GUARDRAILS = """\
- Translate from the Ge'ez chapter corpus above, not from any existing English translation.
- Preserve Jubilees's calendrical vocabulary carefully: "jubilee", "week of years", "years", "sabbaths of years", etc.
- Preserve the Angel-of-the-Presence / Sinai-revelation framing.
- Do NOT harmonize Jubilees back into Genesis/Exodus when Jubilees expands or differs.
- Keep proper names in conventional readable English forms unless the source clearly demands something else.
- If a verse looks segmentation-uncertain, preserve the best literal sense you can and note the uncertainty in footnotes rather than over-smoothing.
"""


def build_jubilees_chapter_prompt(chapter: int) -> ChapterPromptBundle:
    source_payload, warnings = build_source_payload(chapter)
    reference = f"Jubilees {chapter}"
    zone1_sources = [_snapshot_label("Charles 1895 Ethiopic Jubilees working corpus")]
    zone2_known = [entry["name"] for entry in CONSULT_REGISTRY]

    prompt = f"""# Chapter

Reference: {reference}
ID: JUB.{chapter:03d}
Source edition: Charles 1895 Ethiopic critical edition of Jubilees
Source pages: {source_payload['source_pages']}
Verse rows in working corpus: {source_payload['verse_count']}
Validation modes present: {source_payload['validation_modes']}

# Zone 1 primary source (Ge'ez chapter rows)

{json.dumps(source_payload, ensure_ascii=False, indent=2)}

# Zone 2 consult registry (do not reproduce wording)

{json.dumps(CONSULT_REGISTRY, ensure_ascii=False, indent=2)}

# Source integrity notes

{json.dumps(warnings or ['No known integrity warnings for this chapter.'], ensure_ascii=False, indent=2)}

# Jubilees-specific derivative-work guardrails

{JUBILEES_GUARDRAILS}

# DOCTRINE.md excerpt

{doctrine_excerpt()}

# PHILOSOPHY.md excerpt

{philosophy_excerpt()}

# Task

Produce the highest-quality draft English translation you can for the full chapter of {reference}.

Requirements:
- Translate the whole chapter from the Ge'ez source rows above.
- Preserve verse numbering in the English output. Start each verse on its own line with its verse number, e.g. `1. ...`
- Record major lexical decisions in `lexical_decisions`.
- Record major theological / interpretive decisions in `theological_decisions` when relevant.
- Use `footnotes` for segmentation uncertainty, textual difficulty, or meaningful alternate readings.
- Output format: JSON with keys `english_text`, `translation_philosophy`, `lexical_decisions`, optional `theological_decisions`, optional `footnotes`.
"""
    return ChapterPromptBundle(
        chapter=chapter,
        reference=reference,
        prompt=prompt,
        source_payload=source_payload,
        zone1_sources_at_draft=zone1_sources,
        zone2_consults_known=zone2_known,
        source_warnings=warnings,
    )


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    bundle = build_jubilees_chapter_prompt(args.chapter)
    if args.json:
        print(json.dumps(bundle.__dict__, ensure_ascii=False, indent=2))
    else:
        print(bundle.prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
