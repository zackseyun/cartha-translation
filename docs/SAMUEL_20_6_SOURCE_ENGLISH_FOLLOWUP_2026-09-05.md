# 2 Samuel 20:6: source and English follow-up

2026-09-05. **Whole verse remains unresolved; no canonical change.** Direct
Greek and Syriac edition checks now replace two previously unverified version
reports. Grammar review strengthens the objection to treating the Hebrew
perfect as straightforwardly prospective. It does not establish a replacement
Hebrew text. This is follow-up work on a known difficult case, not another
random sample or a fresh blinded assessment.

## Fixed scope and evidence

The [bound record](../sources/textual_restoration/comparisons/samuel_20_6_source_english_followup.v1.json)
preserves the entire pointed source, current English and notes, all 26 chapter
context bindings, and ten frozen input hashes. The unchanged canonical YAML
SHA256 is
`fc699b63aa3751fd07d40931a286af36cdda3aae944de4cdd231f01249c4c504`;
its source-string SHA256 is
`caf989db4d4bcc1f100ea911f364b5a70f9266a3569699fd63a1ba633ad98dd6`.
No accents, vowels, segmentation marks or punctuation have been normalized
away in those bindings. The frozen sample report and receipts remain intact.

The original meaning/ambiguity/literary-function/naturalness rubric is retained.
Chapter 20 was reread: Amasa's delay and David's commission in verses 4–7
explain the urgency, while the fortified refuge and siege in verses 14–22
provide its narrative consequence. That context supports a practical escape
interpretation but cannot prove a particular source spelling.

## Perfect after *pen*: stronger grounds for abstention

