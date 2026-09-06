#!/usr/bin/env python3
"""Reconcile all twelve printed En-Gedi apparatus units with local controls.

Editorial comparison labels are not an independently deciphered transcription.
Only bounded forms/metadata are exported, not the private PDF or SP/QDR corpora.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.build_samaritan_screen import load_sp, consonants
from tools.textual_restoration.extract_qdr_passages import extract_passages

DIR = ROOT / "sources/textual_restoration/discovery"
UNITS = DIR / "en_gedi_apparatus_units.v1.json"
OUT = DIR / "en_gedi_apparatus_check.v1.json"
QDR_SHA = "3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def tokens(text):
    # Slash is a morphology separator within words. Maqqef is a word boundary.
    return [c for w in text.replace("־", " ").split() if (c := consonants(w))]


def locate(sequence, phrase):
    needle = tokens(phrase)
    if not needle:
        raise ValueError("empty comparison context")
    starts = [i for i in range(len(sequence) - len(needle) + 1)
              if sequence[i:i + len(needle)] == needle]
    if len(starts) != 1:
        raise ValueError(f"context is absent or nonunique: {phrase}")
    return {"start_word_zero_based": starts[0], "word_count": len(needle)}


def build(pdf, sp_directory, qdr):
    spec_raw = UNITS.read_bytes()
    spec = json.loads(spec_raw)
    if digest(pdf.read_bytes()) != spec["edition_sha256"]:
        raise ValueError("consulted edition hash mismatch")
    sp, sp_pins = load_sp(sp_directory)
    qdr_raw = qdr.read_bytes()
    if digest(qdr_raw) != QDR_SHA:
        raise ValueError("QDR hash mismatch")
    qdr_corpus = json.loads(qdr_raw)
    qdr_controls = []
    # QDR uses 'Lev 2:8', not our normalized 'Lev.2.8'. These exact tags are
    # checked, not inferred from failed normalized-string lookups.
    for ref, line_number, normalized in (("Lev 2:8", "29", "והביא"), ("Lev 2:9", "31", "ניחוח")):
        hits = extract_passages(qdr_corpus, {ref})[ref]
        target = [h for h in hits if h["manuscript_id"] == "4Q24"]
        if len(target) != 1:
            raise ValueError("expected QDR object not uniquely found")
        line = next(l for l in target[0]["lines"] if l["fragment"] == "f1_7" and l["line"] == line_number)
        if normalized not in consonants(line["diplomatic_text"]):
            raise ValueError("reported QDR comparison form absent")
        qdr_controls.append({"qdr_reference_tag": ref, "manuscript_id": "4Q24",
                             "fragment": "f1_7", "line": line_number,
                             "normalized_comparison_form": normalized,
                             "line_sha256": digest(line["diplomatic_text"].encode()),
                             "basis": "word-tagged digital transcription consultation; surrounding brackets remain relevant; primary 4Q24 edition/image not checked here"})
    checked = []
    for unit in spec["units"]:
        _, c, v = unit["reference"].split(".")
        path = ROOT / f"translation/ot/leviticus/{int(c):03}/{int(v):03}.yaml"
        raw = path.read_bytes()
        pob = yaml.safe_load(raw)
        if pob["source"]["edition"] != "WLC":
            raise ValueError("source edition changed; re-adjudicate")
        source_tokens = tokens(pob["source"]["text"])
        source_span = locate(source_tokens, unit["pob_context"])
        sp_span = locate(tokens(sp[unit["reference"]]), unit["sp_context"])
        form = unit["editorial_form"]
        locate(tokens(unit["pob_context"]), form)
        prefix = unit["supplied_prefix"]
        if not form.startswith(prefix) or (prefix and prefix == form):
            raise ValueError("invalid supplied-prefix annotation")
        if unit["english_excerpt"] not in pob["translation"]["text"]:
            raise ValueError("English excerpt no longer matches current POB")
        checked.append({**unit, "pob_path": str(path.relative_to(ROOT)), "pob_sha256": digest(raw),
                        "pob_source_context_span": source_span, "sp_context_span": sp_span,
                        "editorial_form_matches_pob_context": True,
                        "sp_context_matches_pob_context": tokens(unit["sp_context"]) == tokens(unit["pob_context"]),
                        "published_unbracketed_remainder": form[len(prefix):],
                        "preservation_class": "partly-supplied-editorial-unit" if prefix else "unbracketed-editorial-unit",
                        "english_effect": "no-source-driven-change-selected"})
    if len({u["id"] for u in checked}) != 12 or len(checked) != 12:
        raise ValueError("apparatus unit set changed")
    return {"schema_version": "1.0.0", "checked_date": "2026-09-05",
            "witness_id": "en-gedi-leviticus", "scope": spec["scope"],
            "edition": {"citation": "Segal et al., An Early Leviticus Scroll from En-Gedi: Preliminary Publication, Textus 26 (2016), 1-30",
                        "url": "https://openscholar.huji.ac.il/sites/default/files/he_bible_project/files/m._segal1.1.pdf",
                        "sha256": spec["edition_sha256"], "pages_visually_inspected_this_pass": [8, 9, 10, 11],
                        "notation_policy": spec["notation_policy"],
                        "versional_apparatus_limit": "Footnote 19 says LXX/Peshitta differences are reported selectively where aligned with Hebrew witnesses; silence is not agreement."},
            "units_sha256": digest(spec_raw), "sp_inputs": sp_pins, "qdr_sha256": QDR_SHA,
            "rights": "Edition PDF and CC BY-NC SP/QDR source corpora remain outside Git; only bounded comparison forms, locators and hashes retained, not relicensed as POB CC BY.",
            "summary": {"apparatus_units": len(checked), "pob_verses": len({u["reference"] for u in checked}),
                        "categories": dict(Counter(u["category"] for u in checked)),
                        "unbracketed_editorial_units": sum(not u["supplied_prefix"] for u in checked),
                        "partly_supplied_editorial_units": sum(bool(u["supplied_prefix"]) for u in checked),
                        "sp_context_differences": sum(not u["sp_context_matches_pob_context"] for u in checked)},
            "policy": {"new_image_readings": False, "supplied_letters_count_as_visible": False,
                       "every_printed_dot_transcribed": False, "whole_columns_diplomatically_collated": False,
                       "greek_syriac_apparatus_independently_collated": False,
                       "qdr_is_an_independent_manuscript": False, "english_verses_approved": False,
                       "canonical_change_applied": False},
            "checks": checked, "qdr_controls": qdr_controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edition_pdf", type=Path)
    parser.add_argument("sp_directory", type=Path)
    parser.add_argument("qdr_json", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.edition_pdf, args.sp_directory, args.qdr_json)
    if args.verify_only:
        if result != json.loads(OUT.read_text()):
            raise ValueError("saved apparatus check differs from current inputs")
        print("Verified twelve editorial comparison units; no new decipherment or canonical change.")
    else:
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(f"Wrote {OUT}")
    print(json.dumps(result["summary"]))


if __name__ == "__main__":
    main()
