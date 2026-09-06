# Numbers 22:19: bounded note application package

2026-09-05. Applied locally and independently verified. This package concerns only the existing footnote's anchor and
divine-name wording, plus the review-state bookkeeping necessary to prevent
old agreement flags from certifying a new file. It changes no Hebrew source,
main English prose, lexical decision or theological decision. Samuel remains
outside this package.

## Exact candidate

The sole `[a]` moves from “tonight” to the end of the divine-speech clause,
immediately after “me” and before the period. The note changes from
“Or ‘what else the LORD will speak to me.’” to
“Or ‘what else Yahweh will speak to me.’” Its existing “will speak” wording
is retained. The note is about the speech clause, not the overnight stay;
the name follows the current POB divine-name policy.

The [byte-exact baseline](../sources/textual_restoration/applications/numbers_22_19_note_baseline.v1.yaml)
has SHA256
`74348f325b3cfb563c42c4d5075985ce833193d906dfdfe51a0bcc5eb88ff246`.
The [complete candidate YAML](../sources/textual_restoration/applications/numbers_22_19_note_candidate.v1.yaml)
has SHA256
`eee7a776befc2a210c8f5ca9e2a35cda3c93ae1ed7a4d90436dfe8ce5b608a77`.
The [plan](../sources/textual_restoration/applications/numbers_22_19_note_plan.v1.json)
enumerates every allowed content/metadata difference and the exact judgment
fields required before local application.

Old `status`, `revision_pass` and the complete `cross_check` object are
preserved under `review_history`. Their archive links to the baseline file,
but does not pretend that this is the original input hash of the old model
reviews. Historical input binding remains unverified. Current `status` is
`draft`; current `cross_check` contains only `needs_review`. The original
`ai_draft` remains unchanged and is explicitly historical. The new metadata
disclaims whole-verse reapproval and publication approval. These are scoped
editorial records, not a replacement for production review semantics.

## Real preflight and independent challenge

The unchanged verse schema reports one existing baseline error:
`status: revised` is outside its draft-only enum. The candidate passes that
schema without broadening it: the source is still WLC, the note reason is
still `lexical_alternative`, and current lifecycle state is honestly `draft`.
Schema validity does not confer editorial or publication approval.

The real Numbers exporter was called with separately pinned single-record
baseline and candidate overlays, then against actual current canonical files.
It produced all 36 chapters and 1,289 verse records in this repository's
current export. Only the targeted note/anchor differs. The candidate's exact
marker and note body survive; research history and source objects are not
part of that reader payload. No source change requires additional source
disclosure in this package. Website/CDN behavior and deployment were not
exercised, and existing production-publication failures remain failures.

The [v1 preflight](../sources/textual_restoration/applications/numbers_22_19_note_preflight.v1.json)
is preserved. The independent judge found that its historical reconstruction
guard checked only two of the six frozen protocol files. A simulated change
to the controlling method still returned success. That concrete failure
withheld application approval even though the actual current files matched.

The repair pins the original selection/review receipt bytes, checks all six
protocol inputs and compares the entire reconstructed receipt, including its
complete key set. The [v2 preflight](../sources/textual_restoration/applications/numbers_22_19_note_preflight.v2.json)
reproduces the complete frozen selection and all 101 context bindings.
The judge's original method-drift reproduction now fails closed. Thirteen
focused tests passed, including injected drift in every frozen protocol file.
The exact candidate bytes did not change during this guard repair.

## Historical sample preservation

The unflagged selector, original selection/review receipts and predeclaration
remain byte-exact. A separate read-only overlay supplies only the Numbers
baseline to the original selector and original context checks. The current
Numbers file must be either that exact baseline or the exact candidate with
an approval-bound transaction record. Any third state is rejected. Every
other corpus file and all six original protocol inputs still have to match.

The existing four sample tests now use that guarded historical route; they
do not rewrite expected sample results or accept arbitrary drift. The new
receipt separately reports the current corpus digest and its single allowed
difference from the historical corpus. Passing the historical reconstruction
must never be reported as current-corpus byte identity after application.

