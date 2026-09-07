#!/usr/bin/env python3
"""
export_mobile_bible.py — Export People's Open Bible verse YAMLs into the
mobile app's bundled Bible JSON format.

The mobile app expects a single JSON file shaped like:

{
  "translation": "POB: People's Open Bible (Preview)",
  "books": [
    {
      "name": "Romans",
      "chapters": [
        {
          "chapter": 1,
          "verses": [
            {"verse": 1, "text": "..."}
          ]
        }
      ]
    }
  ]
}

For preview builds we only export chapters that are fully complete in the
translation repo. If a chapter is missing one or more verses, that chapter
and any later chapters in the same book are omitted from the export so the
mobile reader never shows partial chapter content.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import defaultdict
from typing import Any

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import draft  # noqa: E402
import sblgnt  # noqa: E402
import wlc  # noqa: E402
import lxx_swete  # noqa: E402
import terminology_policy  # noqa: E402

try:
    from tools.extra_texts.catalog import flat_export_entries
except ModuleNotFoundError:  # Executed as ``python tools/export_mobile_bible.py``.
    from extra_texts.catalog import flat_export_entries


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANSLATION_ROOT = REPO_ROOT / "translation"

CANONICAL_BOOK_ORDER: list[str] = [
    "GEN", "EXO", "LEV", "NUM", "DEU",
    "JOS", "JDG", "RUT", "1SA", "2SA",
    "1KI", "2KI", "1CH", "2CH", "EZR",
    "NEH", "EST", "JOB", "PSA", "PRO",
    "ECC", "SNG", "ISA", "JER", "LAM",
    "EZK", "DAN", "HOS", "JOL", "AMO",
    "OBA", "JON", "MIC", "NAM", "HAB",
    "ZEP", "HAG", "ZEC", "MAL",
    "MAT", "MRK", "LUK", "JHN", "ACT",
    "ROM", "1CO", "2CO", "GAL", "EPH",
    "PHP", "COL", "1TH", "2TH", "1TI",
    "2TI", "TIT", "PHM", "HEB", "JAS",
    "1PE", "2PE", "1JN", "2JN", "3JN",
    "JUD", "REV",
]

# Deuterocanonical export. Walks `translation/deuterocanon/<slug>/`
# directly so the draft output path and mobile export stay on the same
# internal contract.
APOCRYPHA_ROOT = TRANSLATION_ROOT / "deuterocanon"

APOCRYPHA_BOOK_ORDER: list[str] = [
    "TOB", "JDT", "ESG", "WIS", "SIR", "BAR", "LJE", "PAZ", "SUS", "BEL",
    "1MA", "2MA", "3MA", "4MA", "1ES", "MAN", "PS151",
]

APOCRYPHA_BOOK_TITLES: dict[str, str] = {
    "TOB": "Tobit",
    "JDT": "Judith",
    "ADE": "Greek Esther",
    "ESG": "Additions to Esther",
    "WIS": "Wisdom of Solomon",
    "SIR": "Sirach",
    "BAR": "Baruch",
    "LJE": "Letter of Jeremiah",
    "PAZ": "Prayer of Azariah and Song of the Three",
    "SUS": "Susanna",
    "BEL": "Bel and the Dragon",
    "ADA": "Greek Additions to Daniel",
    "1MA": "1 Maccabees",
    "2MA": "2 Maccabees",
    "3MA": "3 Maccabees",
    "4MA": "4 Maccabees",
    "1ES": "1 Esdras",
    "MAN": "Prayer of Manasseh",
    "PS151": "Psalm 151",
}

APOCRYPHA_BOOK_SLUGS: dict[str, str] = {
    code: meta[4]
    for code, meta in lxx_swete.DEUTEROCANONICAL_BOOKS.items()
}


# Extra-canonical export. Walks `translation/extra_canonical/<slug>/`
# directly. Unlike deuterocanon (verse-level YAMLs), most
# extra-canonical texts are drafted as chapter-level YAMLs -- each
# chapter YAML carries a continuous translation block. Reader exports honor
# explicit witness numbering when present and otherwise use paragraph-sized
# navigation units so readers can select a meaningful portion of the text.
EXTRA_CANONICAL_ROOT = TRANSLATION_ROOT / "extra_canonical"

LEGACY_EXTRA_CANONICAL_BOOK_ORDER: list[str] = [
    "DID",     # Didache
    "1CLEM",   # 1 Clement
    "HERM",    # Shepherd of Hermas
    "ENO",     # 1 Enoch
    "JUB",     # Jubilees
    "2BAR",    # 2 Baruch (Syriac Apocalypse)
    "GOSTR",   # Gospel of Truth
]

LEGACY_EXTRA_CANONICAL_BOOK_TITLES: dict[str, str] = {
    "DID":   "Didache",
    "1CLEM": "1 Clement",
    "HERM":  "Shepherd of Hermas",
    "ENO":   "1 Enoch",
    "JUB":   "Jubilees",
    "2BAR":  "2 Baruch",
    "GOSTR": "Gospel of Truth",
}

LEGACY_EXTRA_CANONICAL_BOOK_SLUGS: dict[str, str] = {
    "DID":   "didache",
    "1CLEM": "1_clement",
    "HERM":  "shepherd_of_hermas",
    "ENO":   "1_enoch",
    "JUB":   "jubilees",
    "2BAR":  "2_baruch",
    "GOSTR": "gospel_of_truth",
}

_CATALOG_FLAT_ENTRIES = flat_export_entries()
EXTRA_CANONICAL_BOOK_ORDER: list[str] = LEGACY_EXTRA_CANONICAL_BOOK_ORDER + [
    entry["code"] for entry in _CATALOG_FLAT_ENTRIES
]
EXTRA_CANONICAL_BOOK_TITLES: dict[str, str] = {
    **LEGACY_EXTRA_CANONICAL_BOOK_TITLES,
    **{entry["code"]: entry["title"] for entry in _CATALOG_FLAT_ENTRIES},
}
EXTRA_CANONICAL_BOOK_SLUGS: dict[str, str] = {
    **LEGACY_EXTRA_CANONICAL_BOOK_SLUGS,
    **{entry["code"]: entry["id"] for entry in _CATALOG_FLAT_ENTRIES},
}

# Extra-canonical books that only have chapter-level YAMLs (single
# text block per chapter) rather than per-verse YAMLs.
#
# Didache, 1 Clement, and Shepherd of Hermas started here, but their
# chapter/section-level drafts have since been split into per-verse YAMLs at
# translation/extra_canonical/<slug>/<NNN>/<VVV>.yaml (via
# tools/split_extra_canonical_into_verses.py for Didache/1 Clement, and
# tools/hermas/split_into_reader_verses.py for Hermas). They are now treated
# as verse-level reader books.
#
# Left in place so future books drafted as pure chapter-level prose can be
# exported through the reader-unit splitter without invoking the source-YAML
# verse splitter. 2 Baruch is intentionally not listed:
# it now has reader-facing per-verse YAMLs under 2_baruch/NNN/VVV.yaml.
EXTRA_CANONICAL_CHAPTER_LEVEL: set[str] = {"GOSTR"} | {
    entry["code"] for entry in _CATALOG_FLAT_ENTRIES
}


def reader_navigation_fields(record: dict[str, Any]) -> dict[str, Any]:
    """Optional export metadata for non-verse editorial divisions.

    Consumers that only understand the existing mobile shape can ignore these
    keys and keep reading `chapter.verses[].text`. Newer website/mobile readers
    can render `heading` while treating it as navigation, not translated text.
    """
    fields: dict[str, Any] = {}
    unit = record.get("unit")
    reference = record.get("reference")
    nav = record.get("reader_navigation")
    if unit:
        fields["unit"] = unit
    if reference:
        fields["reference"] = reference
    if isinstance(nav, dict):
        heading = nav.get("heading")
        if heading:
            fields["heading"] = heading
        fields["reader_navigation"] = nav
    return fields


def _paragraphs(text: str) -> list[str]:
    return [p.strip() for p in str(text or "").splitlines() if p.strip()]


_JESUS_SPEAKER_RE = re.compile(
    r"(?:\[\s*)?(?:Jesus|the Savior|the Saviour|the Lord|the Living One|"
    r"the Holy One|he who is holy)(?:\s*\])?"
    r"[^\n.!?;:”“\"]{0,80}\b"
    r"(?:said|asked|answered|replied|responded|continued|told|cried out|spoke)",
    re.IGNORECASE,
)
_OTHER_SPEAKER_RE = re.compile(
    r"(?:\[\s*)?(?:Judas|Thomas|Mary|Matthew|Peter|Philip|the disciples?|"
    r"his disciples?|they|the apostles?|the child(?: Jesus)?|Joseph|the teacher|"
    r"the priest|the angel)(?:\s*\])?\s+"
    r"(?:then\s+|also\s+|again\s+)?"
    r"(?:said|asked|answered|replied|responded|continued|told|cried out|spoke)",
    re.IGNORECASE,
)


def _quote_range_after(text: str, start: int) -> tuple[int, int, bool] | None:
    """Return the direct quotation following an attribution.

    The extra-canonical witnesses consistently use straight or curly double
    quotation marks for direct speech and single curly marks for quotations
    *inside* a speech.  Keeping the outer delimiter distinction prevents an
    embedded saying from ending Jesus' range early.
    """
    candidates = [(text.find('“', start), '”'), (text.find('"', start), '"')]
    candidates = [(index, closer) for index, closer in candidates if index >= 0]
    if not candidates:
        return None
    quote_start, closer = min(candidates, key=lambda item: item[0])
    quote_end = text.find(closer, quote_start + 1)
    if quote_end < 0:
        return quote_start + 1, len(text), True
    return quote_start + 1, quote_end, False


def _jesus_ranges_for_paragraph(
    text: str,
    *,
    continuing_jesus_speech: bool,
    allow_lord_title: bool = True,
) -> tuple[list[dict[str, int]], bool]:
    """Conservatively identify explicitly attributed Jesus quotations.

    This is an export-time audit aid, not an inference about theology or
    authorship.  It only marks direct speech attributed by the translated text
    itself to Jesus/the Savior/the Lord, plus typographic continuation
    paragraphs in the same open quotation.
    """
    ranges: list[dict[str, int]] = []
    carry = continuing_jesus_speech

    if continuing_jesus_speech:
        stripped_start = len(text) - len(text.lstrip())
        if stripped_start < len(text) and text[stripped_start] in {'“', '"'}:
            closer = '”' if text[stripped_start] == '“' else '"'
            close = text.find(closer, stripped_start + 1)
            end = close if close >= 0 else len(text)
            if end > stripped_start + 1:
                ranges.append({'start': stripped_start + 1, 'end': end})
            carry = close < 0

    attributions: list[tuple[int, bool, re.Match[str]]] = []
    for match in _JESUS_SPEAKER_RE.finditer(text):
        prefix = text[max(0, match.start() - 12):match.start()].lower()
        speaker = match.group(0).lower()
        if prefix.endswith('of ') or prefix.endswith('of the '):
            continue
        if 'lord' in speaker and not allow_lord_title:
            continue
        attributions.append((match.start(), True, match))
    attributions.extend((match.start(), False, match) for match in _OTHER_SPEAKER_RE.finditer(text))
    attributions.sort(key=lambda item: item[0])

    for _, is_jesus, match in attributions:
        quote = _quote_range_after(text, match.end())
        if quote is None:
            if not is_jesus:
                carry = False
            continue
        start, end, remains_open = quote
        # Do not let an attribution claim a quotation that actually belongs to
        # a later speaker attribution in the same paragraph.
        intervening = next((item for item in attributions if match.end() < item[0] < start), None)
        if intervening is not None:
            continue
        if is_jesus and end > start:
            ranges.append({'start': start, 'end': end})
        carry = is_jesus and remains_open

    # Stable, merged ranges keep clients simple and make the exported metadata
    # directly inspectable in tests and CDN snapshots.
    merged: list[dict[str, int]] = []
    for item in sorted(ranges, key=lambda value: (value['start'], value['end'])):
        if merged and item['start'] <= merged[-1]['end']:
            merged[-1]['end'] = max(merged[-1]['end'], item['end'])
        else:
            merged.append(dict(item))
    return merged, carry


def _split_reader_paragraphs(
    text: str,
    *,
    allow_lord_title: bool = True,
) -> list[dict[str, Any]]:
    """Expose editorial prose as numbered paragraph reading units.

    These numbers are modern reader navigation, not claimed ancient verse
    divisions.  Blank-line paragraph boundaries already encode the editors'
    dialogue/narrative structure and are much more usable than one multi-page
    synthetic verse 1.
    """
    paragraphs = _paragraphs(text)
    out: list[dict[str, Any]] = []
    continuing_jesus_speech = False
    for index, paragraph in enumerate(paragraphs, start=1):
        ranges, continuing_jesus_speech = _jesus_ranges_for_paragraph(
            paragraph,
            continuing_jesus_speech=continuing_jesus_speech,
            allow_lord_title=allow_lord_title,
        )
        verse: dict[str, Any] = {
            'verse': index,
            'text': paragraph,
            'is_editorial_section': True,
        }
        if ranges:
            verse['jesus_words'] = ranges
        out.append(verse)
    return out


def _annotate_jesus_words(
    verses: list[dict[str, Any]],
    *,
    allow_lord_title: bool,
) -> list[dict[str, Any]]:
    carry = False
    for verse in verses:
        ranges, carry = _jesus_ranges_for_paragraph(
            str(verse.get('text') or ''),
            continuing_jesus_speech=carry,
            allow_lord_title=allow_lord_title,
        )
        if ranges:
            verse['jesus_words'] = ranges
    return verses


_JESUS_LORD_TITLE_BOOKS = {
    '2CLEM', 'BTHC', 'DSAV', 'GPET', 'PAPI', 'POLY',
}


_MANUSCRIPT_IMAGE_URLS = {
    # Exact public/institutional galleries when a digitized physical witness is
    # available. Nag Hammadi works share the Claremont archive; the exported
    # manuscript name tells readers which codex/tractate to inspect there.
    'THOM': 'https://www.gospels.net/manuscript#the-gospel-of-thomas',
    'GTR': 'https://ccdl.claremont.edu/digital/collection/nha',
    'GOSTR': 'https://ccdl.claremont.edu/digital/collection/nha',
    'GPHIL': 'https://www.gospels.net/manuscript#the-gospel-of-philip',
    'TRES': 'https://ccdl.claremont.edu/digital/collection/nha',
    'APOJ': 'https://ccdl.claremont.edu/digital/collection/nha',
    'HARCH': 'https://ccdl.claremont.edu/digital/collection/nha',
    'ORIGW': 'https://ccdl.claremont.edu/digital/collection/nha',
    'SOJC': 'https://ccdl.claremont.edu/digital/collection/nha',
    'GEGYP': 'https://ccdl.claremont.edu/digital/collection/nha',
    'DSAV': 'https://ccdl.claremont.edu/digital/collection/nha',
    'EXSO': 'https://ccdl.claremont.edu/digital/collection/nha',
    'BTHC': 'https://ccdl.claremont.edu/digital/collection/nha',
    'TRIP': 'https://ccdl.claremont.edu/digital/collection/nha',
    'LPPH': 'https://ccdl.claremont.edu/digital/collection/nha',
    'GJUD': 'https://commons.wikimedia.org/wiki/Codex_Tchacos',
    'GMARY': 'https://www.gospels.net/manuscript#the-gospel-of-mary',
    'GPET': 'https://www.gospels.net/manuscript#the-gospel-of-peter',
    'PROJ': 'https://www.gospels.net/manuscript#the-infancy-gospel-of-james',
    'IGTH': 'https://www.gospels.net/manuscript#the-infancy-gospel-of-thomas',
    '1CLEM': 'https://www.bl.uk/collection/digitised-manuscripts-archives?ref=Royal_MS_1_D_VIII',
    '2CLEM': 'https://www.bl.uk/collection/digitised-manuscripts-archives?ref=Royal_MS_1_D_VIII',
    'HERM': 'https://www.codexsinaiticus.org/en/manuscript.aspx',
    'BARN': 'https://www.codexsinaiticus.org/en/manuscript.aspx',
}
_MANUSCRIPT_THUMBNAIL_URLS = {
    'GJUD': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Codex_Tchacos_p33.jpg?width=960',
}


def _book_source_metadata(book_code: str, records: list[dict[str, Any]]) -> dict[str, Any] | None:
    for record in records:
        source = record.get('source')
        if not isinstance(source, dict):
            continue
        manuscript = str(source.get('manuscript') or '').strip()
        witness_url = str(source.get('witness_url') or '').strip()
        ancient_language = str(source.get('ancient_language') or '').strip()
        images_url = _MANUSCRIPT_IMAGE_URLS.get(book_code, '')
        thumbnail_url = _MANUSCRIPT_THUMBNAIL_URLS.get(book_code, '')
        metadata = {
            key: value
            for key, value in {
                'manuscript': manuscript,
                'ancient_language': ancient_language,
                'source_witness_url': witness_url,
                'manuscript_images_url': images_url,
                'manuscript_thumbnail_url': thumbnail_url,
            }.items()
            if value
        }
        if metadata:
            metadata['division_note'] = (
                'Reader verse numbers follow retained witness paragraph divisions when present; '
                'otherwise they are modern paragraph divisions. They are navigation aids, not '
                'claims about ancient versification.'
            )
            return metadata
    return None


def _split_explicit_chapter_verses(text: str, chapter: int) -> list[dict[str, Any]]:
    """Split legacy chapter blobs whose paragraphs start with ``C:V``.

    Some public-domain witnesses arrive as one chapter YAML even though their
    wording already contains explicit verse boundaries (for example ``1:1``
    and ``1:2``). Emitting that blob as synthetic verse 1 makes readers show a
    duplicate prefix such as ``1 1:1`` and prevents verse-level selection.

    Require at least two increasing markers for the current chapter so prose
    containing an ordinary scripture reference is never split accidentally.
    """
    source = str(text or "")
    matches = list(re.finditer(r"(?:^|\n\s*\n)(\d+):(\d+)\s+", source))
    if len(matches) < 2:
        return []
    if any(int(match.group(1)) != chapter for match in matches):
        return []

    verse_numbers = [int(match.group(2)) for match in matches]
    if verse_numbers[0] != 1 or any(
        current <= previous
        for previous, current in zip(verse_numbers, verse_numbers[1:])
    ):
        return []

    verses: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        body = source[match.end():end].strip()
        if not body:
            return []
        verses.append({"verse": verse_numbers[index], "text": body})
    return verses


_PARENTHETICAL_READER_VERSE_BOOKS = {
    "GPET",
    "IGTH",
    "PROJ",
}

_PARENTHETICAL_READER_VERSE_RE = re.compile(r"(?:^|\s)\((\d+)\)\s+")


def _split_parenthetical_reader_verses(text: str) -> list[dict[str, Any]]:
    """Turn a numbered public-domain witness into selectable reader verses.

    A few early Christian witnesses retain paragraph divisions such as ``(1)``
    and ``(2)`` inside one chapter-sized translation record. The reader already
    paints its own verse number, so keeping those labels in the text duplicates
    the numbering and leaves the whole chapter as one selection target.

    The caller limits this parser to known numbered witnesses. Here we still
    require positive, strictly increasing numbers so a malformed source falls
    back to ordinary paragraph units instead of losing or reordering text.
    Unnumbered prose between two markers remains part of the preceding verse;
    prose before the first marker is preserved at the start of the first verse.
    """
    source = str(text or "")
    matches = list(_PARENTHETICAL_READER_VERSE_RE.finditer(source))
    if not matches:
        return []

    verse_numbers = [int(match.group(1)) for match in matches]
    if any(number < 1 for number in verse_numbers) or any(
        current <= previous
        for previous, current in zip(verse_numbers, verse_numbers[1:])
    ):
        return []

    prefix = source[:matches[0].start()].strip()
    prefix_separator = (
        "\n\n"
        if prefix and "\n" in source[matches[0].start():matches[0].end()]
        else " "
    )
    verses: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        body = source[match.end():end].strip()
        if index == 0 and prefix:
            body = f"{prefix}{prefix_separator}{body}".strip()
        if not body:
            return []
        verses.append({
            "verse": verse_numbers[index],
            "text": body,
            "is_editorial_section": True,
        })
    return verses


def _reader_sections(record: dict[str, Any]) -> list[dict[str, Any]]:
    nav = record.get("reader_navigation")
    raw = record.get("reader_sections")
    if not isinstance(raw, list) and isinstance(nav, dict):
        raw = nav.get("reader_sections")
    if not isinstance(raw, list):
        return []

    out: list[dict[str, Any]] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            continue
        try:
            section = int(item.get("section") or item.get("number") or item.get("order") or index)
            start = int(item.get("paragraph_start") or item.get("paragraphStart") or item.get("start"))
            end = int(item.get("paragraph_end") or item.get("paragraphEnd") or item.get("end") or start)
        except (TypeError, ValueError):
            continue
        title = str(item.get("title") or item.get("heading") or item.get("label") or "").strip()
        if section < 1 or start < 1 or end < start:
            continue
        out.append({"section": section, "start": start, "end": end, "title": title})
    return out


def _split_reader_sections(text: str, sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    paragraphs = _paragraphs(text)
    if not paragraphs or not sections:
        return []

    covered: list[int] = []
    verses: list[dict[str, Any]] = []
    for item in sections:
        start = int(item["start"])
        end = int(item["end"])
        if end > len(paragraphs):
            return []
        body = "\n".join(paragraphs[start - 1:end]).strip()
        if not body:
            return []
        section = int(item["section"])
        title = str(item.get("title") or "").strip()
        covered.extend(range(start, end + 1))
        verse: dict[str, Any] = {
            "verse": section,
            "text": body,
            "section_label": f"§{section}",
            "is_editorial_section": True,
        }
        if title:
            verse["editorial_heading"] = title
            verse["section_heading"] = title
        verses.append(verse)

    if sorted(covered) != list(range(1, len(paragraphs) + 1)):
        return []
    return verses


def book_title(book_code: str) -> str:
    if book_code in sblgnt.BOOK_TITLES:
        return sblgnt.BOOK_TITLES[book_code]
    if book_code in wlc.OT_BOOKS:
        return wlc.OT_BOOKS[book_code][2]
    if book_code in APOCRYPHA_BOOK_TITLES:
        return APOCRYPHA_BOOK_TITLES[book_code]
    raise ValueError(f"Unknown book code: {book_code}")


def expected_chapter_map(book_code: str) -> dict[int, list[int]]:
    """Return {chapter: [verse_numbers...]} covering only verses actually
    present in the critical source text. Source editions (SBLGNT, WLC/UHB)
    legitimately skip verses rejected by textual criticism (e.g. Matt 17:21,
    Matt 23:14), so iterating range(1, last+1) is incorrect — some verse
    numbers simply don't exist."""
    chapter_to_verses: dict[int, list[int]] = {}
    for verse in draft.iter_source_verses(book_code):
        chapter_to_verses.setdefault(verse.chapter, []).append(verse.verse)
    for chapter in chapter_to_verses:
        chapter_to_verses[chapter].sort()
    return chapter_to_verses


