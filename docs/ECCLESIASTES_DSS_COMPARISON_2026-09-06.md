# Ecclesiastes: two-record DSS comparison

2026-09-06. Published-reading screen, not image restoration or all-source collation.
Previous goal turn was progress: Lamentations 1:7's disclosure was applied and
pushed. This pass broadens actual comparison coverage without reopening that case.

## Scope and reproducibility

Root read all 36 published 4Q109 line records and compared all 26 QDR-tagged
canonical verse contexts. One bounded agent read all eight published 4Q110 lines,
all eleven older QDR lines and corresponding canonical sources. This is divided
work, not independent replication. Total: **44 published line records**, versus
47 QDR records with 564 tagged word records and 36 distinct verse tags. Tags
include supply and uncertain assignments, not 36 preserved verses.

| Record | QDR units and line IDs | Published coverage |
|---|---|---|
| 4Q109 | f1i:1–8; f2:1; f1ii+3_6i:1–7,11–21; f1iii+6ii_7:1–5,17–20 | 36 records; 385 QDR tagged words |
| 4Q110 | f1_3:1–11 | 8 records; 179 QDR tagged words; mapping below |

References use Hebrew/current POB numbering; chapter 5 differs from many English
editions. The existing [book map](../sources/textual_restoration/discovery/hebrew_bible_book_map.v1.json)
remains a discovery index, not preserved-text evidence. The earlier
[wisdom-book audit](WISDOM_BOOK_SOURCE_AUDIT_2026-08-28.md) assessed English against
WLC; it does not certify a completed ancient-witness comparison.

Input SHA256 pins:

- QDR `qdr.1.1.biblical.json`: `3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`.
- Local `pob-lxx-morph/db/seeds/lxx_morph/ecclesiastes.json`: `0ec029295874df2ef0d6b6742abf8cb62dc045136187eed19a73e6d9a3a1da24`.
- All 222 canonical Ecclesiastes YAML records: manifest `fd2097c18575f3fd7f6afcee9abeb933b57872e57e48ec46dd554de9225faa06`.

Manifest rule: SHA256 of UTF-8 compact, sorted-key JSON mapping repository-relative
YAML paths to file SHA256. These pins identify inspected inputs, not manuscript dates.

## 4Q109: consequential and controlled differences

