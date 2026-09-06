# First unflagged OT English-fidelity sample

Date: 2026-09-05. Outcome: **two retain/tie judgments, one unresolved
whole-verse judgment, zero established semantic improvements**. No canonical
translation changed. One local readability repair and two reader-note repairs
are proposed below, separately from full-verse approval.

This is one Codex assistant's unblinded first pass against existing pointed
Hebrew, with paragraph context and actual published reference consultations.
It is not a second independent review, publication approval, or a claim that
the whole OT has improved. Current POB, its rationale, and earlier review
metadata were visible. No candidate identity or presentation order was blinded.

## Frozen sample and inputs

The [predeclaration](UNFLAGGED_ENGLISH_SAMPLE_PREDECLARATION_2026-09-05.md)
was written before selection execution and selected-content inspection. It
specifies eligibility, all three book strata, hash ordering, and acceptance
criteria. [The selection receipt](../sources/textual_restoration/samples/unflagged_english_sample.selection.v1.json)
freezes the winners, denominators, exclusions and input hashes. No redraws
occurred. Seed: `POB-unflagged-2026-09-05-v1`.

| Stratum | Eligible | Excluded | Fixed selection | Judgment |
|---|---:|---:|---|---|
| Torah | 4,574 | 1,279 | Numbers 22:19 | Retain/tie |
| Prophets | 6,668 | 2,628 | 2 Samuel 20:6 | Unresolved as a whole verse |
| Writings | 5,181 | 2,934 | Proverbs 24:5 | Retain/tie |

There were 23,264 canonical OT files screened, 16,423 eligible and 6,841
excluded. This stratified sample is one verse per division, not a uniform
three-verse draw over the entire OT. Eligibility rejects textual footnote
signals, source apparatus/markers, unmatched or multiply matched pointed
WLC sequences, and WLC notes. Exclusions are first-failing categories, not
independent counts of all possible signals. Comparison normalization ignores
punctuation, accents and word segmentation, while retaining pointed spelling;
it is not diplomatic identity. “Unflagged” means this local screen, and
“source-stable” means a pinned working base. Neither establishes absence of
variants in a critical apparatus. In fact, review discovered scholarly
alternatives in the randomly selected Samuel and Proverbs passages.

The [review receipt](../sources/textual_restoration/samples/unflagged_english_sample.review.v1.json)
stores exact current Hebrew, POB, notes, candidates, all six rubric dimensions,
counterarguments, differentiated confidence, reopening conditions and hashes
for all 101 context YAMLs. The entire chapters were read in POB and the
embedded Hebrew; selected WLC token morphology was inspected directly.
WLC/OSHB is the local published source, not a fresh manuscript transcription.
Its digital morphology is an aid, not infallible evidence. The prior YAML
labels naming HALOT do not establish a consultation in this pass.

## Numbers 22:19 — retain the English

Context: 22:15–21, with 22:8–14 showing the earlier delegation's overnight
inquiry. Current POB, with its marker omitted here:

> Now please stay here tonight, you also, so that I may know what more Yahweh will say to me.

