"""Shared reader-facing terminology policy for compiled Bible payloads."""

from __future__ import annotations

import re
from typing import Any


_SLAVE_TERM = re.compile(r"\bslaves?\b", re.IGNORECASE)


def _preserve_case(source: str, replacement: str) -> str:
    if source.isupper():
        return replacement.upper()
    if source[:1].isupper() and source[1:].islower():
        return replacement.capitalize()
    return replacement


def normalize_bible_verse_text(text: str) -> str:
    """Use servant/servants for standalone slave/slaves in verse text."""

    if not text:
        return text

    def replace(match: re.Match[str]) -> str:
        source = match.group(0)
        replacement = "servants" if source.lower() == "slaves" else "servant"
        return _preserve_case(source, replacement)

    return _SLAVE_TERM.sub(replace, text)


def normalize_reader_payload_in_place(node: Any) -> Any:
    """Mutate translated verse rows without changing notes or audit metadata."""

    if isinstance(node, list):
        for item in node:
            normalize_reader_payload_in_place(item)
        return node
    if not isinstance(node, dict):
        return node
    if "verse" in node and isinstance(node.get("text"), str):
        node["text"] = normalize_bible_verse_text(node["text"])
    for value in node.values():
        normalize_reader_payload_in_place(value)
    return node
