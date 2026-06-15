#!/usr/bin/env python3
"""Shared Psalm superscription detection helpers.

Psalm superscriptions are reader-facing headers in POB, so they should live in
000.yaml, not in the first numbered content verse.
"""
from __future__ import annotations

import re

# A verse has *content* if it contains a main predication — Yahweh/God doing
# something, first-person prayer, imperatives of praise/lament, beatitudes, etc.
# Superscription clauses are purely nominal/attributive with no such predicate.
CONTENT_RE = re.compile(
    r"""(
        # Vocative address to God — always content, never superscription
        \bO\s+(Yahweh|God|Lord|my\s+God)\b
        |\bYahweh,\s+(my|our|your|O|hear|answer|arise)\b
        # Yahweh / God as subject with any predicate
        |\bYahweh\s+(is\b|are\b|will\b|shall\b|has\b|have\b|was\b|were\b
                    |my\b|your\b|comes?\b|came\b|speaks?\b|spoke\b
                    |delivers?\b|delivered\b|saves?\b|saved\b
                    |reigns?\b|reigned\b|dwells?\b|stands?\b|judges?\b
                    |loves?\b|hears?\b|sees?\b|gives?\b|takes?\b)
        |\bGod\s+(is\b|are\b|will\b|has\b|my\b|your\b|hears?\b|sees?\b
                  |stands?\b|reigns?\b|judges?\b|speaks?\b|gives?\b)
        # First-person subject (prayer / testimony voice)
        |\bI\s+(will\b|have\b|am\b|was\b|shall\b|call\b|cry\b|praise\b
                |lift\b|trust\b|take\b|seek\b|wait\b|put\b|rest\b
                |declare\b|love\b|say\b|know\b|believe\b|walk\b|fear\b)
        |\bmy\s+(soul\b|heart\b|strength\b|God\b|King\b|help\b
                 |refuge\b|rock\b|shield\b|portion\b|prayer\b|cry\b)
        # Second-person address / imperatives to God
        |\b(Hear\s+(my|me|o|a)\b|Save\s+me\b|Help\s+me\b
            |Deliver\s+me\b|Vindicate\s+me\b|Arise\b|Awake\b
            |Contend\b|Give\s+(your|me|ear|thanks|glory)\b
            |Do\s+not\s+(forsake|hide|forget|be\b)\b
            |Answer\s+me\b|Look\s+(on|upon)\b)
        # Lament / question openers
        |\b(How\s+long\b|Why\s+(do|have|has|did|O)\b
            |Blessed\s+(is|are)\b
            |Shout\s+(for|to)\b|Praise\s+(the|Yahweh|God)\b
            |Sing\s+(to|a)\b)
        # Doctrinal / narrative statements
        |\bThe\s+(earth\b|heavens\b|nations\b|fool\b|righteous\b|wicked\b
                  |Mighty\s+One\b|LORD\s+is\b)
        |\bAll\s+the\s+(nations\b|earth\b|peoples\b)
        |\bSurely\s+(God|Yahweh)\b
    )""",
    re.IGNORECASE | re.VERBOSE,
)

# Sentence starters that indicate the clause is attributive (superscription),
# not predicative (content). Used when splitting fused verses.
SUPER_CLAUSE_START = re.compile(
    r"""^(
        for\s+the\s+(choir\s+director|choirmaster|director\s+of\s+music)
        |a\s+(psalm|song|prayer|miktam|maskil|shiggaion|hymn|petition)
        |a\s+song\s+of\s+(ascents|degrees)
        |of\s+(david|asaph|solomon|moses|ethan|heman)
        |of\s+the\s+sons\s+of\s+korah|by\s+the\s+sons\s+of\s+korah
        |according\s+to\b
        |on\s+the\s+(sheminith|gittith|alamoth)
        |with\s+(stringed\s+instruments|flutes)
        |when\s+(he|david|saul|the\s+philistines|joab)\b
        |for\s+(remembrance|the\s+memorial\s+offering|memorial)
    )\b""",
    re.IGNORECASE | re.VERBOSE,
)


def has_content(text: str) -> bool:
    """Return True when text contains actual Psalm body content."""
    if CONTENT_RE.search(text):
        return True
    # Secondary: split into period-delimited clauses; if ANY clause cannot be
    # identified as a superscription phrase, the verse contains content.
    clauses = [c.strip().rstrip(".;:,—") for c in re.split(r"\.\s+", text) if c.strip()]
    for clause in clauses:
        if clause and not SUPER_CLAUSE_START.match(clause):
            return True
    return False


def is_superscription(text: str) -> bool:
    """Return True if text is entirely a superscription with no content verse."""
    stripped = text.strip()
    return not has_content(stripped) if stripped else False


def classify_verse1(text: str) -> str:
    """
    Returns:
      'standalone'  — entire verse is a superscription, no content
      'fused'       — superscription prefix + content in same verse
      'content'     — no superscription, pure content (Ps 1, 2, etc.)
    """
    stripped = text.strip()
    if not stripped:
        return "content"

    if not has_content(stripped):
        return "standalone"

    first_clause = re.split(r"\.\s+", stripped)[0].strip()
    if SUPER_CLAUSE_START.match(first_clause):
        return "fused"
    return "content"


def split_fused(text: str) -> tuple[str, str]:
    """
    Split a fused verse text into (superscription, content).
    E.g. "A psalm of David. Yahweh is my shepherd; I will not lack."
      → ("A psalm of David.", "Yahweh is my shepherd; I will not lack.")
    """
    parts = re.split(r"(\.\s+)", text)
    sentences: list[str] = []
    i = 0
    while i < len(parts):
        s = parts[i]
        if i + 1 < len(parts) and parts[i + 1].startswith("."):
            sentences.append(s + parts[i + 1].rstrip())
            i += 2
        else:
            if s.strip():
                sentences.append(s)
            i += 1

    super_parts: list[str] = []
    content_parts: list[str] = []
    in_content = False
    for sent in sentences:
        if in_content:
            content_parts.append(sent)
            continue
        clause = sent.rstrip(". ")
        if not has_content(sent) and SUPER_CLAUSE_START.match(clause.strip()):
            super_parts.append(sent.rstrip() if sent.endswith(". ") else sent)
        else:
            in_content = True
            content_parts.append(sent)

    super_text = " ".join(super_parts).strip()
    content_text = " ".join(content_parts).strip()
    if super_text and not super_text.endswith("."):
        super_text += "."
    return super_text, content_text
