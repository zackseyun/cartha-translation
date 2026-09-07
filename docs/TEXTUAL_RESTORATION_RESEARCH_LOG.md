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

### 2026-09-05 — Full-verse, literary-form and text-region geometry follow-up

The previous turn was progress: 20 reviewed research files were committed and
pushed as `fa0f994c339370cf3796e101237ac7fadc081cbc`. Local/remote main matched,
the worktree was clean and the revision-pinned public log returned HTTP 200.
This turn rechecked a clean main before continuing. Git publication does not
close scientific or Bible-deployment gates.

Two parallel agents investigated consequential Deuteronomy and Jeremiah
questions while the parent acquired En-Gedi geometry. A separately briefed
read-only judge reviewed their primary evidence and the parent's actual-data
check. This division follows the user's explicit authorization, without
counting agents as additional historical witnesses.

**Deuteronomy:** the [new full-verse supplement](DEUT32_8_ADJUDICATION_FOLLOWUP_2026-09-05.md)
narrows image consultation to IAA B-359054/B-359055, color/IR, both catalogued
as 4Q37 plate 172 fragment 10 recto, Shai Halevi April 2013. Actual pixels were
viewed nonblind and the IR designation is compatible with the published
reading. No new letter is claimed. The section labeled `12` in Qumran-Digital
is not yet certified as the repository's “DJD fragment 12” or linked by a
verified edition crosswalk to IAA fragment 10.

Fresh published-transcription consultation also exposes `בהנחי[ל` at the
opening versus retained WLC `בהנחל` in the composite draft. This is an explicit
orthographic review item, not an automatic English change. The bracketed
middle cannot certify the whole verse. An alternative spelling is recorded
but unselected; the existing moderate working preference is not promoted.
Official Göttingen/Brill browser access revealed purchase/login or no readable
sample, rather than proving universal unavailability from web-tool 403s.
Dayfani full text and the adjacent modern Greek apparatus units remain unread.
The independent judge verified all eight local bindings, actual IAA metadata
and color/IR pixels, the two Qumran-Digital lines and cautious access wording.
It gave a bounded evidence/documentation PASS, not source/English approval.

**Jeremiah:** the [literary-form dossier](JEREMIAH_10_LITERARY_FORM_COMPARISON_2026-09-05.md)
advances a previously queued unit with actual DJD XV and Swete pages. At
10:10, 4Q70 preserves the core `מלך עולם מקצ` with editorial probability marks
on the first two letters; the true/living-God opening is supplied. 4Q71's
shorter 5a–9–5b sequence and absence of 6–8/10 are a spatial reconstruction
from very short line endings, not a surviving whole omission boundary.
4Q72a is chapter-43 evidence and not another chapter-10 vote. Langlois's
later hand/date reassessment is recorded as a competing published view.

Swete's continuous B text has the shorter form, but its Q marginal apparatus
explicitly includes a Greek form of verse 10. The Greek wording also differs
within aligned units: mechanically cutting/reordering current POB would not
translate it faithfully. The longer POB form is provisionally retained and a
literary-form disclosure drafted but unapplied. Full modern Greek/HUB apparatus,
later spatial reconstruction and earliest-form priority remain open. The
agent used the PDF skill for visual preservation/apparatus checks; the judge
independently hash-checked all three PDFs and read the decisive complete pages,
sigla and conventions, passing the eleven-context/three-label checker. Its
bounded documentation PASS does not approve the proposed note or a source form.

**En-Gedi:** the [remerge mapping check](EN_GEDI_REMERGE_MAPPING_2026-09-05.md)
fixed the same-segment map/mask, two 256 MiB ZIP batch ceilings, a separate
2 GiB expanded ASCII ceiling and 68 coordinates before fetching mapping bytes.
The actual acquisition completed with 237,811,326 ZIP-expanded payload bytes;
240,845,435 HTTP body bytes were logged in 64 verified ranges. Full decoding
checked 58,564,800 scalars at 2400 × 4067 positions, with 1,169,004,178 ASCII
bytes. All 68 samples remain: 38 mask-valid and 30 zero-mask. All twelve
upper/central development points are valid, with recorded z about 852.586–1477.817.
These are useful scan-geometry leads, not validated CT indexing or letter labels.

The judge found a real byte-cap defect before any numeric result was accepted:
default universal-newline handling could count a six-byte CRLF fixture as four
characters. The original acquisition implementation was preserved byte-for-byte
as a hash-bound historical text artifact; its private receipt was not altered.
The corrected inspector uses `newline=""` and separately identifies its code.
Regression tests demonstrate the old undercount and repaired cap rejection,
including bare-CR/non-ASCII checks. A separate parent binary scan found zero
CR bytes and 20,719,247 line feeds in the actual mapping, matching the expanded
size, so no observed payload value changed. The judge independently replayed
the full corrected result, checked system-gzip byte count/end decode, verified
public/private receipt equality and range totals, and passed all 18 new/ZIP
tests. Repair/acquisition/geometry received bounded PASS; the earlier failed
registration and all reading-evaluation gates remain open.

The initial broad index listing accidentally included thousands of projection
entries and was truncated; a subsequent exact two-name query supplied the
bounded member metadata actually used. The texture was viewed again with
original-detail requested, but the display still downsampled it; no native-scale
paleographic inspection is claimed from that view. No image editing, generated
image, new CT slice, full transcription, canonical source/English/notes change,
registry migration or deployment occurred. The source audit, approach review,
backlog and discovery index link the results. The full goal remains active.

Final parent validation passed 354 repository tests plus 30 numerical tests
(384 distinct tests), the eight Deuteronomy input bindings, the Jeremiah
eleven-context/three-label checker and the unchanged registry validator.
All five new JSON files parsed and 215 local Markdown targets in 17 scoped
text files resolved; no file exceeded 5 MiB. The judge's final prose check
passed the completed mapping report and integrated summaries with no mandatory
wording correction. Its verdict remains bounded to the actual evidence and
repair, not source/English selection. This checkpoint uses the standing
commit/main/push authority and `[skip ci]`; actual push success must be checked
against the configured remote rather than inferred from the validation.

## 2026-09-06 — bounded note delivery, numbering controls and failed registration

The preceding checkpoint was actually committed and pushed as
`bbc3c51188a61fc04bcb0dc8241d47581950bbbe`; a direct remote-tip check confirmed
that revision before this continuation. Previously frozen September 5 artifacts
keep their original dates. This entry records the September 6 continuation.

**Deuteronomy:** the [numbering check](DEUT32_8_NUMBERING_CHECK_2026-09-05.md)
consulted the Lexham/Pfann publisher preview, ABMC's historical photograph
inventory and the versioned Qumran-Digital transcription. Opening sections 1–5
correspond to columns I–V in the preview; extension to XII remains inference
because the preview stops during V.8. PAM 43.054 and Duncan's dissertation
plates VI–VII are acquisition leads, not inspected target photographs. The
source's top-line circle belongs to 4Q37; the nearby complete parallel belongs
to 4Q45. Actual DJD XIV p. 90/plate access remains unsuccessful. The separate
judge accepted this bounded report, not a completed crosswalk or source choice.
No source, English, registry count or historical frozen candidate changed.

**En-Gedi:** the [new registration](EN_GEDI_REMERGE_REGISTRATION_2026-09-06.md)
fixed SIFT matching, mutual/ratio filters, both-endpoint deduplication,
pixel-center coordinate lifts, whole-tile fitting/validation assignment and
affine-fit/gate parameters before the observed outcome. The actual run retained
957 of 1,065 pairs and rejected 108 duplicates. It found 116 fitting inliers,
but only 82 of 352 validation pairs were within 20 master pixels (23.30%,
required 80%); x/y spans were 22.68%/34.08% (required 25%/50%). This is FAIL,
not a partial reading success. All 68 projected prior points retain null
accepted verse/letter labels. The judge independently recomputed residuals,
partition and endpoint checks and reproduced the saved result from actual
images. That is reporting-integrity approval only. No threshold retuning,
new recovered letters, edited images, ImageGen evidence or source selection
resulted. Local deformation or incorrect correspondences remain possible;
the experiment does not decide their cause.

The numerical runtime requested one OpenCV thread but reported eight. The
judge's full replay reproduced that field too, and a separate diagnostic found
eight reported before and after the request on the GCD-backed build. Frozen
bytes remain intact; no effective single-thread execution is claimed.

**Jeremiah candidate review:** the separate source judge inspected the actual
DJD, Swete and Langlois pages identified in the hash-bound
[judgment](../sources/textual_restoration/applications/jeremiah_10_10_note_judgment.v2.json).
It approved v2's bounded literary-form disclosure, repaired a/b/c anchor
placement, Yahweh connective metadata and explicit archiving of old review
states. Source YAML and marker-free English are unchanged. v1 remains frozen
as the narrower predecessor that left connected defects in place; v2 and both
preflights remain separately preserved. Whole-verse approval, earliest-form
selection, fresh verification of inherited lexicon citations and publication
remain explicitly outside that approval.

The judge's first handoff encountered a usage limit after a complete judgment
had already been saved. The parent inspected that artifact and the resumed
judge confirmed the completed review. No usage reset or purchase was made.
This was an interrupted handoff, not an invented or incomplete source review.

**Application safeguards:** the new transaction tool has no canonical writer.
It requires a separately reviewed executor, exact baseline/candidate/evidence
hashes, a write-once intent, an explicit separate patch and actual post-edit
full-book export verification. Historical replay overlays only the two named
approved note targets and reports the real current corpus digest separately.
The transaction judge identified a lifecycle gap: exact baseline bytes could
otherwise be accepted after an application receipt existed. The parent repaired
this by rejecting an unrecorded rollback and validating an existing intent even
at baseline. Tests and re-review must pass before the canonical patch.

The repaired exact executor received the separate transaction APPROVE. Actual
prepare, separate `apply_patch`, and completion then succeeded; see the
[application report](JEREMIAH_10_10_NOTE_APPLICATION_2026-09-06.md) and its linked
immutable ledgers. Canonical Jeremiah 10:10 now exactly matches approved v2.
The actual export covers 52 chapters/1,364 verses, retains all four notes and
matches the approved candidate; every other exported Jeremiah item is unchanged.
The real current OT corpus digest changed from `f717bc7f9904942cbb2c9d4748d176bef195ad2c108a713a4ae269e00bee082d`
to `c1fba2b816d99268b268e8a175c6be6181e5e66b373872f1f701449272262093`.
The frozen historical digest remains `d7ba46056931eb8f23844b388ca2adeef5e6c7588e40ad3b6b5e8c6336fb5381`.
All 101 historical context bindings and the eleven dossier contexts reproduce
through explicitly identified approved baselines, not by rewriting history.
Sixty relevant tests passed again after the canonical edit. This is a completed
bounded note application, not a complete source/English adjudication or a
deployed-reader change. The all-book research goal remains active.

The complete post-edit repository regression passed 375 tests; the numerical
suite passed 39, for 414 distinct passing tests. The unchanged registry still
validates 31 mixed entries, 20 coverage records, 13 formal comparisons and one
unpromoted selection. Pre-publication file checks parsed all 11 new JSON files
and resolved 241 local Markdown links across the then-current 30 scoped files;
whitespace checks passed and no file exceeded 5 MiB. Revision-refresh fixtures
exercise failure paths intentionally; their printed fixture errors are not an
actual research-branch push failure.

The [final independent verification](../sources/textual_restoration/applications/jeremiah_10_10_note_post_application_verification.v2.json)
then passed actual canonical bytes, approval/intent/application bindings,
full-book export and historical replay, with no mandatory reporting correction.
The judge independently compared the unchanged source block and marker-free
English and repeated 21 transaction tests after application. This checkpoint
is ready for the standing main/commit/push workflow with `[skip ci]`; that Git
publication is not Bible deployment or source-form approval.

## 2026-09-06 — Masoretic coverage, Psalms discovery and Genesis wording controls

The preceding note-application checkpoint was real progress, not a status-only
turn: `398e15cad50dda6911aaf7c70d2414b974afd9da` was committed and pushed, and
this continuation independently confirmed the clean starting worktree and
matching configured remote tip. The goal remains the full source-comparison
program; one applied note does not redefine its completion criteria.

**Masoretic controls:** the [all-book spine](MASORETIC_CODEX_COVERAGE_SPINE_2026-09-06.md)
joins the frozen 39-book discovery map to Leningrad, Aleppo and Sassoon catalogue
evidence, while retaining 24 Tanakh navigation groups. NLI's exact Leningrad
shelfmark/date/representation metadata were directly read. NLR's indexed
caption/prose date discrepancy remains a discrepancy. Aleppo's project page
separates absent main-body parchment from reported recovered pieces, old
photographs and testimony; the map does not erase those surrogate leads or
assume POB book order matches codex order. The ANU Hebrew page succeeded after
two English-route timeouts. Its aggregate Sassoon extent and two Masorah hands
are not a per-verse survival map or new hand adjudication.

Actual local XML headers and all 39 file hashes establish the digital source
snapshot; the UHB manifest records its distinct version and declared source.
The directly consulted UXLC About/Changes pages describe another fork and two
important editorial exceptions. The executed local probe finds ten word nodes
in each of Joshua21:36–37, despite the editor's report that the unit is absent
in LC, and 59 vowel codepoints in Numbers7:19, a repeated-offering example for
the reported supplied pointing. Numbers7:13 is explicitly the first-offering
control, not another claimed omission. These are encoded-text measurements
paired with source-reported manuscript claims, not new pixel observations.
No verse deletion, source upgrade, repointing or English edit follows. The
judge independently checked the institutional/editor claims and passed the
bounded eight-test package. New image/manuscript access failures are retained
in the observation record; no restrictions were bypassed. Observation hashes
do not purport to fingerprint original web responses.

**Psalms:** the [catalogue reconciliation](PSALMS_CATALOGUE_RECONCILIATION_2026-09-06.md)
consulted Flint's 2014 Oxford appendices and institutional IAA metadata, then
reconciled the actual pinned biblical and nonbiblical QDR files with the full
saved modern catalogue index. All 39 existing Psalms labels/1,261 reference
anchors are accounted for. Fourteen additional literary-context targets are
kept separately; thirteen have exact nonbiblical labels. Three collection
labels occur in both files, so their sixteen nonbiblical matches do not mean
sixteen added manuscripts. The check did not scan nonbiblical passage words.
4Q173a remains unmatched; MasPsa's Psalm18 allocation conflicts with the local
Mas1e Psalm81–85 tags; source spelling/numbering conflicts and three historical
provenance leads remain held. This supplies concrete quotation/liturgical
acquisition targets, not accepted readings or a complete Psalms census.

The parent caught one reporting defect before freezing the Psalms receipt:
the checker described the consulted sources as human-consulted. These were
agent consultations. The author corrected that field and regenerated the
code-bound receipt; no human review is invented. No PDF or manuscript image
was inspected in that catalogue pass.

**Genesis4:8:** the [comparison](GENESIS_4_8_SOURCE_COMPARISON_2026-09-06.md)
revisits an existing shorter-text disclosure, rather than claiming a new case.
The published 4Q2 junction supports the shorter transition while much of the
preceding speech clause is supplied. Actual Swete page and introduction checks
identify Alexandrinus as the base at this location; Vaticanus must not acquire
an attestation from the edition's general title. Pinned Samaritan Hebrew,
official Latin and CAL Syriac distinguish field, outside and plain/valley
wording. Jerome's primary discussion and Hendel's full argument in the accessed
preview inform competing loss/completion explanations without closing priority.
The agent used the PDF skill for actual edition-page inspection; no new
manuscript decipherment is claimed.

The proposed note tightens survival and versional wording, retaining the
existing appropriate anchor. It is unapplied. “Spoke to” is separately identified
as a possible English-only alternative to the awkward retained “said to”; its
smoothing tradeoff needs its own review. No source or English promotion follows
from the age of 4Q2 or a simple count of agreeing versions. Unconsulted full
modern apparatuses and unresolved transmission explanations remain explicit.

Parent validation passed 391 repository tests and 39 numerical tests (430
distinct tests). Real-input Psalms and Masoretic receipt reproduction passed;
the Genesis baseline/source hashes and exact proposal/report agreement were
checked. At the pre-judgment checkpoint, five new JSON files parsed and 253
local Markdown links resolved across 17 scoped files, with no file over 5 MiB.
No canonical verse or previously frozen research artifact was edited in this
pass. Tests certify the recorded invariants and unchanged history, not the
earliest biblical text or newly recovered ink.

## 2026-09-06 — Whole-OT edition screen and exact Genesis candidate

The previous source-workstream checkpoint was committed and pushed as
`9b504eac484390728f68e0d2e415c898cba5875c`; main and the remote tip were verified
equal and the worktree clean before this pass. The broader restoration goal
remains active. The user-authorized agent split assigned Psalm91/11Q11 primary
published evidence, an exact Genesis4:8 disclosure candidate, and independent
judgment; the parent executed the whole-OT digital-transcription screen.

The [UXLC/WLC report](UXLC_WLC_WHOLE_OT_SCREEN_2026-09-06.md) records an actual
hash-verified publisher ZIP and all 39 ordinary-book comparisons. All 23,213 verse
labels align by label; five verses differ in the written-consonant lane. Final
first differences are 374 pointing, 3,897 accent/meteg and 203 full-stream format;
18,734 are equal through all declared lanes. Separate qere and token-boundary
diagnostics overlap these categories. These are edition diagnostics, not
independent witnesses, restored letters or automatic English corrections.
The result joins all five consonant leads to current canonical Hebrew and
English without changing either. Four source fields match WLC; the fifth's
literal neither-match includes a separately recognized paragraph-marker issue.