def load_translation_record(book_code: str, chapter: int, verse: int) -> dict[str, Any] | None:
    verse_obj = draft.load_source_verse(book_code, chapter, verse)
    path = draft.translation_path_for_verse(verse_obj)
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def reader_footnotes(record: dict[str, Any], text: str) -> list[dict[str, str]]:
    """Carry inline-referenced notes in the existing web/mobile reader shape.

    Archival/background notes without a marker in this text are not reader
    footnotes. Match the publisher's bracket normalization; retain the optional
    reason understood by both clients. Do not reinterpret manuscript brackets
    as notes or change the translation string.
    """
    raw = (record.get('translation') or {}).get('footnotes')
    if not isinstance(raw, list):
        return []
    notes = []
    for note in raw:
        if not isinstance(note, dict) or note.get('text') is None:
            continue
        raw_marker = note.get('marker')
        marker = re.sub(r'^\[|\]$', '', str(raw_marker if raw_marker is not None else '').strip())
        body = str(note['text']).strip()
        if not marker or not body or f'[{marker}]' not in text:
            continue
        exported = {'marker': marker, 'text': body}
        if isinstance(note.get('reason'), str) and note['reason'].strip():
            exported['reason'] = note['reason'].strip()
        notes.append(exported)
    return notes


def _export_record_verse(verse_num: int, record: dict[str, Any]) -> dict[str, Any] | None:
    text = str(((record.get("translation") or {}).get("text", "")) or "").strip()
    if not text:
        return None
    out: dict[str, Any] = {
        "verse": verse_num,
        "text": text,
    }
    notes = reader_footnotes(record, text)
    if notes:
        out['footnotes'] = notes
    if record.get("is_superscription") or verse_num == 0:
        out["is_superscription"] = True
    return out


