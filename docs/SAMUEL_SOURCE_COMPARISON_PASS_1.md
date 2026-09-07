# Samuel source comparison — pass 1

**Current supplement:** the 2026-09-06 apparatus review below resolves one
formerly disputed Greek attribution and corrects the reader note. Earlier
promotion prerequisites describe the initial pass; a fresh image reading is
not a universal prerequisite for using a published transcription under method 2.0.

Checked: 2026-09-04

## Outcome

The existing 1 Samuel 17:4 pilot has been upgraded from secondary-report-only
evidence to a pinned source comparison. The result strengthens, but does not
canonically promote, the working preference for four cubits and a span:

- WLC reads `שש אמות וזרת`, “six cubits and a span.”
- 4QSama (4Q51), fragments 12–14, line 3, reads
  `]א֯רבע[ א]מות וזרת`, supporting “four cubits and a span.”
- The pinned Rahlfs Greek control reads
  `τεσσάρων πήχεων καὶ σπιθαμῆς`, “four cubits and a span.”

The POB main text still reads six because its declared source remains WLC. Its
measurement footnote is now attached to the measurement rather than to “Gath,”
and it discloses the direct Hebrew and Greek four-cubit reading.

## Evidentiary boundary

The Qumran-Digital transcription places most of the surrounding clause inside
editorial brackets. Within the numeral, the alef is dotted as uncertain while
resh-bet-ayin are preserved. Part of `אמות`, “cubits,” is also supplied. This is
adequate published-transcription support for the numeral four; it is not a
claim that the whole reconstructed line is visible on the leather.

The physical manuscript is counted once. Qumran-Digital is its transcription
layer, the IAA record is its institutional identity and image-access layer, and
the Rahlfs reading is daughter-version evidence. Those access and edition
layers are not additional Hebrew witnesses.

## Reproducible controls

The Greek text was extracted from OpenScriptorium `lxx-morph` at commit
`c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`. During this pass, the earlier
Pentateuch record's upstream commit object was found to be unavailable. All six
stored Pentateuch Greek verses were compared byte-for-byte with the current
resolvable commit and were identical, so their snapshot metadata was refreshed
without changing any reading.

The 4Q51 transcript is pinned to its 2025-03-11 version. The IAA manuscript page
provides the institutional image inventory, but the exact fragments 12–14 image
region has not yet been crosswalked or independently read.

## Adjudication effect

The earlier moderate working preference for four remains appropriately
moderate. Direct early Hebrew and the Greek control converge on four, but the
six reading is also ancient in versional evidence, and the broader short/long
literary forms of the David–Goliath narrative must not be reduced to a single
number substitution.

No main-text change has been made. Before promotion, the passage still requires
image verification, the DJD XVII material and reading notes, individual Greek
manuscript collation beyond an edited Rahlfs control, broader Samuel literary-
form review, an independent editorial pass, and an atomic critical-Hebrew plus
English selection bundle.

## Next Samuel cases

1. 1 Samuel 10:27–11:1 — the Nahash narrative material in 4Q51 and its relation
   to Josephus and the shorter Masoretic transition.
2. 1 Samuel 14:41 — the shorter prayer and longer Urim–Thummim form, while
   keeping Greek retroversion distinct from surviving Hebrew ink.
3. 1 Samuel 1:24 — three bulls versus a three-year-old bull.
4. 1 Samuel 13:1 — a conjecture-control case in which missing numbers must not
   be silently supplied as recovered text.

Machine-readable evidence is in
[`../sources/textual_restoration/coverage/samuel_pilot.v1.json`](../sources/textual_restoration/coverage/samuel_pilot.v1.json)
and
[`../sources/textual_restoration/comparisons/samuel_controls.v1.json`](../sources/textual_restoration/comparisons/samuel_controls.v1.json).

Primary access points:

- [Qumran-Digital 4Q51 versioned transcription](https://lexicon.qumran-digital.org/transcriptions/4Q51/2025-03-11/index.html)
- [IAA Leon Levy Digital Library 4Q51 record](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q51-2?locale=en_US)
- [OpenScriptorium lxx-morph](https://github.com/OpenScriptorium/lxx-morph)

## Greek numeral apparatus directly checked — 2026-09-06

Reused the private consultation copy of [Brooke, McLean and Thackeray,
*The Old Testament in Greek*, II.1 (1927)](https://tmcdaniel.palmerseminary.edu/Brooke%26McLean/LXX_Brooke%26McLean_2-1.pdf),
printed p. 55 / PDF p. 71. The complete rendered page and Samuel preface v
(PDF 11) were visually inspected. The [1906 general conventions](https://tmcdaniel.palmerseminary.edu/Brooke%26McLean/LXX_Brooke%26McLean_1-1.pdf),
printed i–ii / PDF 9–10, were also visually checked: outer-margin sigla identify
the base; the main apparatus and separate additional apparatus have distinct
roles. Samuel warns that some cursive sigla change between volumes.

| Layer | Actually read | Consequence |
|---|---|---|
| Main text, base B | `τεσσάρων πήχεων καὶ σπιθαμῆς` | Four cubits and a span in the Vaticanus-based edition text. |
| Main numeral apparatus | `τεσσαρων] πεντε N… : εξ A…` | Five is explicitly reported for N; six for A (Alexandrinus), with other sigla following each. Ellipses here abbreviate the support lists, not manuscript gaps. |
| Separate bottom apparatus | `σʹ εξ j` within the numeral entry | A separately attributed six reading, not another continuous-text manuscript vote. No new examination of manuscript j or its marginal hand. |

The independent `goliath_apparatus_check` read the same printed page and confirmed
the three numeral readings and the separation of apparatus layers. No complete
support-list transcription, fresh codex collation, new dating, N shelfmark
identification or statistical independence claim is made. In particular, this
resolves the pilot's conflicting Alexandrinus summaries **at the level of this
edition's report**, not by reading its physical leaf. The earlier uncollated
five-cubit lead now has directly consulted published apparatus support.

### Source-selection consequence

Four remains the working preference because the existing qualified Hebrew
transcription and Greek base agree; it is no longer permissible to summarize
the Greek evidence as simply four. Five is a real reported third candidate,
but this page supplies no corresponding Hebrew five-reading or demonstrated
direction of change. Six has Greek as well as Masoretic support. Inflation,
reduction and assimilation remain competing explanations; numeric plausibility
alone cannot select the source. The freshly read [NET note 2](https://classic.net.bible.org/verse.php?book=1Sa&chapter=17&verse=4)
favors four partly as a more reasonable height; that judgment is not manuscript
evidence and is not adopted as a deciding test.

The four/six decision still requires evaluation of the Hebrew edition's reading
notes and its relation to the narrative's literary forms, not another uniform-LXX
claim. The primary Qumran transcription URL failed in the web reader this pass;
the earlier pinned Hebrew finding is reused, not represented as a fresh check.
No new confidence score or source-unit/whole-verse promotion follows.

### Narrow canonical correction

One follow-up to the same reviewer approved two exact note substitutions:
“the Septuagint” becomes “some Greek witnesses”; the outdated universal image
prerequisite becomes “a reviewed critical-source replacement.” This is not a
second consensus vote or source-selection approval. Hebrew, main English,
measurements and other rationales remain unchanged. The old cross-check is
archived verbatim and active status reset. The
[receipt](../sources/textual_restoration/applications/goliath17_4_apparatus_disclosure.v1.json)
records hashes, exact change scope and actual export verification. The larger
source-selection gate remains open; no manuscript restoration or reader
deployment is claimed. PDF rendering followed the PDF skill; no PDF was edited
or redistributed and no new image evidence was manufactured.
