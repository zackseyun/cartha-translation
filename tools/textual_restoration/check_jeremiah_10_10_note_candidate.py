#!/usr/bin/env python3
"""Read-only Jeremiah 10:10 note candidate scope/schema/full-book export preflight."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.build_application_draft import mobile_probe, note_markers

PREFIX = "sources/textual_restoration/applications/jeremiah_10_10_note_"
TARGET = "translation/ot/jeremiah/010/010.yaml"
BASELINE_SHA = "cb5391f363a7fd7ea7b5433f3825e2ef59c7624f3f9263f9b9d1cc87fb0c3661"
CANDIDATE_SHA = "903ec558e3f00594d8e8b5a70e8e66cac3a0cff957ea28d42466dc35cc387fbb"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def run():
    baseline_raw = (ROOT / (PREFIX + "baseline.v1.yaml")).read_bytes()
    candidate_raw = (ROOT / (PREFIX + "candidate.v1.yaml")).read_bytes()
    assert sha(baseline_raw) == BASELINE_SHA, "Baseline snapshot drift"
    assert sha(candidate_raw) == CANDIDATE_SHA, "Candidate drift"
    current_raw = (ROOT / TARGET).read_bytes()
    assert current_raw == baseline_raw, "This unapplied preflight requires canonical baseline"
    before, after = yaml.safe_load(baseline_raw), yaml.safe_load(candidate_raw)
    assert before["id"] == after["id"] == "JER.10.10"
    expected_translation = copy.deepcopy(before["translation"])
    expected_translation["text"] += "[d]"
    expected_translation["footnotes"].append(after["translation"]["footnotes"][-1])
    assert after["translation"] == expected_translation
    assert after["translation"]["footnotes"][-1]["marker"] == "d"
    assert after["translation"]["footnotes"][-1]["reason"] == "textual_variant"
    assert re.sub(r"\[[a-z]+\]", "", before["translation"]["text"]) == re.sub(r"\[[a-z]+\]", "", after["translation"]["text"])
    note_markers(after["translation"])
    allowed = {"translation", "status", "revision_pass", "cross_check", "review_history", "note_application"}
    assert set(after) == (set(before) - {"revision_pass"}) | {"review_history", "note_application"}
    for field in set(before) - allowed:
        assert before[field] == after[field], field
    expected_history = [
        {"field": field, "value": before[field],
         "archived_from_baseline_sha256": BASELINE_SHA,
         "historical_review_input_binding": "not-verified", "certifies_this_candidate": False}
        for field in ("status", "revision_pass", "cross_check")
    ]
    assert after["review_history"] == expected_history
    assert after["status"] == "draft"
    assert after["cross_check"] == {"status": "needs_review"}
    for field in ("whole_verse_reapproved", "earliest_source_form_promoted", "publication_approval"):
        assert after["note_application"][field] is False
    schema = ROOT / "schema/verse.schema.json"
    validator = Draft202012Validator(json.loads(schema.read_text()))
    def errors(record):
        return [{"path": "/".join(map(str, e.absolute_path)), "message": e.message}
                for e in validator.iter_errors(record)]
    baseline_errors, candidate_errors = errors(before), errors(after)
    assert candidate_errors == [], candidate_errors
    probe = mobile_probe(before, after)
    assert probe["all_other_exported_book_content_unchanged"]
    assert probe["draft_english_preserved"] and probe["draft_note_bodies_preserved"]
    assert not any(field in probe["draft_verse"] for field in ("cross_check", "review_history", "note_application"))
    assert (ROOT / TARGET).read_bytes() == current_raw, "Canonical target changed during check"
    pins = [
        "docs/JEREMIAH_10_LITERARY_FORM_COMPARISON_2026-09-05.md",
        "sources/textual_restoration/discovery/jeremiah10_literary_forms.v1.json",
        "docs/TEXTUAL_ADJUDICATION_METHOD.md",
        "tools/prompts/revision_policy.md",
        "DOCTRINE.md",
        "schema/verse.schema.json",
        "tools/export_mobile_bible.py",
        "tools/textual_restoration/build_application_draft.py",
        "tools/textual_restoration/check_jeremiah_10_10_note_candidate.py",
    ]
    return {
        "package_id": "JER.10.10-literary-form-disclosure-2026-09-05-v1",
        "status": "unapplied-candidate-preflight",
        "target": TARGET,
        "baseline_sha256": BASELINE_SHA,
        "candidate_yaml_sha256": CANDIDATE_SHA,
        "input_pins": {path: sha((ROOT / path).read_bytes()) for path in pins},
        "scope_check": {"source_unchanged": True, "main_english_unchanged": True,
                        "existing_three_notes_and_anchors_unchanged": True,
                        "only_added_anchor": "final whole-verse [d]",
                        "complete_historical_values_archived": True,
                        "historical_review_inputs_verified": False},
        "schema_check": {"baseline_errors": baseline_errors, "candidate_errors": candidate_errors},
        "mobile_probe": probe,
        "canonical_change_applied": False,
        "independent_review_completed": False,
        "earliest_source_form_promoted": False,
        "whole_verse_reapproved": False,
        "publication_approved": False,
        "limits": ["Existing a/b/c anchor and LORD-metadata defects remain outside scope.",
                   "A local export checks transport, not manuscript accuracy or deployed reader behavior.",
                   "No independent note judgment or application transaction is implemented by this checker."]
    }

if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
