#!/usr/bin/env python3
"""Import four public-domain ancient church-order witnesses.

The generated reader text is deliberately a *witness bridge*, not a claim of
direct translation from the ancient languages.  Each YAML keeps the complete
English witness and an open source-language review gate so a later editorial
pass can modernize and ground the text without losing provenance.
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import shutil
import urllib.request
from html.parser import HTMLParser
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "sources" / "early_christian_texts"
TRANSLATION_ROOT = ROOT / "translation" / "extra_canonical"


TEXTS: dict[str, dict[str, Any]] = {
    "didascalia_apostolorum": {
        "code": "DASC",
        "title": "Didascalia Apostolorum",
        "url": "https://www.earlychristianwritings.com/text/didascalia.html",
        "snapshot": "witness.html",
        "translator": "R. Hugh Connolly (1929)",
        "license": "Public domain in the United States (published 1929)",
        "manuscript": "Complete Syriac version with surviving Verona Latin fragments",
        "ancient_language": "Greek original lost; Syriac version and Latin fragments",
        "parser": "didascalia",
    },
    "apostolic_tradition": {
        "code": "APTR",
        "title": "Apostolic Tradition",
        "url": "https://www.gutenberg.org/cache/epub/61614/pg61614.txt",
        "snapshot": "witness.txt",
        "translator": "Burton Scott Easton (1934)",
        "license": "Project Gutenberg public-domain text in the United States (ebook 61614)",
        "manuscript": "Reconstruction from Latin, Sahidic, Arabic, Ethiopic, and Greek fragments",
        "ancient_language": "Greek original fragmentary; Latin, Coptic, Arabic, and Ethiopic versions",
        "parser": "tradition",
    },
    "apostolic_church_order": {
        "code": "ACHO",
        "title": "Apostolic Church Order",
        "url": "https://archive.org/download/apostolicalconst00tattrich/apostolicalconst00tattrich_djvu.txt",
        "snapshot": "witness.txt",
        "translator": "Henry Tattam (1848)",
        "license": "Public domain (published 1848)",
        "manuscript": "Bohairic Coptic Alexandrine Sinodos, checked by Tattam against Sahidic",
        "ancient_language": "Greek original; Bohairic and Sahidic Coptic witnesses",
        "parser": "church_order",
    },
    "apostolic_constitutions": {
        "code": "ACON",
        "title": "Apostolic Constitutions",
        "url": "https://ccel.org/ccel/schaff/anf07/cache/anf07.txt",
        "snapshot": "witness.txt",
        "translator": "James Donaldson, Ante-Nicene Fathers VII (1886)",
        "license": "Public domain; CCEL identifies ANF VII as public domain",
        "manuscript": "Greek manuscript tradition of the eight-book Apostolic Constitutions",
        "ancient_language": "Greek",
        "parser": "constitutions",
    },
}


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_number(value: str) -> int:
    total = 0
    previous = 0
    for char in reversed(value):
        number = ROMAN[char]
        total += -number if number < previous else number
        previous = max(previous, number)
    return total


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Cartha-POB-Church-Orders/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read().decode("utf-8", "ignore")


class VisibleText(HTMLParser):
    BLOCKS = {"p", "div", "h1", "h2", "h3", "h4", "li", "br", "tr"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skipped = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "nav"}:
            self.skipped += 1
        elif not self.skipped and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav"} and self.skipped:
            self.skipped -= 1
        elif not self.skipped and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skipped:
            self.parts.append(data)

    def text(self) -> str:
        value = html.unescape("".join(self.parts)).replace("\xa0", " ")
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r" *\n *", "\n", value)
        return re.sub(r"\n{3,}", "\n\n", value).strip()


def clean_prose(value: str) -> str:
    value = value.replace("\r", "")
    value = re.sub(r"(?<=\w)-\n(?=\w)", "", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def sections_from_matches(text: str, matches: list[re.Match[str]], title_prefix: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        body = text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)]
        number = int(match.group("number"))
        body = clean_prose(body)
        if body:
            sections.append({"heading": f"{title_prefix} {number}", "paragraphs": [body]})
    return sections


def parse_didascalia(raw: str) -> list[dict[str, Any]]:
    parser = VisibleText()
    parser.feed(raw)
    text = parser.text()
    start = text.find("CHAPTER I")
    if start < 0:
        raise ValueError("Didascalia chapter I not found")
    text = text[start:]
    pattern = re.compile(r"(?m)^CHAPTER (?P<roman>[IVXLCDM]+)(?:\s+\(p\.\s*\d+\))?\s*$")
    matches = list(pattern.finditer(text))
    sections: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        number = roman_number(match.group("roman"))
        if number > 26:
            break
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = clean_prose(text[match.end() : end])
        parts = re.split(r"\n\s*\n", body, maxsplit=1)
        candidate = re.sub(r"\s+", " ", parts[0]).strip()
        heading = candidate if len(parts) == 2 and len(candidate) < 650 else f"Chapter {number}"
        prose = clean_prose(parts[1]) if heading != f"Chapter {number}" else body
        sections.append({"heading": f"Chapter {number}: {heading}", "paragraphs": [prose]})
    return sections


def parse_tradition(raw: str) -> list[dict[str, Any]]:
    raw = raw.replace("\r", "")
    translation_marker = raw.index("TRANSLATION\n")
    start = raw.rfind("THE APOSTOLIC TRADITION OF HIPPOLYTUS", 0, translation_marker)
    text = raw[start:]
    later_at = text.index("LATER ADDITIONS")
    notes_at = text.index("\n                                NOTES", later_at)
    main = text[:later_at]
    later = text[later_at:notes_at]
    pattern = re.compile(r"(?m)^(?:[A-Z]+(?:\[\d+\])?\s*|\s{8})(?P<number>\d+)\.(?:\[\d+\])?\s*")

    def collect(value: str) -> dict[int, str]:
        matches = [match for match in pattern.finditer(value) if 1 <= int(match.group("number")) <= 38]
        found: dict[int, str] = {}
        for index, match in enumerate(matches):
            number = int(match.group("number"))
            if number in found:
                continue
            body = value[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(value)]
            body = re.sub(r"(?m)^(?:LAT|GRE|SAH|ETH|ARA)(?:\[\d+\])?\s+", "", clean_prose(body))
            found[number] = body
        return found

    bodies = collect(main)
    additions = collect(later)
    for number in (24, 31, 32):
        if number in additions:
            bodies[number] = additions[number]
    bodies[7] = "[No chapter 7 is present in Easton’s reconstructed numbering; the public-domain witness moves from chapter 6 to chapter 8.]"
    return [
        {"heading": f"Chapter {number}", "paragraphs": [bodies[number]]}
        for number in range(1, 39)
    ]


ENGLISH_WORDS = set("the and of to in that shall is be a for with not this he you his they as have from or who it are said let which their by on".split())


def english_only_tattam(raw: str) -> str:
    raw = raw[raw.index("THE  APOSTOLICAL  CONSTITUTIONS.") :]
    raw = raw[: raw.find("\n31.  A  Bishop")]
    kept: list[str] = []
    for paragraph in re.split(r"\n\s*\n", raw):
        words = re.findall(r"[A-Za-z]+", paragraph.lower())
        score = sum(word in ENGLISH_WORDS for word in words)
        if score >= 2 or re.search(r"(?m)^\s*(?:[1-9]|[12]\d|30)\.\s", paragraph):
            paragraph = re.sub(r"(?m)^THE\s+APOSTOLICAL\s+CONSTITUTIONS\.?(?:\s+\d+)?\s*$", "", paragraph)
            kept.append(paragraph)
    return clean_prose("\n\n".join(kept))


def parse_church_order(raw: str) -> list[dict[str, Any]]:
    text = english_only_tattam(raw)
    first_two = re.search(r"(?m)^\s*2\.\s", text)
    if not first_two:
        raise ValueError("Apostolic Church Order section 2 not found")
    text = "1. " + text[: first_two.start()].strip() + "\n\n" + text[first_two.start() :]
    matches: list[re.Match[str]] = []
    cursor = 0
    for number in range(1, 31):
        match = re.search(rf"(?m)^\s*(?P<number>{number})\.\s", text[cursor:])
        if match is None:
            raise ValueError(f"Apostolic Church Order chapter {number} not found")
        # Re-run against the full string so match offsets remain absolute.
        absolute = re.compile(rf"(?m)^\s*(?P<number>{number})\.\s").search(text, cursor)
        assert absolute is not None
        matches.append(absolute)
        cursor = absolute.end()
    return sections_from_matches(text, matches, "Chapter")


def strip_ccel_notes(value: str) -> str:
    paragraphs = re.split(r"\n\s*\n", value)
    kept = [paragraph for paragraph in paragraphs if not re.match(r"^\s*\[\d+\]", paragraph)]
    value = "\n\n".join(kept)
    value = re.sub(r"\[\d+\]", "", value)
    value = re.sub(r"(?m)^\s*_+\s*$", "", value)
    value = re.sub(r"(?mi)^constitutions of the holy apostles\.?\s*$", "", value)
    return clean_prose(value)


def parse_constitutions(raw: str) -> list[dict[str, Any]]:
    start = raw.index("Constitutions of the Holy Apostles. [2523]")
    text = raw[start:]
    end = text.find("The end of the Constitutions of the Holy Apostles")
    text = text[:end]
    pattern = re.compile(r"(?m)^\s*Book (?P<roman>VIII|VII|VI|V|IV|III|II|I)\.\s*$")
    matches = list(pattern.finditer(text))
    sections: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        number = roman_number(match.group("roman"))
        body = text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)]
        sections.append({"heading": f"Book {match.group('roman')}", "paragraphs": [strip_ccel_notes(body)]})
    return sections


PARSERS = {
    "didascalia": parse_didascalia,
    "tradition": parse_tradition,
    "church_order": parse_church_order,
    "constitutions": parse_constitutions,
}


def record(config: dict[str, Any], index: int, section: dict[str, Any]) -> dict[str, Any]:
    witness = "\n\n".join(section["paragraphs"]).strip()
    return {
        "id": f"{config['code']}.{index:03d}",
        "reference": f"{config['title']} — {section['heading']}",
        "unit": "chapter",
        "book": config["title"],
        "reader_navigation": {
            "division_kind": "chapter",
            "order": index,
            "heading": section["heading"],
            "authoritative_division": False,
            "note": "This division follows the cited public-domain edition and is a reader navigation aid.",
        },
        "source": {
            "edition": config["translator"],
            "language": "English",
            "text": witness,
            "text_scope": "public_domain_english_witness",
            "manuscript": config["manuscript"],
            "ancient_language": config["ancient_language"],
            "drafting_basis": "Public-domain English translation witness; direct source-language review and POB modernization pending",
            "witness_url": config["url"],
            "witness_translator": config["translator"],
            "witness_license": config["license"],
            "english_witness": witness,
        },
        "translation": {
            "text": witness,
            "philosophy": "provisional public-domain witness bridge",
            "translator_notes": [
                "Complete historical witness supplied for reading while a direct ancient-language POB revision is composed.",
                "Archaic wording and edition-specific reconstruction choices remain visible rather than being silently modernized.",
            ],
        },
        "ai_draft": {
            "model_id": "none-witness-import",
            "prompt_id": "church_order_pd_witness_import_v1",
            "timestamp": "2026-08-29T00:00:00Z",
        },
        "status": "provisional_source_bridge",
        "source_language_review": "pending",
        "grounding_review": {
            "verdict": "accept",
            "issues": [],
            "method": "Exact public-domain witness import; no substantive modernization in this pass.",
        },
    }


def write_text(text_id: str, config: dict[str, Any], raw: str, sections: list[dict[str, Any]]) -> None:
    if not sections or any(not "".join(section["paragraphs"]).strip() for section in sections):
        raise ValueError(f"{text_id}: empty parsed section")
    source_dir = SOURCE_ROOT / text_id
    translation_dir = TRANSLATION_ROOT / text_id
    source_dir.mkdir(parents=True, exist_ok=True)
    if translation_dir.exists():
        shutil.rmtree(translation_dir)
    translation_dir.mkdir(parents=True)
    snapshot_raw = raw
    if config["parser"] == "constitutions":
        start = raw.index("Constitutions of the Holy Apostles. [2523]")
        end = raw.index("The end of the Constitutions of the Holy Apostles", start)
        snapshot_raw = raw[start:end]
    (source_dir / config["snapshot"]).write_text(snapshot_raw, encoding="utf-8")
    (source_dir / "sections.json").write_text(json.dumps(sections, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = {
        "text_id": text_id,
        "title": config["title"],
        "collection": "apostolic_fathers",
        "manuscript": config["manuscript"],
        "source_language": config["ancient_language"],
        "current_drafting_basis": {
            "kind": "public_domain_english_translation_witness",
            "url": config["url"],
            "translator": config["translator"],
            "license": config["license"],
            "raw_snapshot": str((source_dir / config["snapshot"]).relative_to(ROOT)),
        },
        "direct_source_language_review": "required_before_final",
        "unit": "chapter",
        "expected_units": len(sections),
        "generated_at": "2026-08-29T00:00:00Z",
    }
    (source_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for index, section in enumerate(sections, start=1):
        path = translation_dir / f"{index:03d}.yaml"
        path.write_text(yaml.safe_dump(record(config, index, section), allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", action="append", choices=sorted(TEXTS))
    parser.add_argument("--source-dir", type=pathlib.Path, help="Use pre-fetched files named by each snapshot field")
    args = parser.parse_args()
    selected = args.text or list(TEXTS)
    for text_id in selected:
        config = TEXTS[text_id]
        raw = (args.source_dir / config["snapshot"]).read_text(encoding="utf-8") if args.source_dir else fetch(config["url"])
        sections = PARSERS[config["parser"]](raw)
        expected = {"didascalia_apostolorum": 26, "apostolic_tradition": 38, "apostolic_church_order": 30, "apostolic_constitutions": 8}[text_id]
        if len(sections) != expected:
            raise ValueError(f"{text_id}: parsed {len(sections)} units, expected {expected}")
        write_text(text_id, config, raw, sections)
        print(f"wrote {text_id}: {len(sections)} units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
