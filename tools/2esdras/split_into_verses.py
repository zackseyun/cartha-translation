#!/usr/bin/env python3
"""split_into_verses.py — derive per-verse 2 Esdras YAMLs from chapter YAMLs.

This is a mechanical splitter for 2 Esdras specifically. Unlike the generic
extra-canonical splitter used for Didache / 1 Clement, 2 Esdras already has
explicit verse markers in both the chapter-level Latin source text and the
chapter-level English translation text, so we can split deterministically.
"""
from __future__ import annotations

import pathlib
import re
from typing import Any

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
BOOK_ROOT = REPO_ROOT / 'translation' / 'extra_canonical' / '2_esdras'
BOOK_CODE = '2ES'
BOOK_NAME = '2 Esdras'
VERSE_RE = re.compile(r'(?m)(?<!\S)(\d+)\s')


def parse_verses(text: str) -> dict[int, str]:
    text = text.strip()
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
    return s == str(verse) or s == f'{chapter}:{verse}'


def split_chapter(path: pathlib.Path) -> int:
    doc = yaml.safe_load(path.read_text(encoding='utf-8'))
    chapter = int(doc['source']['chapter'])
    expected = int(doc['source']['verse_count'])
    source_verses = parse_verses(doc['source']['text'])
    translation_verses = parse_verses(doc['translation']['text'])
    expected_set = list(range(1, expected + 1))
    if list(source_verses) != expected_set:
        raise ValueError(f'{path}: source verse sequence mismatch')
    if list(translation_verses) != expected_set:
        raise ValueError(f'{path}: translation verse sequence mismatch')

    out_dir = BOOK_ROOT / f'{chapter:03d}'
    out_dir.mkdir(parents=True, exist_ok=True)
    footnotes = doc['translation'].get('footnotes', []) or []
    written = 0
    for verse in expected_set:
        verse_footnotes = [fn for fn in footnotes if marker_matches(fn.get('marker'), chapter, verse)]
        record: dict[str, Any] = {
            'id': f'{BOOK_CODE}.{chapter}.{verse}',
            'reference': f'{BOOK_NAME} {chapter}:{verse}',
            'unit': 'verse',
            'book': BOOK_NAME,
            'appendix': bool(doc.get('appendix', False)),
            'compositional_layer': doc.get('compositional_layer'),
            'source': {
                'edition': doc['source'].get('edition'),
                'text': source_verses[verse],
                'language': doc['source'].get('language'),
            },
            'translation': {
                'text': translation_verses[verse],
                'philosophy': doc['translation'].get('philosophy'),
            },
            'note': (
                f'Derived mechanically from the chapter-level draft at '
                f'translation/extra_canonical/2_esdras/{chapter:02d}.yaml '
                f'by tools/2esdras/split_into_verses.py. The chapter-level YAML remains '
                f'the authoritative draft/revision record; these verse YAMLs exist for '
                f'reading surfaces, deep links, and per-verse provenance.'
            ),
            'ai_draft_provenance': doc.get('ai_draft', {}),
        }
        if verse_footnotes:
            record['translation']['footnotes'] = verse_footnotes
        out_path = out_dir / f'{verse:03d}.yaml'
        out_path.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False), encoding='utf-8')
        written += 1
    return written


def main() -> int:
    total = 0
    for path in sorted(BOOK_ROOT.glob('[0-9][0-9].yaml')):
        total += split_chapter(path)
        print(f'wrote {path.stem}: {path.stem} -> {total} verses cumulative', flush=True)
    print(f'total verses written: {total}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
