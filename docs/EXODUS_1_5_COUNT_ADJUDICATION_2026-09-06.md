# Exodus 1:5: the number and the Joseph clause

Checked 2026-09-06 under [method 2.0](TEXTUAL_ADJUDICATION_METHOD.md).

## Outcome

**Numeral priority unresolved.** Seventy-five is a serious early Hebrew
candidate, not merely a Greek or Christian alteration. Nevertheless, the
present comparison does not distinguish an early genealogical expansion from
a later reduction strongly enough to promote either as the recovered earlier
reading. Keep seventy in the declared POB base provisionally. This is not an
argument from Masoretic authority, a rejection of seventy-five, or a claim
that a new image transcription is universally required before selection.

**Joseph clause separately unresolved.** Retain its current following position
provisionally. Seventy-five with following Joseph wording is not inherently
an unattested splice, but that does not establish every word of a complete
eclectic sentence or the clause's original position.

Baseline Git: `6fc394300eb778d6dabea711aeb1f56f1ecf7a69`.
[Canonical verse](../translation/ot/exodus/001/005.yaml) SHA256:
`69ed94054c88020229b565f8b6fab6baef2c047d7a85067be6643b911efd7fb4`.
No source, English, note, review flag or other canonical metadata is changed.
The older [comparison dataset](../sources/textual_restoration/comparisons/pentateuch_controls.v1.json)
remains its historical screening checkpoint; this report adds adjudication.

## Hebrew preservation and local literary context

Fresh consultation of the versioned published transcriptions, including the
surrounding physical lines rather than reference-filtered fragments:

| Witness/control | Numeral | Joseph relationship |
|---|---|---|
| WLC and pinned Samaritan control | Seventy | Location clause follows |
| 4Q1, frgs. 17–18, line 2 | Seventy supplied; “and five” preserved | Joseph follows, with an uncertainty mark; location wording supplied |
| 4Q13, Qumran-Digital frg. 1, lines 4–5 | Seventy-five preserved | Joseph occurs in the brothers list; count passes directly to death |
| 4Q11, existing published control | Entire numeral supplied | Following location clause partly preserved |

