#!/usr/bin/env python3
"""Exact Genesis 4:8 note transaction; never writes canonical or historical data.

Default/--post-check are read-only. --prepare-intent and --confirm-application
only create exclusive, bound ledgers around a separately authorized apply_patch.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration import check_genesis_4_8_note_candidate as candidate_check
from tools.textual_restoration import jeremiah_note_transaction as jeremiah
from tools.textual_restoration import apply_numbers_22_19_note as numbers
from tools import export_mobile_bible as exporter

PREFIX = ROOT / "sources/textual_restoration/applications"
TARGET = ROOT / candidate_check.TARGET
BASELINE = PREFIX / "genesis_4_8_note_baseline.v1.yaml"
CANDIDATE = PREFIX / "genesis_4_8_note_candidate.v1.yaml"
PREFLIGHT = PREFIX / "genesis_4_8_note_preflight.v1.json"
JUDGMENT = PREFIX / "genesis_4_8_note_judgment.v1.json"
INPUTS = PREFIX / "genesis4_8_newtransaction_inputs.v1.json"
REVIEW = PREFIX / "genesis4_8_newtransaction_review.v1.json"
INTENT = PREFIX / "genesis4_8_newtransaction_intent.v1.json"
# This path is already declared by the frozen candidate; do not change it.
APPLICATION = PREFIX / "genesis_4_8_note_application.v1.json"
TESTS = ROOT / "tests/test_genesis_note_transaction.py"
DOC = ROOT / "docs/GENESIS_4_8_NOTE_APPLICATION_2026-09-06.md"
MIGRATION = PREFIX / "genesis4_8_newtransaction_test_migration.v1.json"
CURRENT_TEST = ROOT / "tests/test_unflagged_english_sample.py"
METHOD = ROOT / "METHODOLOGY.md"
REVISION_METHOD = ROOT / "REVISION_METHODOLOGY.md"
JUDGMENT_SHA = "2017263197fe6d548e0b058b975fe68d2b397b3f84e8fed4c93849e5471ed525"
PREFLIGHT_SHA = "2ff3a33072113cdd6629c92020d9b33d77640a14d45d87352c46b2b173a4b5b5"
INPUTS_SHA = "8210c8c59246ae7440660b84b652184e5fd9e52a30a80754d317da671c3f482b"
PACKAGE_ID = "GEN.4.8-speech-disclosure-2026-09-06-v1"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jbytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def package():
    require(__debug__, "frozen replay requires non-optimized Python")
    fixed = {BASELINE: candidate_check.BASELINE_SHA, CANDIDATE: candidate_check.CANDIDATE_SHA,
             JUDGMENT: JUDGMENT_SHA, PREFLIGHT: PREFLIGHT_SHA, INPUTS: INPUTS_SHA}
    for path, digest in fixed.items():
        require(sha(path.read_bytes()) == digest, f"fixed package drift: {path}")
    judgment = json.loads(JUDGMENT.read_text())
    require(judgment['decision'] == 'APPROVE' and judgment['note_only_local_application_approved'] is True,
            "missing exact note approval")
    require(all(judgment[k] is False for k in ('source_priority_promoted', 'main_english_change_approved',
                'whole_verse_reapproved', 'publication_approved')), "approval scope drift")
    frozen, inputs = json.loads(PREFLIGHT.read_text()), json.loads(INPUTS.read_text())
    for pins in (frozen['input_pins'], inputs['prior_package_input_pins'], inputs['unchanged_derivative_context_pins']):
        for rel, expected in pins.items():
            require(sha((ROOT / rel).read_bytes()) == expected, f"bound input drift: {rel}")
    # These two earlier applications are completed, not alternative baseline states.
    for target, candidate_path in ((numbers.ROOT / numbers.TARGET_REL, numbers.CANDIDATE),
                                   (jeremiah.TARGET, jeremiah.CANDIDATE)):
        require(target.read_bytes() == candidate_path.read_bytes(), "prior applied canonical state drift")
    migration_state()
    return BASELINE.read_bytes(), CANDIDATE.read_bytes(), frozen


def migration_state():
    plan = json.loads(MIGRATION.read_text())
    digest = sha(CURRENT_TEST.read_bytes())
    require(plan['target'] == str(CURRENT_TEST.relative_to(ROOT)), "test migration target drift")
    states = {plan['baseline_sha256']: 'baseline', plan['candidate_sha256']: 'candidate'}
    require(digest in states, "unknown current-test migration state")
    return states[digest]


def binding():
    return {'package_id': PACKAGE_ID, 'baseline_sha256': candidate_check.BASELINE_SHA,
            'candidate_yaml_sha256': candidate_check.CANDIDATE_SHA, 'judgment_sha256': JUDGMENT_SHA,
            'frozen_preflight_sha256': PREFLIGHT_SHA, 'dependency_manifest_sha256': INPUTS_SHA,
            'executor_sha256': sha(Path(__file__).read_bytes()), 'tests_sha256': sha(TESTS.read_bytes()),
            'application_document_sha256': sha(DOC.read_bytes()), 'test_migration_sha256': sha(MIGRATION.read_bytes()),
            'general_method_sha256': sha(METHOD.read_bytes()), 'revision_method_sha256': sha(REVISION_METHOD.read_bytes())}


def require_review():
    review = json.loads(REVIEW.read_text())
    require(review.get('scoped_transaction_approved') is True and
            all(review.get(k) == v for k, v in binding().items()), "missing or stale transaction review")


def require_transaction():
    require_review()
    for path, status in ((INTENT, 'prepared'), (APPLICATION, 'applied-verified')):
        if path == APPLICATION and not path.exists():
            continue
        record = json.loads(path.read_text())
        require(record.get('status') == status, "invalid transaction state")
        require(all(record.get(k) == v for k, v in binding().items()) and
                record.get('transaction_review_sha256') == sha(REVIEW.read_bytes()), "transaction provenance drift")
        if path == APPLICATION:
            require(record.get('intent_sha256') == sha(INTENT.read_bytes()), "application intent binding drift")


@contextmanager
def historical_view():
    """Only Genesis baseline overlay; compose older overlays explicitly as needed."""
    raw, candidate, _ = package()
    require(not TARGET.is_symlink() and TARGET.resolve() == TARGET.absolute(), "canonical symlink refused")
    reader, text_reader = Path.read_bytes, Path.read_text
    start = reader(TARGET)
    require(start in (raw, candidate), "unknown Genesis state; historical overlay refused")
    require(not (start == raw and APPLICATION.exists()), "baseline contradicts applied ledger; unrecorded rollback")
    if start == candidate or INTENT.exists():
        require_transaction()
    def read_bytes(path):
        return raw if path == TARGET else reader(path)
    def read_text(path, *args, **kwargs):
        return raw.decode('utf-8') if path == TARGET else text_reader(path, *args, **kwargs)
    try:
        with patch.object(Path, 'read_bytes', read_bytes), patch.object(Path, 'read_text', read_text):
            yield
    finally:
        require(reader(TARGET) == start, "canonical changed during historical replay")


def corpus_digest():
    rows = [(p.relative_to(ROOT).as_posix(), sha(p.read_bytes()))
            for p in sorted((ROOT / 'translation/ot').glob('*/*/*.yaml'))]
    return sha(''.join(f'{p}\0{h}\n' for p, h in rows).encode())


def historical_sample_probe():
    start = corpus_digest()
    with historical_view():
        result = jeremiah.historical_sample_probe()
    actual = corpus_digest()
    require(actual == start, "current corpus changed during historical replay")
    return {'historical_selection_reproduced': result['historical_selection_reproduced'],
            'historical_corpus_digest': result['historical_corpus_digest'],
            'current_corpus_digest': actual, 'current_digest_computed_outside_all_overlays': True,
            'context_files_verified': result['context_files_verified'],
            'overlay_paths': [*result['overlay_paths'], candidate_check.TARGET],
            'genesis_current_sha256': sha(TARGET.read_bytes()),
            'jeremiah_probe_under_genesis_baseline_view': result}


def current_export(raw, candidate, frozen):
    """Three real complete GEN exports; actual is outside all historical overlays."""
    actual = exporter.export_book('GEN')
    original = exporter.load_translation_record
    def export_with(record):
        def loader(book, chapter, verse):
            return copy.deepcopy(record) if (book, chapter, verse) == ('GEN', 4, 8) else original(book, chapter, verse)
        with patch.object(exporter, 'load_translation_record', side_effect=loader):
            return exporter.export_book('GEN')
    before, after = export_with(yaml.safe_load(raw)), export_with(yaml.safe_load(candidate))
    def locate(book):
        return next(v for c in book['chapters'] if c['chapter'] == 4 for v in c['verses'] if v['verse'] == 8)
    for book in (actual, before, after):
        require([c['chapter'] for c in book['chapters']] == list(range(1, 51)) and
                sum(len(c['verses']) for c in book['chapters']) == 1533, "incomplete GEN export")
    for role, book in (('baseline', before), ('candidate', after)):
        require(candidate_check.json_sha(book) == frozen['full_gen_export'][role]['book_json_sha256'],
                f"full GEN {role} export drift")
    control = copy.deepcopy(after)
    row = locate(control)
    row.clear()
    row.update(locate(before))
    require(control == before and locate(after) == frozen['mobile_probe']['draft_verse'], "export scope drift")
    require(actual == (before if TARGET.read_bytes() == raw else after), "actual canonical export differs")
    return {'chapters': 50, 'verses': 1533, 'actual_export_outside_historical_overlays': True,
            'baseline_book_json_sha256': candidate_check.json_sha(before),
            'candidate_book_json_sha256': candidate_check.json_sha(after),
            'actual_book_json_sha256': candidate_check.json_sha(actual),
            'actual_matches_baseline': actual == before, 'actual_matches_candidate': actual == after,
            'all_other_content_unchanged': True, 'actual_verse': locate(actual),
            'source_and_review_metadata_exported': False, 'deployed_reader_checked': False,
            'multilingual_or_simplified_records_synchronized': False}


def check():
    raw, candidate, frozen = package()
    initial_binding, start, test_start = binding(), corpus_digest(), CURRENT_TEST.read_bytes()
    with historical_view():
        require(candidate_check.run() == frozen, "historical candidate preflight mismatch")
    historical = historical_sample_probe()
    exported = current_export(raw, candidate, frozen)
    package()
    require(binding() == initial_binding and corpus_digest() == start, "inputs changed during check")
    require(CURRENT_TEST.read_bytes() == test_start, "current test changed during check")
    return {**initial_binding, 'current_target_sha256': sha(TARGET.read_bytes()),
            'current_test_migration_state': migration_state(), 'current_test_sha256': sha(test_start),
            'candidate_preflight_reproduced_under_explicit_genesis_baseline_overlay': True,
            'historical_sample': historical, 'current_export': exported,
            'unchanged_derivative_records_pinned': len(json.loads(INPUTS.read_text())['unchanged_derivative_context_pins']),
            'canonical_change_applied_by_check': False, 'source_changed': False, 'main_prose_changed': False,
            'whole_verse_reapproved': False, 'earliest_source_form_promoted': False, 'publication_ready': False}


def prepare():
    require(not INTENT.exists() and not APPLICATION.exists(), "transaction already exists")
    require_review()
    review_raw, start_binding = REVIEW.read_bytes(), binding()
    result = check()
    require(TARGET.read_bytes() == BASELINE.read_bytes(), "prepare requires exact canonical baseline")
    require_review()
    require(REVIEW.read_bytes() == review_raw and binding() == start_binding, "review or binding changed during prepare")
    record = {**start_binding, 'status': 'prepared', 'prepared_at': datetime.now(timezone.utc).isoformat(),
              'transaction_review_sha256': sha(review_raw), 'preflight': result,
              'canonical_edit_mechanism': 'Separate authorized apply_patch; no canonical writer in this tool'}
    numbers.write_once(INTENT, record)
    return record


def complete():
    require(not APPLICATION.exists(), "application already exists")
    require_transaction()
    review_raw, intent_raw, start_binding = REVIEW.read_bytes(), INTENT.read_bytes(), binding()
    require(TARGET.read_bytes() == CANDIDATE.read_bytes(), "completion requires exact applied candidate")
    result = check()
    require(result['current_export']['actual_matches_candidate'], "actual canonical export differs from candidate")
    require_transaction()
    require(REVIEW.read_bytes() == review_raw and INTENT.read_bytes() == intent_raw and binding() == start_binding,
            "provenance changed during completion")
    require(TARGET.read_bytes() == CANDIDATE.read_bytes(), "candidate changed before completion")
    record = {**start_binding, 'status': 'applied-verified', 'completed_at': datetime.now(timezone.utc).isoformat(),
              'transaction_review_sha256': sha(review_raw), 'intent_sha256': sha(intent_raw), 'post_application': result,
              'canonical_note_change_applied': True, 'source_changed': False, 'main_prose_changed': False,
              'whole_verse_reapproved': False, 'earliest_source_form_promoted': False, 'publication_ready': False}
    numbers.write_once(APPLICATION, record)
    return record


def post_check():
    require(APPLICATION.exists(), "post-check requires completed application")
    require_transaction()
    ledgers = {p: p.read_bytes() for p in (REVIEW, INTENT, APPLICATION)}
    require(TARGET.read_bytes() == CANDIDATE.read_bytes(), "post-check requires exact applied candidate")
    result = check()
    require_transaction()
    require(all(p.read_bytes() == raw for p, raw in ledgers.items()), "ledger changed during post-check")
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--prepare-intent', action='store_true')
    group.add_argument('--confirm-application', action='store_true')
    group.add_argument('--post-check', action='store_true')
    args = parser.parse_args()
    action = prepare if args.prepare_intent else complete if args.confirm_application else post_check if args.post_check else check
    print(json.dumps(action(), ensure_ascii=False, sort_keys=True, indent=2))
