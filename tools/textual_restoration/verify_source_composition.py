"""Verify explicit Hebrew base-plus-patch provenance; never approve or apply text.

Offsets are Unicode code points in the normalized base, not UTF-8 bytes or
positions in an evolving intermediate string. Evidence hashes bind documents,
not their truth. The caller must obtain editorial approval separately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import unicodedata

import yaml

ROOT = Path(__file__).resolve().parents[2]
NORMALIZATION = 'NFD-remove-combining-marks-and-slash-v1'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn' and c != '/')


def pinned(root, pin):
    require(set(pin) == {'path', 'sha256'}, 'Invalid file pin fields')
    path = Path(pin['path'])
    require(not path.is_absolute() and '..' not in path.parts, 'Unsafe pin path')
    target = root / path
    require(not any(p.is_symlink() for p in [target, *target.parents]), 'Symlink pin')
    require(target.is_file(), 'Missing pinned file')
    raw = target.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'Pinned file drift')
    return raw


def compose(base, patches, evidence_count):
    require(isinstance(patches, list) and patches, 'Patches required')
    end = 0
    chunks = []
    for p in patches:
        require(set(p) == {'start', 'before', 'after', 'evidence'}, 'Invalid patch fields')
        start, before, after = p['start'], p['before'], p['after']
        require(type(start) is int and end <= start <= len(base), 'Overlapping or unordered offsets')
        require(isinstance(before, str) and before and isinstance(after, str), 'Invalid patch text')
        require(before != after and normalized(after) == after, 'Patch must change unpointed text')
        require(base[start:start + len(before)] == before, 'Patch does not match base')
        refs = p['evidence']
        require(isinstance(refs, list) and refs and all(type(i) is int and 0 <= i < evidence_count for i in refs), 'Patch evidence missing')
        chunks.extend([base[end:start], after])
        end = start + len(before)
    return ''.join(chunks) + base[end:]


def verify(root, bundle):
    root = Path(root).resolve()
    require(set(bundle) == {'version', 'normalization', 'entries'}, 'Invalid bundle fields')
    require(bundle['version'] == 1 and bundle['normalization'] == NORMALIZATION, 'Unsupported composition contract')
    require(isinstance(bundle['entries'], list) and bundle['entries'], 'Entries required')
    seen = set()
    results, inputs = [], []
    for entry in bundle['entries']:
        require(set(entry) == {'id', 'baseline', 'candidate', 'evidence', 'patches'}, 'Invalid entry fields')
        require(entry['id'] not in seen, 'Duplicate verse')
        seen.add(entry['id'])
        require(entry['baseline']['path'].startswith('translation/ot/'), 'Baseline must be canonical OT')
        require(entry['candidate']['path'].startswith('sources/textual_restoration/applications/'), 'Candidate must be a research artifact')
        base_raw = pinned(root, entry['baseline'])
        candidate_raw = pinned(root, entry['candidate'])
        base, candidate = yaml.safe_load(base_raw), json.loads(candidate_raw)
        require(base['id'] == candidate['id'] == entry['id'], 'Verse identity mismatch')
        require(base['source']['edition'] in {'WLC', 'UHB'}, 'Unsupported base edition')
        require(candidate['source']['edition'] == 'POB-critical-draft', 'Composite must not impersonate base edition')
        require(candidate['source'].get('language') == 'Hebrew', 'Hebrew composition only')
        require(isinstance(candidate['source'].get('note'), str) and candidate['source']['note'].strip(), 'Source disclosure required')
        draft = candidate.get('restoration_draft', {})
        require(draft.get('approved') is False and candidate.get('status') == 'draft', 'Unapproved draft only')
        require(draft.get('canonical_change_applied', False) is False and draft.get('publication_ready', False) is False, 'No application or publication claim')
        require(candidate.get('cross_check') == {'status': 'needs_review'}, 'No inherited approval score')
        evidence = entry['evidence']
        require(isinstance(evidence, list) and evidence, 'Evidence documents required')
        for pin in evidence:
            require(pin['path'].endswith(('.json', '.md', '.yaml')), 'Evidence must be a textual record, not an image')
            pinned(root, pin)
        source = compose(normalized(base['source']['text']), entry['patches'], len(evidence))
        require(source == candidate['source']['text'], 'Unexplained source change')
        inputs.extend([entry['baseline'], entry['candidate'], *evidence])
        results.append({'id': entry['id'], 'source_text': source,
                        'patch_count': len(entry['patches'])})
    # Recheck all consumed inputs before reporting; this is not a write lock.
    for pin in inputs:
        pinned(root, pin)
    return {'composition_verified': True, 'editorial_approval': False,
            'canonical_change_applied': False, 'entries': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(ROOT, json.loads(args.bundle.read_text())), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
