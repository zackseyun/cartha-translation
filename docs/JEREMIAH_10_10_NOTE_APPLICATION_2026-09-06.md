# Jeremiah 10:10 — bounded note application

Application checkpoint: 2026-09-06 (UTC ledger timestamps). This is a
reader-disclosure and connected metadata correction, not selection of an
earliest source form or approval to publish the whole verse.

## Evidence and decision

The [source dossier](JEREMIAH_10_LITERARY_FORM_COMPARISON_2026-09-05.md)
distinguishes partial Hebrew survival in 4Q70, a published spatial reconstruction
of 4Q71, Codex Vaticanus's shorter Greek sequence and a form of verse 10 in
Codex Marchalianus's margin as reported in Swete's apparatus. The shorter form
cannot simply be made by deleting/reordering the present POB English: wording
also differs. Retaining the longer Hebrew form is provisional; this note does
not settle which literary form is earlier.

The [independent source judgment](../sources/textual_restoration/applications/jeremiah_10_10_note_judgment.v2.json)
records actual inspected pages, input hashes, objections, limitations and a
bounded APPROVE for the exact v2 candidate. This is a separate agent's review,
not a blind study or a second model-family transcription. Full modern apparatus
and the further spatial reconstruction cited in the dossier remain unconsulted.

The original v1 proposal only appended disclosure. Review of its surrounding
record exposed already-misplaced note anchors and divine-name metadata that
did not describe the actual English. The parent explicitly expanded the same
verse's candidate to repair these connected defects. Both candidates, plans
and preflights remain frozen; v1 has not been relabeled as the approved package.

## Exact change boundary

- Add note d explaining the shorter/longer evidence and unresolved priority.
- Place a after “But Yahweh,” b after “true God,” c after “everlasting King.”
- Change note a's alternative from “And the LORD” to “And Yahweh” and synchronize
  the opening lexical/conjunction metadata with the existing divine-name policy.
- Archive prior status, revision-pass and cross-check values, preserving their
  baseline hash and stating that their historical input binding is unverified.
  Current status is draft/needs_review, not inherited high agreement.
- Keep the source YAML block and marker-free English unchanged. Existing
  lexicon references remain historical; no fresh HALOT consultation is claimed.

Baseline SHA-256: `cb5391f363a7fd7ea7b5433f3825e2ef59c7624f3f9263f9b9d1cc87fb0c3661`.
Approved/current candidate SHA-256: `ae7d4a731f43fa6a29eca05e0d4c2fcd35c17a06d2dde0837fa7da957eaa9d4a`.

## Transaction and replay

The [scoped executor](../tools/textual_restoration/jeremiah_note_transaction.py)
does not write the canonical verse. Its separate
[transaction review](../sources/textual_restoration/applications/jeremiah_10_10_note_transaction_review.v2.json)
binds the exact executor, package and source judgment. A write-once
[intent](../sources/textual_restoration/applications/jeremiah_10_10_note_intent.v2.json)
records the real baseline and preflight; the parent then applies the exact
reviewed difference with `apply_patch`. The
[application receipt](../sources/textual_restoration/applications/jeremiah_10_10_note_application.v2.json)
is written only after checking actual candidate bytes and actual full-book export.

The judge caught a real lifecycle gap before application: an exact baseline
could otherwise be accepted after a completion record existed. The repaired
tool rejects that unrecorded rollback and validates a pending intent even at
baseline. Tests also reject unknown bytes, stale approval, changed evidence,
wrong ledger states, changed intent binding and overwrite attempts.

Frozen earlier checks still mean what they originally meant. They do not all
accept the changed canonical file when invoked directly. The guarded replay
substitutes only the exact historical Jeremiah and Numbers note baselines,
verifies their approved transaction provenance and reproduces the original
selection plus 101 context-file bindings. It reports the real current OT corpus
digest separately. The current sample test uses this explicit two-target replay;
the original selector, experiment, evidence receipts and six frozen method
inputs remain unchanged.

Recheck with `.venv/bin/python tools/textual_restoration/jeremiah_note_transaction.py`.
Do not rerun the write-once `--prepare` or `--complete` operations after success.
Tests are [transaction safeguards](../tests/test_jeremiah_note_transaction.py)
and [historical sample integrity](../tests/test_unflagged_english_sample.py).

Actual export checks cover all 52 chapters and 1,364 verses of Jeremiah, compare
the new verse with the approved draft export and require every other exported
item to remain unchanged. This checks local transport only. The separate
[reader trace](READER_DISCLOSURE_TRACE_2026-09-05.md) still records website
note-stripping; no deployed-reader repair or publication approval follows here.

The separate [post-application verification](../sources/textual_restoration/applications/jeremiah_10_10_note_post_application_verification.v2.json)
passes the actual canonical/ledger/export/history checks and the bounded
reporting review, with no mandatory correction. It independently compares
unchanged source bytes and marker-free English and repeats 21 transaction tests.
