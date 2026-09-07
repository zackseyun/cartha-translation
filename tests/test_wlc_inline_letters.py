import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import yaml

from tools import wlc

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'sources/textual_restoration/applications/hebrew_inline_letter_repair.v1.json'


class WlcInlineLetterTests(unittest.TestCase):
    def test_retains_special_letters_tails_and_annotations(self):
        element = ET.fromstring('<w>גָּח֜<seg type="x-large">וֹ</seg>ן</w>')
        text, annotations = wlc.word_text(element)
        self.assertEqual(text, 'גָּח֜וֹן')
        self.assertEqual(annotations, [{'type': 'x-large', 'text': 'וֹ', 'offset': 5}])

    def test_initial_and_multiple_inline_letters(self):
        element = ET.fromstring('<w><seg type="x-small">א</seg>ב<seg type="x-suspended">ג</seg>ד</w>')
        text, annotations = wlc.word_text(element)
        self.assertEqual(text, 'אבגד')
        self.assertEqual([a['offset'] for a in annotations], [0, 2])

    def test_unknown_or_reading_markup_is_not_silently_absorbed(self):
        for xml in ('<w>א<note>ב</note></w>', '<w>א<seg type="other">ב</seg></w>',
                    '<w>א<seg type="x-large"><w>ב</w></seg></w>'):
            with self.subTest(xml=xml), self.assertRaises(ValueError):
                wlc.word_text(ET.fromstring(xml))

    def test_all_vendored_written_words_and_annotation_inventory(self):
        annotated = []
        for code, (_, _, _, filename) in wlc.OT_BOOKS.items():
            tree = ET.parse(ROOT / 'sources/ot/wlc' / filename)
            for verse in tree.findall('.//o:verse', wlc.OSIS_NS):
                for word in verse.findall('o:w', wlc.OSIS_NS):
                    text, notes = wlc.word_text(word)
                    self.assertEqual(text, ''.join(word.itertext()).strip())
                    if notes:
                        annotated.append(word.get('id'))
        expected = [w['word_id'] for r in json.loads(RECEIPT.read_text())['entries'] for w in r['words']]
        self.assertEqual(sorted(annotated), sorted(expected))
        self.assertEqual(len(annotated), 11)

    def test_ten_canonical_repairs_and_loaded_morphology(self):
        entries = json.loads(RECEIPT.read_text())['entries']
        self.assertEqual(len(entries), 10)
        for entry in entries:
            with self.subTest(id=entry['id']):
                code, ch, v = entry['source_reference'].split('.')
                verse = wlc.load_verse(code, int(ch), int(v), ROOT / 'sources')
                record = yaml.safe_load((ROOT / entry['path']).read_text())
                self.assertEqual(verse.hebrew_text, entry['after_text'])
                self.assertEqual(record['source']['text'], entry['after_text'])
                self.assertEqual(record['source']['edition'], 'WLC')
                for word in entry['words']:
                    actual = next(w for w in verse.words if w.word_id == word['word_id'])
                    self.assertEqual(actual.annotations, word['annotations'])
                    self.assertIn(word['text'], wlc.morphology_lines(verse))

    def test_qere_stays_out_of_written_word_stream(self):
        verse = wlc.load_verse('JOB', 13, 15, ROOT / 'sources')
        words = {w.word_id: w.text for w in verse.words}
        self.assertIn('184U9', words)
        self.assertNotIn('18Vvg', words)


if __name__ == '__main__':
    unittest.main()
