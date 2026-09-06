"""Bounded negative scope tests; no canonical writes or new transaction framework."""
import copy
import json
import unittest
import yaml

from tools.textual_restoration import check_genesis_4_8_note_candidate as checker


class GenesisNoteCandidateTests(unittest.TestCase):
    def setUp(self):
        self.before = yaml.safe_load((checker.ROOT / (checker.PREFIX + 'baseline.v1.yaml')).read_text())
        self.after = yaml.safe_load((checker.ROOT / (checker.PREFIX + 'candidate.v1.yaml')).read_text())
        self.plan = json.loads((checker.ROOT / (checker.PREFIX + 'plan.v1.json')).read_text())
        self.note = json.loads((checker.ROOT / checker.DOSSIER).read_text())['reader_proposal']['exact_note_text']

    def validate(self):
        checker.validate_records(self.before, self.after, self.plan, self.note)

    def test_exact_allowed_candidate(self):
        self.validate()

    def test_main_english_smoothing_rejected(self):
        self.after['translation']['text'] = self.after['translation']['text'].replace('said to', 'spoke to')
        with self.assertRaises(ValueError):
            self.validate()

    def test_source_change_rejected(self):
        self.after['source']['text'] += ' נלכה השדה'
        with self.assertRaises(ValueError):
            self.validate()

    def test_unrelated_lexical_change_rejected(self):
        self.after['lexical_decisions'][0]['rationale'] = 'New rationale'
        with self.assertRaises(ValueError):
            self.validate()

    def test_truncated_historical_archive_rejected(self):
        del self.after['review_history'][2]['value']['agreement']
        with self.assertRaises(ValueError):
            self.validate()

    def test_stale_current_approval_rejected(self):
        self.after['cross_check'] = copy.deepcopy(self.before['cross_check'])
        with self.assertRaises(ValueError):
            self.validate()

    def test_expanded_edit_plan_rejected(self):
        self.plan['edits'].append({'path': ['translation', 'text'],
                                  'from': self.before['translation']['text'], 'to': 'Changed'})
        with self.assertRaises(ValueError):
            self.validate()

    def test_unapproved_note_even_with_matching_plan_rejected(self):
        self.after['translation']['footnotes'][0]['text'] = 'The invitation is original.'
        self.plan['edits'][0]['to'] = 'The invitation is original.'
        with self.assertRaises(ValueError):
            self.validate()

    def test_false_promotion_flag_even_with_matching_plan_rejected(self):
        self.after['note_application']['earliest_source_form_promoted'] = True
        self.plan['metadata_edits'][-1]['to']['earliest_source_form_promoted'] = True
        with self.assertRaises(ValueError):
            self.validate()


if __name__ == '__main__':
    unittest.main()
