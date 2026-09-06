import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'sources/textual_restoration/discovery/deut32_8_fouad_review.v1.json'


class DeuteronomyFouadReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(RECORD.read_text())

    def test_preserved_noun_does_not_supply_missing_complement(self):
        reading = self.data['published_reading']
        self.assertEqual(reading['normalized_preserved_noun_prefix'], 'υιω')
        self.assertIn('doubtful', reading['normalization_disclosure'])
        self.assertTrue(reading['discriminates_sons_from_angels'])
        for key in ('full_phrase_preserved', 'following_god_word_preserved',
                    'discriminates_god_from_israel', 'exact_hebrew_retroversion_established'):
            self.assertFalse(reading[key])
        self.assertEqual(reading['supplied_continuation_first_option'], 'ν θεου')
        self.assertEqual(reading['supplied_continuation_alternative'], 'ν Ισραηλ')

    def test_physical_mapping_and_preview_limits(self):
        mapping = self.data['witness_mapping']
        self.assertEqual((mapping['rahlfs_id'], mapping['fragment'], mapping['plate'], mapping['column']),
                         ('848', '177', 46, '73*'))
        source = self.data['source']
        self.assertFalse(source['local_pdf_saved'])
        self.assertIsNone(source['sha256'])
        self.assertTrue({133, 134}.issubset({p['preview_page'] for p in source['locators']}))
        self.assertFalse(self.data['assessment']['blind_image_review_completed'])

    def test_corrector_report_is_not_an_extra_manuscript(self):
        report = self.data['correction_report']
        self.assertEqual(report['normalized_reported_phrase'], 'υιων Ισραηλ')
        self.assertTrue(report['supports_prior_cambridge_report'])
        for key in ('independent_manuscript_vote', 'ferrara_hand_image_inspected',
                    'exact_goettingen_apparatus_inspected',
                    'secondary_attribution_conflict_fully_resolved'):
            self.assertFalse(report[key])

    def test_no_promotion_or_canonical_change(self):
        assessment = self.data['assessment']
        for key in ('newly_recovered_letters', 'hebrew_exact_wording_resolved',
                    'canonical_change_applied', 'english_change_applied', 'selection_gate_completed'):
            self.assertFalse(assessment[key])
        control = self.data['pob_control']
        self.assertEqual(hashlib.sha256((ROOT / control['path']).read_bytes()).hexdigest(), control['sha256'])
        selection = json.loads((ROOT / 'sources/textual_restoration/selections/ot_critical_source_pilot.v1.json').read_text())['selections'][0]
        self.assertTrue(all(value == 'pending' for value in selection['review_gates'].values()))


if __name__ == '__main__':
    unittest.main()
