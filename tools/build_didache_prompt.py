#!/usr/bin/env python3
"""build_didache_prompt.py — assemble a Didache chapter translation prompt.

This is the first draft-ready layer for the Phase 13 Group A Greek
pipeline after raw OCR + normalization. It mirrors the spirit of
`tools/build_translation_prompt.py`, but the translation unit here is a
**chapter** rather than a verse.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import didache


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCTRINE_PATH = REPO_ROOT / "DOCTRINE.md"
PHILOSOPHY_PATH = REPO_ROOT / "PHILOSOPHY.md"


@dataclass
class PromptBundle:
    chapter: didache.DidacheChapter
    prompt: str
    source_payload: dict[str, Any]
    zone1_sources_at_draft: list[str]
    zone2_consults_known: list[str]
    source_warnings: list[str]


ZONE2_CONSULTS = [
    "Later Apostolic Fathers critical editions (consult only)",
    "Modern Didache commentary / translation literature (consult only)",
]


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


def build_didache_prompt(chapter_num: int) -> PromptBundle:
    chapter = didache.load_chapter(chapter_num)
    if chapter is None:
        raise LookupError(f"Didache chapter {chapter_num} not found in normalized source layer")

    source_payload = {
        "edition": chapter.source_edition,
        "language": "Greek",
        "text": chapter.text,
        "chapter": chapter.chapter,
        "source_pages": chapter.source_pages,
        "normalization_note": (
            "This chapter comes from the normalized Hitchcock & Brown 1884 OCR layer. "
            "Line-number noise and page segmentation were cleaned, but the translation must stay anchored in the Greek wording."
        ),
    }
    zone1_sources = [
        _snapshot_label("Hitchcock & Brown 1884 (normalized Didache OCR)"),
        _snapshot_label("Schaff 1885 (vendored consult source, not yet OCRed)"),
    ]
    source_warnings: list[str] = []

    prompt = f"""# Chapter

Reference: Didache {chapter.chapter}
ID: DID.{chapter.chapter:02d}
Source pages: {chapter.source_pages}

# Zone 1 primary source

{json.dumps(source_payload, ensure_ascii=False, indent=2)}

# Zone 2 consult registry

{json.dumps(ZONE2_CONSULTS, ensure_ascii=False, indent=2)}

# Source integrity notes

{json.dumps(source_warnings or ['No known source-integrity warnings for this chapter.'], ensure_ascii=False, indent=2)}

# Derivative-work guardrails

- The English output must remain anchored in the Greek chapter text above.
- Do NOT reproduce wording from copyrighted modern English Didache translations.
- You may use later scholarship only as fact-level context, not as phrasing.
- If a clause is uncertain because of OCR normalization or punctuation ambiguity, preserve that uncertainty honestly.

# DOCTRINE.md excerpt

{doctrine_excerpt()}

# PHILOSOPHY.md excerpt

{philosophy_excerpt()}

# Task

Produce the highest-quality draft English translation you can for **Didache chapter {chapter.chapter}**.

Requirements:
- Translate the whole chapter as a coherent literary unit.
- Preserve church-order, liturgical, and moral-imperative language carefully.
- Do not flatten the early-Christian texture into generic modern prose.
- Keep lexical/theological reasoning explicit enough for later audit and revision.
"""

    return PromptBundle(
        chapter=chapter,
        prompt=prompt,
        source_payload=source_payload,
        zone1_sources_at_draft=zone1_sources,
        zone2_consults_known=ZONE2_CONSULTS,
        source_warnings=source_warnings,
    )


def _to_jsonable(bundle: PromptBundle) -> dict[str, Any]:
    return {
        "reference": f"Didache {bundle.chapter.chapter}",
        "id": f"DID.{bundle.chapter.chapter:02d}",
        "prompt": bundle.prompt,
        "source": bundle.source_payload,
        "zone1_sources_at_draft": bundle.zone1_sources_at_draft,
        "zone2_consults_known": bundle.zone2_consults_known,
        "source_warnings": bundle.source_warnings,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", required=True, type=int)
    parser.add_argument("--json", action="store_true", help="Print JSON payload instead of raw prompt")
    args = parser.parse_args()

    bundle = build_didache_prompt(args.chapter)
    if args.json:
        print(json.dumps(_to_jsonable(bundle), ensure_ascii=False, indent=2))
    else:
        print(bundle.prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
