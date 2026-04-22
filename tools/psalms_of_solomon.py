#!/usr/bin/env python3
"""psalms_of_solomon.py — source reader + verse parser for Psalms of Solomon.

Psalms of Solomon is a clean extension of the Phase 8 Swete pipeline: the
Greek text lives in Swete vol 3 pp 788-810, fully transcribed. The book is
not in Codex Vaticanus (Swete's base) but Swete prints it in his appendix.

This module:

  * enumerates the 23 source pages,
  * parses them into 18 chapters of verses,
  * writes the corpus JSONL the LXX drafter consumes.

## Why a dedicated parser (not lxx_swete.parse_pages_to_verses)

PSS has format quirks that aren't present in the main Apocrypha books:

  1. Chapter markers are Greek *keraia-numerals* (``Α΄`` … ``ΙΗ΄``) printed
     on their own line, with inconsistent prime-glyphs — tonos (U+0384),
     modifier prime (U+02B9), acute (U+00B4), or no prime at all — and
     occasional double-labelling (``Χ`` + ``Ἰ´`` for chapter 10).
  2. Verse numbers are often glued directly to the following word
     (``7ἐν τῷ θλίβεσθαι``), not separated by a space.
  3. Each psalm is preceded by an optional subscription/title line
     (``Ψαλμὸς τῷ Σαλωμὼν περὶ Ἰερουσαλήμ.``).
  4. A ``Γʹ`` chapter marker can appear as a running-footer artefact at
     the *top* of a page that still belongs to the previous chapter;
     real chapter boundaries are followed by verse 1, spurious ones by
     a mid-chapter verse number.
"""
from __future__ import annotations

import json
import pathlib
import re
import unicodedata
from dataclasses import dataclass
from typing import Iterator

import lxx_swete


BOOK_CODE = "PSS"
TITLE = "Psalms of Solomon"
SLUG = "psalms_of_solomon"
SWETE_VOL = 3
FIRST_PAGE = 788
LAST_PAGE = 810
CHAPTER_COUNT = 18
SOURCE_EDITION = "swete_1909_vol3"

TRANSCRIBED_DIR = pathlib.Path(lxx_swete.TRANSCRIBED_DIR)
CORPUS_PATH = lxx_swete.FINAL_CORPUS_DIR / f"{BOOK_CODE}.jsonl"


# --- chapter-header parsing ------------------------------------------------

_PRIME_CHARS = {
    "\u0374",  # GREEK NUMERAL SIGN (keraia) — strict form
    "\u0384",  # GREEK TONOS — what Swete actually prints for ``Α΄``, ``Β΄`` …
    "\u02B9",  # MODIFIER LETTER PRIME — e.g. "Γʹ"
    "\u00B4",  # ACUTE ACCENT — e.g. "Δ´"
    "'",
    "\u2032",  # PRIME
}

# Milesian Greek numerals. We only need 1-19 for PSS chapters. Both
# uppercase and lowercase forms are allowed because Swete is inconsistent
# (e.g. "Α΄" but also "ϛ´" and "ζ´").
_MILESIAN = {
    "Α": 1, "α": 1,
    "Β": 2, "β": 2,
    "Γ": 3, "γ": 3,
    "Δ": 4, "δ": 4,
    "Ε": 5, "ε": 5,
    "Ϛ": 6, "ϛ": 6, "Ϝ": 6, "ϝ": 6, "ς": 6,
    "Ζ": 7, "ζ": 7,
    "Η": 8, "η": 8,
    "Θ": 9, "θ": 9,
    "Ι": 10, "ι": 10,
    "Κ": 20, "κ": 20,
}

_ROMAN_CHARS = r"IVXΙΧ"
_ROMAN_ONLY_RE = re.compile(rf"^[{_ROMAN_CHARS}]+\.?$")
_ROMAN_PREFIX_RE = re.compile(rf"^[{_ROMAN_CHARS}]+\s+")

# Bare Chi is ambiguous on its own; authoritative chapter-10 is Ἰ´ on the
# next line.
_STANDALONE_CHI_RE = re.compile(r"^Χ\.?$")


