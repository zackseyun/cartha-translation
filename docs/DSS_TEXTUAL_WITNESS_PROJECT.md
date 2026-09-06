# POB Dead Sea Scrolls and Ancient Witness Project

## Decision

Revised 2026-09-04. [Method 2.0](TEXTUAL_ADJUDICATION_METHOD.md) governs
source selection and publication; the [approach review](TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md)
documents the revised calibration and acceptance policy.

The [central research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md) records the
evidence-linked history, decisions, corrections and unresolved work. Add an
entry after each substantive pass; the detailed reports remain its evidence.

The People's Open Bible will maintain a dedicated, source-grounded program for
the Dead Sea Scrolls and other ancient Hebrew, Aramaic, and Greek witnesses.
The program has two related outputs:

1. **Fresh manuscript data:** lawful images, deterministic image derivatives,
   diplomatic transcriptions, normalized texts, and explicit restoration
   hypotheses.
2. **Comparative translation evidence:** verse- or unit-level alignments that
   show where ancient witnesses agree, differ, or cannot be compared, followed
   by an auditable POB English translation decision.

This is a POB textual-witness project, not a new canon declaration. Manuscript
comparison can help us recover the earliest attainable wording and translate it
more responsibly. It cannot mechanically prove which writings are divinely
inspired or erase the historical and theological work of canon discernment.

## Non-negotiable integrity rules

- **Observed ink is not reconstructed text.** Every character is tagged as
  visible, uncertain, lost, supplied from a parallel, or editorial conjecture.
- **Never paint generated letters into an evidence image.** AI image generation
  may be used for clearly labeled educational art, but never as the source for
  transcription or textual criticism.
- **Enhancement is reversible and reproducible.** Contrast, grayscale,
  sharpening, and spectral combinations retain the original image, parameters,
  and hashes. No generative inpainting is allowed in the evidence lane.
- **A fresh transcription is still accountable to its image.** Owning our data
  means producing and licensing our own transcription and annotations; it does
  not mean hiding the repository, photographer, shelfmark, or image license.
- **Do not copy modern scholarly reconstructions.** Restricted editions may be
  consulted and cited at fact level, but their supplied letters and distinctive
  reconstructions are not silently reproduced.
- **No access circumvention.** Publicly viewable does not mean redistributable.
  The IAA Leon Levy library currently permits only single copies for private use
  absent written permission. Its records remain metadata-only until permission
  is documented.
- **Canonical status stays explicit.** Biblical, deuterocanonical,
  extra-canonical, sectarian, documentary, and unidentified material remain
  distinguishable in data and readers.
- **Two different models provide a working transcription check.** When two
  different model families independently return the exact same diplomatic
  glyphs or tokens from the same image region, POB treats that reading as
  `machine-consensus-accepted`. The models may not see one another's output.
  Two runs of the same model do not satisfy this rule. Accuracy must still be
  measured on frozen controls; consensus is not historical corroboration.
- **Agreement does not turn supplied ink into visible ink.** If both models
  independently supply the same damaged or missing letters, the result is
  `machine-consensus-restored`: accepted as a working comparison hypothesis,
  bracketed and disclosed as a restoration. Translation adoption requires a
  separate source-selection argument and application review.

## Evidence lanes

| Lane | What it contains | May drive translation? |
|---|---|---|
| A — Source image | Lawfully vendored original or externally linked restricted image | Yes, when legible |
| B — Deterministic derivative | Crop, grayscale, contrast, threshold, or non-generative spectral combination | Yes, checked against A |
| C — Diplomatic transcription | Visible characters, line breaks, scribal marks, and lacunae | Yes |
| D — Restoration hypotheses | Ranked completions with method, parallel, confidence, and model-consensus status | Only after a separate textual argument and review; agreement alone is insufficient |
| E — Normalized text | Searchable Hebrew/Aramaic/Greek with orthographic normalization mapped to C | Yes |
| F — Alignment and apparatus | Witness-to-witness units, variants, omissions, additions, and transpositions | Yes |
| G — POB translation | English rendering plus rationale and alternatives | Publication output |
| H — Educational reconstruction | Optional generated illustration or facsimile, visibly watermarked as reconstructed | **Never** |

