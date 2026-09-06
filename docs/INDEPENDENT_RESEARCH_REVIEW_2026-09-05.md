# Independent research review cycle — 2026-09-05

The user authorized parallel agents and an independent judge. Three actual
subtasks ran: `catalogue_reconciliation`, `english_fidelity_sample` and
`independent_judge`. The judge received a fresh-context task, not the parent's
conversation history. It then inspected named records and sources. This is
separate-agent adversarial review, **not** a different-model-family experiment,
a blind manuscript transcription, human peer review or validation of all POB.

## Scope and actual verdicts

| Gate | Final bounded verdict | Evidence and limits |
|---|---|---|
| Method's inference boundaries | Pass | Separates observations, published text, source choice and English; explicitly leaves completeness/calibration open |
| Isaiah preservation and Greek control | Pass for checked records | Judge independently consulted 4Q164/4Q69a published controls and hash-pinned QDR/Greek inputs; not every witness |
| Swete report | Inconclusive → pass | Judge independently verified PDF hash and visually inspected all nine named pages, including printed p. 202; ancient hands and full modern apparatus still unverified |
| Catalogue parser | Fail → repaired → pass | Three concrete malformed-input defects reproduced, repaired by implementation agent and re-tested by judge |
| Catalogue accounting | Pass | Independent enumeration matched all 1,173 labels/URLs; actual pinned-input receipt reproduced; aliases remain candidates |
| Unflagged English sample | Pass for selection/reporting contract | Four tests, protocol hashes and deterministic draw checked; no redraw evidence or corpus-wide gain claim |
| Complete restoration / superior corpus | Inconclusive | No complete census, held-out restoration accuracy or corpus-wide English benefit established |
| Production publication readiness | Fail | Known source schema, reviewed application transaction and website-disclosure gaps remain open |

The parser initially could silently omit a changed row container, accept blank
query parameters, or accept an unclosed superscript. Its observed nesting and
query validation are now strict; three regression tests cover the failures.
The judge reran the concrete failures, all thirteen parser tests, and actual
input reproduction. Counts and saved source evidence did not change.
See the [catalogue report](QUMRAN_DIGITAL_CATALOGUE_INDEX_RECONCILIATION_2026-09-05.md).

For the [English sample](UNFLAGGED_ENGLISH_SAMPLE_2026-09-05.md), the judge
accepted the narrow selection/reporting claims. Static files alone do not
independently prove temporal predeclaration. Samuel 20:6 remains unresolved
as a whole verse. The judge supported the proposed note anchors and warned
that applying its uncertainty note also requires synchronizing the current
lexical entry's spelling and explanation. Historical review prose must remain
history. No proposed edit has been applied and no sample has been redrawn.

The judge independently checked the Swete source scan using the PDF skill:
SHA256 `5f0bfffabf0e588fd32e15bdb24b027872616da219e7f02da3dbdc115cf97d85`,
one-based pages 7–10, 12–14, 24 and 226. It confirmed edition identity, the
acute/grave distinction, bounded quantifier report and apparatus cautions.
CAL controls remain outside that independent attestation check.

## How the review loop continues

Freeze each review's scope and inputs. Record fail/inconclusive/pass separately.
Send concrete failures to the implementer, preserve the failure description,
rerun both the failing example and relevant regressions, then ask the judge
to check the changed output. If evidence remains unavailable or genuinely
undecidable, leave that gate open; do not keep changing the criterion until it
passes. A research-only pass never overrides failed publication gates.

Historical YAML agreement flags are not hash-bound approval of a newly edited
record. The judge highlighted `tools/find_uncovered_verses.py`'s use of nonempty
cross-check metadata as coverage; that cannot become current scientific
certification. Review bindings remain part of the application backlog.

The parent separately investigated two discrepancy leads in the
[identity-hold record](../sources/textual_restoration/discovery/catalogue_identity_holds.v1.json).
The catalogue's raw counts stay intact. These dispositions are not automatically
enforced by an ingestion system and were not covered by the initial judge pass.
The judge subsequently reviewed the integrated documentation and both holds,
independently opening the XAmos transcription, Tov publication record,
Klawans's argument and ArugLev publication record. Final integration received
a bounded pass: no new concrete failure found, with physical identity,
authenticity and full-edition questions still open. The three sampled canonical
files remained unchanged. Publication readiness remains failed.

Final parent regression run: 251 repository tests plus nine numerical tests
passed (260 total); the actual catalogue receipt reproduced, registry validation
passed at 27 entries / 20 physical coverage records / 13 formal cases / one
unpromoted selection, and Git whitespace checks passed. These automated checks
protect consistency; they do not certify historical readings or translation
superiority.

## Subsequent identity and measurement batch

The same three agents continued with bounded tasks; this is another
separate-agent review, not a new model-family experiment.

- [Catalogue identity follow-up](QUMRAN_CATALOGUE_IDENTITY_FOLLOWUP_2026-09-05.md):
  bounded pass. Judge ran all eight tests without skips, inspected the pinned
  QDR records and source HTML, and checked selected live transcription and
  publisher records. Physical identity, inaccessible reassignment arguments
  and manuscript images remain unverified. No new concrete failure required
  an implementation repair in this batch.
- [Wider En-Gedi check](EN_GEDI_WIDER_RENDERER_CHECK_2026-09-05.md): bounded pass
  for frozen-design execution, measurement provenance and reporting. The judge
  inspected the protocol before results, ran six tests and full reproduction,
  and independently implemented scalar sampling against the six actual CT
  slices: all 88 evaluable candidate predictions reproduced. Full spatial
  coverage remains incomplete/inconclusive, including zero evaluated distant
  rows. Neither historical-renderer universality nor letter accuracy passed.

