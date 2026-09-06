import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.textual_restoration import verify_source_composition as m

BUNDLE = m.ROOT / 'sources/textual_restoration/applications/source_compositions.v1.json'


class SourceCompositionTests(unittest.TestCase):
    def setUp(self):
        self.bundle = json.loads(BUNDLE.read_text())

    def test_both_real_candidates_without_promotion(self):
        result = m.verify(m.ROOT, self.bundle)
        self.assertEqual([e['id'] for e in result['entries']], ['ISA.53.11', 'DEU.32.8'])
        self.assertTrue(result['composition_verified'])
        self.assertFalse(result['editorial_approval'])
        self.assertFalse(result['canonical_change_applied'])

    def test_normalization_preserves_consonants_and_punctuation(self):
        self.assertEqual(m.normalized('מֵ/עֲמַ֤ל נַפְשׁ/וֹ֙׃'), 'מעמל נפשו׃')

    def test_unchanged_base_coordinates_for_multiple_patches(self):
        patches = [{'start': 0, 'before': 'אב', 'after': 'אור', 'evidence': [0]},
                   {'start': 3, 'before': 'גד', 'after': 'ה', 'evidence': [0]}]
        self.assertEqual(m.compose('אב גד׃', patches, 1), 'אור ה׃')

    def test_overlap_wrong_unit_and_missing_evidence_fail(self):
        patch = self.bundle['entries'][0]['patches'][0]
        base = 'מעמל נפשו יראה ישבע'
        for change in ({'start': 11}, {'before': 'אחר'}, {'evidence': []},
                       {'evidence': [1]}, {'start': True}, {'after': 'אוֹר'}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                m.compose(base, [dict(patch, **change)], 1)
        with self.assertRaises(ValueError):
            m.compose(base, [patch, patch], 1)

    def test_drift_unsafe_path_duplicate_and_extra_field_fail(self):
        for mutation in ('hash', 'path', 'duplicate', 'extra'):
            b = copy.deepcopy(self.bundle)
            if mutation == 'hash': b['entries'][0]['baseline']['sha256'] = '0' * 64
            if mutation == 'path': b['entries'][0]['evidence'][0]['path'] = '../outside.md'
            if mutation == 'duplicate': b['entries'].append(b['entries'][0])
            if mutation == 'extra': b['approved'] = True
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                m.verify(m.ROOT, b)

    def test_repinning_candidate_does_not_hide_extra_source_change_or_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            b = copy.deepcopy(self.bundle)
            b['entries'] = b['entries'][:1]
            e = b['entries'][0]
            for pin in [e['baseline'], e['candidate'], *e['evidence']]:
                path = root / pin['path']
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((m.ROOT / pin['path']).read_bytes())
            target = root / e['candidate']['path']
            original = json.loads(target.read_text())
            for mutation in ('text', 'edition', 'approved', 'score'):
                c = copy.deepcopy(original)
                if mutation == 'text': c['source']['text'] += ' אור'
                if mutation == 'edition': c['source']['edition'] = 'WLC'
                if mutation == 'approved': c['restoration_draft']['approved'] = True
                if mutation == 'score': c['cross_check']['agreement'] = 0.95
                raw = json.dumps(c, ensure_ascii=False).encode()
                target.write_bytes(raw)
                e['candidate']['sha256'] = hashlib.sha256(raw).hexdigest()
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    m.verify(root, b)

    def test_symlink_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'actual.md').write_text('evidence')
            (root / 'alias.md').symlink_to(root / 'actual.md')
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                m.pinned(root, {'path': 'alias.md', 'sha256': hashlib.sha256(b'evidence').hexdigest()})


if __name__ == '__main__':
    unittest.main()
