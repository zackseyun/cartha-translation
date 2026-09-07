import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from tools import export_mobile_bible as exporter


class ReaderSupplementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / 'nt/romans/016'
        self.directory.mkdir(parents=True)
        self.record = {
            'id': 'ROM.16.25', 'textual_status': 'secondary_witness',
            'reader_supplement': True,
            'source': {'edition': 'rp2005', 'text': 'Τῷ'},
            'translation': {'text': 'To him[a]', 'footnotes': [
                {'marker': 'a', 'text': 'Supplementary reading.', 'reason': 'textual_critical'}]},
        }
        self.enterContext(patch.object(exporter, 'TRANSLATION_ROOT', self.root))

    def write_record(self):
        (self.directory / '025.yaml').write_text(yaml.safe_dump(self.record))

    def test_opt_in_preserves_record_and_adds_no_source_rows(self):
        self.write_record()
        expected = {16: [24]}
        records = exporter.reviewed_supplements('ROM', expected)
        self.assertEqual(records, {(16, 25): self.record})
        self.assertEqual(expected, {16: [24]})

    def test_unreviewed_gap_is_not_inferred_or_exported(self):
        for value in (False, None, 'true'):
            self.record['reader_supplement'] = value
            self.write_record()
            self.assertEqual(exporter.reviewed_supplements('ROM', {16: [24]}), {})

    def test_invalid_opt_in_fails_closed(self):
        original = copy.deepcopy(self.record)
        mutations = [
            ('id', 'ROM.16.26'), ('textual_status', 'primary'),
            ('source', {}), ('translation', {'text': ''}),
            ('source', {'edition': 'unverified-supplementary-greek', 'text': 'Τῷ'}),
            ('translation', {'text': 'No visible marker', 'footnotes': original['translation']['footnotes']}),
            ('translation', {'text': 'Text[a]', 'footnotes': [
                {'marker': 'a', 'text': 'Lexical gloss only.', 'reason': 'lexical'}]}),
        ]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                self.record = copy.deepcopy(original)
                self.record[key] = value
                self.write_record()
                with self.assertRaises(ValueError):
                    exporter.reviewed_supplements('ROM', {16: [24]})

    def test_no_duplicate_when_base_already_contains_verse(self):
        self.write_record()
        self.assertEqual(exporter.reviewed_supplements('ROM', {16: [25]}), {})

    def test_export_uses_supplement_without_loading_nonexistent_base_verse(self):
        self.write_record()
        base = {'translation': {'text': 'Base verse'}}
        with patch.object(exporter, 'expected_chapter_map', return_value={16: [24]}), \
             patch.object(exporter, 'load_translation_record', return_value=base) as loader:
            verses = exporter.export_book('ROM')['chapters'][0]['verses']
        loader.assert_called_once_with('ROM', 16, 24)
        self.assertEqual([v['verse'] for v in verses], [24, 25])
        self.assertEqual(verses[1]['footnotes'], self.record['translation']['footnotes'])

    def test_supplement_does_not_hide_missing_base_verse(self):
        self.write_record()
        with patch.object(exporter, 'expected_chapter_map', return_value={16: [24]}), \
             patch.object(exporter, 'load_translation_record', return_value=None):
            self.assertIsNone(exporter.export_book('ROM'))

    def test_actual_romans_has_all_canonical_ids_and_supplementary_notes(self):
        actual_root = Path(__file__).resolve().parents[1] / 'translation'
        with patch.object(exporter, 'TRANSLATION_ROOT', actual_root):
            book = exporter.export_book('ROM')
        verses = {(c['chapter'], v['verse']): v for c in book['chapters'] for v in c['verses']}
        canonical = {(int(p.parent.name), int(p.stem))
                     for p in (actual_root / 'nt/romans').glob('*/*.yaml')}
        self.assertEqual(len(verses), 433)
        self.assertEqual(set(verses), canonical)
        for number in (25, 26, 27):
            verse = verses[16, number]
            self.assertTrue(verse['footnotes'])
            self.assertIn('[a]', verse['text'])
            self.assertIn('14:', verse['footnotes'][0]['text'])

    def test_attribution_audit_preserves_greek_and_blocks_unverified_sources(self):
        root = Path(__file__).resolve().parents[1]
        audit = json.loads((root / 'sources/textual_restoration/inventory/nt_supplement_attribution.v1.json').read_text())
        self.assertEqual(len(audit['records']), 27)
        self.assertEqual(len({r['id'] for r in audit['records']}), 27)
        held = 0
        for item in audit['records']:
            record = yaml.safe_load((root / item['path']).read_text())
            self.assertEqual(record['source']['text'], item['local_greek'])
            self.assertIsNot(record.get('reader_supplement'), True)
            if item['disposition'] == 'attribution_unverified_hold':
                held += 1
                self.assertEqual(record['source']['edition'], 'unverified-supplementary-greek')
                self.assertEqual(record['source']['claimed_edition_before_audit'], item['claimed_edition'])
                self.assertEqual(record['textual_restoration_review']['status'], 'needs_review')
        self.assertEqual(held, 13)


if __name__ == '__main__':
    unittest.main()
