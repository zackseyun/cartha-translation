# POB biblical source restoration: method and research log

Started 2026-09-05; history backfilled from the linked repository records.
This is the central Git-ready record for this restoration program, not a
claim to reconstruct every event in POB's earlier history. Record decisions,
evidence, alternatives, concise rationales, changes, failures and open questions.
Detailed transcriptions and hashes remain in the linked artifacts. Do not put
credentials, private account envelopes or restricted source images here.

Start here: [current assessment and improvements](TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md#current-reassessment--2026-09-05),
[which OT/NT sources to compare](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md),
[controlling method](TEXTUAL_ADJUDICATION_METHOD.md),
[dated history](#evidence-linked-research-history),
[remaining work](#remaining-work), and
[proposed About summary](#later-about-page-summary--proposed-not-published).

This Markdown file lives in the Git repository; saving it does not itself make
a commit. Its earlier history is a recoverable, evidence-linked backfill, not
an exhaustive transcript. Record concise decision rationales and alternatives,
not a claimed reconstruction of undocumented deliberation. The linked method
controls current work; dated entries preserve what was known at the time.

## Objective and current assessment

Discover the relevant surviving Old Testament sources, investigate whether
measured imaging data can reveal unread text, compare witnesses, establish the
best-supported attainable Hebrew/Aramaic source, and test whether that changes
or improves POB English. Extend the same principles to NT Greek. ImageGen can
illustrate a documented reconstruction; it cannot supply evidentiary ancient
strokes or increase confidence in a reading.

The foundation is useful but incomplete. The program has not established a
complete restored critical Bible, a newly deciphered biblical variant, or a
measured improvement rate over existing editions. A newer model reviewing
earlier work is not independent blind corroboration.

Snapshot, 2026-09-05: 27 mixed OT witness/edition/family registry entries,
13 formal comparison cases, 20 physical passage-coverage records and one
unpromoted atomic source/English selection. These are different units, not
counts of completed collations. The canonical inventory covers 66 books /
31,221 verse files; the NT edition apparatus is not a manuscript census.

## Our approach, end to end

1. **Define the target.** Seek the earliest attainable text within documented
   transmission and a specified literary form, not an asserted autograph.
   Preserve alternative forms where combining them makes an unsupported
   composite. OT Aramaic remains Aramaic; NT Greek remains Greek.
2. **Discover broadly.** Use institutional catalogues, critical editions,
   published corrections and dated transcription releases. Reconcile object
   IDs, aliases, provenance, language, genre, passage survival, scribal hand,
   access and rights. List disputed, unpublished and inaccessible material.
3. **Prioritize transparently.** Include contrary evidence. Prioritize sources
   that preserve the disputed unit, distinguish alternatives and could affect
   meaning or literary form. Catalogue-screened, acquired, transcribed,
   collated and adjudicated are separate milestones.
4. **Preserve evidence layers.** Keep measurements/photos, deterministic
   derivatives, diplomatic transcription, normalization, supplied reconstruction
   and generative illustration distinct. Record processing steps and hashes.
   A bright or letter-shaped artifact is not necessarily ink. Pin software
   revisions and parameters; compatible period code is not automatically the
   code used for an archived result. Keep static inspection, numerical emulation
   and execution of the original renderer distinct.
5. **Test restoration.** Freeze development and held-out controls with known
   uncertainty, clear text, damage, loss and artifacts. Separate artificial
   masking from real damage. Measure wrong asserted letters, supplied-as-visible
   errors, abstentions and legible-text errors. Different model families' unseen
   first passes are a working gate, not proof of accuracy or historical priority.
6. **Align by content.** Allow different numbering, suffixes, relocated blocks,
   verse splits and literary forms. An index hit does not prove that the
   decisive letters survive. Keep brackets and uncertain glyphs traceable.
7. **Establish each version's own text.** An edition is not a manuscript.
   Distinguish Greek revisions, Latin Psalters, Syriac versions, Targum works
   and hands. Read apparatus conventions before interpreting silence.
   Hebrew/Greek back-translations remain hypotheses.
8. **Adjudicate locally.** Assess external evidence, copying explanations,
   translation habits, grammar and context. Record the strongest counterargument.
   Age, majority and a desired theological result do not win automatically.
   Reading certainty, historical priority and rendering confidence stay separate.
9. **Evaluate English separately.** Compare POB, a close source gloss and a
   candidate in context for fidelity, unsupported additions, ambiguity, literary
   function, naturalness and justified consistency. Source-stable English
   improvements need no invented manuscript variant.
10. **Apply and verify together.** Require a pinned base, exact selected unit,
    retained alternatives, synchronized source/English/notes, review evidence,
    hashes and export checks. Schema success is not historical proof. Preserve
    uncertainty and do not silently promote proposals.

Controlling detail: [shared method](TEXTUAL_ADJUDICATION_METHOD.md),
[charter](DSS_TEXTUAL_WITNESS_PROJECT.md),
[approach review](TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md),
[OT/NT source coverage](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md),
[NT method](NT_TEXTUAL_WITNESS_METHOD.md) and
[source-use policy](../REFERENCE_SOURCES.md).

## Evidence-linked research history

Dates follow the source reports. Backfilled entries summarize their documented
outcomes; they do not imply those experiments were rerun today.

### 2026-09-02 — image pilot and source/English separation

Lawful LOC assets and pixel-exact crops established an acquisition route. One
OpenAI image-only pass returned 13 line/stroke-group rows and 68 segments; its
three self-labeled clear segments were not independently verified words.
Earlier attempts timed out. Anthropic returned an access error, not a second
transcription. No two-family acceptance, restored words or publication resulted.
The source-wording pilot separated working preferences from canonical impact.

Evidence: [image results, attempts and limitations](../sources/dead_sea_scrolls/pilots/2026-09-02-dual-vision/RESULTS.md),
[Hebrew pilot](HEBREW_PILOT_ADJUDICATION.md),
[English-impact record](../sources/textual_restoration/decisions/english_impact_check.v1.json).
That historical access error does not establish present service availability.

### 2026-09-03–04 — audit, calibration policy and discovery

The audit separated source selection from translation and rejected inventory
coverage as proof of a completed critical corpus. It corrected Genesis 4:8
metadata claiming an absent speech clause was included. The review withdrew
automatic publication implications from model agreement and required measured
calibration. The full QDR word-reference screen found 266 records / 265 labels
and corrected an Isaiah casebook anchor. The Samaritan reference screen examined
5,841 verse nodes; 3,969 same-label consonantal differences are leads, not errors.

Evidence: [initial audit](TEXTUAL_RESTORATION_AUDIT_2026-09-03.md),
[approach review](TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md),
[discovery receipts](../sources/textual_restoration/discovery/README.md),
[Samaritan screen](SAMARITAN_CORPUS_SCREEN_2026-09-04.md).

### 2026-09-04 — Pentateuch comparisons and corrections

Genesis 4:8 and Exodus 1:5 / 12:40 received Hebrew, Samaritan and Greek controls.
Exodus's longer residence forms were distinguished. A re-audit withdrew
overclaims: 4Q11's count and 2Q2's geography are supplied; 4Q14 supports only a
local sequence. At Deuteronomy 27:4, 4Q33's supplied mountain name votes for
neither Ebal nor Gerizim. Deuteronomy 32:43's Hebrew and Greek longer forms were
kept distinct. At 32:8, published 4Q37 supports sons of God, while 4Q45 loses
the decisive phrase. A research selection bundle prevents changing English
without synchronized source selection; promotion remains pending.

Evidence: [pass 1](PENTATEUCH_SOURCE_COMPARISON_PASS_1.md),
[corrected pass 2](PENTATEUCH_SOURCE_COMPARISON_PASS_2.md),
[pass 3](PENTATEUCH_SOURCE_COMPARISON_PASS_3.md),
[pass 4 and selection gates](PENTATEUCH_SOURCE_COMPARISON_PASS_4.md).
Reader-note and metadata repairs are not new main-text selections.

### 2026-09-04 — Samuel and Psalm 22

The Goliath-height dossier improved its published Hebrew basis while retaining
the uncertain alef and supplied surroundings. At 1 Samuel 14:41, the 4Q52
identification dispute prevents positive Hebrew support. At 2 Samuel 21:19,
1Q7's isolated traces do not decide the names; Chronicles is a parallel work,
not another Samuel manuscript. The 1 Samuel 1:24 investigation separated animal,
bread and narrative questions. Its edition-linked historical photograph was
partially inspected; a mismatched plate route was excluded. Greek apparatus
and Syriac controls supplied further, non-uniform evidence.

Psalm 22 distinguished the published Nahal Hever spelling from 4Q88's uncertain
and supplied letters. Syriac injury wording and the Targum's biting/lion wording
do not establish one exact Hebrew verb. Historical priority remains unresolved.

Evidence: [Samuel 1](SAMUEL_SOURCE_COMPARISON_PASS_1.md),
[Samuel 2](SAMUEL_SOURCE_COMPARISON_PASS_2.md),
[Samuel 3 and follow-ups](SAMUEL_SOURCE_COMPARISON_PASS_3.md),
[Psalm 22 and versional follow-up](PSALM_22_SOURCE_COMPARISON_PASS_1.md).

### 2026-09-04 — beyond Qumran and En-Gedi discovery

Reconciliation found 22 non-Qumran-associated labels already in QDR; naming
alone does not establish provenance or genre. En-Gedi is not the Arugot
Leviticus index entry. Three published En-Gedi words matched POB source words,
but did not validate fresh unwrapping. Greek Minor Prophets material was
registered as one object with publication layers, not one vote per discovery.

Evidence: [non-Qumran report](NON_QUMRAN_SOURCE_RECONCILIATION_2026-09-04.md).

### 2026-09-05 — relocation, Psalm 145 and Latin revision

Ten apparently missing Exodus incense-altar labels belonged to a relocated
block. Order agreement differed from clause agreement; notes were repaired
without new source/English main wording.

Psalm 145's missing acrostic letter and published 11Q5 line were checked against
Greek, Syriac and Targum controls. A Greek suffix and Hebrew tags spanning
refrains exposed importer hazards. The reader note now gives witness-specific
wording; inclusion and exact wording remain separate. Latin consultation then
corrected “Jerome omits it” to edition-specific evidence: Weber–Gryson omits
the line, Harden prints it and reports A H R omission. Printed apparatus and
sigla were visually checked. No edition was counted as new Hebrew evidence.

Evidence: [Exodus alignment](EXODUS_INCENSE_ALIGNMENT_2026-09-05.md),
[Psalm 145 including Latin correction](PSALM_145_SOURCE_COMPARISON_2026-09-05.md).
The Latin follow-up's 136 targeted tests passed; they check record constraints,
not the historical conclusion.

### 2026-09-05 — measured-data acquisition and this central log

The En-Gedi high-resolution master was acquired, its listed MD5 verified, and
SHA256/dimensions recorded. A bounded HTTP-range tool indexed the segmentation
archive and CRC-verified four merge5 files: material, mesh, texture and mask.
There are 29,285 entries / 29,259 files, agreeing with the archive's file count
after excluding directories. Seven segment groups are indexed. The full archive
checksum, per-pixel mapping payload and raw CT were not acquired/verified.
Master and texture received context-informed overview, not transcription/scoring.

The published master was manually merged and contrast-adjusted. A suspicious
mark needs a traceable path through rendering/segmentation to measurement data
before a fresh recovery claim. These assets advance acquisition, not completed
calibration. They remain outside Git under the dataset's noncommercial license.
See the [asset follow-up](NON_QUMRAN_SOURCE_RECONCILIATION_2026-09-04.md#en-gedi-asset-follow-up--2026-09-05)
and [checksum receipt](../sources/textual_restoration/discovery/en_gedi_asset_check.v1.json).

At the user's request, this log was added and linked from repository entry
points. Cross-checking uncovered an obsolete “already optimal” paragraph in
REFERENCE_SOURCES.md contradicting its revised assessment; it was replaced
with the bounded current claim. No About-page change, deployment or Git commit
was performed in this pass. Local edits are not a published repository release.

Verification: 145 targeted unit tests passed, including bounded HTTP response,
ETag, ZIP-header/CRC and acquisition-boundary checks. The asset builder verified
the actual local master and four payloads against the saved receipt. The OT
registry validator and `git diff --check` passed; all 28 local links in this log
resolved. These checks establish the tested data/record integrity, not a
restoration accuracy rate or a historical reading.

### 2026-09-05 — CT mapping acquisition and numerical sensitivity check

The next pass acquired the 137.9 MB merge5 gzip mapping, reconstruction log,
and four CT slices using explicit per-member limits and streaming CRC checks.
The complete mapping stream has 39,671,412 values; its dimensions match the
segment texture/mask. The scan index has 4,504 numbered slices, excluding Mac
sidecars. The log establishes that these are reconstructed CT slices, not raw
X-ray projections; earlier “raw CT” wording was imprecise.

At a preselected interior coordinate, normal-offset sampling materially changes
intensity. Direct-index and +2 indexing hypotheses were both tested because
the log and archive start labels differ; neither was promoted. These numeric
profiles do not reproduce the published neighborhood renderer or establish ink,
letter identity, a correct coordinate origin or transcription accuracy. A zero
mapping outside the mask is not a sample at the volume origin. No image edit,
generated image, POB source change or English change occurred.

Evidence and reproduction: [coordinate-probe report](NON_QUMRAN_SOURCE_RECONCILIATION_2026-09-04.md#en-gedi-coordinate-and-intensity-probe--2026-09-05)
and [input/output receipt](../sources/textual_restoration/discovery/en_gedi_volume_probe.v1.json).
The original acquisition receipt now explicitly limits its verification scope
so its earlier exclusions cannot be mistaken for current acquisition status.

Verification: 147 targeted repository tests and five NumPy/Pillow mapping tests
passed in their respective runtimes. Both acquisition and volume-probe builders
reproduced their saved receipts from local payloads. Registry validation and
`git diff --check` passed; all 30 local links in this log resolved. The five
mapping tests exercise synthetic parser/interpolation cases, not ancient-letter
accuracy. The complete scientific restoration benchmark remains unexecuted.

### 2026-09-05 — historical renderer inspection

Question: can period code explain the acquired mapping and define the next
reproduction test? The 2016 paper specifies bidirectional line sampling, a
seven-voxel primary axis and a maximum filter. A September 2016 Volume
Cartographer revision writes the same six-channel OpenCV YAML format. Its
rendering call chain uses half-voxel sample intervals and directly numbered
slice filenames, without adding the reconstruction log's first-section label.
This supports direct indexing as a code-grounded candidate; it does not yet
prove registration of this particular archived output.

Static inspection also found a nonstandard corner reference in that revision's
interpolator, integer rounding, and float-valued sample coordinates. The caller
was traced through VolumePkg to Volume rather than assuming that similarly
named code was used. These details matter to reproducibility, but the revision
has not been established as the executable used for the published scroll.
No claim that this affected the published letters follows from this inspection.

Decision: retain the previous numerical receipt as an ordinary-trilinear
sensitivity experiment. Do not relabel it a historical rendering reproduction,
choose an indexing shift by one pixel's brightness, or silently equate the
paper's axis length with a software radius parameter. Freeze a documented
candidate protocol before testing additional held-out coordinates. The
strongest alternative explanation is that the archive was generated with a
different revision or parameterization.

Evidence: [historical code inspection and pinned source links](NON_QUMRAN_SOURCE_RECONCILIATION_2026-09-04.md#en-gedi-historical-renderer-inspection--2026-09-05).
This pass changes documentation only; it executes no new renderer, transcription
benchmark, source selection or English revision. Direct PMC access was
intermittently challenged; the relevant primary-paper passage was available
through indexed search. No new unit-test result is claimed for static inspection.
The central log remains linked from the README, source policy, charter,
discovery README and TODO. About integration and a Git commit remain unperformed.
Verification: all 31 local links in this log and nine in the En-Gedi report
resolve; direct whitespace checks passed for both files, including these
untracked documents. The new report section used by the cross-reference exists.

### 2026-09-05 — fixed numerical renderer candidates and local exact matches

Question: do the historically motivated sampling conventions predict archived
texture values without tuning to new pixels? A hashed protocol fixed eight
candidates, the already known center, and eight geometric horizontal neighbors
before their texture values were inspected. The first attempted calculation
stopped on missing measurements. Preflight identified precisely slices 1648
and 1653; both were acquired and CRC/SHA256-verified outside Git. No test point
was dropped and no radius, offset, contrast or interpolation choice was tuned.
ZIP-directory searches found no entries containing config, readme or metadata;
that filename search does not establish that export settings are unrecoverable.

Result: radius parameter 7, direct slice indexing and the historical corner
interpolation candidate matched the center and all eight held-out values
exactly. Other candidates did not match all nine. The coordinates span four
recorded normals but are locally correlated, same-row samples in one segment.
This advances local numerical reproduction; it is not whole-scroll validation,
an identified original executable, a transcription benchmark or new letters.
The candidate grid and prior sensitivity receipt remain unchanged.

Decision/rationale: preserve all candidate results and the observed exact
matches without an automatic source or renderer promotion. The strongest
limitation is generalization beyond this local set; rounded maximum values
also need not identify a unique underlying implementation. Reproducing the
historical interpolation discrepancy helps trace the archive, but does not
make it the best recovery algorithm. Keep correct ordinary interpolation as
a separate comparison and judge recovery against independent physical controls,
not merely against a historical rendering or expected biblical wording.

Changed artifacts: [protocol](../sources/textual_restoration/discovery/en_gedi_renderer_protocol.v1.json),
[result/input receipt](../sources/textual_restoration/discovery/en_gedi_renderer_probe.v1.json),
[reproduction tool](../tools/textual_restoration/build_en_gedi_renderer_probe.py),
mapping/receipt tests, the shared payload verifier's optional hash set, registry
acquisition/next-action fields and discovery documentation. The
[full report](NON_QUMRAN_SOURCE_RECONCILIATION_2026-09-04.md#en-gedi-fixed-candidate-renderer-test--2026-09-05)
contains every candidate's error summary, limitations and reproduction commands.
No image was edited/generated, and no Hebrew or English main text was changed.

Verification: the new builder reproduced the complete saved result from the
private, checksum-pinned inputs and also reverified the prior volume receipt.
149 targeted repository tests and nine NumPy/Pillow numerical tests passed;
registry validation passed with the unchanged 25/20/13/1 scope counts. All 35
local links in this log, 12 in the En-Gedi report and 11 in the discovery README
resolve. Direct whitespace checks cover the new untracked artifacts as well.
These checks support numeric/data integrity, not transcription accuracy.

Next: predeclare wider spatial and multi-segment checks of the locally supported
candidate, then establish master registration and independently labeled real
damage/material/ink controls. These remain prerequisites to a recovery claim.

### 2026-09-05 — all twelve En-Gedi published comparison units

The textual branch advanced beyond the earlier three-word spot check to all
twelve units explicitly listed in the 2016 edition's pp. 10-11 apparatus.
The PDF skill required visual review: rendered pp. 8-11 were inspected because
text extraction dropped bracketed Hebrew. The original PDF hash matched;
a fresh institutional fetch timed out, without invalidating the local copy.

Result: all twelve editorial forms align with current POB source contexts
across ten verses. Ten units are unbracketed labels and two have supplied
prefixes. The pinned SP control differs in ten local contexts. For 4Q24, the
QDR transcription also contains the two reported comparison forms at the
correct tags/lines. Initial dotted-reference lookups returned no hits; source
tags use spaces and colons. This was corrected rather than recorded as absence.
An overbroad diagnostic output was truncated; subsequent inspection was limited
to the actual relevant lines and did not rely on the omitted output.

Decision/rationale: no source-driven main-text English change was selected.
Published supplied stems remain supplied, and a reported ghost stroke is not
accepted as an ancient letter. Footnote 19 makes the Greek/Syriac apparatus
selective, so silence cannot be a supporting vote. Edition alignment does not
prove original priority or full verse agreement. The strongest remaining
limitations are the lack of primary 4Q24 image/apparatus verification, complete
versional controls and a full diplomatic line/loss map.

A distinct source-stable English lead was recorded for the later agents in
Lev 2:8. The existing cross-check flag is not an independent explanation of
this issue: its cited review JSON was absent at the recorded local path.
No Hebrew, English, note or lexical rationale was changed on that basis.

Artifacts: [apparatus units](../sources/textual_restoration/discovery/en_gedi_apparatus_units.v1.json),
[checked receipt](../sources/textual_restoration/discovery/en_gedi_apparatus_check.v1.json),
[reproduction tool](../tools/textual_restoration/build_en_gedi_apparatus_check.py),
[full report](EN_GEDI_APPARATUS_COMPARISON_2026-09-05.md), six new unit tests,
discovery documentation and the registry's En-Gedi role/next steps. This does
not add twelve formal critical selections or twelve independent witnesses.
The earlier numeric and three-word receipts are unchanged.

Verification: the apparatus builder reproduced its receipt from the actual
pinned edition/SP/QDR inputs and current POB files. 155 repository tests plus
nine numerical tests passed; registry validation retained 25 source entries,
20 coverage records, 13 formal comparisons and one unpromoted selection.
All 39 local links in this log, four in the new report, seven in the TODO and
12 in the discovery README resolve; direct whitespace checks also covered the
new untracked files. These are provenance/alignment/record checks, not a
measured ancient-letter accuracy score.

### 2026-09-05 — Leviticus 2:8 agency and pointing review

The preceding pass was progress: twelve published comparison units were checked
and an English-agency lead was identified. This follow-up consulted the actual
WLC verse, the local UWHB morphology, a pinned Rahlfs-derived Greek snapshot and
the publisher's NET note. Failed HTML routes included a wrong-passage response;
the publisher PDF was acquired and its full relevant page visually inspected
under the PDF skill. It reports a tentative imperative repointing, not merely
an English style preference. BHS and the commentaries it cites were not
independently inspected and are not claimed as consulted sources.

The Hebrew sequence has an initial second-person verb followed by third-person
forms. Greek's approach participle at the end of its verse 8 continues with the
explicit priest subject in verse 9; analysis must cross the numbering boundary.
UWHB and WLC are controls on the same tradition, not separate manuscript votes,
and the digital Greek morphology's confidence labels are not textual certainty.

Decision: repair two lexical rationales that prematurely assigned priestly
agency to delivery to the priest. Preserve source, main English, reader notes
and old review state. Contextual agent names remain inferred; an imperative
chosen through new Hebrew pointing is a separate source-interpretation decision.
The strongest objection to the retained English is its ambiguous repeated he;
the strongest objection to explicit names is that they add inferred agents.
Neither candidate was blind-reviewed or promoted in this pass.

The [agency report](LEVITICUS_2_8_AGENCY_REVIEW_2026-09-05.md) and
[repair record](../sources/textual_restoration/decisions/leviticus_2_8_agency_review.v1.json)
preserve sources, exact before/after lines and hashes, unchanged components,
alternatives and remaining gates. Tests reverse the two substitutions and
reconstruct the complete pre-edit byte stream. The twelve-unit apparatus
receipt was refreshed only for the current Lev 2:8 file binding; the comparison
results did not change. The shared method now explicitly separates pointing
choices from consonant-stable English clarification. The TODO and prior report
link this follow-up. No new letter, reader-text revision or deployment occurred.

Verification: 160 repository tests plus nine numerical tests passed, including
five new agency/repair checks. The apparatus builder reproduced the refreshed
receipt from pinned inputs; registry counts remain 25/20/13/1. All 41 local
links in this log, three in the agency report, eight in the method, five in
the earlier apparatus report and eight in the TODO resolve. Direct whitespace
checks included the new untracked repair/test files. The tests establish the
repair's bounds and record consistency, not the best historical reading.

### 2026-09-05 — Leviticus identity reassessment and documentation continuity

Question: does the legacy 4Q24 identifier adequately describe the Hebrew
control used in the En-Gedi comparison? Institutional metadata identifies
Tigchelaar's two-manuscript reassessment (online 2020, journal issue 2021).
Himbaza's publisher-provided 2020 introduction places the local passage in
proposed 4Q24a. The full reassessment and DJD figures remain uninspected;
access failures are recorded, not concealed as successful consultation.

Evidence, exact access limits, PDF hash, inspected pages and next gates:
[Leviticus witness identity review](LEVITICUS_WITNESS_IDENTITY_REVIEW_2026-09-05.md).
The PDF skill prompted full visual review of the four catalogue-table pages,
including footnotes and a page-spanning row. The publisher's open-access PDF
remains private outside Git; no republication license was assumed.

Decision: keep upstream QDR locators reproducible while adding an explicit
identity warning. Require a sourced fragment/hand crosswalk before migrating
IDs, dates or counts. An old label can preserve a correct transcription, so
this finding does not justify changing the Hebrew or English. It does require
checking provenance before later adjudication. The dated book-wide table is
a discovery aid, not certification that all current witnesses are compared.

Updated the shared method, source audit, prior apparatus report and TODO to
propagate this qualification. Also refreshed the audit's stale three-word
En-Gedi summary to the later twelve-unit bounded comparison and linked the
agency-only rationale repair. No evidence receipt, translation, registry count,
About section, deployment or commit changed in this pass.
Clarified that the prior En-Gedi report's pp. 1-30 are internal PDF pagination,
not the final journal's 29-58 reported by Himbaza; existing locators are retained.

Documentation commitment: this Git-ready Markdown log is the durable entry
point requested by the user. It records recoverable history and concise
decision rationales with evidence links, not an invented exhaustive transcript
of undocumented earlier activity. Continue adding outcomes, corrections,
failed attempts, tests and open questions here. The later About summary below
remains a proposal until explicitly requested.

Verification for this documentation-only pass: all 83 local links across the
six touched documents resolve; direct trailing-whitespace/newline checks pass,
including untracked documents. Git diff whitespace checks pass for the two
tracked documents. The registry validator passes with unchanged 25 source
entries, 20 coverage records, 13 comparisons and one unpromoted selection.
No runtime code changed, so the earlier 169-test result was not rerun or
represented as a new test run here. These checks verify document integrity
and registry consistency, not the scholarly reassignment itself.

### 2026-09-05 — complete Leviticus table-to-QDR identity screen

The previous pass was progress: it added a sourced identity qualification and
changed the next action from unqualified 4Q24 use to a fragment-aware crosswalk.
This pass inspected the current documents and pinned QDR bytes, then visually
rechecked all four catalogue-table pages under the PDF skill. It implemented
and ran the [catalogue reconciliation](LEVITICUS_CATALOGUE_RECONCILIATION_2026-09-05.md)
against every target name in that table, not only the two pilot verses.

Findings: 30 source-reported names (27 categorized as published, three as
unpublished in 2020); 18 have scoped hits across 17 QDR labels, and 12 queried
names are absent from the pinned biblical file. Current IAA search-index
metadata supplies primary-edition routes for two Greek witnesses and the
Aramaic Leviticus targum. It also exposes a pap-label/parchment-metadata
qualification that is preserved rather than silently normalized. No IAA image
or DJD text was inspected in this pass.

The legacy 4Q24 reference tags partition into 31 early-chapter and 101
later-chapter anchors, while f29/f30 have no Leviticus-shaped tags and remain
unassigned. The strongest contrary explanation to any 'missing witness' claim
is scope: this is one QDR biblical dataset, and En-Gedi is already present
elsewhere in POB. We therefore report an index/acquisition gap, not manuscript
nonexistence, universal QDR absence or 12 entirely new discoveries.

Implementation: added a 30-target metadata specification, reproducible
hash-pinned builder, derived receipt and 13 tests covering split-label counting,
untagged/mixed fragments, reference aliases, collisions, missing labels versus
missing scoped anchors, input pinning and no private text/index export. The
existing validated QDR scanner is reused. Source/canonical/English selection
flags remain false. Updated the discovery README, source audit, identity
report and TODO to point to the new evidence. The generic bookkeeping can be
reused for other books, but their catalogues have not thereby been inspected.

No source/translation files, formal registry records, About section, deployment
or commit changed. No AI-generated image or newly recovered letter is claimed.

Verification: the final builder reproduced the saved receipt from the pinned
private QDR and PDF inputs with `--verify-only`. All 173 repository tests plus
nine numerical En-Gedi tests passed (182 total), including the 13 new catalogue
tests. The registry still validates 25/20/13/1. All 88 local links in the six
touched Markdown documents resolve; direct whitespace checks include the new
untracked code/JSON/documents, and tracked-file Git diff checks pass. Tests
establish screening behavior and reproducibility, not manuscript authenticity,
historical priority or the best English rendering.

### 2026-09-05 — 4Q120 preservation versus grammatical inference

The preceding catalogue screen was progress: it identified missing versional
targets and supplied reproducible acquisition priorities. This pass followed
4Q120 rather than treating its absence from QDR as absence of evidence.
Current worktree records and the existing POB verse were inspected first.

Consulted Wagner's 2021 Duke manuscript profile and Wevers's institutionally
hosted Leviticus introduction. The PDF skill required rendering and visually
checking the relevant four profile pages. At tentative 2:7-8 the quoted verb's
ending is supplied; its unbracketed prefix cannot alone distinguish the
illustrative second/third-person forms. This changes the next action from
using a verse-range hit to inspecting the discriminating letters and exact
clause alignment. It does not demonstrate that all of 4Q120 lacks useful
constraints or that either illustrative form is an attested apparatus variant.

Evidence and locators: [4Q120 preservation review](4Q120_LEVITICUS_PRESERVATION_REVIEW_2026-09-05.md)
and its linked JSON. The live IAA B-503625 browser record confirms plate 376,
fragment 3 metadata; no target pixels or passage mapping were verified. The
web tool's URL failure and a noisy numeric search are recorded. DJD IX full
text/plates remain uninspected; secondary summaries were not substituted for
that primary edition. The dissertation PDF stays private outside Git.

Registered 4Q120 as an individual Greek witness (26 total mixed source entries)
without creating formal physical coverage or comparison cases. Clarified the
registry's En-Gedi preliminary-versus-final pagination, already documented in
the prior pass. Added a preservation record and five checks, propagated the
finding to method, source audit, catalogue report, TODO and discovery README.
POB source/English/notes/rationales and the prior catalogue receipt are unchanged.
No image-generated evidence, new letter, deployment, About change or commit.

Verification: 178 repository tests plus nine numerical tests passed (187
total). The five new checks preserve the published supply/uncertainty markers,
demonstrate only the shared-prefix contrast, prevent image/retroversion
promotion, verify the unchanged POB verse hash and confirm the registered
object's Greek role. The registry validates 26/20/13/1; the prior catalogue
receipt still reproduces unchanged from real pinned inputs. All 104 local
links across the seven touched Markdown files resolve; direct whitespace and
tracked Git diff checks pass. These checks do not verify the ancient ink,
the exact image/passage mapping or historical reading priority.

### 2026-09-05 — return to Deuteronomy 32:8 and consolidate documentation

The priority/method review directed work back to the existing unpromoted
selection rather than expanding catalogue scaffolding indefinitely. Inspected
the pinned selection, prior pass-4 comparison, coverage record and current
research history. The leading candidate remains a research preference, not a
completed source/English application.

Consulted Dayfani's institutional abstract/bibliography, Tov's online witness
table and notes, and relevant manuscript-list sections of Wevers's author-
translated Deuteronomy introduction. Exact links, locators, observations and
consultation limits are in the [pass-4 follow-up](PENTATEUCH_SOURCE_COMPARISON_PASS_4.md).
This identifies genre context and concrete Greek acquisition targets without
claiming fresh manuscript readings. A published interpretation of a scribal
motive is not an observed act; a version does not settle exact Hebrew spelling.
The strongest procedural counterargument is that neither abstract-level genre
classification nor edition-listed passage coverage decides the disputed unit.
Keep the existing gates and check those units directly.

DOI/publisher article requests returned web-tool errors; no full Dayfani or
DJD edition review occurred. Searches of the Greek introduction for literal
`32,8` and `106c` returned no matches, not proof of missing textual evidence.
Third-party search leads were not substituted for manuscript or apparatus
collation. The original IAA plate-tab context does not identify the target
fragment region by itself. No new manuscript pixels were inspected in this pass.

Updated the pass report, controlling method, 4Q37 coverage note, source audit,
ordered TODO and approach review. The latter now directs current counts to
this log and explicitly marks its old En-Gedi acquisition statement superseded.
Earlier dated snapshots are retained as history. This log remains the Git-ready
documentation target for the requested later About summary/link; no About
integration, commit or deployment was made. No canonical verse, source
selection, English, note, image-derived evidence or review gate changed.

Verification: 178 repository tests and nine numerical tests passed (187 total).
The registry validates 26 source entries / 20 coverage records / 13 comparisons /
one unpromoted selection. All 101 local links across the six touched Markdown
files resolve; whitespace checks pass, and the Deuteronomy verse hash still
matches the pinned baseline. These checks protect structure and existing evidence
boundaries; they do not verify the newly identified manuscript readings or
establish historical priority. Full article/apparatus review, exact image
mapping and synchronized application remain the next substantive work.

### 2026-09-05 — Greek noun preservation and a conflicting correction report

The preceding turn was progress: it updated authoritative documentation and
identified concrete acquisitions. This pass rechecked the worktree and followed
those targets into primary printed evidence rather than repeating the plan.

Acquired Grenfell/Hunt's 1901 Amherst II and Brooke/McLean's 1911 Numbers/
Deuteronomy privately; reused the existing 1906 Genesis preface. The PDF skill
required rendering and visual inspection of the complete relevant pages.
Exact hashes, pages and findings are in the
[Greek review receipt](../sources/textual_restoration/discovery/deut32_8_greek_review.v1.json)
and [pass-4 report](PENTATEUCH_SOURCE_COMPARISON_PASS_4.md).

The Amherst transcription preserves an angel-noun prefix, with the ending
supplied and the following God word unpreserved in that line. This adds a
discriminating published component to the formal comparison, not a newly
deciphered phrase. Its plate was located in a context-informed overview only.
Kraft's comparative anthology hypothesis was consulted and remains qualified.

The Cambridge apparatus reports sons of Israel for p's later correction, with
an uncertainty marker. Its prefatory sigla establish p/106 and the meaning of
the correcting-hand symbol. This conflicts with the earlier consulted Tov
complete-phrase report. The method now explicitly requires joining all relevant
apparatus units for the same hand before claiming a full phrase. Adjacent-word
conflation is a possible explanation, not an established history of the error.
Modern Göttingen and the Ferrara correction have not been directly checked;
the qualified Cambridge reading is not silently upgraded to certain ancient ink.

Access/attempts: the Morgan object page returned 403 to the web tool, so its
search metadata was not treated as a live image inspection. A Birzeit PDF
route failed (web retrieval error and local 403); the Palmer Seminary-hosted
Cambridge scan succeeded. The Amherst web PDF redirect failed but the public
download succeeded locally. One plate preview failed before rendering finished;
the same completed render was subsequently inspected, not regenerated or
mistaken for a lost source. Other search-result apparatus quotations remained
leads, not substitutes for direct consultation.

Changed the existing comparison, pass report, method, TODO, discovery index,
source audit and this log; added one bounded evidence receipt and five tests.
Registry and formal physical-coverage counts remain 26/20, with 13 cases and
one unpromoted selection. No canonical Hebrew, English, notes, selection gates,
About section, commit, deployment or ImageGen evidence changed. The next
consequential action is exact modern apparatus/848 inspection, followed by
the existing Hebrew image and synchronized source/English review gates.

Verification: 183 repository tests plus nine numerical tests passed (192 total).
The five new checks preserve the partial-word boundary, test noun-level
discrimination only, keep the conflicting correction report qualified, prevent
promotion claims and verify the unchanged canonical baseline and formal
comparison link. All 111 local links in the six touched Markdown files resolve.
The three actual private PDFs match their recorded hashes; direct whitespace
and tracked Git diff checks pass. Registry validation remains 26/20/13/1.
These checks establish consistency, not manuscript legibility or historical
priority; no missing primary evidence was inferred from passing tests.

### 2026-09-05 — OHB sample: consultation succeeds; conjecture remains distinct

Question: does the published critical-edition sample resolve the outstanding
Deuteronomy 32:8 Greek attribution or supply a source decision ready for POB?
Consulted the institutional [2008 sample article](https://digitalcommons.unl.edu/classicsfacpub/98/)
by Crawford, Joosten and Ulrich, DOI `10.1163/156853308X302015`, in the normal
browser PDF viewer. Crawford's Deuteronomy main text p. 354, apparatus p. 355
and complete 32:8 commentary paragraph p. 357 were visually read (PDF 4, 5,
7 of the displayed 16 pages). Some introductory and preceding commentary
context was also inspected; neither a full-article reading nor a review of
the Kings/Jeremiah samples is claimed.

Observation: the sample selects `בני אל` while explicitly acknowledging no
extant Hebrew witness for that exact phrase. Its transmission explanation is
an editorial reconstruction. The paragraph uses a Greek phrase without
identifying the disputed 106 hand or individually documenting 848. It does
not settle the conflict recorded in the previous pass.

Decision and counterargument: retain our attested Hebrew-based working
candidate, not a canonical promotion. Include the El conjecture in the
full-verse editorial comparison: a proposed common ancestor may explain the
alternatives, but explanatory appeal must be tested against direct attestation
and non-unique retroversion. This is not an automatic ban on conjecture or an
automatic preference for an edition's main text. No new manuscript or recovered
letter was added. A published scholar's argument is not an independent review
of our project-specific decision and does not satisfy our pending gates.

Access correction: the particular sample is no longer merely an inaccessible
lead. The direct command-line request returned 403 and web PDF retrieval failed,
but the normal institutional URL loaded in the browser. Resetting the UI
session restored the documented control API; no undocumented browser methods,
credential extraction, security bypass or purchase was used. The PDF skill
guided visual inspection of the relevant rendered passages. Download produced
no verified local file; content export was unsupported and asset inventory was
empty. Therefore the receipt uses edition/URL/page provenance with an explicit
null hash, not a claimed acquired PDF. Browser scroll/page-down attempts did not
move the viewport; direct page-number and zoom controls supplied the relevant
readable views. No PDF or screenshot was copied into Git and no redistribution
license is assumed. DJD and exact Göttingen access limits remain unchanged.

Changes: added the [OHB consultation receipt](../sources/textual_restoration/discovery/deut32_8_ohb_review.v1.json)
and four regression tests; updated the pass-4 report, discovery index, method,
TODO and selection's dated open questions. The method now explicitly separates
selected editorial text from manuscript attestations. Existing source choice,
English candidate and all six pending gates remain unchanged. The canonical
Deuteronomy 32:8 file retains SHA-256
`1caf32ddf68b552d662a94cff90970e5eacd9028ac0a4b8c89228634b14702af`.
No About integration, commit, deployment or canonical text/notes change occurred.

Verification: 187 repository tests plus nine numerical tests passed (196 total).
The new checks distinguish conjecture from attestation, prevent fabricated
acquisition provenance or Greek-resolution claims, and verify the unchanged
baseline and pending selection gates. Registry validation remains 26 entries,
20 physical coverage records, 13 cases and one unpromoted selection. These are
consistency checks, not additional evidence for historical priority. Next:
resolve the exact Greek apparatus and 848/106 evidence, complete the Hebrew
image/DJD work, then explicitly adjudicate attested versus conjectural wording
in the synchronized full-verse source/English package.

### 2026-09-05 — Full-record candidate and actual export preflight

The previous goal pass made progress by directly distinguishing the OHB
conjecture from manuscript attestation. This pass advances the application
side of the objective: can the current Deuteronomy working selection be
represented as an explicit source/English/notes draft without inheriting old
approval or silently dropping its disclosure during export?

Inspected the authoritative canonical verse, selection, selection validator,
canonical verse schema, local mobile exporter and existing review/export tools.
No additional ancient source or new lexicon was consulted. Built a bounded
[draft materializer and preflight](APPLICATION_DRAFT_PREFLIGHT_2026-09-05.md),
an explicit edit plan, byte-exact baseline snapshot, full candidate record and
hash-pinned receipt under `sources/textual_restoration/applications/`.
The baseline SHA-256 remains
`1caf32ddf68b552d662a94cff90970e5eacd9028ac0a4b8c89228634b14702af`;
the candidate JSON hash is
`7f7ee48c97c0d8ef54419ba653f075f5a7b40baa784bf9e2d96231dda02f6797`.
The receipt also pins the selection, plan, four research evidence files,
canonical schema, exporter and builder, plus before/after component hashes.

Draft composition is disclosed as unpointed baseline WLC consonants plus the
single proposed Elohim phrase. This is not a full 4Q37 transcription, recovered
pointing or approved earliest text. English changes only the selected referent,
preserves the existing note markers and unrelated note, and updates the affected
textual note and two rationale entries. The conjectural El alternative remains
an explicitly different proposal. Unchanged lexical and theological metadata
was carried forward, not newly certified. The formal selection's full-verse
field remains null and every gate pending: construction and review are distinct.

The draft archives the original `cross_check` and `revision_pass` objects and
uses `needs_review` without inherited agreement scores. The archive is bound
to the observed baseline snapshot, not falsely to an unverified historical
review input. Original AI-draft metadata stays explicitly historical. This
preserves useful provenance without treating earlier approval as portable
across edited source, English and notes. The canonical file itself is untouched.

Observed integration problems: the current schema already rejects the
baseline's `revised` lifecycle status because its enum only permits `draft`.
The candidate's explicit `POB-critical-draft` source label is also unsupported.
These are different failures, not evidence that the draft should be relabeled
WLC or that every existing verse must be changed to draft. The production
critical-source data model still needs a deliberate design.

Ran the real full-book Deuteronomy mobile export against the baseline and
against a one-record in-memory loader overlay. Proposed English survives and
all other exported book content is identical. The output retains note markers
but omits note bodies and the source object. Counterqualification: a lightweight
payload need not contain every source field and another consumer may supply
notes separately; this pass did not inspect a deployed reader or that potential
alternate path. Therefore we do not call the whole publication system broken,
nor do we mark source/notes synchronization verified. The actual disclosure
path must be traced and tested. No bundle or deployment was written.

The builder writes only fixed research outputs, rejects baseline drift and
ambiguous/missing edit targets, preserves a different existing snapshot rather
than overwriting it, and refuses symlink outputs. It has no canonical apply or
approval option. Successful generation is not successful publication readiness;
the receipt explicitly says false and records that an application transaction
is still unimplemented. The new candidate is a concrete object for later review,
not a substitute for the requested reviewed source corpus.

Verification: 200 repository tests plus nine numerical tests passed (209
total), including thirteen new staging/export regression tests. These reproduce
the actual candidate and receipt, verify the byte-exact baseline archive,
exercise the real exporter, reject incorrect edits/generated evidence, and
test snapshot/symlink write guards in temporary fixtures. Registry validation
remains 26/20/13/1; Git diff whitespace checks passed. Early path searches used
nonexistent schema locations or unmatched shell globs; actual file discovery
resolved them without treating missing search output as missing functionality.

Updated the method, TODO, pass-4 report and source index with the draft's exact
role and limits. No canonical Hebrew, English, notes, review flags, formal
selection status, source-schema enum, exporter implementation, About section,
commit, deployment or image evidence changed. Next: finish the source evidence
and independent editorial/English review, design the critical-source record,
trace reader disclosure consumers, and implement the reviewed application
transaction. Broader OT/NT discovery and measured restoration remain open.

### 2026-09-05 — Reader path trace and local footnote-export repair

The previous pass made concrete progress with a full-record candidate and an
observed export failure. This pass traced the disclosure path before changing
it. Read the repository's cross-platform map, publisher/build references and
the actual related repository sources. The project-list tool returned no saved
projects, but the documented repositories were present in the local projects
directory. Six relevant source files are hash-pinned with exact locators in
the [reader-disclosure receipt](../sources/textual_restoration/applications/reader_disclosure_review.v1.json).
No external ancient text, new manuscript image or lexicon was consulted.

Initial code-level finding: the CDN publisher already includes referenced
marker/text note pairs, and native/web reader components accept notes. A deeper
loader check then contradicted the inference that web component support meant
delivery: `cartha.website`'s POB sanitizer strips markers and deletes note arrays
before the renderer. This refinement was explicitly communicated while working.
Static component inspection alone would have missed it.

Executed the actual website filter block (file lines 213-251) in an isolated
Node context with the hash-pinned Deuteronomy candidate. Under `pob`, its two
notes become zero and their markers disappear. Under the `kjv` control key,
the same input retains two notes and unchanged text. This is a conditional
execution probe, not a KJV translation experiment, full web-loader execution,
React render or deployed UI test. The caller was inspected separately. The
read-only probe is reproducible and its actual output exactly matches the
recorded receipt. Node was absent from PATH; the bundled runtime was located
and used without installation. No authentication, publisher/Lambda call,
network payload fetch or deployment was performed.

Implemented the local fix in `tools/export_mobile_bible.py`: canonical OT/NT
book export now shares the verse helper used by Psalms, and that helper retains
referenced note bodies using the already supported marker/text/optional-reason
shape. It normalizes surrounding marker brackets, omits unreferenced archival
or empty/malformed notes, and does not reinterpret manuscript brackets or alter
translation strings. It does not resolve pre-existing duplicate/conflicting
notes. Separate deuterocanonical/extra-canonical paths were not changed or
certified. The final payload normalizer was also inspected and tested for note
preservation; its existing terminology policy was not modified or newly endorsed.

The original failed preflight v1 remains unchanged at SHA-256
`55923eafd0a40491c817360f53fa7551bab886d1f188d9ffb539b2787c5806fa`.
New preflight v2 at
`852d096fc03bb5ae63a3a2080bf743f4285cad883bfc1c1379c74d47b5f7b6b9`
reports preserved note bodies for the actual full-book candidate-overlay run.
The candidate and byte-exact canonical baseline hashes are unchanged. Restoring
the baseline verse in that run makes all other output identical to the new
exporter's baseline output. This does not claim no difference from the old
exporter: adding existing note bodies is the intentional output change.

Decision and contrary consideration: the local missing-data defect is repaired
without inventing a new consumer format. The website's explicit POB-family
stripping policy is a separate issue; its original design intent was not
established and related repository/UI behavior was not changed. Also, a
lightweight reader need not contain the full source object, but an actual
reader-accessible critical-source disclosure must still be verified. Neither
the local fix nor the existence of note components completes publication review.
All selection gates remain pending and the source-schema gap remains open.

Added the [trace report](READER_DISCLOSURE_TRACE_2026-09-05.md), receipt,
isolated probe and eight export tests; updated the draft builder to emit v2,
added a historical-receipt assertion, and updated preflight documentation and
the TODO. Verification: 209 repository tests plus nine numerical tests passed
(218 total). The tests include all thirteen actual comparison baselines,
ordinary OT/NT book branches, Psalm headers, note normalization/non-mutation,
final payload assembly/JSON round trip, and the existing actual Deuteronomy
export probe. All six cross-repository source hashes matched; the isolated
web-filter output reproduced exactly. Registry validation remains 26/20/13/1
and Git diff whitespace checks passed. None of these tests certify historical
wording, independent editorial approval or a running reader.

No canonical Hebrew, English, notes, review flags, formal selection status,
source-schema enum, related-repository file, About section, commit, deployment
or image evidence changed. The local export code is the material implementation
change. Next return to the outstanding manuscript/source adjudication; before
an approved change is published, address the web-loader policy with a scoped
reader implementation and visual verification, then complete the critical-source
representation and hash-bound application transaction.

### 2026-09-05 — Fouad 848: exact plate, partial noun and missing complement

Question: does the actual Fouad witness preserve the complete divine phrase
at Deuteronomy 32:8, as the earlier secondary table appears to imply?

Acquisition first separated Dunand's introduction from the text/plate
publication. The [IFAO catalogue](https://www.ifao.egnet.net/publications/catalogue/3260050221450/)
was readable earlier in the pass, but its later repeat timed out; no PDF route
was established and no purchase was made. An Open Library introduction-volume
record pointed to text/apparatus in *Études de papyrologie* IX, pp. 81–150;
inconsistent dates in discovery listings were not resolved by guessing.
Kraft's [early Jewish LXX observations, section 08](https://ccat.sas.upenn.edu/rak/earlylxx/jewishpap.html)
provided the 848 identity and photographic-edition route, not the decisive
verse reading. Its linked papyrus image returned an image-only web response
and was not visually inspected. No nearby-fragment picture was counted as
32:8 evidence. Catalogue, image locator and transcription are separate results.

The [Bibliographie Papyrologique record 1980-0006](https://bibpap.be/BP_enl/tcPdf/examples/?fsp=1&n=1980-0006)
confirmed Aly/Koenen, *Three Rolls of the Early Septuagint*, PTA 27, Habelt
1980, xiii–143 pages and 57 plates. A user-uploaded Scribd scan offered an
ordinary ad-supported browser preview. The web extraction contained metadata,
not edition text; the browser actually displayed the printed pages after the
offered ad/Skip-ad sequence. No subscription, login, payment, download or
restriction bypass was initiated. The PDF skill required visual inspection
of relevant pages; this was done in the preview, not by inventing local assets.

Verified the scan's imprint/CIP at preview page 5, visible preface at 6,
contents at 10, fragment table at 13 (printed xii), passage table at 14
(xiii), relevant conventions at 38–40 (25–27), complete verse-8 note at 133
(120), and the upper target plate at 134 (plate 46). Only the stated portions
were inspected; this is not a complete book read. The exact page/scope record
is the [Fouad supplement](../sources/textual_restoration/discovery/deut32_8_fouad_review.v1.json).
Initial blank page renders were rechecked after load. One broad scroll jumped
far beyond the intended paragraph and a later stale control index failed;
fresh page controls and ordinary PageDown corrected the navigation. Printed
labels, not an assumed PDF offset, established the final locators.

Observation: the concordance and plate map verse 8 to fragment 177, plate 46,
column 73*, line 4. The asterisk denotes added fragments or another textual
change relative to Dunand, not uncertain ink. The note at p. 120 prints the
sons prefix, normalized `υιω`, with omega doubtful, before the supplied
continuation. It discusses both God and Israel completions. The photographed
fragment's extent and location were inspected after this note, not through
a blind, calibrated letter-reading experiment. No new letters were recovered.

Decision: accept bounded published support for the sons noun against angels,
but **do not count 848 as surviving proof of the following God complement**.
The strongest contrary consideration is that the editor's proposed restoration
and broader evidence may favor God; plausibility does not turn supplied letters
into ink. Nor does this prefix choose exact Hebrew El versus Elohim. This
qualifies the earlier secondary full-phrase report without weakening the
separate published 4Q37 Hebrew observation by association.

The same p. 120 explicitly associates the Israel continuation with
`106[corr.]`. It agrees with the earlier Cambridge report and further challenges
the secondary complete-phrase attribution. It is another editorial report of
the same witness, not another independent manuscript vote. The precise modern
Göttingen apparatus and Ferrara hand remain unread; the origin of the
secondary discrepancy is not fully resolved.

Added the machine-readable supplement and four constraint tests; updated the
pass-4 dossier, source coverage audit, discovery index and TODO. The earlier
Greek receipt and all frozen application inputs/preflight receipts remain
unchanged. This supplement postdates preflight v2's evidence set: that receipt
continues to demonstrate its structural/export experiment, not current scholarly
approval. The next adjudication/application review must incorporate the new
bounded evidence. Canonical Hebrew/English/notes and all selection gates remain
unchanged. No related-repository edits, About integration, commit or deployment.

Verification: 213 repository tests plus nine numerical tests passed (222 total).
Registry validation remains 26 mixed entries / 20 physical coverage records /
13 cases / one unpromoted selection. Git whitespace checks passed. These checks
protect preservation distinctions, physical identifiers, no-invented-acquisition
claims, the canonical hash and pending gates; they do not prove historical
priority or independent palaeographic agreement.

Next: obtain a lawful stable higher-resolution edition/fragment source and
exact modern apparatus; finish 4Q37's DJD/image/genre and independent reviews.
The central log remains the Git-ready history target already linked in README.
Its earlier history is explicitly backfilled and incomplete; record recoverable
evidence and concise decision rationales, not an invented exhaustive transcript.
The proposed About summary remains unpublished until separately requested.

### 2026-09-05 — Isaiah copy-list reconciliation and missing commentary class

The previous Fouad turn was progress: it added source evidence and corrected
the preservation claim. This pass broadened discovery to Isaiah rather than
treating selected disputed verses as the entire source-coverage task.

Question: which explicitly catalogued Isaiah sources are represented in the
pinned biblical QDR file, and which relevant source classes are missed?
Consulted Tov's author-hosted 2008 revised chapter, section 1, PDF pp. 1–2,
including every note on those pages. The PDF skill required rendering and
visual inspection of the list and its counting caveat. Tov lists 21 Qumran
copies and separately Mur 3; note 1 warns that fragment/hand-based manuscript
counts remain revisable. This historical list is not a present exhaustive
census or a newly authenticated set of physical objects.

The author site's HTTPS routes failed (web timeout/safety response, curl
certificate hostname mismatch); its non-www host failed DNS. The ordinary
HTTP URL explicitly given in the author's bibliography succeeded. No TLS
verification was disabled. SHA256 of the acquired 16-page chapter is
`065ca32f3b6eb851ebc96b74dfc62a81dea903c3616b0b78abc0b7482cf5f8f5`.
A hash pins these bytes, not authenticated transport. The unrelated museum
overview's direct request returned 502; Brill's Tov chapter returned 403.
Those failures are access observations, not evidence of manuscript absence.
An initial search named a nonexistent local receipt; `rg --files` located the
actual existing discovery files. `pdftotext` was unavailable, so the bundled
PDF reader extracted navigation text and Poppler rendered the required pages.

Acquired SBL's *Celebrating the Dead Sea Scrolls* (2011) front matter, SHA256
`d056d76a382f4b6d00ebf977504229be92bdd0bbf84e157f996c8554824ee7f7`.
Visually inspected complete printed xviii, xx and xxi / PDF 18, 20 and 21;
title/imprint were extracted from the opening pages. The sigla identify 1Q8
with 1QIsab and preserve the inserted 4Q62a/Isaiah-i mapping. They also name
five cave-4 Isaiah pesharim. The selected abbreviation page omits 4Q68; an
IAA institutional search record supplies its Isaiah-o crosswalk. Unrelated
incorrect book labels in that abbreviation list were not propagated.

IAA records supplied 5Q3, Mur 3, 3Q4 and cave-4 pesher identifiers/publication
routes. Several direct page extractions returned only titles; metadata claims
are explicitly attributed to the fuller institutional search-index records.
The USC West Semitic Research Project's 4Q162 description distinguishes
quoted Isaiah 5 material from its interpretive commentary. Search results for
newer Qumran-Digital pesher transcriptions are next-access leads, not texts
read or collated here. Full consulted URLs and limits are in the
[target specification](../sources/textual_restoration/discovery/isaiah_catalogue_targets.v1.json).

Executed the existing generic reconciler on the real pinned QDR JSON and
primary PDF: all 22 copy-list names have scoped matches in 22 distinct labels,
and six separately classified pesharim (3Q4, 4Q161–165) have no queried labels
in that biblical-only file. The union contains 1,291 distinct Isaiah anchors;
the Great Isaiah label itself has 1,290. These index counts neither establish
complete surviving verses nor prove omissions. There are no unmatched
Isaiah-tagged labels or out-of-query-scope anchor/locator pairs in this screen.

Decision: retain the matched copy-list coverage and add the six commentaries
as a concrete acquisition queue. The contrary consideration is that commentary
can paraphrase, adapt or restore its quoted lemma; it must not be counted as
a continuous Isaiah copy or imported wholesale into the biblical text. Yet
its genre is not a reason to exclude genuinely discriminating preserved
quotations. Absence from this one file does not imply absence from the whole
QDR project or other POB resources. Material labels such as `pap` do not
identify a Greek version.

Added targets, a hash-bound metadata-only receipt, five tests and the
[Isaiah report](ISAIAH_CATALOGUE_RECONCILIATION_2026-09-05.md); updated the
coverage audit, discovery index and TODO. No generic builder/scanner changes
were needed. The builder checks the primary PDF hash; the supplemental SBL
PDF was separately hashed and visually checked, not automatically revalidated
by that command. The prior Leviticus receipt and application inputs remain
unchanged. Full PDFs/renders remain outside Git; no private transcription or
complete verse-to-witness index was republished.

Verification: real-input `--verify-only` reproduced the saved result. The
218 repository tests and nine numerical tests passed (227 total), including
the new role, alias, fingerprint and no-automatic-reading-support assertions.
Registry validation stays 26/20/13/1; Git whitespace checks passed. These
checks establish accounting and evidence boundaries, not ancient readings.
No source or English wording, reader notes, selection gate, production code,
About section, commit or deployment changed.

Next: acquire and segment the pesher lemmas, check updated DJD and later
identity/preservation work, and extend Isaiah's non-DSS/Greek/versional
coverage. Broader quotations and allusions remain outside this 28-name screen.
No completeness claim, ImageGen recovery or new ancient letters resulted.

### 2026-09-05 — consolidated approach assessment and documentation handoff

Request: reassess the work and source choices, improve the approach, and keep
a repository document covering the recoverable history for a later About link.
Reviewed the current method, approach review, OT/NT coverage audit, NT method,
research-log status/history and README link. The worktree already contained
extensive changes and untracked research artifacts; they were preserved.

Rechecked the [IAA archive landing page](https://www.deadseascrolls.org.il/explore-the-archive),
[NTVMR landing page](https://ntvmr.uni-muenster.de/),
[SBLGNT apparatus explanation](https://sblgnt.com/about/introduction/apparatus/)
and [INTF CBGM description](https://www.uni-muenster.de/INTF/en/forschung/cbgm/index.html).
These confirm the distinction between discovery resources, edition comparison
and passage-level reconstruction. No new witness census, book apparatus or
edition-release audit was completed in this pass; prior release statements
retain their dated consultation basis. INTF's summary supports distinguishing
an inferred initial text from an extant autograph; it does not validate any
particular POB selection.

Assessment: retain the evidence-linked framework, but prevent catalogue counts
from standing in for adjudication or translation results. Added a current
assessment above the older snapshot in the approach review and an explicit
translation-evaluation contract in the controlling method. The contract
requires stated defects and tradeoffs, actual review records, and a frozen
sample including unflagged passages before corpus-wide superiority claims.
The strongest counter-consideration is that exhaustive image work would stall
useful published-text and English-only improvements; therefore those tracks
can proceed separately without waiving existing case-specific gates.

The interrupted Isaiah follow-up remains unfinished. Its carried-forward notes
report a preliminary 4Q164 quotation/commentary-boundary check, not a completed
collation or newly read image. A fresh request for the
[2026-05-21 transcription](https://lexicon.qumran-digital.org/transcriptions/4Q164/2026-05-21/index.html)
returned a non-retryable web safety/access error in this pass; no bypass was
attempted. Earlier source observations need their own completed dossier before
promotion. Directly reread Isaiah 54:11–12 YAML: note markers remain misplaced
(54:11 a/b belong to sapphires/antimony; 54:12 b/d belong to pinnacles/boundary
walls). This documents a pending repair, not a completed edit or a newly
verified gemstone interpretation. The earlier exact-reference extraction
attempt using `Isa` rather than the stored `Is` is an index-query mismatch,
not evidence that the physical text is absent.

Changed only this log and the existing approach/method documents. Added a
navigation section; kept the README's existing log link and unpublished About
draft. No source/English/notes, registry, frozen application input, production
code, About page, commit or deployment was changed by this documentation pass.
Verification: registry validation confirmed 26 mixed entries / 20 coverage
records / 13 comparison cases / one selection. The 74 targeted registry,
Isaiah-catalogue, application-draft and reader-footnote tests passed; 111 local
Markdown file-link targets resolved; `git diff --check` passed. This was not
a rerun of the entire prior 227-test suite or a validation of ancient readings.
Next deliverables: finish the bounded Isaiah check and marker repair, complete one reviewed
application dossier, expand dated book-level source coverage, and execute
calibration before broad machine-reading acceptance.

### 2026-09-05 — Isaiah 54 pesher comparison and preservation-context safeguard

Previous turn classification: progress. It updated the authoritative method
and research documentation, with the Isaiah investigation explicitly pending.
This pass resumed that investigation and completed a bounded published-text
comparison plus reader-note repair; the larger source/restoration goal remains
active and incomplete.

Read Qumran-Digital's 4Q164 releases 2025-08-25 and 2026-02-11, then followed
its version list to the latest listed 2026-05-21 release. Inspected frg. 1
lines 1–7 and the source/licence statement. Direct requests initially produced
internal/safety errors; ordinary page links subsequently worked, without any
access-control bypass. Direct Great Isaiah web access still failed, so that
control uses the existing private QDR published transcription. Full sources
and exact locators are in the [Isaiah 54 report](ISAIAH_54_PESHER_REVIEW_2026-09-05.md)
and [receipt](../sources/textual_restoration/discovery/isaiah54_pesher_review.v1.json).

Observation: 4Q164's published quotation tail has an extra quantifier before
the architectural term, followed by an explicit commentary marker. The prior
clause is supplied; the subsequent interpretation is not biblical source
wording. WLC and the pinned Great Isaiah control lack that quantifier at this
position. Full 4Q57 frg. 44–47 line 4 and 4Q69a frg. 1 line 3 were read in
their 2026-02-11 editions: neither gap establishes surviving omission. The
former preserves the architectural term but loses the preceding wording;
the latter supplies the relevant clause. No primary image or full DJD/critical
apparatus was inspected. The 4Q164 stone word in verse 11 also has a supplied
ending, so it cannot be reported as a complete newly recovered reading.

Decision: retain current source and English provisionally. The strongest
argument for expansion is a discriminating Hebrew quotation; the strongest
counterargument is adaptation in a pesher with a contrary continuous-copy
control. Source priority, exact lexical meaning and commentary interpretation
are different questions. The new reading lead is not promoted or added as an
extra formal registry case. No novel ink or ImageGen-based evidence resulted.

Executed exact `Is 54:11` / `Is 54:12` extraction on the hash-verified QDR file:
four labels at the former and three at the latter. These overlap and are not
seven independent witnesses. The earlier `Isa` spelling caused empty exact
queries, not manuscript absence. Crucially, 4Q69a's opening supply bracket is
attached to verse 11 on the same physical line; a verse-12-only extraction
drops it. Added opt-in `--include-line-context`, with original word positions
and an explicit unassessed-preservation warning. Default output is unchanged;
cross-line supply still requires edition inspection. A synthetic regression
fixture checks the bracket hazard without republishing a restricted line.
Executed the new option on real input and confirmed the missing opening bracket
is visible in full-line context.

Repaired only note-marker positions in Isaiah 54:11–12: gemstone notes now
attach to their gemstones, and the architectural/boundary alternatives attach
to their actual terms. The receipt stores old/new English strings and file
hashes; tests reverse the replacement to reproduce each old file byte-for-byte.
All source text, unmarked English wording, note bodies and historical review
metadata remain unchanged. Those old reviews are not new approval of this
edit. Local export checks preserve all six notes; deployed disclosure remains
a separate unresolved check.

Added the bounded report, receipt and seven tests; updated the discovery index,
Isaiah catalogue follow-up, source coverage audit, controlling method, TODO
and this log. The full private corpus stays outside Git. No frozen application
inputs, selection gates, registry counts, About section, commit or deployment
changed. Verification: 225 repository tests plus nine numerical tests passed
(234 total). Registry validation remains 26 mixed entries / 20 coverage
records / 13 cases / one unpromoted selection. All 96 checked local Markdown
file-link targets resolve; Git whitespace checks passed. Tests verify accounting,
reversible marker changes, export behavior and context retention, not manuscript
legibility, historical priority or new independent review.
An actual full Isaiah book export also retained the corrected anchors and all
two/four notes at 54:11/12; no payload was saved for publication or deployed.
Next: full 4Q164 edition/reassessment and image mapping, Hebrew/Greek apparatus,
discriminating versions and separate lexical review; continue the other pesher
and book-coverage work without treating this narrow result as comprehensive.

### 2026-09-05 — Isaiah 54 versional and Hebrew lexical controls

Previous pass: progress, with published pesher comparison, context safeguard
and verified marker repairs. This pass asks whether other versions decide the
extra quantifier or justify changing POB's architectural word. Consulted the
existing unchanged OpenScriptorium checkout and pinned Isaiah JSON, surfaces
at 54:11–13; its SHA256 is
`c60980806a91bfde385004f5bbc030268f95803503527224ba760330390bed56`.
No morphology/model-rationale field was treated as ancient evidence. No matching
Isaiah 54 Greek transcription was found in the local Swete text search; its
manifest/README were inspected, not a Swete page or apparatus.

Followed CAL's Peshitta and Targum browsers to Isaiah chapter 54, reading target
verses 11–13, book source information and selected lexical analyses. Peshitta
62012 is Leiden-derived with selected 7a1 corrections. Targum Jonathan 51012
text 1 is HaKeter/Bar Ilan-derived, with separately numbered Sperber variants
and toseftot. Text numbers and automatically converted pointing are not merged
into a hypothetical ancient manuscript. CAL's AI links were not used as
evidence. These are dynamic consultation records without invented page hashes
or full-corpus imports. Exact sources and locators are in the
[versional supplement](../sources/textual_restoration/discovery/isaiah54_versions_review.v1.json)
and the appended [Isaiah report](ISAIAH_54_PESHER_REVIEW_2026-09-05.md#greek-syriac-and-targum-follow-up--2026-09-05).

Observation: the Greek and Syriac lack both the proposed extra quantifier and
the later boundary quantifier actually present in WLC. Both express the next
verse's children quantifier. This local contrast prevents overclaiming that
their silence uniquely establishes Hebrew absence; it is not a measured
whole-book omission tendency. Targum text 1 retains the boundary quantifier
but gives a different architectural interpretation. Greek battlements, Syriac
walls and Targum woodwork are not one uniform ancient definition. Shared Greek
and Syriac gemstone vocabulary makes dependence worth checking but does not
prove it; neither related editions nor versions become extra Hebrew votes.

Checked LSJ's Greek defensive senses and CAL's Syriac wall/stone and Aramaic
wood analyses. The Sefaria HTML root page gave no entry text; the official
documented read-only lexicon API succeeded by ordinary curl after web-tool
failure. Selected BDB Dictionary record BDB10425, sense 5, with its actual
Oxford 1906 attribution, rather than the separately returned augmented Strong
record. The first multi-entry output was truncated; a filtered request exposed
the complete relevant sense. BDB permits both pinnacles and battlements here.
No HALOT, DCH or full Hebrew critical apparatus was newly consulted.

Decision: retain the current wording and alternative note. Battlements may
better convey defensive structure; pinnacles may suggest pointed ornament.
But the Hebrew lexical control allows both and the versions are non-uniform.
This is a documented tradeoff, not a demonstrated correction. Do not import
Greek/Syriac gemstone identifications automatically or claim that modern
mineral names resolve ancient lexical uncertainty. Historical quantifier
priority remains open; unchanged English is an evidence-based outcome here.

Registered CAL Targum Isaiah as a modern transcription, extending existing
Greek and Peshitta coverage. Current accounting is 27 mixed registry entries,
20 physical coverage records, 13 formal comparison cases and one unpromoted
selection. Added the supplement and five tests; updated the existing Isaiah
report, discovery index, source audit, current-count summaries and TODO.
Canonical Isaiah hashes still match the previous marker-only repair. No
source, English, notes, canonical metadata, application input/gate, About section,
commit, deployment or generated image changed in this pass. Verification:
230 repository tests and nine numerical tests passed (239 total); registry
validation passed at 27/20/13/1. The Greek excerpt exactly reproduced from the
hash-pinned real input, 105 local Markdown file-link targets resolved and Git
whitespace checks passed. These are accounting and regression checks, not proof
of ancient readings or independent adjudication. Access failures also included a BiblIndex
403 and guessed CAL routes; ordinary documented navigation supplied usable
CAL pages. Search snippets were leads, not substitutes for the pinned Greek.

Next: consult full book apparatuses and physical witnesses, assess versional
translation practice and the Hebrew lexical alternatives in paragraph context,
and continue systematic coverage beyond this passage. These three version
controls do not complete the Isaiah source census or the wider restoration goal.

### 2026-09-05 — Isaiah 54 printed Greek apparatus and edition identity

Question: does a printed Greek edition with manuscript-attributed apparatus
change the quantifier or architectural assessment? Reacquired the volume III
PDF linked in the existing Swete manifest. The initial 180-second download
timed out after 43,777,760 bytes; a range-resume completed the same file.
Its 57,077,650 bytes and SHA256
`5f0bfffabf0e588fd32e15bdb24b027872616da219e7f02da3dbdc115cf97d85`
match the prior manifest. The scan stays outside Git; the stable acquisition
URL and exact page mapping are in the
[receipt](../sources/textual_restoration/discovery/isaiah54_swete_review.v1.json).

Used the PDF skill: pypdf OCR navigated the 932-page file, and complete pages
were rendered and visually inspected, with the target also viewed at original
resolution. Consulted PDF pages 7–10, 12–14, 24 and 226: title, edition history,
base-text explanation, relevant manuscript conventions, sigla and the target
page. Printed p. 202 = one-based PDF p. 226. Title/imprint establish volume III,
third edition, Cambridge 1905. Corrected the former 1909–1930 blanket date in
the Swete README/manifest and specified the consulted edition in the registry.
Volumes I/II were not newly inspected. The old acquisition rationale is marked
historical and linked to the updated Rahlfs record, not presented as a fresh
exhaustive licensing assessment.

Observation: verse 12 lexically agrees with the pinned Rahlfs control, including
absence of both architectural and boundary quantifiers; verse 13 expresses
the children quantifier. Raw-string equality initially failed a test: Swete
prints the final adjective with acute, the digital control with grave. Both
source forms are retained and the test now checks the explicit difference.
The selected verse-12 apparatus reports architecture/jasper/crystal spelling
loci, including a correction label and a `vid` qualification. No added “all”
is reported at the disputed architecture or boundary loci. This records the
edition's reports, not freshly read ancient hands. Full manuscript strings
are not inferred from its selected apparatus.

The page has B as base and א/A/Q in its apparatus margin. The introduction
distinguishes Marchalianus corrections and Hexaplaric annotations from text.
Its explicit warning about undecipherable Cryptoferratensis Γ makes silence
unsafe as an agreement vote; OCR calls this siglum F, corrected against the
scan. Γ is not among the target apparatus margin sigla, so no target omission
vote is assigned to it. These are specific examples of the controlling method's
edition/manuscript, hand and passage-coverage distinctions.

Decision: retain POB provisionally. Bounded printed Greek corroboration improves
provenance but is not another independent ancient witness or universal Greek
agreement. Counterargument remains: Greek's translation practice could explain
absence, and the old selective apparatus is not a complete modern census.
The pesher's historical priority and Hebrew lexical alternatives remain open.
Verified Ziegler's *Isaias*, Göttingen XIV, third edition (1983), in the
[institutional publication list](https://septuaginta.uni-goettingen.de/publications/septuaginta/).
That is bibliographic consultation only; the full Isaiah 54 apparatus remains
unread. Archive metadata and a Cambridge introduction summary were research
leads; the actual scan controls edition identity and the reported readings.

Added the Swete receipt and four tests; appended the existing Isaiah report;
updated the discovery index, source audit, Swete documentation, registry and
TODO. No canonical source, English, notes or metadata, frozen application
input, review gate, About section, commit or deployment changed. Final
verification: 234 repository tests plus nine numerical tests passed (243 total).
Registry validation remains 27 mixed entries / 20 physical coverage records /
13 formal cases / one unpromoted selection. All 127 checked local Markdown
file-link targets resolve and Git whitespace checks passed. These checks
protect record consistency and unchanged files, not manuscript legibility or
independent historical adjudication. Next: full modern apparatus, direct
manuscript/hand checks and pesher priority, while retaining the wider all-book
coverage and real-image calibration backlog.

### 2026-09-05 — Parallel catalogue reconciliation, English sample and judge loop

The user explicitly authorized parallel task agents and an independent judge
with repair/re-review cycles. Ran three bounded subtasks: catalogue index
reconciliation, an unflagged English-fidelity sample, and a fresh-context
judge. This is separate-agent review using the same configured model, not
different-model replication, blind transcription or human peer review. The
[review record](INDEPENDENT_RESEARCH_REVIEW_2026-09-05.md) preserves actual
failures, repairs, final verdicts and gates that did not pass.

**Catalogue question:** what does the current whole Qumran-Digital index add
to the existing QDR screen? Consulted the actual index, its CSS classification
and FAQ; pinned HTML SHA256
`e1211f26d0c37ac46bc7c8cdb23587393742abaef80fcce001bb8b90752683f5`.
The raw 216,543-byte index is retained outside Git in the task's
`research_sources/qumran-digital-index-2026-09-05.html`. The
[report](QUMRAN_DIGITAL_CATALOGUE_INDEX_RECONCILIATION_2026-09-05.md) and
[receipt](../sources/textual_restoration/discovery/qumran_digital_catalogue_index.v1.json)
pin source URLs and comparisons. This is metadata inspection, not consultation
of all linked transcriptions or a census of every extant biblical manuscript.

There are 1,173 index entries: 263 styled biblical, 866 other DSS and 44
non-DSS. Within the biblical class, 231 match QDR labels exactly, 19 match
only under conservative typography normalization and 13 remain unmatched.
Across the entire index, 237 of QDR's 265 distinct labels match exactly,
19 are typography candidates and nine remain unmatched. Six exact matches
fall outside the biblical CSS class; the receipt retains these rather than
treating website genre as physical identity. QDR has 266 records because
one label occurs twice. The exported reconciliation has 269 rows, not 269
independent manuscripts. QDR and Qumran-Digital share transcription lineage;
agreement cannot automatically count as independent ancient attestation.

The judge found three parser failures despite the original tests passing:
a changed row container could silently lose a record, blank URL query values
could evade validation, and an unclosed superscript could be accepted. The
implementation agent tightened observed nesting and query validation, added
three regression tests, and reproduced the unchanged receipt. The judge
independently reran the failures, all 13 parser tests and full input accounting:
fail → repaired → bounded pass. This illustrates why test success alone does
not close a review gate.

The parent investigated two discrepancy leads. XAmos's explicit Tov-2014
label and passage support a bibliographic crosswalk, not authenticated
physical identity. A published authenticity challenge prompted a research
hold, not a finding of laboratory-proven forgery or an actual retraction.
The [hold record](../sources/textual_restoration/discovery/catalogue_identity_holds.v1.json)
links the actual transcription, publication abstract and challenge, and
distinguishes an owner defense reported there from a newly read owner statement.
The owner pages returned verification/loading failure or timeout; no bypass
was attempted. XLeviticus/Arugleviticus remains an identity candidate based
on the earlier passage dossier and newly consulted publication metadata;
the full edition and physical alias were not verified. It must not be merged
with En-Gedi. These are documented holds, not implemented ingestion filters;
raw discrepancy counts remain unchanged. The judge subsequently checked the
integrated holds against the named primary sources and passed their bounded
reporting claims.

**English question:** does source-based review find gains away from already
flagged variant cases? The implementation agent wrote a
[predeclaration](UNFLAGGED_ENGLISH_SAMPLE_PREDECLARATION_2026-09-05.md), then
executed a fixed-seed, one-verse-per-Tanakh-division selection. Static files
do not independently prove the timing of predeclaration. Out of 23,264 OT
files, 16,423 met the operational screen and 6,841 were excluded. The frozen
sample is Numbers 22:19, 2 Samuel 20:6 and Proverbs 24:5. Current Hebrew,
POB and prior metadata were visible: this was unblinded and not a historical
held-out sample. “Unflagged” is a local metadata filter, not proof that no
ancient variants exist. The
[report](UNFLAGGED_ENGLISH_SAMPLE_2026-09-05.md) links exact selection/review
receipts, source and protocol hashes, and all 101 chapter-context file hashes.

Read the selected chapters and pinned WLC/OSHB controls; actually consulted
the publisher's NET notes and the specified electronic BDB entries. Existing
HALOT labels were not treated as new consultations. A requested BDB lookup
for אמץ returned no entry; full modern critical apparatuses and directly
collated ancient versions remain absent from this small pass. Outcomes:
two retain/tie judgments, one unresolved whole verse, zero established semantic
improvements. “You too” does not demonstrate a gain over “you also”; “wise
warrior” may clarify the military context while narrowing a broader Hebrew
subject. Samuel's verbal aspect and final eye/sight expression prevent a
whole-verse fidelity approval. These negative/uncertain results are retained,
not replaced by more favorable draws.

Proposed separately: two misplaced note anchors, a less overconfident Samuel
note and “pursue after him” → “pursue him” for readability. None was applied.
The judge required a future Samuel note repair to synchronize the current
lexical entry's Hebrew spelling and explanation while preserving historical
review prose. Applying any change must retain the frozen baseline and create
a new before/after application receipt; do not rewrite sample history to make
current-input tests pass. The judge passed the selection/reporting contract
and four tests, not the correctness of every interpretive judgment.

**Review of previous work:** the judge independently checked the named Isaiah
published preservation controls, hash-pinned Greek excerpt and all nine
previously cited Swete PDF pages. Initial inability to inspect the scan was
recorded as inconclusive before direct inspection produced a bounded pass.
CAL was not independently verified. Whole-corpus restoration and superior
translation remain unestablished. Publication readiness remains failed due
to the known schema/application/review-binding and website-disclosure gaps.
Historical YAML agreement labels and nonempty cross-check metadata are not
current, hash-bound approval of edited text.

Added the two agent reports and predeclaration, parser/selector tools, 17
tests, three machine receipts, identity holds and independent-review record;
updated the discovery index, coverage audit, TODO and this log. No canonical
source, English, notes or metadata, frozen application candidate, About page,
commit or deployment changed during this batch. Final observed verification:
251 repository tests plus nine numerical tests passed (260 total); actual
index reproduction passed; registry remains 27 mixed entries / 20 physical
coverage records / 13 formal cases / one unpromoted selection. All 50 changed
JSON files parsed and 442 local Markdown link targets in changed/new documents
resolved. The initial link-check command could not find Node on PATH; the
bundled runtime completed it successfully. Git whitespace checks passed.
These validate record consistency, not ancient authenticity,
image-recovery accuracy or corpus-wide improvement.

Next gates: resolve the 13 index-side and nine QDR-side gaps and 19 typography
candidates with institutional identifiers and edition/image locators; do not
automatically promote aliases or disputed fragments. Continue the frozen
English-review program and focused Samuel grammar/apparatus work. Complete
a separately reviewed application transaction and real-image calibration.
Expand NT manuscript/hand coverage explicitly; this OT batch does not advance
an all-NT-comparison claim. Continue fail/repair/re-review on concrete bounded
deliverables, leaving unavailable or undecidable evidence open rather than
relaxing the pass criterion.

### 2026-09-05 — Identity conflicts, Greek targets and wider measured rendering

Previous goal turn classification: **progress**. It changed authoritative
research records, exposed specific source gaps and completed an actual
parser fail/repair/re-review cycle. This continuation reused the three
authorized agents for bounded identity research, measured-renderer testing
and independent review while the parent extended Greek source discovery.
No task or live calculation was restarted merely because observation expired.

**Identity research:** the
[follow-up](QUMRAN_CATALOGUE_IDENTITY_FOLLOWUP_2026-09-05.md) compares pinned QDR
records with actual versioned Qumran-Digital pages and publication records.
An important result changes the next action: exact `4Q8a`/`4Q8b` labels are
not safe cross-project joins. Four content/locator correspondences now show
where those differently named records overlap. That is not proof that physical
fragments should be merged. A title indexed at a biblical reference also
cannot become continuous verse evidence.

Reciprocal 4Q54b/4Q69c locators identify a double-counting hazard under
alternative book assignments. A named 2023 publication challenges 4Q54a/4Q47a
assignment, but its full subscriber-only argument was not consulted. The
publication title is a reason to hold promotion and obtain the paper, not
proof that the reassignment is correct. The two 4Q483 records have distinct
ordinals, hashes and line extents, with a published-line offset and supplied
context problem: neither deletion as duplicate bytes nor counting two objects
is justified. A publisher abstract independently establishes scholarly use
of the 4Q103a designation without resolving its exact fragment assignment.
The receipt pins 14 acquired HTML pages and eight local QDR records; private
source files remain outside Git. All eight new tests ran without skips in
this environment. The judge independently checked the named sources, local
records and reciprocal locators and passed bounded reporting. No raw earlier
catalogue count was rewritten as a resolved physical-manuscript count.

**Greek discovery:** the parent read actual rendered IAA metadata for 4Q119,
4Q121, 4Q122, 7Q1 and 7Q2 after basic web extraction returned only shells.
Read all image links for three records and explicitly only the first twelve
for the two longer lists. An institutional image listing supplies candidates,
not inspected pixels. The [Greek report](JUDEAN_GREEK_SOURCE_FOLLOWUP_2026-09-05.md)
and receipt distinguish IAA identities, Kraft's scholarly-survey aliases and
chapter leads, bibliographic DJD targets and unverified image regions.
Registered four individual Greek comparison targets, with source-specific
language, dating basis, rights and next actions. 7Q2 stays an adjacent
Letter of Jeremiah lead rather than canonical Jeremiah attestation.
Paraphrase/unidentified candidates remain separately classified.

Direct consultation of the current rendered Göttingen Ra 943 record exposed
a competing physical-grouping interpretation. Corrected our registry's former
forced same-object instruction and annotated the earlier report; the existing
ID remains an umbrella, not an object-count decision. This affects how future
evidence is grouped, not a current Greek or Hebrew reading. Neither a shared
catalogue ID nor a new fragment announcement supplies automatic independence.

The PDF skill was read before attempting Tov's author-hosted survey. Web
retrieval failed, curl rejected a hostname/certificate mismatch and the
non-www hostname failed DNS. No TLS checks were disabled and no PDF was read
or hashed. Publisher metadata located the chapter but did not supply its
argument. Guessed padded Göttingen routes and Trismegistos routes failed;
no missing-object claim follows. Accessible institutional browser records
and Kraft's HTML supplied the recorded evidence instead. No unauthorized
image downloads, full-corpus copying or authentication bypass occurred.

**Measured restoration experiment:** the agent froze a 288-target protocol
before inspecting new texture values; the judge reviewed that protocol before
results. Its hash is
`52b6f6235f45c17391b3a6f1c9259e113991cb6b155c6b8485355924a2858a4e`.
The [wider renderer report](EN_GEDI_WIDER_RENDERER_CHECK_2026-09-05.md) records
selection geometry, the availability-informed band, masks, coordinate/index
conventions, all eight prior candidate methods, unfitted exact-match criterion,
every signed residual and missing neighborhood. No replacement targets or
parameter fitting followed inspection. Only merge5 and six existing CT slices
were locally available; no new acquisition or second-segment check occurred.

Of 288 targets, 151 are mask-invalid and 137 valid. The prior favored
radius-7/direct-index/historical-corner emulator exactly predicts nine new
available values across three columns and five rows; its other 128 valid
targets lack required measurements. All distant-row points remain unevaluable.
Across candidates, 15 points can be evaluated and seven are common to all
eight; candidate summaries distinguish these denominators. The alternatives'
nonzero errors and point-level ties remain in the receipt. The historical
corner behavior is retained explicitly rather than silently replaced with
ordinary trilinear interpolation. The emulator is not a claim to reproduce
every historical compiler/build.

The judge independently implemented scalar sampling against the six actual
CT slices, reproducing all 88 evaluable candidate predictions without the
shared interpolation functions. It also reproduced the complete new and old
receipts from pinned inputs. Bounded execution/reporting passed; full spatial
validation remains incomplete/inconclusive. No ancient-letter label was
recovered or scored. These results inform measurement-pipeline work, not
translation selection or an ImageGen-based restoration claim. Static protocol
files alone do not independently prove predeclaration timing.

**Integration and checks:** added the identity and Greek reports/receipts,
wider-renderer report/protocol/receipt/tool, and nineteen tests across the
three tasks; updated the registry, coverage audit, approach review, discovery
index, earlier non-Qumran report, TODO and this log. No canonical source,
English, reader note, lexical metadata, frozen English sample or application
candidate changed. No About integration, commit, deployment or generated
image occurred. Observed 264 repository tests and 15 numerical tests passed
(279 total), with no skips reported. Parent actual-data reproduction verified
both wider and prior nine-point renderer receipts. Registry validation now
reports 31 mixed entries / 20 passage-coverage records / 13 formal cases /
one unpromoted selection. These checks establish consistency and bounded
numerical reproducibility, not authenticity or translation superiority.

The judge subsequently independently opened the five IAA records, Ra 943,
Kraft's relevant sections and classification controls in its own browser;
the Greek metadata and final integrated scope received a bounded pass. No
new concrete failure was found in this batch. Physical identities, full
editions and image collation remain open; publication readiness still fails.
The parent retained an identical copy of the fourteen identity source pages
under the task's `research_sources/catalogue-identity-2026-09-05/` and
reran all eight identity tests against that copy successfully. Nothing was
deleted from the original private snapshot directory.
Final documentation checks parsed 54 changed JSON files, resolved 465 local
Markdown link targets and passed Git whitespace validation. They do not test
remote-link availability or historical conclusions.

Next: acquire/inspect the named reassignment arguments and physical locators,
collate the Greek fragments rather than treating catalogue metadata as text,
and plan a bounded additional measurement acquisition based on the explicit
missing-neighborhood list. Whole-height and multi-segment tests must remain
open until those actual measurements exist. A two-family real-damage letter
benchmark, all-book source census, NT manuscript expansion and reviewed
source/English application package remain outstanding. Unavailable evidence
is not converted into a pass to finish the judge loop.

### 2026-09-05 — Distant measured rows, actual 4Q119 Greek and reviewed note application

**Progress classification:** the preceding identity/Greek-catalogue/wider-sample
turn made bounded progress; it did not complete the restoration goal. This
continuation kept two implementation agents and a separate read-only judge,
with the parent performing acquisition, numerical work and integration. This
is separate-agent checking, not human peer review or different-model-family
validation. The judge's pass applies only to its stated checks.

**4Q119:** the [clause dossier](4Q119_LEVITICUS_26_12_REVIEW_2026-09-05.md)
advances a catalogue target to published Greek at Lev 26:12. Himbaza 2020's
table prints μοι εθνος without brackets; Wevers 2005's detailed discussion
prints μοι εθν[ος and reports μοι clear. Thus the ending must remain supplied,
even though the stem supports a noun different from the Rahlfs-derived
μου λαός. The agent and judge separately rendered and read all seven relevant
PDF pages. Full source locators, hashes, current three-verse POB/Greek context
and the normalized closing-bracket convention are recorded in the dossier.

Himbaza argues for ethnos as earlier; Wevers finds usage inconclusive and
retains Rahlfs. Both nouns can represent Hebrew עם. Our bounded conclusion
is to retain POB's Hebrew עם and “my people,” not force a Hebrew גוי
retroversion or declare the earliest Greek recovered. The opening-clause
omission/transposition question remains separate. The dossier repaired an
ambiguous chronology phrase to “Wevers' 2005 discussion.” A plate28 versus
XXXVIII locator discrepancy remains unresolved; DJD IX, ancient photographs,
the full Göttingen apparatus and NT quotation witnesses were not inspected.
The publisher download extractor failed, but the direct publisher PDF worked
and the local copy was hash-verified; no access protection was bypassed.
Seven focused tests passed without skips and the judge gave a bounded
evidence/preservation pass. No canonical or registry changes arose from this
comparison. A misplaced Lev 26:12 note anchor was added to the backlog only.

**Measured En-Gedi expansion:** the [distant-row dossier](EN_GEDI_DISTANT_ROWS_CHECK_2026-09-05.md)
records a protocol frozen and independently inspected before new intensities.
For each nonempty whole-height row in the previous 288-target sample, select
the mask-valid point nearest x984, ties toward smaller x. Six anchors at
y419/839/1258/2098/2517/2937 require 36 new slices across all eight unchanged
candidate methods. Selection uses existing geometry/availability, not unseen
intensities. It is centered and availability-informed, not a blind random sample.

The frozen ZIP index and strong ETag were checked against bounded HTTP ranges;
all selected member offsets, sizes, CRCs, lengths and SHA256 hashes were
verified. Payload totals were 31,703,069 compressed / 141,329,016 expanded bytes,
within the declared 32/144 MiB caps; logged HTTP response bytes were 32,477,915.
An initial index inspection encountered Apple metadata filenames; requiring a
numeric TIFF stem separated these from actual CT slices. The full 3.87 GB ZIP
was not downloaded or checksum-verified. All 36 new CT slices remain private
outside Git under the dataset's declared CC BY-NC 4.0 terms. They are
reconstructed CT slices, not raw X-ray projections or generated imagery.

Reproducing the frozen older receipt and re-evaluating all 288 targets with
42 total slices yields 151 invalid / 137 valid targets, 27 points evaluable
by any method, 14 common to all eight, and 164 candidate predictions. The
unchanged radius7/direct-index/historical-corner candidate matches 19/19
evaluated values exactly, ten newly available across six distant rows; 118
valid targets still lack measurements. Six acquisition anchors and four
neighbors became evaluable under the all-original-target rule; none replaced
a failure. Every other candidate fails its observed exact-match gate. All
eight full spatial scopes remain incomplete, which must not conceal observed
nonzero errors. The complete signed residuals and different denominators
remain in the machine receipt, not only a favorable summary statistic.

The judge independently recomputed all 164 predictions with a scalar sampler
that did not import the shared sampling functions, including maximizing
offsets and sample counts. Five focused tests, actual old/new receipt
reproduction and report scope received a bounded pass. The parent observed
20 numerical tests pass. Prior code/receipts were not rewritten. This adds
distant-row numerical support but no lateral completeness, second segment,
historical-compiler universality, letter labels or reading-accuracy result.
No canonical source or English was changed by this experiment. ImageGen was
not used and remains illustration-only, never evidentiary input.

**Numbers note package:** the [bounded application dossier](NUMBERS_22_19_NOTE_APPLICATION_2026-09-05.md)
preserves the exact NUM22:19 baseline and candidate, component hashes,
historical review objects, old preflight and corrected preflight. The sole
note anchor moves from “tonight” to the final speech clause, and its note
uses “Yahweh” instead of “the LORD.” Hebrew, marker-stripped main English,
lexical/theological decisions and original draft metadata are unchanged.
Old agreement flags are archived as history with unverified original input
bindings; current state becomes draft/needs_review, not whole-verse approved.
The unchanged schema accepts this candidate; the baseline's existing revised
status error is retained in the record. This does not repair the separate
critical-source schema/publication gaps.

The judge found a concrete P2 failure before application: the historical
sample overlay checked only two of six frozen protocol inputs, so a simulated
controlling-method change still produced a success claim. Application stopped.
The repair pins original selection/review bytes, checks all six inputs and
compares the complete reconstructed selection. Six drift injections and the
judge's original reproduction now reject changes. V1 preflight remains
unchanged; v2 and the exact executor were independently reproduced and hashed.
Thirteen focused tests passed before the judge authorized only the exact
candidate's local note application. The parent recorded the judge-authored
JSON verbatim and separately checked its candidate/executor/preflight hashes.

The application then persisted intent, used a cooperative package lock and
expected-byte atomic single-file replacement, and wrote an applied-verified
receipt after actual post-application checks. These operations are not a
multi-file atomic ledger or protection against noncooperating writers. Final
canonical SHA256 is
`eee7a776befc2a210c8f5ca9e2a35cda3c93ae1ed7a4d90436dfe8ce5b608a77`.
The real full Numbers exporter produced 36 chapters / 1,289 records with the
approved anchor/note and no other book-content differences. The original
sample selector, selection/review receipts and protocol remain byte-exact;
a narrowly guarded overlay reproduces the old selection and all 101 context
bindings without accepting unknown corpus drift. The new corpus digest is
recorded separately, not called identical to the old corpus. Note usefulness
remains an editorial question; this is not a new semantic-improvement rate,
fresh manuscript adjudication or authorization to deploy. Samuel candidates
and the separately identified Leviticus marker remain unapplied.

**Method implications:** detailed preservation checks override flattened
synoptic displays; Greek lexical differences do not automatically require
different Hebrew; model failures, missing measurements and untested reading
accuracy need distinct statuses. Continue toward defensible source/English
decisions with recorded alternatives and abstentions, not forced harmonization
of every witness into a single supposedly certain original. These refinements
are linked in the approach review, source index and TODO. The source registry
remains a partial census; this batch does not expand NT manuscript coverage.

**Final checks:** the judge independently verified the applied Numbers bytes,
intent/final receipt, fresh complete preflight and actual export; its seventeen
post-application application/sample tests passed. Post-application bounded
PASS leaves whole-verse/publication gates unapproved. The parent observed
284 repository tests and 20 numerical tests pass (304 distinct tests total),
plus registry validation at 31 mixed entries / 20 passage records / 13 formal
cases / one unpromoted selection. No commit, About-page integration, deployment
or generated image occurred. Full licensed source/CT payloads remain outside
Git. The research log is an in-repository working document, not yet a public
revision. Next work remains exact DJD/image mapping, measured real-damage
reading labels, additional source/English adjudication and NT witness expansion.

The judge also read the final central integration and found its scope accurate.
It flagged one documentation-state gap: the Numbers dossier still ended with
pre-application wording despite its successful transaction. That outcome
section was then completed and independently re-read. Final integration
received a bounded PASS with no outstanding concrete defect from this batch.
This was a documentation correction, not a new manuscript or implementation
verdict. Final documentation checks parsed 63 changed JSON files, resolved
494 local Markdown targets and passed Git whitespace validation; remote links
and historical conclusions are not certified by those checks.

### 2026-09-05 — Full 4Q24 reassessment, Samuel controls and failed region grounding

**Progress classification:** the previous goal turn made concrete progress:
new measured slices and published Greek evidence, a reviewed Numbers note
application and a recorded fail–repair–recheck cycle. It did not finish the
source census, restoration benchmark or publication gates. This continuation
used the same two research agents and separate read-only judge; the parent
performed En-Gedi region analysis and integration. No new canonical edit was
authorized or made in this batch.

**4Q24 primary reassessment:** the [new dossier](4Q24_LEVITICUS_2_PRIMARY_FOLLOWUP_2026-09-05.md)
supersedes the abstract-only access limit for Tigchelaar's fourteen-page
institutional manuscript. An ordinary verified-HTTPS Pretoria download
succeeded after the web extractor failed; all fourteen pages were inspected
by the research agent. The actual argument retains fragment numbers while
assigning1–8 to proposed4Q24a, considers a repair-sheet alternative, and
qualifies fragment8's similarity. We record this as the author's argued
reassessment, not our independent hand adjudication.

The paper identifies BlockA with DJDplateXXXI and its edition fragment1
with IAA B-368070, whose museum label is plate1079/fragment2. Edition and
museum fragment numbering must not be silently merged. Dated Qumran-Digital
rows and pinned QDR agree on reported והביא at Lev2:8 and ניחוח at2:9;
adjoining supplied and uncertain letters remain explicit. They are derivative
digital controls, not independent votes or our examination of DJD target words.
The individual physical fragments carrying lines29/31 remain unmapped.
IAA viewers showed black canvases, not consulted ancient pixels. Checked
institutional/bibliographic/preview routes did not provide the required DJD
pages; this is not proof that all lawful routes are unavailable.

The judge independently inspected seven decisive PDF pages, parsed the
actual HTML rows and checked IAA metadata. Seven focused tests passed without
skips. Bounded source-faithfulness/identity/disclosure PASS does not close the
target-edition, target-pixel, hand-identity or earliest-reading gates. Registry
and formal coverage records were not expanded by this publication consultation.

**2 Samuel20:6:** the [follow-up dossier](SAMUEL_20_6_SOURCE_ENGLISH_FOLLOWUP_2026-09-05.md)
directly checked Rahlfs–Hanhart2006 Greek, CAL's Leiden-derived Syriac,
GKC's relevant discussion and Driver's1913 scan, with BDB lexical controls.
The pointed source and all26 chapter context records are hash-bound; the
original sample remains frozen. Greek has future shading with plural eyes;
Syriac has an injury action, an additional taking-a-stand clause and Joab
instead of Abishai. Those are not one agreed Hebrew retroversion. GKC/Driver
recommend an imperfect emendation here because of the following consecutive;
they must not be represented as directly endorsing the retained perfect.
The stronger grammar objection therefore strengthens abstention, not a claim
that the emended letters are already present in the pinned source.

The actual consulted digital/scan locators, metadata-popup alignment issue,
source hashes and limits are recorded in the dossier. A reported Lucian
escape reading remains uncollated; full modern Greek/Syriac apparatuses and
manuscript dependencies were not examined. The judge independently checked
the decisive references and ten tests plus external PDF hashes. Its separate
hash-bound judgment grants a bounded evidence/integrity PASS while earliest
source and best whole-verse rendering remain INCONCLUSIVE. The naturalness
and uncertainty-note candidates are unapplied; no new source, English,
lexical metadata, note, exporter payload or publication approval follows.

**En-Gedi region grounding:** the [new experiment](EN_GEDI_REGION_GROUNDING_2026-09-05.md)
began by inspecting the actual master and merge5 PNGs and full relevant Segal
edition pages5,7,8,9,10,15,20. Merge5 visually resembles the initial blank
margin, not an inscribed column. This observation is a hypothesis, not
authenticated pixel correspondence or proof that every point lacks ink.
Yardeni's appendix expressly calls the drawings conjectural and discusses
distortion; Figure3 cannot supply an independent truth label for the same
rendering it interprets. Edition artifact leads and supplied letters likewise
remain distinct from independently verified reading labels.

A fixed, explicitly development-only SIFT/mutual-ratio affine experiment
was written and judge-inspected before matching results. Its correlated
every-third feature split is not spatially independent or blind. The frozen
v1 receipt records372 pairs,98 fitting inliers,124 validation pairs and
60 within20 master pixels (48.39%, below80%); the fitting-inlier vertical span
is36.70%, below50%. Thus the coarse registration gate FAILED. All residuals
and all19 projected prior targets are retained; projected locators remain
unaccepted and all letter labels null. No threshold relaxation, replacement
targets, image output or generated imagery was used. Prior numerical agreement
receipts remain valid on their limited terms, not evidence of readable letters.

The parent raised a pixel-center concern and the judge independently confirmed
a P2 coordinate-labeling defect using an actual OpenCV area-resize ramp and
its primary implementation. Scale-only lifting omits the center offsets.
The original v1 code/protocol/receipt were retained; a separate v2 correction
reproduces v1 from actual images, translates feature coordinates and conjugates
the existing matrix without new fitting or threshold changes. Original
integer targets remain unchanged. Their projections move approximately
(1.061456,0.945537) master pixels; residual changes are below2e-12 pixels and
the scientific gate remains FAILED. This repairs the coordinate bookkeeping,
not the failed registration. The judge also found372 descriptor pairs cover
only327 distinct geometric pairs, with32 validation rows duplicating fitting
locations. The parent reproduced this dependence; no after-the-fact
deduplication/refit or independent-validation claim follows.

The edition and runtime access details are in the dossier: absent pdftotext,
pypdf navigation followed by full-page visual inspection, a font-configuration
warning with rendered pages checked, and a private optional OpenCV package
installation. Source images and licensed PDFs stay outside Git. No image
editing or ImageGen operation occurred. The next acquisition is a bounded
triage of text-bearing segment textures, followed by their actual mappings
and required CT neighborhoods, not more purported letter tests in an
unlocated region. Exact image/edition labels, a separately frozen evaluation
set, errors/abstentions and two imaging families remain required.

**Checks:** parent repository regression passed301 tests and numerical
regression passed30 tests (331 distinct tests total). The original failed
registration receipt reproduced from actual inputs; both source agents'
bounded reviews are documented separately. Registry validation remains
31 mixed entries /20 passage records /13 formal cases /one unpromoted
selection. This batch changed research tools/receipts, tests and method/log
documentation, not canonical Hebrew, main English, notes or review flags.
No About integration, commit, deployment or new manuscript coverage was
claimed. The full goal remains active and incomplete, with safe next work.

Final coordinate-repair review: a fresh separately briefed read-only judge
independently derived the3×3 conjugation, checked all372 corrected pairs and
residuals, ran ten registration tests and exactly reproduced both receipts
from actual images. It gave a bounded repair/report PASS, with scientific
registration still FAILED and no new ink or publication approval. The prior
judge's continuation was reported as pending initialization, not a live
experiment; that uncompleted final review was not counted and was stopped
after the fresh review completed. Source-agent reviews above remain their
actually completed separate dispositions.

### 2026-09-05 — Standing Git publication authorization

The user explicitly authorized committing completed task changes, merging into
main and pushing the configured remote, while preserving unrelated work.
This supersedes the earlier lack of Git-push authorization; it does not change
scientific adjudication or reader-publication gates. The accumulated research
checkpoint contains206 scope-checked text files, including prior documented
note/metadata repairs and the local exporter correction. No full licensed
PDF, scan, CT slice, image payload or private dependency directory is staged.
No staged file exceeds5MiB. Pre-commit checks parsed69 changed JSON files,
resolved519 local Markdown links and passed staged whitespace validation.

The working branch was already main. A fresh origin fetch found five remote
commits after the old base, affecting revision-statistics tooling, status and
an open-transcription policy. Their changes must be retained in the ordinary
merge, not replaced with this research snapshot. The incoming policy requires
publishing completed independently produced transcriptions with provenance
while preserving third-party rights and canonical-review gates; this batch
does not claim a newly completed independent manuscript transcription.

Repository operational documentation says main pushes touching translation
files can trigger CodeBuild Bible publication, while `[skip ci]` suppresses
those jobs. This research checkpoint therefore uses that documented marker;
local validation is reported explicitly, and no separate deployment or
production-readiness claim is made. Final commit/merge/push outcomes are to
be verified against Git and the configured remote, not inferred from intent.

The research checkpoint was committed as `574f204de7`; ordinary merge
`883ae9160b` retained incoming origin/main `d7f7277027` without conflicts.
Both shared README additions survived. The incoming superseded revision-job
plist removal and replacement tooling were retained as remote history, not
discarded or independently redesigned by this task. Post-merge numerical
regression passed30 tests; the combined repository regression passed318 tests,
including the incoming revision-refresh suite (348 distinct tests total).
Its logged fixture failures are tested failure paths, not real failed pushes
or publication jobs. A final documentation checkpoint records
the completed coordinate review before pushing main. Push completion is not
inferred from these local commits.

### 2026-09-05 — Published checkpoint, all-book map, version controls and texture triage

The preceding turn made progress: the documented research checkpoint and
ordinary merge were pushed successfully. Local and remote main both resolved
to `b95cb7e473b2ad8c286da8377e8888335d2459ea`; the public revision-pinned
research-log URL returned HTTP 200. The next turn began with a clean main
tracking origin/main. This verifies Git publication, not Bible deployment or
scientific acceptance. No newly completed independent transcription was claimed.

The user explicitly requested parallel task agents and an independent judge
with repair/re-review loops. Two bounded agents handled all-book discovery and
Leviticus version controls while the parent acquired and inspected En-Gedi
textures. The judge received each completed artifact set for read-only review;
its actual disposition must be recorded separately, not inferred from test
results. No model upgrade supplies new manuscript evidence.

**All-book discovery:** the [39-book map](HEBREW_BIBLE_BOOK_WITNESS_MAP_2026-09-05.md)
actually processes all 218,217 word records in the pinned QDR file, with hashes
for all 39 WLC controls and preceding identity/genre evidence. It exposes 318
book–record pairs across 36 books. 1 Chronicles, Nehemiah and Esther have no
positive book tag here; Pam43113, Pam43124 and X4 remain book-unassigned.
Josh 5:0 is retained as an off-WLC numbering/alignment issue. No source record
or nonbiblical reference is silently dropped. This is a completed map of one
dataset, not a completed census of discovered manuscripts.

The supplied-text diagnostic is intentionally conservative: 134,985 biblical-tagged
word records belong to fragments with unbalanced/nested bracket syntax and
remain unresolved. The other syntax bins do not establish surviving ink either.
This is a concrete reason to require edition-context and exact-letter evidence,
not a reason to assume that most words are present or absent. Book-specific
label discrepancies, the 18 held Isaiah/Leviticus missing-label targets and
all-book family gaps now provide actionable acquisition queues. Ten new tests
and actual receipt/report regeneration passed before independent review.

**Leviticus 2:8–9:** the [version-control pass](LEVITICUS_2_VERSION_CONTROLS_2026-09-05.md)
directly consulted Rahlfs–Hanhart's publisher chapter and CAL's current Syriac
chapter/lexical/file-information pages. Greek has third-person opening and
delivery; its approach participle must be read with the explicit priest in
2:9. Syriac context supports second-person opening and delivery, then third-person
altar action. Opening agreement therefore does not establish whole-verse
agreement with stored Hebrew pointing or settle every agent.

CAL's displayed aroma alternative and shared lexical parse must not become
a claimed Hebrew waw reading or an identified manuscript variant; its siglum
identity and full Leiden apparatus remain unverified. CAL identifies its
edition-derived text as including some 7a1 corrections; no particular target
word was established as such a correction. The checker binds 15 local inputs
and two manually retained selected observation transcripts. Their hashes do
not represent raw page bytes. Publisher curl 403, obsolete CAL route 404,
unsupported browser export and CAL's no-scraping response were recorded;
ordinary bounded browser consultation succeeded without bypassing restrictions.
Seven new tests and five prior agency tests passed. Source priority, best
English, full apparatus and 4Q24 target pixels remain open; no canonical edit.

**En-Gedi:** the [texture triage](EN_GEDI_TEXTURE_TRIAGE_2026-09-05.md) froze
all six remaining `textured.png` selections and explicit member/batch budgets
before downloading their payloads. The actual verified-range acquisition
retained 62,316,462 expanded PNG bytes, with 65,415,587 HTTP body bytes logged.
The previous strong archive ETag and a fresh central-directory match were
required; all six payloads passed length/CRC checks and were rehashed locally.
The full archive was not hash-verified. Private payloads retain upstream
CC BY-NC terms; only protocols, hashes, ranges and observations enter Git.

All six unaltered full-image overviews were inspected at display-downsampled
resolution. Several show repeated bright text-shaped rows; `remerge` was
selected after inspection for the next mapping/CT development step, with
merge1/merge2 retained as alternatives. This is neither blind validation nor
six independent witnesses. No letters, verse locators or blank controls are
accepted. The earlier merge5 registration still fails. No image was enhanced,
edited or generated, and no new mapping/mask/CT payload was acquired in this
pass. Ten new tests plus nine existing ZIP tests passed; the actual six-payload
checker passed separately. Tests verify integrity and bounded claims, not ink.

The approach review, source-coverage audit, discovery index and backlog now
link these three completed bounded results. Historical frozen methods, receipts,
canonical Hebrew/English/notes, review flags and the registry are unchanged.
The next scientific gates are primary book-specific identity/preservation
work, full version apparatus and actual text-region mapping with separately
frozen evaluation labels. The broad OT/NT restoration goal remains incomplete.

Parent validation of this checkpoint passed 345 repository tests and 30
separate numerical tests (375 distinct tests). The actual 39-book map regenerated
exactly; the version checker passed all 15 local and two private transcript
bindings; the texture checker reverified all six actual private payloads.
Registry validation remains 31 mixed entries / 20 coverage records / 13 cases /
one unpromoted selection. Five new JSON files parsed and all 203 local Markdown
targets in the 20 scoped files resolved. Whitespace checks passed. Revision-job
test fixture failures are expected failure-path output, not real failed pushes.
A fresh origin fetch succeeded; publication of this new batch is not inferred
from the earlier checkpoint. An additional separately briefed read-only image
judge was assigned the texture batch to divide final review from the textual
judge's two dossiers.

The image judge subsequently completed its review and gave a bounded
acquisition/overview PASS, with no blocking defect. Beyond the parent checker,
it independently verified each whole-file ZIP CRC and internal PNG chunk CRCs,
the exact prior-index member selection and byte-identical public/private
receipts. It reproduced all budget/range totals, inspected all six unaltered
overviews and passed the 19 focused/ZIP tests. The additional index/header/name
range bodies total 3,114,519 bytes. Its PASS does not accept any letter, ink,
verse coordinate, blind evaluation or publication claim. Prefetch timing rests
on the recorded execution history, not on an independently provable ordering
in the retained files alone. The parent wrote the protocol before acquisition.

The textual judge then completed both dossiers with bounded PASS verdicts and
no actionable defect. It independently counted the entire pinned QDR corpus
without importing the builder, verified every one of the 39 book counts and
all 318 first locators against nested source data, reproduced the outputs and
passed ten focused tests. The book-map receipt SHA-256 is
`122adba01e0dbbbfba9ff68d4039a692c20499c3cd6af5a09781db9e5951328a`.
This is census/accounting/reproduction approval, not complete witness coverage
or letter survival.

For Leviticus, the judge independently consulted the publisher Greek chapter
and edition credit, CAL chapter and edition metadata, four decisive verb lexical
pages and the aroma/shared-parse page in its own browser session. The retained
observations agree; all 15 local and two private bindings and seven focused
tests passed. Receipt SHA-256 is
`379d79d7283eb0303f399d9efad32803e4f4b956077a136121ed1d686d2e8957`.
Its PASS covers source fidelity and clause-specific person/agent/retroversion
distinctions. Full apparatus, CAL siglum identity, Hebrew priority and best
English remain open. The judge also checked integrated summaries for matching
limits. Neither judge found a defect requiring a repair loop in this batch;
the earlier recorded failures and repairs remain intact. This checkpoint is
ready for a routine scoped Git commit/push under the user's standing authority,
with `[skip ci]` and no direct deployment or scientific-promotion claim.

## Remaining work

- Dated institutional-catalogue coverage across all relevant books/sources.
- Full apparatus and image-dependent questions in the existing dossiers.
- Real-image development labels, frozen evaluation inputs and two-family
  calibration with measured errors/abstentions; the old pilot is insufficient.
- En-Gedi legacy coordinate/index conventions, segment-to-master correspondence,
  exact renderer revision/parameters, documented texturing filters and labeled
  damage controls before a reading recovery benchmark; one numeric probe and
  static period-code inspection do not complete these.
- One complete reviewed source/English/notes/export application package.
- Source-stable English review, including unflagged passages.
- NT manuscript/hand coverage beyond edition disagreements.

Detailed backlog: [DSS TODO](DSS_TEXTUAL_WITNESS_TODO.md) and
[restoration priorities](TEXTUAL_RESTORATION_PRIORITIES.md).

## How future work must be logged

Append a dated entry for every substantive research pass: question; actually
consulted sources and locators/versions; observations versus hypotheses;
decision and contrary explanation; changed files and source/English effect;
checks and what they establish; unsuccessful attempts/access limits; next gates.
Link machine evidence rather than duplicating corpora. Identify superseded
claims when correcting them and propagate corrections to affected records.
Never invent dates, independent reviews, completed experiments or commit IDs.

## Later About-page summary — proposed, not published

> POB's ongoing source-comparison program examines biblical manuscripts and
> ancient translations, records uncertainty, and tests possible improvements
> to its source texts and English. Its research log includes findings,
> corrections and unresolved questions. AI-generated illustrations are not
> manuscript evidence.

When requested, link this summary to this log using a public repository URL
and a real committed revision. Review against the then-current status first;
do not claim comprehensive comparison or recovered originals prematurely.
This file provides the documentation target; no About integration is implemented.
