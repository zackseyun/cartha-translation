"""Current source-changing contract; historical note-only tests run separately."""
import copy
import json
import unittest
from unittest.mock import patch

from tools.textual_restoration import verify_critical_successor as m

PLAN = m.PREFIX + 'isaiah53_11_successor_plan.v1.json'
REVIEW = m.PREFIX + 'test-only-review.json'


class CriticalSuccessorTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(m.safe_read(m.ROOT, PLAN))
        self.review = {'canonical_application_approved': True, 'publication_approved': False,
                       'implementation_pins': {p: m.sha(m.safe_read(m.ROOT, p)) for p in m.BINDINGS}}
        self.read = m.safe_read

    def run_verify(self, *, mocked=False, plan=None, review=None, corpus=None, exports=None):
        plan = self.plan if plan is None else plan
        review = copy.deepcopy(self.review if review is None else review)
        plan_raw = json.dumps(plan).encode()
        review['plan_sha256'] = m.sha(plan_raw)
        review_raw = json.dumps(review).encode()
        def read(root, path):
            if path == PLAN: return plan_raw
            if path == REVIEW: return review_raw
            return self.read(root, path)
        with patch.object(m, 'safe_read', side_effect=read):
            if not mocked:
                return m.verify(PLAN, REVIEW, m.sha(review_raw))
            baseline = dict(m.checkpoint())
            prior = {'protected_targets': [m.JOB], 'preserved_exports': {}}
            book = {'chapters': [{'verses': []}]}
            with patch.object(m, 'prior_context', return_value=prior), \
                 patch.object(m.previous, 'current_corpus', side_effect=corpus or [baseline, baseline]), \
                 patch.object(m.previous.exporter, 'export_book', return_value=exports or book):
                return m.verify(PLAN, REVIEW, m.sha(review_raw))

    def test_real_live_corpus_and_exports(self):
        result = self.run_verify()
        self.assertIn(result['state'], ('baseline', 'candidate'))
        self.assertEqual(result['canonical_yaml_count'], 23264)
        self.assertEqual(set(result['actual_exports']), {'ISA', 'JOB', '2SA'})
        self.assertTrue(result['prior_note_applications_preserved'])
        self.assertFalse(result['publication_approved'])

    def test_exact_complete_states_only(self):
        baseline = {'a': 'old', 'b': 'old'}
        candidate = {'a': 'new', 'b': 'new'}
        self.assertEqual(m.corpus_state(baseline, baseline, candidate), 'baseline')
        self.assertEqual(m.corpus_state(candidate, baseline, candidate), 'candidate')
        for live in ({'a': 'new', 'b': 'old'}, {'a': 'old'}, {**baseline, 'c': 'new'}):
            with self.assertRaisesRegex(ValueError, 'Unapproved or partial'):
                m.corpus_state(live, baseline, candidate)

    def test_review_scope_and_bindings(self):
        for field, value in (('canonical_application_approved', 1), ('publication_approved', True),
                             ('implementation_pins', {})):
            review = copy.deepcopy(self.review)
            review[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.run_verify(mocked=True, review=review)

    def test_candidate_and_source_trust_drift(self):
        for field in ('before_sha256', 'after_sha256', 'trusted_source_sha256'):
            plan = copy.deepcopy(self.plan)
            change = plan['changes'][0]
            (change['trust'] if field.startswith('trusted') else change)[field] = '0' * 64
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.run_verify(mocked=True, plan=plan)

    def test_empty_duplicate_unknown_and_protected_targets(self):
        for changes in ([], self.plan['changes'] * 2,
                        [{**self.plan['changes'][0], 'target': 'unknown'}],
                        [{**self.plan['changes'][0], 'target': m.JOB}]):
            plan = {**self.plan, 'changes': changes}
            with self.assertRaises(ValueError): self.run_verify(mocked=True, plan=plan)

    def test_unrelated_live_change_rejected(self):
        changed = dict(m.checkpoint())
        changed['translation/ot/genesis/001/001.yaml'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'Unapproved or partial'):
            self.run_verify(mocked=True, corpus=[changed])

    def test_wrong_actual_export_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Affected-book export drift'):
            self.run_verify(mocked=True)

    def test_mid_check_corpus_drift_rejected(self):
        plan = copy.deepcopy(self.plan)
        book = {'chapters': [{'verses': []}]}
        plan['books']['ISA'].update(chapters=1, verses=0, baseline_export_sha256=m.json_sha(book))
        with self.assertRaisesRegex(ValueError, 'Corpus changed during'):
            self.run_verify(mocked=True, plan=plan, corpus=[dict(m.checkpoint()), {}], exports=book)

    def test_untrusted_review_rejected(self):
        with patch.object(m, 'safe_read', return_value=b'{}'):
            with self.assertRaisesRegex(ValueError, 'Trusted application review'):
                m.verify(PLAN, REVIEW, '0' * 64)

    def test_application_receipt_rejects_rollback_tamper_and_wrong_trust(self):
        actual = {'state': 'candidate', 'checkpoint': m.CHECKPOINT,
                  'review_sha256': 'review', 'plan_sha256': 'plan',
                  'current_corpus_verified': True}
        record = {'status': 'applied-verified', 'after': actual,
                  'before': {**actual, 'state': 'baseline'}}
        raw = json.dumps(record).encode()
        with patch.object(m, 'safe_read', return_value=raw), patch.object(m, 'verify', return_value=actual):
            self.assertTrue(m.verify_applied(PLAN, REVIEW, 'review', 'receipt', m.sha(raw))['application_record_verified'])
            with self.assertRaisesRegex(ValueError, 'Trusted application receipt'):
                m.verify_applied(PLAN, REVIEW, 'review', 'receipt', 'wrong')
        for change in ({'state': 'baseline'}, {'current_corpus_verified': 1}):
            with patch.object(m, 'safe_read', return_value=raw), \
                 patch.object(m, 'verify', return_value={**actual, **change}):
                with self.assertRaises(ValueError):
                    m.verify_applied(PLAN, REVIEW, 'review', 'receipt', m.sha(raw))


if __name__ == '__main__':
    unittest.main()
