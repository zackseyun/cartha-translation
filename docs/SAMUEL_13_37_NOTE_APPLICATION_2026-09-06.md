# Exact Samuel disclosure application contract

This contract permits only the previously reviewed embedded candidate in
`samuel13_37_disclosure_candidate.v1.json`. No source/name selection, main-English
rewrite, whole-verse reapproval, multilingual synchronization or deployment.

The [executor](../tools/samuel_note_transaction.py) never writes canonical YAML.
Its default check verifies candidate/source bindings, exact current bytes, all
OT canonical bytes through one of two fixed corpus digests, 15 derivative pins,
prior completed-note integrity, and an actual complete 695-verse 2SA export.
The former current-test dependency is superseded by the independently reviewed
[historical-test migration](HISTORICAL_TEST_MIGRATION_2026-09-06.md), not by new
global read overlays. Original research and candidate reviews remain frozen.

The entire candidate `note_proposal` block, including its unapproved/unapplied
status, is **historical preparation metadata**, not the live application state.
The separate `samuel13_37_application.v1.json` is authoritative for this scoped
application only after its bindings and current bytes verify. The document does
not declare an application performed merely by describing these steps.

## State transitions

1. Independent transaction review binds exact implementation/test/contract and
   migration dependency bytes, with scoped application approval only.
2. `python -m tools.samuel_note_transaction prepare` requires exact baseline and
   absent ledgers, verifies current inputs/export, then exclusively creates intent.
3. A separate authorized `apply_patch` replaces the canonical file with the exact
   embedded candidate. No other canonical file changes.
4. `python -m tools.samuel_note_transaction confirm` requires the reviewed intent
   and exact candidate; actual corpus/export verification precedes exclusive
   creation of the applied ledger. A failed confirmation cannot claim completion.
5. Run read-only `check` after confirmation and current integration tests. Record
   actual results in the research log. Commit/push is not deployment.

Unknown bytes, unrelated corpus changes, symlink targets, partial ledgers,
unrecorded rollback, stale reviews and changed dependency bindings fail closed.
Existing ledgers cannot be overwritten. Do not silently repair a failed state
by deleting records or relaxing expected digests; investigate and document it.
Baseline without ledgers is a valid unprepared state, not approval to apply.

No new manuscript interpretation is required for this exact disclosure. It
adds the approved patronymic note, moves the unchanged mourning explanation to
“he mourned,” and archives/resets stale review metadata as already reviewed.
The retained source, marker-free English, lexical decisions and original draft
remain unchanged. Source/review metadata are not part of mobile export; their
preservation is checked in YAML rather than inferred from exported output.
