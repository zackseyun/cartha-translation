# Old and New Testament Textual Restoration Priorities

## Decision

Revised 2026-09-06 under [method 2.0](TEXTUAL_ADJUDICATION_METHOD.md).
The [approach review](TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md) gives
the current assessment and immediate delivery order. The source lists below
are the long-range research queue, not a requirement to restore every image
before improving any translation.

The People's Open Bible will attempt this work independently with **Codex as
the transcription, collation, and textual-reasoning system**. The project will
not depend on commissioning new human diplomatic transcriptions or
paleographic review.

ImageGen may be used after the textual work to create a readable visual
reconstruction, but an ImageGen output is never manuscript evidence. It must
be visibly labeled, stored outside the evidence lanes, and excluded from OCR,
transcription, collation, confidence scoring, and translation decisions.

The target is the **earliest attainable text supported by surviving evidence**,
not a claim that we have recovered a lost autograph. The project keeps four
things separate:

1. ink visible in an archival image;
2. deterministic enhancement of that image;
3. Codex's text-restoration hypothesis based on visible traces and comparison
   witnesses; and
4. ImageGen's non-evidentiary visual reconstruction.

## No-human operating standard

Two different model families, run blind from one another, remain the project's
working transcription gate. Exact agreement may be accepted as a working
transcription or restoration proposal even when a second historical witness is
unavailable. Two runs of the same model do not count. Agreement does not
establish historical priority or authorize publication. Calibration against
frozen controls is still pending. A reading receives one of these statuses:

| Status | Meaning | May change the POB main text? |
|---|---|---|
| `machine-observed` | Codex identifies visible strokes in deterministic views checked against the original. | Only after separate source selection and application review. |
| `machine-consensus-accepted` | Two different blinded models return the same visible diplomatic glyphs or tokens. | Working transcription only; separate source selection and review required. |
| `machine-consensus-restored` | Two different blinded models supply the same damaged or missing letters. | Agreement alone is insufficient; retain supplied status and a separate textual argument. |
| `machine-corroborated` | A reading has comparison support with documented relationships. | Only after source selection, English review, and application checks. |
| `machine-hypothesis` | A plausible completion based on spacing, grammar, orthography, or a parallel, but the letters are not fully visible. | No. It remains in the apparatus or research record. |
| `lost` | The material is physically absent or no reading survives. | No. Missing text is never presented as recovered ink. |
| `visual-reconstruction` | ImageGen rendering made from an already documented reading or hypothesis. | Never. Display only. |

A reading produced by only one model remains `machine-hypothesis`. Exact
agreement by two different blinded models assigns the appropriate working
machine-consensus state. Independent historical corroboration must be recorded
when available, but is not required for working transcription acceptance.
An edition or transcription of the same manuscript is not an independent
historical witness. Neither confidence scores nor exact agreement establish
the accuracy of a supplied reconstruction.

## Restoration priority queue

Text selection follows the [source-wording adjudication method](TEXTUAL_ADJUDICATION_METHOD.md):
older manuscripts have a modest preference when other evidence is comparable,
but legibility, textual relationships, and transmission explanations can
outweigh age. The method is applied in the [three-passage report](HEBREW_PILOT_ADJUDICATION.md).

### Priority 0 — Resolve consequential differences using the existing system

The registry, coverage map, comparison records and application pilots already
exist. Do not rebuild them as prerequisites for each case. Choose one question
whose answer could affect source selection, English meaning or necessary reader
disclosure. Start from the existing dossier and current POB wording. Obtain only
the evidence that can distinguish the remaining alternatives; stop with retain,
propose change, or unresolved with a precise reopening condition. A research
decision is not application approval. Image-workflow calibration remains required
for new machine-transcription claims, not for accurately reporting a published
edition's reading.

Efficiency constraint reaffirmed 2026-09-06: reuse existing evidence, record one
consequential decision per pass, and keep documentation proportional to the
finding. Use one bounded independent review for a substantive change; repeat
only to check concrete corrections, not until agreement can be manufactured.
Do not rerun settled acquisition or build new validation infrastructure without
a specific unresolved defect. Model agreement is neither a new witness nor a
reason to raise historical confidence.

