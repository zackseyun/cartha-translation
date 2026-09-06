"""Audit receipt bookkeeping plus actual pinned inputs when locally available.

These are provenance/locator checks, not a paleographic identity adjudication.
"""
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'sources/textual_restoration/discovery/qumran_catalogue_identity_followup.v1.json'
QDR = Path(os.environ.get('POB_IDENTITY_QDR', '/private/tmp/pob-qdr/data/qdr.1.1.biblical.json'))
SOURCES = Path(os.environ.get('POB_IDENTITY_SOURCES', '/private/tmp/pob-catalogue-identity.uqNkwj'))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class IdentityReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(RECEIPT.read_text())

    def test_crosswalks_never_promote_physical_alias(self):
        rows = self.receipt['content_crosswalks']
        self.assertEqual([(r['qdr_label'], r['catalogue_label']) for r in rows],
                         [('4Q8a', '4Q8'), ('4Q8b', '4Q8'), ('4Q8c', '4Q8a'), ('4Q8d', '4Q8b')])
        self.assertTrue(all(r['status'] == 'content-locator-correspondence-not-physical-alias' for r in rows))
        self.assertFalse(self.receipt['policy']['exact_label_is_safe_cross_project_join_key'])

    def test_decision_sources_resolve_and_no_physical_or_canonical_promotion(self):
        sources = {s['id'] for s in self.receipt['source_snapshots']}
        self.assertEqual(len(sources), len(self.receipt['source_snapshots']))
        self.assertTrue(all(set(d['source_ids']) <= sources for d in self.receipt['decisions']))
        self.assertFalse(self.receipt['policy']['physical_identity_verified_by_this_pass'])
        self.assertFalse(self.receipt['policy']['canonical_change_applied'])
        self.assertIsNone(self.receipt['policy']['new_independent_witness_count'])
        decision = next(d for d in self.receipt['decisions'] if d['id'] == '4q54a-4q47a-published-challenge')
        self.assertFalse(decision['proposal_adopted'])

    def test_duplicate_record_identity_is_not_lost(self):
        rows = [r for r in self.receipt['qdr_records'] if r['label'] == '4Q483']
        self.assertEqual([r['source_record_index'] for r in rows], [2, 209])
        self.assertNotEqual(rows[0]['record_sha256'], rows[1]['record_sha256'])
        self.assertEqual(rows[0]['fragment_line_numbers']['f1'], ['1', '2', '3'])
        self.assertEqual(rows[1]['fragment_line_numbers']['f1'], ['4', '5'])

    @unittest.skipUnless(QDR.is_file(), 'private pinned QDR snapshot unavailable')
    def test_real_qdr_records_hashes_labels_and_fragment_locators(self):
        raw = QDR.read_bytes()
        self.assertEqual(digest(raw), self.receipt['qdr_source']['sha256'])
        corpus = json.loads(raw)
        for row in self.receipt['qdr_records']:
            with self.subTest(record=row['source_record_index']):
                record = corpus[row['source_record_index']]
                self.assertEqual(record['scroll'], row['label'])
                self.assertEqual(digest(json.dumps(record, ensure_ascii=False, sort_keys=True,
                                                  separators=(',', ':')).encode()), row['record_sha256'])
                self.assertEqual({f['id']: [l['n'] for l in f['lines']] for f in record['fragments']},
                                 row['fragment_line_numbers'])

    @unittest.skipUnless(QDR.is_file(), 'private pinned QDR snapshot unavailable')
    def test_real_reference_tags_distinguish_exact_label_traps(self):
        raw = QDR.read_bytes()
        self.assertEqual(digest(raw), self.receipt['qdr_source']['sha256'])
        corpus = json.loads(raw)
        expected = {46: {'Gen 1:8', 'Gen 1:9', 'Gen 1:10'},
                    47: {'Gen 2:17', 'Gen 2:18'}, 48: {'Gen 12:4', 'Gen 12:5'},
                    49: {'Gen 1:1'}, 167: {'Prov 9:16', 'Prov 9:17', 'Prov 10:30', 'Prov 10:31', 'Prov 10:32'},
                    209: {'Gen 1:29'}}
        for ordinal, refs in expected.items():
            self.assertEqual({w[5] for f in corpus[ordinal]['fragments'] for l in f['lines'] for w in l['words']}, refs)

    @unittest.skipUnless(SOURCES.is_dir(), 'private downloaded source snapshots unavailable')
    def test_real_downloaded_source_hashes(self):
        for source in self.receipt['source_snapshots']:
            with self.subTest(source=source['id']):
                self.assertEqual(digest((SOURCES / source['file']).read_bytes()), source['sha256'])

    @unittest.skipUnless(SOURCES.is_dir(), 'private downloaded source snapshots unavailable')
    def test_real_reciprocal_pam_references_cover_every_main_line(self):
        for label, other in [('4Q54b', '4Q69c'), ('4Q69c', '4Q54b')]:
            raw = (SOURCES / f'{label}.html').read_bytes()
            source = next(s for s in self.receipt['source_snapshots'] if s['file'] == f'{label}.html')
            self.assertEqual(digest(raw), source['sha256'])
            html = raw.decode()
            for line in range(1, 5):
                self.assertIn(f'<span class="secondary-reference"> ({other} frg. 1,{line} + Add PAM-42.082-2-4,{line}) </span>', html)

    def test_exported_qdr_fields_are_metadata_only(self):
        expected = {'source_record_index', 'label', 'record_sha256', 'fragment_line_numbers', 'reference_tag_scope'}
        self.assertTrue(all(set(row) == expected for row in self.receipt['qdr_records']))


if __name__ == '__main__':
    unittest.main()
