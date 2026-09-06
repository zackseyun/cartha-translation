#!/usr/bin/env python3
"""Read-only versioned Jeremiah note preflight; v1 evidence/checker stay immutable."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import re
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration import check_jeremiah_10_10_note_candidate as v1

CANDIDATE_SHA = "ae7d4a731f43fa6a29eca05e0d4c2fcd35c17a06d2dde0837fa7da957eaa9d4a"
AFTER_TEXT = "But Yahweh[a] is the true God[b]; he is the living God and the everlasting King[c]. At his wrath the earth quakes, and the nations cannot endure his indignation.[d]"

def run(version=2):
    if version == 1:
        return v1.run()
    if version != 2:
        raise ValueError("Unsupported version")
    baseline_raw = (ROOT / (v1.PREFIX + "baseline.v1.yaml")).read_bytes()
    first_raw = (ROOT / (v1.PREFIX + "candidate.v1.yaml")).read_bytes()
    candidate_raw = (ROOT / (v1.PREFIX + "candidate.v2.yaml")).read_bytes()
    assert v1.sha(baseline_raw) == v1.BASELINE_SHA
    assert v1.sha(first_raw) == v1.CANDIDATE_SHA
    assert v1.sha(candidate_raw) == CANDIDATE_SHA
    assert (ROOT / v1.TARGET).read_bytes() == baseline_raw, "Unapplied preflight requires canonical baseline"
    before, first, after = map(yaml.safe_load, (baseline_raw, first_raw, candidate_raw))
    expected = copy.deepcopy(first)
    expected["translation"]["text"] = AFTER_TEXT
    expected["translation"]["footnotes"][0]["text"] = before["translation"]["footnotes"][0]["text"].replace("And the LORD", "And Yahweh")
    expected["lexical_decisions"][0].update({
        "chosen": "But Yahweh", "alternatives": ["And Yahweh"],
        "rationale": "The divine name יהוה is rendered 'Yahweh' under current POB policy. The prefixed conjunction can be simply connective ('and') or mildly adversative in context; here 'But' reflects the contrast with the idols in the preceding context."})
    expected["theological_decisions"][1].update({
        "chosen_reading": "But Yahweh", "alternative_readings": ["And Yahweh"],
        "rationale": "The immediate literary context contrasts Yahweh with idols; 'But Yahweh' expresses that contrast, while 'And Yahweh' preserves the connective alternative noted in footnote a."})
    application = expected["note_application"]
    for key in ("package_id", "independent_note_review", "application_receipt"):
        application[key] = application[key].replace("v1", "v2")
    application["scope"] = "Literary-form disclosure, three note-anchor repairs, and related divine-name metadata synchronization; no source or main-prose change"
    application["existing_lexicon_citations_role"] = "Historical draft citations retained; no fresh HALOT consultation claimed"
    assert after == expected, "Unlisted component change"
    assert before["source"] == after["source"]
    source_block = lambda raw: re.search(rb"(?ms)^source:\n.*?(?=^translation:)", raw).group()
    assert source_block(baseline_raw) == source_block(candidate_raw), "Source YAML byte component changed"
    plain = lambda text: re.sub(r"\[[a-z]+\]", "", text)
    assert plain(before["translation"]["text"]) == plain(after["translation"]["text"])
    assert after["translation"]["footnotes"][1:3] == before["translation"]["footnotes"][1:3]
    v1.note_markers(after["translation"])
    assert re.findall(r"\[([a-z]+)\]", AFTER_TEXT) == ["a", "b", "c", "d"]
    assert after["review_history"] == [
        {"field": field, "value": before[field], "archived_from_baseline_sha256": v1.BASELINE_SHA,
         "historical_review_input_binding": "not-verified", "certifies_this_candidate": False}
        for field in ("status", "revision_pass", "cross_check")]
    assert after["status"] == "draft" and after["cross_check"] == {"status": "needs_review"}
    assert "revision_pass" not in after
    validator = Draft202012Validator(json.loads((ROOT / "schema/verse.schema.json").read_text()))
    def errors(record):
        return [{"path": "/".join(map(str, e.absolute_path)), "message": e.message}
                for e in validator.iter_errors(record)]
    assert errors(after) == []
    probe = v1.mobile_probe(before, after)
    assert all(probe[k] for k in ("all_other_exported_book_content_unchanged", "draft_english_preserved", "draft_note_bodies_preserved"))
    assert not any(k in probe["draft_verse"] for k in ("review_history", "cross_check", "note_application"))
    assert (ROOT / v1.TARGET).read_bytes() == baseline_raw, "Canonical target changed"
    paths = [v1.PREFIX + suffix for suffix in ("baseline.v1.yaml", "candidate.v1.yaml", "plan.v1.json", "preflight.v1.json", "candidate.v2.yaml", "plan.v2.json")]
    paths += ["tools/textual_restoration/check_jeremiah_10_10_note_candidate.py",
              "tools/textual_restoration/check_jeremiah_10_10_note_candidate_v2.py",
              "tools/textual_restoration/build_application_draft.py", "tools/export_mobile_bible.py",
              "schema/verse.schema.json", "docs/SOURCE_NEAR_EDITORIAL_STANDARD.md", "docs/REVISION_PROCESS.md",
              "DOCTRINE.md", "tools/prompts/revision_policy.md", "docs/TEXTUAL_ADJUDICATION_METHOD.md",
              "docs/JEREMIAH_10_LITERARY_FORM_COMPARISON_2026-09-05.md",
              "sources/textual_restoration/discovery/jeremiah10_literary_forms.v1.json"]
    return {
        "package_id": application["package_id"], "status": "unapplied-candidate-preflight",
        "baseline_sha256": v1.BASELINE_SHA, "candidate_yaml_sha256": CANDIDATE_SHA,
        "target": v1.TARGET, "input_pins": {p: v1.sha((ROOT / p).read_bytes()) for p in paths},
        "scope_check": {"entire_expected_record_matches": True, "source_yaml_component_byte_identical": True,
                        "main_english_unchanged": True, "existing_notes_b_c_unchanged": True,
                        "anchors_match_respective_phrases": True, "opening_name_metadata_synchronized": True,
                        "complete_historical_values_archived": True, "historical_review_inputs_verified": False,
                        "fresh_HALOT_consultation": False},
        "schema_check": {"baseline_errors": errors(before), "candidate_errors": errors(after)},
        "mobile_probe": probe, "canonical_change_applied": False, "independent_review_completed": False,
        "earliest_source_form_promoted": False, "whole_verse_reapproved": False, "publication_approved": False,
        "limits": ["A local export checks transport, not manuscript accuracy or deployed reader behavior.",
                   "No independent note judgment or application transaction is implemented by this checker.",
                   "Historical lexicon citations and unrelated reasoning are retained without fresh verification."]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", choices=(1, 2), type=int, default=2)
    print(json.dumps(run(parser.parse_args().version), ensure_ascii=False, sort_keys=True, indent=2))
