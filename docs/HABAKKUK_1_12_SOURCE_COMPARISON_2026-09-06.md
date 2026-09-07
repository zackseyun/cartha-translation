# Habakkuk 1:12: preserved text versus scribal-correction tradition

**Application update:** the scoped footnote/rationale correction described at
the end of this report is now applied in the repository. The original research
decision below is retained as preparation history, not current application status.

Checked 2026-09-06. **Retain “We will not die” provisionally; propose a more
precise footnote.** No canonical source, English, or review metadata is changed
by this report. This is a bounded comparison, not exhaustive manuscript collation.

## Question and current record

The [canonical verse](../translation/ot/habakkuk/001/012.yaml) declares WLC,
reads לא נמות, and translates “We will not die.” Its SHA256 at inspection was
`a1ef00ec0ee8c24c8584abec3481f18cd27d613ac7288688f74ec4a4a3116bbe`.
The alternative “You do not die” would require a different Hebrew subject,
conventionally represented by לא תמות, not merely different English style.
The current note's “preserved in some traditions” does not identify the kind
of evidence; its rationales blur reported scribal euphemism and manuscript text.

## Actually consulted evidence

| Source and locator | Observation | Consequence for the disputed subject |
|---|---|---|
| WLC in the current POB source record | לא נמות, first-person plural | Supports the current English as a translation of the declared base; not automatic proof of earliest wording. |
| [Qumran-Digital, 1QpHab, version 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/1QpHab/2026-05-21/index.html), IV.16–17; V.1–5 | IV.17 prints the entire clause in supply brackets, including `[יהוה אלוהי קודשי לוא נמות יהוה]`. V.3's commentary says God will not destroy his people through the nations. | The supplied biblical clause is not preserved-letter evidence for נמות. The commentary provides indirect contextual support for a communal-survival interpretation, not the missing verb's exact spelling. |
| [Qumran-Digital, Mur. 88, version 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/Mur._88/2026-05-21/index.html), XVIII.10–11 | The disputed expression is printed `[לא נ]מות`. | The published preserved suffix מות fits both נמות and תמות. The supplied נ cannot decide “we” against “you.” |
| [Rashi on Habakkuk 1:12, Chabad/Judaica Press presentation](https://www.chabad.org/library/bible_cdo/aid/16197/jewish/Chapter-1.htm), verse 12 commentary | Rashi associates the written communal wording with scribal euphemism; the accompanying English explanation relates the alternative sense to God's not dying. Rashi also explains the received wording as an appeal not to be delivered to death. | This is evidence for an interpretive/scribal-correction tradition, not an inspected Hebrew biblical manuscript preserving תמות or proof that a specific historical alteration occurred. |

The Qumran-Digital entries are published transcriptions, not fresh readings of
photographs. Their parallel-reference rows were distinguished from each
manuscript's own text rows. The release date is not a manuscript date. Short
transcription excerpts above retain the publishers' supply brackets; the
project credits Qumran-Digital and its predecessor transcription sources
under its stated CC BY-SA 4.0 terms. No images were restored or generated.

## Decision and strongest alternative

The divine-subject reading coheres with the preceding address to God's antiquity
and holiness. A reported euphemistic avoidance of speaking about God's death
could explain the communal wording. That is a transmission hypothesis, however,
not an observed correction in these witnesses. Conversely, communal survival
is intelligible alongside the appointment of an instrument of judgment, and
the pesher's commentary shows that such an interpretation is not only modern.
Neither contextual argument uniquely establishes the lost earlier wording.

Retain the declared base provisionally, without claiming that two Desert
manuscripts independently preserve its distinguishing letter or increasing
confidence on that basis. A clearer **proposed, not applied** footnote is:

> Hebrew: “We will not die.” An alternative, “You do not die,” is associated
> with a scribal-correction tradition that treats the received wording as a
> euphemism; it is not established here by preserved manuscript letters.

Any application should also revise the two relevant rationales: the reported
euphemism concerns the received communal wording, not a demonstrated scribal
preference to replace it with “You.” Preserve the historical review record;
its old agreement score does not approve a newly worded note.

## Limits and next discriminating step

Sefaria's Rashi page/API failed in the web tool; Chabad supplied the actual
commentary. A BiblIndex search returned a Greek first-person-plural lead, but
opening the page failed. It is **not counted as a consulted Greek edition or
manuscript**. No complete modern critical apparatus, Greek witness collation,
or history of the scribal-correction lists was inspected in this pass.

For the next source-selection step, consult the passage-specific critical
apparatus and its cited witnesses, testing any reported second-person reading
against actual preservation. Reopen these two Hebrew transcriptions only for
a concrete contrary reading or new material evidence, not another identical
search. The disclosure proposal can receive a separate editorial decision
without pretending those remaining historical questions have been settled.

## Scoped disclosure application — 2026-09-06

The [exact candidate](../sources/textual_restoration/applications/habakkuk1_12_disclosure_candidate.v1.yaml)
uses plainer reader wording than the research proposal: it explains the tradition
as a reverent substitution and limits the preservation claim to the manuscript
passages checked. It also corrects the two relevant rationales, archives the
unchanged former cross-check, and resets live review status. Independent
`habakkuk_disclosure_editor` approved that exact candidate for scoped application
after reading the report, current policy and Habakkuk 1:11–13; this was unblinded.

The [application record](../sources/textual_restoration/applications/habakkuk1_12_disclosure_application.v1.json)
binds before/after bytes, preserves the review decision, and records actual
checks. Hebrew, main English, unrelated decisions and historical revisions are
unchanged. Schema and exact-byte checks passed. The full actual Habakkuk export
(3 chapters, 56 verses) changes only the verse-12 footnote text. The tracked
canonical diff from the recorded checkpoint contains only this verse. A terminal
blank line remains to preserve the exact reviewed candidate; the whitespace
check reports it. No full-corpus historical-verifier pass or deployment is claimed.