## Initial corpus

The machine-readable inventory is
[`sources/dead_sea_scrolls/registry.v1.json`](../sources/dead_sea_scrolls/registry.v1.json).
The first wave is intentionally diverse rather than enormous:

- **Anchor scrolls:** Great Isaiah Scroll, Community Rule, War Scroll,
  Thanksgiving Hymns, Pesher Habakkuk, Temple Scroll, Damascus Document,
  Genesis Apocryphon, 4QMMT, and Songs of the Sabbath Sacrifice.
- **Already-known works represented at Qumran:** 1 Enoch, Jubilees, Tobit,
  Sirach, Letter of Jeremiah, and the Psalms material that includes Psalm 151.
- **Biblical comparison pilots:** Isaiah, Samuel, Jeremiah, Psalms,
  Deuteronomy, the Twelve, and Daniel. These offer useful examples of spelling,
  smaller variants, larger textual forms, ordering, and translation alignment.

The first lawful image seed contains two independent Library of Congress views
each of the War Scroll and Pesher Habakkuk. The LOC records say **“No known
restrictions on publication.”** These are research photographs rather than the
full modern multispectral archive, so they are suitable for pipeline setup and
limited paleographic work—not full-scroll transcription.

## Comparison expansion beyond Qumran

The comparison program should add witnesses only when their provenance and
reuse status are known. Priorities are recorded in
[`sources/dead_sea_scrolls/comparison_witnesses.v1.json`](../sources/dead_sea_scrolls/comparison_witnesses.v1.json).

### Hebrew and closely related witnesses

- Samaritan Pentateuch manuscripts and a legally reusable transcription.
- Nash Papyrus, Ketef Hinnom, Masada, Wadi Murabba'at, and Nahal Hever.
- Cairo Genizah biblical manuscripts and Hebrew Ben Sira witnesses.
- Aleppo Codex, Leningrad Codex, and other carefully selected medieval Masoretic
  witnesses, without mistaking date for textual value.

### Aramaic witnesses

- Qumran Aramaic works and biblical translations.
- Targum Onkelos, Targum Jonathan, and selected Palestinian Targum witnesses.
- Syriac Peshitta witnesses when they help identify an earlier Semitic reading.
- Aramaic Levi and other works whose Qumran witnesses overlap later copies.

### Greek witnesses

- Greek Judaean Desert fragments, especially the Minor Prophets scroll from
  Nahal Hever.
- Old Greek/Septuagint witnesses represented by public-domain editions and
  lawfully usable manuscript images.
- Codices Sinaiticus, Vaticanus, and Alexandrinus where their image or text terms
  permit the intended use.
- Greek New Testament papyri and major codices for New Testament comparison.

Latin, Syriac, Ge'ez, Coptic, and other daughter versions remain valuable
controls when Hebrew, Aramaic, or Greek is lost. They must never be mislabeled
as direct surviving originals.

## Workflow

### Phase 0 — Registry and rights gate (started)

1. Give every object a stable manuscript ID, composition ID, shelfmark, holding
   institution, language, script, date range, image record, and rights status.
2. Store immutable URLs and SHA-256 hashes for every downloaded file.
3. Allow automated download only for `public-domain`, compatible open licenses,
   or `no-known-restrictions` records. Everything else is metadata-only.

### Phase 1 — Image acquisition and derivatives (pilot complete)

1. Retrieve the four LOC preview files and full-resolution TIFF masters.
2. Keep full masters rehydratable and out of ordinary Git history; record their
   exact hashes in the registry.
3. Produce deterministic transcription views with a JSON provenance sidecar.
4. Request written permission from the IAA/Israel Museum for the priority
   archive, including redistribution and derivative-processing rights.