Following the user's efficiency audit, image calibration is paused unless a
specific translation-relevant question requires a new image reading. The
unfinished Leningrad label check is retained, not a prerequisite for using
published editions. Finish actionable disclosures from existing comparisons
before opening another acquisition or calibration cycle. This does not waive
calibration for future machine-transcription claims or narrow the OT/NT scope.

Current bounded results: the [1 Samuel 1:24–25 comparison](SAMUEL_SOURCE_COMPARISON_PASS_3.md)
tested the singular-bull argument against a published grammatical control and
retains the current text pending its recorded reopening evidence. Do not repeat
that acquisition. The [Job 13:15 comparison](JOB_13_15_SOURCE_COMPARISON_2026-09-06.md)
now tests the waiting/hope interpretation against published counterarguments and
the book's annotated verb occurrences. Its exact full-record rationale/note
candidate has now been applied after scoped editorial/application review and
actual full-book export checks. The reusable successor verifier resolves the
prior corpus-integrity integration gate without changing frozen receipts.
Hebrew and main English remain unchanged; do not repeat the completed disclosure.
Neither pass establishes historical priority. The separate
[2 Samuel 13:37 disclosure](SAMUEL_13_37_NOTE_APPLICATION_2026-09-06.md) was applied
at `d73c9aecc4` after resolving the earlier integration constraint; source and
main English are unchanged. Existing promotion gates remain in force. Select
the next case by its discriminating evidence and translation consequence, not
by an obsolete blocker or the availability of another infrastructure task.

Isaiah 53:11's provisional “light” source and English have now been adopted in
the canonical repository and integrated with the updated source-distinction
policy at `a90a1d9954`; see the research log and
[policy compatibility record](../sources/textual_restoration/applications/isaiah53_11_policy_compatibility.v1.json).
Do not restart its completed source/schema/application work. Reader deployment
is a separate, still-unverified claim.

The [Deuteronomy 32:8 triage](DEUT32_8_EVIDENCE_TRIAGE_2026-09-06.md) retains
the current canonical text for now and keeps the divine-referent proposal
provisional. It identifies the precise remaining Greek/4Q37 evidence questions,
distinguishes completed image/Fouad consultations from uncompleted claims, and
sets a no-repeat acquisition stop until a new resource is available. Other
consequential cases need not wait for its inaccessible apparatus.

First working demonstration: [three Hebrew variants and their English
effects](HEBREW_COMPARISON_SAMPLE.md), with a machine-readable source snapshot.
It compares published readings; it does not claim new image restoration.

The [Exodus 1:5 count adjudication](EXODUS_1_5_COUNT_ADJUDICATION_2026-09-06.md)
now tests opposing genealogical histories and actual Greek clause-order
evidence. Priority remains unresolved; seventy-five is a serious candidate,
not confined to omission/preposition of the Joseph clause. Its bounded follow-up
has now consulted the DJD English discussions and relevant thesis pages and
checked a local Greek/Hebrew numeral-order control. **Park the case** unless
identified new evidence can discriminate the histories or test a decisive
locus-specific reconstruction. Do not repeat the now-completed DJD argument
acquisition or make a cosmetic note correction. Source and English remain unchanged.

The [Exodus 12:40 adjudication](EXODUS_12_40_SOURCE_ADJUDICATION_2026-09-06.md)
now provisionally retains the base with low confidence in priority, after
checking distinct Greek fathers positions and first-hand/corrected numerals.
Do not repeat this apparatus acquisition. Its source reopening conditions are
recorded in that report. The identified note/metadata correction is now
[applied and export-verified](../sources/textual_restoration/applications/exodus12_40_disclosure.v1.json);
do not repeat that completed disclosure. The source and main English remain
unchanged, and full-verse rendering review is a separate open question.

A newly examined local-note lead,
[Ruth 3:15](RUTH_3_15_SOURCE_COMPARISON_2026-09-06.md), provisionally retains
the masculine subject after published DSS preservation and Greek variant
comparison. Its qualified disclosure and two anchor repairs are applied and
full-book export-checked; do not repeat the completed bare-Greek gender check.

