# Historical research tests versus current translation integrity

## Decision

Supersede the **current test consumers**, not the frozen research records.
The previous Genesis transaction bound the current sample test's bytes while
that test also required the original whole-OT corpus. Adding another legitimate
note therefore broke historical replay. Extending per-verse overlays would
couple every later change to that old experiment.

The [runner](../tools/textual_restoration/replay_historical_tests.py) instead
executes unmodified tests/code/data at trusted Git checkpoint
`7637f998fd1edd9f7ab1acabf1e3037f2024b7e7` in a temporary archive. Its only
allowed suites are the original 28 Genesis transaction tests, four unflagged
sample tests and five Genesis-related registry tests. The fixed checkpoint
contains the old test bytes required by the original guards. No historical
receipt, executor or application ledger is rewritten or silently rebound.

The three current test files explicitly dispatch those historical checks.
Current normalization and 47 current registry tests remain live, including a
synthetic-fixture test proving the current validator reports changed canonical
bytes. Synthetic fixture hashes are not research approvals.

## Live protections retained

The separate [live integrity audit](../tools/textual_restoration/check_live_note_integrity.py)
checks 83 exact expected files: the three completed canonical notes, Genesis
package/ledger/method bindings, transitive prior-package input pins, and three
explicitly hash-bound migrated test files. Expectations come from the fixed Git
checkpoint, never by accepting hashes from edited current manifests. Only those
three test replacements supersede historical test bytes. Rollback, receipt,
source, executor, migration-test, application-document and symlink negatives
exercise rejection. The live test suite also invokes the original unchanged
full-GEN export checker outside historical overlays.

This audit protects the stated completed packages, **not every current verse**.
It approves no new note, source choice or publication. Each new application
still needs its exact candidate, authorized change scope, current inputs and
actual export checks. A later intentional change to protected package inputs
needs explicit supersession; unknown drift must continue to fail.

Do not run the old Genesis `check`/`post_check` entrypoints against the migrated
checkout and interpret their old test-binding failure as a lost historical
receipt. Use the historical runner for that historical contract and the live
audit/current export test for their stated current-state scopes. The original
entrypoints remain byte-for-byte available at the checkpoint.

## Run and verify

From the repository root:

```sh
.venv/bin/python -m tools.textual_restoration.replay_historical_tests genesis
.venv/bin/python -m tools.textual_restoration.replay_historical_tests unflagged
.venv/bin/python -m tools.textual_restoration.replay_historical_tests registry_genesis
.venv/bin/python -m tools.textual_restoration.check_live_note_integrity
.venv/bin/python -m unittest discover -s tests -p test_live_note_integrity.py
```

Archive extraction rejects links, traversal and special files using the existing
safe extractor. The runner accepts no arbitrary commit or test name, launches
Python with `-I` in the private tree, propagates child failure/timeout, rejects
missing/skipped/expected-failure checks, and cleans up. Local Git history and
the installed Python dependencies are required; this is not a vendored runtime
or a network fallback. Expect several minutes for the legacy Genesis suite.

## Actual integration evidence

A read-only simulation exposed the exact frozen 2 Samuel 13:37 candidate through
`Path.read_bytes`/`read_text` in the parent process. The real file stayed at its
baseline; isolated historical children received no such substitution.
All 105 parent tests passed in 200.339 seconds, including the three wrappers
that executed all 37 original historical tests. This batch included the live
registry, current normalization, candidate-scope tests, Numbers/Jeremiah packages
and runner/extractor tests. The later live-audit repair was tested separately.

The real exporter under the simulated reads matched both frozen full-2SA
exports: baseline `01a45f9398382dc8a5b896187a976b7522e826d85a25c7eaf4076c5307835f69`;
candidate `a434d6e5d515c8d1fd5135c07dd6d8e56ae12036d641d70a077895e5fc102289`.
The actual OT digest before/after was
`89d6910840ac91c621fe2c929edd8add3eebb17e2229831a7a12ca253c936ec0`;
the in-memory candidate digest was
`ebc5a784b4f4dc8773c6818297fb2d5e531329a685ab016171c6ee6f2df496c4`.
These are not deployed exports or an applied Samuel transaction.

The independent reviewer required retained live integrity rather than historical
passes alone, then found an omitted application-document pin. Both defects were
fixed and the scoped repair passed review. An initial integration command used
the wrong export hash field after its tests passed; a corrected separate export
check passed. No failed attempt is counted as application success. No new
manuscript research, generated image or canonical edit occurred in this migration.
