"""
sblgnt.py — Parse the MorphGNT SBLGNT text files.

MorphGNT format: tab-separated, one row per Greek word. Columns:

    BCV    POS   PARSING   TEXT    WORD    NORMALIZED    LEMMA

Where BCV is a 6-digit book-chapter-verse code (book 01-27 for NT books
in canonical order starting with Matthew). See METHODOLOGY.md for full
description.

This module exposes a single entry point, `load_verse`, that returns a
structured representation of a requested verse suitable for feeding into
the drafting prompt.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass, field
from typing import Iterator


# NT book code → (MorphGNT number, directory slug, SBLGNT filename prefix).
# The MorphGNT filename itself is prefix + "-morphgnt.txt" under sources/nt/sblgnt/.
NT_BOOKS: dict[str, tuple[int, str, str]] = {
    "MAT": (1, "matthew", "61-Mt"),
    "MRK": (2, "mark", "62-Mk"),
    "LUK": (3, "luke", "63-Lk"),
    "JHN": (4, "john", "64-Jn"),
    "ACT": (5, "acts", "65-Ac"),
    "ROM": (6, "romans", "66-Ro"),
    "1CO": (7, "1_corinthians", "67-1Co"),
    "2CO": (8, "2_corinthians", "68-2Co"),
    "GAL": (9, "galatians", "69-Ga"),
    "EPH": (10, "ephesians", "70-Eph"),
    "PHP": (11, "philippians", "71-Php"),
    "COL": (12, "colossians", "72-Col"),
    "1TH": (13, "1_thessalonians", "73-1Th"),
    "2TH": (14, "2_thessalonians", "74-2Th"),
    "1TI": (15, "1_timothy", "75-1Ti"),
    "2TI": (16, "2_timothy", "76-2Ti"),
    "TIT": (17, "titus", "77-Tit"),
    "PHM": (18, "philemon", "78-Phm"),
    "HEB": (19, "hebrews", "79-Heb"),
    "JAS": (20, "james", "80-Jas"),
    "1PE": (21, "1_peter", "81-1Pe"),
    "2PE": (22, "2_peter", "82-2Pe"),
    "1JN": (23, "1_john", "83-1Jn"),
    "2JN": (24, "2_john", "84-2Jn"),
    "3JN": (25, "3_john", "85-3Jn"),
    "JUD": (26, "jude", "86-Jud"),
    "REV": (27, "revelation", "87-Re"),
}

# Reverse lookup: human book name → 3-letter code.
BOOK_NAME_TO_CODE: dict[str, str] = {
    "matthew": "MAT", "mark": "MRK", "luke": "LUK", "john": "JHN",
    "acts": "ACT", "romans": "ROM",
    "1 corinthians": "1CO", "2 corinthians": "2CO",
    "galatians": "GAL", "ephesians": "EPH",
    "philippians": "PHP", "colossians": "COL",
    "1 thessalonians": "1TH", "2 thessalonians": "2TH",
    "1 timothy": "1TI", "2 timothy": "2TI",
    "titus": "TIT", "philemon": "PHM",
    "hebrews": "HEB", "james": "JAS",
    "1 peter": "1PE", "2 peter": "2PE",
    "1 john": "1JN", "2 john": "2JN", "3 john": "3JN",
    "jude": "JUD", "revelation": "REV",
}

BOOK_TITLES: dict[str, str] = {
    "MAT": "Matthew",
    "MRK": "Mark",
    "LUK": "Luke",
    "JHN": "John",
    "ACT": "Acts",
    "ROM": "Romans",
    "1CO": "1 Corinthians",
    "2CO": "2 Corinthians",
    "GAL": "Galatians",
    "EPH": "Ephesians",
    "PHP": "Philippians",
    "COL": "Colossians",
    "1TH": "1 Thessalonians",
    "2TH": "2 Thessalonians",
    "1TI": "1 Timothy",
    "2TI": "2 Timothy",
    "TIT": "Titus",
    "PHM": "Philemon",
    "HEB": "Hebrews",
    "JAS": "James",
    "1PE": "1 Peter",
    "2PE": "2 Peter",
    "1JN": "1 John",
    "2JN": "2 John",
    "3JN": "3 John",
    "JUD": "Jude",
    "REV": "Revelation",
}


@dataclass
class Word:
    """A single word in a verse, with MorphGNT morphological annotation."""

    pos: str            # Part of speech code (e.g., "N-", "V-", "P-")
    parsing: str        # Parsing code (e.g., "----NSM-" for nom sg masc)
    text: str           # Greek with punctuation and diacritics
    word: str           # Greek without surrounding punctuation
    normalized: str     # Lowercase, normalized form
    lemma: str          # Dictionary form / lexical entry


@dataclass
class Verse:
    """A parsed SBLGNT verse."""

    book_code: str      # e.g., "PHP"
    book_number: int    # MorphGNT number (1-27)
    chapter: int
    verse: int
    words: list[Word] = field(default_factory=list)

    @property
    def greek_text(self) -> str:
        """Concatenated Greek text of the verse (with punctuation)."""
        return " ".join(w.text for w in self.words).strip()

    @property
    def reference(self) -> str:
        """Human-readable reference, e.g., 'Philippians 1:1'."""
        return f"{BOOK_TITLES[self.book_code]} {self.chapter}:{self.verse}"

    @property
    def book_slug(self) -> str:
        """Directory slug used under translation/nt/."""
        _, slug, _ = NT_BOOKS[self.book_code]
        return slug

    @property
    def canonical_id(self) -> str:
        """Canonical verse ID per schema, e.g., 'PHP.1.1'."""
        return f"{self.book_code}.{self.chapter}.{self.verse}"


def sblgnt_file_for(book_code: str, sources_root: pathlib.Path) -> pathlib.Path:
    """Absolute path to the SBLGNT file for a given NT book."""
    if book_code not in NT_BOOKS:
        raise ValueError(f"Unknown NT book code: {book_code!r}")
    _, _, prefix = NT_BOOKS[book_code]
    return sources_root / "nt" / "sblgnt" / f"{prefix}-morphgnt.txt"


def parse_row(line: str) -> tuple[int, int, int, Word]:
    """Parse a single tab-separated MorphGNT row.

    Returns (book_number, chapter, verse, Word).
    """
    # MorphGNT rows use space separation per the canonical distribution
    # (some mirrors use tab). Accept either; split on whitespace of 2+.
    parts = line.rstrip("\n").split()
    if len(parts) < 7:
        raise ValueError(f"Malformed MorphGNT row (need 7 cols): {line!r}")

    bcv, pos, parsing, text, word, normalized, lemma = parts[:7]
    if len(bcv) != 6 or not bcv.isdigit():
        raise ValueError(f"Malformed BCV code: {bcv!r}")

    book = int(bcv[0:2])
    chapter = int(bcv[2:4])
    verse = int(bcv[4:6])

    return book, chapter, verse, Word(
        pos=pos,
        parsing=parsing,
        text=text,
        word=word,
        normalized=normalized,
        lemma=lemma,
    )


def iter_book_rows(path: pathlib.Path) -> Iterator[tuple[int, int, int, Word]]:
    """Yield every parsed row from a MorphGNT book file."""
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            yield parse_row(line)


def load_verse(
    book_code: str,
    chapter: int,
    verse: int,
    sources_root: pathlib.Path,
) -> Verse:
    """Load a single verse from SBLGNT as a Verse object."""
    path = sblgnt_file_for(book_code, sources_root)
    book_number = NT_BOOKS[book_code][0]

    collected: list[Word] = []
    for b, c, v, word in iter_book_rows(path):
        if b != book_number:
            raise ValueError(
                f"Book number mismatch in {path.name}: expected "
                f"{book_number}, got {b} — check source file integrity."
            )
        if c == chapter and v == verse:
            collected.append(word)

    if not collected:
        raise LookupError(
            f"No words found for {book_code} {chapter}:{verse} in {path.name}"
        )

    return Verse(
        book_code=book_code,
        book_number=book_number,
        chapter=chapter,
        verse=verse,
        words=collected,
    )


def iter_verses(book_code: str, sources_root: pathlib.Path) -> Iterator[Verse]:
    """Yield every verse in an NT book, grouped from the MorphGNT rows."""
    path = sblgnt_file_for(book_code, sources_root)
    book_number = NT_BOOKS[book_code][0]

    current_chapter: int | None = None
    current_verse: int | None = None
    current_words: list[Word] = []

    for b, c, v, word in iter_book_rows(path):
        if b != book_number:
            raise ValueError(
                f"Book number mismatch in {path.name}: expected "
                f"{book_number}, got {b} — check source file integrity."
            )

        if current_chapter is None:
            current_chapter, current_verse = c, v

        if (c, v) != (current_chapter, current_verse):
            yield Verse(
                book_code=book_code,
                book_number=book_number,
                chapter=current_chapter,
                verse=current_verse,
                words=current_words,
            )
            current_chapter, current_verse = c, v
            current_words = []

        current_words.append(word)

    if current_chapter is not None and current_verse is not None:
        yield Verse(
            book_code=book_code,
            book_number=book_number,
            chapter=current_chapter,
            verse=current_verse,
            words=current_words,
        )


def morphology_lines(verse: Verse) -> str:
    """Render the verse's morphology as a plain-text table for the prompt."""
    header = f"# Morphology for {verse.reference}\n# Greek: {verse.greek_text}\n"
    rows = [
        f"  {i+1:2d}. {w.text:<20}  lemma={w.lemma:<15}  "
        f"pos={w.pos}  parsing={w.parsing}"
        for i, w in enumerate(verse.words)
    ]
    return header + "\n".join(rows)