def export_psalms_book() -> dict[str, Any] | None:
    """Export Psalms from the normalized reader files.

    WLC counts many Psalm superscriptions as source verse 1. POB stores those
    as reader headers in 000.yaml and shifts the body so English verse numbering
    starts at 1. Walking the normalized files prevents mobile exports from
    treating the source-edition verse count as a missing final English verse.
    """
    psalms_dir = TRANSLATION_ROOT / "ot" / "psalms"
    if not psalms_dir.exists():
        return None

    chapters_out: list[dict[str, Any]] = []
    for chapter_dir in sorted(psalms_dir.iterdir(), key=lambda d: int(d.name) if d.name.isdigit() else 999):
        if not chapter_dir.is_dir() or not chapter_dir.name.isdigit():
            continue
        chapter_num = int(chapter_dir.name)
        by_verse: dict[int, dict[str, Any]] = {}
        for verse_file in sorted(chapter_dir.glob("*.yaml")):
            if not verse_file.stem.isdigit():
                continue
            verse_num = int(verse_file.stem)
            record = yaml.safe_load(verse_file.read_text(encoding="utf-8")) or {}
            verse_out = _export_record_verse(verse_num, record)
            if verse_out is not None:
                by_verse[verse_num] = verse_out

        body_nums = sorted(v for v in by_verse if v > 0)
        if not body_nums:
            continue
        if body_nums != list(range(1, body_nums[-1] + 1)):
            continue

        verses_out: list[dict[str, Any]] = []
        if 0 in by_verse:
            verses_out.append(by_verse[0])
        verses_out.extend(by_verse[v] for v in body_nums)
        chapters_out.append({
            "chapter": chapter_num,
            "verses": verses_out,
        })

    if not chapters_out:
        return None

    return {
        "name": book_title("PSA"),
        "chapters": chapters_out,
    }


