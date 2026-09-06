import hashlib
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'sources/textual_restoration/discovery/isaiah54_versions_review.v1.json'


class Isaiah54VersionsTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(RECORD.read_text())

    def test_greek_text_fingerprint_and_local_quantifier_control(self):
        greek = self.data['greek']
        self.assertEqual(hashlib.sha256(greek['text'].encode()).hexdigest(), greek['text_sha256'])
        self.assertIn('ἐπάλξεις', greek['text'])
        self.assertNotIn('πάν', greek['text'])
        self.assertTrue(greek['all_before_children_in_54_13'])
        for key in ('all_before_architecture', 'all_before_boundary', 'absence_proves_hebrew_omission'):
            self.assertFalse(greek[key])

    def test_versional_absence_is_not_automatic_hebrew_omission(self):
        for version in ('greek', 'peshitta', 'targum'):
            with self.subTest(version=version):
                self.assertFalse(self.data[version]['all_before_architecture'])
                self.assertFalse(self.data[version]['absence_proves_hebrew_omission'])
                self.assertFalse(self.data[version]['full_apparatus_consulted'])
        self.assertFalse(self.data['peshitta']['all_before_boundary'])
        self.assertTrue(self.data['targum']['all_before_boundary'])
        self.assertFalse(self.data['peshitta']['greek_dependence_established'])

    def test_nonuniform_architecture_and_edition_roles(self):
        glosses = {self.data[v]['architecture_gloss'] for v in ('greek', 'peshitta', 'targum')}
        self.assertEqual(len(glosses), 3)
        self.assertEqual(self.data['targum']['language'], 'Aramaic')
        self.assertEqual(self.data['targum']['script'], 'Hebrew')
        registry = json.loads((ROOT / 'sources/textual_restoration/ot_witness_registry.v1.json').read_text())
        entries = {w['id']: w for w in registry['witnesses']}
        for version in ('greek', 'peshitta', 'targum'):
            entry = entries[self.data[version]['registry_id']]
            self.assertIn(entry['witness_class'], ('critical-edition', 'modern-transcription'))
        self.assertEqual(entries['cal-targum-isaiah']['languages'], ['Aramaic'])

    def test_actual_pob_keeps_wording_and_correct_notes(self):
        for control in self.data['pob_controls']:
            self.assertEqual(hashlib.sha256((ROOT / control['path']).read_bytes()).hexdigest(), control['sha256'])
        verse = yaml.safe_load((ROOT / self.data['pob_controls'][1]['path']).read_text())
        self.assertIn('pinnacles[b]', verse['translation']['text'])
        note = next(n for n in verse['translation']['footnotes'] if n['marker'] == 'b')
        self.assertIn('battlements', note['text'])
        # The Hebrew's later quantifier is an actual positive local control.
        consonants = ''.join(re.findall('[א-ת]', verse['source']['text']))
        self.assertIn('וכלגבול', consonants)

    def test_no_new_recovery_or_review_claim(self):
        a = self.data['assessment']
        for key in ('all_ancient_versions_agree_on_architecture', 'exact_hebrew_retroversion_established',
                    'source_wording_changed', 'english_wording_changed', 'notes_changed',
                    'newly_recovered_letters', 'independent_model_review_completed',
                    'imagegen_used_as_evidence', 'selection_gate_completed'):
            self.assertFalse(a[key], key)
        bdb = next(s for s in self.data['lexical_sources'] if s['id'] == 'bdb')
        self.assertIn('BDB10425, sense 5', bdb['locator'])
        self.assertIn('not a new HALOT consultation', bdb['result'])


if __name__ == '__main__':
    unittest.main()
