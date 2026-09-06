#!/usr/bin/env python3
"""Read-only exact Genesis 4:8 note scope, schema and full-GEN export preflight."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from unittest.mock import patch

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.build_application_draft import mobile_probe, note_markers

PREFIX = "sources/textual_restoration/applications/genesis_4_8_note_"
TARGET = "translation/ot/genesis/004/008.yaml"
BASELINE_SHA = "7552677368239e42f115445ef63b0bfdf9d774677790ffc49214e818837da426"
CANDIDATE_SHA = "81e5cd475506a97c8acfd1bcbc353a7c6ffa2b5c27a942a7fff53d8b6865973f"
PLAN_SHA = "97a77a0d6e844dc6a1073bde68a8200c957087bda5329d255237c27639a6095b"
REVIEW = "sources/textual_restoration/discovery/source_workstreams_review.2026-09-06.v1.json"
REVIEW_SHA = "48f301c1ac864fcebf68be0f08d98f821638ae06d8072ecb086091ba126a2fe7"
DOSSIER = "sources/textual_restoration/discovery/genesis4_8_comparison.v1.json"
REPORT = "docs/GENESIS_4_8_SOURCE_COMPARISON_2026-09-06.md"
ALLOWED_EDITS = {
    ("translation", "footnotes", 0, "text"),
    *(('lexical_decisions', 3, key) for key in ('alternatives', 'lexicon', 'rationale')),
    *(('theological_decisions', 0, key) for key in ('chosen_reading', 'alternative_readings', 'rationale')),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_sha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def validate_records(before, after, plan, approved_note):
    """Reject every unlisted change, including archive truncation and stale flags."""
    expected = copy.deepcopy(before)
    paths = [tuple(edit['path']) for edit in plan['edits']]
    require(len(paths) == len(ALLOWED_EDITS) and set(paths) == ALLOWED_EDITS, "Unexpected edit paths")
    for edit in plan['edits']:
        obj = expected
        for key in edit['path'][:-1]:
            obj = obj[key]
        key = edit['path'][-1]
        require(obj[key] == edit['from'], f"Stale edit baseline: {edit['path']}")
        obj[key] = copy.deepcopy(edit['to'])
    expected['review_history'] = [
        {'field': field, 'value': copy.deepcopy(before[field]),
         'archived_from_baseline_sha256': BASELINE_SHA,
         'historical_review_input_binding': 'not-verified', 'certifies_this_candidate': False}
        for field in ('status', 'revision_pass', 'cross_check')
    ]
    expected.pop('revision_pass')
    expected['status'] = 'draft'
    expected['cross_check'] = {'status': 'needs_review'}
    application_edits = [edit for edit in plan['metadata_edits'] if edit['field'] == 'note_application']
    require(len(application_edits) == 1, "Missing or duplicated application declaration")
    expected['note_application'] = copy.deepcopy(application_edits[0]['to'])
    require(after == expected, "Unlisted record change or inexact historical archive")
    require(after['translation']['footnotes'][0]['text'] == approved_note, "Unapproved note text")
    require(after['id'] == before['id'] == 'GEN.4.8', "Wrong target")
    require(after['source'] == before['source'], "Source changed")
    require(after['translation']['text'] == before['translation']['text'], "Main English or anchor changed")
    require(after['revisions'] == before['revisions'], "Historical revisions changed")
    for field in ('whole_verse_reapproved', 'earliest_source_form_promoted', 'publication_approval'):
        require(after['note_application'][field] is False, "Approval boundary changed")
    require(after['note_application']['baseline_sha256'] == BASELINE_SHA, "Archive baseline mismatch")
    note_markers(after['translation'])


def run():
    paths = {PREFIX + 'baseline.v1.yaml': BASELINE_SHA,
             PREFIX + 'candidate.v1.yaml': CANDIDATE_SHA,
             PREFIX + 'plan.v1.json': PLAN_SHA, REVIEW: REVIEW_SHA}
    raw = {path: (ROOT / path).read_bytes() for path in paths}
    for path, digest in paths.items():
        require(sha(raw[path]) == digest, f"Pinned package changed: {path}")
    baseline_raw, candidate_raw = raw[PREFIX + 'baseline.v1.yaml'], raw[PREFIX + 'candidate.v1.yaml']
    require((ROOT / TARGET).read_bytes() == baseline_raw, "Unapplied preflight requires exact canonical baseline")
    plan, review = json.loads(raw[PREFIX + 'plan.v1.json']), json.loads(raw[REVIEW])
    require(review['decision'] == 'PASS' and review['genesis4_8']['exact_proposed_note_precision_and_readability'] == 'PASS', "Missing substantive approval")
    for path in (DOSSIER, REPORT):
        require(sha((ROOT / path).read_bytes()) == review['package_bindings_sha256'][path], f"Stale source review: {path}")
    note = json.loads((ROOT / DOSSIER).read_text())['reader_proposal']['exact_note_text']
    require(sha(note.encode()) == review['genesis4_8']['note_text_utf8_sha256'], "Approved note hash mismatch")
    require(review['genesis4_8']['baseline_sha256'] == BASELINE_SHA, "Stale source review baseline")
    before, after = yaml.safe_load(baseline_raw), yaml.safe_load(candidate_raw)
    validate_records(before, after, plan, note)
    source = lambda data: re.search(rb'(?ms)^source:\n.*?(?=^translation:)', data).group()
    english = lambda data: re.search(rb'(?m)^  text: And Cain.*$', data).group()
    require(source(baseline_raw) == source(candidate_raw), "Source YAML bytes changed")
    require(english(baseline_raw) == english(candidate_raw), "English YAML bytes changed")
    validator = Draft202012Validator(json.loads((ROOT / 'schema/verse.schema.json').read_text()))
    errors = lambda obj: [{'path': '/'.join(map(str, e.absolute_path)), 'message': e.message}
                          for e in validator.iter_errors(obj)]
    require(errors(after) == [], "Candidate schema errors")

    # Pin every GEN input around both real exports, not merely the target record.
    snapshot = lambda: {str(p.relative_to(ROOT)): sha(p.read_bytes())
                        for p in sorted((ROOT / 'translation/ot/genesis').glob('*/*.yaml'))}
    book_before = snapshot()
    from tools import export_mobile_bible as exporter
    export = exporter.export_book
    exports = []

    def capture(code):
        require(code == 'GEN', "Wrong exported book")
        book = export(code)
        exports.append({'chapters': [c['chapter'] for c in book['chapters']],
                        'verses': sum(len(c['verses']) for c in book['chapters']),
                        'book_json_sha256': json_sha(book)})
        return book

    with patch.object(exporter, 'export_book', side_effect=capture):
        probe = mobile_probe(before, after)
    require(len(exports) == 2, "Expected baseline and candidate full exports")
    require(all(e['chapters'] == list(range(1, 51)) and e['verses'] == 1533 for e in exports), "Incomplete GEN export")
    for field in ('all_other_exported_book_content_unchanged', 'draft_english_preserved', 'draft_note_bodies_preserved'):
        require(probe[field], f"Export mismatch: {field}")
    require(set(probe['draft_verse']) == {'verse', 'text', 'footnotes'}, "Unexpected mobile fields")
    require(snapshot() == book_before, "GEN input changed during preflight")
    require((ROOT / TARGET).read_bytes() == baseline_raw, "Canonical target changed")
    pins = list(paths) + [DOSSIER, REPORT, 'schema/verse.schema.json',
        'docs/SOURCE_NEAR_EDITORIAL_STANDARD.md', 'docs/REVISION_PROCESS.md',
        'docs/TEXTUAL_ADJUDICATION_METHOD.md', 'tools/prompts/revision_policy.md', 'DOCTRINE.md',
        'tools/textual_restoration/check_genesis_4_8_note_candidate.py',
        'tests/test_genesis_4_8_note_candidate.py', 'tools/textual_restoration/build_application_draft.py',
        'tools/export_mobile_bible.py', 'tools/wlc.py', 'tools/sblgnt.py', 'tools/draft.py',
        'tools/lxx_swete.py', 'tools/terminology_policy.py', 'tools/extra_texts/catalog.py',
        'sources/ot/wlc/Gen.xml']
    return {'schema_version': '1.0.0', 'package_id': plan['package_id'],
        'status': 'unapplied-candidate-preflight', 'target': TARGET,
        'baseline_sha256': BASELINE_SHA, 'candidate_yaml_sha256': CANDIDATE_SHA,
        'input_pins': {p: sha((ROOT / p).read_bytes()) for p in pins},
        'scope_check': {'entire_expected_record_matches': True, 'source_yaml_byte_identical': True,
            'main_english_and_anchor_byte_identical': True, 'exact_approved_note': True,
            'only_connected_invitation_metadata_changed': True, 'full_old_review_values_archived': True,
            'historical_review_inputs_verified': False, 'fresh_HALOT_consultation': False},
        'schema_check': {'baseline_errors': errors(before), 'candidate_errors': errors(after)},
        'full_gen_export': {'book': 'GEN', 'baseline': exports[0], 'candidate': exports[1],
            'canonical_yaml_records': len(book_before), 'canonical_manifest_json_sha256': json_sha(book_before),
            'all_canonical_GEN_bytes_unchanged_during_check': True},
        'mobile_probe': probe,
        'mobile_source_boundary': 'Mobile exporter omits source and review metadata by design; source bytes verified in YAML, not falsely reported as mobile transport.',
        'substantive_note_proposal_approved': True, 'exact_candidate_independent_judgment_completed': False,
        'canonical_change_applied': False, 'transaction_implemented': False,
        'earliest_source_form_promoted': False, 'whole_verse_reapproved': False, 'publication_approved': False}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