def _strip_primes(s: str) -> str:
    s = s.strip()
    while s and (s[-1] in _PRIME_CHARS or s[-1] in ".,"):
        s = s[:-1]
    return s.strip()


def _strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")


def parse_chapter_header(line: str) -> int | None:
    """Return the Milesian numeric value of a chapter-header line.

    Handles all variants Swete prints: ``Α΄``, ``Γʹ``, ``Δ´``, ``ϛ´``,
    ``ζ´``, ``Ἰ´``, ``ΙΑ´`` … ``ΙΗ´``, trailing-period noise, and prime-
    less ``ΙΔ``. Returns None for non-header lines.
    """
    s = line.strip()
    if not s or _STANDALONE_CHI_RE.match(s):
        return None

    stripped = _strip_primes(s)
    if not stripped or len(stripped) > 3:
        return None

    normalized = _strip_diacritics(stripped)
    if not all(ch in _MILESIAN for ch in normalized):
        return None

    total = sum(_MILESIAN[ch] for ch in normalized)
    if 1 <= total <= CHAPTER_COUNT:
        return total
    return None


# --- body cleaning + verse scanning ---------------------------------------

_GREEK_CHAR = r"[\u0370-\u03FF\u1F00-\u1FFF]"
_VERSE_MARKER_RE = re.compile(
    rf"(?<![0-9])(?P<num>\d+)\s*(?P<word>{_GREEK_CHAR}[^\s]*)"
)
_HYPHEN_LINEBREAK_RE = re.compile(rf"({_GREEK_CHAR})[-‐]\s+({_GREEK_CHAR})")
_PILCROW_RE = re.compile(r"¶\s*")


_GREEK_SIGLUM_PREFIX_RE = re.compile(r"^[Α-Ωα-ω]\s+(?=\d)")


def _strip_line_prefix(s: str) -> str:
    """Drop leading noise that commonly precedes a PSS verse marker:
      * Β siglum (``Β 1 Κύριε …``)
      * single-Greek-letter siglum before a digit (``γ 39κατάξει …``)
      * Roman-numeral chapter-restatement (``I 1 ἘΒΟΗΣΑ …``, ``ΧΙΙ 1 …``)
    """
    s = s.strip()
    if s.startswith("Β "):
        s = s[2:].strip()
    s = _GREEK_SIGLUM_PREFIX_RE.sub("", s, count=1)
    s = _ROMAN_PREFIX_RE.sub("", s, count=1)
    return s


def _extract_verse_marker(line: str) -> tuple[int, str] | None:
    """If ``line`` starts with a verse marker, return (verse_num, rest).
    Tolerates leading Β / single-letter / Roman sigla and verse numbers
    glued directly to the next word (``7ἐν τῷ θλίβεσθαι``)."""
    s = _strip_line_prefix(line)
    m = _VERSE_MARKER_RE.match(s)
    if not m:
        return None
    return int(m.group("num")), s[m.start("word"):].strip()


def _iter_inline_verse_markers(line: str) -> Iterator[tuple[int, int, int]]:
    """Yield (match_start, verse_num, match_end) for every verse marker
    found anywhere in ``line``. Used for inline verse transitions like
    ``…δικαιοσύνῃ 26ἐξῶσαι …`` where a marker starts mid-line."""
    for m in _VERSE_MARKER_RE.finditer(line):
        yield m.start(), int(m.group("num")), m.start("word")


@dataclass(frozen=True)
class SwetePage:
    scan_page: int
    running_head: str
    body_text: str
    path: pathlib.Path


@dataclass
class PSSVerse:
    chapter: int
    verse: int
    greek: str
    source_pages: list[int]
    title_hint: str | None = None


_RUNNING_HEAD_RE = re.compile(
    r"\[RUNNING HEAD\]\s*\n(.*?)\n\[BODY\]", re.DOTALL
)


def page_path(scan_page: int) -> pathlib.Path:
    return TRANSCRIBED_DIR / f"vol{SWETE_VOL}_p{scan_page:04d}.txt"