The [corpus-wide Hebrew and NT map](HEBREW_AND_NT_VARIANT_MAP.md) now indexes
all 66 canonical books, WLC written/read variants, and the official 27-book
SBLGNT edition apparatus. The [48-case shortlist](TEXTUAL_VARIANT_CASEBOOK.md)
prioritizes passage-level work; the [NT method](NT_TEXTUAL_WITNESS_METHOD.md)
defines the move from edition comparisons to actual Greek manuscript evidence.
This is screening coverage, not completion of all manuscript adjudications.

Use the declared source in each verse as the starting point; do not silently
replace it with an eclectic reading. Broad catalogue screening supplies leads
and coverage gaps, while passage-level comparison supplies textual decisions.
Neither requires completing a universal image-restoration apparatus first.

Maintain and extend these existing capabilities only when the active case needs them:

- a unified witness registry with shelfmark, language, date, passage coverage,
  textual role, image provenance, rights, and hashes;
- image-addressable diplomatic transcription records;
- normalized Hebrew, Aramaic, and Greek layers mapped back to the diplomatic
  text;
- passage-level alignments and variation units;
- a human-readable and machine-readable critical apparatus;
- a decision record connecting every accepted reading to the POB verse YAML;
- a separate ImageGen visual-reconstruction manifest.

### Priority 1 — Direct Hebrew and Aramaic gaps and major OT variants

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Qumran Tobit 4Q196–4Q200** | Fragmentation, fading, edge loss, and mixed Aramaic/Hebrew witnesses. | Fragment images and metadata; Codex diplomatic text; Greek long and short recensions; Old Latin controls; overlap map by Tobit reference. | Aramaic/Hebrew fragment corpus, ranked restoration candidates, and a Tobit variation apparatus. |
| **Hebrew Ben Sira: Geniza MSS A–F, Masada, and Qumran** | Torn and stained leaves, uncertain letters, scattered witnesses, and differing Hebrew forms. | Existing Geniza photographs and open transcriptions; Masada and Qumran consultation records; Swete/Göttingen Greek; Syriac control; reference alignment. | Witness-separated Hebrew corpus and a verse-level Hebrew/Greek/Syriac apparatus. |
| **4QSam-a** | Fragmentary Hebrew that sometimes represents an older or different textual form. | Qumran image/transcription layer; WLC/UHB; Septuagint/Old Greek; relevant Masoretic codices. | Samuel variation units classified as spelling, copying, expansion, omission, or literary edition. |
| **4QJer-b and 4QJer-d** | Fragmentation plus shorter/longer textual forms and different ordering. | Qumran Hebrew; WLC/UHB; Old Greek Jeremiah; later Hebrew controls. | Jeremiah literary-form alignment without forcing every witness into MT order. |
| **4QDeut-q/n and 4QpaleoExod-m** | Fragmentation, paleo-Hebrew script, harmonization, and overlap with Samaritan/Greek readings. | Qumran witnesses; WLC/UHB; Samaritan Pentateuch; Old Greek; Targum/Peshitta controls where useful. | Pentateuchal variant apparatus with textual-family classification. |
| **11QPs-a / Hebrew Psalm 151** | Fragment order, different psalm sequence, lacunae, and non-Masoretic composition evidence. | Scroll text; WLC Psalms; Swete/Old Greek; other Qumran Psalms witnesses. | Psalms order/composition map and direct Hebrew Psalm 151 comparison. |

