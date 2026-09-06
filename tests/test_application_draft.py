import copy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from tools.textual_restoration import build_application_draft as module

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / 'sources/textual_restoration/applications'


class ApplicationDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selection = json.loads(module.SELECTION.read_text())['selections'][0]
        cls.raw = (ROOT / cls.selection['baseline']['repo_path']).read_bytes()
        cls.before = yaml.safe_load(cls.raw)
        cls.plan = json.loads(module.PLAN.read_text())
        cls.candidate, cls.receipt = module.build()

    def test_checked_outputs_reproduce_from_current_inputs(self):
        self.assertEqual(self.raw, (ROOT / self.receipt['baseline_snapshot_path']).read_bytes())
        self.assertEqual(module.json_bytes(self.candidate),
                         (ARTIFACTS / 'deut32_8_candidate.v1.json').read_bytes())
        self.assertEqual(module.json_bytes(self.receipt),
                         (ARTIFACTS / module.PREFLIGHT_NAME).read_bytes())

    def test_full_source_is_labeled_composite_not_wlc_or_fragment(self):
        expected = module.unpointed(self.before['source']['text']).replace('בני ישראל', 'בני אלוהים')
        self.assertEqual(self.candidate['source']['text'], expected)
        self.assertEqual(self.candidate['source']['edition'], 'POB-critical-draft')
        self.assertFalse(self.candidate['restoration_draft']['entire_verse_attested_in_selected_fragment'])
        self.assertFalse(self.candidate['restoration_draft']['approved'])

    def test_notes_and_unrelated_english_survive(self):
        translation = self.candidate['translation']
        self.assertEqual(translation['text'], self.before['translation']['text'].replace('the sons of Israel', 'the sons of God'))
        self.assertEqual(translation['footnotes'][1], self.before['translation']['footnotes'][1])
        module.note_markers(translation)
        malformed = copy.deepcopy(translation)
        malformed['footnotes'].append(malformed['footnotes'][0])
        with self.assertRaisesRegex(ValueError, 'markers'):
            module.note_markers(malformed)

    def test_old_agreement_is_archived_not_reused(self):
        self.assertEqual(self.candidate['cross_check'], {'status': 'needs_review'})
        self.assertNotIn('revision_pass', self.candidate)
        for field in ('cross_check', 'revision_pass'):
            old = next(x for x in self.candidate['review_history'] if x['field'] == field)
            self.assertEqual(old['value'], self.before[field])
            self.assertEqual(old['historical_review_input_binding'], 'not-verified')
            self.assertFalse(old['certifies_this_candidate'])
        self.assertEqual(self.candidate['ai_draft'], self.before['ai_draft'])

    def test_other_metadata_is_unchanged(self):
        affected = {'source', 'translation', 'lexical_decisions', 'theological_decisions',
                    'cross_check', 'revision_pass', 'status', 'review_history', 'restoration_draft'}
        for key in set(self.before) - affected:
            self.assertEqual(self.before[key], self.candidate[key])
        self.assertEqual(self.before['lexical_decisions'][:-1], self.candidate['lexical_decisions'][:-1])
        self.assertEqual(self.before['theological_decisions'][1:], self.candidate['theological_decisions'][1:])

    def test_baseline_drift_stops_composition(self):
        with self.assertRaisesRegex(ValueError, 'baseline drift'):
            module.draft_record(self.raw + b'\n', self.selection, self.plan)

    def test_mismatched_hebrew_cannot_enter_draft(self):
        plan = copy.deepcopy(self.plan)
        plan['source_replacement']['to'] = 'בני אל'
        with self.assertRaisesRegex(ValueError, 'working selection'):
            module.draft_record(self.raw, self.selection, plan)

    def test_missing_or_duplicate_metadata_target_stops_composition(self):
        plan = copy.deepcopy(self.plan)
        plan['lexical_decisions']['match'] = 'not a source word'
        with self.assertRaisesRegex(ValueError, 'match one entry'):
            module.draft_record(self.raw, self.selection, plan)

    def test_generated_evidence_or_promoted_selection_is_rejected(self):
        selection = copy.deepcopy(self.selection)
        selection['generated_images_used'] = True
        with self.assertRaisesRegex(ValueError, 'Generated images'):
            module.draft_record(self.raw, selection, self.plan)
        selection = copy.deepcopy(self.selection)
        selection['promotion_status'] = 'promoted'
        with self.assertRaisesRegex(ValueError, 'unpromoted research'):
            module.draft_record(self.raw, selection, self.plan)

    def test_actual_mobile_export_preserves_notes_but_not_full_source(self):
        result = self.receipt['mobile_probe']
        self.assertTrue(result['all_other_exported_book_content_unchanged'])
        self.assertTrue(result['draft_english_preserved'])
        self.assertTrue(result['draft_note_bodies_preserved'])
        self.assertFalse(result['draft_source_preserved'])
        self.assertFalse(result['deployed_reader_checked'])

    def test_schema_gaps_and_unfinished_gates_are_not_certification(self):
        result = self.receipt
        self.assertEqual([e['path'] for e in result['schema_check']['baseline_errors']], ['status'])
        self.assertEqual([e['path'] for e in result['schema_check']['candidate_errors']], ['source/edition'])
        self.assertTrue(all(v == 'pending' for v in result['review_gates'].values()))
        self.assertFalse(result['publication_ready'])
        self.assertFalse(result['canonical_change_applied'])
        self.assertFalse(result['applier_implemented'])
        self.assertEqual(self.raw, (ROOT / self.selection['baseline']['repo_path']).read_bytes())

    def exercise_write_guard(self, symlink):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            baseline = root / self.selection['baseline']['repo_path']
            baseline.parent.mkdir(parents=True)
            baseline.write_bytes(self.raw)
            output = root / 'sources/textual_restoration/applications'
            output.mkdir(parents=True)
            snapshot = root / self.receipt['baseline_snapshot_path']
            if symlink:
                (output / 'deut32_8_candidate.v1.json').symlink_to(baseline)
            else:
                snapshot.write_bytes(b'prior research snapshot must survive')
            with patch.object(module, 'ROOT', root), patch.object(module, 'OUTPUT', output), \
                 patch.object(module, 'build', return_value=(self.candidate, self.receipt)), \
                 patch('sys.argv', ['build_application_draft.py', '--write']), \
                 redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError, 'symlink|snapshot differs'):
                    module.main()
            self.assertEqual(baseline.read_bytes(), self.raw)
            self.assertFalse((output / module.PREFLIGHT_NAME).exists())
            if not symlink:
                self.assertEqual(snapshot.read_bytes(), b'prior research snapshot must survive')

    def test_write_refuses_to_replace_another_baseline_snapshot(self):
        self.exercise_write_guard(symlink=False)

    def test_write_refuses_symlink_to_canonical_file(self):
        self.exercise_write_guard(symlink=True)

    def test_previous_failed_preflight_remains_historical(self):
        old = json.loads((ARTIFACTS / 'deut32_8_preflight.v1.json').read_text())
        self.assertFalse(old['mobile_probe']['draft_note_bodies_preserved'])
        self.assertNotEqual(old['inputs']['exporter_sha256'], self.receipt['inputs']['exporter_sha256'])
        self.assertEqual(old['candidate_json_sha256'], self.receipt['candidate_json_sha256'])


if __name__ == '__main__':
    unittest.main()