def extract_running_head(page_text: str) -> str:
    m = _RUNNING_HEAD_RE.search(page_text)
    return m.group(1).strip() if m else ""


def iter_pages() -> Iterator[SwetePage]:
    for scan_page in range(FIRST_PAGE, LAST_PAGE + 1):
        path = page_path(scan_page)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        yield SwetePage(
            scan_page=scan_page,
            running_head=extract_running_head(text),
            body_text=lxx_swete.extract_body(text),
            path=path,
        )


def transcribed_pages() -> list[int]:
    return [page.scan_page for page in iter_pages()]


def missing_pages() -> list[int]:
    present = set(transcribed_pages())
    return [pg for pg in range(FIRST_PAGE, LAST_PAGE + 1) if pg not in present]


def is_transcription_complete() -> bool:
    return not missing_pages()


# --- parser ----------------------------------------------------------------


def _collect_lines() -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for page in iter_pages():
        for ln in page.body_text.splitlines():
            cleaned = _PILCROW_RE.sub("", ln).rstrip()
            out.append((page.scan_page, cleaned))
        out.append((page.scan_page, ""))  # page separator
    return out


def _peek_first_verse_num(
    lines: list[tuple[int, str]], start: int
) -> int | None:
    """Scan forward from `start` for the first verse marker, skipping
    blanks, Roman-numeral restatements, and psalm subscriptions. Stops at
    another chapter header. Returns the verse number or None."""
    for i in range(start, min(start + 10, len(lines))):
        s = lines[i][1].strip()
        if not s:
            continue
        if parse_chapter_header(s) is not None:
            return None
        marker = _extract_verse_marker(s)
        if marker is not None:
            return marker[0]
    return None


