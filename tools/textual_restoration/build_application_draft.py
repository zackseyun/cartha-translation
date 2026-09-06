#!/usr/bin/env python3
"""Materialize a bounded review draft, never apply it to canonical translation.

This is a staging/preflight tool, not an approval or publication mechanism.
The CLI can write only its fixed research-artifact paths with --write.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
from unittest.mock import patch

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PLAN = ROOT / 'sources/textual_restoration/applications/deut32_8_draft_plan.v1.json'
SELECTION = ROOT / 'sources/textual_restoration/selections/ot_critical_source_pilot.v1.json'
OUTPUT = PLAN.parent
PREFLIGHT_NAME = 'deut32_8_preflight.v2.json'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def unpointed(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn' and c != '/')


def note_markers(translation: dict) -> None:
    markers = [n['marker'] for n in translation.get('footnotes', [])]
    inline = re.findall(r'\[([a-z]+)\]', translation['text'])
    if len(markers) != len(set(markers)) or set(inline) != set(markers):
        raise ValueError('Inline footnote markers and note bodies must match uniquely')


def draft_record(raw: bytes, selection: dict, plan: dict) -> dict:
    """Compose one provisional record with a hash-pinned whole-file baseline."""
    if sha(raw) != selection['baseline']['sha256']:
        raise ValueError('Canonical baseline drift')
    if plan['selection_id'] != selection['id'] or plan['status'] != 'unapproved-draft':
        raise ValueError('Plan must identify this selection and remain unapproved')
    if selection['promotion_status'] != 'not-promoted' or selection['canonical_change_applied']:
        raise ValueError('This tool stages unpromoted research only')
    if selection['generated_images_used']:
        raise ValueError('Generated images cannot support a source draft')
    before = yaml.safe_load(raw)
    if before['reference'] != selection['reference']:
        raise ValueError('Reference mismatch')
    baseline = selection['baseline']
    if (before['source']['edition'] != baseline['declared_source_edition']
            or before['source']['text'] != baseline['declared_source_text']
            or before['translation']['text'] != baseline['english_text']):
        raise ValueError('Selection baseline fields do not match canonical record')
    out = copy.deepcopy(before)
    change = plan['source_replacement']
    if change['to'] != selection['critical_source']['normalized_variation_unit']:
        raise ValueError('Draft source replacement differs from working selection')
    text = unpointed(before['source']['text'])
    if text.count(change['from']) != 1:
        raise ValueError('Source replacement must match exactly one bounded phrase')
    # No new vocalization or accentuation is inferred. This is an editorial
    # composite of the normalized baseline plus one explicit proposed unit.
    out['source'] = {
        'edition': 'POB-critical-draft',
        'language': 'Hebrew',
        'text': text.replace(change['from'], change['to']),
        'note': plan['source_disclosure'],
        'apparatus': copy.deepcopy(plan['source_apparatus']),
    }
    old_rendering = plan['english_replacement_from']
    if out['translation']['text'].count(old_rendering) != 1:
        raise ValueError('English replacement must match exactly one phrase')
    out['translation']['text'] = out['translation']['text'].replace(
        old_rendering, selection['english_candidate']['rendering'])
    plain = re.sub(r'\[[a-z]+\]', '', out['translation']['text'])
    if plain != selection['english_candidate']['full_verse_text']:
        raise ValueError('Draft English differs from the bound selection candidate')
    notes = out['translation']['footnotes']
    matches = [n for n in notes if n['marker'] == plan['note_replacement']['marker']]
    if len(matches) != 1:
        raise ValueError('Note replacement must match one marker')
    matches[0].update(plan['note_replacement'])
    note_markers(out['translation'])

    for key, selector in (('lexical_decisions', 'source_word'),
                          ('theological_decisions', 'issue')):
        edit = plan[key]
        entries = [e for e in out[key] if e.get(selector) == edit['match']]
        if len(entries) != 1:
            raise ValueError(f'{key} replacement must match one entry')
        entries[0].clear()
        entries[0].update(copy.deepcopy(edit['replacement']))

    # Old flags are archival observations, not approvals of the candidate.
    # The current baseline hash identifies what we archived; it is NOT a
    # fabricated input hash for the historical review's unavailable payload.
    history = out.setdefault('review_history', [])
    for key in ('cross_check', 'revision_pass'):
        if key in out:
            history.append({
                'field': key, 'value': out.pop(key),
                'archived_from_baseline_sha256': sha(raw),
                'historical_review_input_binding': 'not-verified',
                'certifies_this_candidate': False,
            })
    out['status'] = 'draft'
    out['cross_check'] = {'status': 'needs_review'}
    out['restoration_draft'] = {
        'selection_id': selection['id'], 'approved': False,
        'source_composition': 'unpointed-baseline-plus-one-proposed-unit',
        'entire_verse_attested_in_selected_fragment': False,
        'ai_draft_metadata_role': 'historical-original-draft-not-current-approval',
        'review_gates': copy.deepcopy(selection['review_gates']),
    }
    return out


def mobile_probe(before: dict, candidate: dict) -> dict:
    """Exercise the real full-book exporter using a one-record memory overlay.

    No canonical file, generated app bundle, or deployed reader is modified.
    """
    from tools import export_mobile_bible as exporter
    code, chapter, verse = before['id'].split('.')
    chapter, verse = int(chapter), int(verse)
    baseline_book = exporter.export_book(code)
    original_loader = exporter.load_translation_record

    def overlay(book, ch, vn):
        if (book, ch, vn) == (code, chapter, verse):
            return copy.deepcopy(candidate)
        return original_loader(book, ch, vn)

    with patch.object(exporter, 'load_translation_record', side_effect=overlay):
        draft_book = exporter.export_book(code)

    def locate(book):
        return next(v for c in book['chapters'] if c['chapter'] == chapter
                    for v in c['verses'] if v['verse'] == verse)

    actual_before, actual_after = locate(baseline_book), locate(draft_book)
    control = copy.deepcopy(draft_book)
    target = locate(control)
    target.clear()
    target.update(actual_before)
    return {
        'mode': 'actual-full-book-exporter-with-one-record-in-memory-overlay',
        'baseline_verse': actual_before,
        'draft_verse': actual_after,
        'all_other_exported_book_content_unchanged': control == baseline_book,
        'draft_english_preserved': actual_after.get('text') == candidate['translation']['text'],
        'draft_note_bodies_preserved': actual_after.get('footnotes') == candidate['translation']['footnotes'],
        'draft_source_preserved': actual_after.get('source') == candidate['source'],
        'deployed_reader_checked': False,
    }


def build(root: Path = ROOT, probe=mobile_probe) -> tuple[dict, dict]:
    plan_path = root / PLAN.relative_to(ROOT)
    selection_path = root / SELECTION.relative_to(ROOT)
    plan_raw, selection_raw = plan_path.read_bytes(), selection_path.read_bytes()
    plan = json.loads(plan_raw)
    records = json.loads(selection_raw)['selections']
    matches = [r for r in records if r['id'] == plan['selection_id']]
    if len(matches) != 1:
        raise ValueError('Selection ID absent or duplicated')
    selection = matches[0]
    path = (root / selection['baseline']['repo_path']).resolve()
    if not path.is_relative_to((root / 'translation/ot').resolve()) or not path.is_file():
        raise ValueError('Canonical baseline path outside OT translation')
    raw = path.read_bytes()
    before = yaml.safe_load(raw)
    candidate = draft_record(raw, selection, plan)
    schema_raw = (root / 'schema/verse.schema.json').read_bytes()
    validator = Draft202012Validator(json.loads(schema_raw))
    schema_errors = lambda record: [
        {'path': '/'.join(map(str, e.absolute_path)), 'message': e.message}
        for e in sorted(validator.iter_errors(record), key=lambda e: str(e.absolute_path))
    ]
    exported = probe(before, candidate)
    if sha(path.read_bytes()) != sha(raw):
        raise ValueError('Canonical baseline changed during preflight')
    inputs = {
        'baseline': {'path': str(path.relative_to(root)), 'sha256': sha(raw)},
        'selection': {'path': str(selection_path.relative_to(root)), 'sha256': sha(selection_raw)},
        'plan': {'path': str(plan_path.relative_to(root)), 'sha256': sha(plan_raw)},
        'verse_schema_sha256': sha(schema_raw),
        'exporter_sha256': sha((root / 'tools/export_mobile_bible.py').read_bytes()),
        'builder_sha256': sha((root / 'tools/textual_restoration/build_application_draft.py').read_bytes()),
    }
    evidence = []
    for relative in plan['evidence_paths']:
        evidence_path = (root / relative).resolve()
        if not evidence_path.is_relative_to((root / 'sources/textual_restoration').resolve()) or not evidence_path.is_file():
            raise ValueError('Evidence path missing or outside restoration sources')
        evidence.append({'path': relative, 'sha256': sha(evidence_path.read_bytes())})
    inputs['evidence'] = evidence
    receipt = {
        'schema_version': '1.0.0', 'checked_date': plan['checked_date'],
        'status': 'unapproved-draft-not-application-receipt',
        'baseline_snapshot_path': 'sources/textual_restoration/applications/deut32_8_baseline.v1.yaml',
        'inputs': inputs, 'candidate_json_sha256': sha(json_bytes(candidate)),
        'components': {
            key: {'before_sha256': sha(json_bytes(before.get(key))),
                  'after_sha256': sha(json_bytes(candidate.get(key))),
                  'changed': before.get(key) != candidate.get(key)}
            for key in sorted(set(before) | set(candidate))
        },
        'schema_check': {'baseline_errors': schema_errors(before),
                         'candidate_errors': schema_errors(candidate)},
        'mobile_probe': exported,
        'review_gates': copy.deepcopy(selection['review_gates']),
        'publication_ready': False, 'canonical_change_applied': False,
        'applier_implemented': False,
        'limits': [
            'Draft construction is not source adjudication or independent review.',
            'The full-verse draft does not complete the selection full-verse gate.',
            'Historical review inputs were not verified; archived flags are not reapproved.',
            'This probes the local mobile export, not website/CDN consumers or deployment.',
            'A complete reviewed application transaction and receipts remain unimplemented.'
        ],
    }
    return candidate, receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write fixed research outputs, never canonical files')
    args = parser.parse_args()
    candidate, receipt = build()
    if args.write:
        # Fixed paths, no user-controlled output root or canonical apply option.
        if OUTPUT.resolve() != OUTPUT:
            raise ValueError('Research output directory must not traverse a symlink')
        OUTPUT.mkdir(parents=True, exist_ok=True)
        baseline = (ROOT / receipt['inputs']['baseline']['path']).read_bytes()
        if sha(baseline) != receipt['inputs']['baseline']['sha256']:
            raise ValueError('Baseline changed before snapshot write')
        snapshot = ROOT / receipt['baseline_snapshot_path']
        outputs = {
            snapshot: baseline,
            OUTPUT / 'deut32_8_candidate.v1.json': json_bytes(candidate),
            OUTPUT / PREFLIGHT_NAME: json_bytes(receipt),
        }
        if any(p.is_symlink() for p in outputs):
            raise ValueError('Research output must not overwrite a symlink target')
        if snapshot.exists() and snapshot.read_bytes() != baseline:
            raise ValueError('Existing baseline snapshot differs; create a new version instead')
        for path, content in outputs.items():
            path.write_bytes(content)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
