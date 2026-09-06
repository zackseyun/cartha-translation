import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Isaiah54SweteTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'sources/textual_restoration/discovery/isaiah54_swete_review.v1.json').read_text())

    def test_exact_edition_pin_and_page_mapping(self):
        source = self.data['source']
        manifest = (ROOT / 'sources/lxx/swete/MANIFEST.md').read_text()
        self.assertIn(source['sha256'], manifest)
        self.assertEqual(source['pdf_page_1based'], 226)
        self.assertEqual(source['printed_page'], '202')
        self.assertIn('1905', source['edition'])
        self.assertIn(226, source['visually_consulted_pdf_pages_1based'])
        self.assertFalse(source['direct_manuscript_image'])

    def test_edition_agreement_not_additional_manuscript_vote(self):
        previous = json.loads((ROOT / 'sources/textual_restoration/discovery/isaiah54_versions_review.v1.json').read_text())
        # Preserve the actual acute/grave difference rather than silently changing a source.
        swete = self.data['main_text']['text']
        self.assertNotEqual(swete, previous['greek']['text'])
        self.assertEqual(swete.replace('ἐκλεκτούς', 'ἐκλεκτοὺς'), previous['greek']['text'])
        self.assertEqual(self.data['main_text']['apparatus_margin_sigla'], ['א', 'A', 'Q'])
        self.assertFalse(self.data['assessment']['independent_ancient_witness_added'])
        self.assertFalse(self.data['apparatus']['silence_proves_all_greek_manuscripts_agree'])
        self.assertFalse(self.data['next_full_apparatus']['full_isaiah54_apparatus_consulted'])

    def test_quantifier_and_hand_report_are_bounded(self):
        main = self.data['main_text']
        self.assertFalse(main['all_before_architecture'])
        self.assertFalse(main['all_before_boundary'])
        self.assertTrue(main['all_before_children_in_54_13'])
        self.assertIn('אc.b', self.data['apparatus']['architecture_report'])
        self.assertIn('vid', self.data['apparatus']['report_policy'])
        self.assertFalse(self.data['apparatus']['reports_added_all_before_architecture_at_54_12'])

    def test_unchanged_pob_and_no_promotion(self):
        for control in self.data['pob_controls']:
            self.assertEqual(hashlib.sha256((ROOT / control['path']).read_bytes()).hexdigest(), control['sha256'])
        for key in ('exact_hebrew_retroversion_established', 'newly_recovered_letters',
                    'independent_review_completed', 'source_or_english_changed', 'selection_gate_completed'):
            self.assertFalse(self.data['assessment'][key], key)


if __name__ == '__main__':
    unittest.main()
