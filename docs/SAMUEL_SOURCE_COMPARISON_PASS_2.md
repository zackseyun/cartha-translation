# Samuel source comparison - pass 2

Checked: 2026-09-04

## Outcome

Two QDR index hits have now received passage-level checks. Neither supplies
secure Hebrew support for the disputed wording. The POB source fields and
English sentences remain unchanged, apart from moving footnote markers to the
phrases they explain. Notes and lexical rationales now disclose the limits.

| Passage | What the controls establish | What the fragment does not establish |
|---|---|---|
| 1 Samuel 14:41 | WLC has the short prayer; the pinned Rahlfs Greek control has a longer prayer | 4Q52 fragment 2 does not securely establish that longer Hebrew prayer: most text is supplied and its passage identification is disputed |
| 2 Samuel 21:19 | WLC Samuel and the Greek control name Goliath; 1 Chronicles 20:5 names Lahmi, his brother | The 1Q7 index hit does not preserve the disputed names or establish their assignment to verse 19 |

These are held comparisons, not adjudications of earliest wording. Keeping the
current WLC-aligned text is an interim publication choice, not a verdict that
WLC must win. The validated ledger now contains nine comparison cases and
16 passage-coverage records; those counts include uncertain coverage, not just
supporting witnesses.

## 1 Samuel 14:41: three distinct questions

The [versioned 4Q52 transcription](https://lexicon.qumran-digital.org/transcriptions/4Q52/2026-05-21/index.html?v=2026-05-21)
assigns fragment 2 to 1 Samuel 14:41-42. Its first line contains the excerpt
`[אם יש בי] או ב֯[יונתן בני העון]`. The brackets mark supplied text;
the dot marks an uncertain letter. The supplied longer line includes Urim,
and the next line supplies Thummim. Neither word is preserved Hebrew ink in
this transcription. We inspected the published transcription, not a newly
acquired image of the manuscript.

The Greek control does attest a longer prayer. Its requests include
`δὸς δήλους` and `δὸς δὴ ὁσιότητα`. Reading those in terms of Urim and Thummim
is an interpretive and source-language reconstruction question, separate from
what the Greek actually prints and from surviving Hebrew characters.

There is also a prior identification question. Sarah Yardney's
[author-hosted 2019 presentation abstract](https://chicago.academia.edu/SarahYardney)
explicitly challenges the assignment of fragment 2 to this passage. Her
[2024 Textus article](https://doi.org/10.1163/2589255X-bja10040),
*Correcting Some Claims of LXX Readings in the Publication of the Samuel
Scrolls from Qumran (DJD XVII)*, addresses misreadings and misidentifications.
The author abstract and publisher metadata were checked; the full 2024 article
and its image arguments were unavailable in this pass. We therefore record
the dispute without claiming to have independently settled it.

The author's [2017 dissertation](https://knowledge.uchicago.edu/records/sn039-sg771),
*Interpretation in the Septuagint of Samuel*, pp. 136-138 (PDF pages 148-150),
represents an earlier assessment. Those complete relevant pages, including the
Hebrew reconstruction and footnotes, were visually inspected. The dissertation
accepts broad support for a longer form, but warns that a reconstruction guided
by Greek cannot independently establish its exact Hebrew wording. It must not
be cited as if it answers the author's later identification challenge.

Current disposition: `coverage-only-disputed-identification`, with coverage
itself marked uncertain. The fragment contributes no positive support to a
preferred source selection until the identification dispute is examined.
This does not refute the longer Greek reading or settle its historical priority.

## 2 Samuel 21:19: a parallel is not a Samuel manuscript

The [versioned 1Q7 transcription](https://lexicon.qumran-digital.org/transcriptions/1Q7/2026-05-21/index.html?v=2026-05-21)
locates fragment 3 at 2 Samuel 21:16-18. Line 5 reads
`[הרפה -- ]ל[ -- ]ל[ -- ]`. Its supplied opening links to verse 18;
QDR assigns the isolated lamed traces to verse 19. This pass does not securely
establish that verse assignment. The disputed opponent, patronymic, and
“brother of” wording are not preserved by these traces.

WLC Samuel and the pinned Greek control name Goliath as Elhanan's opponent.
The local WLC text of 1 Chronicles 20:5 names Lahmi, Goliath's brother, but
Chronicles is a distinct parallel composition. It is relevant to the literary
and textual problem, not another copy of Samuel to add to a witness count.
Neither corruption nor the direction of literary revision has been established
merely by comparing these forms. Importing “brother of” to resolve the narrative
tension would exceed the current evidence review.

Current disposition: `coverage-only-unassigned-traces-after-21-18`. The note
now explains the parallel and why 1Q7 does not decide it. The patronymic note
has been moved from “Philistines” to “Jaare-oregim.”

## Reproducibility and review limits

- Greek controls: OpenScriptorium `lxx-morph` commit
  `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`; exact verse strings are stored in
  the comparison record. This is an edited Greek control, not individual Greek
  codex collation.
- Hebrew controls: local WLC source fields, with current verse-file SHA256
  values in the comparison record; Chronicles has its own pinned parallel
  source entry.
- Institutional identity/access: [IAA 4Q52](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q52-1?locale=en_US)
  and [IAA 1Q7](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/1Q7-1?locale=en_US).
  Exact manuscript image regions remain unacquired and uncollated.
- Earlier model scores and revision timestamps in the verse YAML are historical
  records. They do not certify the newly edited notes. No new blind or
  independent model review is claimed.

The [comparison records](../sources/textual_restoration/comparisons/samuel_controls.v1.json)
and [coverage records](../sources/textual_restoration/coverage/samuel_pilot.v1.json)
preserve these distinctions. Regression tests reject positive support claims
for the two disputed/unassigned entries and keep the Chronicles relationship
separate from Samuel manuscript evidence.

## Consequence for the approach

A transcription webpage's recent release date does not prove that it
incorporates every later correction to the edition it represents. Check
identification disputes, errata, and changes in an author's assessment before
using decisive readings. Hold unresolved evidence out of positive support;
do not replace one unexamined authority with another.

Next work: obtain and examine the full 2024 discussion and exact institutional
images; collate the relevant Greek manuscript traditions; continue the
1 Samuel 1:24 and 10:27-11:1 candidates. No generated image has been used as
manuscript evidence, and no critical Hebrew or English main-text selection is
promoted by this pass.
