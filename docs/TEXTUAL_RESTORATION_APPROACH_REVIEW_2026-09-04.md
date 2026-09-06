# Review of the POB textual-restoration approach

Reviewed: 2026-09-04. This reviews the restoration program, its method documents,
source records, seven source comparisons, and validation machinery. It is not a
fresh scholarly adjudication of every case or a linguistic audit of all 31,221
canonical verse files. The review is a continuation by Codex with access to the
earlier work; it must not be described as an independent blind review.

## Assessment

Keep the project and most of its infrastructure. The strongest achievement is
an increasingly inspectable connection between a manuscript claim and a POB
translation decision. We have found real disclosure and metadata problems,
distinguished manuscript survival from editorial reconstruction, and created
reproducible comparison records. Those are useful results even when the English
main text does not change.

The central weakness is calibration. We have more statements about what the
system will accept than measurements showing when that acceptance is reliable.
The early charter also allowed agreement between two models on missing letters
to imply permission to use them in the main text. That conflated a working
transcription decision with historical text selection. The revised method keeps
the agreed two-family workflow, while making source selection and publication
separate decisions.

This work has not yet demonstrated a newly deciphered biblical reading or an
improvement rate over established editions. The current findings largely
reassess published variants. A newer model can help find omissions and test
arguments; its identity supplies no additional manuscript evidence.

## What the work actually establishes

### Current reassessment — 2026-09-05

The table below preserves the September 4 snapshot. The current ledger is
31 mixed registry entries, 20 physical coverage records, 13 formal OT comparison
cases and one unpromoted source/English selection. The NT has an edition-level
screen and an initial Mark 1:41 dossier, not a completed manuscript census.
See the [research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md) for dated evidence
and corrections. This reassessment is a continuation, not an independent review.

**Keep:** evidence-linked passage dossiers, original-language comparison,
observed/supplied distinctions, explicit contrary evidence, reproducible inputs,
and separate source-selection and English decisions. Correcting an overstated
attestation is a substantive improvement even when the preferred text survives.

**Improve the delivery discipline:** run broad catalogue discovery, consequential
passage adjudication, source-stable English review and measured imaging as
distinct workstreams. Catalogue growth must not be reported as translation
progress; imaging calibration need not hold up a published-text comparison.
Finish one end-to-end reviewed case while expanding the coverage ledger. The
Deuteronomy 32:8 draft/preflight is an engineering demonstration, not that
completed case. Its next review must incorporate the later Fouad supplement.