def export_book(book_code: str) -> dict[str, Any] | None:
    """Include every chapter that is fully drafted. Skip chapters with
    gaps rather than failing fast — a later complete chapter should not
    be withheld just because an earlier one is still being drafted.
    This matches the CDN publisher Lambda's behaviour."""
    if book_code == "PSA":
        return export_psalms_book()

    expected = expected_chapter_map(book_code)
    supplements = reviewed_supplements(book_code, expected)
    for chapter, verse in supplements:
        expected.setdefault(chapter, []).append(verse)
    chapters_out: list[dict[str, Any]] = []

    for chapter in sorted(expected):
        verses_out: list[dict[str, Any]] = []
        chapter_complete = True

        for verse in sorted(expected[chapter]):
            record = supplements.get((chapter, verse))
            if record is None:
                record = load_translation_record(book_code, chapter, verse)
            if record is None:
                chapter_complete = False
                break

            verse_out = _export_record_verse(verse, record)
            if verse_out is None:
                chapter_complete = False
                break

            verses_out.append(verse_out)

        if not chapter_complete:
            continue

        chapters_out.append({
            "chapter": chapter,
            "verses": verses_out,
        })

    if not chapters_out:
        return None

    return {
        "name": book_title(book_code),
        "chapters": chapters_out,
    }


