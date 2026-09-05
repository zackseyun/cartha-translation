#!/usr/bin/env python3
"""Event-driven revisions statistics refresh; no daemon or periodic scan.

Batch completion writes a durable request and starts a short-lived worker.
Requests coalesce for 60 seconds, one worker owns the lock, and unchanged
source metadata skips YAML parsing. On battery a request stays pending until
another batch or an explicit refresh on AC; there is no power-polling daemon.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

OUTPUTS = ('revisions.json', 'revisions-summary.json')


def state_dir(repo: Path) -> Path:
    path = repo / 'state' / 'revisions-refresh'
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def write_json(path: Path, value: dict) -> None:
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    tmp.write_text(json.dumps(value) + '\n')
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)


def request_refresh(repo: Path, *, background: bool = True) -> None:
    """Called once after a real batch, not on each verse or idle poll."""
    repo = repo.resolve()
    state = state_dir(repo)
    write_json(state / 'request.json', {'id': uuid.uuid4().hex, 'at': time.time()})
    if background:
        with (state / 'worker.log').open('ab') as log:
            subprocess.Popen([sys.executable, str(Path(__file__).resolve()),
                              '--repo', str(repo), '--run-pending', '--publish'],
                             stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                             start_new_session=True, close_fds=True)


def request_after_batch(repo: Path) -> None:
    """Dashboard maintenance must not turn successful translation into failure."""
    try:
        request_refresh(repo)
    except Exception as exc:
        print(f'[revisions-refresh] could not queue dashboard refresh: {exc}', flush=True)


def on_ac_power() -> bool:
    if sys.platform != 'darwin':
        return True
    try:
        result = subprocess.run(['/usr/bin/pmset', '-g', 'batt'],
                                capture_output=True, text=True, timeout=5, check=True)
        return "Now drawing from 'AC Power'" in result.stdout
    except (OSError, subprocess.SubprocessError):
        return False  # unknown power state must not start a costly laptop scan


def source_fingerprint(repo: Path) -> str:
    """Metadata-only, after a batch event; never parses the verse/review corpus."""
    digest = hashlib.sha256()
    paths = []
    for relative in ('translation', 'state/reviews'):
        root = repo / relative
        for parent, dirs, files in os.walk(root):
            dirs.sort()
            for name in sorted(files):
                if name.endswith(('.yaml', '.json')):
                    paths.append(Path(parent) / name)
    paths.extend(repo / name for name in ('tools/build_revisions_index.py',
                 'tools/lxx_swete.py', 'book_metadata.json'))
    for path in paths:
        try:
            st = path.stat()
            digest.update(f'{path.relative_to(repo)}:{st.st_size}:{st.st_mtime_ns}\n'.encode())
        except FileNotFoundError:
            digest.update(f'{path.relative_to(repo)}:missing\n'.encode())
    return digest.hexdigest()


def output_stamp(repo: Path) -> dict:
    return {name: [int((repo/name).stat().st_size), (repo/name).stat().st_mtime_ns]
            for name in OUTPUTS if (repo/name).is_file()}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=repo, text=True,
                                   stderr=subprocess.STDOUT).strip()


def prepare_publish(repo: Path) -> None:
    if git(repo, 'branch', '--show-current') != 'main':
        raise RuntimeError('publish deferred: merge the completed batch onto main first')
    if git(repo, 'diff', '--cached', '--name-only'):
        raise RuntimeError('publish deferred: existing staged changes were left untouched')
    dirty = git(repo, 'diff', '--name-only', 'HEAD').splitlines()
    if any(path not in OUTPUTS for path in dirty):
        raise RuntimeError('publish deferred: commit the completed batch; unrelated local changes were left untouched')
    # Never rebase/autostash a user checkout in the background. Fast-forward
    # only when clean, so a pending dashboard-only commit can simply retry push.
    if not dirty:
        git(repo, 'fetch', 'origin', 'main')
        if git(repo, 'rev-list', '--count', 'HEAD..origin/main') != '0':
            git(repo, 'merge', '--ff-only', 'origin/main')


def publish(repo: Path) -> None:
    if git(repo, 'status', '--porcelain', '--untracked-files=normal', '--', *OUTPUTS):
        git(repo, 'add', '--', *OUTPUTS)
        git(repo, 'commit', '--only', '-m', 'revisions: refresh after completed batch [skip ci]', '--', *OUTPUTS)
    # Retry an earlier successful commit whose push failed, even when clean.
    git(repo, 'push', 'origin', 'HEAD:main')


def run_pending(repo: Path, *, publish_changes: bool = False,
                allow_battery: bool = False, quiet_seconds: float = 60) -> int:
    state = state_dir(repo)
    with (state / 'worker.lock').open('a') as lock:
        # Wait rather than dropping a request in the tiny exit/unlock race.
        # Waiting workers immediately return without scanning when the owner
        # has already consumed their generation.
        fcntl.flock(lock, fcntl.LOCK_EX)
        while True:
            request = read_json(state / 'request.json')
            if not request or request.get('id') == read_json(state / 'completed.json').get('id'):
                print('[revisions-refresh] no pending batch; no scan', flush=True)
                return 0
            if not allow_battery and not on_ac_power():
                print('[revisions-refresh] pending on battery; retry after plugging in', flush=True)
                return 0
            delay = quiet_seconds - (time.time() - request.get('at', 0))
            if delay > 0:
                time.sleep(min(delay, 5))  # only a queued, short-lived worker waits
                continue
            try:
                if publish_changes:
                    prepare_publish(repo)
                signature = source_fingerprint(repo)
                cached = read_json(state / 'built.json')
                outputs_changed = cached.get('outputs') != output_stamp(repo)
                missing = any(not (repo / name).is_file() for name in OUTPUTS)
                if signature != cached.get('signature') or missing or outputs_changed:
                    subprocess.run([sys.executable, str(repo / 'tools/build_revisions_index.py')],
                                   cwd=repo, check=True, timeout=3600)
                    if source_fingerprint(repo) != signature:
                        print('[revisions-refresh] inputs changed during build; keeping request pending', flush=True)
                        # Another completion event lets this same worker retry.
                        if read_json(state / 'request.json').get('id') != request['id']:
                            continue
                        return 0
                    for name in OUTPUTS:
                        if not isinstance(json.loads((repo/name).read_text()), dict):
                            raise RuntimeError(f'invalid generated snapshot: {name}')
                    write_json(state / 'built.json', {'signature': signature, 'outputs': output_stamp(repo)})
                else:
                    print('[revisions-refresh] inputs unchanged; skipped rebuild', flush=True)
                if publish_changes:
                    # Recheck before staging anything: concurrent edits are not ours.
                    prepare_publish(repo)
                    if source_fingerprint(repo) != signature:
                        print('[revisions-refresh] inputs changed before publish; keeping pending', flush=True)
                        return 0
                    publish(repo)
                write_json(state / 'completed.json', {'id': request['id']})
                # A request arriving mid-build is consumed on the next iteration;
                # identical inputs skip the expensive builder and remain serialized.
            except (OSError, ValueError, subprocess.SubprocessError, RuntimeError) as exc:
                print(f'[revisions-refresh] pending; refresh failed: {exc}', flush=True)
                return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--request', action='store_true', help='Record a completed batch')
    parser.add_argument('--background', action='store_true', help='Queue a short-lived worker and return')
    parser.add_argument('--run-pending', action='store_true', help='Retry queued work without a new event')
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--allow-battery', action='store_true', help='Explicit manual override')
    parser.add_argument('--quiet-seconds', type=float, default=60)
    args = parser.parse_args()
    if args.background:
        if not args.request:
            parser.error('--background requires --request')
        request_refresh(args.repo)
        return 0
    if args.request:
        request_refresh(args.repo, background=False)
    return run_pending(args.repo.resolve(), publish_changes=args.publish,
                       allow_battery=args.allow_battery, quiet_seconds=args.quiet_seconds)


if __name__ == '__main__':
    raise SystemExit(main())
