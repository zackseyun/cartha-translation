"""Compose/validate a full critical verse in memory, never apply or approve it."""
import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from tools.textual_restoration import reviewed_critical_source as source_checks
from tools.textual_restoration.verify_source_composition import ROOT, pinned, require

SCHEMA = 'schemas/ot-critical-verse.schema.json'


def schema_validator(root=ROOT):
    root = Path(root)
    legacy = json.loads((root / 'schema/verse.schema.json').read_text())
    source = json.loads((root / source_checks.SCHEMA).read_text())
    schema = json.loads((root / SCHEMA).read_text())
    registry = Registry().with_resources([
        (legacy['$id'], Resource.from_contents(legacy)),
        ('urn:pob:reviewed-critical-source:1', Resource.from_contents(source)),
    ])
    return Draft202012Validator(schema, registry=registry)


def compose_record(source_pin, *, trusted_source_sha256, trusted_review_sha256,
                   trusted_composition_sha256, root=ROOT):
    root = Path(root).resolve()
    require(source_pin['sha256'] == trusted_source_sha256, 'Trusted source-record mismatch')
    source_raw = pinned(root, source_pin)
    source = json.loads(source_raw)
    source_checks.validate(source, trusted_review_sha256, trusted_composition_sha256, root=root)
    candidate_pin = source['provenance']['candidate']
    candidate_raw = pinned(root, candidate_pin)
    out = copy.deepcopy(json.loads(candidate_raw))
    # Only the source stage/disclosure changes. All approved English, notes,
    # rationales, historical data and review flags remain byte-value identical.
    out['source'] = copy.deepcopy(source['source'])
    out['critical_source_integration'] = {
        'record': copy.deepcopy(source_pin),
        'restoration_draft_role': 'historical-preparation-not-current-selection-status',
    }
    schema_validator(root).validate(out)
    require(pinned(root, source_pin) == source_raw and pinned(root, candidate_pin) == candidate_raw,
            'Integration inputs changed during validation')
    return out


def validate(record, *, trusted_source_sha256, trusted_review_sha256,
             trusted_composition_sha256, root=ROOT):
    schema_validator(root).validate(record)
    expected = compose_record(record['critical_source_integration']['record'],
                              trusted_source_sha256=trusted_source_sha256,
                              trusted_review_sha256=trusted_review_sha256,
                              trusted_composition_sha256=trusted_composition_sha256,
                              root=root)
    # Python equality conflates False/0 and True/1. Preserve JSON scalar types,
    # including archival fields that the legacy schema leaves unconstrained.
    canonical = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True,
                                         separators=(',', ':'), allow_nan=False)
    require(canonical(record) == canonical(expected),
            'Full verse differs from the reviewed candidate integration')
    return {'full_critical_verse_verified': True, 'canonical_application_approved': False,
            'publication_approved': False}