def reviewed_supplements(
    book_code: str, expected: dict[int, list[int]],
) -> dict[tuple[int, int], dict[str, Any]]:
    """Opt-in NT supplements, never inferred from a numbering gap.

    Inclusion is an editorial reader decision, not an assertion that the base
    edition contains the verse or that its historical priority is established.
    Require an explicit per-record decision and a visible textual disclosure.
    Unreviewed records remain excluded; malformed opted-in records fail closed.
    """
    if book_code not in sblgnt.NT_BOOKS:
        return {}
    directory = TRANSLATION_ROOT / "nt" / sblgnt.NT_BOOKS[book_code][1]
    supplements = {}
    for path in sorted(directory.glob("[0-9][0-9][0-9]/[0-9][0-9][0-9].yaml")):
        chapter, verse = int(path.parent.name), int(path.stem)
        if verse in expected.get(chapter, []):
            continue
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or record.get("reader_supplement") is not True:
            continue
        source = record.get("source") or {}
        text = str((record.get("translation") or {}).get("text") or "").strip()
        notes = reader_footnotes(record, text)
        if (
            chapter < 1 or verse < 1
            or record.get("id") != f"{book_code}.{chapter}.{verse}"
            or record.get("textual_status") != "secondary_witness"
            or not isinstance(source, dict)
            or not str(source.get("edition") or "").strip()
            or source.get("edition") == "unverified-supplementary-greek"
            or not str(source.get("text") or "").strip()
            or not text
            or not any(n.get("reason") in {"textual_critical", "textual_variant"} for n in notes)
        ):
            raise ValueError(f"Invalid reader supplement or missing visible textual note: {path}")
        supplements[(chapter, verse)] = record
    return supplements


