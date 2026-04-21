"""normalize.py — light Geʿez OCR cleanup helpers.

These helpers are intentionally conservative. They exist to make:
  - OCR-vs-oracle comparisons fairer
  - verse splitting more reliable
  - cross-edition comparisons less sensitive to whitespace noise

They are NOT a textual-critical layer and should not silently rewrite
real witness differences.
"""
from __future__ import annotations

import re
import unicodedata

ETHIOPIC_RE = r"\u1200-\u137F"
ETHIOPIC_PUNCT = "፡።፤፥፦፧፨"
VERSE_MARKER_RE = re.compile(
    rf"(?:(?<=^)|(?<=\s)|(?<=[{ETHIOPIC_PUNCT}]))"
    rf"(?P<marker>\d{{1,3}}|[፩-፱፲-፺፻፼]+)[\.:፡።፤፥\)\]-]*"
    rf"(?=\s*[{ETHIOPIC_RE}])"
)


def _nfkc(text: str) -> str:
    return unicodedata.normalize("NFKC", text or "")


def strip_running_headers(text: str) -> str:
    text = _nfkc(text)
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.fullmatch(r"[0-9IVXLCDMivxlcdm\-–—\s\.]+", line):
            continue
        if "መጽሐፈ" in line and len(line) <= 40:
            continue
        if "ምዕራፍ" in line and len(line) <= 40:
            continue
        lines.append(line)
    return "\n".join(lines)


def keep_ethiopic_core(text: str) -> str:
    text = _nfkc(text)
    text = strip_running_headers(text)
    text = re.sub(rf"[^{ETHIOPIC_RE}{ETHIOPIC_PUNCT}\s0-9]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_for_comparison(text: str) -> str:
    text = keep_ethiopic_core(text)
    text = VERSE_MARKER_RE.sub("", text)
    text = re.sub(r"[0-9]+", "", text)
    text = re.sub(r"\s*፡\s*", "፡", text)
    text = re.sub(r"\s*።\s*", "።", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_for_alignment(text: str) -> str:
    text = normalize_for_comparison(text)
    text = re.sub(r"\s+", "", text)
    return text