## Transaction boundaries and reproduction

The [executor](../tools/textual_restoration/apply_numbers_22_19_note.py) is
restricted to this fixed verse and candidate. Application requires a recorded
independent judgment bound to the complete candidate YAML hash, followed by
schema/export/historical checks and an exclusive advisory package lock.
It preserves an intent before staging the approved bytes on the same
filesystem, fsyncs, rechecks the current baseline immediately before an atomic
replacement and then verifies actual canonical export and historical context.
A final receipt records the exact resulting file and validation results.

The atomic operation covers one file's visibility. The intent, target and
final receipt are not a multi-file atomic transaction. The lock coordinates
cooperating writers, and the immediate expected-byte check does not claim
a general compare-and-swap against noncooperating editors. Unknown current
content is never overwritten. Interrupted candidate state can resume only
with matching prepared provenance; an existing different final receipt is
not replaced. A post-write validation failure is a failed/incomplete local
transaction, not publication success or permission to overwrite later edits.

```sh
.venv/bin/python tools/textual_restoration/apply_numbers_22_19_note.py
.venv/bin/python -m unittest discover -s tests -p 'test_numbers_22_19_note_application.py'
.venv/bin/python -m unittest discover -s tests -p 'test_unflagged_english_sample.py'
```

The first command performs read-only preflight. The separately gated `--apply`
operation is not a publication or deployment command. Candidate-content
acceptance alone did not authorize execution; the exact executor and repaired
preflight also received the bounded approval recorded below.

## Actual application and independent postcheck

The [independent judgment](../sources/textual_restoration/applications/numbers_22_19_note_judgment.v1.json)
approved these exact candidate bytes, executor and v2 preflight for the scoped
local transaction. The parent recorded the judge's supplied JSON without
claiming a human review or different-model-family validation. The approved
transaction then completed with status `applied-verified`, preserving its
[prepared intent](../sources/textual_restoration/applications/numbers_22_19_note_intent.v1.json)
and [final application receipt](../sources/textual_restoration/applications/numbers_22_19_note_application.v1.json).

The canonical Numbers 22:19 file now equals the approved candidate SHA256
`eee7a776befc2a210c8f5ca9e2a35cda3c93ae1ed7a4d90436dfe8ce5b608a77`.
The actual current full Numbers export equals the candidate export SHA256
`8d2d0a5b60567e12baadaa1514d31e80746d316a9ca99a4e36c59af685f7f3c0`:
all 36 chapters and 1,289 verse records were checked, all other reader content
is unchanged, and the single final anchor and corrected note survive export.
The Hebrew/source object and main prose minus its marker remain unchanged.

The frozen selection receipt, all six protocol inputs and all 101 context
bindings reproduce through the guarded baseline overlay. Current corpus
identity is deliberately distinct: current SHA256
`f717bc7f9904942cbb2c9d4748d176bef195ad2c108a713a4ae269e00bee082d`
versus historical SHA256
`d7ba46056931eb8f23844b388ca2adeef5e6c7588e40ad3b6b5e8c6336fb5381`.
The sole permitted difference is `translation/ot/numbers/022/019.yaml`.

After application, 13 focused application tests and all four historical
sample tests passed. The independent judge also passed those 17 tests and
independently verified all application bindings, exact canonical bytes,
the full Numbers export, frozen reconstruction and distinct current digest;
a freshly recomputed postflight equaled the saved `post_application` object.
This is a bounded local-application PASS, not whole-verse approval,
publication approval or authentication of historical review inputs.
`publication_ready` remains false.

Final receipt SHA256:
`a109403a695ad217afdaa791a43ab215d3a10e3848715954977231c1349286cf`.
Prepared intent SHA256:
`0436d5383fbb620dd857615a793f13ea72116e2d0a580103aa446fff5b058c0e`.
Recorded judgment SHA256:
`aedeaf0c9716bebce74af745bcebde63540b3fd6e20e9d8bccf4acc2103666b7`.