def export_apocrypha_book(book_code: str) -> dict[str, Any] | None:
    """Walk `translation/deuterocanon/<slug>/<NNN>/<VVV>.yaml` directly.
    Apocrypha books have no SBLGNT/WLC source to validate completeness
    against, so `expected_chapter_map` can't be used. Instead we include
    each chapter whose published verse YAMLs form a contiguous 1..N
    sequence — any gap mid-chapter disqualifies that chapter, but later
    chapters with gaps are still skipped individually (a gap in chapter
    2 doesn't withhold chapter 3). This mirrors the canonical export's
    policy that partial chapters never ship to the reader."""
    slug = APOCRYPHA_BOOK_SLUGS.get(book_code)
    if slug is None:
        return None
    book_dir = APOCRYPHA_ROOT / slug
    if not book_dir.exists():
        return None

    by_chapter: dict[int, dict[int, str]] = defaultdict(dict)
    for chapter_dir in sorted(book_dir.iterdir()):
        if not chapter_dir.is_dir():
            continue
        try:
            chapter_num = int(chapter_dir.name)
        except ValueError:
            continue
        for verse_file in sorted(chapter_dir.glob("*.yaml")):
            try:
                verse_num = int(verse_file.stem)
            except ValueError:
                continue
            record = yaml.safe_load(verse_file.read_text(encoding="utf-8")) or {}
            text = str(((record.get("translation") or {}).get("text", "")) or "").strip()
            if not text:
                continue
            by_chapter[chapter_num][verse_num] = text

    chapters_out: list[dict[str, Any]] = []
    for chapter in sorted(by_chapter):
        verses = by_chapter[chapter]
        verse_nums = sorted(verses)
        if not verse_nums:
            continue
        # Contiguous 1..N required — a missing verse mid-chapter leaves
        # the reader staring at a misnumbered body.
        expected = list(range(1, verse_nums[-1] + 1))
        if verse_nums != expected:
            continue
        chapters_out.append({
            "chapter": chapter,
            "verses": [
                {"verse": verse_num, "text": verses[verse_num]}
                for verse_num in verse_nums
            ],
        })

    if not chapters_out:
        return None

    return {
        "name": APOCRYPHA_BOOK_TITLES[book_code],
        "chapters": chapters_out,
    }


