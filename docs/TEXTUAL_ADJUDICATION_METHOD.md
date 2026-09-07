# POB source-wording adjudication method

Version: 2.0.0 · Revised: 2026-09-05 (identity/provenance and evaluation clarification)

This is the controlling method for source selection and English impact. The
[approach review](TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md) records the
assessment, calibration plan, delivery sequence, and implementation gaps.
Existing version-1 decision records require case-level review before claiming
version-2 compliance. Transcription consensus labels do not confer publication
authority.

The [OT/NT source coverage audit](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md)
defines the required source classes, dated catalogue checks, edition-status
checks, and inclusion/exclusion criteria. A family registry or edition index
does not certify that all known manuscripts have been compared.

## Objective and operating constraint

Reconstruct the earliest attainable wording justified by the surviving
evidence, in the language actually attested. This is not a promise to recover
an autograph, a new canon declaration, or a rule that every later reading is
inferior. Codex performs the work; newly commissioned human transcriptions are
not a prerequisite. Existing editions and published readings remain usable
sources under the repository's rights policy.

**Older manuscripts receive a modest preference when other evidence is
comparable.** This preference is explicit but is never an automatic override.
A late copy can transmit an early reading, and an early copy can contain an
error. Record separately the date of the physical object, the date of a
translation or author's work, and the earliest attestation of a reading. Do not
give a medieval copy the date of the ancient translation it contains. Overlapping
or unverified date ranges do not establish a precise chronological advantage.

## Four separate decisions

1. **Observation:** what marks or published readings are actually available?
2. **Transcription:** what does this particular witness say, including its
   errors, corrections, gaps, and supplied characters?
3. **Text selection:** which reading best accounts for the transmission of this
   passage, and how certain is that choice?
4. **Translation:** how should the chosen wording be expressed in English,
   preserving important ambiguity and disclosing alternatives?

A correct transcription of a late copy is not automatically the best critical
text. A fluent English sentence is not evidence for its supposed Hebrew source.
The existing two-model transcription workflow is a working accuracy check, not
an additional ancient witness or a statistical proof of authenticity. Never
claim a second blinded model pass occurred unless its actual output is stored.

## Evaluation order

### 1. Establish the target and the available evidence

- Search the applicable catalogues and critical apparatuses, record the cutoff
  and actual query results, and distinguish discovered, accessible, collated,
  and adjudicated coverage. Log exclusions and unavailable evidence; never
  silently turn a convenience sample into an exhaustive witness list.
- Declare the target literary form and whether the output is diplomatic,
  eclectic, or parallel-edition text. Use a pinned base plus explicit changes;
  justify combinations across literary forms at passage level.
- Give the book, passage, fragment, language, and edition an unambiguous ID.
- Preserve upstream IDs separately from proposed object identities. Record
  fragment joins/splits, hand assignments, dates, authority and review status
  in a versioned crosswalk before migrating labels. An old catalogue whole
  and its reassigned parts must not become extra independent votes. A passage
  range does not verify every fragment assignment or surviving letter; see the
  [4Q24 identity review](LEVITICUS_WITNESS_IDENTITY_REVIEW_2026-09-05.md).
- Identify direct-language manuscripts, ancient translations, quotations or
  retellings, and later reception evidence separately.
- Distinguish language from textual function: a Hebrew excerpt collection is
  direct Hebrew evidence but not automatically a continuous book copy. Test
  adaptation and excerpt boundaries locally; do not exclude or privilege it
  solely by genre. Record whether a later reassessment was read in full or
  only its abstract; see the [4Q37 follow-up](PENTATEUCH_SOURCE_COMPARISON_PASS_4.md).
- For a report from an edition, say **published reading**; for newly read
  pixels, give the image ID and region. Do not substitute one claim for the other.
- Check errata, disputed fragment identifications, and later reassessments of
  decisive readings. A recent digital release date does not establish that
  earlier editorial claims have been revised. Record which arguments and
  images were actually inspected; an unresolved identification cannot count as
  secure reading support. See the [Samuel pass-2 example](SAMUEL_SOURCE_COMPARISON_PASS_2.md).
- Distinguish an attested omission from a physical lacuna or a witness that
  does not cover the passage. No coverage contributes no evidence either way.