### Priority 2 — High-value Greek palimpsest and papyrus restoration

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Codex Ephraemi Rescriptus, OT and NT** | Erased biblical undertext beneath later writing, incomplete survival, and difficult layer separation. | Gallica color images; deterministic channel/rotation/contrast derivatives; existing editions as non-copying controls; Vaticanus, Sinaiticus, Alexandrinus, papyri, and current critical apparatus. | Line-addressable Greek undertext hypotheses, with observed and supplied characters kept separate. |
| **P45** | Abraded and highly fragmentary Gospel/Acts papyrus. | Images from all holding institutions; existing transcriptions; ECM/UBS apparatus; major Gospel and Acts witnesses. | Unified virtual-fragment registry and Greek variation units. |
| **P46** | Damaged edges, missing leaves, corrections, and distributed holdings. | Dublin/Michigan images and metadata; independent existing transcriptions; Pauline witnesses and current ECM preparation/critical apparatus. | Virtual codex order, hand/correction layers, and edge-reading candidates. |
| **P66** | Fragmentation and extensive scribal/self-correction layers. | Images, hand-separated transcription, P75/Vaticanus/Sinaiticus, and Johannine critical apparatus. | First-hand and correction-layer apparatus rather than a flattened consensus text. |
| **P75** | Localized edge loss and fragmentary Gospel coverage. | Vatican images; existing diplomatic text; P66 and major codices; current Luke/John apparatus. | Targeted verification of consequential readings; no unnecessary wholesale restoration. |
| **Oxyrhynchus NT fragments** | Scattered ownership, variable images, abrasion, and inconsistent identifiers. | Gregory-Aland-to-shelfmark registry; IIIF/archive links; passage mappings; current apparatus. | Searchable fragment registry and prioritized unresolved reading list. |

### Priority 3 — Major codex layers and the current gallery problem

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Codex Vaticanus, OT and NT** | Original ink, later retracing, corrections, and marginal signs need to be distinguished. | Vatican IIIF images and metadata; targeted deterministic derivatives; Sinaiticus/Alexandrinus; Old Greek and NT critical apparatus. | Layer-aware diplomatic records and a list of readings where the earlier hand can be distinguished. |
| **Codex Sinaiticus, OT and NT** | Numerous correctors and erasures; POB currently has a printed Tischendorf facsimile rather than manuscript photographs in the gallery. | Official standard/raking/multispectral images; official linked transcription; hand/corrector metadata; other major codices. | Replace or relabel the gallery source and import only unresolved correction-layer units for new analysis. |
| **Aleppo Codex** | Missing leaves and localized torn or faded surviving areas. Lost leaves cannot be recovered photographically. | Surviving images; recovered fragments; historical notes/descriptions; Leningrad and Sassoon comparisons. | Diplomatic surviving text plus clearly labeled documentary reconstruction of missing Masoretic information. |
| **Codex Sassoon 1053 and Leningrad** | Primarily collation, Masorah, vocalization, and localized-damage questions rather than large-scale physical recovery. | High-resolution images or lawful transcriptions; Aleppo; WLC/UHB; BHQ/BHS apparatus. | Masoretic comparison layer and transcription-error audit of the current POB base. |

### Priority 4 — Ancient versional witnesses

These can preserve early readings, but they are translations. Codex must restore
the Latin or Syriac witness first and must not silently turn it into certain
Greek.

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Codex Bobiensis** | Fire, damp, fragmentation, shrinkage, and old restoration. | Modern color images; older photographs/facsimiles; Old Latin comparison; Greek Mark/Matthew variation units. | Fresh Latin diplomatic layer and constrained Greek-reading implications. |
| **Codex Vercellensis Evangeliorum** | Severe deterioration and faded/erased text; multispectral work already exists. | Existing color/MSI derivatives if accessible; Old Latin witnesses; Greek Gospel apparatus. | Machine re-evaluation of recovered Latin letters without repeating imaging unnecessarily. |
| **Sinai Syriac 30** | Palimpsest undertext already substantially recovered by spectral imaging. | Published spectral images; existing Syriac editions; Curetonian Syriac; Greek Gospel apparatus. | New machine-readable Syriac diplomatic comparison, not a fresh-image-first project. |
| **Other Old Latin, Syriac, Coptic, Armenian, Georgian, and Geʿez witnesses** | Translation ambiguity and uneven digitization. | Book-specific version corpora and explicit translation-character profiles. | Targeted controls only where they can distinguish competing Hebrew/Aramaic/Greek readings. |

### Priority 5 — Lower-yield or tightly bounded targets

- **P52:** verify visible strokes and margins, but do not attempt to recreate its
  lost context.
- **Codex Washingtonianus:** target only consequential faded or corrected
  readings.
- **Well-preserved Leningrad passages:** use as transcription controls rather
  than image-restoration targets.
