import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

import yaml

from tools import export_mobile_bible as exporter
from tools.textual_restoration.extract_qdr_passages import extract_passages

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'sources/textual_restoration/discovery/isaiah54_pesher_review.v1.json'


class Isaiah54PesherTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(RECEIPT.read_text())

    def test_published_quote_not_supplied_lead_or_commentary(self):
        c = self.data['comparison']
        self.assertEqual(c['published_4q164_quote_tail'], 'כול שמשותיך')
        self.assertEqual(c['following_commentary_marker'], 'פשרו')
        self.assertTrue(c['quote_tail_published_as_preserved'])
        self.assertFalse(c['preceding_words_preserved'])
        self.assertFalse(c['interpretation_is_biblical_source'])
        self.assertFalse(c['verse11_stone_word_complete_in_4q164'])

    def test_lacunae_do_not_vote_for_omission(self):
        c = self.data['comparison']
        self.assertFalse(c['4q57_discriminates_kol_presence'])
        self.assertFalse(c['4q69a_discriminates_kol_presence'])
        self.assertFalse(c['great_isaiah_kol_before_architectural_term'])
        self.assertEqual(c['historical_priority'], 'unresolved')

    def test_marker_repair_is_the_only_byte_change(self):
        for repair in self.data['pob_repairs']:
            with self.subTest(path=repair['path']):
                raw = (ROOT / repair['path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), repair['after_sha256'])
                after = repair['after_text'].encode()
                self.assertEqual(raw.count(after), 1)
                reconstructed = raw.replace(after, repair['before_text'].encode(), 1)
                self.assertEqual(hashlib.sha256(reconstructed).hexdigest(), repair['before_sha256'])
                self.assertEqual(re.sub(r'\[[a-z]\]', '', repair['before_text']),
                                 re.sub(r'\[[a-z]\]', '', repair['after_text']))

    def test_correct_anchors_and_local_export_keep_every_note(self):
        for repair in self.data['pob_repairs']:
            record = yaml.safe_load((ROOT / repair['path']).read_text())
            self.assertEqual(record['translation']['text'], repair['after_text'])
            for anchor in repair['required_anchors']:
                self.assertIn(anchor, record['translation']['text'])
            out = exporter._export_record_verse(int(record['id'].split('.')[-1]), record)
            self.assertEqual(out['text'], repair['after_text'])
            self.assertEqual(out['footnotes'], record['translation']['footnotes'])

    def test_no_new_image_reading_or_source_promotion(self):
        a = self.data['assessment']
        for key in ('newly_recovered_letters', 'images_inspected', 'imagegen_used_as_evidence',
                    'complete_apparatus_collation', 'source_wording_changed',
                    'english_lexical_wording_changed', 'note_bodies_changed',
                    'independent_review_completed', 'selection_gate_completed'):
            self.assertFalse(a[key], key)
        self.assertTrue(a['note_anchors_changed'])

    def test_line_context_retains_bracket_outside_selected_reference(self):
        # Synthetic fixture, not an imported restricted manuscript line.
        words = [['', t, '', '', '', r] for t, r in
                 [('prior [supplied', 'Is 54:11'), ('target', 'Is 54:12'), (']visible', 'Is 54:12')]]
        corpus = [{'scroll': 'fixture', 'fragments': [{'id': 'f1', 'lines': [{'n': '3', 'words': words}]}]}]
        before = copy.deepcopy(corpus)
        old = extract_passages(corpus, {'Is 54:12'})['Is 54:12'][0]['lines'][0]
        new = extract_passages(corpus, {'Is 54:12'}, include_line_context=True)['Is 54:12'][0]['lines'][0]
        self.assertNotIn('line_context', old)
        self.assertEqual(old['diplomatic_text'], new['diplomatic_text'])
        self.assertNotIn('[', new['diplomatic_text'])
        self.assertIn('[', new['line_context']['diplomatic_text'])
        self.assertEqual(new['line_context']['selected_word_indices'], [1, 2])
        self.assertFalse(new['line_context']['preservation_assessed'])
        self.assertIn('earlier physical line', new['line_context']['warning'])
        self.assertEqual(corpus, before)

    def test_exact_reference_mismatch_is_not_normalized_silently(self):
        corpus = [{'scroll': 'fixture', 'fragments': [{'id': 'f1', 'lines': [
            {'n': '1', 'words': [['', 'word', '', '', '', 'Is 54:12']]}]}]}]
        self.assertEqual(extract_passages(corpus, {'Isa 54:12'}), {'Isa 54:12': []})
        self.assertEqual(extract_passages(corpus, {'Is 54:12'})['Is 54:12'][0]['manuscript_id'], 'fixture')


if __name__ == '__main__':
    unittest.main()
