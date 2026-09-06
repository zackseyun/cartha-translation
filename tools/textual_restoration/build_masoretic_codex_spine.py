#!/usr/bin/env python3
"""Catalogue-led navigation and actual local edition probes, never ink coverage."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "sources/textual_restoration/discovery"
SOURCES = DIR / "masoretic_codex_sources.v1.json"
BOOK_MAP = DIR / "hebrew_bible_book_map.v1.json"
OUTPUT = DIR / "masoretic_codex_spine.v1.json"
NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
TWELVE = "hosea joel amos obadiah jonah micah nahum habakkuk zephaniah haggai zechariah malachi".split()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def group(book):
    if book in TWELVE:
        return "the_twelve"
    if book in ("ezra", "nehemiah"):
        return "ezra_nehemiah"
    for name in ("samuel", "kings", "chronicles"):
        if book in ("1_" + name, "2_" + name):
            return name
    return book


def aleppo_status(book, policy):
    if book in policy["main_body_absent_books"]:
        status = "main-body-missing-in-cited-list"
    elif book in policy["source_reported_partial_books"]:
        status = "partial-loss-reported"
    else:
        status = "not-listed-as-missing-completeness-unverified"
    return {"body_status": status,
            "gap_locator_as_reported": policy["source_reported_partial_books"].get(book),
            "special_evidence": policy["special_evidence"].get(book, []),
            "direct_reading_collated": False}


def validate_sources(data, books):
    if len(books) != 39 or len(set(books)) != 39 or len({group(b) for b in books}) != 24:
        raise ValueError("39/24 navigation accounting changed")
    a = data["aleppo"]
    sets = [set(a["main_body_absent_books"]), set(a["source_reported_partial_books"])]
    if sets[0] & sets[1] or not (sets[0] | sets[1] | set(a["special_evidence"])) <= set(books):
        raise ValueError("invalid Aleppo book assignment")
    source_ids = [r["id"] for r in data["sources"]]
    if len(source_ids) != len(set(source_ids)) or a["source_id"] not in source_ids:
        raise ValueError("source identity mismatch")
    for key in ("all_source_coverage_complete", "catalogue_extent_proves_exact_reading",
                "digital_full_text_proves_all_marks_survive", "edition_agreement_is_independent_manuscript_support",
                "fresh_image_transcription_performed", "canonical_change_applied"):
        if data["policy"].get(key) is not False:
            raise ValueError("unsupported promotion: " + key)


def vowel_count(text):
    # Includes sheva and vowel signs, excludes dagesh, accents, meteg, shin dots.
    return sum("\u05b0" <= c <= "\u05bb" or c == "\u05c7" for c in text)


def probe(wlc, canonical, osis_id):
    verse = ET.parse(wlc).find(f".//o:verse[@osisID='{osis_id}']", NS)
    if verse is None:
        raise ValueError("missing local verse " + osis_id)
    words = verse.findall(".//o:w", NS)
    word_text = " ".join("".join(w.itertext()) for w in words)
    record = yaml.safe_load(canonical.read_text())
    role = "first-offering-vocalized-control" if osis_id == "Num.7.13" else (
        "repeated-offering-supplied-vowels-lead" if osis_id == "Num.7.19" else "reported-LC-omission-in-digital-edition")
    return {"osis_id": osis_id, "probe_role": role, "local_wlc_verse_present": True,
            "wlc_word_element_count": len(words), "wlc_vowel_codepoint_count": vowel_count(word_text),
            "canonical_source_edition": record["source"]["edition"],
            "canonical_source_vowel_codepoint_count": vowel_count(record["source"]["text"]),
            "canonical_text_and_source_sha256": sha(canonical),
            "wlc_notes": [{"type": n.get("type"), "subType": n.get("subType"),
                           "text": "".join(n.itertext())} for n in verse.findall(".//o:note", NS)],
            "counts_measure": "digital encoding only; not a count of physically surviving manuscript marks",
            "source_claim_basis": "uxlc-changes editor report, not new LC pixel inspection"}


def build():
    data = json.loads(SOURCES.read_text())
    discovery = json.loads(BOOK_MAP.read_text())
    books = [r["book"] for r in discovery["books"]]
    validate_sources(data, books)
    files = [SOURCES, BOOK_MAP, ROOT / "sources/ot/uwhb/manifest.yaml"]
    manifest = yaml.safe_load(files[-1].read_text())["dublin_core"]
    rows = []
    for entry in discovery["books"]:
        book = entry["book"]
        wlc = ROOT / "sources/ot/wlc" / (entry["wlc_book"] + ".xml")
        files.append(wlc)
        header = ET.parse(wlc).find(".//o:header", NS)
        revisions = [{"date": r.findtext("o:date", namespaces=NS),
                      "description": r.findtext("o:p", namespaces=NS)}
                     for r in header.findall("o:revisionDesc", NS)]
        rows.append({"book": book, "tanakh_navigation_group": group(book),
                     "qdr_reference_anchors": entry["qdr_indexed_reference_anchors"],
                     "qdr_zero_is_not_global_absence": True,
                     "leningrad": {"extent": "complete-codex-reported-not-every-mark-certified",
                                    "source_ids": ["nli-leningrad", "nlr-leningrad"],
                                    "verse_and_layer_collation_complete": False},
                     "aleppo": aleppo_status(book, data["aleppo"]),
                     "sassoon": {"extent": "book-family-represented-specific-passage-survival-unmapped",
                                 "source_ids": ["anu-sassoon", "sothebys-sassoon"],
                                 "aggregate_percentage_applied_to_book": False,
                                 "verse_and_hand_collation_complete": False},
                     "local_wlc": {"path": wlc.relative_to(ROOT).as_posix(),
                                   "sha256": sha(wlc), "header_revisions": revisions}})
    probes = []
    for book, short, chapter, verse in [("joshua", "Josh", 21, 36), ("joshua", "Josh", 21, 37),
                                      ("numbers", "Num", 7, 13), ("numbers", "Num", 7, 19)]:
        wlc = ROOT / "sources/ot/wlc" / (short + ".xml")
        canonical = ROOT / f"translation/ot/{book}/{chapter:03}/{verse:03}.yaml"
        files.append(canonical)
        probes.append(probe(wlc, canonical, f"{short}.{chapter}.{verse}"))
    return {"schema_version": "1.0.0", "checked_date": data["checked_date"],
            "scope": data["scope"], "policy": data["policy"],
            "summary": {"pob_books": len(rows), "tanakh_navigation_groups": len({group(b) for b in books}),
                        "named_physical_codex_targets": 3, "physical_independence_adjudicated": False,
                        "zero_qdr_books_retained": [r["book"] for r in rows if r["qdr_reference_anchors"] == 0],
                        "new_source_readings_adopted": 0},
            "local_uhb": {k: manifest[k] for k in ("version", "issued", "source", "rights")},
            "local_inputs": {p.relative_to(ROOT).as_posix(): sha(p) for p in files},
            "books": rows, "digital_vs_manuscript_probes": probes,
            "reading_decision": "Retain current texts pending separate passage/source review. Catalogue and digital encoding do not authorize adding, deleting or repointing POB.",
            "next_targets": ["Obtain actual Aleppo missing-region photos/editions and preserve layer provenance",
                             "Obtain Sassoon passage-level loss/hand map; no uniform92-percent inference",
                             "Collate pinned UXLC corrections against actual LC images and POB source/English",
                             "Expand beyond three codices to other Masoretic/Genizah witnesses and apparatuses"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.write:
        with OUTPUT.open("x") as stream:
            stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    elif result != json.loads(OUTPUT.read_text()):
        raise ValueError("saved spine/input drift")
    print(json.dumps(result["summary"], indent=2))