The pinned מָ֥צָא is Qal perfect, not the imperfect יִמְצָא. BDB's
perfect-apprehension category allows a dreaded result construed as possibly
already accomplished. Its local parenthesis nevertheless prefers an
imperfect here because of the following verb. The earlier sample's caution
was warranted, but the positive objection deserved greater emphasis.
Only BDB's scholarly entry was used, not the host's topical material.
[BDB, פֶּן §2](https://biblehub.com/hebrew/6435.htm)

GKC §107q's note distinguishes 2 Kings 2:16 from this verse and recommends
Driver's imperfect emendation for Samuel because a consecutive perfect
follows. §152w refers back to that discussion. It would misstate GKC to cite
it as directly endorsing retained מָצָא here. This is a grammatical argument
for changing letters, not evidence that the pinned text already contains them.
[GKC digital PDF](https://tmcdaniel.palmerseminary.edu/GeseniusGrammar.pdf)

The PDF skill prompted rendered-page inspection. The local reflow's relevant
pages are 291 (§107q, note 3) and 436–437 (§152w and its remark), one-based.
Page 450 was also inspected but belongs to the conditional-sentence discussion,
not §152w. Some unrelated Hebrew glyphs are defective; the decisive note is
legible. This is a digital reflow, not a photograph of the original edition.

Against the same retained source, “lest he find” is natural apprehensive
English but suppresses any anterior nuance. “For fear he has already found”
makes that nuance explicit but may overstate a disputed reading; “before he
finds” narrows it still further to prospective prevention. None is established
as the better whole-verse replacement. The strongest retention argument is
that a feared completed scenario can motivate present urgency without a rigid
English-tense equivalent. The following consecutive remains the strongest
counterargument. Confidence is high in the morphology and reported grammar,
not in historical priority.

## The eye expression: observed versions, distinct hypotheses

The selected text of Rahlfs–Hanhart 2006 has a finding clause with an aorist
subjunctive, then **σκιάσει**, future indicative: a shading action with plural
eyes. The consulted publisher page also identifies the edition. This confirms
the Greek wording, not all Greek witnesses or an exact Hebrew retroversion.
Its addressee is Abessa, corresponding to the pinned Abishai.
[Rahlfs–Hanhart, REGNORUM II 20:6](https://www.die-bibel.de/en/bible/LXX,VUL/2SA.20)

CAL's Syriac chapter control has an additional taking-a-stand clause and an
eye-excavation action. The injury token is tagged G, root ḥṭṭ; the contextual
imperfect-third-masculine-singular analysis is ours, not a complete parse
supplied by CAL. Its addressee is Joab. These were read from the actual chapter,
token and metadata pages, not inferred from an English Peshitta translation.
[CAL 62009, 20:6](https://cal.huc.edu/get_a_chapter.php?cset=H&file=62009&sub=20),
[injury token](https://cal.huc.edu/getlex.php?coord=620092006&word=27&hasvariant=0)

CAL identifies its text as Leiden-derived with corrections from 7a1. The
source-information popup incorrectly labels the chapter/verse, so alignment
is established by the originating chapter, verse label and matching content.
The edition is not a direct reading of one manuscript. Displayed variants
earlier in the verse do not include another final phrase; that is not proof
of manuscript unanimity. The full Leiden apparatus remains uncollated.
[CAL source information](https://cal.huc.edu/get_file_info.php?coord=6200920)

Driver's actual 1913 scan, printed pages 341–342 (PDF 463–464), was read in
full. It distinguishes eye removal, metaphorical elusion, a repointed shadow
derivation, and a Lucian-based escape-from-us proposal. Its literal gloss uses
singular eye, unlike the current POB lexical discussion's plural wording.
The Lucian wording remains a report by Driver/BDB here: no direct Lucian
edition or manuscript collation was performed.
[Driver, second edition](https://biblicalstudies.gospelstudies.org.uk/pdf/e-books/driver_s-r/samuel_driver.pdf)

For the retained Hiphil of נצל, the eye is the object, not an explicit
“from our eyes” phrase. BDB records competing explanations rather than a
settled idiom. [BDB, נצל Hiphil §1](https://biblehub.com/hebrew/5337.htm)

The distinction matters: metaphorical escape and serious injury can be
interpretations of the same removal expression. A new shadow derivation
requires a separate source-interpretation/repointing decision; Niphal escape
with “from us” is a different Hebrew proposal. Neither the Greek nor Syriac
form proves the exact Hebrew letters behind it. Joab versus Abishai is a
genuine addressee difference, not permissible English clarification; possible
adjustment to the surrounding Joab-led action is its strongest counterreading.

## Bounded English findings

- “Pursue after him” → “pursue him” remains a small naturalness proposal,
  not recovered source meaning. The existing expression is understandable.
- Move the note's anchor from Abishai to the final phrase. A research-only
  candidate is: “Hebrew, ‘and take away our eye’; the expression is uncertain.
  ‘Escape from our sight’ is one interpretation.” This corrects disclosure
  and anchoring without selecting an alternative Hebrew text.
- Keep the whole verse unresolved. The competing aspect and eye analyses
  have not been settled merely because two version reports are now verified.

The strongest objection to the cautious note is reader burden: the present
rendering has a coherent military sense. That does not justify an anchor at
the wrong name or presenting the difficult expression as certain. Neither
proposal has been applied, exported as a new candidate, or publication-approved.

## Reproduction and limits

```sh
.venv/bin/python tools/textual_restoration/check_samuel_20_6_followup.py
.venv/bin/python tools/textual_restoration/check_samuel_20_6_followup.py --check-external-pdfs
.venv/bin/python -m unittest discover -s tests -p 'test_samuel_20_6_followup.py'
```

The checker and ten tests passed: exact source/English, ten frozen inputs,
26 context files, scope flags, evidence references and versional boundaries
are checked. Injected drift in every frozen input and every context file is
rejected. External verification checked both downloaded PDF hashes. These are
integrity tests, not tests proving Hebrew meaning. PDF paths/hashes and the
brief consultation excerpts are in the record; no dictionary or version
corpus was copied into the repository. Online page observations are not
represented as frozen full-HTML snapshots.

No HALOT, full modern apparatus, DSS manuscript, Greek genealogy or Syriac
dependency collation occurred. BDB, Driver and GKC are related older
scholarship, not independent ancient votes. Provisional source retention
does not claim earliest wording. Further apparatus/version-practice work and
a separately bound candidate review are required before any application.

## Actual independent review

The separate agent's [exact judgment](../sources/textual_restoration/comparisons/samuel_20_6_source_english_followup.judgment.v1.json)
records a bounded PASS for consulted-source fidelity, separation of same-source
interpretation from emendation, frozen-input/context integrity, and honest
coverage limits. The judge independently ran all ten tests and the two external
PDF hash checks, and checked the decisive BDB, GKC, Driver, Greek and CAL
controls. Its actual visual checks did not include the later GKC pages 436–437;
the judgment preserves that limit. No concrete repair finding was returned.

The judgment binds the unchanged research record, checker, tests and the
pre-verdict report bytes. Only this report's review-status paragraph was then
replaced with the present outcome section. The research record's requested
review status remains its frozen pre-review state; the separate judgment is
the actual review outcome. Earliest source and best whole-verse reading remain
INCONCLUSIVE. Canonical application, whole-verse reapproval and publication
approval are all explicitly false.