- **Physically missing Aleppo leaves:** documentary reconstruction only.
- **Sinaiticus passages already securely transcribed from official images:** no
  duplicate restoration work.

## Comparison-source packages to create

The source layout should extend the existing
`sources/dead_sea_scrolls/` evidence model rather than create an incompatible
second system:

```text
sources/textual_restoration/
├── registry.v1.json
├── images/
│   ├── original/                 # lawful archival pixels only
│   ├── derived/                  # deterministic Codex aids + sidecars
│   └── visual_reconstructions/   # ImageGen, watermarked and excluded
├── transcriptions/
│   ├── diplomatic/              # line/image-addressable readings
│   ├── normalized/              # mapped Hebrew/Aramaic/Greek text
│   └── passes/                  # frozen blinded Codex outputs
├── comparisons/
│   ├── ot_masoretic/
│   ├── ot_judean_desert/
│   ├── ot_old_greek/
│   ├── nt_greek/
│   └── ancient_versions/
├── alignments/                      # passage and fragment mappings
├── apparatus/                       # machine + reader-facing variants
├── restoration_candidates/          # never merged into observed ink
└── decisions/                       # POB adoption/non-adoption records
```

Each comparison package must say whether its source is:

- a direct Hebrew, Aramaic, or Greek witness;
- a daughter translation;
- a modern diplomatic transcription;
- a critical edition or apparatus;
- an editorial reconstruction; or
- an ImageGen visual reconstruction.

## Codex execution loop

Select the evidence route before starting. **Published-reading comparison is the
default:** identify the exact edition/apparatus and passage, preserve its
observed-versus-supplied distinctions, compare the discriminating witnesses and
strongest counterargument, and record the source/English consequence. Do not
require fresh image crops, model transcription or a new restoration receipt
merely to report a published reading. If the proposed claim depends on disputed
marks, corrections, joins or fresh decipherment, the controlling method's image
checks are required. Label published-only results “published-source comparison,”
not “machine-restored.”

**Fresh image transcription is a separate route**, required when the proposed
claim depends on those image-level questions. Use the steps
below for that route; previously imposed case-specific image gates remain in
force unless explicitly reassessed and reviewed:

1. Register the object, image, rights, hash, passage coverage, and comparison
   witnesses.
2. Preserve the archival image unchanged.
3. Generate only deterministic evidence derivatives: crop, registration,
   grayscale, contrast, channel separation, threshold, denoise, and permitted
   spectral combinations.
4. Run blinded transcription passes from at least two different model families
   over the same registered region and freeze both outputs.
5. Reconcile at glyph level. Exact agreement becomes
   `machine-consensus-accepted` for visible text or
   `machine-consensus-restored` for supplied text; preserve disagreements.
6. Compare against independent manuscripts, open transcriptions, critical
   apparatuses, and ancient versions.
7. Assign the observed, model-consensus, historically corroborated,
   hypothesis, or lost status at token level.
8. Emit the apparatus and a POB decision record. Main-text use requires a
   separate source-selection argument, English review, and synchronized
   application. Matching supplied letters retain their restoration status.
   Consensus flags alone cannot authorize a canonical change.
9. Optionally ask ImageGen to create a complete-looking educational image from
   the already documented text. Watermark it **RECONSTRUCTED — NOT MANUSCRIPT
   EVIDENCE**, store the prompt and source IDs, and prevent the image from
   re-entering step 3.

## Completion standard

A bounded comparison is complete when its actual evidence, serious alternatives,
uncertainty, source/English decision and reopening condition are documented.
Published-reading cases cite their consulted editions; new transcription cases
add source images, regions, frozen passes and diplomatic/normalized text under
the image gates above. Neither kind closes whole-book or all-source coverage.
An accepted change additionally needs the separate application checks; an
unresolved or no-change decision must not be advertised as a recovered reading.
Use one concise case record and one independent review, repeating review only for
substantive defects or changed evidence. ImageGen is optional and never raises
textual confidence.

Public claims must describe the work actually performed: published-source
comparison, machine transcription, or explicitly hypothetical reconstruction.
None is human-verified or definitive merely because an agent review passed.
The project should favor an explicit unresolved reading over a fluent invented one.
