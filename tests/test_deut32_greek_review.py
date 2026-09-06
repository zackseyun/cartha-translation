import hashlib
import json
from pathlib import Path
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "sources/textual_restoration/discovery/deut32_8_greek_review.v1.json"


def normalized(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value)
                   if unicodedata.category(c) != 'Mn')


class DeuteronomyGreekReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(RECORD.read_text())

    def test_published_word_preserves_supply_boundary(self):
        word = self.data['amherst_192']
        self.assertEqual(word['published_line'], '] ' + word['unbracketed_letters'] + '[' + word['supplied_completion'])
        self.assertFalse(word['complete_noun_preserved'])
        self.assertFalse(word['following_god_word_preserved_here'])

    def test_prefix_discriminates_noun_not_full_phrase(self):
        word = self.data['amherst_192']
        prefix = word['unbracketed_letters']
        self.assertTrue(normalized(word['noun_contrast'][0]).startswith(prefix))
        self.assertFalse(normalized(word['noun_contrast'][1]).startswith(prefix))

    def test_correction_report_cannot_be_counted_as_sons_of_god(self):
        report = self.data['cambridge_106_report']
        self.assertEqual(report['printed_witness_marker'], 'p^b(uid)')
        self.assertEqual(report['normalized_reported_phrase'], 'υιων Ισραηλ')
        self.assertFalse(report['counted_as_sons_of_god_support'])
        self.assertIn('uninspected', report['resolution_status'])

    def test_consultation_and_promotion_limits_remain_explicit(self):
        self.assertTrue(all(value is False for value in self.data['policy'].values()))
        for source in self.data['sources']:
            self.assertRegex(source['sha256'], r'^[0-9a-f]{64}$')
            self.assertTrue(source['pdf_pages_visually_inspected'])

    def test_baseline_and_formal_comparison_agree(self):
        control = self.data['pob_control']
        self.assertEqual(hashlib.sha256((ROOT / control['path']).read_bytes()).hexdigest(), control['sha256'])
        comparison = json.loads((ROOT / 'sources/textual_restoration/comparisons/pentateuch_controls.v1.json').read_text())
        case = next(c for c in comparison['cases'] if c['id'] == 'DEU.32.8.referent')
        reading = next(r for r in case['readings'] if r.get('witness_id') == 'amherst-192')
        self.assertEqual(reading['text'], self.data['amherst_192']['published_line'])
        self.assertEqual(reading['reading_class'], 'angel-noun-prefix-only')
        self.assertFalse(case['canonical_change_applied'])


if __name__ == '__main__':
    unittest.main()