Close gloss: “And now, remain please here, also you, tonight, and let me know
what Yahweh will add to speak with me.” שְׁבוּ is a plural imperative;
נָא marks the request; גַּם אַתֶּם explicitly includes the new delegation;
וְאֵדְעָה is cohortative; יֹּסֵף ... דַּבֵּר expresses further speaking.
The [NET publisher's notes](https://classic.net.bible.org/passage.php?passage=Num+22:19)
support the stay verb and verbal combination. POB conveys the agency and
content, including repetition, without adding a motive such as bargaining
for a reward or attempting to change God's mind.

Candidate: “Now please stay here tonight, you too, so that I may know what
more Yahweh will say to me.” This is a naturalness option, not a demonstrated
semantic gain. The strongest objection to retaining POB is the interruption
caused by the postposed “you also”; the existing wording nevertheless keeps
its scope explicit. Confidence is high in fidelity to this local base,
moderate in the retain/tie preference. A reader comparison or new contextual
argument could reopen it.

The existing note belongs to the final clause but its marker follows
“tonight.” A separate proposed repair moves it to the final clause and uses
“Or ‘what else Yahweh will say to me.’” This also follows the project's
divine-name policy. The near-synonymous note could instead be removed after
review. Neither repair has been applied.

## 2 Samuel 20:6 — local readability gain; whole verse unresolved

Context: 20:4–7, after Amasa's delay, and the refuge/siege at 20:14–22.
POB preserves David's comparison with Absalom, his emphatic command to
Abishai, the lord/servant hierarchy and the threat of fortified cities.
“Pursue after him” can straightforwardly become “pursue him”: English
*pursue* already expresses the relation conveyed by רדף אחריו. The concrete
full-verse candidate is stored in the receipt and makes only this change.
This is a readability improvement, not restored source content.

Two harder questions prevent a full fidelity finding. The pinned מָצָא is
perfect after פֶּן. [BDB, פֶּן §2](https://biblehub.com/hebrew/6435.htm)
permits apprehension of an event possibly already accomplished, while also
reporting an imperfect emendation; [NET's note](https://classic.net.bible.org/passage.php?passage=2Sa+20:6)
prefers an emendation. Thus “lest he find” may smooth a temporal nuance;
changing the Hebrew to support it would require a separate source decision.
No such change was made.

The final וְהִצִּיל עֵינֵנוּ has the close sense “and snatch away our eye,”
with its exact image uncertain. [BDB, נצל Hiphil §1](https://biblehub.com/hebrew/5337.htm)
records escape/sight, shading and grievous-harm explanations as well as
textual proposals. POB's escape interpretation fits the urgent pursuit and
later fortified refuge; this is the strongest argument for retaining it.
But the current note calls it a settled idiom, and its marker is attached
to Abishai rather than the final phrase. Proposed note: “Hebrew literally
‘and snatch away our eye’; the expression is uncertain. ‘Escape from our
sight’ is a contextual interpretation.” BDB's reports of versions were not
independently collated, and the electronic excerpt was not scan-verified.

Confidence is high in the local readability repair, moderate to low in the
exact final image, and uncertain on the aspect question. The whole-verse
outcome is unresolved, with the existing pointed source provisionally retained.
A focused grammar and apparatus review would reopen it. The readability
repair can be separately considered without claiming the whole verse passed.

## Proverbs 24:5 — retain; the narrower candidate is not clearly better

Context: the 24:5–6 couplet, with 24:3–4 as nearby wisdom/knowledge context.

> A wise man is strong, and a man of knowledge increases strength.

Close gloss: “A wise man [is] in strength, and a man of knowledge strengthens
strength.” The predication and Piel participle are represented. Two subjects
and two parallel assertions remain audible. Verse 6 gives a military
application. The [NET publisher's notes](https://classic.net.bible.org/passage.php?passage=Pro+24:5)
support predicative בַּעוֹז and argue for a warrior sense of גבר.

Candidate: “A wise warrior is strong, and a man of knowledge increases his
strength.” Its strongest advantage is a clearer connection with verse 6 and
a more ordinary possessive in English. Yet “warrior” narrows the subject,
and current “man” accommodates both the generic and military application.
The absent Hebrew possessive suffix does not by itself make English “his”
an illicit addition: that is a contextual rendering choice. This pass finds
no decisive improvement and retains POB, with moderately high confidence in
local-base fidelity and moderate confidence in the preference.

A comparative rendering involving a wise man being better than a strong
one surfaced in a publisher's version note during search. Its ancient
version attributions were not collated here. It is a source-choice lead,
not a superior English rendering demonstrated from the pinned Hebrew.
The canonical file already contains an August 28 audit of this possessive
question. Consequently this draw is frozen for the current first pass but
is not held out from historical project development.

## Verification and limits

Run the read-only selector with
`.venv/bin/python tools/textual_restoration/build_unflagged_english_sample.py`.
Run the four integrity/reproduction checks with
`.venv/bin/python -m unittest discover -s tests -p 'test_unflagged_english_sample.py'`.
All four checks passed on 2026-09-05 (13.092 seconds).
These check the frozen draw against current inputs, pointed-spelling
distinctions, source/context hashes, outcome counts and no-promotion flags;
they cannot test scholarly truth. Historical protocol hashes remain in the
receipt even if shared method documentation later changes.

The corpus SHA256 aggregate is
`d7ba46056931eb8f23844b388ca2adeef5e6c7588e40ad3b6b5e8c6336fb5381`;
Git HEAD was `fb759ec23e9bd778c42d48efa1bb71a795cd552a` in a dirty tree.
The receipt pins every WLC book file, selected verse file, source/English
string, method, schema, doctrine, selector and predeclaration. No text corpus
or dictionary was newly copied. The requested BDB אמץ web page supplied no
entry and is explicitly logged as an unsuccessful lookup. HALOT and modern
critical apparatuses were not consulted. No image reading, reader study,
cross-model acceptance test, export or deployment occurred.

Denominator: three selected verses. Two retain/tie, one unresolved, no
whole-verse changes accepted, no accepted candidate regressions observed;
regressions were not independently measured. This is a small source-based
assessment with useful negative results, not an OT error rate or improvement
percentage. No inference about newly recovered earliest wording follows.
