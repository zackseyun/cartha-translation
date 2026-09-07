import copy
import json
import unittest

from jsonschema import ValidationError
from tools.textual_restoration import critical_verse as m

SOURCE_PIN = {'path': 'sources/ot/pob_critical/isaiah/053/011.json',
              'sha256': 'f7014f607b0344d8a3b5723cd7edcc314029916dfeee4c341d9dd9b394f0f9e9'}
TRUST = {
    'trusted_source_sha256': SOURCE_PIN['sha256'],
    'trusted_review_sha256': '2695236defe6209ccdd7806bd7f9e8696d261125ef09e1a6fd485c837b50043f',
    'trusted_composition_sha256': 'd7f01021de7d9b3817d1d75799958c6c0e87fca3320e36f74a7417ebb7f72b1e',
}


class CriticalVerseTests(unittest.TestCase):
    def setUp(self):
        self.record = m.compose_record(SOURCE_PIN, **TRUST)

    def test_real_full_verse_is_accepted_without_application_approval(self):
        result = m.validate(self.record, **TRUST)
        self.assertTrue(result['full_critical_verse_verified'])
        self.assertFalse(result['canonical_application_approved'])
        self.assertFalse(result['publication_approved'])
        self.assertEqual(self.record['source']['edition'], 'POB-critical')

    def test_every_non_source_candidate_field_is_preserved(self):
        candidate = json.loads((m.ROOT / 'sources/textual_restoration/applications/isaiah53_11_candidate.v1.json').read_text())
        restored = copy.deepcopy(self.record)
        restored.pop('critical_source_integration')
        restored['source'] = candidate['source']
        self.assertEqual(restored, candidate)

    def test_unreviewed_english_notes_rationale_and_history_fail(self):
        for field in ('english', 'note', 'lexical', 'history', 'score'):
            record = copy.deepcopy(self.record)
            if field == 'english': record['translation']['text'] += ' Added.'
            if field == 'note': record['translation']['footnotes'][0]['text'] = 'Certain original.'
            if field == 'lexical': record['lexical_decisions'][0]['rationale'] = 'Different claim.'
            if field == 'history': record['revisions'] = []
            if field == 'score': record['cross_check']['agreement'] = 1
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'Full verse differs'):
                m.validate(record, **TRUST)

    def test_missing_provenance_and_wrong_edition_fail_schema(self):
        for mutation in ('provenance', 'edition'):
            record = copy.deepcopy(self.record)
            if mutation == 'provenance': record.pop('critical_source_integration')
            else: record['source']['edition'] = 'WLC'
            with self.assertRaises(ValidationError): m.validate(record, **TRUST)

    def test_false_to_zero_changes_in_archival_metadata_fail(self):
        for field in ('preparation', 'history'):
            record = copy.deepcopy(self.record)
            if field == 'preparation': record['restoration_draft']['approved'] = 0
            else: record['review_history'][0]['certifies_this_candidate'] = 0
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'Full verse differs'):
                m.validate(record, **TRUST)

    def test_record_cannot_replace_its_source_pin(self):
        self.record['critical_source_integration']['record']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Trusted source-record'):
            m.validate(self.record, **TRUST)

    def test_schema_checks_existing_full_verse_fields_offline(self):
        self.record['translation']['philosophy'] = 'unrecognized'
        with self.assertRaises(ValidationError): m.schema_validator().validate(self.record)

    def test_live_verse_remains_unchanged(self):
        path = m.ROOT / 'translation/ot/isaiah/053/011.yaml'
        before = path.read_bytes()
        m.validate(self.record, **TRUST)
        self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
