"""Read-only whole-OT verification for explicitly reviewed critical successors.

Preserves the completed note applications without projecting away live source
changes. A separate manual edit and application receipt perform the mutation.
"""
from functools import lru_cache
import argparse
import json
from pathlib import Path

import yaml

from tools.textual_restoration import critical_verse
from tools.textual_restoration import verify_corpus_successor as previous

ROOT = previous.ROOT
CHECKPOINT = '783e61ec70c5a152468f5cbe619656e0857182d4'
PREFIX = 'sources/textual_restoration/applications/'
MIGRATED = 'tests/test_corpus_successor.py'
JOB = 'translation/ot/job/013/015.yaml'
PRIOR_PINS = {
    PREFIX + 'job13_15_successor_plan.v1.json': '72bae7e99c21fbc9433eb78ab8b64e81391da96be678e5c8776e474bcdfe7945',
    PREFIX + 'job13_15_successor_review.v1.json': '26e6e02bfe089a3eb448441b1bffefa0d9ce4029316397d419e245d8bc34c4f2',
    PREFIX + 'job13_15_successor_application.v1.json': 'fb85aa879265820e344666e917bdbe0feea03bcc3252e65de09d639b90626803',
}
BINDINGS = (
    'tools/textual_restoration/verify_critical_successor.py',
    'tools/textual_restoration/critical_verse.py',
    'tools/textual_restoration/reviewed_critical_source.py',
    'tools/textual_restoration/verify_source_composition.py',
    'schemas/ot-critical-verse.schema.json',
    'schemas/ot-reviewed-critical-source.schema.json',
    'schema/verse.schema.json',
    'tools/textual_restoration/verify_corpus_successor.py',
    'tools/textual_restoration/check_live_note_integrity.py',
    'tools/textual_restoration/replay_unflagged_sample.py',
    'tools/export_mobile_bible.py',
    'tools/textual_restoration/replay_source_predecessor_tests.py',
    'tests/test_corpus_successor.py', 'tests/test_source_composition.py',
    'tests/test_critical_successor.py',
)
safe_read, sha, blob = previous.safe_read, previous.sha, previous.blob
require, json_sha, git = previous.require, previous.json_sha, previous.git


@lru_cache(maxsize=1)
def checkpoint():
    require(git(ROOT, 'rev-parse', '--verify', CHECKPOINT + '^{commit}').decode().strip() == CHECKPOINT,
            'Checkpoint mismatch')
    tree = {}
    for entry in git(ROOT, 'ls-tree', '-rz', CHECKPOINT, '--', 'translation/ot').split(b'\0'):
        if not entry:
            continue
        meta, path = entry.decode().split('\t', 1)
        mode, kind, oid = meta.split()
        require(mode == '100644' and kind == 'blob', 'Nonregular checkpoint corpus entry')
        if path.endswith('.yaml'):
            tree[path] = oid
    require(tree, 'Empty checkpoint')
    return tree


def prior_context(root):
    """Original package hashes stay fixed; only the named test wrapper migrates."""
    for path, digest in PRIOR_PINS.items():
        require(sha(safe_read(root, path)) == digest, 'Prior Job package drift')
    plan = json.loads(safe_read(root, PREFIX + 'job13_15_successor_plan.v1.json'))
    review = json.loads(safe_read(root, PREFIX + 'job13_15_successor_review.v1.json'))
    application = json.loads(safe_read(root, PREFIX + 'job13_15_successor_application.v1.json'))
    require(application['status'] == 'applied-verified', 'Prior Job application not applied')
    pins, samuel_export = previous.protected()
    for path, digest in {**pins, **plan['input_pins'], **review['implementation_pins']}.items():
        if path != MIGRATED:
            require(sha(safe_read(root, path)) == digest, 'Prior protected input drift: ' + path)
    live = previous.check_current(root)
    job_change = plan['changes'][0]
    job_raw = safe_read(root, job_change['candidate'])
    require(job_change['target'] == JOB and sha(job_raw) == job_change['after_sha256'], 'Prior Job candidate drift')
    require(safe_read(root, JOB) == job_raw, 'Applied Job disclosure drift')
    expected = dict(previous.checkpoint())
    expected[JOB] = blob(job_raw)
    require(checkpoint() == expected, 'New checkpoint is not the verified prior corpus successor')
    return {'protected_targets': [*live['completed_note_targets'], JOB, 'translation/ot/2_samuel/013/037.yaml'],
            'preserved_exports': {'JOB': {'chapters': 42, 'verses': 1070, 'sha256': plan['books']['JOB']['candidate_export_sha256']},
                                  '2SA': {'chapters': 24, 'verses': 695, 'sha256': samuel_export}},
            'completed_note_files_verified': live['files_verified']}


def corpus_state(live, baseline, candidate):
    require(live == baseline or live == candidate, 'Unapproved or partial corpus state')
    return 'baseline' if live == baseline else 'candidate'


