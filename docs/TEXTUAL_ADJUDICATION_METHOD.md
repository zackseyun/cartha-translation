# POB source-wording adjudication method

Version: 1.0.0 · Adopted: 2026-09-02

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

- Give the book, passage, fragment, language, and edition an unambiguous ID.
- Identify direct-language manuscripts, ancient translations, quotations or
  retellings, and later reception evidence separately.
- For a report from an edition, say **published reading**; for newly read
  pixels, give the image ID and region. Do not substitute one claim for the other.
- Distinguish an attested omission from a physical lacuna or a witness that
  does not cover the passage. No coverage contributes no evidence either way.
- Preserve spelling, vowels, accents, scribal hands, and corrections in the
  diplomatic layer; normalize only in a separately mapped comparison layer.

### 2. Assess each witness in this passage

Evaluate legibility, whether the relevant letters survive, date uncertainty,
corrections, and the witness's local copying or translation behavior. Reputation
or antiquity of the manuscript as a whole does not replace passage-level work.
A supplied word cannot become visible ink through model agreement.

### 3. Assess relationships before counting support

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

Research records do not automatically change canonical verse YAML. Promotion
is a separate recorded action after the relevant source, rights, review, and
reader-disclosure checks. No deployment is implied by source adjudication.

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