The acquisition retained full archive/header/site assets privately and exports
only biblical text and factual metadata under the publisher's terms. Direct
web XML reading was unsupported; ordinary HTTPS acquisition succeeded. An
initial member-path error and an initial parser rejection of nested decorated
letters are documented in the report; neither was concealed as a successful
run. Explicit mixed-content and punctuation handling repaired the parser before
the saved comparison. Tests cover actual multiword, empty and insertion-only
qere examples, exclude descendant-word duplication, retain decorated letters
and tails, and verify the saved inputs and layer partition.

The Genesis author prepared an [exact unapplied candidate](../sources/textual_restoration/applications/genesis_4_8_note_candidate.v1.yaml),
[plan](../sources/textual_restoration/applications/genesis_4_8_note_plan.v1.json)
and [preflight](../sources/textual_restoration/applications/genesis_4_8_note_preflight.v1.json).
The previously approved note is verbatim; only connected invitation descriptions
and explicit archival of old review/status fields accompany it. The source,
main English and existing anchor remain byte-identical. Both real full-Genesis
exports contain 50 chapters/1,533 verses with only the target disclosure changed
in the candidate output; all canonical inputs remain unchanged. This is not
a deployed-reader test, a transaction, a source-priority promotion or whole-
verse reapproval. In particular, the English “said to” versus “spoke to” question
has not been smuggled into a note-only edit. Any later application must also
preserve the frozen historical sampling and prior application records.

