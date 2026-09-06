# Samuel 13:37 application readiness — held

Date: 2026-09-06. This records implementation findings, not a completed
transaction or new source adjudication. The [approved exact candidate](SAMUEL_13_37_DISCLOSURE_CANDIDATE_2026-09-06.md)
remains **unapplied**. Its [candidate-only review](../sources/textual_restoration/applications/samuel13_37_disclosure_candidate_review.v1.json)
does not authorize an unexamined executor. The current canonical YAML still
has baseline SHA-256 `b6ce63c3ce743f13332997712d04a70258d6844b24428d74556ee58794f87e22`.

## What happened

An implementation subagent inspected the proposal and historical dependencies;
an independent judge separately identified lifecycle and test-consumer hazards.
The implementation agent's connection failed before it saved an executor,
tests or application records. A bounded readiness-report retry also failed.
The parent therefore checked the concrete dependencies and wrote this record.
No successful implementation, virtual-applied integration, application intent,
canonical write, confirmation receipt or post-application export occurred.
This is incomplete work, not evidence that the candidate is unsafe or that
the scientific source question has been settled.

## Verified dependency findings

1. The frozen candidate's `note_proposal.status` literally says
   `research-only-unapproved-unapplied-candidate`. Applying the exact reviewed
   bytes must treat that entire block as **historical preparation metadata**
   and expose actual current state in a separately bound, validated receipt.
   Alternatively, changing that block requires a new exact candidate and review.
   Silently changing the approved candidate is not an acceptable shortcut.
2. `tools/genesis_note_transaction.py` calls `migration_state()` from
   `package()`; this reads `tests/test_unflagged_english_sample.py` and admits
   only two hashes in its frozen migration record. The current test is the
   approved `acc1eea8…71e4b0` state. A new import/overlay edit to that test would
   be a third hash and fail the existing guard. Merely adding Samuel to the
   test's overlay list cannot be assumed to preserve Genesis replay.
3. Current unflagged-sample checks invoke the Genesis historical probe. Current
   registry tests and Genesis transaction tests also enter its guarded view.
   They are real downstream consumers; any future adapter must exercise them
   together and refuse unrelated drift, not just pass a new Samuel unit test.
4. The historical corpus selector and its original receipts must remain
   historical. A live corpus digest and actual complete Samuel export must be
   computed outside historical overlays. Prior export results are useful
   candidate evidence, not a post-application check of an unperformed change.

These are read-only findings from the actual files. An initial query looked
for `migration_state` in the dependency manifest and returned null; the actual
state pairs are in `genesis4_8_newtransaction_test_migration.v1.json`, confirmed
against the executor's `MIGRATION` constant. The null result was not accepted
as evidence that no dependency existed.

## Required implementation and review

- Freeze an exact transaction contract: candidate, source/English/notes scope,
  allowed state transitions, review, intent, confirmation, derivative pins and
  rollback/tamper rejection. Preserve the historical proposal separately from
  authoritative applied state.
- Provide an explicit immutable historical corpus interface or a narrowly
  bounded compatible adapter. Do not grow arbitrary global read overlays or
  relax old hash guards just to absorb the next edit. Architecture and any
  current-consumer migration require their own exact review.
- Test virtual baseline/applied states, partial ledgers, stale reviews, unknown
  canonical bytes, unrelated corpus drift, symlinks, rollback and test-consumer
  drift. Run existing dependent checks as well as new transaction tests.
- Recheck all 695 Samuel verses in the actual export; verify exact note order,
  anchors, unchanged marker-free English/source/draft/lexical history, and the
  unsynchronized status of the 15 derivative contexts.
- Only after independent transaction approval, apply the exact YAML with
  `apply_patch`, confirm the bound transaction, verify live export/current
  corpus outside overlays, and record the result. Commit/push is separate from
  deploying a reader or translating derivative languages.

No claim is made that this readiness checklist passes those requirements.
Source/name priority remains unresolved. The substantive reader improvement
remains the reviewed disclosure and mourning-note anchor correction, not a
replacement of Ammihur with a supposedly recovered original.

## Exact inspected dependency pins

| Repository path | SHA-256 |
|---|---|
| `tools/genesis_note_transaction.py` | `a0555416eaafa6e7d81b6400ffc974f785b5254c3830c89f81e876208e84b2fb` |
| `tests/test_unflagged_english_sample.py` | `acc1eea85b5051b5f2779cfc2b4a7ab9d6b49eef4feb4d9546879e71a371e4b0` |
| `tests/test_ot_witness_registry.py` | `0b082a1c3d29fb9fecd4025f8beb76061f39f839252454c2c81591346dfe1891` |
| `tests/test_genesis_note_transaction.py` | `071aa364d678521bc2cb477cbd23380ab6c33d76d82edb18caa4e7c2aa5a525d` |
| `sources/textual_restoration/applications/genesis4_8_newtransaction_test_migration.v1.json` | `592e6aa42ae3c84d87f69087314b099cc8284ccbbe7d1261557035b5cfb51fe8` |

Fresh baseline tests and final review results belong in the chronological
[research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md); a baseline pass must not
be represented as virtual-applied or post-application verification.
