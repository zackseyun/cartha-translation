#!/usr/bin/env python3
"""Check pinned context/locators and conservative boundaries, not textual truth."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "sources/textual_restoration/discovery/jeremiah10_literary_forms.v1.json"


def check() -> None:
    record = json.loads(RECORD.read_text())
    expected_paths = {
        f"translation/ot/jeremiah/010/{verse:03d}.yaml" for verse in range(3, 14)
    }
    if set(record["pob_context_pins"]) != expected_paths:
        raise ValueError("Expected complete pinned POB context10:3–13")
    for relative, expected in record["pob_context_pins"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"POB context changed: {relative}")
    book_map = json.loads((ROOT / record["qdr"]["book_map"]).read_text())
    # Locate the book object without depending on unrelated metadata keys.
    def objects(value):
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from objects(child)
        elif isinstance(value, list):
            for child in value:
                yield from objects(child)

    jeremiah = next(obj for obj in objects(book_map) if obj.get("book") == "jeremiah")
    indexed = {item["label"]: item for item in jeremiah["source_records"]}
    for crosswalk in record["qdr"]["label_crosswalk"]:
        if indexed[crosswalk["qdr_label"]]["source_record_index"] != crosswalk["source_record_index"]:
            raise ValueError("QDR label/ordinal mismatch")
    if indexed["4Q71"]["bracket_syntax_word_counts"]["unresolved_fragment_bracket_syntax"] == 0:
        raise ValueError("4Q71 bracket caveat requires review")
    assessment = record["assessment"]
    for field in ("source_or_english_changed", "newly_recovered_letters", "independent_review_completed", "all_jeremiah_coverage_claimed", "generated_image_evidence"):
        if assessment[field] is not False:
            raise ValueError(f"Research-only boundary changed: {field}")
    for field in ("canonical_changes", "coverage_records_added", "registry_entries_added"):
        if assessment[field] != 0:
            raise ValueError(f"Research-only count changed: {field}")
    if record["greek_controls"]["all_greek_omits_verse10"] is not False:
        raise ValueError("Greek marginal counterevidence erased")
    if record["greek_controls"]["opposing_verse10_apparatus"]["siglum"] != "Qmg":
        raise ValueError("Marginal witness attribution changed; review required")
    if record["literary_forms"]["full_verse10_hebrew_survival_claim"] is not False:
        raise ValueError("Supplied verse10 wording promoted to surviving ink")
    aramaic = next(unit for unit in record["published_preservation_units"] if unit["id"] == "4q71-line7")
    if aramaic["language"] != "Aramaic":
        raise ValueError("Verse11 language must remain Aramaic")
    if not (ROOT / record["report"]).is_file():
        raise ValueError("Missing companion report")
    print("Jeremiah10: 11 pinned context files, 3 label/ordinal mappings, research boundaries OK; scholarly truth not certified")


if __name__ == "__main__":
    check()