A second bounded source review found the existing NT categories appropriate
and proposed operational refinements now recorded in the
[coverage audit](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md#operational-nt-refinements--2026-09-06):
distinguish catalogue/image/transcription/apparatus/survival access, pin
ECM/CBGM book and dataset, name specific versional acquisition routes, record
patristic citation transmission, and track editorial dependence. Official
NTVMR page attempts exposed navigation rather than passage evidence. No NT
manuscript collation or restricted apparatus import is claimed.

Parent validation at this checkpoint passed 413 repository tests, including 13 new
comparison tests and 9 Genesis candidate tests, plus 39 numerical tests: 452 distinct
tests. This is validation of the defined invariants, not scientific proof of
textual priority or model accuracy. Independent judgment and any resulting
repairs are recorded separately below before final freeze/commit.

The independent judge rejected the first saved UXLC result for normalization
order: removing blockers after NFD can leave combining marks noncanonically
ordered, generating false differences. The parent applied NFD after each lane's
filtering too, added a blocker/mark-order regression, and reran all 39 books.
The private rejected result is retained at SHA-256
`515b365164a135a545f95765bb669cd0efb7c481d00c111b9108c8f181bcb6b8`;
its earlier 824 pointing/4,277 accent/197 full-stream counts are superseded.
The corrected receipt has 4,535 flagged rows and 67 qere-payload flags rather
than 5,356 and 75. The five consonant leads, 13 qere-presence/word-count flags,
24 token-boundary/payload flags and all raw inputs are unchanged. The new test
raises the current distinct test total to 453 (414 repository plus 39 numeric).
No rejected result is being presented as a scientific pass.

The subsequent publisher-history follow-up located all five consonant changes
in pinned book headers and the actual dated change records. These are reported
same-codex transcription corrections. Ezekiel16:36 remains explicitly uncertain:
the summary/TEI's c versus detailed action/current XML's t discrepancy is kept,
not resolved by majority of descriptions. Samuel13:37's uncertainty concerns
the preceding vav/yod, not the publisher's final dalet reading. A diagnostic
removing only Samuel14:7's terminal paragraph פ establishes an exact WLC match;
the receipt's literal neither-match remains unchanged. Folio/column/line and
word locators in the report now provide concrete next image targets. No pixels
or BHL apparatus were newly examined in this follow-up.

The [Psalm91/11Q11 comparison](PSALM_91_11Q11_COMPARISON_2026-09-06.md)
advances the catalogue lead to published transcription and actual Greek edition
pages. The accessible Lexham/Biblia preview reaches columnVI.3–9; QDR's private
surface text continuesVI.10–14 but receives an explicitly lower evidence status.
The Qumran-Digital web page stops before the Psalm despite its presence in the
other resources. Švarc's actual2026publication of a2025issue paper supplies
competing reconstructions; SweteII's printed336–337 and apparatus were visually
inspected, along with relevant study/thesis pages using the PDF skill.
No DJDXXIII or scroll-pixel consultation is claimed.

Most importantly, the proposed speech verb in verse9 is [קר]את: the initial
letters are supplied, not a fully preserved word that compels inserting
“said/called” into POB. Verse2/4 alternatives merit focused consideration;
verse13 and the ending rely on QDR beyond the accessible published preview.
The parent caught wording that initially blurred that preview boundary for
verse13; the author qualified both the result and table before final review.
Greek apparatus evidence also prevents an unqualified claim that all Greek
witnesses omit “all” in verse11. Collection-specific adaptation remains a live
alternative to earliest-text priority. All sixteen POB Psalm91 files are
unchanged, and no restoration or source selection is accepted.

Final package review: the independent judge reproduced the repaired full UXLC
receipt exactly, passed all 14 comparator tests, and checked the five publisher
change entries with their retained uncertainties. The Psalm91 review checked
21 source/control hashes, the actual private column-VI transcription, accessible
preview boundary, Greek apparatus and consulted scholarly pages. The bounded
packages pass; no manuscript restoration or historical-priority claim passes
by implication. The exact Genesis candidate judgment is
`2017263197fe6d548e0b058b975fe68d2b397b3f84e8fed4c93849e5471ed525`:
note/connected-metadata approval only, transaction approval still false.
After the normalization repair, the parent reran the full repository suite:
414 tests passed; the unchanged numerical suite passed 39, totaling 453 distinct
tests. The backlog now distinguishes completed bounded comparisons from open
image/apparatus/application work. No canonical files or frozen earlier research
artifacts changed. About-page integration and deployment remain unperformed.

## 2026-09-06 — Actual Leningrad photographs and guarded Genesis application

The previous turn was verified progress, committed/pushed as
`17ff36ca71255b6bdab11dce91bbadac295c101c`; the remote tip matched and the
worktree was clean. This pass pursues actual evidence behind the five written-
consonant leads rather than treating the edition screen as final adjudication.

All five mapped full-color folios were legitimately accessible. The
[three orthographic checks](UXLC_ORTHOGRAPHIC_IMAGE_FOLLOWUP_2026-09-06.md)
cover 2Samuel14:7, 2Chronicles27:4 and Amos7:2; the
[Samuel/Ezekiel check](SAMUEL_EZEKIEL_CODEX_IMAGE_FOLLOWUP_2026-09-06.md)
covers 2Samuel13:37 and Ezekiel16:36. Sefaria's actual documented manuscript API
provides page IDs, verse intervals, exact full-image URLs and photographer/
institutional attribution. The source metadata's USC link currently serves a
DSS page; the actual Biblical Manuscripts page and date/campaign distinctions
are recorded without silently converting API1008 versus USC1010 into new
objects or exact JPEG capture dates. Photo redistribution clearance is absent,
so the raw photographs, native crops and downloaded metadata remain private.
No generic biblical-text license is asserted over the photographs.

Whole-page displays established context and were explicitly downsampled by the
viewer. Native-resolution, lossless rectangular crops then supplied local
letter observations. The orthographic author verified21 hashes, three image
dimensions/byte lengths, three API mappings and six exact crop rectangles.
The parent verified16 hashes, two image dimensions/byte lengths, two API
mappings and seven exact rectangles. No resizing, enhancement, threshold,
spectral reconstruction or ImageGen was used on the letter crops. All bounds
and hashes are retained. The image selector's unsuccessful Go action, guessed
URL failure and web-reader failures remain documented; no popup/security
setting or access restriction was bypassed.

The three orthographic crops favor the publisher's extra-yod/defective-spelling
observations, with Samuel's pale trace less decisive. Samuel13:37's final letter
locally favors dalet against nearby controls, but its preceding vav/yod remains
separate and unresolved. Ezekiel16:36 remains an abstention between bet and kaf;
its irregular contour and conflicting c/t metadata do not permit certainty.
These are known-reading, context-informed inspections and report-aware second
checks, not a blinded two-family transcription experiment, calibrated acceptance
or historical-priority decision. The held image questions are not made to pass
by a model vote. No Hebrew or English source-selection patch follows here.

Reading the actual Samuel13:37 YAML also clarified a reader-facing defect:
the marker after Ammihur points to a note about David as the implicit subject
of mourning, not a name-variant disclosure. The name/source question and note
anchor therefore need a separately scoped proposal; the old note cannot count
as already disclosing the ketiv/qere. Ezekiel's separate bronze/wealth revision
history was read but is not reapproved by this one-letter check.

The Genesis agent prepared a [guarded implementation](GENESIS_4_8_NOTE_APPLICATION_2026-09-06.md)
for the already approved exact note candidate. It has no canonical writer:
exclusive intent and completion ledgers surround a separate parent apply_patch.
It composes an explicit third historical overlay around the frozen Jeremiah
and Numbers replay helpers, measures the actual corpus digest outside every
overlay, rechecks exact review/input/ledger bytes, and verifies full current
GEN export separately from the historical candidate preflight. The exact
current-test migration also passes the active Path reader explicitly, so
outer overlays are not bypassed by an import-time default. No frozen checker,
candidate, receipt or policy is rewritten.

The parent raised a possible lifecycle concern about the nine frozen Genesis
candidate tests. Actual file inspection, prompted by the judge, disproved it:
they read frozen baseline/candidate records and test scope only, not live
canonical preflight. They remain in the complete suite unchanged. Only the old
checker's CLI/run is baseline-specific and needs the explicit historical view.
No invented failure or test exclusion was introduced. Parent execution of all
28 new transaction tests passed before application; those tests include actual
full GEN exports and historical replay using simulated candidate reads.

Seventeen derivative/simplified Genesis4:8 records are pinned unchanged, not
synchronized or certified. Existing simplified English supplies an invitation;
a German record retains older note wording. These predate the new candidate.
An unchanged Hebrew source hash cannot demonstrate note freshness, and English
GEN validation is not multilingual validation. This scope limit is explicit in
the implementation and review rather than hidden by a coverage-test pass.

### Actual Genesis application and image-review decisions

The independent judge approved the exact Genesis executor package, then the
parent prepared an exclusive intent at 09:08:26 UTC, applied the frozen YAML
candidate and exact five-replacement current-test migration with apply_patch,
and completed the application at 09:09:37 UTC. The resulting target and test
hashes match their approved candidates. The
[actual verification record](GENESIS_4_8_NOTE_VERIFICATION_2026-09-06.md)
separates this applied state from the preserved implementation draft.
No Hebrew, main English or note-anchor change was made. The old review values
are archived and the current verse remains draft/needs_review rather than
inheriting historical agreement scores as approval of new note bytes.

The completion receipt and fresh parent post-check both verify the actual
50-chapter/1,533-verse Genesis export against the frozen candidate export
`908ddbcef18f990ba77df4622e82d595c027301646fee572b2ceca51789cfca3`.
Only the target note differs in that book export. The actual OT corpus digest,
outside all historical overlays, is
`89d6910840ac91c621fe2c929edd8add3eebb17e2229831a7a12ca253c936ec0`.
The original sample and its 101 context files are reproduced only under the
three explicitly named baseline views; this does not certify an unchanged
current corpus. Publication, derivative synchronization and historical source
priority remain unapproved.

Both image reports passed independent faithfulness/reproducibility review:
[orthographic review](../sources/textual_restoration/discovery/uxlc_orthographic_image_review.v1.json)
and [Samuel/Ezekiel review](../sources/textual_restoration/discovery/samuel_ezekiel_image_review.v1.json).
The reviewer inspected actual full-page context and native crops but already
knew the reported alternatives. These are report-aware second checks, not
blinded two-family transcription acceptance. The Samuel dalet fit is qualified,
the three orthographic fits do not supply new English, and Ezekiel remains
inconclusive. No canonical source-selection patch follows from these reviews.

Fresh [independent Genesis post-verification](../sources/textual_restoration/applications/genesis4_8_newtransaction_postverification.v1.json)
also passed, reproducing the exact completion result and checking the actual
source/main/anchor invariance, old-review archival, 22 prior package pins,
17 derivative pins and exact five test edits. Its 13 post-application tests
passed without removing the nine frozen candidate tests. The previous
implementation-stage review remains a separate artifact, not a retrospective
claim that it had already inspected the applied state.

The first full post-application regression exposed an additional integration
gap: 442 tests ran in 197.019 s, with 441 passing and one failing. The current
registry test passed a frozen Pentateuch comparison directly to its original
validator, which correctly reported `GEN.4.8.speech: canonical baseline drift`.
The 28-test executor review and 13-test post-check had not exercised this
consumer. The parent sent this real failure to the implementer and independent
judge for a separate current-test repair, preserving the frozen comparison,
validator and completed transaction. A historical view must be explicitly
labeled, direct current snapshot staleness must remain detectable, and the
baseline-drift negative test must not pass merely because of an unrelated
already-known mismatch. All 39 numerical tests passed separately. There is no
all-pass claim at this stage and no forced scientific conclusion from testing.

The separate [registry-test repair review](../sources/textual_restoration/applications/genesis4_8_registry_test_repair_review.v1.json)
then approved only the current test-file diff. It adds four tests and makes the
corrupted-hash negative clean-first and specific. All 51 registry tests passed
for both implementer and judge; the judge independently reproduced the original
failure and confirmed that the unchanged standalone live validator still exits
1 with the exact Genesis baseline mismatch. Current registry/coverage/selection
checks and historical comparison checks are now explicitly separated. The
parent started a complete rerun of the selected research regression suite;
the later result must be recorded separately, not inferred from targeted passes.
The approach review now proposes an immutable-corpus snapshot interface and
component-specific dependency audit before bulk changes; no such broader
architecture was implemented in this repair.

The complete selected research rerun then passed: 446 tests in 186.482 s,
plus 39 numerical tests in 0.053 s, for 485 distinct tests. The
[regression receipt](../sources/textual_restoration/applications/genesis4_8_integration_regression.v1.json)
records exact module lists, runtimes, before/after outcomes and bindings.
Overlapping targeted runs are not counted again, and this is not a claim that
every repository test was run. Passing negative fixtures emitted simulated
refresh/push failures; those are distinguished from the genuine registry
failure. Parent final package/transaction validation and 13 new review-map
bindings passed. Only Genesis4:8 changed under translation in this checkpoint;
the two image packages changed no canonical source or English. Final reporting
review and Git publication are separate from textual/publication approval.

### 2026-09-06 — Samuel13:37 contrary controls and Leviticus identity targets

This follows the committed `d1ad333fc6c595f129bd5a7f883f85eecca5a295`
checkpoint, which was verified clean and equal to remote main at the start of
this pass. That prior turn made substantive progress; it was not a blocker.
The broader goal remains active and incomplete. This entry records source
research and documentation, not another canonical application.

The user authorized parallel research and independent judge loops. One agent
investigated Hebrew controls, one the remaining Leviticus catalogue holds,
and an independent agent checked source claims while the parent examined
Greek/Latin/Syriac editions and updated documentation. Reviews are contextual,
not blind or human-specialist certification. A reporting PASS must never turn
an unresolved source question into a scientific PASS.

The [Samuel Hebrew report](SAMUEL_13_37_HEBREW_CONTROLS_2026-09-06.md)
finds the exact4Q51 verse hit but the entire patronymic inside a supplied gap.
It also inspects the actual Aleppo publisher photograph, whose written form
appears resh-ending and whose marginal reading is different. The prior
Leningrad dalet fit remains source-specific, with its penultimate stroke held.
The initial Aleppo URL used the public one-based book number instead of the
reader script's zero-based number; actual1Kings text exposed the mistake.
That acquisition was rejected and the correct2Samuel image acquired. The
publisher's processing, private image/crop hashes, neighboring text and exact
rectangles are documented. No original raw camera file, Sassoon locus, or
fresh BHL AppendixA/modern Hebrew apparatus was obtained.

The [version report](SAMUEL_13_37_VERSION_CONTROLS_2026-09-06.md)
consults publisher Rahlfs–Hanhart Greek, Weber–Gryson Vulgate and CAL's
Leiden-derived Syriac text. Greek and Syriac have d-ending forms; Vulgate
has r-ending Amiur. Cambridge1927 pp149–150 and its preface additionally
report Old Latin Amiot, distinct Coptic forms and precise Greek/Ethiopic
supports. Independent page inspection corrected the working patronymic
group to include n and confirmed Old Latin final t. Mourning-clause variants
were kept in their own apparatus units across the page break. The ordinary
browser succeeded at CAL after web retrieval failures; unsupported tab export
was not presented as a successful page archive. Short observations, not a
full copyrighted chapter, were retained. Full modern apparatuses remain open.

Decision: hold Samuel's source/name bytes and earliest-form priority. A
Leningrad transcription correction, qere choice and historical reconstruction
are different decisions. A precise name-disclosure candidate and relocation
of the unrelated David-mourning note marker remain actionable next work,
but no exact candidate or new review status is approved here. The parent also
viewed the native Aleppo target crop with context; this repeats a contextual
check, not a new blinded witness. Contrary forms remain visible rather than
being resolved by a count of editions or reconstructed letters.

The [Leviticus report](LEVITICUS_CATALOGUE_IDENTITY_FOLLOWUP_2026-09-06.md)
obtains complete2005/2006 ArugLev publications through the Jeselsohn Center
and a2019 Cave11 publisher preview. Exact QDR/current-XLeviticus units now
map to edition targets, with A4 and ii12 discrepancies retained. Supplied
verse19 context is not surviving text. The actual P1038B fragment list
retains a Judges-or-Leviticus alternative; it is not a secure whole-label book
identification. Older box988/plate988a records are not equated with P1038B
by matching numbers. Failed download/security-check routes were not bypassed.
Actual Cave11 body arguments/photos, source-project alias documentation and
original ArugLev image questions remain open. The
[independent review](../sources/textual_restoration/discovery/leviticus_catalogue_identity_review.v1.json)
passes these bounded claims after actual edition/preview inspection and
integrity checks; it approves no physical merger or additional witness count.

The approach review, source-coverage audit, backlog and discovery index now
link these results. The central log remains the future About-link target;
no About page, public image redistribution, NT reading, registry count,
canonical text or executable code changed in this pass. Historical comparison
and application receipts remain frozen. The previous485-test regression is
historical evidence, not a fresh test result for this documentation checkpoint.
Final current checks and reporting review are recorded separately below.

The [combined Samuel review](../sources/textual_restoration/discovery/samuel13_37_controls_review.v1.json)
then passed the two exact reports and receipts with no mandatory repairs.
The judge independently inspected Aleppo pixels/crop reproduction, full QDR
bracket context, the published Greek/Latin pages and actual CAL browser row,
metadata and token, alongside Cambridge's pages/conventions. It confirmed
unchanged canonical bytes. This approves the bounded reporting, not a name,
source, note-anchor or earliest-form decision.

Parent checks passed: 27 file-hash checks, one archive-member hash, three
native-crop pixel-equality comparisons, and320 local Markdown targets across
the eight new/updated reports and central documents. These establish artifact
integrity and local link existence, not external URL availability or historical
priority. Current QDR discovery and UXLC/WLC comparison modules each passed
14 tests (28 distinct;0.003s and0.257s). No broader regression or fresh export
is claimed. A Git diff against HEAD confirmed no changes under translation,
tools, tests or sources/ot. Final review bindings and Git publication remain
separate from these checks and from any future source/translation decision.

### 2026-09-06 — Reviewed Samuel candidate, Genizah pilot and actual4Q122 images

The previous goal turn made progress: `b7ad6bd106b88ba90b6ecd9a1d3a82573cf7774e`
committed and pushed the reviewed Samuel/Leviticus research. This pass began
with a clean main at that commit. The full restoration/source-comparison goal
remains active; this is not a completion or blocker declaration.

Parallel researchers prepared an exact Samuel disclosure candidate and a
bounded Cambridge Genizah pilot while the parent followed an existing Greek
fragment target into actual images. The independent judge reviewed the
candidate and source packages against their actual evidence. No new model
identity or agreeing contextual review is treated as an ancient witness.

The [Samuel candidate](SAMUEL_13_37_DISCLOSURE_CANDIDATE_2026-09-06.md)
adds a name-variation note at Ammihur and moves the existing mourning note,
unchanged in body/reason, to “he mourned.” Conventional a/b order replaces an
initial design that would have kept the old note's letter but confused reading
order. Before/after records preserve that identity change explicitly. All
source bytes and marker-free English remain unchanged. Old review/status
values are archived without inventing their original input bindings; candidate
status is draft/needs_review. The old ai_draft and lexical blocks are preserved.
The record embeds exact original and proposed YAML, seven declared path changes,
input hashes,15 derivative contexts and full-book export results.

The [independent candidate judgment](../sources/textual_restoration/applications/samuel13_37_disclosure_candidate_review.v1.json)
approves only the exact6146-byte candidate, SHA256
`63d80b610ed4c20bc4da1b4716447727cdda57a70c1a75bd8545fc7b90c8ada1`.
Both author and judge exported the full24-chapter/695-verse book with one
in-memory overlay and checked every other exported row and the695-file input
manifest. Four negative mutations were rejected. Existing baseline schema
failure for `status: revised` was disclosed; candidate validation passes.
The exporter omits source metadata by design, so source equality was verified
separately. No executor or canonical write occurred. Exact application guards,
historical snapshot dependencies, derivative freshness and publication remain
separate gates; no earliest-name choice is made.

The [Genizah pilot](GENIZAH_BIBLICAL_CATALOGUE_PILOT_2026-09-06.md)
screens every description on the first Cambridge Genesis and Psalms search
pages:40 distinct shelfmarks. Approximate totals529/738 are overlapping keyword
universes, not an independently verified manuscript denominator. Only three
sampled descriptions qualify as fuller-text targets; the other37 remain
usable for the quotations, abbreviations, commentary or liturgy they actually
preserve. Two complete records, TEIs/manifests and contextual images were
examined. T-S B6.24 canvas1r bears handwritten2a and Genesis17:24–26 context,
supporting a local catalogue-folio2 alignment. T-S A43.8's last canvas has
nonadjacent Psalm contexts, not a verified Psalm145/nun-line locator.
Structured/prose column-count conflicts, bilingual Hebrew/Aramaic lanes,
server-limited whole images, native regional requests and image/metadata rights
are explicit. No representative sample, global census or new textual priority.
The [Genizah review](../sources/textual_restoration/discovery/genizah_biblical_catalogue_pilot_review.v1.json)
passes these bounded claims after actual queries, records and image checks.

The [4Q122 follow-up](4Q122_DEUT11_IMAGE_FOLLOWUP_2026-09-06.md)
acquires IAA full-spectrum/infrared images of plate265 fragment24 and the
scholarly Kraft thumbnail. They fit the same apparent physical fragment.
Received images are1200×1200, not the3296×3296 advertised tile pyramid.
The damaged middle line fits published Greek ERUQRAS contextually; locally
broken strokes, fragile identification, uncertain dating and missing full
DJD/associated-fragment controls remain explicit. No accepted new diplomatic
transcription or restored divine-name slot. Greek “red” does not prove a
Hebrew word for red, crossing geography, or the preferred English rendering.
Current DEU11:4's Sea-of-Reeds note is wrongly anchored after Egypt; that is
an identified but unapplied note-placement candidate, separate from lexical
adjudication. Old review scores cannot approve its future repair.
The [4Q122 review](../sources/textual_restoration/discovery/4q122_deut11_image_review.v1.json)
passes the exact source/image report and record, including11 private-asset
hashes and actual dimensions. It accepts no new transcription or text selection.

The parent browser was unavailable because the Mac was locked; ordinary
public-source HTTPS retrieval remained usable. Tov's author-PDF route failed
TLS hostname verification, which was not disabled. Failed web routes did not
become absence claims. An accessible BIOSCS PDF's opening page was visually
checked as an edition-search lead, not misreported as the4Q122 edition.
Manuscript images remain private; no generated or enhanced letters were used.
The PDF skill required visual inspection rather than trusting extracted text.

Fresh focused regression passed79 tests in0.387s: QDR discovery, UXLC/WLC
comparison and OT witness-registry modules. This is not a whole-repository
test result or another application/export receipt. The candidate's export and
negative checks are separately recorded; overlapping judge checks do not add
new distinct cases. Source/candidate reviews, final reporting checks and Git
publication are separate from scientific/source-selection approval.

Parent final checks also passed:21 private asset hashes/byte counts, nine
received image dimensions (including the PDF search-lead render),338 local
Markdown target occurrences across eight documents, two embedded YAML
hashes/byte counts,21 candidate input pins,15 derivative pins and the current
695-file Samuel manifest. Parent separately confirmed exact live baseline,
source/ai_draft/lexical equality, marker-free English equality and exact a/b
markers with the preserved old note body/reason. Link existence is not external
URL or heading-anchor validation; file dimensions do not certify manuscript
legibility. These are scoped checks, not new independent textual votes.

## Genizah local abbreviation and guarded Samuel preparation — 2026-09-06

The [Psalm77 follow-up](GENIZAH_PSALM_77_NAME_FOLLOWUP_2026-09-06.md)
advances the prior catalogue lead to actual institutional images, source-native
regions, same-leaf abbreviation controls and publisher-selected Hebrew/Greek
texts. The target is Hebrew77:8 = POB77:7. Two yod-like bodies occur where the
base has Adonai; a nearby Adonai slot uses alef/dalet. This supports a local
written-form difference, not four visible יהוה consonants or its exemplar's
wording. Occasional scribal/recitational substitution remains a counterargument;
Greek κύριος cannot discriminate the proposed Hebrew contrast. Priority is
held, current Lord retained provisionally, and no new note applied.

Cambridge attributes AS67.19 and four other sampled shelfmarks to one manuscript.
That is institutional relationship evidence, not a new independently verified
join or five votes. Both image sides and text order fit the catalogue's
back-to-front conservation warning. Copy dating remains unavailable in the
record. Initial incomplete-download viewing and crops needing supplementary
context are disclosed; successful completed assets, not partial views, support
the final report.

The [Psalm145 check](GENIZAH_PSALM_145_ABBREVIATION_CHECK_2026-09-06.md)
finds T-S A43.8's target on canvas2/1v using the title, acrostic context and
actual source-coordinate regions. The visible mem and samech entries are
adjacent; no separate nun row is between them. But the mem entry and nearby
entries abbreviate text. The result is therefore a located layout observation,
not secure continuous-copy omission evidence. No claim about every margin or
all eight canvases, no expanded shorthand and no historical-priority change.
This pass newly viewed canvases1/2; the prior pilot viewed8. Canvases3–7 were
not newly read once the target was located. The fresh native-coordinate regions
are institutional JPEG derivatives, not full raw masters or generated letters.

The method consequence is to inspect abbreviation at the decisive unit,
separate digital/physical/textual order, and preserve related-object statements
before counting support. Both manuscripts remain useful evidence without
forcing a source or English replacement. Images stay private under the actual
institutional terms; metadata CC0 is not image republication permission.

Samuel application preparation also exposed two integration hazards: the
exact approved candidate retains historical “unapproved-unapplied” proposal
metadata, and frozen Genesis guards pin a current test consumer. An application
must explicitly distinguish historical snapshot status from actual live state,
and must not silently weaken old input bindings to make tests pass. These are
implementation gates, not reasons to alter the reviewed name/source decision.
The [readiness record](SAMUEL_13_37_NOTE_APPLICATION_READINESS_2026-09-06.md)
pins the actual consumers and migration state. The implementation agent and
its bounded retry failed on transport before saving an executor or readiness
file. Parent read the actual dependency code and wrote the held readiness
record. No intent, virtual-applied test, canonical change, application receipt
or post-application export occurred. An initial lookup in the wrong manifest
returned null; the correct frozen migration record was then located and read.

The independent [Psalm145 judgment](../sources/textual_restoration/discovery/genizah_psalm145_abbreviation_review.v1.json)
and [Psalm77 judgment](../sources/textual_restoration/discovery/genizah_psalm77_name_review.v1.json)
approve the bounded reports, with no mandatory repairs. They accept neither
historical priority nor a new restored transcription. The judge's Psalm77
connection initially failed and its resumed turn completed the actual review;
the author also failed after saving the report/record, so the parent performed
and recorded its pending structural validation. No failed agent turn is
counted as a completed independent review.

Fresh parent checks passed79 tests: QDR discovery14 (0.002s), UXLC/WLC14
(0.241s), and OT registry51 (0.157s). Parent also verified10 repository input
pins,20 private asset hashes (including two reused inputs),18 new byte counts,
14 image dimensions, and13 exact source-review bindings. These are integrity
and regression results, not palaeographic truth or a whole-repository pass.
All inspected canonical/code/frozen-policy files remain unchanged.

The additional confirmed baseline process completed28 Genesis transaction tests
in167.668s and4 unflagged-sample tests in19.611s, all passing: **111 distinct
tests across five modules** including the79 above. During the longer run its
specific session remained live, produced progress and was re-polled; it was
not restarted on an observation timeout. This verifies the existing applied
Genesis state, not a virtual or actual Samuel application. The judge separately
verified the readiness report's five dependency pins and showed an injected
unknown test hash is rejected without changing the actual file. That diagnostic
is not an additional full test suite or a Samuel transaction approval.

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

### Existing B7.14 lead triaged without expansion — 2026-09-06

Parent inspected the interrupted agent's Genesis42:18 comparison, current POB
source/lexical rationale, and its two saved institutional image regions. The
visible Hebrew `זאת עשו וחיו` fits current “Do this and live”; `האלהים` in the
neighboring region is also compatible with the retained source. A generic
catalogue divine-name description therefore does not establish a Yahweh/God
variant at this unit. No source or main-wording change is justified by these
observations. This is contextual triage, not full diplomatic transcription or
approval of the unfinished six-image record. The square image was displayed
at1600×1600 from2000×2000; no fine pointing claim follows. Both asset hashes
matched the draft (main `d3c4bfca…be48080`, context `82cf8760…84f34c0`), stored
privately under `/private/tmp/pob-genizah-b714.nWiFws/`. Reopen for a specific
contrary reading, not merely more photographs. The broader draft stays untracked
and unapproved; no agents restarted or additional source requests were made.

### Bounded historical replay implemented — 2026-09-06

Added `tools/textual_restoration/replay_unflagged_sample.py` and four focused
tests. Run `.venv/bin/python -m tools.textual_restoration.replay_unflagged_sample`.
It extracts only required inputs from immutable Git commit
`574f204de77e89c8abba04c72209bdf5efb317f9` into a private temporary directory,
checks installed selector-code hashes, and compares the entire rebuilt receipt.
It never imports archived code, monkeypatches global file reads, or edits the
working corpus. Unsafe archive paths, links, special files, duplicate members
and mutable Git references are refused. Git replacement objects are disabled.

The first actual run failed equality: Numbers22:19 had already changed in the
receipt's commit. Its separately preserved baseline in that same commit matches
the receipt's original selected-file hash. The repaired replay verifies both
committed and baseline hashes, then substitutes that one file in the private
tree only. The second actual run passed full receipt equality:23,264 records,
historical digest `d7ba46056931eb8f23844b388ca2adeef5e6c7588e40ad3b6b5e8c6336fb5381`.
Four focused tests passed. No source interpretation or English decision changed.

One independent code review passed after the substantive repair. The judge
checked the actual Git baseline/target hashes, reran the four tests, and tested
five negative cases: changed baseline, committed target, selected path, selected
hash and nonselected receipt data. The full-corpus replay above is parent-run,
not duplicated as an independent experiment. Review of exact tool SHA256
`bea23f0b67c47f219f2914cdcc90e0ad54b2f55e670a1254bb23bac4134aab57`
approved historical reproducibility only; no additional review ledger was made.

This is historical reproducibility, explicitly **not** validation of current
corpus drift, transaction provenance, or permission to apply Samuel. Existing
frozen guards/tests remain untouched. Next integrate this separate historical
check with explicit current-state checks; do not present this tool alone as a
completed Samuel application. The untracked B7.14 draft remains untouched.

### Efficiency review and paused exploratory work — 2026-09-06

The maintainer requested a quick cost/value check. Git inspection found 4,871
insertions across32files in the last three commits, with no canonical changes.
The goal tracker reported16,505,374 cumulative tokens; this is its accounting
value, not a verified billing total. Active Genizah and snapshot-interface
agents were interrupted. The approach review now limits concurrency, repetitive
reviews, documentation duplication and open-ended case expansion. No scientific
or existing application gate was waived. This entry preserves prior work rather
than commissioning another evidence/reporting review loop.

Before the pause, public INTF queries retrieved a complete response for the
specific `featureCode=Liste` filter:6,146 distinct document IDs, matching the
separate count response. This is **not**6,146 surviving or independent Greek
manuscripts: the filter includes removed entries and T/Os appendix records.
The official UI supplied the filter; its search limit is measured in pages.
Raw responses remain private at `/private/tmp/pob-ntvmr-census.DPlLll/`:
`liste-feature-documents.json` SHA256
`d75a306fdb8b3789b6dc2f58f4d7f2979ff499f8db4fa79aa87af2248590fd13`;
`liste-feature-count.json` SHA256
`b0a133359e6268d23cfd43bd809c7cc5c5caf5d740837eeb5ef2c6d85b0a3705`.
Twenty-seven book-count requests also completed; no deduplicated book inventory,
manuscript collation or new Greek reading follows. The judge's preliminary
source check identified P14 as both Liste and Removed, and the institutional
[2024 appendix explanation](https://ntvmr.uni-muenster.de/intfblog/-/blogs/amulets-and-ostraca)
as a reason to retain category/alias distinctions. No exact NT package review
was completed and no catalogue data was publicly vendored.

The interrupted B7.14 agent left an untracked discovery JSON; it is preserved
as incomplete work, not committed or approved by this checkpoint. No snapshot
interface or Samuel executor was saved. Further exploration remains paused
while the next bounded translation-relevant deliverable is selected.

### 2026-09-06 — Remove the image-first routing conflict

Current-file inspection found that `TEXTUAL_RESTORATION_PRIORITIES.md` still
instructed “build the comparison system first” and applied fresh image passes
to every target, contradicting the approach review's efficiency correction.
Revised that operational document to default to published-source comparison,
reserve new image work for discriminating uncertainty, and label outputs by the
work actually done. Existing case-specific promotion/application gates remain.
Selected the existing 1 Samuel 1:24–25 dossier as the next substantive research
question: animal expression, bread and literary form must be assessed together;
the current verse and note were inspected, not newly adjudicated. Samuel 13:37's
application tooling remains held. No new external sources, manuscript readings,
canonical changes or generated images in this pass. Validation: local-link and
diff checks, plus one bounded independent method review. The reviewer caught a
too-categorical image exemption; corrected it to require image checks for claims
depending on disputed marks, corrections, joins or fresh decipherment. The
reviewer checked that repair and returned PASS for method consistency only.
No corpus test rerun for these prose-only changes.

### 2026-09-06 — Test the Samuel singular-bull argument

Extended the existing [Samuel dossier](SAMUEL_SOURCE_COMPARISON_PASS_3.md#grammatical-counter-control-and-bounded-decision--2026-09-06),
not a new framework. Visually checked Yale's printed pp. 36–37 and verified
its Numbers 21:6–7 grammatical control against local WLC; also checked Genesis
15:9–10 and the current Samuel wording. A singular noun can refer back to a
plural group, so Samuel's singular does not alone justify emending verse 24.
That possibility does not prove collective reference in Samuel or MT priority.
Ratner's original article remains access-limited. Retain source/English and
the existing disclosure provisionally; animal, bread and narrative decisions
remain separate. PDF provenance and precise reopening requirements are in the
dossier. No images or external PDFs vendored; no canonical changes or corpus
test rerun. Local links and diff checks passed. The independent reviewer checked
the rendered Yale argument, PDF hash and local Hebrew against the stated revision,
and returned PASS for this bounded addition, not source selection or publication.

### 2026-09-06 — Job 13:15 source-local alternative

The [Job comparison](JOB_13_15_SOURCE_COMPARISON_2026-09-06.md) verifies both
ketiv and qere in vendored OSHB/WLC, compares the pinned Greek clause and local
verb contexts, and identifies a misleading original-language-versus-tradition
rationale in current POB. The qere is Hebrew-source evidence, not merely an
English preference. Proposed a clearer note/rationale without adopting either
historical priority or a new English rendering. Canonical application, full
apparatus, physical-witness coverage and independent versional inference remain
open. Exact inputs, consulted context and failed retrievals are in the case
record. No generated images or new validation framework. Local links and diff
checks passed; the independent reviewer verified XML/YAML, contextual controls,
the Greek download and all three hashes, returning PASS for the report only.

### 2026-09-06 — Migrate historical test consumers without changing evidence

Implemented the [historical-test migration](HISTORICAL_TEST_MIGRATION_2026-09-06.md)
and a separate live completed-note audit; three current test entrypoints now
separate snapshot checks from current behavior. An implementer was interrupted
after producing no files; the parent completed the code. Under simulated exact
Samuel-candidate reads, 105 parent tests passed, including wrappers executing
37 original tests against fixed Git bytes. Full-2SA baseline/candidate exports
matched; actual canonical bytes/digest stayed unchanged. An export-field typo
after the successful tests was corrected and its assertion rerun separately.
Independent review required restoring live target/package integrity and a
missing application-document pin; both repairs passed. The final live suite's
five tests passed in 19.867 seconds, including actual full-GEN export; the final
83-file integrity check also passed under virtual Samuel reads. This is a
tested consumer migration, not Samuel application, source-selection approval or
publication. Existing receipts/executors remain unchanged; no source research,
ImageGen, new per-verse overlay or canonical edit was added.

### 2026-09-06 — Apply the reviewed Samuel name disclosure

After the maintainer's renewed efficiency check, closed the existing application
rather than starting another research or infrastructure task. The exact reviewed
candidate is now in `translation/ot/2_samuel/013/037.yaml`: an 84-word name-variant
note and the unchanged mourning explanation anchored at “he mourned.” Hebrew,
marker-free English, lexical decisions and the original AI draft are unchanged.
Old review flags are archived, not reused to certify the edited verse.

The [scoped transaction review](../sources/textual_restoration/applications/samuel13_37_transaction_review.v1.json)
approved the exact implementation before application; no new research judgment
or repeated independent review was requested in this pass. The existing prepared
intent was verified, the exact candidate applied, and `confirm` followed by the
read-only `check` succeeded. The [application record](../sources/textual_restoration/applications/samuel13_37_application.v1.json)
records the live scoped state. The embedded `note_proposal` block is historical
preparation metadata as specified in the reviewed
[contract](SAMUEL_13_37_NOTE_APPLICATION_2026-09-06.md), not current status.

Actual post-application OT digest:
`ebc5a784b4f4dc8773c6818297fb2d5e531329a685ab016171c6ee6f2df496c4`.
Actual complete 2SA export (24 chapters, 695 verses):
`a434d6e5d515c8d1fd5135c07dd6d8e56ae12036d641d70a077895e5fc102289`.
The current 83-file prior-note integrity check passed. A single real-checkout
integration batch passed 121 parent tests in 245.309 seconds: Genesis transaction,
unflagged sample, witness registry, Genesis candidate, Numbers application,
Jeremiah transaction, historical replay, sample replay, live integrity and Samuel
transaction suites. The historical wrappers also executed 37 original tests in
their immutable snapshot; these do not validate the current corpus. Current
export/integrity checks ran separately from those historical snapshots. Internal
Samuel tests simulate both allowed states; the actual post-application `check`
provided the live-state evidence. Diff whitespace checks passed.

Fifteen derivative contexts remain pinned but unsynchronized; no deployment,
source-priority decision, whole-verse reapproval or new manuscript reading.
Preserved the unrelated untracked B7.14 discovery draft. Updated the approach
review's current application status and reiterated that bespoke per-verse
transaction machinery is not the default. The broader OT/NT inventory,
comparison and confidence-calibration work remains incomplete; the next research
pass should address discriminating evidence, not add another framework.

### 2026-09-06 — Test Job's waiting interpretation against published arguments

Extended the existing [Job comparison](JOB_13_15_SOURCE_COMPARISON_2026-09-06.md#published-counterarguments-and-book-wide-verb-control--2026-09-06).
Read NET notes 1–3, the authorized Reyburn/UBS excerpt, and the reproduced
Cambridge commentary's section 15. Reproduced all eight direct-word Job XML
occurrences annotated with lemma 3176 and read 13:13–19. The Cambridge waiting
argument concerns a potentially earlier fatal confrontation; it is not blanket
endorsement of POB's explanation. The Hebrew controls allow desired expectation
within waiting. Thus negation alone cannot choose waiting over lost hope, and
qere alone cannot compel hopeful trust. Identified the live source-audit summary,
alongside the theological rationale, as needing a later scoped correction.
Retain main text provisionally; the existing note proposal remains unapplied.
Historical priority still requires discriminating apparatus/versional evidence.

XML/YAML hashes remained unchanged; exact locus/form assertions, local links
and diff checks passed. The independent reviewer checked the three published
arguments and reproduced the XML controls, returning PASS for the addition only.
No new receipt, application tooling, corpus test run, manuscript transcription,
image generation or canonical change. Cambridge print pagination and reported
version support were not verified; no such claims were adopted. Corrected stale
priority-document references to the now-completed Samuel application. The
unrelated B7.14 draft remains untouched.

### 2026-09-06 — Proverbs 8:16 source variant, not an English synonym

Added the [Proverbs comparison](PROVERBS_8_16_SOURCE_COMPARISON_2026-09-06.md)
and linked it from the existing casebook. Read the published critical apparatus
and its competing NET argument; the PDF skill prompted visual verification of
the decisive printed pages. Checked local Hebrew context and parallel phrases,
and the existing pinned Greek surface text. The earth alternative is reported
within Hebrew transmission; it is not merely another translation of justice.
POB's lexical note does not disclose that difference. Proposed a source-variant
note, while retaining source/main English because assimilation and thematic
arguments do not conclusively establish direction. No fresh restoration claim.

The independent reviewer verified current Proverbs YAML/XML, NET, pinned Greek
and rendered Fox pp. 154–155, returning PASS for the report, not application.
Ancillary sigla/policy pages, local parallels and edition-status checks are parent
checks, not independently repeated review. Exact inputs, retrieval failures,
unconsulted witnesses and reopening conditions are in the case record. Target
and Hebrew hashes, final-word/no-qere assertions, local links and diff checks
passed. No canonical edit, new transaction code, corpus-wide tests, external
corpus vendoring or generated reconstruction image. Preserved the B7.14 draft.

### 2026-09-06 — Consult the Hebrew transmission report behind Proverbs 8:16

The [Proverbs follow-up](PROVERBS_8_16_SOURCE_COMPARISON_2026-09-06.md#norzis-correction-reports--follow-up-2026-09-06)
now reads Norzi's Aramaic/Hebrew commentary directly in its digital edition.
It reports corrections in both directions and combined readings, making these
documentary evidence rather than only hypothetical explanations. Preserved both
public-domain source segments in a compact snapshot: the available community
English translation omits the second. No website chronology was imported and
no physical erasure was claimed. This is the same underlying report used by
the critical edition, not an additional independent ancient witness.

Keep source/main English and the existing unapplied note proposal unchanged;
further source selection needs identified witness/hand evidence. Direct API
retrieval succeeded after web-reader failures. Source-segment and phrase checks,
canonical hash, local links and diff checks passed. The independent reviewer
reproduced both segments and the complete response hash, returning PASS for the
addition and snapshot only. No new framework, image work or corpus test run.

### 2026-09-06 — Route Greek apparatus acquisition across all OT books

Extended the [existing coverage audit](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md#greek-apparatus-routes-for-all-39-pob-ot-books--2026-09-06)
with a dated book-to-edition route: 17 volumes on Göttingen's current publication
list cover 30 POB books; IOSCS supplies fallback/alternate routes for the other
nine. A direct assertion checked all 39 repository book directories occur once.
Mapped Esdrae II and Threni explicitly and noted the IOSCS Reigns label error.
FAU's catalogue clarifies that Psalms 2025 is a reprint with a supplement, not a
newly collated biblical text. Publisher links returned 403; no apparatus was
acquired or passage re-adjudicated. An incidental project blog was opened while
locating the Psalms edition; its unrelated variant discussion was not promoted
into evidence or a new case.

The independent reviewer checked the exact routes/dates against the official
lists and the Psalms qualification against the library record, returning PASS.
Local-link and diff checks passed. Corrected the audit's obsolete Samuel-note
application statements. No new framework, manuscript counts, text restoration,
canonical changes or corpus test run: this closes a routing gap, not the broader
inventory, apparatus-access or collation gaps.

### 2026-09-06 — Prepare the exact Job disclosure correction, stop at integration

Following the efficiency check, converted the existing Job findings into one
[full-record candidate and reviewed outcome](JOB_13_15_SOURCE_COMPARISON_2026-09-06.md#exact-disclosure-candidate-and-editorial-review--2026-09-06).
Rechecked the actual Job XML ketiv/qere and the NET/authorized Reyburn notes.
Corrected the proposed reader note and lexical/theological/audit explanations;
retained Hebrew and main English, and archived old review objects without
reusing their scores as candidate approval. No additional manuscript claim.

One independent reviewer passed exact candidate bytes for editorial scope only.
Schema, field-preservation and marker checks passed. Actual and separately
simulated Job exports each cover 42 chapters/1,070 verses; only the proposed
footnote differs. Hashes and the one-record simulation boundary are in the case
record. Canonical YAML, executables, tests and derivatives remain untouched.

The existing Samuel current-state verifier hashes every OT verse, so a disjoint
Job application would invalidate its frozen corpus check. This is an identified
integration constraint from inspecting the verifier, not a failed application
or a reason to repeat research. Did not relax its bindings or create another
per-verse tool. Next enabling work is a separately reviewed successor-state
mechanism preserving prior package verification. Job editorial preparation stops
here pending that integration; main-English selection and historical priority
remain unresolved on their separate evidentiary grounds.

### 2026-09-06 — Unblock successors and apply the Job disclosure correction

Completed one enabling implementation and its consequential editorial outcome.
The reusable [successor verifier](CORPUS_SUCCESSOR_VERIFICATION.md) checks the
current OT state against a fixed Git checkpoint plus an exact, independently
reviewed note/metadata plan. It preserves frozen Samuel records and all prior
completed-note obligations; only the reviewed Samuel test consumer is migrated
to run the original eleven tests in an actual checkpoint archive. Explicit
trusted review/application hashes prevent mutable plans or stale receipts from
silently certifying changes. This is not textual-confidence measurement.

Independent `/root/successor_review` approved the exact mechanism and Job plan,
including source/main-English/history preservation. Preserved the actual
baseline verification, applied the already reviewed candidate using apply_patch,
then verified the actual candidate corpus and complete Job/Samuel exports.
The [Job case record](JOB_13_15_SOURCE_COMPARISON_2026-09-06.md#scoped-application-verified--2026-09-06)
links the plan, approval, preflight, application record and reproducible command.
Only the Job reader note and related metadata change; Hebrew/main English and
historical revision entries are retained. Prior reviews are archived, not reused
as full-verse approval. No derivative synchronization or deployment.

Initial tests exposed a missing Genesis derivative dependency in the historical
archive, a schema-exception expectation and the temporary directory's macOS
symlink alias. Fixed those failures rather than counting them as passes. Final
post-application integration passed 13 parent tests in 53.631 seconds: twelve
current successor tests plus a wrapper running all eleven original Samuel
tests. Five prior live-integrity tests and eight reader-footnote tests also
passed during pre-application validation. Checks cover scope, protected bytes,
full exports, malformed/unapproved states and rollback, not scholarly truth.

No new apparatus or image claim was needed. Stop Job disclosure work here;
the separately unresolved source-priority and complete-English questions retain
their original reopening criteria. The earlier broad-corpus blocker is resolved
for this reviewed successor path, not hidden by repinning old receipts.

### 2026-09-06 — Compare Amos 9:12 with the Greek forms and Acts quotation

The [Amos comparison](AMOS_9_12_SOURCE_COMPARISON_2026-09-06.md) answers a
consequential source question without another application framework. A bounded
Hebrew-control agent checked pinned QDR coverage and the versioned primary
transcription: Mur. 88 supports Edom as unbracketed text, but only the verb's
ending survives in that transcription. Its supplied beginning cannot establish
“possess” over “seek.” The pinned 4Q82 record supplies no 9:11–12 anchor; related
9:11 quotations are not direct 9:12 noun/verb witnesses.

Inspected the original Swete vol. III page 27 image and its apparatus. The main
Greek text lacks an explicit seeking-object, while Swete reports “the Lord” in
Alexandrinus; Acts explicitly has that object. The local AI apparatus string
`των αν` is a corruption of printed `τον κν`. Recorded an erratum while preserving
the original model output and its provenance. No physical codex image or modern
Göttingen apparatus was consulted; no Greek form was retroverted into supposedly
surviving Hebrew. Existing POB Amos/Acts main translations are retained.

Independent `/root/amos_comparison_judge` inspected the original Greek scan,
primary Hebrew HTML, WLC and canonical records and passed the exact report
SHA256 `0772baf858136279d56f95a534156f2fe57fda4c96619aa3cb4798c555eb477d`.
Local links, canonical/input hashes, WLC no-qere and Acts object checks passed.
The report records unavailable NET/web-reader access and the successful direct
HTML retrieval after an unavailable parser dependency. No canonical, source-data,
executable or test change; no corpus-wide test run, ImageGen or deployment.
Stop at retain; only discriminating new evidence reopens historical selection.

### 2026-09-06 — Isaiah light recommendation and renewed efficiency stop

The [Isaiah 53:11 comparison](ISAIAH_53_11_LIGHT_COMPARISON_2026-09-06.md)
provisionally favors the attested Hebrew object אור, “light.” Two published
Hebrew transcriptions preserve the complete word; a third supplies partial
support. Greek supports light with different syntax. The report preserves the
contrary clarification/expansion explanation and separates published readings
from fresh manuscript inspection. No canonical source or English was changed.
Independent `/root/isaiah_light_judge` passed report SHA256
`97764669c753de18ea538eb8f90d817898d8c9ed1bb930df0368060f89757c0d`;
this is a research-report verdict, not approval to apply a full verse.

The maintainer again requested a quick efficiency check. The goal tracker now
reports 17,991,140 cumulative tokens, versus 16,505,374 in the earlier check:
1,485,766 additional reported tokens. These are tracker values, not a verified
billing total or per-deliverable attribution. Recent work produced a Job
disclosure correction, an Amos retain decision and this Isaiah proposal, but
that does not justify calling the overall process efficient. Repeated review
and application bookkeeping have consumed disproportionate effort.

Stop additional exploration at this checkpoint; all current subagents are
completed or interrupted. Save the finished report without another judge loop,
framework, corpus-wide test run or new research task. For resumed work, use one
prioritized textual question, one concise case record, and at most one initial
independent review; re-review only a concrete substantive defect. Start each
batch with an explicit effort ceiling and expected decision, then stop at
retain, propose or unresolved. Reopen only for evidence that could change the
decision. Research completeness and the larger project goal remain unclaimed.

### 2026-09-06 — Concrete Isaiah candidate and identity-blinded English review

The previous pass completed a reviewed source-unit report and an efficiency
stop (progress, not a verified wait). Goal continuation resumed with one
deliverable and a roughly ten-minute effort ceiling: materialize the existing
Isaiah finding, without new source acquisition or application infrastructure.

The [complete candidate](../sources/textual_restoration/applications/isaiah53_11_candidate.v1.json)
is an unapproved WLC-based editorial composite, labeled `POB-critical-draft`,
not WLC. Its unpointed source adds only אור; the English adds only “light.”
Both footnote anchors now attach to their own phrases. The exact original
source and English are retained in the candidate's baseline block; Git
`78732e3150576aea40c690de957add7373c63a0f` preserves the full original record.
Historical draft/revision data are preserved, old status/review metadata are
archived without claiming verified original review-input bindings, and the
candidate has no inherited 0.95 approval. The earlier lexical claim “he himself”
is aligned with the unchanged sentence's “he”; that stronger alternative remains
documented. The knowledge rationale no longer claims the suffix settles its
interpretation. Unchanged lexical entries are carried forward, not newly checked
against their named lexicons.

Before review, the contract fixed the proposed consonantal source, retained
base analysis elsewhere, a close gloss, Isaiah 53:10–12 context, and POB's
source-fidelity/ambiguity/readability policy. Inputs are the verse records at
the Git revision above. The reviewer received the source and context, not the
current POB identity or the source-selection report. Meaning and unsupported
additions took priority over literary effect, readability and consistency.
One fresh agent, `/root/isaiah_full_english_review`, assessed these anonymous
sentences in A/B/C order; no repeated-order experiment was performed:

- A: “From the anguish of his soul he will see light and be satisfied; by his
  knowledge my righteous servant will justify many, and he himself will bear
  their iniquities.”
- B: “After his suffering he will see the light of life and be satisfied; by
  knowledge of him my righteous servant will justify many, and he will bear
  their iniquities.”
- C: “From the anguish of his soul he will see light and be satisfied; by his
  knowledge my righteous servant will justify many, and he will bear their
  iniquities.”

Actual verdict: slight preference for C, with A defensible and neither blocked
under the supplied source/analysis constraints. A's “himself” makes plausible
emphasis more explicit than necessary. B selects a temporal relationship,
adds “of life,” and chooses the alternative knowledge interpretation; the
reviewer rejected it for this narrowly sourced candidate. C preserves the light
image and leaves the disputed character of justification open. This confirms
the minimal candidate preference, not earliest Hebrew priority.

The reviewer retained three cautions: knowledge-of-him remains consequential;
attachment of the knowledge phrase to satisfaction rather than justification
remains a clause-level question; “the many” would represent the article more
explicitly. None was judged a blocker while retaining the stipulated base
analysis. “From” was preferred to the more determinate “after.” The light note
must distinguish Hebrew attestation from the Greek's different construction;
the candidate does so. One AI review of supplied sentences and summaries is
not independent witness verification, a calibrated translation benchmark, or
approval of every field in the full candidate. Existing full-source/editorial/
English-promotion/export gates therefore remain pending.

Read-only checks passed: exact pinned baseline and report, normalized Hebrew
with only the object addition (including retained final punctuation), English
with only “light” added after removing markers, correct unique note anchors,
unchanged original AI/revision history, and exact archived review values.
Candidate SHA256:
`34d14ddf897b5f1c5fb0b07f0012ae3428ed929bd9762f53cf39130e815de706`.
The current verse schema rejects only the candidate's honest critical-draft
edition label; the enum was not loosened to force acceptance. No actual export
or canonical application was attempted. No fresh web, image, lexicon, code,
test framework, or publication work. Stop here; the next enabling decision is
the existing shared critical-source representation/application gap, not another
Isaiah attestation search or review loop.

### 2026-09-06 — Shared Hebrew composition contract, not a promotion shortcut

Previous turn: progress through the complete Isaiah candidate and independent
English comparison. This continuation implements the base-plus-patch provenance
portion of the critical-source integration gap. The production schema and
application gap are **not closed** by this change.

One [composition bundle](../sources/textual_restoration/applications/source_compositions.v1.json)
now binds the existing Isaiah and Deuteronomy candidates to their exact canonical
baseline bytes and evidence records. One
[read-only verifier](../tools/textual_restoration/verify_source_composition.py)
reconstructs both sources. The contract explicitly normalizes using Unicode NFD,
removes combining marks and slash token separators, and retains consonants and
punctuation. Patch offsets count Unicode code points in that normalized original
base; ordered, nonoverlapping patches carry exact before/after text and evidence
indices. No intermediate-string offset drift or unlisted source edit is allowed.
This is a common representation for two existing cases, not another per-verse
application executor. Candidates, old schemas and frozen receipts are unchanged.

Pins establish which documents were consulted, not whether their claims are
true. Matching the source proves composition only; it does not prove historical
priority, legitimate rights, correct English, or independent editorial approval.
The verifier accepts only unapproved Hebrew research candidates and cannot write
canonical files or waive pending gates. It rejects composite-as-WLC labels and
inherited current approval scores. Proposed readings remain proposed. Images
cannot serve as the manifest's textual provenance records, but file type/hashing
alone cannot establish that a textual document used legitimate evidence; that
remains an editorial check. No generated image was used in this pass.

Seven focused tests passed, including both real candidates, normalization,
multi-patch coordinates, overlap/mismatch, missing evidence, pin drift, unsafe
paths, symlinks, and repinned-but-unexplained candidate changes or approval flags.
These checks do not replace the existing whole-record application requirements.

The unchanged actual mobile exporter was also exercised across Isaiah with a
single in-memory candidate overlay: candidate English and note bodies survive,
and all other exported book content is unchanged. The full source object is
absent from that payload; no deployed reader was inspected. Exporter SHA256:
`4f77493c1818896d63f5df1e229225a3034559b059f8cd20038f4cd1df06b20c`.
No exporter modification, bundle write, schema relaxation or canonical edit.

Reproduce from the repository root:

```bash
.venv/bin/python tools/textual_restoration/verify_source_composition.py sources/textual_restoration/applications/source_compositions.v1.json
.venv/bin/python -m unittest tests.test_source_composition
```

Independent `/root/source_composition_review` passed the bounded contract after
running all seven tests and the CLI, with no substantive defects. Exact tool
SHA256: `e35fbe38d0a0b33a6eb6ed7653ebb4f1a6e391f259093918cc69fa97291d4195`.
The reviewer confirmed there is no canonical write path and did not claim
production compatibility or evidence truth. System Python lacks PyYAML; the
documented repository virtual environment works. No repeat review was needed.

Stop after this shared validation step and its independent code review. The
next integration must connect verified provenance and actual editorial review
to the production source representation and reader disclosure; changing only
an edition enum or treating this composition result as approval is insufficient.

### 2026-09-06 — Isaiah editorial approval and existing source-page path

Previous turn: progress through shared source composition verification. This
pass closes a different question: whether the complete candidate is editorially
adoptable, rather than whether a research report is accurate or its strings
recompose. The independent agent `/root/isaiah_editorial_gate` approved the exact
candidate for **provisional source selection and full-record editorial adoption**.
The [review record](../sources/textual_restoration/applications/isaiah53_11_editorial_review.v1.json)
preserves the actual decision, input pins, counter-explanation, unchanged-base
scope and cautions. No new source search or manuscript reading was commissioned.
Knowledge attachment and “the many” were judged nonblocking under the declared
base analysis. No substantive new source/English prerequisite was identified.
Technical application and publication approval remain false. The candidate's
preparation flags are not rewritten; the external review is the later decision,
not permission to treat every old pending flag as complete.

Read-only inspection of `cartha.website` at
`25bb34e1cd769dde85dbd72e23bb56cd60582add` found an existing source-record route,
which narrows the earlier lightweight-export gap:

- `BibleReader.jsx`, lines 1578–1590, 4971–4975 and 23029–23038: “Check
  Provenance” opens `/peoples-open-bible/verse?ref=ISA.53.11` for this verse.
- `bibleData.js`, `parsePobProvenanceRef`: source references resolve to canonical
  verse YAML paths. The ordinary reader's separate POB footnote-stripping branch
  remains present; this finding does not repair or deny that branch.
- `verse/page.jsx`, lines 101–126 and 258–284: the route loads the canonical
  YAML from the repository's main branch and its body displays source text,
  edition and apparatus. It also renders footnotes and links the raw YAML.

The actual `VerseProvenanceBody` was server-rendered with the unchanged candidate
as props using installed Next SWC and ReactDOM. The whole JSX module was compiled
as CommonJS (ECMAScript JSX parser, classic React transform); framework imports
for navigation/theme/footer and the unused route-data import were stubbed, while
the actual body, helpers and styles executed. This was not a full Next route,
network fetch, browser interaction, visual-layout check or deployment. Results:
Hebrew text, draft edition, every apparatus note, both footnote bodies and the
raw-YAML link were present. The full `source.note` composition disclosure was
absent. Thus absence from the mobile payload does **not** establish absence of
an accessible source path; the existing page avoids needing a new provenance
reader. It still needs deliberate composite-source disclosure and deployed-path
verification before publication. No website or other repository was modified.

Exact inspected website file SHA256 values:

- `src/app/(main)/peoples-open-bible/verse/page.jsx`:
  `6c57d7407f960e9c88c54e381420f5777536572c8913ad1c8f1a268c7b442c0e`.
- `src/app/(main)/peoples-open-bible/bibleData.js`:
  `9d97b47c95ce9a3c5b37010846229c4acbce731dd9490dc3dcb5606ebb957d97`.
- `src/app/(main)/peoples-open-bible/BibleReader.jsx`:
  `dceb26ab849cb30966b8539f3afb27dc5043e36922a1a950aa45678ccff18775`.

The shell had no Node on PATH and local Babel packages were unavailable; the
bundled Node executable and existing Next SWC worked without installing anything.
Review input hashes and scope were checked against current files; the canonical
Isaiah baseline remains unchanged. Stop at this editorial approval plus precise
reader-gap finding, with production source/application integration still open.

### 2026-09-06 — Display the existing source-composition disclosure

Previous turn: progress through Isaiah editorial approval and the missing
`source.note` display finding. Implemented that specific shared reader change
in `cartha.website`, `src/app/(main)/peoples-open-bible/verse/page.jsx`: render
nonempty string notes as labeled, escaped text below the Hebrew/source text.
Exterior whitespace is trimmed; interior line breaks are retained. Missing,
blank and nonstring notes create no empty disclosure. No script/HTML execution,
new source claims, Scripture edits, footnote-filtering policy change or About
integration is part of this patch.

The new `test/pob-provenance-source-note.test.mjs` compiles the actual page with
Next SWC and server-renders its actual body with React; it checks preservation
of the source, apparatus and footnotes, record nonmutation, missing/malformed
notes and HTML escaping. Together with the existing source-text and original-
source-YAML tests, eight focused tests passed. The actual unchanged Isaiah
candidate was separately supplied to that component: its source note, Hebrew,
all apparatus notes and both footnote bodies now render. Framework route
dependencies were stubbed; no full-route fetch or browser layout test is claimed.

Independent `/root/source_note_ui_review` returned PASS after running the same
eight tests and inspecting the bounded change. Page SHA256:
`d9514dbefb47224ab8d8161b18c71325e0c1938d2d9f11d427da9cff17c348b7`;
new test SHA256:
`c4dde108e8257c565a854d89b4668d0963a160904648a82b9d185b59f0c976e0`.
Website implementation commit `f043e3df` was merged with current remote main
without target-file conflicts and pushed as `d07491b948d22e49cf4d1d5db37fb73be3f98fb0`.
The eight tests passed again after integration and the reviewed page hash stayed
identical. Unrelated upstream website/bundle changes were preserved, not authored
or reviewed by this task.

The website workflow documentation says main is picked up by a scheduled
deployment. The user was informed before push; no deployment was manually
triggered and no live release was verified. This closes the local component's
missing-note behavior, not deployed disclosure or the source-schema/application
requirements. The canonical Isaiah verse and its candidate remain unchanged.

### 2026-09-06 — First strictly verified, provisionally reviewed Hebrew source record

Previous turn: progress through the source-note renderer repair. This pass adds
the source-record portion of production integration without loosening the
historically pinned canonical verse schema or rewriting completed receipts.
[Isaiah 53:11](../sources/ot/pob_critical/isaiah/053/011.json) is now the first
record in a deliberately partial `sources/ot/pob_critical` corpus. It contains
the exact editorially approved Hebrew and apparatus, explicitly labeled
`POB-critical`, with a provisional composite-source disclosure. This is one
reviewed source record, not all Isaiah, a canonical English change, a new
manuscript discovery, or publication approval.

The [strict source schema](../schemas/ot-reviewed-critical-source.schema.json)
requires provenance rather than merely accepting a new edition string. The
[read-only validator](../tools/textual_restoration/reviewed_critical_source.py)
checks the actual editorial review, candidate, evidence and explicit composition.
It reads the original canonical base from its pinned Git revision and verifies
its exact bytes, preserving provenance after a future live-verse change. The
source text and apparatus must equal the reviewed candidate; only source-stage
labeling and the specified generic composition disclosure differ from the
historical draft. Application/publication authority remain false.

Independent `/root/reviewed_source_contract_judge` found a substantive first-pass
defect: although approved text was protected, a replacement composition bundle
could describe a whole-verse patch, cite the candidate itself, and be repinned
inside the source record. Fixed this by requiring a separately trusted composition
hash as well as the separately trusted editorial-review hash. A mutable source
record can no longer select its own replacement provenance. The exact bypass
is now a regression test; no editorial judgment was changed to make tests pass.

The reviewer rechecked that repair and passed. Sixteen focused tests pass,
including actual records, malformed source/provenance, text/apparatus drift,
approval boundaries, replacement-plus-repin, multiple-patch coordinates, and
use of the Git baseline rather than a live canonical-file pin. No broader
corpus or deployed-reader claim follows. Final validator SHA256:
`b15c6b416adf5e260ba035f38f64b34d96a1ee68720d4c8150805d1cd34d54d1`.
Schema SHA256: `bf56e6e1d4d71bb8ec0600c5d4b8017ebef957ebd5532c09afe7bb79d822d1fc`.
Source record SHA256: `f7014f607b0344d8a3b5723cd7edcc314029916dfeee4c341d9dd9b394f0f9e9`.

The [corpus README](../sources/ot/pob_critical/README.md) gives the exact
verification command and trust inputs. Existing research candidates and old
schema/tests remain unchanged. Next integrate this verified source object with
the full canonical verse and reviewed application mechanism; source-record
acceptance alone does not finish that migration or synchronize reader editions.

### 2026-09-06 — Full critical-verse schema and exact candidate integration

Previous turn: progress through the first reviewed Hebrew source record.
Added the [alternative full-verse schema](../schemas/ot-critical-verse.schema.json)
and [in-memory integration](../tools/textual_restoration/critical_verse.py).
All legacy non-source field contracts are reused through an explicit offline
schema registry; the source uses the strict reviewed-source contract. The full
record must also link its independently trusted source record. No permissive
edition addition or modification of the frozen old schema was made.

The approved candidate is copied in memory, replacing only its source with the
reviewed source-stage representation and adding a provenance link. Every English
phrase, footnote, rationale, draft history and current review flag is retained.
The old restoration-draft block is explicitly historical preparation, not the
current source-selection status. No additional full-candidate artifact is saved.
Validation requires externally supplied source-record, review and composition
hashes; equality to the approved integration is checked after schema validation.

Independent `/root/critical_verse_integration_judge` found a real first-pass
defect: Python dictionary equality allowed a historical false flag to become
JSON number zero. Replaced it with type-sensitive canonical JSON comparison,
rejecting nonfinite values. Added regression cases for preparation and archived
review flags. The reviewer rechecked the specific repair and passed; all 24
focused tests pass. Final integration-tool SHA256:
`e30b17f3bce07a6617f98ea359c2872ece47113fb7a52338b33ef4595dd0d68b`.

The full integrated record also passed the actual full-book Isaiah exporter
with a one-record memory overlay: English and note bodies survive and all other
exported book content is unchanged. The lightweight payload still omits the
source object, whose existing provenance-page path was addressed separately.
No canonical write, asset synchronization or deployed-reader claim was made.

Read-only inspection of the frozen safeguards confirmed Isaiah 53:11 is not in
the Samuel or three-note protected-file pins, but the old verse schema is pinned.
The current successor verifier explicitly forbids source/main-English changes.
That is the remaining application boundary, not a failed source or full-verse
schema decision. This pass does not repin old reviews or claim the note-only
transaction can already apply Isaiah. Next implement the explicitly reviewed
source-changing successor while preserving the prior completed-note checks.

### 2026-09-06 — Efficiency reset and actual Isaiah 53:11 application

The user asked whether this work was proportionate to its cost. A read-only
audit found valuable source decisions and real defects caught by review, but
also diminishing returns from successive validation layers while Isaiah was
still unapplied. The goal tracker reported approximately 18.37 million cumulative
tokens; that is not a billing figure. This pass therefore finishes the existing
case without new manuscript research or another general framework.

Working rule going forward: prioritize comparisons that can change a source
reading, English wording or explanatory note; reuse the existing source and
application contracts. Use one independent review per bounded deliverable and
repeat it only for concrete repairs. Record concise decisions and link evidence;
do not duplicate prior dossiers or count infrastructure as textual progress.
The previous status-only exchange supplied evidence for this change of course,
not a new textual result. ImageGen remains inadmissible as manuscript evidence.

Applied the exact [integrated Isaiah candidate](../sources/textual_restoration/applications/isaiah53_11_full_record.v1.yaml)
to [the canonical verse](../translation/ot/isaiah/053/011.yaml). English now reads
"he will see light"; the Hebrew composite adds אור to the declared retained base.
The shorter Masoretic alternative, partial third-scroll support, Greek syntax
difference and uncertainty remain disclosed. No fresh parchment inspection,
lexicon consultation or new witness claim was made in this implementation pass.
Earlier source-priority and full-record editorial approval remain provisional.

The [source-changing verifier](../tools/textual_restoration/verify_critical_successor.py)
checks all 23,264 current OT YAML files against checkpoint
`783e61ec70c5a152468f5cbe619656e0857182d4`, accepting only the whole baseline
or the exact reviewed replacement. It validates the trusted source/English
integration and real ISA, JOB and 2SA exports. Original Job/Samuel packages and
all 83 earlier-note protected files stay fixed. Old note-only tests were migrated
to an explicit historical replay: the migration agent ran all 19 original tests,
zero skips/expected failures; both wrappers passed in 56.087 seconds. That run
was reused, not repeated. Current source-changing tests are separate.

Independent `/root/isaiah_application_review` passed the bounded application,
not publication. It inspected the exact plan/candidate, validation chain and
historical migration, and independently checked the actual baseline and prior
notes. Twenty-six focused tests passed in 33.772 seconds; the added receipt
regression passed separately in 0.002 seconds. The reviewer inspected that
test-only addition and reaffirmed its verdict. No general re-review was needed.

Actual [preflight](../sources/textual_restoration/applications/isaiah53_11_successor_preflight.v1.json)
was saved before the canonical edit; the
[application receipt](../sources/textual_restoration/applications/isaiah53_11_successor_application.v1.json)
records the successful real postflight. All other canonical OT files are byte-
identical to the fixed baseline. Isaiah's actual export contains 66 chapters and
1,291 verse records; its digest changed from
`5fb07a70ce313fa729b77378f6dfce179e01038db5b066bf62a9bfa9d7b85cb1`
to `c4fc4c4e7b33b7a744f2ff1f63c44aa1274f982bef25a416439e1915715a450b`.
Job and Samuel exports remain unchanged. Application review SHA256:
`66d8f2fee1d76aa2b0285659d347b1738af6bde8ef620f60c5961638bcb4d34d`;
application receipt SHA256:
`0b486ef4d070e9b9d24307ff3c1480b325cb50bb47addd0f154fa40a16543b96`.
The [source README](../sources/ot/pob_critical/README.md) gives the verification command.
The separate applied-receipt check then passed against the real current corpus,
returning `application_record_verified: true`; `git diff --check` also passed.

This supersedes earlier log statements that canonical Isaiah application was
pending; it does not rewrite historical draft-stage flags or reviews. No reader
asset synchronization or manual deployment was performed. The public repository
and existing raw-YAML provenance route can expose this adoption, but deployed
reader behavior is not verified. The next useful follow-through is to verify
that reader presentation preserves these disclosures, then apply the same
bounded process to the next substantive textual decision. Comprehensive OT/NT
comparison and a recovered autograph are not claimed.

#### Integration outcome: local application verified; remote publication withheld

Implementation commit `b6c87caad0` was merged with the then-current remote's
status-only update as `3779bf013912949e7cdf5868bb49ddc19343cc1a`.
The push was rejected because remote main advanced concurrently to
`d5a458706f9984276e7787e4a62d125bcd2f0b59`. A subsequent fetch and inspection
found substantive changes to `DOCTRINE.md`, `METHODOLOGY.md`, drafting/review
tools and a new source-distinction policy. That second update is not merged
locally and this application has not been pushed.

The new doctrine prioritizes source-transparent English comparisons and explicitly
preserves approved John 21 agape-love/phileo-love distinctions. This pass does not
reverse or adjudicate those unrelated changes. The Isaiah editorial review pins
the earlier doctrine bytes, and the source validator checks that pin against the
live file. Therefore the successful local receipts do not establish compatibility
with the newly advanced remote. Do not silently repin the old review, weaken the
check, or present this local result as published. Next reconcile the historical
policy evidence and current policy in one bounded compatibility review before
merging/pushing; no repeat manuscript research is needed. This is also concrete
evidence that global live-document pins are imposing maintenance cost and should
not be multiplied in future casework.

### 2026-09-06 — Current-policy compatibility resolved without another validator layer

The previous turn made real progress: exact Isaiah adoption and verification,
followed by discovery of a concurrent policy update. This pass fetched and
inspected that update, then merged it as
`4b42db932de29181e76ad17ac76d620f8cf8d208`. It changes no OT verse files.
Four historical protected paths changed upstream: `DOCTRINE.md`,
`METHODOLOGY.md`, `tools/draft.py`, `tools/prompts/revision_policy.md`.
No unrelated policy or John 21 rendering was reverted.

Independent `/root/isaiah_current_policy_review` read the new policies, Isaiah
53:10–12, the frozen source report, earlier editorial judgment and recorded
A/B/C English alternatives. It approved public repository adoption of the exact
provisional Isaiah record, without bundled-reader/deployment approval. The
[compatibility record](../sources/textual_restoration/applications/isaiah53_11_policy_compatibility.v1.json)
preserves the policy hashes, actual full-sentence comparisons and limitations.
It is a new judgment, not a silent replacement of old review inputs.

The reviewer compared explicit "he himself" with "he"; "light of life" and
"by knowledge of him" with the current wording; and "declare many righteous"
with "justify many" to make the צדק root repetition visible. It retained the
current sentence provisionally. The last comparison exposes a real tradeoff:
"declare ... righteous" preserves the English root repetition but narrows the
action toward a declarative mechanism; "justify" does not reproduce that root
pattern in English. This remains open to stronger linguistic evidence, not an
assertion that the present wording is uniquely optimal. No new manuscript or
lexicon retrieval was performed. The incoming heuristic scanner returned no
Isaiah candidates; the model-noticed root pattern demonstrates why that result
is not evidence of exhaustive coverage.

Direct current-state checks compared every one of 23,264 actual OT YAML blobs
to the verified application commit `b6c87caad0b9c737dc670b89912af2e4d9e966f5`.
All match exactly. The current Isaiah bytes equal the approved candidate and
pass the full critical-verse schema. All application-review implementation pins
remain unchanged. Actual ISA/JOB/2SA exports match the application receipt;
the corpus was inventoried again afterward to detect concurrent mutation.
The union of historical note-protection and Job input pins differs only in the
four upstream paths above. All these results are in the compatibility record.

The incoming source-distinction suite passed all 27 tests in 0.230 seconds using
its native unittest runner. An initial pytest invocation failed because pytest
is unavailable; no installation was needed. The old applied-receipt verifier
was also actually tried and rejects `Prior protected input drift: DOCTRINE.md`.
This expected historical-policy mismatch is explicitly documented, not hidden
with skips, repins or a green full-suite claim. The older 27 source/application
test passes remain evidence for their original checkpoint, not the new policy.

To avoid compounding maintenance cost, no new validation framework or replay
layer was added. Frozen tools and receipts remain unchanged; their current
scope limitation is stated in the source README. A concrete source change,
separately reviewed policy compatibility, exact whole-corpus preservation and
real export checks justify repository integration here. They do not establish
deployed disclosure, a complete OT/NT comparison or recovered autographs. The
earlier remote-publication blocker is resolved editorially; the Git push result
must still be checked before claiming the result is on remote main.

### 2026-09-06 — Deuteronomy 32:8 evidence triage and explicit stop condition

The preceding Isaiah work was pushed to main as `a90a1d9954`. Returned to
textual evidence rather than extending its validation machinery. Read the
current Deuteronomy verse, existing candidate and successive Greek, Fouad,
Hebrew-image, numbering and OHB records. Independent triage separated genuinely
discriminating evidence from partly stale acquisition instructions.

The [new bounded report](DEUT32_8_EVIDENCE_TRIAGE_2026-09-06.md) records actual
consultation of Bar-On/Paz pp. 29–31, especially the complete note 5, with PDF
hash and locators. The PDF skill prompted rendered-page verification after web
screenshots timed out; the institutional download and local rendering succeeded.
The independent agent confirmed the interpretation of the relevant printed
note. Neither model consultation counts as a new manuscript or modern apparatus
inspection. Temporary source PDF/renderings were not committed.

Wevers's ordinary p. 513 preview explicitly refused viewing; no bypass or
purchase followed. Dayfani's institutional abstract was read, not the full
reconstruction. Second-hand apparatus transcriptions were search leads only.
The report records remaining complement/hand and excerpt-adaptation questions,
without treating every unfinished archival task as an automatic editorial veto.

Decision: no canonical change, no confidence increase; preserve the moderate
divine-referent working proposal and contrary readings. Do not repeatedly chase
the same unavailable pages or repeat the completed Fouad/IAA consultations.
The priorities page now reflects this stop/reopening condition and Isaiah's
completed repository adoption. Canonical Deut 32:8 SHA256 remains
`1caf32ddf68b552d662a94cff90970e5eacd9028ac0a4b8c89228634b14702af`;
candidate SHA256 remains
`7f7ee48c97c0d8ef54419ba653f075f5a7b40baa784bf9e2d96231dda02f6797`.
This documentation-only pass adds no code, new restoration or publication claim.

### 2026-09-06 — Live Isaiah reader check and misleading review-count repair

The previous Deuteronomy report was pushed as `4c3e0c8910`. This pass verified
whether the completed Isaiah source work reaches actual readers. In ordinary
Chrome, the legacy source URL redirected to
`https://peoplesbible.com/verse/?ref=ISA.53.11`. Its loaded UI displayed “he will
see light,” the POB-critical Hebrew, the provisional composite-source note,
all apparatus entries and both note bodies. Clicking footnote a navigated to
`#footnote-a`; a screenshot confirmed the disclosure was readable. No mock
server, repository-only rendering or new manuscript evidence is claimed here.

The live chapter route, `https://peoplesbible.com/bible?book=Isaiah&chapter=53&verse=11`,
still displayed the old “he will see and be satisfied.” Opened settings confirmed
POB, not another translation. Read-only HTTP checks found both
`https://bible.cartha.com/manifest.json` and
`https://peoplesbible.com/bibles/pob_manifest.json` identify commit
`b6717921daaa86c38c599a4b294bd792626b2631`, timestamp
`2026-09-07T00:07:45.773Z`, 135 books, 2,651 chapters, 45,109 verses. Git ancestry
and the bounded OT diff establish that this precedes the Isaiah application.
The website manifest's content-derived version is
`ee8d08e331ee2eca51eb810e85899516b860af5954522c573de9cd7f5ed1596f`;
its upstream version and CDN version are `b6717921daaa`.

Independent asset tracing confirmed local preview and Isaiah book assets also
contain the older wording. The existing single-book exporter returns light
and both notes correctly. Website `sync:pob` fetches the upstream bundle and
rewrites all lazy books, not one selected verse. `scripts/publish_pob.sh` runs
corpus validation, invokes the publisher and triggers a website rebuild.
Neither command was run. The user was asked whether to authorize that broader
publication; no approval was assumed. Runtime removal of POB main-reader notes
was not changed; the verified provenance route remains the disclosure path.

The live source page also exposed a real display defect: `cross_check` containing
only `status: needs_review` was shown as one completed pass, zero concerns, a
success checkmark and generic passed-review prose. In `cartha.website`, repaired
only `src/app/(main)/peoples-open-bible/verse/page.jsx` and added
`test/pob-provenance-review-status.test.mjs`. Missing/malformed counters now stay
unknown; pending/recheck status cannot imply current approval; valid populated
records retain their actual counts. Generic explanatory copy no longer claims
that merely having a cross-check section proves review happened or passed.

Independent `/root/provenance_count_fix_judge` passed the bounded repair and
independently ran its eight new tests. Root's combined actual-component/source
tests reported 13 passes, zero failures/skips, in about 0.43 seconds; diff-check
passed. Implementation commit `80eafe75` was merged with unrelated upstream
changes and pushed as `d7831fca58b3db5f284764c429d3b00022d31b8d`. Reviewed page SHA256:
`abcc61460cbd4b85752c0e7f2c4d9a53514eed19bc2dc21e794a5d27e6e2b2bf`;
new test SHA256:
`b09a5727451ec815e73b039cccb6fe9765298bbca6bb53a895e75ad6c4d62a7f`.
No source/candidate YAML or reader asset changed. Website main is picked up by
its documented scheduled deployment; no manual deployment was triggered and
the new count repair is not yet claimed verified live. The canonical record
also carries old preparation-era pending language in a rationale; this check
does not relabel those historical statements as a new source decision.

### 2026-09-06 — Efficiency check and Habakkuk 1:12 preservation decision

The user requested an efficiency check. The goal tracker reported 18,767,479
cumulative tokens at that check (not a dollar-cost estimate); no subagents
were then running. Retain useful source decisions and tested repairs, but
stop repetitive acquisition, overgrown audit scaffolding and open-ended
judge loops. The priorities page now records that operating constraint.

The next bounded [Habakkuk comparison](HABAKKUK_1_12_SOURCE_COMPARISON_2026-09-06.md)
consulted the actual versioned 1QpHab IV.17/V.3 and Mur. 88 XVIII.10
transcriptions and Rashi's verse-12 commentary. The disputed biblical clause
is supplied in 1QpHab; Mur. 88 supplies the distinguishing prefix. The pesher
commentary is indirect interpretation evidence. The report therefore retains
the current wording provisionally and proposes a footnote identifying the
scribal-correction tradition accurately. It does not claim recovered letters,
all-witness comparison, increased historical confidence or application approval.
Access failures and the unconsulted Greek/critical-apparatus step are explicit.
No canonical verse, frozen screening inventory, image, software or publication
asset was changed. The casebook links the new decision without rewriting its
historical screening snapshot.

Independent `habakkuk_preservation_check` reviewed the three published passages
and the report and passed the bounded preservation/tradition distinction; it
did not approve canonical application or establish earliest wording. Root
rechecked the canonical SHA256 against the report, unchanged, and checked the
documentation diff for whitespace errors. No software test or deployment
claim follows from these documentation checks.

### 2026-09-06 — Habakkuk disclosure applied without new infrastructure

Applied the [Habakkuk report's scoped disclosure](HABAKKUK_1_12_SOURCE_COMPARISON_2026-09-06.md)
after one independent unblinded editorial/application review. The
[application record](../sources/textual_restoration/applications/habakkuk1_12_disclosure_application.v1.json)
records exact baseline/candidate hashes, judgment, actual complete-book export
comparison and field checks. Only the footnote, two rationales and review-state
handling change. Old cross-check contents are preserved separately; no old
agreement score certifies the revised note. No new tool, image acquisition,
source selection, historical receipt rewrite or whole-corpus publication.

The initial exact-byte comparison caught a missing final blank line and passed
after correction. The schema/field/canonical-target checks passed; the complete
56-verse export differs only at the intended footnote. The whitespace check
reports the retained terminal blank line, not a clean result. Historical
whole-corpus policy-pin verifiers remain outside this scoped validation claim.

### 2026-09-06 — Repair a demonstrated image-consensus annotation leak

Reviewed the saved dual-vision pilot, its actual outputs, response protocol and
comparison code to test restoration readiness. The historical second-provider
run remains a saved access failure, not current inference; no retry or new
model call occurred. Broad calibration remains unexecuted. A separate protocol
limitation prevents successful empty observations on blank controls and is now
explicit in the method; the frozen pilot artifacts remain unchanged.

Reproduced a concrete comparator defect before editing: matching clear tokens
containing a parenthesized Latin restoration comment, a generic combining
underdot, or angle-bracket supplied text each yielded one accepted token.
Changed only `tools/dss/pilot.py` to restrict automatic eligibility to Hebrew
letters and Hebrew combining marks. Punctuation, mixed prose and editorial
annotations stay available in the comparison report but require adjudication.
Added regression tests in `tests/test_dss_pilot.py` for these cases and retained
eligibility of matching pointed Hebrew. The actual pilot/project test command
reported 21 passes in 0.007 seconds, including validation of the saved crops
and unchanged comparison. This is not an accuracy benchmark, new manuscript
reading, historical-confidence increase or translation change.

Independent `dss_annotation_guard_review` passed the two-file repair and reran
all 21 focused tests successfully. Documentation/code diff-check passed. The
review was scoped to this concrete safeguard, not the full restoration system.

### 2026-09-06 — Explicit image abstentions for future calibration

Closed the response-format defect identified in the preceding pass by adding
opt-in [observation protocol 2.0](../sources/dead_sea_scrolls/protocols/README.md).
The existing validator/comparator now distinguishes text-present, no-visible-text
and unassessable regions; empty observations require an explicit version/status
and explanation. Matching no-text observations never create accepted letters;
unassessable and conflicting observations remain unresolved. The old protocol
and saved pilot outputs remain unchanged and validate normally.

Added a versioned schema/prompt and ten regression tests, not a new runner or
model call. The existing runner and saved-pilot validator now enforce the
frozen response schema locally as well as semantic observation rules; the
review identified why relying on schema alone or semantic checks alone was
insufficient. Actual final focused validation reported 31 passes in 0.019 seconds.
These tests prove response handling, not calibration accuracy. A frozen labelled
control set and legitimate second-provider inference are still needed; the user
was asked whether access has changed, without requesting credentials. No new
attempt was inferred from the historical failure or launched without a new
access lead. No manuscript image, source reading, or translation was changed.

Independent `dss_abstention_review` passed the bounded protocol change and the
specific schema-enforcement correction, independently rerunning all 31 tests.
Diff-check passed; the historical pilot directory and canonical translation
tree have no changes in this pass. Provider compatibility remains untested.

### 2026-09-06 — Freeze actual observation development controls

Prepared [four exact-image controls](../sources/dead_sea_scrolls/pilots/2026-09-06-observation-development/README.md)
instead of another framework. Rehydrated only the needed registered 1QM TIFF,
whose full-resolution local copy was absent, and verified its existing SHA256.
The existing preparation script made exact RGB crops; root inspected all four.
The repository virtualenv lacked Pillow, so the bundled runtime was used without
installation. The LOC item page returned 403; the source download matched the
prior registered bytes and prior rights classification, not a new rights audit.

Two positive text-presence and two negative observation labels were independently
checked by `observation_control_labels`, which saw only the images and no expected
labels. This was label review, not a provider run or a different-family accuracy
test. One crop repeats the earlier development pilot and all four share one
manuscript: no held-out, independent-witness or character-ground-truth claim.

The freeze pins images, labels, prompt/schema and pre-run criteria; failed or
abstaining outputs cannot count as correct blanks, and negative-crop text claims
remain errors even when two models agree. Input/crop validation passed. No model
call, generated image, restoration, Hebrew selection or English change occurred.
Legitimate second-model access and the later varied held-out evaluation remain
separate unfinished requirements.

All 32 focused tests passed, including the new frozen-input hash/label-coverage
check. The existing pilot validator verified all four new crop hashes, and
diff-check passed. These checks establish input integrity, not model accuracy.

### 2026-09-06 — First actual frozen-control provider result

Executed one OpenAI low-effort pass against the frozen four-region development
set, using the existing read-only/no-tool runner and installed Codex CLI 0.153.4.
OpenAI Docs required official documentation and local invocation checks first;
the [result report](../sources/dead_sea_scrolls/pilots/2026-09-06-observation-development/RESULTS.md)
links the actual official source and records observed invocation evidence.
No labels, other readings or repository context were supplied to the isolated
model. No second-provider retry or new configuration followed the result.

The run succeeded in 41.58 seconds: 4/4 observation classes matched, with zero
negative-crop tokens, region abstentions or missing/invalid regions. However,
the writing regions yielded only 43 unreadable and two gap placeholders, no
Hebrew letters. This passes only the predefined observation smoke test, not
transcription, restoration, two-family comparison or held-out calibration.
The score records actual CLI token counters and hashes. Frozen files remain
unchanged, raw envelopes remain ignored, and no canonical text changed.

Independent `observation_run_score_check` verified all nine frozen input hashes
and the score against the actual response, passing the observation-only claim.
All 32 focused tests, four-crop validation and diff-check passed. No repeat
inference was needed to verify these counts.

### 2026-09-06 — Sharper Leningrad image; control label withheld

After the blurred-photo run produced no letters, acquired one sharper Leningrad
Codex photograph through the public file linked in its Commons description.
The original download matched the publisher's SHA-1; local SHA256, dimensions,
provenance/rights qualifications and final crop are in the
[control candidate](../sources/textual_restoration/controls/2026-09-06-leningrad-clear/README.md).
The web image fetch timed out; the direct original download succeeded. No archive
bulk download or new custodian-provenance certification occurred.

Root inspected the page/crop, then checked the corresponding local WLC substring.
The expected words were withheld from `leningrad_control_letters`, which reported
a different tentative reading and ambiguity. Both readings remain recorded.
This is not a manuscript variant, second-family consensus or a usable frozen
glyph answer key. No additional vote was sought to turn the disagreement into
a pass. The next step requires explicit glyph-label resolution, not assuming
that a high-resolution file guarantees accurate model reading. No canonical
source/English or earlier frozen evaluation inputs changed.

Direct checks passed for source/crop hashes, source dimensions and exact pixel
correspondence between the saved crop and its declared rectangle. Diff-check
passed. These checks verify the image preparation, not the disputed label.

### 2026-09-06 — Efficiency action: finish Proverbs 8:16 disclosure

The preceding user-requested audit verified disproportionate cumulative effort
and changed the next action: pause image calibration and finish a consequential
pending disclosure using existing evidence. The broad source-comparison goal
remains open; unresolved Leningrad labels are not a prerequisite for reporting
published readings. The priorities document now states that pause explicitly.

Reused the Proverbs comparison and saved Minchat Shai source, and freshly opened
[NET Proverbs 8:14–17, note 5](https://classic.net.bible.org/passage.php?passage=Pro+8:14-17).
It reports both Hebrew readings and Greek earth wording, while favoring justice
as the harder reading. No new PDF, manuscript image or broad acquisition was
needed. The evidence warrants disclosing the alternative, not selecting its
historical priority. No added witness count or confidence claim follows.

One independent, nonblind `proverbs_disclosure_review` approved the exact
footnote/review-state edits conditionally; all conditions passed. Applied the
expanded note while retaining its lexical alternatives and unchanged Hebrew,
main English and rationales. Preserved the former cross-check verbatim under a
historical key and reset active status to draft/needs_review. The
[receipt](../sources/textual_restoration/applications/proverbs8_16_disclosure_application.v1.json)
pins before/after bytes and review scope. Schema and exact-record checks passed;
actual full-book exports covered 31 chapters/915 verses with only the note text
and reason changed. Eight reader-footnote tests and diff-check passed. No new
framework, provider run, repeat judge loop or deployment occurred. Source choice
still requires the specific witness/hand and versional evidence identified in
the existing report, not further copies of the same published argument.

### 2026-09-06 — Mark 1:41 direct-apparatus attempt; no new reading

The preceding Proverbs application was completed progress. Selected the
existing NT pilot's consequential anger/compassion question instead of more
image calibration. Read its current SBLGNT-based verse and prior published-report
review. The official INTF directory links Mark Phase 3.5; direct application
metadata confirmed public read access. Web retrieval of that application timed
out, while direct HTTP and browser access loaded its shell. The NTVMR ECM page
also supplied navigation but no usable apparatus in the inspected browser state.

Read the public app configuration and bounded code excerpts to identify its
read-only lookup route. Requests to `api/mark/ph35/passage.json/0` with
`siglum=Mc&chapter=1&verse=41&word=4`, then the same with `button=Go`, both
returned HTTP 500. No successful navigator response established those parameter
values; the failure is not proof of a service outage or absent evidence.
Stopped without further endpoint probing. No manuscript readings, stemma,
apparatus support counts or ECM preference were obtained, so source selection,
confidence and canonical text remain unchanged. The
[pilot update](NT_PILOT_ADJUDICATION.md#direct-ecm-access-check--2026-09-06)
records this precise limitation and no-repeat condition. No inference run,
subagent, PDF/image acquisition or new comparison infrastructure was used.
Only these two documentation files changed; diff-check is the relevant local
check, not a claim to have validated a new textual result.

### 2026-09-06 — Saul's regnal numbers: separate evidence from conjecture

Did not retry the failed ECM lookup. The previous pass documented an access
limit, not a textual advance. This pass used the existing Samuel target,
local WLC and Acts source, and directly consulted NET textual notes to resolve
an actionable disclosure ambiguity. The
[comparison and application record](SAMUEL_13_1_NUMBERS_REVIEW_2026-09-06.md)
distinguishes published readings from proposed restoration without promoting
new Hebrew or English wording. Sefaria returned no usable verse body.

One independent scoped reviewer approved the exact note and review-state
correction, conditional on local checks. Preserved historical cross-check data;
active draft/needs_review does not borrow its scores. The first export check
failed my assumed 810-verse count: POB's actual Hebrew source map and export
both contain 811 records. Replaced that assumption with an exact chapter/verse
map comparison. The receipt records the final result and hashes, not an
unqualified first-attempt pass. No image work, apparatus acquisition loop,
new validation framework or reader deployment was undertaken.

### 2026-09-06 — Goliath: directly checked Greek four/five/six apparatus

The preceding Saul disclosure was completed progress. Returned to an open
source-selection question instead of another calibration run. Used the PDF
skill to inspect the already-downloaded Cambridge Samuel edition, printed55 /
PDF71, its Samuel prefacev and the general 1906 conventionsi–ii. Extraction
missed Greek search strings; bounded page-header inspection located the target,
then the complete page was rendered and read at original resolution. Private
PDF hash matches the recorded source; no new PDF or manuscript was acquired.

The [Samuel supplement](SAMUEL_SOURCE_COMPARISON_PASS_1.md#greek-numeral-apparatus-directly-checked--2026-09-06)
records the decisive new evidence and limits: B-based main text four, explicit
N five and A six in the apparatus, plus a separate bottom attribution. This
resolves the earlier conflicting Alexandrinus summaries at edition-report
level and advances the formerly uncollated five lead. It does not resolve
earliest priority. The primary Qumran URL failed; earlier Hebrew evidence was
reused without claiming a fresh consultation. NET's actual note was read but
its height-plausibility argument was not used to decide the source.

One independent apparatus check confirmed the finding, then approved the exact
connected note correction in a single scoped follow-up. Changed the Greek
attribution to “some Greek witnesses” and removed the outdated universal
image-reading prerequisite; no source promotion was authorized. Preserved
historical cross-check, reset active review state, and left Hebrew/main English
and other rationales unchanged. Schema, exact-record and full source-mapped
31-chapter/811-verse export comparisons passed with only note b changed; eight
footnote tests and diff-check passed. The
[receipt](../sources/textual_restoration/applications/goliath17_4_apparatus_disclosure.v1.json)
pins the evidence and application. No corpus publication or deployment occurred.

### 2026-09-06 — Goliath four-cubit source applied after DJD and editorial review

Completed the previous pass's named Hebrew reading-note gate using the existing
DJD XVII consultation copy, pp78–80, not another acquisition. The PDF skill
required complete-page visual inspection after locating the poorly OCRed text.
The [Samuel report](SAMUEL_SOURCE_COMPARISON_PASS_1.md#djd-reading-notes-and-provisional-critical-source-application--2026-09-06)
records qualified numeral preservation, limited longer-form17:41 evidence,
the contrary reduction explanation and the rejection of assumed scribal piety
as a decisive criterion. One independent agent separately approved the source
unit and exact full verse/application, with actual evidence limits retained.

Applied a disclosed POB-critical Hebrew source and corresponding four-cubit
English, preserving WLC exactly in history, six/five alternatives, uncertainty,
and the existing draft/needs_review state. Repaired the champion-note anchor.
Reused existing composition/source/full-verse validators and separate receipts;
no executor, schema or image-model change. An unsupported in-memory clone helper
failed before writes and was replaced without repeating research.

The exact candidate integration, explicit externally recorded trusted hashes,
schema, historical preservation and complete31-chapter/811-record reader export
passed. Export differences are confined to the target sentence and note.
Eight reader-footnote tests passed. The additional18-test regression invocation
returned11 errors: the Isaiah-based reviewed-source/full-verse fixtures reject
their older pinned inputs. It is not an all-green suite; the actual new Goliath
record passes the same validators with its separately reviewed current pins.
No frozen Isaiah receipts are repinned or overridden. The
[application receipt](../sources/textual_restoration/applications/goliath17_4_source_application.v1.json)
separates these results. No deployment or exhaustive critical-edition claim.

### 2026-09-06 — Exodus 12:40 source adjudication and Greek hand distinctions

Previous goal turn classified as progress: Goliath's reviewed source and
English application reached canonical Git state. This pass reused the
Pentateuch dossier to test whether Canaan belongs in Exodus 12:40's source.
The [new report](EXODUS_12_40_SOURCE_ADJUDICATION_2026-09-06.md) records actual
Cambridge1909 page inspection, exact locators/hashes, separate Greek variation
units, competing loss/expansion explanations and a low-confidence retention
decision. It preserves the edition's uncertainty about the corrector and the
limits of the existing Hebrew fragments. One independent agent checked the
new evidence and decision; no judge-until-agreement loop occurred.

The publisher-directory open failed, but search provided a working PDF link;
the PDF downloaded successfully. No repeated failed acquisition, image
calibration, model inference experiment or new validation infrastructure.
The canonical verse, source, English and old review fields remain unchanged.
The report flags narrower disclosure/metadata repairs for a separate scoped
application; no claim that those repairs or corpus-wide collation are complete.
Documentation checks cover baseline hash, local links and diff integrity only.
No deployment. The full OT/NT source-comparison goal remains open.

### 2026-09-06 — Apply the reviewed Exodus 12:40 disclosure

Previous goal turn classified as progress: new Greek apparatus evidence and
a reasoned source hold were committed. This pass finishes its concrete reader
disclosure correction using the existing dossier, without new acquisition.
The [application receipt](../sources/textual_restoration/applications/exodus12_40_disclosure.v1.json)
pins baseline/applied verse bytes, research checkpoint, policy and exporter.
It records actual independent scoped review, including confirmation of the
exact written metadata, not a new historical witness or a blinded comparison.

Canonical changes: qualified source note; separate Samaritan/Greek theological
alternatives; provisional-retention rationale recognizing Samaritan Hebrew;
relative-clause metadata accurately describing current English; old review
objects archived verbatim with live draft/needs-review status. No Hebrew,
main-English, anchor, other lexical-entry, ai_draft or revision-history change.
The source-priority and full-verse rendering questions remain open.

Actual checks passed: verse schema, exact record delta, complete before/after
EXO export against every source identifier (40 chapters, 1,213 verses), sole
export difference at the target note, eight reader-footnote tests, diff check.
No validation infrastructure added or frozen comparison receipts repinned;
known unrelated Isaiah fixture drift was not rerun. No new access failure or
image experiment. No deployed-reader or exhaustive-corpus claim.

### 2026-09-06 — Exodus 1:5: test genealogical histories before numeral promotion

Previous turn was progress: Exodus 12:40's reviewed disclosure was applied and
export-verified. This pass addressed the consequential seventy/seventy-five
source question rather than continuing disclosure cleanup. The
[adjudication report](EXODUS_1_5_COUNT_ADJUDICATION_2026-09-06.md) records new
Cambridge Exodus/Genesis apparatus consultation, contextual Hebrew and Greek
controls, full-line published DSS preservation checks, and actual opposing
arguments by Kislev, Tov and Longacre. Numeral and Joseph-clause decisions stay
separate. Root's tentative inclination toward seventy-five and the independent
agent's unresolved-priority verdict are retained, with the substantive reason
for the final hold. No historical witness count is increased by model review.

The source remains provisionally seventy; no canonical file or note changed.
The new evidence removes an overly rigid literary-splice concern but does not
settle direction of genealogy revision. DJD XII pp. 19 and 85 are the precise
next source discussions, not newly consulted sources. Shell-only IAA responses,
a corrected out-of-range PDF locator scan and a corrected source-label lookup
are documented without treating access failures as textual absence. Existing
local PDFs were reused; no restoration experiment or new validation code.
Checks cover baseline preservation, links and diff integrity; no export or
whole-corpus test is claimed for this documentation-only pass. Not deployed.

### 2026-09-06 — Close the Exodus count follow-up; enforce the efficiency stop

The preceding user-requested efficiency check was progress in choosing the next
action: it verified that no other agent was running and identified repeated
Exodus reasoning as diminishing-return work. It made no repository changes.
This pass preserves the previously obtained DJD/thesis findings in the
[existing report](EXODUS_1_5_COUNT_ADJUDICATION_2026-09-06.md#djd-follow-up-and-stopping-decision--2026-09-06)
and replaces the obsolete unread-DJD next step in the priority queue.
The report distinguishes English DJD OCR, visually inspected thesis pages and
the single independent agent's narrower review. No fresh agent was launched.

New local check: Greek Exod 39:2,5 and WLC Exodus 38:25,28 reverse the seventy/five
order, limiting mechanical retroversion without settling Exodus 1:5 priority.
The report records the thesis table-extraction omission corrected by visual
inspection. No new acquisition, restoration claim, canonical edit or infrastructure.
The numeral and Joseph questions remain unresolved and are parked behind a
discriminating-evidence condition, not another opinion-gathering cycle.

Verification: existing Greek and thesis SHA256 values and the unchanged Exodus
1:5 baseline were checked. Local links and Git diff checks cover documentation
integrity only; no corpus export, exhaustive collation or deployment is claimed.
The existing coverage audit still distinguishes all-book screening from actual
passage collation; broader OT/NT work remains unfinished. Next selection must
use an underexamined source/reading with a consequential test, not reopen this
case simply because its scholarly disagreement persists.

### 2026-09-06 — Ruth 3:15: distinguish gender evidence and apply disclosure

Previous goal turn was progress: the Exodus follow-up was committed and parked
behind a discriminating-evidence condition. This pass chose an unexamined Ruth
lead from the existing local-note inventory rather than reopening that case.
The [Ruth report](RUTH_3_15_SOURCE_COMPARISON_2026-09-06.md) records the actually
read versioned 2Q17 transcription, CATSS Greek target apparatus, local Greek
and Hebrew context, and SIL's attributed versional report. 2Q17's disputed verb
is supplied; the Greek base verb is gender-neutral, but published variants
explicitly add either Ruth or Boaz. Neither modern translations nor separate
editions of the same fragment count as additional ancient witnesses.

Retained masculine Hebrew and “he” provisionally, preserving the competing
narrative explanation. Applied qualified note `b`, two anchor corrections,
and connected rationale updates; historical reviews preserved and current
record marked draft/needs-review. One independent local comparison and its
bounded candidate review supported this scope; external-source observations
were root's, not independently reread by the agent. Access failures and the
precise reopening condition are in the report. No image work or new validator.

Schema, exact record delta, source/plain-English preservation, archived-review
equality, all 85 Ruth source/export identifiers, exact full-book output delta,
eight reader-footnote tests and diff checks passed. The report holds actual
input/output hashes. No other verse was changed and no deployment occurred.
Context inspection also exposed misplaced notes in Ruth 3:16 and 4:1; those
are separate preexisting defects, not silently included in this application.
This adds one actual passage comparison, not full Ruth or all-source coverage.

### 2026-09-06 — Whole-set Ruth DSS screen and a source-faithful English repair

Previous turn was progress: Ruth 3:15's reviewed disclosure was applied and
pushed. This pass expanded from one disputed verse to all four Ruth records
in the pinned QDR dataset. The [report](RUTH_DSS_COMPARISON_2026-09-06.md) and
[receipt](../sources/textual_restoration/comparisons/ruth_dss_screen.v1.json)
record full published-line context, input hashes, all 42 tagged anchors and
72 line records, with supplied text, unresolved brackets and unassigned traces
excluded from preserved-reading claims. Root compared Cave 2; one agent
compared Cave 4. The older bracket-syntax counters were not mistaken for
automatic preservation assessments. No new collation engine was built.

Identified lexical, prepositional and grammatical candidates alongside spelling
differences, without promoting supplied words or declaring all witnesses
collated. A concrete result at 2:21 changes “young women” to “young men,”
preserving the source contrast while disclosing potentially generic reference.
The reviewer compared full-verse men/workers/current-women alternatives under
the source-distinction contract. Its note-preservation correction was accepted.
The prior historical review/revision records are retained, with live review
status reset rather than inherited. Hebrew is unchanged.

Exact application/schema checks, all 85 Ruth source/export identifiers, sole
target export delta, eight reader-footnote tests and diff checks passed; hashes
and scope reside in the receipt. No access failure, new image claim, judge loop,
new validation infrastructure or deployment. The untracked Geniza file was
left untouched. Next textual priority is the consequential source candidates,
not reopening the completed 3:15 gender test or polishing spelling-only variants.

### 2026-09-06 — Adjudicate five Ruth leads using local Greek controls

Previous turn was progress: whole-set Ruth screening and the 2:21 English
correction were pushed. This pass tested five consequential leads together,
reusing published fragment evidence and consulting actual CATSS target units.
The [follow-up](RUTH_DSS_COMPARISON_2026-09-06.md#consequential-candidate-adjudication-follow-up--2026-09-06)
records the local Greek being/residence discriminator at 1:2, exact birth-clause
position of uncertain “again” at 1:12, separate 3:14 omission and 3:15 locative
questions, and Hebrew/Greek interrogative variation at 3:16. A published
handbook's generalized Greek-omission claim is narrowed to the inspected
witness report. One agent handled chapter 1 alongside root's chapter 3 work;
its additional objection/note checks used disclosed root observations.

No Hebrew changes selected. Applied 3:16 note/anchor/rationale correction with
source and marker-free English unchanged. Retained interpretive alternatives,
historical reviews and the uncertain priority; current draft/needs-review does
not inherit old approval. The report gives actual target/export hashes and
the passing schema, exact-delta, whole-Ruth identifier/output and eight-test
checks. No new infrastructure, acquisition failure, image work or deployment.
The five source leads now have explicit stopping/reopening conditions. Full
Ruth and broader OT/NT comparison remain incomplete.

### 2026-09-06 — Preserve completed Lamentations screen after efficiency audit

The preceding efficiency audit verified recent results and stopped further
expansion, but did not advance the textual comparison itself: conservatively
classified as no progress toward corpus completion. This pass rechecked the
current repository and preserved previously completed, uncommitted research
rather than repeating acquisition. The [report](LAMENTATIONS_DSS_COMPARISON_2026-09-06.md)
and [receipt](../sources/textual_restoration/comparisons/lamentations_dss_screen.v1.json)
record four pinned QDR records, 103 physical line records and 62 tagged anchors.
Root's 4Q111 work and one agent's other-three-record screen were complementary,
not independent replication. No additional agent or judge loop was launched.

The consequential result is a linked literary-form comparison in 4Q111 and
specific 5Q6 candidates; no historical-priority or restoration claim follows.
Local Greek controls expose an adjacent-row boundary that must not be called
an omission. Reference-only diffing also misses a cross-verse short junction.
Published supply, uncertain brackets and unassigned traces remain distinguished
from preserved readings. The article abstract/bibliography, not its PDF body
or cited DJD edition, were consulted. No acquisition was retried this pass.

Input hashes and the 154-record canonical manifest were revalidated against
the earlier screen. No canonical source, English, note, application approval
or reader deployment changed. JSON, both input pins, all line/unit/reference
and untagged inventories, 103/939/62 totals, the unchanged canonical manifest,
Greek adjacent-row anchors, report local links and `git diff --check` passed.
These checks establish record consistency, not historical priority. The
unrelated untracked Geniza file remains untouched.
Next work requires evidence addressing a named source-choice question, not
more scaffolding or repetition of this screen.

### 2026-09-06 — Lamentations 1:7: test historical directions and apply disclosure

Previous turn was progress: completed Lamentations screening was committed and
pushed. This pass read the previously unconsulted Kotzé PDF argument, printed
pp.596–607, with critical Hebrew/argument pages checked visually under the PDF
skill. The [follow-up report](LAMENTATIONS_DSS_COMPARISON_2026-09-06.md#lamentations-17-argument-and-disclosure-follow-up--2026-09-06)
records the PDF pin, actually read scope, opposing historical explanations,
source-distinction full-verse alternatives and the limit of the independent
review. Cited editions were not silently promoted into directly consulted sources.
The earlier abstract-only status is superseded for this article, not for DJD.

Retained the opening provisionally; no restoration or historical certainty claimed.
Applied source disclosure and lexical-note/anchor corrections, with Hebrew and
marker-free English unchanged. Historical reviews preserved; current status is
draft/needs-review. One bounded independent objection review and exact-application
check passed; no consensus loop. Current/local Greek context was inspected by root.
Schema, exact record delta, preservation/history checks, all 154 source/export
IDs, sole target output delta and eight footnote tests passed; hashes are in the
report. No new infrastructure, failed acquisition or deployment. The unrelated
untracked Geniza file remains untouched. Park the opening unless new evidence
discriminates the recorded historical directions; no repeat article acquisition.

### 2026-09-06 — Ecclesiastes: published/QDR scope reconciliation and noun comparison

Previous turn was progress: the reviewed Lamentations 1:7 disclosure was pushed.
The [Ecclesiastes report](ECCLESIASTES_DSS_COMPARISON_2026-09-06.md) broadens
actual witness comparison to both pinned records. Root compared all 36 published
4Q109 lines against current source fields; one bounded agent compared all eight
published 4Q110 lines and eleven older QDR lines. Complementary labor is not
independent replication. The 44/47 line-count difference and final unidentified
4Q110 traces expose a concrete limit on the older contextual reconstruction.
No new fragment identity or pixel reading was asserted.

Ten local Greek selected-text contexts were read. The 7:2 noun comparison
provisionally favors retaining the feasting/joy distinction, while preserving
the reverse-development explanation. A full-verse check is recorded without
claiming the noun-only alternative translates the complete scroll form. Remaining
lexical, conditional and correction candidates are screened, not adjudicated.
The earlier WLC-based wisdom audit does not certify this new witness coverage.
One Brill preview attempt returned 403; its body was not read or retried.
No canonical source, English, notes, historical review, infrastructure or deployment
changed. Both input pins, QDR counts, the unchanged 222-record canonical manifest,
exact full-verse check, Greek noun anchors, report links and diff checks passed.
The unrelated untracked Geniza file remains untouched. Do not reopen 7:2 or
repair its incidental note anchor merely to prolong this comparison.

### 2026-09-06 — Romans 5:1: manuscript reports, spelling/mood and disclosure

Previous turn was progress: Ecclesiastes comparison was committed and pushed.
This pass advanced an NT priority beyond edition comparison. The
[report](ROMANS_5_1_SOURCE_COMPARISON_2026-09-06.md) records the licensed THGNT
apparatus with original/corrected hands and 0220 vid, Wallace's article, the
Head/Williams/Holmes/Heide discussion, Hsieh's locator excerpt and institutional
Wyman-fragment information. No manuscript pixels, complete ECM apparatus or
new versional collation were obtained. Older publication and correction stories
were not treated as observed history; a future-ECM prediction is not evidence.

Root and one bounded agent read Romans 4:23–5:11. The agent independently
assessed the contextual objection and then passed the exact scoped application.
Two full-verse alternatives are recorded. Greek and marker-free English remain
unchanged; qualified note a, repaired a/b anchors and connected rationale were
applied, preserving b/c notes and historical review/revision objects. Current
status is draft/needs-review, not inherited full approval. The NT method now
explicitly separates attested spelling from regular morphology and intended mood.
Validation results and an unresolved export limitation are recorded in the report. No new validator,
PDF/image workflow, repeated acquisition, judge loop or deployment. The unrelated
untracked Geniza file remains untouched; the source question is parked unless
specified discriminating evidence appears.

### 2026-09-06 — Efficiency check and bounded Romans closeout

The user's quick efficiency check confirmed excessive cumulative expenditure
relative to applied translation changes. The goal tracker reported approximately
21 million tokens (not a dollar-cost measure); no subagents were doing additional
research. Stop open-ended expansion and repeated unresolved-case debate; the
existing proportional-documentation and bounded-review rules remain controlling.
The preceding check changed the next action to closing the pending work rather
than opening another comparison case.

The full Romans ID check exposed 433 canonical records versus 430 exported
verses. Read the parser, source iterator, exporter and supplementary drafting
records; verified the vendored Romans file against the upstream MorphGNT file
byte-for-byte. Its verse list ends at 16:24; the three supplementary doxology
records are outside the export's source-driven list. This is an open coverage
limitation, not a parser failure or a newly adjudicated textual omission.
The scoped 5:1 preservation/export checks and eight footnote tests pass; no
full-Romans coverage pass is claimed. The report records hashes and the next
delivery gate. No new agent, restoration experiment, exporter change or
deployment was used in this closeout. Keep the unrelated Geniza file untouched.

### 2026-09-06 — Verified doxology source placement and restored reader coverage

Resolved the prior Romans coverage limitation with three explicit supplementary
export opt-ins, not fabricated SBLGNT rows or a global inclusion of unreviewed
material. Official byztxt v2.0.3 Greek matches the three existing source strings
apart from case; its references are 14:24–26, unlike POB's 16:25–27. Corrected
the placement disclosures and restored missing note anchors. The [existing report](ROMANS_5_1_SOURCE_COMPARISON_2026-09-06.md#supplementary-doxology-delivery--2026-09-06)
records evidence, independent review, hashes, 433/433-ID validation and 15 passing
tests. Two missing historical draft hashes per record remain schema errors;
no provenance values were invented. The 27 other source-absent NT records remain
outside the opt-in gate. No manuscript-priority debate, source replacement,
main-English rewrite, generated reader bundle or deployment occurred.

### 2026-09-07 — Closeout of the September 6 supplementary attribution batch

The preceding Romans pass made verified progress; this pass tested the remaining
27 records together rather than opening 27 research cases. Compared seven pinned
byztxt v2.0.3 CSV files, preserving URLs, hashes and primary rows in one
[inventory](../sources/textual_restoration/inventory/nt_supplement_attribution.v1.json).
Found 14 word-level matches and 13 unresolved attributions (including changed
reference order and Greek wording, not merely punctuation). Changed only the
13 active attribution labels and review status, preserved original labels and
historical review objects, and blocked unresolved sources from supplementary
export. Greek and English remain unchanged; no new reader inclusions or deployment.
One independent check corroborated John 8:5 and the three absent references.
The [report](NT_SUPPLEMENT_ATTRIBUTION_AUDIT_2026-09-06.md) records scope, contrary
possibilities, linked-passage hazards, checks and exact reopening conditions.
The old generation script is labeled as a historical attribution list, not a
verified registry; its paid drafting workflow was not executed.

### 2026-09-07 — Whole-OT base screen exposed dropped inline Hebrew letters

Returned to the Hebrew corpus after the NT batch. Reused existing parsers to
screen all 23,264 canonical OT records; separated paragraph/heading representation
from meaningful source letters. Found production `.text` extraction dropped 11
inline-annotated words across ten verses, including Deuteronomy 6:4. Fixed the
parser and ten WLC source strings; preserved critical-source adoptions and main
English. One independent XML/context check confirmed the defect and identified
the already-existing Moses/Manasseh choice in Judges, which was not re-adjudicated.
Corrected four connected lexical citations and Isaiah's truncated Hebrew note
quotation. The [report and receipt](HEBREW_INLINE_LETTER_REPAIR_2026-09-07.md)
record exact inputs, repairs, normalization limits, tests and preexisting snapshot
drift. No manuscript restoration claim, fresh acquisition, image generation,
canonical punctuation rewrite or deployment. Psalms' source-context/heading
mapping remains a separate limitation, not a license to delete repeated context.

### 2026-09-07 — Judges 18:30 source/English divergence remains unresolved

Checked the name-choice issue exposed by the parser repair. NET's editorial
note supports Moses; a 2025 primary research abstract challenges that consensus,
but its full argument was inaccessible. No historical-priority decision or Hebrew
emendation follows. Corrected the misleading “Hebrew: Moses” reader note and
added explicit unresolved source/English readings while preserving both texts.
The [bounded report](JUDGES_18_30_SOURCE_SELECTION_2026-09-07.md) distinguishes
actually inspected evidence from inaccessible pages and unconsulted manuscript
claims, with a concrete reopening gate. No extra agent, paid access, image work,
repeated failed acquisition, source replacement or deployment.

### 2026-09-07 — Mapped all Psalms source contexts without renumbering readers

Resolved the preceding Hebrew-screen mapping gap in one batch: 2,564 unique
exact matches, 13 repeated-string matches resolved by neighboring references,
and Psalm 60's combined two-verse heading. The [map and report](PSALMS_SOURCE_CONTEXT_MAP_2026-09-07.md)
cover all 2,578 POB records and 2,527 vendored WLC references; 52 source verses
are shared as heading/body context. Verified every current source
string and coverage set rather than assuming matching chapter totals suffice.
Found 36 body IDs differing from explicit XML KJV-reference notes, chiefly the
two-part headings in Psalms 51/52/54. No text, note, ID or reader migration was
performed. No new acquisition, agent, reconstruction or deployment; Judges 18:30
remains parked. Source-context completeness does not certify English span or
versification alignment, manuscript coverage or historical priority.

### 2026-09-07 — Efficiency constraint and Lamentations 5:3 follow-up

The preceding efficiency check supplied measured usage and changed the next
action: defer Psalm 107 wording polish and bound subsequent source questions.
Recorded that constraint in the priorities. Followed the existing Lamentations
lead with current 5:1–7 context, 5Q6 column iv line 7 and van Rooy's published
2012 discussion of 5:3. The [follow-up](LAMENTATIONS_DSS_COMPARISON_2026-09-06.md#lamentations-53-targeted-follow-up--2026-09-07)
records the daughter-loss interpretation, expansion/simplification alternatives,
source uncertainties, full-verse comparison and a precise reopening condition.
Provisional retention, no canonical change or new manuscript-priority claim.
Initial broad search results were unhelpful; a siglum-specific follow-up found
the relevant discussion. Other search hits were not treated as consulted
arguments. No paid acquisition, agent loop, new infrastructure or deployment.
Checked the retained verse/hash and new JSON against the unchanged record,
local links and Git whitespace; no runtime-test claim for documentation-only work.

### 2026-09-07 — Added the 4Q176 Lamentations excerpt target

The prior 5:3 pass made documented progress and remains parked. Checked a
separate source-coverage lead: 4Q176 was a label-only Psalms-context target,
not a registered Lamentations excerpt. Consulted the 2019 primary publisher
abstract and relevant current QDR transcription lines. Added one registry
entry for partial 4:21–22 coverage, recording linked fragment presentations,
possible secondary addition, access limits and unverified physical placement.
The [report](LAMENTATIONS_DSS_COMPARISON_2026-09-06.md#excerpt-coverage-follow-up--2026-09-07)
distinguishes the original four-copy screen from this excerpt target. No
canonical changes, new manuscript votes, image generation, frozen-receipt
rewrites or deployment. Checked registry validity and exact preservation of
all earlier entries and canonical records. No new validator or agent loop.

### 2026-09-07 — Restored three missing OT textual-note anchors

The preceding 4Q176 registration was progress. Shifted from acquisition to
delivery: an OT scan found three unlinked textual-variant notes. Attached them
at the relevant dates/counts in 2 Kings 15:30 and 1 Chronicles 18:4; 25:3,
preserving Hebrew, marker-free English, note bodies and archived reviews.
One bounded independent review passed. The [application report](OT_TEXTUAL_NOTE_DELIVERY_2026-09-07.md)
records local evidence, exact hashes, schema checks, eight passing tests and
full-book export comparisons (719/943 verse keys, only three changed objects).
No manuscript-priority claim, unrelated lexical-note repair, new infrastructure,
image work or deployment.

### 2026-09-07 — Haggai source comparison and 2:1 disclosure

The preceding OT note-delivery repair was progress. Compared the Haggai portions
of the three existing QDR book-map records, with 87 indexed lines and 36 reference
tags distinguished from surviving verse coverage. Root read the canonical book
and Mur88; one agent handled 4Q77/4Q80. Found Mur88 22:15's recipient formula
against WLC's explicit agency formula at 2:1; consulted selected local Greek
controls without treating them as manuscript votes. Added qualified disclosure
and repaired its existing agency-note anchor after one independent locus check.
The [report and receipt](HAGGAI_DSS_COMPARISON_2026-09-07.md) record preservation
limits, contrary transmission explanations, unchanged source/main English,
38-verse export verification and the stop condition. No new image reading,
all-source completeness claim, validator, frozen-receipt rewrite or deployment.

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
