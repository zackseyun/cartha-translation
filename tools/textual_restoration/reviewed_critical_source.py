"""Read-only source-record verification; no verse application or publication.

External trusted review and composition hashes are mandatory: a mutable source
record cannot approve itself or substitute its own patch/evidence history. The original base is read
from Git so later canonical application need not destroy source provenance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import yaml
from jsonschema import Draft202012Validator

from tools.textual_restoration.verify_source_composition import (
    ROOT, NORMALIZATION, compose, normalized, pinned, require,
)

SCHEMA = 'schemas/ot-reviewed-critical-source.schema.json'
NOTE = ('Provisional editorial composite, not a transcription of one manuscript '
        'or a recovered autograph. The unpointed text retains the declared base '
        'except for the recorded changes; interpretive vocalization outside '
        'those changes follows the base.')


def validate(record, trusted_review_sha256, trusted_composition_sha256, *, root=ROOT):
    root = Path(root).resolve()
    Draft202012Validator(json.loads((root / SCHEMA).read_text())).validate(record)
    p = record['provenance']
    require(p['editorial_review']['sha256'] == trusted_review_sha256, 'Trusted editorial review mismatch')
    require(p['composition']['sha256'] == trusted_composition_sha256, 'Trusted composition mismatch')
    review = json.loads(pinned(root, p['editorial_review']))
    require(review.get('source_selection_approved') is True and review.get('full_record_editorially_approved') is True, 'Editorial approval absent')
    require(review.get('candidate') == p['candidate'], 'Review/candidate binding mismatch')
    candidate = json.loads(pinned(root, p['candidate']))
    bundle = json.loads(pinned(root, p['composition']))
    require(bundle.get('version') == 1 and bundle.get('normalization') == NORMALIZATION, 'Composition contract mismatch')
    entries = [e for e in bundle['entries'] if e['id'] == record['id']]
    require(len(entries) == 1, 'Composition entry missing or duplicated')
    entry = entries[0]
    require(entry['candidate'] == p['candidate'] and entry['baseline'] == p['base'], 'Composition provenance mismatch')
    path = Path(p['base']['path'])
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix().startswith('translation/ot/'), 'Unsafe baseline path')
    require(re.fullmatch(r'[0-9a-f]{40}', p['base_revision']), 'Full Git revision required')
    raw = subprocess.run(['git', '-C', str(root), 'show', f"{p['base_revision']}:{path.as_posix()}"], check=True, capture_output=True).stdout
    require(hashlib.sha256(raw).hexdigest() == p['base']['sha256'], 'Historical baseline drift')
    base = yaml.safe_load(raw)
    require(base['id'] == candidate['id'] == record['id'] and base['reference'] == candidate['reference'] == record['reference'], 'Verse identity mismatch')
    require(base['source']['edition'] in {'WLC', 'UHB'}, 'Unsupported baseline edition')
    require(candidate['source']['edition'] == 'POB-critical-draft', 'Reviewed input must be the declared candidate')
    require(review.get('input_pins', {}).get(path.as_posix()) == p['base']['sha256'], 'Review baseline binding missing')
    for name, digest in review['input_pins'].items():
        if name != path.as_posix():
            pinned(root, {'path': name, 'sha256': digest})
    for pin in entry['evidence']:
        pinned(root, pin)
    text = compose(normalized(base['source']['text']), entry['patches'], len(entry['evidence']))
    require(text == candidate['source']['text'] == record['source']['text'], 'Unreviewed source text')
    require(record['source']['apparatus'] == candidate['source']['apparatus'], 'Unreviewed apparatus')
    require(record['source']['note'] == NOTE, 'Unexpected source-composition disclosure')
    # Fresh checks cover mutable evidence/review/candidate files, not just schema.
    for pin in [p['editorial_review'], p['candidate'], p['composition'], *entry['evidence']]:
        pinned(root, pin)
    return {'source_record_verified': True, 'selection_status': p['selection_status'],
            'canonical_application_approved': False, 'publication_approved': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--trusted-review-sha256', required=True)
    parser.add_argument('--trusted-composition-sha256', required=True)
    args = parser.parse_args()
    print(json.dumps(validate(json.loads(args.record.read_text()), args.trusted_review_sha256, args.trusted_composition_sha256), indent=2))


if __name__ == '__main__':
    main()
