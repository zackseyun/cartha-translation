#!/usr/bin/env python3
"""psalms_of_solomon.py — source coverage helper for Psalms of Solomon.

This module does not yet attempt full verse parsing. Its purpose is to
make the now-complete Swete page coverage for Psalms of Solomon easy to
inspect and consume while the book-specific parser is built.
"""
from __future__ import annotations

import pathlib
import re
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

TRANSCRIBED_DIR = pathlib.Path(lxx_swete.TRANSCRIBED_DIR)
RUNNING_HEAD_RE = re.compile(r"\[RUNNING HEAD\]\s*\n(.*?)\n\[BODY\]", re.DOTALL)


@dataclass(frozen=True)
class SwetePage:
    scan_page: int
    running_head: str
    body_text: str
    path: pathlib.Path


def page_path(scan_page: int) -> pathlib.Path:
    return TRANSCRIBED_DIR / f"vol{SWETE_VOL}_p{scan_page:04d}.txt"


def page_meta_path(scan_page: int) -> pathlib.Path:
    return TRANSCRIBED_DIR / f"vol{SWETE_VOL}_p{scan_page:04d}.meta.json"


def extract_running_head(page_text: str) -> str:
    m = RUNNING_HEAD_RE.search(page_text)
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


def summary() -> dict:
    pages = list(iter_pages())
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
        "running_heads_sample": {
            p.scan_page: p.running_head for p in pages[:5]
        },
    }


if __name__ == "__main__":
    import pprint

    pprint.pp(summary())