From the [versioned published transcription](https://lexicon.qumran-digital.org/transcriptions/4Q109/2026-05-21/index.html?v=2026-05-21):

| Verse; unit/line | Published target against WLC; disposition |
|---|---|
| 5:14; f1i:1 | כיא / כאשר: conjunction interpretation open. |
| 6:3–4; f1ii+3_6i:1–2 | Reordered stillborn comparison; raised corrections and deleted שמו; corrected הלך / ילך. Preserve editorial stages. |
| 6:6; same:3 | ואם לוא / ואלו: conditional/spelling analysis needed; do not infer negation mechanically. |
| 6:8; same:6–7 | כמה / כי מה; following traces unresolved. |
| 7:2; same:15–16 | [ש]מחה / משתה; כול סוף / סוף כל. Noun preference below; remainder not silently normalized. |
| 7:4–5; same:17–19 | בית / בבית; גערות / גערת; corrected מלשמוע / מאיש שמע. Crossed-out material not recovered. |
| 7:7; f1iii+6ii_7:2 | ויעוה֯ / ויאבד: verb candidate, uncertain final letter. |
| 7:19; same:18–19 | תעזר / תעז; following complement partly supplied/uncertain. |

Other readable lines mostly agree or show spelling/conjunction differences.
The supplied 6:12 line 11 and the trace tagged 7:18 cannot establish omissions or
readings. This is a comparison of published readings, not newly observed ink.

## 4Q110: do not promote older contextual reconstruction

The [published transcription](https://lexicon.qumran-digital.org/transcriptions/4Q110/2026-05-21/index.html?v=2026-05-21)
has eight records labeled fragment 1–2. By surviving text, published lines 1–8
correspond to QDR f1_3 lines 4–11. QDR lines 1–3 have no counterpart on this
page; this does not prove that a physical fragment was lost or reidentified.

Published 1–6 cover surviving runs at 1:10–14, with ordinary spelling differences
and אשר נעשו against שנעשו, equivalent relative constructions. Line 7 has only
גבו֯ between gaps: QDR's supplied 1:15–16 context does not establish a readable
“mighty” variant. Line 8 is an unidentified trace, not the lamed and 1:16 context
in QDR. Neither final line has a secure published verse assignment. No source
change follows; retain upstream identities separately pending editorial explanation.

## Local Greek controls and one source decision

Root read selected Greek surfaces at 5:14; 6:3–4,6,8; 7:2,4–5,7,19, ignoring
generated morphology/confidence. These are selected-text controls, not individual
manuscript votes or a completed critical apparatus. At 7:2 the control has πότου,
whereas 7:4 has εὐφροσύνης: it preserves the feasting/joy distinction. At 7:5 it
retains a man hearing, and at 7:7 its verb expresses destruction, although its
following phrase differs from POB. At 7:19 its helping verb fits the scroll's
root more directly but can interpret the WLC's strengthening sense; no exact
Hebrew spelling follows from that semantic fit. At 6:6 it presents a condition
without negating living; that does not resolve the scroll's orthography.

**7:2 noun decision:** prefer WLC משתה provisionally, with moderate confidence
in this limited preference. The scroll's joy-word could assimilate to 7:4's
nearby בית שמחה. The Greek control preserves the two distinct nouns. Strongest
objection: feasting could instead sharpen a more general joy-word, or the Greek
could already depend on that sharpened form. Neither the date nor the selected
Greek text proves direction. Do not turn this noun judgment into approval of
every clause in 7:2 or every reading of either manuscript.

Full-verse source-distinction check:

```json
{"source_distinction_checks": [{
  "candidate_id": "eccl7_2-feasting-versus-joy",
  "disposition": "retain_after_comparison",
  "source_evidence": "WLC בית משתה (7:2), בית שמחה (7:4); published 4Q109 [בית ש]מחה at 7:2. The supplied prefix/context must remain distinguished from preserved מחה.",
  "proposed_text": "It is better to go to a house of mourning than to go to a house of feasting[a], because that is the end of every person, and the living should take it to heart.",
  "alternative_text": "It is better to go to a house of mourning than to go to a house of joy[a], because that is the end of every person, and the living should take it to heart.",
  "rationale": "Retain the event-specific feasting against the broader emotional joy, preserving the source contrast with 7:4. This alternative tests only the noun; it is not a full translation of the scroll's differently ordered clause. The preexisting note a concerns every person and is misplaced; this pass does not repair it or certify complete verse quality."
}]}
```

## Stop, remaining candidates and limits

No canonical source, English, notes or historical approvals changed. The 7:2
noun question is parked unless apparatus evidence or a locus-specific transmission
argument discriminates the directions; another copy of the same text is insufficient.
The other candidates remain screened, not adjudicated. In particular, contextual
similarity to corruption language in Exodus 23:8 and Deuteronomy 16:19 does not
by itself select Ecclesiastes 7:7's verb: neither parallel has that exact verb.
The surviving correction at 7:5 needs edition/hand analysis before historical
claims; 7:19 needs versional discrimination; 6:6 needs conditional-orthography analysis.

A Brill THB preview acquisition returned HTTP 403; no preview body was read.
Search snippets were not used as scholarly verdicts. No new PDF/image reading,
validator, judge loop, canonical application or deployment occurred. This pass
does not establish exhaustive Ecclesiastes, OT or NT source coverage.

Verification passed: both source pins; QDR 36+11 records, 385+179 tagged words
and 36 unique tags; all 222 canonical file hashes unchanged; exact current
full-verse comparison text; selected Greek noun anchors; local report links;
`git diff --check`. Published 36+8 line coverage was read directly, not inferred
from those QDR counts. No reader export was needed for this documentation-only pass.