### Phase 2 — Diplomatic transcription

1. Segment by fragment, column, line, and image region.
2. Run at least two independent passes from different model families without
   showing one pass to the other.
3. Preserve word spacing, line endings, damaged glyphs, supralinear additions,
   cancellations, and scribal marks.
4. Reconcile only after independent passes are frozen.
5. Promote exact agreement on visible text to `machine-consensus-accepted`.
   Promote exact agreement on supplied text to `machine-consensus-restored`
   while preserving brackets and the restoration rationale. Disagreements stay
   `machine-hypothesis` until evidence resolves them. These are working
   transcription states, not source-selection or publication approvals.

Measure the workflow on frozen controls before scaling acceptance. Separate
image-only reading from context-informed completion and record their different
error modes. A later model reviewing prior outputs is not a blind pass.

### Phase 3 — Restoration hypotheses

For each lacuna, store zero or more candidate restorations with:

- visible left/right context;
- number of missing character spaces;
- supporting parallel witness, if any;
- grammatical and orthographic rationale;
- model and prompt provenance;
- confidence and competing candidates;
- both model/pass IDs, exact-agreement scope, comparison source IDs, and the
  model-consensus decision.

The diplomatic layer continues to show the lacuna and brackets even when a
candidate receives working model consensus. Translation records must allow a
reader or export to distinguish and optionally exclude restored wording.

### Phase 4 — Witness alignment and collation

1. Map units to POB references without forcing non-biblical works into biblical
   versification.
2. Align the DSS reading against WLC/UHB, relevant Septuagint witnesses,
   Samaritan Pentateuch, Targums, Peshitta, and other witnesses by availability.
3. Classify differences: orthography, morphology, lexical substitution,
   omission, addition, transposition, harmonization, or larger literary form.
4. Record both agreement and non-comparability; silence is not agreement.

Apply the [source-wording adjudication method](TEXTUAL_ADJUDICATION_METHOD.md)
when choosing among readings. Older manuscripts receive a modest preference,
not an automatic win; transcription acceptance and historical text selection
remain separate decisions.

### Phase 5 — English translation adjudication

Codex receives the visible source, diplomatic transcription, normalized text,
alignment, and variants—not merely a consensus string. It records:

- the earliest attainable reading used;
- why one witness or reading was preferred;
- equally plausible alternatives;
- whether the choice changes meaning or only spelling/style;
- whether an English footnote is required;
- whether canonical-status or source-survival disclosure is required.

### Phase 6 — Machine corroboration and publication

- At least two blinded passes from different model families for fresh image
  transcription. Exact agreement is a working consistency check; measured
  accuracy and historical corroboration are separate fields.
- Working transcription acceptance does not confer publication authority.
  Complete the source-selection argument, English review, and synchronized
  source/English/notes/export checks. Published-text research uses its own
  documented evidence and review route; fresh images are required for claims
  that depend on fresh decipherment or unresolved marks.
- Public issue/discussion link for disputed units.
- Corpus release only after license, hash, schema, image-region, transcription,
  corroboration, and uncertainty checks pass.
- Reader surfaces show the actual lawful manuscript image when making a
  manuscript claim; otherwise they say that the image is unavailable or
  representative.

## Completion standard

A manuscript is not “reconstructed” merely because a model produced fluent
Hebrew or English. A unit is complete only when the source image and rights are
recorded, the diplomatic text is image-addressable, every supplied character is
marked, two different blinded models have been reconciled, the comparison
apparatus is stored, and the model-consensus status is explicit. Public claims
must say **dual-model transcribed** or **dual-model restored and source-compared**,
not human-verified. These descriptions must match work actually performed.
For published-text cases, say “published-source comparison.” Completion of
research does not certify a novel reading, recovered autograph, or publication.
Publication and deployment remain separate steps. The target order and source
packages are defined in
[`TEXTUAL_RESTORATION_PRIORITIES.md`](TEXTUAL_RESTORATION_PRIORITIES.md).