**Define “more optimal” before comparing candidates:** prefer demonstrable
source fidelity under POB's stated translation policy, with explicit tradeoffs
in ambiguity, literary effect and readability. Do not optimize for a model's
preference, novelty, agreement with familiar translations, or theological fit.
For every proposal specify the defect, source evidence, candidate improvement,
strongest objection and any lost nuance. “No change” and “unresolved” are
successful research outcomes. Corpus-wide superiority requires a predeclared,
held-out evaluation including unflagged passages; selected success stories
cannot establish it. See the [evaluation contract](TEXTUAL_ADJUDICATION_METHOD.md#translation-evaluation-contract).

**Use the right sources without claiming all have been used:** the
[OT/NT evidence map](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md#old-testament-required-evidence-map)
covers the necessary source classes. OT work needs Masoretic codices and
apparatuses, Judean Desert witnesses, Samaritan evidence for the Torah, Greek
editions/manuscripts/revisions, and discriminating versions and quotations.
NT work needs manuscript-and-hand records for papyri, majuscules, minuscules,
lectionaries and commentary witnesses, with versions and patristic evidence.
These are required coverage categories, not a claim of completed acquisition.
The IAA archive supports searches across sites, languages and content; the
NTVMR provides manuscript catalogues and research tools. The SBLGNT apparatus
compares editions, so it cannot substitute for the NT witness ledger.
[IAA](https://www.deadseascrolls.org.il/explore-the-archive),
[NTVMR](https://ntvmr.uni-muenster.de/),
[SBLGNT apparatus](https://sblgnt.com/about/introduction/apparatus/)
(pages checked 2026-09-05; no fresh catalogue census performed).

**Close reader-facing verification:** source/English/notes must agree and the
actual reader must retain the disclosure. Local exporter tests now exist;
the [reader trace](READER_DISCLOSURE_TRACE_2026-09-05.md) still records a
separate website note-stripping problem. No deployed fix or approved canonical
source change is established by a passing local test.

The project is worth continuing. Its present achievement is a more auditable
and self-correcting research process, not a demonstrated recovery of originals
or proof that POB is globally the best translation.

### Earlier review snapshot

| Completed work | What it establishes | What remains open |
|---|---|---|
| 66-book inventory; 590 local note leads; WLC annotations; 6,934 SBLGNT apparatus entries | A reproducible screening queue | Exhaustive manuscript coverage or the accuracy of unflagged verses |
| Seven passage comparisons and 14 coverage records | Specific published readings and their survival boundaries | Comprehensive collation of all witnesses in those passages |
| 4Q33 and 4Q45 exclusions | Verse coverage can fail to preserve the disputed phrase | Which alternative is historically prior |
| Deuteronomy 32:8 and 1 Samuel 17:4 | Better documented support for existing working preferences | Final source selection, image checks, and publication review |
| Verse notes, markers, and metadata repairs | Readers and editors can see previously obscured alternatives | A measured improvement in translation accuracy across the corpus |
| Source/English selection pilot and validators | Structural checks against unsupported linkage and stale inputs | A complete application, review, and export-receipt system |

Counts are snapshots of the local inventory, not quality scores. The SBLGNT
publisher explicitly describes its apparatus as a comparison of editions;
manuscript-level work must be added separately.
[Publisher apparatus description](https://sblgnt.com/about/introduction/apparatus/).

## Changes to the approach

Current status, September 5: use the [central research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md)
for the latest snapshot (31 registry entries, 20 coverage records, 13 cases,
one unpromoted selection). Counts and acquisition statements in the dated
paragraphs below describe their earlier passes. In particular, En-Gedi measured
assets have since been acquired privately and numerical probes executed;
the earlier “unacquired” statement below is superseded, not a current blocker.

The later [identity follow-up](QUMRAN_CATALOGUE_IDENTITY_FOLLOWUP_2026-09-05.md)
demonstrates that even exact labels can join different content across projects.
Treat a catalogue match as a lead until content, physical locators and edition
history are reconciled. The [Greek follow-up](JUDEAN_GREEK_SOURCE_FOLLOWUP_2026-09-05.md)
also corrects a forced same-object instruction: uncertain physical grouping
must stay uncertain, without creating automatic independent votes.

The [wider numerical check](EN_GEDI_WIDER_RENDERER_CHECK_2026-09-05.md) illustrates
another necessary discipline: report requested, invalid, unavailable and
evaluated samples separately. Nine new exact local predictions do not make
the 128 unavailable valid targets pass. Independent review reproduced the
evaluated numbers, not the absent observations or a recovered-letter benchmark.
These additions refine implementation of the existing method; historical
protocol snapshots remain unchanged.
The recovery benchmark and full coordinate validation remain incomplete.

The subsequent [distant-row experiment](EN_GEDI_DISTANT_ROWS_CHECK_2026-09-05.md)
acquired 36 specifically selected CT slices under frozen geometry and byte
limits, then re-evaluated all 288 original targets. The same primary candidate
now matches 19 evaluated values, including ten newly available observations;
118 valid targets remain unavailable. This is evidence for one numerical
pipeline, not readable-letter recovery. Keep both observed model failures and
missing-data status visible; an incomplete scope must not conceal nonzero errors.

The [4Q119 comparison](4Q119_LEVITICUS_26_12_REVIEW_2026-09-05.md) adds a textual
lesson: a synoptic edition's unbracketed word may conceal supplied letters
explicit in the detailed collation. Preserve that distinction and compare
translation technique before retroverting another Hebrew word. The published
Greek variant here does not require replacing Hebrew עם or English “my people.”
Neither finding changes the rule that an optimal translation is an argued,
uncertainty-bearing decision, not a majority vote or a generated reconstruction.

The [Numbers note transaction](NUMBERS_22_19_NOTE_APPLICATION_2026-09-05.md)
implements one deliberately narrow application: preserve baseline evidence,
bind approval to exact candidate bytes, archive stale review state, and check
actual export after replacement. The judge's failed method-drift test was
repaired before application. Historical samples now need an explicit guarded
baseline overlay after approved edits; silently updating expected results
would erase the distinction between the experiment and the revised corpus.
This local note application is not a completed source-selection or publication
package, and its near-synonymous note does not demonstrate semantic gain.

The [region-grounding follow-up](EN_GEDI_REGION_GROUNDING_2026-09-05.md)
adds a substantive check before more rendering work: establish that the
measured region actually contains the proposed reading control. Merge5
visually resembles the initial blank margin; a fixed affine registration
failed its own coarse gate. Keep that failure and leave projected locators
unaccepted. Select a text-bearing segment next instead of treating more exact
numeric values as progress on reading accuracy. Conjectural paleographic
drawings are not independent ground truth for the render they interpret.

The [Samuel follow-up](SAMUEL_20_6_SOURCE_ENGLISH_FOLLOWUP_2026-09-05.md)
demonstrates why direct version and grammar checks can strengthen abstention:
Greek shading, Syriac injury and a grammar-driven emendation are distinct
evidence, not agreement on one recovered Hebrew. The
[full 4Q24 reassessment](4Q24_LEVITICUS_2_PRIMARY_FOLLOWUP_2026-09-05.md)
also upgrades a previously abstract-only identity lead without pretending its
processed figure supplies the still-unverified target-word pixels.

The [Deuteronomy follow-up](PENTATEUCH_SOURCE_COMPARISON_PASS_4.md) makes
genre-aware assessment explicit and narrows the next manuscript acquisitions.
This reinforces the delivery priority: finish a consequential dossier instead
of allowing ever-wider catalogue discovery to substitute for adjudication.

The September 5 Latin follow-up corrects a substantive overgeneralization:
“Jerome's Hebrew Psalter omits the Psalm 145 line” is now an edition-specific
statement. Weber–Gryson omits it, whereas Harden prints it and records contrary
manuscript reports. The registry now has 25 entries, still only 13 comparison
cases and 20 physical coverage records. This strengthens the case for exact
edition/hand attribution and apparatus-convention checks before reconciliation;
it is not a new Hebrew discovery or a reason to count editions as witnesses.
See the linked Psalm 145 report for primary-source locators and limitations.

The [Psalm 145 follow-up](PSALM_145_SOURCE_COMPARISON_2026-09-05.md) adds direct
edition/transcription checks to an existing provisional decision. The running
ledger reaches thirteen cases and twenty coverage records. It demonstrates two
import hazards: a suffixed Greek verse label and a Hebrew index tag containing
both the target line and surrounding refrains. Source-specific wording remains
separate from inclusion preference; POB now discloses the line without an
unapproved main-text addition.

The [September 5 Exodus follow-up](EXODUS_INCENSE_ALIGNMENT_2026-09-05.md)
operationalizes many-to-one passage alignment: ten apparent missing labels
are a relocated instruction block, and order agreement differs from clause
agreement. The running ledger is twelve cases and 19 coverage records; the
table above remains the earlier snapshot. This reinforces passage-specific
comparison rather than fixed family rankings. It also corrects a POB footnote
attachment without prematurely changing Hebrew source or English main wording.

Follow-up audit: the [OT/NT source coverage review](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md)
confirms that the pilot uses relevant but incomplete evidence. It adds missing
apparatus/catalogue requirements and current edition checks. Applying the
preservation rule also caught overclaims in Exodus: 4Q11's numeral and 2Q2's
geography are supplied; 4Q14 supports only the local Egypt-to-duration sequence.
The [corrected pass 2](PENTATEUCH_SOURCE_COMPARISON_PASS_2.md) records the
withdrawn claims and the narrower evidence. This is a concrete reliability
improvement, not a new decipherment or a new main-text selection.

Subsequent [Samuel pass 2](SAMUEL_SOURCE_COMPARISON_PASS_2.md) brings the ledger
to nine comparison cases and 16 coverage records (the table above preserves
the earlier review snapshot). It withholds support from disputed 4Q52 fragment
identification and unassigned 1Q7 traces. The controlling method now explicitly
requires checking later corrections to published readings; a recent digital
release is not evidence that all reassessments were incorporated.

The [third Samuel pass](SAMUEL_SOURCE_COMPARISON_PASS_3.md) brings the running
ledger to ten cases and 17 coverage records. Its follow-up connects a published
reading to the edition-cited historical infrared photograph, with a private
two-tile provenance receipt. The inspection was context-informed and partial;
it does not establish a new decipherment or close source-selection gates.
It also exposed an unreliable plate-range route. Operationally, identify a
fragment using edition/object identifiers and matching text before treating
its photograph as evidence for a passage.

The [non-Qumran follow-up](NON_QUMRAN_SOURCE_RECONCILIATION_2026-09-04.md)
adds two operational improvements: reconcile what an index already contains
before declaring entire findspots absent, and test restoration pipelines for
false letter-shaped artifacts. En-Gedi provides a measured-data benchmark
candidate and three published-word retention checks, not a new decipherment.
Its dataset remains unacquired and the benchmark unexecuted. Greek Minor
Prophets fragments receive one object identity with publication/hand layers,
not one independent vote per discovery announcement.

### 1. Define the textual target before selecting words

Maintain three products: witness transcriptions, a versioned POB critical
source with apparatus, and English tied to that source. Define the intended
literary form for each book or substantial passage. An eclectic source is
permissible when justified, but it must identify every departure from its base
and test whether the combined result is coherent. Keep alternative editions
available where their relationship cannot be resolved.

“Earliest attainable” needs this qualification: earliest attainable within the
documented transmission and chosen textual target. It does not authorize
speculative recovery of a pre-manuscript composition. Tov describes the
difficulty of ordering early formulations and the judgment involved in choosing
among them. The INTF similarly describes reconstruction of an initial text
from transmission evidence.
[Tov's methodological introduction](https://www.thetorah.com/series/textual-criticism-of-the-torah-ten-short-case-studies),
[INTF on the initial text](https://www.uni-muenster.de/INTF/en/forschung/cbgm/index.html).

Keep the existing modest preference for earlier attestation when evidence is
otherwise comparable. Make its effect explicit and test whether the decision
would survive removing that preference. Do not add another age bonus after
already counting the same early witness in the external evidence.

### 2. Use published evidence first; target new image work

Build passage dossiers from reliable editions, versioned transcriptions, and
institutional catalogues. Commission no new human work as a prerequisite;
retain the authorized Codex-led workflow. Existing scholarship is evidence to
evaluate, including where scholars disagree.

Prioritize images when a consequential letter, correction, join, or lacuna
could change the decision. Fresh image inspection is required for a claimed
fresh decipherment. It need not be an absolute gate for every published-text
comparison or every English improvement. A literature-based decision can
advance when exact attestations, editorial qualifications, opposing evidence,
and its review basis are documented. Unresolved image-dependent claims stay
open. The existing Deuteronomy pilot keeps its explicit pending image gate.

ImageGen remains educational. It receives an already documented hypothesis and
cannot increase confidence in a reading. Deterministic enhancement also needs
comparison with the original: reproducibility does not establish that a
sharpened edge or thresholded mark represents an ancient stroke.

### 3. Calibrate the machine workflow before broad acceptance

Retain different model families and freeze their outputs before reconciliation.
For an image-reading pass, withhold the reference, expected reading, and other
pass output where practical. Record unavoidable identifying context. A familiar
passage can be recalled despite neutral labels; blind inputs reduce this risk
without proving absence of training-data contamination.

Use a separate context-informed pass for restoration hypotheses and textual
criticism. Measure how much the output changes after context is supplied.
Agreement on supplied letters establishes a shared proposal; it does not
establish that the lost material contained those letters.

Start with a development set and a frozen evaluation set covering clear text,
faint text, corrections, edge loss, full lacunae, and unfamiliar passages. Keep
fragments of the same manuscript out of both sides where feasible. Published
readings used as reference labels need their own certainty and source fields;
disputed labels cannot be scored as unquestionable truth. Artificial masking
tests contextual completion only, and must be reported separately from real
damage.

Report character errors on legible text, wrong assertions among accepted
readings, supplied characters mislabeled visible, abstentions, and disagreement
resolution. Show sample sizes and results by damage class. Set acceptance
criteria before the frozen run; do not choose a success threshold after seeing
results. Repeat the frozen comparison after a material model or prompt change.
No numerical historical-confidence claim follows from transcription accuracy.

Research has demonstrated position bias in model evaluations. That supports
randomizing candidate order and hiding model identities in our English and
argument reviews. It does not provide a measured error rate for this project's
manuscript workflow.
[Wang et al., ACL 2024](https://aclanthology.org/2024.acl-long.511/).

### 4. Separate the dimensions of confidence

Report confidence in object identification, reading/legibility, passage
alignment, interpretation of a daughter version, historical priority, and
English rendering separately. A well-attested phrase can have uncertain
priority; a secure Hebrew source can allow several English renderings.

Record which decisive letters survive and which are supplied at the variation
unit, rather than attaching a blanket support label to a reconstructed verse.
Existing support labels are triage summaries and need this finer audit before
promotion. Treat relationship groups as provisional dependency statements,
not established genealogies. A transcription and its manuscript are two
evidence layers for one witness; an edition and an ancient version are different
objects again.

### 5. Give English review its own testable track

Some improvements need no source change. Run these alongside manuscript work:
lexical sense, syntax, referents, idiom, discourse, poetry, and meaningful
ambiguity. Compare a close source gloss, the current POB sentence, and a
candidate in paragraph context. Record both what improves and what nuance is
lost. Grammatical gender alone does not settle the English referential scope.
Apply and disclose POB's stated translation commitments; this review does not
silently rewrite DOCTRINE.md.

Use an explicit rubric: semantic fidelity, unsupported additions, ambiguity,
literary function, natural English, and consistency with justified exceptions.
Hide which candidate is current POB and vary presentation order during review.
Model preference, back-translation, or agreement with familiar English Bibles
alone does not establish superior fidelity.

### 6. Reduce bookkeeping and close complete cases

Use one shared method, one ordered backlog, and generated case reports. Retain
the chronological pass reports as research history. Their assertions must not
override newer evidence. Preserve superseded source hashes and explain changes;
a later matching text cannot prove why an earlier commit became unavailable.

The LXX snapshot repair illustrates the need for content hashes and lawful,
rehydratable evidence snapshots in addition to repository commit IDs. The
previous commit did not resolve in a fresh clone; the six stored Greek texts
matched the replacement commit exactly. The cause of the missing object was
not established.

The selection pilot now rejects empty review gates, source phrases found only
in notes, and fully bracketed selected phrases. It also rejects publication
claims outright: review receipts and actual source/English/export application
have not been implemented. Passing a schema checks structure, not historical
truth or completed publication.

## Next delivery sequence

1. Complete the calibration design and freeze its evaluation inputs before
   expanding machine acceptance. Benchmark execution remains outstanding.
2. Finish the existing dossiers (now thirteen formal comparison cases) to a definite research outcome: retain,
   propose a change, or unresolved. State precisely what evidence would change
   each outcome; do not force a decision because a case is old.
3. Implement one reviewable source-and-English change package, including base
   text, selected unit, notes, affected metadata, before/after hashes, review
   evidence, and downstream export checks. A full source can be derived from a
   pinned base plus explicit reviewed patches; reconstructing every unchanged
   word anew is unnecessary.
4. Expand Samuel and Jeremiah with passage/book-form maps; extend the NT queue
   through individual manuscript and hand records. Rank new cases by English
   consequence, tractability, source access, and unresolved evidence.
5. Scale discovery and collation by book. Report denominators separately for
   catalogued witnesses, accessible witnesses, passage coverage, compared
   units, adjudicated units, and reviewed English. Do not call note screening
   “all texts compared.” Keep a sampled unflagged control set to test what the
   discovery method misses.

## Implementation status and migration

The shared method is now version 2.0.0. This review, the charter, priorities,
backlog, and NT method have been aligned. Existing decision datasets retain
their recorded method version 1.0.0 until individually re-reviewed; none has
been retroactively labeled calibrated or independently reviewed.

The existing DSS machine-consensus status names remain valid as working
transcription/reconstruction labels. They carry no automatic canonical
promotion authority. Calibration measurements, richer token-level support,
dependency records, review receipts, and the release application mechanism
remain implementation work. No new manuscript reading was promoted by this
method review.
