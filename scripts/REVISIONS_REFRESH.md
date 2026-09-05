# Revisions dashboard refresh: completed batches only

The former 30-minute `cob` / `pob` revisions LaunchAgent is retired. Do not
reinstall it. There is no periodic full scan, directory watcher, or persistent
refresh daemon.

## What requests a refresh

- A completed merge/publication through `scripts/sync_pob.sh`.
- The chapter master supervisor reaching a drained queue.
- A Gemini review worker finishing its batch or first reaching an empty queue
  after doing work (not every idle poll).
- An auto-apply cycle or one-shot that actually applied changes; never dry runs.
- An Azure bulk review completing real work; never dry runs.

Other custom/editorial batches should finish with:

```bash
scripts/pob-revisions-flywheel.sh --background
```

This records a durable request under gitignored `state/revisions-refresh/` and
launches a short-lived worker. Requests coalesce for 60 seconds. A filesystem
lock serializes workers. A metadata-only input fingerprint skips the expensive
YAML/review parse when inputs match the previous successful build. A failed
publish can retry without rebuilding identical statistics. Requests arriving
during a build are retained; inputs changed during a build are not published.

## Laptop and publication safety

On a Mac, no automatic scan starts unless AC power is confirmed. Battery or
unknown power leaves the request pending and exits; **plugging in alone does not
start a process**. The next completed batch retries, or explicitly retry on AC:

```bash
python3 tools/revisions_refresh.py --run-pending --publish --quiet-seconds 0
```

A deliberate manual refresh may use `--allow-battery`. This is an override,
not a setting that enables periodic battery work.

Publication requires main, no staged changes, and no unrelated tracked changes.
Commit/merge the completed translation batch first. The worker never rebases,
autostashes, force-pushes, or adds unrelated files. A rejected fast-forward or
push leaves the request pending, with details in `state/revisions-refresh/worker.log`.
Clean source checkouts can fast-forward before refreshing. Side worktrees should
be merged into main before dashboard publication; local-only reviews must be
available in the checkout performing the refresh.

Only `revisions.json` and `revisions-summary.json` are published. Bible text,
reader behavior, and CDN Bible-text releases are unchanged.

## Retire an existing install

Unload the old LaunchAgent and move its plist out of `~/Library/LaunchAgents`
(keep a rollback copy). Both historical labels must be checked:
`com.cartha.cob-revisions-flywheel` and `com.cartha.pob-revisions-flywheel`.
The old `~/scripts/cob-revisions-flywheel.sh` command can remain as a compatibility
wrapper invoking the repository's new `scripts/pob-revisions-flywheel.sh`.
No launchd job replaces it.

## Verification

```bash
python3 -m unittest discover -s tests -p test_revisions_refresh.py -v
```

Tests use tiny temporary fixtures and mock publication, never the production
corpus or live credentials. They cover idle/no-scan, battery deferral, manual
override, unchanged work, review edits/deletions, translation edits, missing
outputs, build/push failures, overlapping requests, and concurrent source edits.
