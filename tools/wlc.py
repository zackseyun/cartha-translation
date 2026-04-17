"""
wlc.py — Parse Westminster Leningrad Codex / OSHB OSIS XML files.

This mirrors the NT `tools/sblgnt.py` module closely enough for the OT
pipeline to reuse the same prompting and validation strategy later.
"""

from __future__ import annotations

import functools
import pathlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Iterator


OSIS_NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}

OT_BOOKS: dict[str, tuple[str, str, str, str]] = {
    "GEN": ("Gen", "genesis", "Genesis", "Gen.xml"),
    "EXO": ("Exod", "exodus", "Exodus", "Exod.xml"),
    "LEV": ("Lev", "leviticus", "Leviticus", "Lev.xml"),
    "NUM": ("Num", "numbers", "Numbers", "Num.xml"),
    "DEU": ("Deut", "deuteronomy", "Deuteronomy", "Deut.xml"),
    "JOS": ("Josh", "joshua", "Joshua", "Josh.xml"),
    "JDG": ("Judg", "judges", "Judges", "Judg.xml"),
    "RUT": ("Ruth", "ruth", "Ruth", "Ruth.xml"),
    "1SA": ("1Sam", "1_samuel", "1 Samuel", "1Sam.xml"),
    "2SA": ("2Sam", "2_samuel", "2 Samuel", "2Sam.xml"),
    "1KI": ("1Kgs", "1_kings", "1 Kings", "1Kgs.xml"),
    "2KI": ("2Kgs", "2_kings", "2 Kings", "2Kgs.xml"),
    "1CH": ("1Chr", "1_chronicles", "1 Chronicles", "1Chr.xml"),
    "2CH": ("2Chr", "2_chronicles", "2 Chronicles", "2Chr.xml"),
    "EZR": ("Ezra", "ezra", "Ezra", "Ezra.xml"),
    "NEH": ("Neh", "nehemiah", "Nehemiah", "Neh.xml"),
    "EST": ("Esth", "esther", "Esther", "Esth.xml"),
    "JOB": ("Job", "job", "Job", "Job.xml"),
    "PSA": ("Ps", "psalms", "Psalms", "Ps.xml"),
    "PRO": ("Prov", "proverbs", "Proverbs", "Prov.xml"),
    "ECC": ("Eccl", "ecclesiastes", "Ecclesiastes", "Eccl.xml"),
    "SNG": ("Song", "song_of_songs", "Song of Songs", "Song.xml"),
    "ISA": ("Isa", "isaiah", "Isaiah", "Isa.xml"),
    "JER": ("Jer", "jeremiah", "Jeremiah", "Jer.xml"),
    "LAM": ("Lam", "lamentations", "Lamentations", "Lam.xml"),
    "EZK": ("Ezek", "ezekiel", "Ezekiel", "Ezek.xml"),
    "DAN": ("Dan", "daniel", "Daniel", "Dan.xml"),
    "HOS": ("Hos", "hosea", "Hosea", "Hos.xml"),
    "JOL": ("Joel", "joel", "Joel", "Joel.xml"),
    "AMO": ("Amos", "amos", "Amos", "Amos.xml"),
    "OBA": ("Obad", "obadiah", "Obadiah", "Obad.xml"),
    "JON": ("Jonah", "jonah", "Jonah", "Jonah.xml"),
    "MIC": ("Mic", "micah", "Micah", "Mic.xml"),
    "NAM": ("Nah", "nahum", "Nahum", "Nah.xml"),
    "HAB": ("Hab", "habakkuk", "Habakkuk", "Hab.xml"),
    "ZEP": ("Zeph", "zephaniah", "Zephaniah", "Zeph.xml"),
    "HAG": ("Hag", "haggai", "Haggai", "Hag.xml"),
    "ZEC": ("Zech", "zechariah", "Zechariah", "Zech.xml"),
    "MAL": ("Mal", "malachi", "Malachi", "Mal.xml"),
}


@dataclass
class Word:
    text: str
    lemma: str
    morph: str
    word_id: str


@dataclass
class Verse:
    book_code: str
    chapter: int
    verse: int
    words: list[Word] = field(default_factory=list)
    punctuation: list[str] = field(default_factory=list)

    @property
    def reference(self) -> str:
        title = OT_BOOKS[self.book_code][2]
        return f"{title} {self.chapter}:{self.verse}"

    @property
    def canonical_id(self) -> str:
        return f"{self.book_code}.{self.chapter}.{self.verse}"

    @property
    def book_slug(self) -> str:
        return OT_BOOKS[self.book_code][1]

    @property
    def hebrew_text(self) -> str:
        rendered = [word.text for word in self.words]
        if not rendered:
            return ""
        text = " ".join(rendered)
        for punct in self.punctuation:
            text += punct
        return text.strip()


def wlc_file_for(book_code: str, sources_root: pathlib.Path) -> pathlib.Path:
    if book_code not in OT_BOOKS:
        raise ValueError(f"Unknown OT book code: {book_code!r}")
    return sources_root / "ot" / "wlc" / OT_BOOKS[book_code][3]


@functools.lru_cache(maxsize=None)
def load_book_tree(path: str) -> ET.Element:
    return ET.parse(path).getroot()


def parse_osis_id(osis_id: str) -> tuple[int, int]:
    parts = osis_id.split(".")
    if len(parts) != 3:
        raise ValueError(f"Unexpected osisID: {osis_id!r}")
    return int(parts[1]), int(parts[2])


def load_verse(
    book_code: str,
    chapter: int,
    verse: int,
    sources_root: pathlib.Path,
) -> Verse:
    path = wlc_file_for(book_code, sources_root)
    root = load_book_tree(str(path))
    osis_code = OT_BOOKS[book_code][0]
    target_osis_id = f"{osis_code}.{chapter}.{verse}"

    verse_elem = root.find(f".//o:verse[@osisID='{target_osis_id}']", OSIS_NS)
    if verse_elem is None:
        raise LookupError(f"No verse found for {book_code} {chapter}:{verse} in {path.name}")

    words: list[Word] = []
    punctuation: list[str] = []

    for child in verse_elem:
        tag = child.tag.rsplit("}", 1)[-1]
        text = (child.text or "").strip()
        if tag == "w":
            words.append(
                Word(
                    text=text,
                    lemma=child.attrib.get("lemma", ""),
                    morph=child.attrib.get("morph", ""),
                    word_id=child.attrib.get("id", ""),
                )
            )
        elif tag == "seg" and text:
            punctuation.append(text)

    return Verse(
        book_code=book_code,
        chapter=chapter,
        verse=verse,
        words=words,
        punctuation=punctuation,
    )


def iter_verses(book_code: str, sources_root: pathlib.Path) -> Iterator[Verse]:
    path = wlc_file_for(book_code, sources_root)
    root = load_book_tree(str(path))

    for verse_elem in root.findall(".//o:verse", OSIS_NS):
        osis_id = verse_elem.attrib.get("osisID")
        if not osis_id or not osis_id.startswith(OT_BOOKS[book_code][0] + "."):
            continue
        chapter, verse = parse_osis_id(osis_id)
        yield load_verse(book_code, chapter, verse, sources_root)


def morphology_lines(verse: Verse) -> str:
    header = f"# Morphology for {verse.reference}\n# Hebrew: {verse.hebrew_text}\n"
    rows = [
        f"  {index + 1:2d}. {word.text:<20}  lemma={word.lemma:<15}  morph={word.morph}"
        for index, word in enumerate(verse.words)
    ]
    return header + "\n".join(rows)
