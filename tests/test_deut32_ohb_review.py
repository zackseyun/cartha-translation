import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'sources/textual_restoration/discovery/deut32_8_ohb_review.v1.json'


class DeuteronomyOHBReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(RECORD.read_text())

    def test_conjecture_is_not_a_hebrew_attestation(self):
        proposal = self.data['editorial_proposal']
        self.assertEqual(proposal['normalized_phrase'], 'בני אל')
        self.assertEqual(proposal['classification'], 'conjectural-exact-hebrew-wording')
        self.assertFalse(proposal['direct_hebrew_attestation_claimed_by_editor'])
        self.assertFalse(proposal['editorial_argument_is_observed_scribal_history'])
        self.assertNotEqual(proposal['normalized_phrase'], proposal['published_4q37_phrase_reported'])

    def test_visual_consultation_does_not_invent_acquisition(self):
        source = self.data['source']
        self.assertFalse(source['local_pdf_saved'])
        self.assertIsNone(source['sha256'])
        self.assertEqual([(p['pdf_page'], p['printed_page']) for p in source['relevant_locators']],
                         [(4, 354), (5, 355), (7, 357)])

    def test_greek_attribution_is_not_resolved_by_editorial_argument(self):
        self.assertEqual(self.data['editorial_proposal']['greek_manuscript_ids_specified_in_32_8_commentary'], [])
        self.assertFalse(self.data['pob_assessment']['greek_106_conflict_resolved'])

    def test_selection_and_canonical_baseline_remain_unpromoted(self):
        assessment = self.data['pob_assessment']
        for field in ('exact_wording_resolved', 'full_verse_source_gate_completed',
                      'independent_pob_review_completed', 'newly_recovered_letters',
                      'canonical_change_applied', 'english_change_applied'):
            self.assertFalse(assessment[field])
        selection = json.loads((ROOT / 'sources/textual_restoration/selections/ot_critical_source_pilot.v1.json').read_text())['selections'][0]
        self.assertEqual(selection['critical_source']['normalized_variation_unit'], assessment['working_phrase'])
        self.assertTrue(all(v == 'pending' for v in selection['review_gates'].values()))
        self.assertTrue(any('OHB' in q for q in selection['open_questions']))
        control = self.data['pob_control']
        self.assertEqual(hashlib.sha256((ROOT / control['path']).read_bytes()).hexdigest(), control['sha256'])


if __name__ == '__main__':
    unittest.main()
