# Exodus incense altar: order is not wording

Checked: 2026-09-05. Published/digital-text comparison by Codex, not a fresh
image reading, independent blind review, or completed historical adjudication.

## Result

The whole-Torah screen's ten unmatched Exodus labels represent relocated
instructions in this Samaritan reference, not missing instructions. An explicit
11-segment map connects its extended Exodus 26:35 to WLC 26:35 and 30:1–10.

| Control | Incense instructions | Mercy-seat placement clause corresponding to MT 30:6 |
|---|---|---|
| WLC / Masoretic base | 30:1–10 | Present |
| Pinned Samaritan transcription | Within extended 26:35, after the table/lampstand instruction | Absent |
| Pinned Rahlfs Greek control | 30:1–10 | Absent |

Passage order and clause wording require separate decisions. This is an
edition/transcription comparison, not a census of manuscript support. Locally
similar shorter wording does not establish identical Hebrew exemplars behind
the two traditions.

## Reproducible alignment

The [metadata receipt](../sources/textual_restoration/discovery/exodus_incense_alignment.v1.json)
records unique, editor-selected instruction boundaries. All spans are zero-based,
half-open offsets in raw Samaritan sign text, including spaces. They exactly
reassemble all 721 characters, including two trailing spaces.

| WLC target | SP character span | Consonantal comparison |
|---|---|---|
| 26:35 | 0–92 | Different |
| 30:1 | 92–132 | Different |
| 30:2 | 132–186 | Different |
| 30:3 | 186–260 | Equal |
| 30:4 | 260–354 | Different |
| 30:5 | 354–392 | Equal |
| 30:6 | 392–447 | Different |
| 30:7 | 447–508 | Different |
| 30:8 | 508–577 | Different |
| 30:9 | 577–628 | Equal |
| 30:10 | 628–721 | Different |

Differences include spelling, not only substantive variants. Normalization
ignores pointing and word division but preserves matres and final letter forms.
POB's source is checked against WLC, allowing paragraph signs only where its
XML explicitly encodes them. The final pe in 30:10 is such a sign, not an extra
lexical letter or a reason to change the source.

SP input: DT-UCPH 7.1.3, commit
`2f2120286ac48d4ff3d04e0107e33efd864aa9e1`; Exodus uses Chester Beatty Library
751, not the separate Rylands manuscript. Greek input: `lxx-morph`, commit
`c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`, file
`db/seeds/lxx_morph/exodus.json`. Feature files, WLC books, Greek input, segments,
and current POB verse files have content hashes in the receipt. The external
SP corpus is not vendored or relicensed; the receipt exports metadata only.

```bash
.venv/bin/python tools/textual_restoration/build_samaritan_screen.py /path/to/sp/tf/7.1.3 --incense-alignment --greek-json /path/to/lxx-morph/db/seeds/lxx_morph/exodus.json
.venv/bin/python tools/textual_restoration/build_samaritan_screen.py /path/to/sp/tf/7.1.3 --incense-alignment --greek-json /path/to/lxx-morph/db/seeds/lxx_morph/exodus.json --verify-only
.venv/bin/python -m unittest tests.test_samaritan_screen tests.test_ot_witness_registry
```

## Qumran evidence: preserve its limits

The versioned 4Q11 transcription, fragments 30 ii–34, lines 10–11, presents the
table/lampstand instruction followed by the entrance-screen instruction
(26:35→36), with damaged and supplied letters marked. This supports the
published arrangement without an intervening incense block, not a fresh
inspection of the manuscript photograph.
[Qumran-Digital, version 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/4Q11/2026-05-21/index.html?v=2026-05-21).

Dayfani's section 3 reports chapter-26 placement for 4Q22 and SP, and its absence
there in 4Q11. Chapter 30 is not preserved in 4Q11; that witness does not establish
where it originally placed the block. Neither this order evidence nor a general
family label establishes its wording at 30:6. Direct 4Q22 transcription/material
verification remains pending: our 4Q22 statement rests on this scholarly report,
not a newly inspected edition or image.
[Hila Dayfani, Textus 30 (2021), 105–129, section 3](https://doi.org/10.1163/2589255X-BJA10017).

## Actual POB impact

In [Exodus 30:6](../translation/ot/exodus/030/006.yaml), an existing note offered
“atonement cover” at the ark-of-testimony marker. It belongs to “mercy seat.”
The corrected notes distinguish those terms, disclose the shorter Samaritan/
standard Greek reading, and explain retention of MT's wording and order. The
stale lexical entry now matches the displayed “before.” Hebrew source and
English words are unchanged; markers, notes and explanatory metadata changed.

The UBS handbook also identifies the mercy seat as the ark's cover and discusses
the shorter Greek reading. Its unspecified additional Hebrew manuscripts are
not converted into identified witnesses in our ledger.
[UBS commentary on Exodus 30:6](https://tips.translation.bible/story/translation-commentary-on-exod-306/).

`EXO.30.6.mercy-seat-clause` is the twelfth formal OT comparison case. Its three
digital controls add no physical coverage record. It remains unadjudicated;
the registry still has 22 entries and 19 passage-coverage records.

## Next decision gates

Inspect the appropriate Hebrew/Greek apparatuses, Samaritan critical edition,
and direct 4Q22 publication before assigning broader support. Test omission
through repeated phrasing, explanatory expansion, and local translation
technique against context. Natural furniture order could reflect editorial
rearrangement; a shorter clause is not necessarily earlier. Do not combine
preferred order and preferred wording into a synthetic source without an
explicit literary target and a coherent transmission argument.

This pass closes a mapping problem and a reader-note defect, not the historical
source-selection question. It does not recover previously unread text.