def verify(plan_path, review_path, trusted_review_sha256, *, root=ROOT):
    root = Path(root).resolve()
    require(root == ROOT, 'Actual corpus/export checks require the repository root')
    review_raw, plan_raw = safe_read(root, review_path), safe_read(root, plan_path)
    require(sha(review_raw) == trusted_review_sha256, 'Trusted application review mismatch')
    review, plan = json.loads(review_raw), json.loads(plan_raw)
    require(review.get('plan_sha256') == sha(plan_raw), 'Reviewed plan mismatch')
    require(review.get('canonical_application_approved') is True and review.get('publication_approved') is False,
            'Application review scope mismatch')
    require(set(review.get('implementation_pins', {})) == set(BINDINGS), 'Missing implementation bindings')
    for path, digest in review['implementation_pins'].items():
        require(sha(safe_read(root, path)) == digest, 'Reviewed implementation drift: ' + path)
    require(plan.get('checkpoint') == CHECKPOINT and plan.get('scope') == 'critical-source-and-English', 'Plan scope mismatch')
    prior = prior_context(root)
    baseline, candidate_tree = dict(checkpoint()), dict(checkpoint())
    require(isinstance(plan.get('changes'), list) and plan['changes'], 'Changes required')
    seen, books = set(), set()
    for change in plan['changes']:
        target = change['target']
        require(target in baseline and target not in seen and target not in prior['protected_targets'], 'Unknown, repeated or protected target')
        seen.add(target)
        before_raw = git(ROOT, 'show', f'{CHECKPOINT}:{target}')
        after_raw = safe_read(root, change['candidate'])
        require(sha(before_raw) == change['before_sha256'] and sha(after_raw) == change['after_sha256'], 'Before/after binding drift')
        before, after = yaml.safe_load(before_raw), yaml.safe_load(after_raw)
        require(before['id'] == after['id'] and before['reference'] == after['reference'], 'Target identity mismatch')
        critical_verse.validate(after, root=root, **change['trust'])
        candidate_tree[target] = blob(after_raw)
        books.add(before['id'].split('.')[0])
    require(set(plan.get('books', {})) == books, 'Affected-book coverage mismatch')
    start = previous.current_corpus(root)
    state = corpus_state(start, baseline, candidate_tree)
    exports = {}
    for code in sorted(books | set(prior['preserved_exports'])):
        actual = previous.exporter.export_book(code)
        result = {'chapters': len(actual['chapters']),
                  'verses': sum(len(c['verses']) for c in actual['chapters']), 'sha256': json_sha(actual)}
        if code in prior['preserved_exports']:
            require(result == prior['preserved_exports'][code], 'Prior note export drift')
        if code in books:
            spec = plan['books'][code]
            require(result == {'chapters': spec['chapters'], 'verses': spec['verses'],
                               'sha256': spec[state + '_export_sha256']}, 'Affected-book export drift')
        exports[code] = result
    require(previous.current_corpus(root) == start, 'Corpus changed during verification')
    require(prior_context(root) == prior, 'Prior context changed during verification')
    require(safe_read(root, review_path) == review_raw and safe_read(root, plan_path) == plan_raw, 'Plan/review changed during verification')
    for path, digest in review['implementation_pins'].items():
        require(sha(safe_read(root, path)) == digest, 'Implementation changed during verification')
    for change in plan['changes']:
        raw = safe_read(root, change['candidate'])
        require(sha(raw) == change['after_sha256'], 'Candidate changed during verification')
        critical_verse.validate(yaml.safe_load(raw), root=root, **change['trust'])
    return {'state': state, 'checkpoint': CHECKPOINT, 'plan_sha256': sha(plan_raw),
            'review_sha256': trusted_review_sha256, 'canonical_yaml_count': len(start),
            'actual_exports': exports, 'current_corpus_verified': True,
            'prior_note_applications_preserved': True, 'canonical_files_written': False,
            'publication_approved': False}


def verify_applied(plan, review, trusted_review_sha256, application, trusted_application_sha256):
    raw = safe_read(ROOT, application)
    require(sha(raw) == trusted_application_sha256, 'Trusted application receipt mismatch')
    record = json.loads(raw)
    actual = verify(plan, review, trusted_review_sha256)
    require(record.get('status') == 'applied-verified' and actual['state'] == 'candidate', 'Application absent or rolled back')
    require(json_sha(record.get('after')) == json_sha(actual), 'Stale application receipt')
    before = record.get('before', {})
    require(before.get('state') == 'baseline' and before.get('checkpoint') == CHECKPOINT
            and before.get('review_sha256') == trusted_review_sha256 and before.get('plan_sha256') == actual['plan_sha256'], 'Invalid before receipt')
    require(safe_read(ROOT, application) == raw, 'Application receipt changed')
    return {**actual, 'application_record_verified': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan')
    parser.add_argument('review')
    parser.add_argument('--trusted-review-sha256', required=True)
    parser.add_argument('--application')
    parser.add_argument('--trusted-application-sha256')
    args = parser.parse_args()
    if bool(args.application) != bool(args.trusted_application_sha256):
        parser.error('--application and --trusted-application-sha256 must be supplied together')
    result = (verify_applied(args.plan, args.review, args.trusted_review_sha256,
                             args.application, args.trusted_application_sha256)
              if args.application else verify(args.plan, args.review, args.trusted_review_sha256))
    print(json.dumps(result, indent=2))
