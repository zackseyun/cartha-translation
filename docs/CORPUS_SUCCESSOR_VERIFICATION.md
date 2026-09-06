# Current corpus successors and immutable application history

The read-only `tools/textual_restoration/verify_corpus_successor.py` separates
historical application evidence from verification of explicitly reviewed later
note/metadata edits. This supersedes the current-check role of the old Samuel
entrypoint, not its bytes or receipts. Its original eleven tests now run against
the unchanged Git checkpoint `9af0a131c7f6368217cf1c33a3d7f4bf3c231de1`.
The archive uses the repository's Git object store for read-only historical
queries; no current source file or candidate is overlaid into that archive.

## Scope and authority

A plan names exact baseline/candidate hashes, source input pins and complete
affected-book export expectations. A separate independent review binds that
plan and this implementation, tests, migrated Samuel wrapper and contract.
Supply its trusted SHA explicitly; computing a SHA from an arbitrary review is
not approval. These bindings preserve an actual review, not authenticate a
reviewer's identity or establish scholarly truth. No self-approval is generated.
This mechanism permits only retained-source, retained-main-English disclosure
and metadata corrections. Source selection and main-English changes require a
separately reviewed extension; this tool cannot approve them.

The current verifier checks every canonical OT YAML path and Git blob against
the immutable checkpoint plus all exact changes in the reviewed plan. Plans
describe complete successor states from that checkpoint, not unchecked partial
overlays. Added/deleted files, unexpected-depth YAML, unknown edits, symlinks,
duplicate targets and partial multi-file applications fail. The four previously
completed note targets are protected from successor edits. Extending the scope
to revise one of those targets needs explicit supersession, not a new allowlist.

Frozen Samuel package, review, ledgers, source/implementation and derivative
bindings are checked independently of whole-corpus identity. The existing
three-note live integrity audit remains unchanged. Only the exact reviewed
Samuel test-wrapper replacement supersedes a frozen test consumer. Actual
full Samuel and affected-book exports run against real current files, without
an overlay. Other derivative contexts remain unsynchronized; publication is
not implied. Candidate schema acceptance does not certify the complete verse.

## Operating sequence

1. Obtain editorial review of an exact candidate and review of its application
   plan, implementation bindings and checks. Keep the source comparison record.
2. Run the verifier with the plan, review and externally trusted review SHA.
   Preserve its baseline result before any canonical edit.
3. Apply only the reviewed candidate using a separate authorized file edit.
4. Run the same verifier again. Preserve the actual candidate-state result with
   the baseline result, plan/review hashes and scoped application record. A
   failure cannot be represented as an applied-and-verified change.
5. Run the historical Samuel wrapper and current successor/integrity tests.
   Commit/push is separate from publication or multilingual synchronization.

The verifier never writes canonical files, approvals, intent or application
ledgers. A returned baseline/candidate state is an observation, not proof that
an application transaction or publication occurred. The caller must preserve
the separate before/after record. Reviews must cover the entire plan, including
prior successors retained in a later plan. Do not blindly regenerate expected
hashes to make a failing check pass.

For later verification of an applied change, additionally supply the application
record and its trusted SHA using `--application` and `--application-sha256`.
That mode requires the actual candidate state to match the recorded after-state;
rollback, edited records or stale bindings fail. Omitting the application record
checks only the observed plan state, not the completed application lifecycle.

The old `tools/samuel_note_transaction.py check` is now a historical contract:
it intentionally rejects the migrated current test consumer or successor
corpus. Use its checkpoint replay for that contract and the successor verifier
for the current state. Its refusal is not erased or reported as a current pass.
