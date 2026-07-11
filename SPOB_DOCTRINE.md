# SPOB Translation Doctrine

The **Simplified People's Open Bible (SPOB)** is the understanding-first English
edition of the People's Open Bible (POB). POB remains the controlling translation
and audit layer. SPOB communicates the meaning POB has established in language a
modern reader can understand on the first reading.

SPOB is allowed to be interpretive. It is not allowed to be unaccountably
interpretive.

## 1. Governing aim

For each passage, SPOB asks:

> What wording will let a modern common reader understand as much as possible of
> what this passage is communicating, without mistaking an interpreter's theory
> for what the passage itself establishes?

The target is **maximum warranted understanding**, not maximum verbal similarity.
SPOB should freely replace unfamiliar idioms, inherited church vocabulary,
opaque metaphors, ancient measures, and difficult syntax when their meaning is
reasonably clear. It should retain or explain them when replacing them would erase
an important image, ambiguity, or theological claim.

## 2. Authority order

Every interpretive rendering must follow this order:

1. **Source text and textual evidence** recorded in the POB source payload.
2. **Immediate literary context**: sentence, paragraph, argument, genre, and
   repeated vocabulary in the same book.
3. **POB's audited decisions**: lexical decisions, theological decisions,
   footnotes, revision history, and documented cross-checks.
4. **Broader canonical usage** where it genuinely clarifies the author's meaning.
5. **Historical and modern interpreters** as witnesses, never as controlling
   authorities.

An interpretation associated with a historical teacher, church tradition,
denomination, or modern interpreter may alert reviewers to a possible meaning.
It enters SPOB's main text only when the higher layers independently support it.
If the interpretation depends on an interpreter's larger doctrinal system rather
than the passage itself, it belongs in attributed study material, not in the
translation.

## 3. Interpretive expansion rule

SPOB may state an implication more directly than POB when all of these are true:

1. The implication is strongly supported by the source and immediate context.
2. It helps a modern reader recover meaning that a formally correct English phrase
   would likely hide.
3. It does not collapse a live ambiguity, merge distinct source terms, or add a
   doctrinal conclusion the passage does not require.
4. The draft records the expansion, evidence, confidence, and preserved
   alternatives in `interpretive_expansions`.

Use three confidence levels:

- **High** — the main text may express the meaning directly.
- **Moderate** — prefer a bounded phrase that preserves semantic range, or retain
  the POB wording with a short note.
- **Low or tradition-dependent** — do not put it in the main text.

## 4. Preserve distinctions, not obscurity

Understanding-first translation does not mean reducing several ideas to one.
When the source uses two meaningful terms, SPOB should normally keep two ideas in
clear English.

### Calibration example: Ecclesiastes 1:2

POB:

> Breath of breaths, says Qoheleth; breath of breaths, all is mere breath.

Preferred SPOB direction:

> **“Vapor of vapors,” says Qoheleth. “Everything is vapor—brief, impossible to
> hold onto, and often not what we expect.”**

Why this is warranted:

- Hebrew `הֶבֶל` (*hevel*) literally evokes breath or vapor, not modern “vanity”
  as self-admiration.
- Across Ecclesiastes, the image carries transience, elusiveness, and the mismatch
  between what people expect and what actually happens.
- “Vapor” preserves the concrete image. The bounded explanation helps readers
  understand the author's recurring point without turning it into the stronger
  claim that absolutely nothing has meaning.
- “Gas” may be useful in conversation, but “vapor” is the better main-text word:
  gas sounds scientific and stable, while *hevel* evokes something visible for a
  moment that cannot be held.

An under-translation would retain “vanity” or “breath” without helping modern
readers recover the image's force. An over-translation would reduce the whole book
to “nothing matters,” which Qoheleth's argument does not require.

### Additional calibration examples

- **Genesis 1:1** — preserve the live relation between the opening creation
  statement and the following description rather than pretending every English
  translation resolves the syntax identically.
- **Isaiah 7:14** — make the immediate historical wording understandable while
  preserving the textual and Christian reception questions normally represented
  by “young woman” and “virgin.”
- **Luke 17:21** — explain that God's kingdom is present “among” or “in the midst
  of” the hearers when context supports that sense; do not silently turn the saying
  into only an inward private experience.
- **Romans 3:25** — explain the atonement/mercy-seat image without forcing a single
  later theory into the verse.
- **Philippians 2:6** — make the difficult “something to be grasped/exploited”
  phrase understandable while preserving the interpretive decision in the audit.
- **1 Timothy 2:12** — do not hide the disputed force of the rare authority verb;
  the main text and note must distinguish what is established from what remains
  debated.

## 5. Main-text permissions

SPOB may:

- turn source idioms into their clear modern meaning;
- make an implied subject, object, or logical connection explicit when grammar
  and context establish it;
- use a bounded clarifier such as “spiritually,” “that is,” or “meaning” when it
  prevents a likely modern misunderstanding;
- split long sentences and reorder clauses;
- use common modern equivalents for ancient social, monetary, legal, ritual, and
  agricultural language;
- translate vivid contextual action naturally, such as “prowls” in a lion image.

SPOB must not:

- insert a denomination's doctrinal system into the main text;
- convert a possible application into the passage's only meaning;
- erase uncertainty that POB intentionally preserves;
- silently harmonize one passage to another;
- weaken difficult moral, judgment, supernatural, or theological claims merely
  to make them more comfortable;
- turn Scripture into commentary, sermon language, or motivational advice.

## 6. Named-interpreter safeguard

External interpreters can affect SPOB in only three auditable ways:

1. **Question generator** — their reading identifies something to investigate.
2. **Corroborating witness** — their reading agrees with a conclusion already
   supported by source, context, and POB reasoning.
3. **Attributed alternative** — a study note records the interpretation and names
   its source without putting it into the Bible text.

No model prompt should say “translate according to” any single teacher. If an
interpreter's reading is supplied during review, the record should identify it
under `external_witnesses` and explain whether the text independently supports it.

## 7. Required review questions

A SPOB draft passes only if reviewers can answer **yes** to each:

1. Is it materially easier to understand than POB?
2. Does it communicate POB's controlling meaning rather than merely shorten it?
3. Are any added interpretive words warranted by source, context, and POB notes?
4. Does it preserve distinct ideas, meaningful ambiguity, and theological force?
5. Could a reader tell from the record where a contested interpretation came
   from?
6. Would readers from different Christian traditions still recognize the verse
   as a responsible rendering rather than a hidden denominational commentary?

## 8. Publication status

AI output is a **draft**, never self-authenticating Scripture. Model agreement is
useful evidence about clarity, not proof of correctness. High-risk verses—those
with interpretive expansions, textual variants, doctrinal disputes, or named
external witnesses—require explicit human review before moving beyond
`simplified_draft`.
