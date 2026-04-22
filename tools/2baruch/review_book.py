#!/usr/bin/env python3
"""review_book.py — generate a whole-book review snapshot for 2 Baruch.

This is a mechanical / source-aware review pass, not a philological final verdict.
It answers the practical question: after drafting every chapter, where are the likely
risk pockets worth reviewing first?
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

import yaml
import importlib.util

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
TRANSLATION_ROOT = REPO_ROOT / 'translation' / 'extra_canonical' / '2_baruch'
RANGE_PATH = REPO_ROOT / 'sources' / '2baruch' / 'syriac' / 'transcribed' / 'ceriani1871' / 'page_chapter_ranges.json'
OUT_JSON = REPO_ROOT / 'sources' / '2baruch' / 'BOOK_REVIEW_2026-04-22.json'
OUT_MD = REPO_ROOT / 'sources' / '2baruch' / 'BOOK_REVIEW_2026-04-22.md'

spec = importlib.util.spec_from_file_location('baruch_multi_witness', REPO_ROOT / 'tools' / '2baruch' / 'multi_witness.py')
multi_witness = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(multi_witness)


@dataclass
class ChapterReview:
    chapter: int
    reference: str
    translation_chars: int
    lexical_decision_count: int
    footnote_count: int
    source_pages: list[int]
    medium_boundary: bool
    has_kmosko_control: bool
    has_ellipsis: bool
    short_translation: bool
    notes: list[str]
    risk_score: int


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def load_ranges() -> list[dict[str, Any]]:
    return json.loads(RANGE_PATH.read_text(encoding='utf-8'))


def load_yaml(chapter: int) -> dict[str, Any]:
    path = TRANSLATION_ROOT / f'{chapter:03d}.yaml'
    return yaml.safe_load(path.read_text(encoding='utf-8')) or {}


def review_chapter(chapter: int, medium_pages: set[int]) -> ChapterReview:
    data = load_yaml(chapter)
    translation = (data.get('translation') or {})
    source = (data.get('source') or {})
    text = str(translation.get('text') or '').strip()
    footnotes = translation.get('footnotes') or []
    lexical = data.get('lexical_decisions') or []
    pages = [int(p) for p in (source.get('pages') or [])]
    bundle = multi_witness.chapter_bundle(chapter)
    usable_kmosko = any(block.get('usable') for block in bundle['secondary']['kmosko1907'])

    notes: list[str] = []
    medium_boundary = any(p in medium_pages for p in pages)
    if medium_boundary:
        notes.append('Touches medium-confidence boundary page(s).')
    has_ellipsis = '...' in text or '…' in text
    if has_ellipsis:
        notes.append('Translation includes ellipsis / explicit incompleteness.')
    short_translation = len(text) < 250
    if short_translation:
        notes.append('Short translation text; verify chapter really is this short.')
    if not usable_kmosko:
        notes.append('No usable Kmosko control page attached to this chapter zone.')

    risk_score = 0
    risk_score += 2 if medium_boundary else 0
    risk_score += 2 if has_ellipsis else 0
    risk_score += 1 if short_translation else 0
    risk_score += 1 if not usable_kmosko else 0

    return ChapterReview(
        chapter=chapter,
        reference=f'2 Baruch {chapter}',
        translation_chars=len(text),
        lexical_decision_count=len(lexical),
        footnote_count=len(footnotes),
        source_pages=pages,
        medium_boundary=medium_boundary,
        has_kmosko_control=usable_kmosko,
        has_ellipsis=has_ellipsis,
        short_translation=short_translation,
        notes=notes,
        risk_score=risk_score,
    )


def build_payload() -> dict[str, Any]:
    ranges = load_ranges()
    medium_pages = {int(r['pdf_page']) for r in ranges if r.get('confidence') == 'medium'}
    reviews = [review_chapter(ch, medium_pages) for ch in range(1, 88)]
    highest = sorted(reviews, key=lambda item: (-item.risk_score, item.chapter))
    payload = {
        'generated_at': utc_stamp(),
        'book': '2 Baruch',
        'chapters_total': 87,
        'chapters_reviewed': len(reviews),
        'medium_boundary_pages': sorted(medium_pages),
        'summary': {
            'drafted_chapters': sum(1 for r in reviews if r.translation_chars > 0),
            'short_translation_chapters': [r.chapter for r in reviews if r.short_translation],
            'ellipsis_chapters': [r.chapter for r in reviews if r.has_ellipsis],
            'medium_boundary_chapters': [r.chapter for r in reviews if r.medium_boundary],
            'no_kmosko_control_chapters': [r.chapter for r in reviews if not r.has_kmosko_control],
            'highest_risk_chapters': [r.chapter for r in highest if r.risk_score >= 3][:20],
        },
        'chapters': [asdict(r) for r in reviews],
    }
    return payload


def write_report(payload: dict[str, Any]) -> None:
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = payload['summary']
    high = summary['highest_risk_chapters']
    lines = [
        '# 2 Baruch — whole-book review snapshot',
        '',
        f"Generated: `{payload['generated_at']}`",
        '',
        '## Summary',
        '',
        f"- Drafted chapters: **{summary['drafted_chapters']} / 87**",
        f"- Chapters touching medium-confidence boundary pages: **{len(summary['medium_boundary_chapters'])}**",
        f"- Chapters with no usable Kmosko control page: **{len(summary['no_kmosko_control_chapters'])}**",
        f"- Chapters with ellipsis / explicit incompleteness: **{len(summary['ellipsis_chapters'])}**",
        f"- Very short chapters flagged for spot-check: **{len(summary['short_translation_chapters'])}**",
        '',
        '## Highest-priority review chapters',
        '',
        ', '.join(str(ch) for ch in high) if high else '_none_',
        '',
        '## Review categories',
        '',
        f"- Medium-boundary chapters: `{summary['medium_boundary_chapters']}`",
        f"- No-Kmosko-control chapters: `{summary['no_kmosko_control_chapters']}`",
        f"- Ellipsis chapters: `{summary['ellipsis_chapters']}`",
        f"- Short chapters: `{summary['short_translation_chapters']}`",
        '',
        '## Conclusion',
        '',
        '2 Baruch is fully drafted at the chapter level. The book is now in a whole-book review state: finish by spot-checking the risk chapters above first, then do a consistency/polish pass over the whole book.',
    ]
    OUT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    payload = build_payload()
    write_report(payload)
    print(json.dumps(payload['summary'], ensure_ascii=False, indent=2))
    print(f'wrote {OUT_JSON.relative_to(REPO_ROOT)}')
    print(f'wrote {OUT_MD.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
