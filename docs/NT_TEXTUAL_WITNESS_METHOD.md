# New Testament source-wording track

## Scope

Revised 2026-09-04 under method 2.0. The
[approach review](TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md) also applies
to this track: calibrate model review, separate transcription certainty from
historical priority, and test English fidelity independently of source changes.

Apply the [shared source-wording method](TEXTUAL_ADJUDICATION_METHOD.md) to
Greek, not to a guessed Hebrew original of the New Testament. The working
target is the earliest attainable Greek text within a documented textual
history. Older manuscripts receive a modest preference, while local scribal
behavior and relationships can outweigh date.

The [66-book map](HEBREW_AND_NT_VARIANT_MAP.md) and
[priority casebook](TEXTUAL_VARIANT_CASEBOOK.md) are the initial research queue.
They do not authorize silent source replacement.

### Supplementary reader records

An absent base-edition verse is not a missing row to invent. Where POB already
has a secondary-witness translation, verify the cited edition/version, exact
wording and source-to-reader reference mapping before setting
`reader_supplement: true`. Preserve the secondary status and disclose editorial
placement in an anchored textual note. The mobile exporter requires those
structural safeguards; the boolean records a scoped editorial inclusion decision,
not an automated provenance check, earliest-text judgment or whole-verse approval.
Unreviewed supplementary records stay excluded. Check both base-edition and POB
record coverage so a successful export cannot be mistaken for complete coverage.
The [Romans pilot](ROMANS_5_1_SOURCE_COMPARISON_2026-09-06.md#supplementary-doxology-delivery--2026-09-06)
has 433/433 IDs with three disclosed supplements; its missing legacy generation
hashes remain explicit schema debt, not reconstructed evidence.

The [2026-09-04 source coverage audit](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md)
adds the catalogue-backed discovery requirements, including minuscules,
lectionaries, commentary manuscripts, versions and quotations. UBS6 is an
available consultation target; the publisher currently schedules NA29 for
2027-02-28. Neither has been imported by this audit. Record the actual edition
consulted rather than calling SBLGNT the latest apparatus.
[UBS6](https://shop.die-bibel.de/Greek-New-Testament-GNT6.-Standardausgabe/5310),
[NA29](https://shop.die-bibel.de/Novum-Testamentum-Graece-NA29./5320).

## Three evidence levels

1. **Edition comparison — now imported.** The pinned official SBLGNT apparatus
   covers all 27 NT books. Its raw entries locate disagreements among edited
   texts, including WH, Treg, RP, and NA labels. This is a reproducible starting
   index, not manuscript-level attestation, the latest critical edition, or an
   exhaustive list of variants.
2. **Manuscript collation — next per case.** Use the INTF/NTVMR catalogue and
   available ECM material to establish exactly which Greek manuscript and hand
   support each reading. Record Gregory–Aland number, holding institution,
   folio, line, date range, corrector, and whether the passage actually survives.
3. **Ancient versions and quotations — supplementary.** Latin, Syriac, Coptic,
   Armenian, Georgian, and other versions help only where their language and
   translation habits distinguish the Greek alternatives. Patristic quotations
   can establish early circulation but may be paraphrased or textually revised.

Modern editions are not independent manuscripts. Repeated copies and related
versions are not separate votes. CBGM/genealogical findings are evidence about
transmission, not an automatic count of manuscripts or proof of an autograph.

## Required distinctions

- Original scribe, immediate correction, later correction, retracing, marginal
  annotation, and modern editorial supply stay separate.
- A version label is not a uniform text. Record the Latin/Syriac/Coptic or
  other version's precise revision, edition and manuscript basis; check its
  own variants and apparatus conventions before inferring Greek. The
  [Psalm 145 Latin follow-up](PSALM_145_SOURCE_COMPARISON_2026-09-05.md) is an
  OT demonstration of this shared safeguard, not an NT attestation.
- A missing leaf is not an omission; a manuscript with no coverage is not
  counted on either side. Being an early papyrus does not imply it preserves
  the passage under discussion.
- Expansion of abbreviated sacred names must remain traceable to the original
  letters; do not erase uncertainty about similar abbreviations.
- Presence/absence, addition, omission, word substitution, word order,
  grammatical form, punctuation, and literary placement are separate questions.
- A whole passage's authenticity and the reading of one word within that
  passage are separate decisions.
- Source-text selection and translation ambiguity are separate. For example,
  Acts 20:28's God/Lord wording is not the same question as how to understand
  the following blood/own construction.
- Written spelling and intended grammatical mood can also separate. The
  [Romans 5:1 comparison](ROMANS_5_1_SOURCE_COMPARISON_2026-09-06.md) records
  omicron/omega interchange and competing interpretations. Keep the attested
  letters, their regular morphological analysis, any proposed spelling variation
  and contextual interpretation distinct. Do not silently normalize a witness
  or let a fluent English rendering certify its earliest Greek spelling.
- Do not select a variant to make the text more orthodox, less supernatural,
  more familiar, or more dramatic. Record arguments on both sides.

## First verified edition-level examples

These are abbreviated comparisons of the pinned SBLGNT apparatus, not new
manuscript readings. English below illustrates the changed phrase only.

| Passage | Greek alternatives | English effect | Current POB |
|---|---|---|---|
| Mark 1:41 | ὀργισθείς / σπλαγχνισθείς | being angry / moved with compassion | Angry; the alternative is footnoted. |
| John 1:18 | μονογενὴς θεός / ὁ μονογενὴς υἱός | the one and only God / the only Son | God; the alternative is footnoted. |
| Jude 5 | Ἰησοῦς / κύριος, with further article/placement differences | Jesus / Lord | Jesus; alternatives are footnoted. |

The source XML is at
[`sources/nt/sblgnt_apparatus/`](../sources/nt/sblgnt_apparatus/), with edition
labels and signs preserved. The [first Mark 1:41 review](NT_PILOT_ADJUDICATION.md)
now compares published manuscript attestations and provisionally prefers
compassion, while retaining anger and its strongest argument. It is not an
image-verified or cross-model-reviewed result, and POB's wording is unchanged.
The other examples remain queued; no result is decided by which printed
edition has more supporters.

The [Romans 5:1 comparison](ROMANS_5_1_SOURCE_COMPARISON_2026-09-06.md) now
adds actually consulted THGNT manuscript/hand reports and opposing scholarly
arguments. It retains indicative meaning provisionally while leaving earliest
spelling unresolved; its qualified note and repaired anchors were applied.
Neither it nor the initial Mark dossier constitutes full NT manuscript coverage.

## A deliberate completeness check: Revelation 13:18

The imported edition apparatus has two entries at Revelation 13:18, but they
address an added verb and forms of the number 666; they do not record the 616
reading. The local POB verse already notes 616 versus 666. This demonstrates
why neither an entry count nor edition-level agreement can substitute for
manuscript collation.

P115 / P.Oxy. 4499 is a real additional manuscript target. The
[Oxford institutional record](https://doi.org/10.25446/oxford.21178999) identifies
it, gives a late-third/early-fourth-century date, and marks the images In
Copyright. It is a metadata/consultation target here: no Oxford image was
vendored. The [CSNTM account of patristic evidence](https://www.csntm.org/2024/06/24/church-fathers-and-the-new-testament-text/)
also discusses Irenaeus's knowledge of both numbers. An early author's work is
not itself a surviving manuscript of that date. No numeral has been newly
deciphered or selected by this import.

## Publication boundary

Treat the current Mark 1:41 assessment as a version-1 working decision until
its dossier has been re-reviewed. A newer model reading the old argument does
not constitute a second blinded review. For fresh image work, model consensus
is a working transcription state; publication still requires a separate source
decision and review evidence. Existing scholarly apparatuses may support
published-text decisions without repeating every image transcription.

For each case, store its witness matrix, exact attestation, alternatives,
dependency cautions, chronological effect, counterargument, and reasoned
outcome. Follow the actual model-review gate; do not claim a second blinded
review happened unless its output exists. Preserve uncertainty and apparatus
notes in reader exports. Canonical changes and deployment remain separate from
this inventory, and ImageGen never becomes source evidence.

## Primary project references

- [Publisher explanation of the SBLGNT apparatus](https://sblgnt.com/about/introduction/apparatus/)
- [Publisher source and CC BY 4.0 license](https://github.com/Faithlife/SBLGNT)
- [INTF's research objective and manuscript resources](https://www.uni-muenster.de/INTF/en/institut/index.html)