The decisive excerpts are `[יצאי ירך יעקב שבעים] וחמש נפש ויוס֯ף[ היה במצרים`
in [4Q1, version 2024-07-30](https://lexicon.qumran-digital.org/transcriptions/4Q1/2024-07-30/index.html),
and `חמש ושבעים נפש וימת[ יוסף]` in
[4Q13, version 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/4Q13/2026-05-21/index.html?v=2026-05-21).
The latter's line 4 includes Joseph after Zebulun. Its supplied earlier clause
must not become preserved evidence for every surrounding word. Reuse the
[pass-2 qualification](PENTATEUCH_SOURCE_COMPARISON_PASS_2.md#exodus-15)
for 4Q11; no new reading of that manuscript is claimed here.

Tov calls the 4Q13 object fragment 2; Qumran-Digital labels its unit fragment 1.
Record these as source-local locators, not a resolved physical-number crosswalk
or two witnesses. This provenance issue does not erase the published numeral.

## Greek and genealogy controls actually inspected

Brooke–McLean *Exodus and Leviticus* (1909), printed pp. 155–156
(PDF 13–14): B-based main text has seventy-five and the Joseph clause before
the count. The v5 apparatus also reports the clause after the count in a
Greek group. This is not uniform Greek clause order. No complete witness list
or new physical-codex reading is claimed.
[PDF](https://tmcdaniel.palmerseminary.edu/Brooke%26McLean/LXX_Brooke%26McLean_1-2.pdf),
SHA256 `8d63914f75fd1e4539fb953fa8ec50223be6b41e91509ea37c401e03d32d16c9`.

Brooke–McLean *Genesis* (1906), printed pp. 137–139 (PDF 153–155):
the Genesis 46:20–27 text uses A, not B, at the target. It includes the
additional Joseph descendants and multigenerational Benjamin list; Rachel's
subtotal is eighteen, followed by sixty-six, nine Joseph offspring, and
seventy-five total. The apparatus reports other numerical forms. Do not
silently change nine to seven to manufacture a flawless count.
[PDF](https://tmcdaniel.palmerseminary.edu/Brooke%26McLean/LXX_Brooke%26McLean_1-1.pdf),
SHA256 `c5031defb2e2f8de3e4db1f47244f0565ea001a529e3f924680e4f3c7ead1519`.
Complete relevant pages were visually inspected. General conventions are
reused from the [preceding consultation](EXODUS_12_40_SOURCE_ADJUDICATION_2026-09-06.md).

The local Rahlfs surface-text control corroborates these principal Genesis
values and Exodus's seventy-five; **its Deuteronomy 10:22 still has seventy**.
Thus “the Greek tradition consistently harmonizes everything to seventy-five”
is not an adequate explanation. This is edition evidence, not a proof of
Greek manuscript unanimity or independent ancestry. Source-local labels are
`Gen 46:20–27`, `Exod 1:5`, and `Deut 10:22`.

Inputs reused at `/private/tmp/pob-lxx-morph/db/seeds/lxx_morph/`, SHA256:

- `genesis.json`: `5fe6e515f018585edb59bd3aa0a9a81f22cd6a87a4d10d02723423ea9329f93c`
- `exodus.json`: `c5a775d14720b26c70dfcdb72c3c473ac21c33894714ebd85d03f132ebf45267`
- `deuteronomy.json`: `4f3f3251a5182071d3482753ba9c7208d527705dee418846499134cd19aa46dc`

Local Hebrew Genesis 46:20–27, Numbers 26:29,35–36,46 and Deuteronomy 10:22
were inspected as contextual controls. The agent also checked the pinned
Samaritan data through the existing hash-checking loader. Acts 7:14's seventy-five
is reception evidence, not another Hebrew Exodus manuscript; the local SBLGNT
apparatus is edition-comparison evidence, not a census of manuscript variants.

## Competing histories tested

[Kislev (2015)](https://www.thetorah.com/article/jacobs-descendants-who-go-to-egypt-mt-versus-lxx)
argues that an older multigenerational list was shortened and flattened to fit
Genesis chronology. His Serah and concubine observations support testing list
relationships beyond arithmetic. They do not prove that every shared feature
was transmitted in one direction. Nor must a later contributor always avoid
chronological tension; supplementary genealogy could introduce it.

[Tov (2023)](https://www.thetorah.com/article/how-many-descendants-of-jacob-came-to-egypt-genesis-46-27-exodus-1-5)
endorses Kislev and proposes assimilation to Deuteronomy's seventy. These are
related arguments, not additional ancient witnesses. His nine-to-seven
explanation is an editorial diagnosis, not the printed reading inspected above.

[Longacre (2017)](https://www.logos.com/grow/two-significant-uses-of-the-dead-sea-scrolls/)
instead favors seventy, explaining seventy-five through an expanded Genesis
list related to Numbers 26. He also proposes a marginal origin for the Joseph
clause. Distinct numeral orders and clause locations make these possibilities
worth testing but do not establish independent additions or original omission.
All three authors' relevant arguments were actually read, not inferred from
search snippets. Their cited underlying monographs/DJD discussions were not
read at that checkpoint; the bounded follow-up below supersedes the DJD gap.

The independent agent `/root/exodus_count_context` audited local context and
then read these three essays. It relied on root's printed-apparatus observations;
it did not claim a second image inspection. Root considered a low-confidence
seventy-five preference; the agent favored unresolved priority. The final hold
reflects the substantive objection: both genealogical histories remain plausible
before our surviving copies. It is not a vote or a judge-until-agreement result.

Chronological sensitivity: early direct Hebrew favors taking seventy-five very
seriously and gives a slight inclination when other evidence is comparable.
Here relationships and direction of change remain too uncertain to treat the
comparison as a settled tie. Without that chronological tilt the result is
still unresolved; with it, no promotion is justified in this pass.

## Original next step and verification (superseded below)

Consult the actual opposing DJD XII discussions identified by Tov: Davila p. 19
and Cross p. 85, with their transcription/material context. Test whether they
supply additional grounds for genealogical expansion or reconstruction limits,
rather than collecting another general endorsement of a number. The exact
4Q13 physical-fragment numbering and 4Q1/4Q11 restoration arguments also remain
open. No failed DJD acquisition is claimed: those pages were not obtained here.

IAA manuscript-page requests returned navigation/title shells without usable
dating details. No precise dates or fresh photographs follow from those calls.
One PDF locator scan exceeded the document length and raised IndexError;
bounded indices then located the actual Genesis pages. The initial Greek
`Ex 1:5` lookup had no hit; using the observed `Exod 1:5` label succeeded.
Neither failed lookup is negative manuscript evidence.

Baseline hash, local document links and diff checks establish documentation
integrity and unchanged canonical state only. No image calibration, ImageGen,
new infrastructure, canonical-note rewrite or deployment was performed. The
next source-selection step is the named publication comparison, not repeating
this completed general-argument pass. The broader OT/NT goal remains open.

## DJD follow-up and stopping decision — 2026-09-06

**Park this case: priority remains unresolved.** The named DJD arguments have
now been consulted; their previous unread status is no longer a reason to
continue acquisition. No source, English or note change follows.

### Sources actually consulted

[DJD XII public text rendering](https://www.scribd.com/document/929201148/Qumran-Cave-4-VII-Genesis-to-Numbers-Discoveries-in-the-Eugene-Ulrich-Frank-Moore-Cross-James-R-Davila-Jastram-WeLib-org),
Davila pp. 18–19 and Cross pp. 83–86: both favor seventy, opposing the
seventy-five proposal rather than each other. Davila connects expansion with
genealogy and different numeral orders. Cross's recalculation history is
conditional; his wider Greek-affiliation argument does not establish direction.
He distinguishes preserved variants from spatial reconstructions: the shortened
count introduction and omission of Joseph before it depend on reconstruction.
Davila reports lost fragment 18 and older photograph PAM 43.010; this does not
identify the numeral-bearing leather by itself. Cross's target is headed
fragment 1, followed by fragment 2 at Exodus 1:16–21. These remain source-local
locators, not a resolved physical crosswalk. This was English OCR consultation,
not DJD page-image inspection; corrupted Hebrew and sigla support no new glyph claims.

[Longacre's institutional doctoral thesis](https://etheses.bham.ac.uk/5780/1/Longacre15PhD.pdf),
printed pp. 107–110, 183–184, 245 (PDF 122–125, 198–199, 260), was visually
inspected, not read in full. SHA256:
`5249bc05ff4f622a469dad4f6d2a71e96776af51936447d1e1cb55dd0b0a5dff`.
Its revised column estimates for 4Q1 and 4Q13 are broader material arguments,
not new surviving letters at the numeral. It assigns 4Q11 fragment 39 to
Exodus 1:1–5 more firmly than DJD; that still does not make a supplied count
preserved. Its discussion reports disputed classifications of 4Q13, so Cross's
Greek affiliation is not a settled family assignment. Table 4.15 visibly gives
4Q1 as `[שבעים] וחמש`; extraction dropped the five, demonstrating why the
table's text and supply marks needed visual checking. Page 245's footnote
identifies a Greek/Hebrew numeral-order control, tested separately below.
The PDF remains private research material, not redistributed in Git.

### New local control and its limits

The already-pinned Rahlfs surface-text file (Exodus hash above) has
`ἑβδομήκοντα πέντε` in both `Exod 39:2` and `Exod 39:5`.
The corresponding WLC source fields in
[Exodus 38:25](../translation/ot/exodus/038/025.yaml) and
[38:28](../translation/ot/exodus/038/028.yaml) instead put five before seventy.
These are aligned silver-accounting clauses, not matching modern verse numbers.
Only surface text was used, not generated morphological confidence labels.

Inference: Greek order cannot mechanically establish the Hebrew Vorlage's
order. This weakens an inference from Greek agreement to a particular Hebrew
numeral sequence. It does not explain away the different orders in the direct
Hebrew witnesses or decide whether seventy or seventy-five came first. These
are edition controls, not newly inspected manuscript hands.

One independent agent, `/root/djd_exodus_arguments`, checked the English DJD
arguments and likewise retained unresolved priority. It did not inspect DJD
images or independently read the thesis. No repeated review or consensus vote.

### Reopening condition

Reopen only for an identified source that can discriminate the remaining
histories or materially test a locus-specific reconstruction: for example,
preserved wording or a documented spatial constraint excluding an alternative.
A newly accessible page, another scholarly preference, unresolved fragment
numbering alone, or another model opinion is insufficient without that link.
Broader column-height revisions alone do not invalidate local line-width claims.
Until then, retain seventy and the following Joseph clause provisionally and
move research to other source-coverage gaps. No image calibration or new
validation infrastructure is warranted by this result.
