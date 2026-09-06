#!/usr/bin/env python3
"""Read-only deterministic selector; emits a JSON receipt to stdout."""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_variant_inventory import NS, OT_MAP, footnote_signals

ROOT = Path(__file__).resolve().parents[2]
SEED = "POB-unflagged-2026-09-05-v1"
STRATA = {
    "torah": "genesis exodus leviticus numbers deuteronomy".split(),
    "prophets": "joshua judges 1_samuel 2_samuel 1_kings 2_kings isaiah jeremiah ezekiel hosea joel amos obadiah jonah micah nahum habakkuk zephaniah haggai zechariah malachi".split(),
    "writings": "ruth 1_chronicles 2_chronicles ezra nehemiah esther job psalms proverbs ecclesiastes song_of_songs lamentations daniel".split(),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized(text: str) -> str:
    """Preserve pointed spelling, discard accents/punctuation/segmentation."""
    return "".join(c for c in text if "\u05d0" <= c <= "\u05ea"
                   or "\u05b0" <= c <= "\u05bc" or c in "\u05c1\u05c2\u05c7")


def rank(path: str, stratum: str) -> str:
    return sha(f"{SEED}\0{stratum}\0{path}".encode())


def digest_rows(rows: list[tuple[str, str]]) -> str:
    return sha("".join(f"{path}\0{digest}\n" for path, digest in sorted(rows)).encode())


def build(root: Path = ROOT) -> dict:
    strata = {book: name for name, books in STRATA.items() for book in books}
    assert set(strata) == set(OT_MAP.values())
    wlc = {}
    source_files = []
    for osis, book in OT_MAP.items():
        path = root / f"sources/ot/wlc/{osis}.xml"
        raw = path.read_bytes()
        source_files.append((path.relative_to(root).as_posix(), sha(raw)))
        index = defaultdict(list)
        for verse in ET.fromstring(raw).findall(".//o:verse", NS):
            words = verse.findall("o:w", NS)
            source = " ".join("".join(word.itertext()) for word in words)
            index[normalized(source)].append((verse.get("osisID"), bool(verse.findall(".//o:note", NS))))
        wlc[book] = index
    populations = defaultdict(list)
    exclusions = defaultdict(Counter)
    corpus = []
    for path in sorted((root / "translation/ot").glob("*/*/*.yaml")):
        rel = path.relative_to(root).as_posix()
        book = path.parents[1].name
        if book not in strata:
            raise ValueError(f"Undeclared OT book: {book}")
        group = strata[book]
        raw = path.read_bytes()
        digest = sha(raw)
        corpus.append((rel, digest))
        record = yaml.load(raw, Loader=yaml.CSafeLoader)
        source = record.get("source") or {}
        translation = record.get("translation") or {}
        reason = None
        text = source.get("text") or ""
        matches = wlc[book].get(normalized(text), [])
        if not text.strip() or not str(translation.get("text") or "").strip():
            reason = "empty-source-or-english"
        elif source.get("edition") not in {"WLC", "UHB"}:
            reason = "non-base-edition"
        elif footnote_signals(record):
            reason = "textual-footnote-signal"
        elif source.get("apparatus"):
            reason = "source-apparatus"
        elif any(c in text for c in "⸀⸁⸂⸃⸄⸅[]<>"):
            reason = "source-editorial-marker"
        elif len(matches) != 1:
            reason = "no-unique-pointed-wlc-alignment"
        elif matches[0][1]:
            reason = "wlc-note"
        if reason:
            exclusions[group][reason] += 1
        else:
            populations[group].append({"path": rel, "yaml_sha256": digest,
                "id": record["id"], "reference": record["reference"],
                "wlc_alignment": matches[0][0], "rank_sha256": rank(rel, group),
                "source_text_sha256": sha(text.encode()),
                "english_text_sha256": sha(translation["text"].encode())})
    result = {"seed": SEED, "corpus_files": len(corpus), "corpus_digest": digest_rows(corpus),
              "source_files": dict(source_files), "strata": {}, "protocol_inputs": {}}
    for rel in ["docs/UNFLAGGED_ENGLISH_SAMPLE_PREDECLARATION_2026-09-05.md",
                "tools/textual_restoration/build_unflagged_english_sample.py",
                "tools/textual_restoration/build_variant_inventory.py",
                "docs/TEXTUAL_ADJUDICATION_METHOD.md", "schema/verse.schema.json", "DOCTRINE.md"]:
        result["protocol_inputs"][rel] = sha((root / rel).read_bytes())
    for group in STRATA:
        rows = sorted(populations[group], key=lambda r: (r["rank_sha256"], r["path"]))
        result["strata"][group] = {"eligible": len(rows), "excluded": dict(exclusions[group]),
            "eligible_digest": digest_rows([(r["path"], r["yaml_sha256"]) for r in rows]),
            "selected": rows[0]}
    return result


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
