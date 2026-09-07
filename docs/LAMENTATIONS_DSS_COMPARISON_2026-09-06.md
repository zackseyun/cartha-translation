# Lamentations: bounded DSS comparison

Date: 2026-09-06. Status: published-reading screen; historical priority open.

## Result and scope

The four Lamentations records in the pinned QDR snapshot contain consequential
differences, including linked changes in voice, wording and order. Preserve
these as comparison candidates, not isolated words to insert into POB.
No canonical Hebrew, English or notes changed. This is not a complete census
of discovered witnesses or a completed Lamentations critical text.

The [receipt](../sources/textual_restoration/comparisons/lamentations_dss_screen.v1.json)
pins inputs, all physical-line identifiers and tagged references. Root read
4Q111's 33 published line records; one bounded agent read the other 70 against
canonical `source.text`. This was divided labor, not independent replication.
The 103 records contain 939 tagged word records and 62 distinct verse tags;
tags include supply, punctuation and uncertain assignments, not 62 preserved
verses. The 154 canonical Lamentations records remain unchanged.

## Published readings worth pursuing

[4Q111, versioned transcription](https://lexicon.qumran-digital.org/transcriptions/4Q111/2026-05-21/index.html?v=2026-05-21):

| Location | Observation / comparison target |
|---|---|
| Unit 2:1 / 1:6 | Doubled לוא and מצא ומרעה; do not silently regularize. |
| 2:2–5 / 1:7 | זכו֯רה יהוה and מכאובנו change the remembered subject/object into an appeal about our pains; compare משבריה. |
| 2:6–9 / 1:8–9 | לנוד, הזילו and פלאות warrant lexical/grammatical review. |
| 3:1 / 1:10–11 | Continuous published text joins לא יבואו to מחמדיה באוכל; substantial WLC material between them is absent, not merely hidden by a supplied gap. |
| 3:2–6 / 1:11–15 | זולל, הוגירני, ויורידני, חשיבני, שומם, נקשרה and אבידי raise linked grammatical/lexical questions. No new confident gloss for damaged or difficult readings. |
| 3:7–10 / 1:15–18 | Order is 15→17→16→18; 17 includes מכול אוהביה צדיק אתה יהוה, with further voice/name differences. Preserve the sequence in comparison. |

Unit 1 is heavily supplied; fragment 4 gives sparse 2:5 evidence. Neither
establishes complete agreement with WLC.

[5Q6, versioned transcription](https://lexicon.qumran-digital.org/transcriptions/5Q6/2026-05-21/index.html?v=2026-05-21):
4:18 has היום against ימינו; 5:1 has חרפותי[נו] against חרפתנו.
At 5:3, לא֯ ב֯נ֯ות ואלמנות differs substantially from כאלמנות but remains
uncertain in reading and interpretation. At 4:14–15, בל, damaged יבג[ ],
and טמ֯א֯ו need qualified review, not automatic lexical replacement.
The 5:1 הביטה matches the qere, not a novel reading. Other leads are mostly
spelling/phonetic differences. Twenty-two lines in fragments 2–12 remain
unassigned; blank or supplied lines are not omissions.

[3Q3](https://lexicon.qumran-digital.org/transcriptions/3Q3/2026-05-21/index.html?v=2026-05-21)
produced no secure consequential variant; fragment 2's nested bracket syntax
prevents reliable preservation claims.
[5Q7](https://lexicon.qumran-digital.org/transcriptions/5Q7/2026-05-21/index.html?v=2026-05-21)
does not independently oppose 5Q6 at 4:18: its ימינו is supplied.
Its final trace has no defensible verse assignment despite a QDR 4:21 tag.
These are published-transcription observations, not newly read manuscript ink.

## Greek controls and a concrete alignment limitation

Only `words[].surface` and reference labels from the pinned local Greek file
were used, not generated morphology or confidence. This is a selected-text
control, not a collation of Greek manuscripts or a claim of versional unanimity.

At 1:7 the control has Jerusalem remembering her desired things, rather than
4Q111's appeal concerning our pains. At 4:18 it has “our days”; at 5:1 singular
“our reproach”; at 5:3 “as widows.” These provide comparisons, not decisive
Hebrew retroversions: a translation can neutralize a number distinction or
interpret its source. Greek manuscript variation remains unexamined here.

The local row labeled 1:15 ends with ἐπὶ τούτοις ἐγὼ κλαίω, corresponding to
the opening of Hebrew 1:16. Read adjacent rows together: the phrase is not
missing. Continuous Greek content puts weeping before Zion's outstretched
hands, unlike the inspected 4Q111 order. Whether the row boundary comes from
edition numbering or upstream ingestion remains unverified; no upstream edit
was made. Separately, the initial reference-filtered character comparison
missed 4Q111's cross-verse 1:10–11 junction. Such diffs locate candidates;
they cannot establish completeness or omissions. No new engine is needed to
apply this already-required contextual check.

## Decision, competing explanations and stopping rule

Keep the current POB text provisionally, not because WLC has won the historical
argument. At issue are an earlier alternative form, subsequent literary
reshaping, and local copying changes; the screen does not discriminate them.
Choosing attractive words independently could manufacture an unsupported
composite. The next consequential decision must compare the linked form and
then assess source selection separately from English rendering.

The [Kotzé 2011 article landing page](https://www.scielo.org.za/scielo.php?pid=S1010-99192011000300003&script=sci_arttext)
provided its abstract and bibliography only. Its
[PDF body](https://www.scielo.org.za/pdf/ote/v24n3/03.pdf) and the cited DJD XVI
4QLam edition, pages 229–237, were identified but **not read** in this pass.
Do not attribute detailed arguments to them. A targeted consultation addressing
1:7's competing textual histories is justified; another whole-book screen,
image-calibration cycle or consensus loop is not. For 5Q6, reopen with relevant
critical-apparatus evidence or a decisive reading clarification, not another
copy of the same transcription.

This pass preserves completed research after the efficiency audit. No source
acquisition was repeated, no new validator was built, and no deployment occurred.