def _enoch_expected_verse_map() -> dict[int, list[int]]:
    """Return the expected per-chapter verse numbers for 1 Enoch.

    This lets the mobile export withhold half-drafted chapters even though 1 Enoch
    is stored directly as verse-level YAMLs.
    """
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    from tools.enoch import verse_parser

    return {
        chapter: verse_parser.recovered_verse_numbers(chapter)
        for chapter in range(1, 109)
    }


def export_extra_canonical_book(book_code: str) -> dict[str, Any] | None:
    """Walk `translation/extra_canonical/<slug>/<NNN>.yaml` for
    chapter-level books (Didache, 1 Clement, etc.), or the nested
    chapter/verse layout for any future verse-level extra-canonical
    books. Chapter-level editorial YAMLs emit their existing blank-line
    paragraphs as numbered reader units. These are explicitly modern
    navigation divisions rather than claims about ancient versification.

    A missing or empty chapter file is skipped; the export is
    complete-chapters-only (same policy as canonical and apocrypha
    exports).
    """
    slug = EXTRA_CANONICAL_BOOK_SLUGS.get(book_code)
    if slug is None:
        return None
    book_dir = EXTRA_CANONICAL_ROOT / slug
    if not book_dir.exists():
        return None

    chapters_out: list[dict[str, Any]] = []
    source_records: list[dict[str, Any]] = []

    if book_code in EXTRA_CANONICAL_CHAPTER_LEVEL:
        # Chapter-level YAMLs: translation/extra_canonical/<slug>/NNN.yaml
        for chapter_file in sorted(book_dir.glob("*.yaml")):
            try:
                chapter_num = int(chapter_file.stem)
            except ValueError:
                continue
            record = yaml.safe_load(chapter_file.read_text(encoding="utf-8")) or {}
            source_records.append(record)
            text = str(((record.get("translation") or {}).get("text", "")) or "").strip()
            if not text:
                continue
            reader_verses = _split_explicit_chapter_verses(text, chapter_num)
            if (
                not reader_verses
                and book_code in _PARENTHETICAL_READER_VERSE_BOOKS
            ):
                reader_verses = _split_parenthetical_reader_verses(text)
            if not reader_verses:
                reader_verses = _split_reader_sections(text, _reader_sections(record))
            if not reader_verses:
                reader_verses = _split_reader_paragraphs(
                    text,
                    allow_lord_title=book_code in _JESUS_LORD_TITLE_BOOKS,
                )
            reader_verses = _annotate_jesus_words(
                reader_verses,
                allow_lord_title=book_code in _JESUS_LORD_TITLE_BOOKS,
            )
            chapter_payload = {
                "chapter": chapter_num,
                "verses": reader_verses,
            }
            chapter_payload.update(reader_navigation_fields(record))
            chapters_out.append(chapter_payload)
    else:
        # Verse-level nested layout: translation/extra_canonical/<slug>/<NNN>/<VVV>.yaml
        by_chapter: dict[int, dict[int, str]] = defaultdict(dict)
        for chapter_dir in sorted(book_dir.iterdir()):
            if not chapter_dir.is_dir():
                continue
            try:
                chapter_num = int(chapter_dir.name)
            except ValueError:
                continue
            for verse_file in sorted(chapter_dir.glob("*.yaml")):
                try:
                    verse_num = int(verse_file.stem)
                except ValueError:
                    continue
                record = yaml.safe_load(verse_file.read_text(encoding="utf-8")) or {}
                source_records.append(record)
                text = str(((record.get("translation") or {}).get("text", "")) or "").strip()
                if not text:
                    continue
                by_chapter[chapter_num][verse_num] = text

        enoch_expected = _enoch_expected_verse_map() if book_code == "ENO" else None
        for chapter in sorted(by_chapter):
            verses = by_chapter[chapter]
            verse_nums = sorted(verses)
            if not verse_nums:
                continue

            if enoch_expected is not None:
                expected = enoch_expected.get(chapter, [])
                if verse_nums != expected:
                    continue
            # Extra-canonical scholarly editions legitimately skip
            # verse numbers in some chapters (e.g. 1 Clement 16's Isaiah
            # 53 quotation, where the Greek source per Funk 1901 simply
            # doesn't carry markers for verses 3 and 9). Unlike the
            # canonical NT/OT where textual criticism is the only reason
            # for gaps, here gaps reflect the source editions' own
            # numbering conventions. We emit what we have and preserve
            # the verse numbers so the reader sees the scholarly numbering
            # even when it skips.
            chapter_verses = [
                {"verse": verse_num, "text": verses[verse_num]}
                for verse_num in verse_nums
            ]
            _annotate_jesus_words(
                chapter_verses,
                allow_lord_title=book_code in _JESUS_LORD_TITLE_BOOKS,
            )
            chapters_out.append({
                "chapter": chapter,
                "verses": chapter_verses,
            })

    if not chapters_out:
        return None

    book_payload = {
        "name": EXTRA_CANONICAL_BOOK_TITLES[book_code],
        "chapters": chapters_out,
    }
    metadata = _book_source_metadata(book_code, source_records)
    if metadata:
        book_payload["metadata"] = metadata
    return book_payload


