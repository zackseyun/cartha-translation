#!/usr/bin/env python3
"""Recheck Psalm 145 controls; textual facts, not a historical-selection score."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources/textual_restoration/discovery/psalm145_control_check.v1.json"
QDR_SHA = "3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295"
GREEK_SHA = "a34b87a5fbe2857fb453c3bd1bcd2cb0408bb2522b409b6e44d678356ee08103"
NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
ALPHABET = "אבגדהוזחטיכלמנסעפצקרשת"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def letters(text: str) -> str:
    return "".join(re.findall("[א-ת]", text))


def acrostic(verses: list[ET.Element]) -> dict:
    starts = []
    for number, verse in enumerate(verses, 1):
        if verse.get("osisID") != f"Ps.145.{number}":
            raise ValueError("Psalm 145 verses must be unique and consecutive")
        words = [letters("".join(w.itertext())) for w in verse.findall("o:w", NS)]
        if number == 1:
            if words[:2] != ["תהלה", "לדוד"]:
                raise ValueError("Psalm 145 superscription boundary changed")
            words = words[2:]
        if not words or not words[0]:
            raise ValueError("empty poetic opening")
        starts.append(words[0][0])
    return {"stanza_count": len(starts), "opening_letters": "".join(starts),
            "missing_alphabet_letters": "".join(c for c in ALPHABET if c not in starts),
            "title_handling": "Only the explicitly checked two-word superscription in 145:1 is excluded"}


def build(qdr_path: Path, greek_path: Path) -> dict:
    qraw, graw = qdr_path.read_bytes(), greek_path.read_bytes()
    if sha(qraw) != QDR_SHA or sha(graw) != GREEK_SHA:
        raise ValueError("External input differs from pinned snapshot")
    wpath = ROOT / "sources/ot/wlc/Ps.xml"
    wraw = wpath.read_bytes()
    verses = [v for v in ET.fromstring(wraw).findall(".//o:verse", NS)
              if v.get("osisID", "").startswith("Ps.145.")]
    shape = acrostic(verses)
    records = [s for s in json.loads(qraw) if s["scroll"] == "11Q5"]
    if len(records) != 1:
        raise ValueError("11Q5 label absent or duplicated")
    columns = [f for f in records[0]["fragments"] if f["id"] == "17"]
    if len(columns) != 1:
        raise ValueError("11Q5 XVII absent or duplicated")
    rows = {}
    for line in columns[0]["lines"]:
        if line["n"] in rows:
            raise ValueError("duplicate manuscript line")
        rows[line["n"]] = line["words"]
    # Editor-selected token boundaries, not a verse-tag-only extraction:
    # the QDR Ps 145:13 tag also includes both flanking refrains.
    selected = rows["2"][-1:] + rows["3"][:8]
    if any(w[5] != "Ps 145:13" for w in selected):
        raise ValueError("Selected token references changed")
    direct = "".join(letters(w[1]) for w in selected)
    comp = json.loads((ROOT / "sources/textual_restoration/comparisons/psalms_controls.v1.json").read_text())
    case = next(c for c in comp["cases"] if c["id"] == "PSA.145.13.nun")
    readings = {r["source_ref"]: r for r in case["readings"]}
    if direct != letters(readings["qumran-digital-psalms"]["text"]):
        raise ValueError("QDR excerpt differs from separately consulted published transcription")
    greek = [v for v in json.loads(graw) if v["ref"] == "Ps 144:13a"]
    if len(greek) != 1:
        raise ValueError("Greek suffixed reference absent or duplicated")
    surface = " ".join(w["surface"] for w in greek[0]["words"])
    if surface != readings["lxx-morph-rahlfs"]["text"]:
        raise ValueError("Greek formal comparison differs from pinned surface text")
    baseline = case["baseline"]
    if sha((ROOT / baseline["repo_path"]).read_bytes()) != baseline["sha256"]:
        raise ValueError("POB baseline drift")
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-05",
        "scope": "Psalm 145 WLC acrostic, bounded 11Q5 token mapping and Rahlfs suffixed-line control",
        "inputs": {"qdr_sha256": QDR_SHA, "greek_sha256": GREEK_SHA,
                   "wlc_psalms_sha256": sha(wraw), "pob_baseline": baseline},
        "wlc_acrostic": shape,
        "qdr_mapping": {"manuscript": "11Q5", "column": "17",
                        "line_2_token_span": [len(rows["2"]) - 1, len(rows["2"])],
                        "line_3_token_span": [0, 8],
                        "span_convention": "zero-based, half-open, QDR morphological tokens, not printed words",
                        "matches_published_consonants": True,
                        "qdr_word_tags_alone_isolate_nun_line": False},
        "greek": {"reference": "Ps 144:13a", "surface_sha256": sha(surface.encode()),
                  "formal_comparison_matches": True},
        "policy": {"consonantal_match_verifies_visible_ink": False,
                   "acrostic_gap_proves_accidental_omission": False,
                   "version_agreement_proves_exact_hebrew": False,
                   "external_full_text_exported": False, "historical_selection_applied": False},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qdr_json", type=Path)
    parser.add_argument("greek_psalms_json", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.qdr_json, args.greek_psalms_json)
    if args.verify_only:
        if result != json.loads(OUT.read_text()):
            raise SystemExit("Psalm 145 receipt differs from recomputed controls")
        print("Verified Psalm 145 receipt against pinned controls and current POB baseline")
    else:
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(result["wlc_acrostic"], ensure_ascii=False))


if __name__ == "__main__":
    main()
