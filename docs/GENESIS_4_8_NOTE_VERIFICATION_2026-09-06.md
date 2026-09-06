# Genesis 4:8 note — actual application and verification

## Result and limits

The exact independently approved note/connected-metadata candidate was applied
locally on 2026-09-06. The Hebrew source, main English (including “said to”),
existing note anchor, historical revisions and original draft metadata remain
unchanged. This corrects the disclosure of published evidence; it does not
decide whether Cain's invitation is earlier than the shorter Hebrew form.
No new manuscript reading, whole-verse reapproval, multilingual synchronization
or deployed-reader/publication approval follows.

The [implementation draft](GENESIS_4_8_NOTE_APPLICATION_2026-09-06.md) is retained
unchanged as a review-bound historical artifact. Its “unapplied” status describes
the implementation-review stage, not the current canonical state. This document
records the subsequent application without rewriting that evidence.

## Exact transaction

The [independent executor review](../sources/textual_restoration/applications/genesis4_8_newtransaction_review.v1.json)
approved only the frozen candidate and the exact five-replacement current-test
migration. The parent then ran `--prepare-intent`, used `apply_patch` separately
for the canonical record and current sample test, checked both resulting hashes,
and ran `--confirm-application`. The executor has no canonical writer.

- Baseline YAML SHA-256: `7552677368239e42f115445ef63b0bfdf9d774677790ffc49214e818837da426`.
- Applied YAML SHA-256: `81e5cd475506a97c8acfd1bcbc353a7c6ffa2b5c27a942a7fff53d8b6865973f`.
- Applied current-test SHA-256: `acc1eea85b5051b5f2779cfc2b4a7ab9d6b49eef4feb4d9546879e71a371e4b0`.
- Executor review SHA-256: `08f344ae021f6d86bde7b774682638e306c0256309e795efe90d8b9ead517af7`.
- [Prepared intent](../sources/textual_restoration/applications/genesis4_8_newtransaction_intent.v1.json), 09:08:26 UTC, SHA-256: `2d2c10e22c253ec7786eeed31cc72346ae6bd5e3c95345f78304c6da039ffcb4`.
- [Applied receipt](../sources/textual_restoration/applications/genesis_4_8_note_application.v1.json), 09:09:37 UTC, SHA-256: `022a86d65d00e5173d2708923eba2752fc77b4d6ef7e748ff16952695e2d2848`.

Intent and completion were exclusive writes. No retry replaced a ledger, and
no frozen checker, candidate, review, policy or earlier application was edited.
This is a controlled local workflow, not an atomic multi-file transaction.

## Current reader result versus historical replay

Completion checked the actual full Genesis export: 50 chapters and 1,533 verses.
Its SHA-256 is `908ddbcef18f990ba77df4622e82d595c027301646fee572b2ceca51789cfca3`,
matching the previously frozen candidate export. The comparison baseline export
remains `602aca5d5a3a06f750a29058d12f52550c3258746e9e5359d33a6bec3081a374`.
Only Genesis 4:8's exported note differs; every other exported value is equal.
The exporter transports English and notes, not source or review metadata.

The actual current OT corpus digest, measured outside all historical overlays,
is `89d6910840ac91c621fe2c929edd8add3eebb17e2229831a7a12ca253c936ec0`.
The old unflagged-sample experiment and its 101 context files are reproduced
under three explicit baseline views: Numbers 22:19, Jeremiah 10:10 and Genesis
4:8. Its historical digest is
`d7ba46056931eb8f23844b388ca2adeef5e6c7588e40ad3b6b5e8c6336fb5381`.
This does not describe an unchanged live corpus. Unknown unrelated drift is
still rejected, and the two earlier applied canonical candidates remain pinned.

The nine frozen Genesis candidate tests continue to test frozen fixtures.
They were neither removed nor redefined as live application tests. The current
sample test alone was migrated to compose the three historical views explicitly.

Seventeen derivative/simplified records remain byte-identical and unreviewed for
this new note. Simplified English already supplies an invitation, and a German
record retains older note wording. These pre-existing discrepancies are separate
work; an unchanged Hebrew source hash does not certify note synchronization.

## Independent post-check and regression

Fresh parent `post_check()` and an independently executed `--post-check` both
passed. The [independent post-verification](../sources/textual_restoration/applications/genesis4_8_newtransaction_postverification.v1.json),
SHA-256 `7194b56ed490a6ec741b993ea9b27770143308b767c09d087affaee30f1f6f85`,
records the actual output; it exactly equals the completion receipt's
`post_application` object. The judge separately checked the exact source/main/
anchor invariance, three archived review values, 22 prior package pins,
17 derivative pins and the five test replacements against the previous Git
baseline. Thirteen post-application candidate/sample tests passed in 19.999 s.

The first full regression run executed 442 tests in 197.019 s: 441 passed and
one failed. `tests.test_ot_witness_registry.test_current_registry` still called
the frozen Pentateuch comparison validator against current canonical bytes,
producing `GEN.4.8.speech: canonical baseline drift`. That is a real integration
gap missed by the 28-test implementation review and 13-test post-check, not a
failed note/source-scope check. The historical comparison is genuinely stale as
a live-corpus snapshot and must not be rewritten to hide that fact.

The original registry validator's direct live-corpus invocation therefore still
reports this baseline mismatch. A passing explicitly historical test will not
mean that the original CLI has become a current-corpus validator or that the
old comparison has been scientifically re-adjudicated.

The [separate current-test repair](../sources/textual_restoration/applications/genesis4_8_registry_test_repair_review.v1.json)
was independently approved, SHA-256
`9a75488ade181b41706c9cf65973afc9b3a80e376125a29f9493bcebaa16e5fc`.
Only `tests/test_ot_witness_registry.py` changed in this repair: 47 insertions,
5 deletions, resulting SHA-256
`0b082a1c3d29fb9fecd4025f8beb76061f39f839252454c2c81591346dfe1891`.
It separates live registry checks from explicit historical comparison replay,
asserts the exact direct live stale-snapshot error, establishes a clean positive
control before deliberately corrupting a baseline hash, and tests unknown
Genesis bytes and unrelated Exodus drift. All 51 targeted tests passed for the
implementer (0.138 s) and independent judge (0.153 s). The judge also reproduced
the original failure and the unchanged validator CLI's exit 1 with that exact
baseline error. No frozen validator, comparison or transaction was changed.

The complete selected research regression rerun passed: 446 tests in 186.482 s,
plus 39 numerical tests in 0.053 s, **485 distinct tests**. The
[regression receipt](../sources/textual_restoration/applications/genesis4_8_integration_regression.v1.json)
records both runs, the actual 43 research modules and six numerical modules,
runtime paths, exact repair bindings and the original failure. Earlier
overlapping 28/13/51 checks are not added again. This is the selected research
suite, not every test in the repository. Deliberate revisions-refresh fixture
failure messages belong to passing negative tests; they are not the actual
registry integration failure recorded above.

Parent final package/transaction checks and 13 bindings across the two image
reviews and registry-test repair also pass. These integrity checks neither
certify manuscript readings nor make the original live registry CLI pass.

## Next gate

The note remains a scoped disclosure correction with `status: draft` and
`cross_check.status: needs_review`; previous review values are archived, not
represented as approval of new bytes. Historical priority still needs further
passage-level evidence and adjudication. Derivative synchronization and the
known deployed website disclosure problem require separate work and validation.
