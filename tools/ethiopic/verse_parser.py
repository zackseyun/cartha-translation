"""verse_parser.py — split Ethiopic OCR text into verse records.

Primary target right now is Charles 1906, which prints explicit verse
numbers. The parser is a little broader than that so it can also pick
up Ethiopic numeral markers where present.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
from dataclasses import dataclass, asdict

try:
    from normalize import strip_running_headers, _nfkc  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    from tools.ethiopic.normalize import strip_running_headers, _nfkc  # type: ignore

ETHIOPIC_LETTER_RE = r"[\u1200-\u137F]"
MARKER_RE = re.compile(
    rf"(?:(?<=^)|(?<=\s)|(?<=[።፤፥]))"
    rf"(?P<marker>\d{{1,3}}|[፩-፱፲-፺፻፼]+)"
    rf"(?:[\.:፡።፤፥\)\]-]+|\s+)"
    rf"(?={ETHIOPIC_LETTER_RE})"
)

_ETH_NUMERAL_MAP = {
    "፩": 1, "፪": 2, "፫": 3, "፬": 4, "፭": 5, "፮": 6, "፯": 7, "፰": 8, "፱": 9,
    "፲": 10, "፳": 20, "፴": 30, "፵": 40, "፶": 50, "፷": 60, "፸": 70, "፹": 80, "፺": 90,
    "፻": 100, "፼": 10000,
}


@dataclass
class ParsedVerse:
    verse: int
    marker: str
    text: str


def geez_numeral_to_int(marker: str) -> int:
    if re.fullmatch(r"[0-9]+", marker):
        return int(marker)
    total = 0
    current = 0
    for ch in marker:
        val = _ETH_NUMERAL_MAP.get(ch)
        if val is None:
            raise ValueError(f"Unrecognized Ethiopic numeral: {marker!r}")
        if val == 100:
            current = max(current, 1) * 100
        elif val == 10000:
            current = max(current, 1) * 10000
            total += current
            current = 0
        else:
            current += val
    return total + current


def _prepare(text: str) -> str:
    text = _nfkc(text)
    text = strip_running_headers(text)
    text = re.sub(r"\[[^\]]+\]", " ", text)
    text = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹*]+", "", text)
    text = re.sub(r"\b[IVXLCDM]+\.\s*", " ", text)
    text = re.sub(r"\b\d+\s*[-–—]\s*\d+\b", " ", text)  # page/header ranges like 1-5
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_verses(text: str) -> list[ParsedVerse]:
    prepared = _prepare(text)
    matches = list(MARKER_RE.finditer(prepared))
    if not matches:
        return []

    verses: list[ParsedVerse] = []
    for idx, match in enumerate(matches):
        marker = match.group("marker")
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(prepared)
        body = prepared[start:end].strip()
        if not body:
            continue
        try:
            verse_num = geez_numeral_to_int(marker)
        except ValueError:
            continue
        verses.append(ParsedVerse(verse=verse_num, marker=marker, text=body))
    return verses


def write_verses(chapter_text_path: pathlib.Path, output_dir: pathlib.Path) -> dict:
    text = chapter_text_path.read_text(encoding="utf-8")
    verses = parse_verses(text)
    output_dir.mkdir(parents=True, exist_ok=True)
    for verse in verses:
        (output_dir / f"v{verse.verse:03d}.txt").write_text(verse.text + "\n", encoding="utf-8")
    manifest = {
        "chapter_source": str(chapter_text_path),
        "verse_count": len(verses),
        "verses": [asdict(v) for v in verses],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output_dir")
    args = ap.parse_args()
    manifest = write_verses(pathlib.Path(args.input), pathlib.Path(args.output_dir))
    print(json.dumps({"verse_count": manifest["verse_count"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
