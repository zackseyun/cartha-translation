"""Guard the approved Greek-word mapping and its public revision trail."""
import hashlib
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {15: ['agape-love', 'phileo-love'],
            16: ['agape-love', 'phileo-love'],
            17: ['phileo-love', 'phileo-love', 'phileo-love']}


def record(edition, verse):
    return yaml.safe_load((ROOT / edition / 'nt/john/021' / f'{verse:03}.yaml').read_text())


class JohnLoveWordingTests(unittest.TestCase):
    def test_all_seven_occurrences_in_both_editions(self):
        for edition in ('translation', 'translation_simplified'):
            for verse, expected in EXPECTED.items():
                with self.subTest(edition=edition, verse=verse):
                    text = record(edition, verse)['translation']['text']
                    self.assertEqual(re.findall(r'\b(?:agape|phileo)-love\b', text), expected)
                    self.assertNotRegex(text, r'(?<!-)\blove\b')
                    self.assertNotIn('fileo', text)

    def test_greek_source_and_derivative_grounding(self):
        for verse in EXPECTED:
            pob = record('translation', verse)
            spob = record('translation_simplified', verse)
            self.assertEqual(pob['source'], spob['source'])
            self.assertEqual(pob['translation']['text'], spob['base_translation']['text'])
            self.assertEqual(pob['translation']['footnotes'], spob['base_translation']['footnotes'])
            digest = hashlib.sha256(yaml.safe_dump(pob['source'], allow_unicode=True,
                sort_keys=False, width=1000).strip().encode()).hexdigest()
            self.assertEqual(digest, spob['source_grounding']['source_text_sha256'])
            self.assertRegex(spob['source_grounding']['pob_commit_sha'], r'^[a-f0-9]{40}$')
            greek = pob['source']['text']
            self.assertEqual(greek.count('ἀγαπᾷς'), 1 if verse < 17 else 0)
            self.assertEqual(greek.count('φιλῶ'), 1)
            if verse == 17:
                self.assertIn('φιλεῖς με', greek)
                self.assertIn('Φιλεῖς με', greek)

    def test_no_love_debate_notes_or_orphaned_markers(self):
        for edition in ('translation', 'translation_simplified'):
            for verse in EXPECTED:
                tr = record(edition, verse)['translation']
                notes = tr.get('footnotes', [])
                self.assertEqual(set(re.findall(r'\[([a-z])\]', tr['text'])),
                                 {f['marker'] for f in notes})
                for note in notes:
                    self.assertNotRegex(note['text'], r'(?i)agapa|phile|ἀγαπάω|φιλέω|verbs for .love')
        self.assertIn('more than these[a]', record('translation', 15)['translation']['text'])
        self.assertIn('second time[a]', record('translation', 16)['translation']['text'])
        self.assertIn('you know[a]', record('translation', 17)['translation']['text'])

    def test_revision_reasoning_is_posted_and_old_reviews_are_historical(self):
        for verse in EXPECTED:
            pob = record('translation', verse)
            revision = pob['revisions'][-1]
            self.assertTrue(revision['approved_revision'])
            self.assertTrue(revision['public_proposal'])
            self.assertEqual(revision['proposal_source'], 'maintainer')
            self.assertEqual(revision['to'], pob['translation']['text'])
            self.assertNotEqual(revision['from'], revision['to'])
            self.assertIn('third-question change', revision['rationale'])
            self.assertTrue((ROOT / revision['source_review']).is_file())
            self.assertEqual(pob['cross_check_history'][-1]['applies_to_translation_text'], revision['from'])
            self.assertIn('ai_draft', pob)
            self.assertNotIn('cross_check', pob)


if __name__ == '__main__':
    unittest.main()