- [Greek source follow-up](JUDEAN_GREEK_SOURCE_FOLLOWUP_2026-09-05.md): bounded
  pass. Using its own browser, the judge independently read the five IAA
  records and exact partial image lists, Ra 943, Kraft's relevant survey
  sections, IAA's Greek summary and 4Q127 classifications. Five tests and
  registry validation passed. Full editions, ancient pixels and exhaustive
  catalogue coverage remain unverified. The judge also passed final integrated
  scope reporting; no new actionable failure was found.

Parent observed 264 repository tests and 15 numerical tests pass (279 total),
and reproduced both new and previous numerical receipts from actual inputs.
The registry is now 31 mixed entries, with the same 20 passage records,
13 formal cases and one unpromoted selection. No canonical file changed in
this batch. Existing failed publication gates remain failed.

## Subsequent distant-row, 4Q119 and note-application batch

The same separate-agent judge checked three bounded deliverables:

- [4Q119 at Lev 26:12](4Q119_LEVITICUS_26_12_REVIEW_2026-09-05.md): independently
  rendered and read all seven cited primary-publication PDF pages and ran
  seven focused tests without skips. Bounded evidence/preservation PASS after
  an ambiguous chronology phrase was clarified. The noun ending is supplied;
  no forced Hebrew change, earliest-Greek priority or ancient-pixel pass follows.
- [En-Gedi distant rows](EN_GEDI_DISTANT_ROWS_CHECK_2026-09-05.md): reviewed the
  frozen geometry/acquisition protocol before new results; reproduced the
  actual old/new receipts and five focused tests. A separate scalar sampler
  against 42 verified CT slices independently reproduced all 164 evaluable
  predictions, maximizing offsets, counts and residuals. Execution and scope
  reporting PASS. The primary model's 19 observed values match exactly; seven
  other candidates FAIL observed exact agreement. All full spatial scopes
  remain INCOMPLETE; reading accuracy and multiple segments are untested.
- [Numbers note application](NUMBERS_22_19_NOTE_APPLICATION_2026-09-05.md):
  initial P2 FAIL. The historical overlay checked only two of six frozen
  protocol inputs; a mocked controlling-method change still returned success.
  The implementer repaired complete-input/receipt binding, preserved v1 and
  created v2. The judge's original reproduction then rejected drift; thirteen
  focused tests passed. Only then did the judge approve the exact candidate,
  executor and v2 preflight for this local note repair. The parent recorded
  that judgment verbatim and independently checked its three hashes.

After application, the judge independently verified the exact canonical
candidate, intent, final receipt and actual complete Numbers export. Fresh
preflight exactly reproduced the saved post-application checks; all six frozen
protocol files, 101 contexts and the complete historical sample reproduced.
Seventeen application/sample tests passed in the judge's post-application run.
The current corpus is explicitly different from the historical corpus only
at the approved Numbers record. Source and marker-stripped English remain
unchanged. Post-application bounded PASS does not approve the whole verse,
authenticate old reviews, demonstrate semantic gain or authorize publication.

Parent post-application regression: 284 repository tests passed; the numerical
suites separately passed 20 tests (304 distinct tests total). Registry validation
remains 31 mixed entries / 20 passage records / 13 formal cases / one
unpromoted selection. No additional ancient-text coverage is implied by these
counts. The only canonical edit in this batch is the reviewed Numbers note
and its archived/current review-state bookkeeping. No deployment occurred.

The final integrated documents received a bounded PASS after the judge flagged
and rechecked a missing completed-outcome section in the Numbers dossier.
No concrete defect remains from this batch; publication readiness still fails.

## Subsequent primary-source and region-grounding batch

- [4Q24 follow-up](4Q24_LEVITICUS_2_PRIMARY_FOLLOWUP_2026-09-05.md): bounded
  PASS for faithfully reporting the actually consulted reassessment, dated
  digital readings and missing primary/pixel gates. Judge independently read
  seven decisive pages, parsed source HTML, checked IAA metadata and ran seven
  focused tests. The target-word image/edition gate did not pass.
- [Samuel20:6 follow-up](SAMUEL_20_6_SOURCE_ENGLISH_FOLLOWUP_2026-09-05.md):
  bounded PASS with a separate exact-hash judgment. Ten tests and two PDF
  hash checks passed; decisive BDB/GKC/Driver/Greek/CAL claims were independently
  checked. GKC's later pages436–437 were outside the judge's visual inspection.
  Source priority and best whole-verse rendering remain INCONCLUSIVE; no
  canonical application is authorized by this review.
- [En-Gedi region grounding](EN_GEDI_REGION_GROUNDING_2026-09-05.md): the fixed
  scientific registration gate FAILED. The parent raised and the judge
  independently confirmed a P2 pixel-center coordinate defect in v1, using
  an actual OpenCV ramp and the primary implementation. The parent preserved
  v1 and produced a separate v2 coordinate-conjugation repair, not a new fit
  or a relaxed acceptance rule. Both receipts reproduced from actual images
  in the parent's checks, and all30 numerical tests passed. The scientific
  gate remains failed; every projected locus is unaccepted.

The judge also identified repeated geometric locations across descriptor
partitions:372 descriptor pairs,327 unique geometric pairs and32 validation
rows sharing a fitting location. These counts are now disclosed and were
independently reproduced by the parent; no independent holdout claim follows.
Parent full relevant repository regression passed301 tests, plus30 numerical
tests, for331 distinct tests. Existing publication gates remain failed or
unapproved; the user's later Git-push authorization is a repository workflow
instruction, not scholarly certification or a request to deploy the Bible.