def export_translation() -> dict[str, Any]:
    books: list[dict[str, Any]] = []
    for book_code in CANONICAL_BOOK_ORDER:
        exported = export_book(book_code)
        if exported is not None:
            books.append(exported)
    # Apocrypha appended after the 66-book canon so every consumer's
    # OT/NT ordering assumption stays intact. Frontends partition these
    # into a dedicated Apocrypha section by book name, so position
    # in this list is purely a sort key.
    for book_code in APOCRYPHA_BOOK_ORDER:
        exported = export_apocrypha_book(book_code)
        if exported is not None:
            books.append(exported)
    # Extra-canonical (Apostolic Fathers etc.) after deuterocanon.
    # Labeled in the reader as a separate "Extra-canonical writings"
    # section by the frontend. First-pass translations only; subject
    # to further review.
    for book_code in EXTRA_CANONICAL_BOOK_ORDER:
        exported = export_extra_canonical_book(book_code)
        if exported is not None:
            books.append(exported)

    payload = {
        "translation": "POB: People's Open Bible (Preview)",
        "books": books,
    }
    return terminology_policy.normalize_reader_payload_in_place(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        required=True,
        help="Where to write the mobile JSON artifact.",
    )
    args = parser.parse_args()

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = export_translation()
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )

    book_count = len(payload["books"])
    chapter_count = sum(len(book["chapters"]) for book in payload["books"])
    verse_count = sum(
        len(chapter["verses"])
        for book in payload["books"]
        for chapter in book["chapters"]
    )
    print(
        f"Wrote {output_path} ({book_count} books, {chapter_count} chapters, {verse_count} verses)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