- Preserve spelling, vowels, accents, scribal hands, and corrections in the
  diplomatic layer; normalize only in a separately mapped comparison layer.

### 2. Assess each witness in this passage

Original-language primacy is not automatic Masoretic priority. When another
Hebrew/Aramaic manuscript differs, both are direct-language evidence. Likewise,
theological usefulness or avoidance of a theological reading cannot decide
between them. Retaining a declared base while adjudication remains open must
be described as provisional retention, not a demonstrated historical victory.
See the [Psalm 22 comparison](PSALM_22_SOURCE_COMPARISON_PASS_1.md).

Evaluate legibility, whether the relevant letters survive, date uncertainty,
corrections, and the witness's local copying or translation behavior. Reputation
or antiquity of the manuscript as a whole does not replace passage-level work.
A supplied word cannot become visible ink through model agreement.

Reference filtering must not erase preservation context. A supply bracket can
open in another verse or physical line; inspect the complete surrounding
transcription before treating an unbracketed excerpt as preserved. The
[Isaiah 54 check](ISAIAH_54_PESHER_REVIEW_2026-09-05.md) demonstrates this with
4Q69a. The extractor's optional line context is a navigation safeguard, not
an automatic preservation assessment.

Check whether the preserved portion actually distinguishes the alternatives.
A word-prefix or verse-range hit may locate a candidate while leaving the
decisive ending missing. Record a shared-prefix fit as inconclusive for that
specific contrast, not universal irrelevance of the witness. Use reconstructed
space or other surviving features only with their own evidence. Keep illustrative
linguistic contrasts distinct from attested apparatus variants; see the
[4Q120 preservation review](4Q120_LEVITICUS_PRESERVATION_REVIEW_2026-09-05.md).

For an ancient translation, record three separate claims: **the attested
wording in that language**, **which competing source interpretations it can
distinguish**, and **any proposed Hebrew/Aramaic or Greek back-translation**.
The first does not prove the third. Check local morphology, semantic range,
expansion and omission, then the book's translation practice and possible
dependence on another version. Shared broad meaning is not necessarily shared
source spelling. An interpretive addition is evidence about the version, not
automatically a lost source word. Keep the strongest counter-explanation.

Language is not script: Targum Psalms in Hebrew letters is Aramaic. Identify
the actual edition and its manuscript basis; a modern electronic compilation
is not one ancient copy. An empty local variant display does not establish
unanimity. Psalm 22 illustrates the distinction: the Syriac injury action and
the Targum's biting-plus-lion rendering must not be collapsed into one shared
Hebrew verb. The same rule applies when using NT versions to infer Greek.

Version names do not imply internally uniform texts. Record the exact
translation/revision, edition and date, manuscript or hand where available,
and source-local passage label plus a content-based alignment anchor. Consult
all adjacent apparatus units needed to assemble the claimed phrase for the
same witness and hand. Agreement on the first noun does not establish agreement
on its following modifier; retain corrections and uncertainty qualifiers.
The [Deuteronomy Greek follow-up](PENTATEUCH_SOURCE_COMPARISON_PASS_4.md)
shows why a secondary complete-phrase attribution requires this check. Consult
the apparatus conventions before turning silence into support; distinguish an
explicit omission report from an unmentioned or unavailable witness. An
edition's absence claim must not silently become absence in an entire version.
The [Psalm 145 Latin follow-up](PSALM_145_SOURCE_COMPARISON_2026-09-05.md)
demonstrates disagreement between two editions of the Hebrew-based Latin
Psalter itself. Preserve both controls and contrary apparatus reports; resolve
the version's text before using it to infer Hebrew or Greek. This applies to
OT and NT versional evidence alike.

### 3. Assess relationships before counting support

