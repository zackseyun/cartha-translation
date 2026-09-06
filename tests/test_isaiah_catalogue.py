import json
from pathlib import Path
import unittest

from tools.textual_restoration import build_catalogue_reconciliation as M
from tests.test_catalogue_reconciliation import record

SPEC = M.TARGETS.with_name('isaiah_catalogue_targets.v1.json')
RECEIPT = SPEC.with_name('isaiah_catalogue_check.v1.json')
PESHARIM = {'3Q4', '4Q161', '4Q162', '4Q163', '4Q164', '4Q165'}


class IsaiahCatalogueTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(SPEC.read_text())
        self.receipt = json.loads(RECEIPT.read_text())

    def test_saved_inputs_and_target_accounting(self):
        M.validate_targets(self.spec)
        self.assertEqual(self.receipt['inputs']['targets_sha256'], M.sha(SPEC.read_bytes()))
        self.assertEqual(self.receipt['inputs']['builder_sha256'], M.sha(Path(M.__file__).read_bytes()))
        self.assertEqual(self.receipt['inputs']['scanner_sha256'],
                         M.sha((M.ROOT / 'tools/textual_restoration/build_qdr_discovery.py').read_bytes()))
        self.assertEqual([e['id'] for e in self.spec['entries']],
                         [e['catalogue_id'] for e in self.receipt['targets']])
        summary = self.receipt['summary']
        self.assertEqual(summary['catalogue_target_names'], 28)
        self.assertEqual(summary['target_names_with_scoped_index_hits'], 22)
        self.assertEqual(summary['target_names_without_index_labels'], 6)
        self.assertEqual(summary['pinned_index_book_anchors'], 1291)
        self.assertEqual(summary['unmatched_book_labels'], 0)

    def test_copy_list_and_commentaries_remain_distinct(self):
        copies = [e for e in self.spec['entries'] if e['role'] == 'direct-language-candidate']
        pesharim = [e for e in self.spec['entries'] if e['role'] == 'pesher-quotation-candidate']
        self.assertEqual(len(copies), 22)
        self.assertEqual({e['id'] for e in pesharim}, PESHARIM)
        self.assertTrue(all(e['catalogue_source'] == 'tov-2008' for e in copies))
        self.assertTrue(all(e['catalogue_source'] != 'tov-2008' for e in pesharim))

    def test_gaps_are_index_gaps_not_missing_manuscripts(self):
        absent = {e['catalogue_id'] for e in self.receipt['targets']
                  if e['index_status'] == 'label-not-in-pinned-index'}
        self.assertEqual(absent, PESHARIM)
        policy = self.receipt['policy']
        for key in ('all_current_witnesses_reconciled', 'indexed_anchors_prove_preserved_letters',
                    'no_index_hit_proves_manuscript_absence', 'canonical_change_applied',
                    'transcription_exported', 'full_verse_index_exported'):
            self.assertFalse(policy[key])
        self.assertTrue(all(e['reading_support'] == 'not-assessed' for e in self.receipt['targets']))

    def test_aliases_do_not_skip_letter_i_or_invent_an_extra_copy(self):
        rows = {e['id']: e for e in self.spec['entries']}
        self.assertEqual(rows['1QIsab']['query_labels'], ['1Q8'])
        self.assertNotIn('1Q8', rows)
        self.assertEqual(rows['4Q62a']['catalogue_name'], '4QIsai')
        self.assertEqual(rows['4Q63']['catalogue_name'], '4QIsaj')
        self.assertEqual(rows['4Q68']['crosswalk_source'], 'iaa-68')
        self.assertEqual(rows['4Q69']['catalogue_name'], '4QpapIsap')
        self.assertEqual(rows['4Q69']['role'], 'direct-language-candidate')

    def test_future_quotation_hit_does_not_become_a_reading_adjudication(self):
        result = M.reconcile([record('4Q161', ('Isa 5:1', 'Hos 1:1'))], self.spec)
        row = next(e for e in result['targets'] if e['catalogue_id'] == '4Q161')
        self.assertEqual(row['indexed_anchor_count'], 1)
        self.assertEqual(row['role'], 'pesher-quotation-candidate')
        self.assertEqual(row['reading_support'], 'not-assessed')
        self.assertNotIn('PRIVATE-TEXT', json.dumps(result))


if __name__ == '__main__':
    unittest.main()
