import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from jsonschema import ValidationError
from tools.textual_restoration import reviewed_critical_source as m

RECORD = m.ROOT / 'sources/ot/pob_critical/isaiah/053/011.json'
TRUSTED_REVIEW = '2695236defe6209ccdd7806bd7f9e8696d261125ef09e1a6fd485c837b50043f'


TRUSTED_COMPOSITION = 'd7f01021de7d9b3817d1d75799958c6c0e87fca3320e36f74a7417ebb7f72b1e'


def validate(record, review):
    return m.validate(record, review, TRUSTED_COMPOSITION)


class ReviewedCriticalSourceTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECORD.read_text())

    def test_real_reviewed_source_without_application(self):
        result = validate(self.record, TRUSTED_REVIEW)
        self.assertTrue(result['source_record_verified'])
        self.assertFalse(result['canonical_application_approved'])
        self.assertFalse(result['publication_approved'])

    def test_cannot_self_approve_by_replacing_trusted_review_pin(self):
        self.record['provenance']['editorial_review']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Trusted editorial'):
            validate(self.record, TRUSTED_REVIEW)

    def test_unreviewed_text_apparatus_or_disclosure_is_rejected(self):
        for field in ('text', 'apparatus', 'note'):
            record = copy.deepcopy(self.record)
            if field == 'apparatus': record['source'][field][0]['note'] = 'Different claim'
            else: record['source'][field] += ' changed'
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate(record, TRUSTED_REVIEW)

    def test_schema_rejects_missing_provenance_mislabeling_and_publication(self):
        mutations = [lambda r:r.pop('provenance'),
                     lambda r:r['source'].update(edition='WLC'),
                     lambda r:r['provenance'].update(publication_approved=True),
                     lambda r:r['source'].update(language='Greek')]
        for mutation in mutations:
            record = copy.deepcopy(self.record); mutation(record)
            with self.assertRaises(ValidationError):
                validate(record, TRUSTED_REVIEW)

    def test_baseline_and_candidate_bindings_cannot_drift(self):
        for field in ('base', 'candidate', 'composition'):
            record = copy.deepcopy(self.record)
            record['provenance'][field]['sha256'] = '0' * 64
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate(record, TRUSTED_REVIEW)

    def test_invalid_revision_and_identity_are_rejected(self):
        record = copy.deepcopy(self.record)
        record['provenance']['base_revision'] = 'main'
        with self.assertRaises(ValidationError): validate(record, TRUSTED_REVIEW)
        self.record['reference'] = 'Isaiah 53:12'
        with self.assertRaisesRegex(ValueError, 'identity'): validate(self.record, TRUSTED_REVIEW)

    def test_baseline_is_read_from_git_not_live_canonical_file(self):
        original = m.pinned
        baseline = self.record['provenance']['base']['path']
        def reject_live_base(root, pin):
            if pin['path'] == baseline:
                raise AssertionError('Must use the immutable Git baseline')
            return original(root, pin)
        with patch.object(m, 'pinned', side_effect=reject_live_base):
            self.assertTrue(validate(self.record, TRUSTED_REVIEW)['source_record_verified'])

    def test_replacement_composition_cannot_be_reapproved_by_repinning(self):
        original = m.pinned
        path = self.record['provenance']['composition']['path']
        bundle = json.loads((m.ROOT / path).read_text())
        # Preserve the same resulting source while substituting another account
        # of which passage changed and what evidence supports that change.
        entry = bundle['entries'][0]
        candidate = json.loads((m.ROOT / entry['candidate']['path']).read_text())
        base = candidate['restoration_draft']['baseline']['source']['text']
        entry['patches'] = [{'start': 0, 'before': m.normalized(base),
                            'after': candidate['source']['text'], 'evidence': [0]}]
        entry['evidence'] = [entry['candidate']]
        replacement = json.dumps(bundle, ensure_ascii=False).encode()
        self.record['provenance']['composition']['sha256'] = hashlib.sha256(replacement).hexdigest()
        def substituted(root, pin):
            return replacement if pin['path'] == path else original(root, pin)
        with patch.object(m, 'pinned', side_effect=substituted):
            with self.assertRaisesRegex(ValueError, 'Trusted composition'):
                validate(self.record, TRUSTED_REVIEW)

    def test_input_records_and_canonical_bytes_are_not_written(self):
        paths = [RECORD, *[m.ROOT / p['path'] for k,p in self.record['provenance'].items() if isinstance(p,dict)]]
        before = {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        original = copy.deepcopy(self.record)
        validate(self.record, TRUSTED_REVIEW)
        self.assertEqual(self.record, original)
        self.assertEqual(before, {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})


if __name__ == '__main__':
    unittest.main()