Keep an edition's **selected text** separate from its **attested readings**.
A conjecture may explain the surviving alternatives without itself occurring
in a manuscript. Label it explicitly, identify the evidence and competing
explanation, and do not convert scholarly adoption into a new witness or an
independent project-review receipt. The 2008 OHB Deuteronomy 32:8 sample
illustrates this distinction: see the [bounded review](PENTATEUCH_SOURCE_COMPARISON_PASS_4.md#ohb-sample-editorial-conjecture-check--2026-09-05).

Group related evidence and document uncertainty about those relationships.
WLC and UHB are two digital controls on a largely shared Masoretic tradition,
not two independent ancient Hebrew branches. An Old Latin rendering derived
from Greek is not a second independent Hebrew attestation. A historian may
depend on the same Greek textual form as an extant translation tradition.

The number of supporting witnesses may be reported descriptively, but it must
not select the reading. Modern English translations are not manuscript votes.

### 4. Test competing explanations

For every serious candidate, record both the strongest supporting evidence and
the strongest objection. Consider common copying changes: skipped repeated
endings, duplicated text, similar letters, numerical assimilation,
harmonization, explanatory expansion, word order, and corrections.

Ask which candidate best explains the others with the fewest unsupported
steps. Neither **shorter** nor **more difficult** automatically means earlier.
Do not invent an ancient scribe's motive. Grammar and context can rule against
an implausible proposal, but should not manufacture unattested letters.

### 5. Apply the modest chronological preference

Use older physical witnesses to tilt a close comparison, especially where an
early direct-language reading agrees with an independently transmitted version.
Explain the effect in prose. Do not assign arbitrary numerical weights or
present a model-generated percentage as the probability of the original text.

If chronology conflicts with clear copying evidence, the better transmission
explanation wins. If the earlier attestation is a translation, record what
source-language alternatives it can and cannot distinguish.
Test whether removing the chronological preference would change the outcome.
Do not count the same early attestation twice under different criteria.

### 6. Preserve genuine literary alternatives

Where witnesses represent different literary forms, do not silently create a
hybrid that existed in neither tradition. Decide and disclose the target form
per book or passage, retaining the other form in the apparatus. A versional
reading may justify a source-language hypothesis, but not a claim that its
exact retroverted Hebrew survives.

### 7. Record a calibrated outcome

Use a reasoned working preference, a held decision, or an unresolved outcome.
State separately confidence in **attestation** and confidence in **priority**.
Published attestation may be secure while the earliest wording remains unclear.
Split decisions when necessary: a line's inclusion and its exact wording can
have different outcomes.

Also distinguish object identification, alignment, daughter-version inference,
and English-rendering uncertainty. No single “confidence” field substitutes
for these judgments. Record the decisive observed/supplied characters locally.

Research records do not automatically change canonical verse YAML. Promotion
is a separate recorded action after the relevant source, rights, review, and
reader-disclosure checks. No deployment is implied by source adjudication.

## Calibration and review

Retain the two-family blinded workflow for fresh machine transcription. Freeze
outputs before reconciliation, withhold known readings where practical, and
keep image-only observation separate from context-informed restoration.
Two agreeing restorations remain supplied proposals until a separate textual
argument supports their use. Different models can share errors or recall the
same familiar text. A model upgrade does not create an independent review.

Before broad acceptance, freeze a varied evaluation set and acceptance criteria
and measure errors, false visible-letter claims, abstentions, and errors among
accepted readings. Stratify results by script and damage; uncertain published
labels remain uncertain. Record actual outputs and measured performance.
Benchmark execution is pending; no current result is certified by this plan.

Implementation check, 2026-09-06: the existing DSS pilot comparator now excludes
editorial annotations from automatic clear-token agreement using a conservative
Hebrew-character filter. Before the repair, matching angle-bracket supplies,
Latin restoration comments and generic combining uncertainty dots could be
counted as accepted. Annotated tokens remain in the report for adjudication;
valid Hebrew points remain eligible. This is a tested software safeguard, not
measured image-reading accuracy or proof that a model's clear label is correct.

The frozen two-crop pilot still has only one successful provider response; its
saved second-provider access failure is not a live process or a second reading.
Do not repeat inference without a legitimate new access route. Before adding
blank controls, use the new opt-in [observation protocol 2.0](../sources/dead_sea_scrolls/protocols/README.md)
to distinguish no visible text from failure to assess. The legacy protocol
requires a nonempty token row for every region and cannot represent a successful
empty observation. The new schema, prompt and tested validator support that
distinction, but provider execution and benchmark evaluation remain pending.
The old prompts, schemas and receipts are preserved, not retroactively upgraded.

A [four-region development control set](../sources/dead_sea_scrolls/pilots/2026-09-06-observation-development/README.md)
now freezes actual image crops, observation-only labels, prompt/schema and
pre-run criteria. It has two writing regions and two negative regions from one
already-used manuscript photograph. Inputs were visually checked and labels
independently reviewed without expected labels. The [first OpenAI run](../sources/dead_sea_scrolls/pilots/2026-09-06-observation-development/RESULTS.md)
matched all four observation classes but produced no Hebrew letters: all text
tokens were unreadable/gap placeholders. No character-accuracy result exists.
The set is not held out and does not replace the varied,
manuscript-disjoint evaluation required before broad acceptance.

Published-text comparisons may proceed without freshly transcribing every
image. Require image checks where the proposed claim depends on disputed marks,
corrections, joins, or a fresh decipherment. Existing case-specific pending
gates cannot be waived merely by changing a status flag.

## English review and application

Review textual changes and English-only improvements separately. Compare the
chosen source, a close gloss, current POB, and a candidate in paragraph context.
Assess meaning, ambiguity, unsupported additions, literary effect, readability,
and justified consistency. Blind candidate identity and vary candidate order.
Record translation-policy effects explicitly, including where grammatical
form and referential meaning differ. Unchanged POB is a valid outcome.

Unchanged consonants do not necessarily mean an English-only decision. A new
vocalization or morphological analysis requires an explicit source-interpretation
record; contextual English referent clarification is a different operation.
Distinguish a repointed imperative from an imperative used only as an English
restatement of an injunction. See the
[Leviticus 2:8 review](LEVITICUS_2_8_AGENCY_REVIEW_2026-09-05.md).

Apply approved changes through one package linking the pinned base, selected
source units, resulting source text, English, notes, metadata, review evidence,
and export verification. Old review scores and timestamps describe their old
input hashes; they cannot certify edited text. Preserve before/after records.
The current selection schema supports research bundles only. It does not yet
implement application receipts or certify canonical publication.

A concrete [full-record draft and preflight](APPLICATION_DRAFT_PREFLIGHT_2026-09-05.md)
now exercises this boundary without applying a change. Materializing a complete
candidate is not completing its full-source review gate. Archive old review
flags without inventing their original input bindings, and inspect the actual
exported notes/disclosure, not just successful export of the English string.
Schema acceptance, local export behavior and deployed reader behavior are
separate checks. A source label must describe the editorial corpus honestly;
do not retain a base-edition label solely to satisfy an existing enum.

### Translation evaluation contract

Before a candidate comparison, record the passage/context, pinned source and
POB inputs, translation-policy constraints, intended improvement and rubric.
Keep source-selection changes separate from rendering changes against the same
source. Review meaning and unsupported additions first, then preserved
ambiguity, literary function, naturalness and justified consistency. Explain
tradeoffs rather than collapsing them into an unexplained overall score.

Store actual candidate assessments and disagreements. Hide candidate identities
and vary order where a blind comparison is claimed; a continuation by the same
assistant is not an independent review. A successful round-trip translation or
model preference is only a diagnostic, not proof of fidelity.

For a broad improvement claim, freeze the sample and acceptance criteria before
evaluation. Include randomly selected unflagged passages alongside stratified
high-impact/difficult cases, report those strata separately, and prevent
development examples from becoming held-out evaluation examples. Report the
denominator, improvements, regressions, ties, unresolved cases and review basis.
No such corpus-wide result has yet been established. Log negative results and
state what new evidence would reopen a closed or held case.

## ImageGen and restoration

ImageGen is display-only. It cannot supply textual evidence, recover an absent
spectral exposure, or validate a lost letter. Retain raw images and reproducible
non-generative derivatives. Mark the image lane, observation basis, restored
characters, and model-pass provenance explicitly.

## First applied pass

The three-passage [applied report](HEBREW_PILOT_ADJUDICATION.md) uses a
[machine-readable decision record](../sources/textual_restoration/decisions/hebrew_pilot.v1.json)
with additional witnesses, dependency cautions, chronological effects, and
counterarguments. It is an editorial assessment of published readings, not a
fresh manuscript transcription or an assertion of cross-model review.

Validate and regenerate it with:

```bash
python3 tools/textual_restoration/adjudication.py --check-current-baseline --report
python3 -m unittest discover -s tests -p 'test_textual_adjudication.py'
```

The validator checks the record's integrity, provenance references, and
disclosure gates. It cannot validate scholarly truth. Disagreements remain in
the record and can change the working preference as better evidence arrives.