def iter_verses() -> Iterator[PSSVerse]:
    """Parse all 18 chapters of Psalms of Solomon into verse records."""
    lines = _collect_lines()

    chapter: int = 1
    verse: int | None = None
    text_parts: list[str] = []
    pages_for_verse: list[int] = []
    title_hint: str | None = None
    pending_title: str | None = None
    awaiting_first_verse = True

    def flush() -> PSSVerse | None:
        nonlocal text_parts, pages_for_verse, title_hint
        if verse is None or not text_parts:
            return None
        raw = " ".join(text_parts).strip()
        raw = _HYPHEN_LINEBREAK_RE.sub(r"\1\2", raw)
        raw = re.sub(r"\s+([·,.;])", r"\1", raw)
        raw = re.sub(r"\s+", " ", raw).strip()
        out = PSSVerse(
            chapter=chapter,
            verse=verse,
            greek=raw,
            source_pages=sorted(set(pages_for_verse)),
            title_hint=title_hint,
        )
        text_parts = []
        pages_for_verse = []
        title_hint = None
        return out

    for idx, (scan_page, line) in enumerate(lines):
        s = line.strip()
        if not s:
            continue

        # (1) Chapter header? Validate via peek for an upcoming verse 1 / 2.
        ch = parse_chapter_header(s)
        if ch is not None:
            ahead = _peek_first_verse_num(lines, idx + 1)
            if ahead is not None and ahead <= 2:
                v = flush()
                if v:
                    yield v
                chapter = ch
                verse = None
                pending_title = None
                awaiting_first_verse = True
                continue
            continue  # spurious running-footer artefact

        # (2) Bare Chi (Roman-X synonym). Ἰ´ lands on the next line.
        if _STANDALONE_CHI_RE.match(s):
            continue

        # (3) Verse marker at line start (possibly with Roman/siglum prefix).
        marker = _extract_verse_marker(s)
        if marker is not None:
            num, tail = marker

            def advance(new_num: int, new_tail: str) -> PSSVerse | None:
                """Start a new verse with text ``new_tail``. Returns the
                yielded-out previous verse, if any."""
                nonlocal verse, text_parts, pages_for_verse, title_hint
                nonlocal pending_title, awaiting_first_verse
                emitted = flush()
                verse = new_num
                text_parts = [new_tail] if new_tail else []
                pages_for_verse = [scan_page]
                if pending_title and new_num == 1:
                    title_hint = pending_title
                pending_title = None
                awaiting_first_verse = False
                return emitted

            if verse is None or num == 1 or num < verse:
                # Chapter-boundary / initial verse / verse restart.
                v = advance(num, tail)
                if v:
                    yield v
                continue

            if num > verse and num - verse <= 30:
                # Normal forward progression — including small editorial
                # gaps like PSS 17:3 → 17:5.
                v = advance(num, tail)
                if v:
                    yield v
                continue

            # Huge jump (> 30) or num == verse → probably a marginal
            # line-number leak. Fold into current verse's continuation.
            if verse is not None:
                text_parts.append(s)
                if scan_page not in pages_for_verse:
                    pages_for_verse.append(scan_page)
            continue

        # (4) Pre-verse noise inside a chapter.
        if awaiting_first_verse:
            if not _ROMAN_ONLY_RE.match(s) and not _STANDALONE_CHI_RE.match(s):
                pending_title = s
            continue

        # (5) Continuation line — but watch for inline mid-line verse
        # markers ("…δικαιοσύνῃ 26ἐξῶσαι …"). Split the line at every
        # legitimate verse-marker boundary.
        if verse is None:
            continue
        cursor = 0
        for m_start, m_num, word_start in _iter_inline_verse_markers(s):
            if m_start == 0:
                # Handled in branch (3) above; we shouldn't get here.
                break
            if m_num <= verse or m_num - verse > 30:
                continue  # not a legitimate inline transition
            # Everything before the marker belongs to the current verse.
            pre = s[cursor:m_start].strip()
            if pre:
                text_parts.append(pre)
                if scan_page not in pages_for_verse:
                    pages_for_verse.append(scan_page)
            v = flush()
            if v:
                yield v
            verse = m_num
            text_parts = []
            pages_for_verse = [scan_page]
            cursor = word_start
        # Remaining tail after the last inline marker (or the whole line).
        tail_text = s[cursor:].strip()
        if tail_text:
            text_parts.append(tail_text)
            if scan_page not in pages_for_verse:
                pages_for_verse.append(scan_page)

    v = flush()
    if v:
        yield v


# --- corpus writer ---------------------------------------------------------


def build_corpus(path: pathlib.Path | None = None) -> pathlib.Path:
    """Write PSS.jsonl in the LXX drafter corpus format."""
    target = path or CORPUS_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    verses = list(iter_verses())
    with target.open("w", encoding="utf-8") as fh:
        for v in verses:
            record = {
                "book": BOOK_CODE,
                "chapter": v.chapter,
                "verse": v.verse,
                "greek": v.greek,
                "source": "Swete 1909 vol 3 (Psalms of Solomon appendix)",
                "source_pages": v.source_pages,
                "source_edition": SOURCE_EDITION,
                "validation": "swete_direct",
            }
            if v.title_hint:
                record["psalm_title"] = v.title_hint
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return target


def summary() -> dict:
    pages = list(iter_pages())
    verses = list(iter_verses())
    per_chapter: dict[int, int] = {}
    for v in verses:
        per_chapter[v.chapter] = per_chapter.get(v.chapter, 0) + 1
    return {
        "book_code": BOOK_CODE,
        "title": TITLE,
        "slug": SLUG,
        "swete_volume": SWETE_VOL,
        "scan_page_range": f"{FIRST_PAGE}-{LAST_PAGE}",
        "chapter_count": CHAPTER_COUNT,
        "transcribed_pages_present": [p.scan_page for p in pages],
        "missing_pages": missing_pages(),
        "transcription_complete": is_transcription_complete(),
        "parsed_verse_count": len(verses),
        "verses_per_chapter": per_chapter,
    }


if __name__ == "__main__":
    import pprint
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "build":
        path = build_corpus()
        print(f"wrote {path}")
        pprint.pp(summary())
    else:
        pprint.pp(summary())
