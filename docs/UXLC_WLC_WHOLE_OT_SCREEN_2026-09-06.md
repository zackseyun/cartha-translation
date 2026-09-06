# Whole-OT digital-transcription screen — 2026-09-06

## Result and limits

All 39 ordinary UXLC 2.5 book files were compared with POB's actual vendored
OSHB/WLC XML: 23,213 shared chapter/verse labels, none unmatched. This is a
complete comparison of these two pinned digital inputs at the defined layers,
**not** a comparison of all OT manuscripts or proof of an optimal source text.
Both inputs represent the Leningrad tradition; their agreement is not two
independent manuscript votes. No canonical source, English, or note was changed.

| First differing written-text layer | Verse labels |
| --- | ---: |
| Consonants | 5 |
| Pointing (consonants equal) | 374 |
| Accents/meteg (lower layers equal) | 3,897 |
| Other full-stream characters/punctuation | 203 |
| Equal through the normalized full stream | 18,734 |

These mutually exclusive counts total 23,213. Separate, overlapping diagnostics:
67 ordered qere-payload differences, 13 qere-presence/word-count differences,
24 written token-boundary-or-payload differences. There are 4,535 distinct
flagged verse rows. Counts are not numbers of scribal errors or English defects.
Moving marks between a ketiv and its qere can create a pointing difference
without changing either tradition's intended pronunciation.

## Five consonant leads, not adopted corrections

| Passage | Vendored written token | UXLC written token | Next question |
| --- | --- | --- | --- |
| 2 Samuel 13:37 | עמיחור | עמיחוד | Inspect dalet/resh and ketiv/qere history; both files' qere is Ammihud. |
| 2 Samuel 14:7 | ונמתהו | ונמיתהו | Check the additional yod against the codex and editorial change record. |
| 2 Chronicles 27:4 | בירניות | ביריניות | Check orthography; do not infer different fortress terminology from a spelling difference. |
| Ezekiel 16:36 | בתזנותיך | כתזנותיך | Check bet/kaf, possible grammatical effect and contrary evidence. |
| Amos 7:2 | לאכול | לאכל | Check plene/defective spelling; this alone does not establish an English change. |

The receipt joins all five to current POB source and English, preserving each
canonical file hash. Four source fields match the vendored consonant stream;
2 Samuel 14:7 matches neither under the deliberately literal comparison. An
explicit follow-up removed only its terminal paragraph-marker פ diagnostically:
the remaining consonants exactly match WLC, still not UXLC. Both XML inputs
encode that paragraph sign separately. This is not a third lexical spelling;
the yod difference is still real. The receipt preserves the original literal
neither-match and does not silently strip or correct the canonical source.
POB's 2 Samuel 13:37 currently prints Ammihur with a note; this is a concrete
follow-up candidate, not permission to change a name merely because UXLC differs.

### Publisher change-history follow-up

A separate agent checked the pinned book headers and actual publisher change
records. All five are reported word-level corrections to the transcription of
the **same codex**, not extra witnesses or mere Unicode normalization. The
following are publisher observations, not our own readings of manuscript pixels
or independent consultation of the BHL apparatus mentioned by the publisher.

| Lead | Change entry; word locator; reported codex position | Editorial explanation and retained uncertainty |
| --- | --- | --- |
| 2 Samuel 13:37 | 2022.08.30–23; 13:37.7; folio175B, col3, line19 | Publisher reads final dalet in both ketiv/qere; retained t uncertainty concerns the preceding vav/yod, not dalet versus resh. |
| 2 Samuel 14:7 | 2022.08.30–24; 14:7.12; folio176A, col1, line20 | Publisher identifies a yod with a lighter lower portion, possibly flaking; reports BHL body/appendix disagreement. |
| 2 Chronicles 27:4 | 2023.08.10–10; 27:4.7; folio359A, col2, line10 | Publisher identifies an additional unpointed yod after resh; reports BHL body/appendix disagreement. |
| Ezekiel 16:36 | 2022.12.11–10; 16:36.10; folio283B, col2, line14 | Explicitly uncertain bet/kaf in poorly preserved writing. Summary/TEI says add c, but detailed action and current XML use t. Do not call this a certain repair. |
| Amos 7:2 | 2022.12.12–3; 7:2.4; folio311A, col1, line18 | Publisher removes vav and puts holam on kaf. Its Unicode prose accidentally retains vav on both sides; displayed Hebrew, instruction and current XML agree on removal. |

Sources: [Samuel changes](https://www.tanach.us/Changes/2022.12.07%20-%20Changes/2022.12.07%20-%20Changes.html),
[Chronicles changes](https://www.tanach.us/Changes/2023.10.19%20-%20Changes/2023.10.19%20-%20Changes.html),
[Ezekiel/Amos changes](https://www.tanach.us/Changes/2023.04.01%20-%20Changes/2023.04.01%20-%20Changes.html).
The exact corresponding book-header correction citations are retained inside
the pinned private archive. Locators now make image follow-up concrete, but
the screen does not independently resolve any uncertain ink.

## Inputs, acquisition and attribution

Source: **Unicode/XML Leningrad Codex: UXLC 2.5 (27.6), Tanach.us Inc.,
West Redding, CT, USA, April 2026**. The publisher describes it as a fork of
WLC 4.20, revised against Leningrad images; it must not itself be labelled WLC.
[Publisher's description](https://www.tanach.us/Pages/About.html).

The actual ZIP has 2,365,002 bytes and SHA-256
`1bc6e006f43d3b18f2f718cefa3aa4774cac2c54092c28d173dd61996c43a050`,
matching the [publisher's verification table](https://www.tanach.us/Pages/Technical.html).
Its build is 27.6, timestamp 31 March 2026 12:00; book headers state publication
1 April 2026. Those are edition dates, not manuscript dates. All 39 local WLC
files and UXLC members have individual hashes in the receipt.

Ordinary HTTPS acquisition used a 3,000,000-byte cap and 60-second deadline.
The ZIP's declared expanded size is 14,382,486 bytes, below the 20,000,000-byte
cap; members were read in memory, never extracted. Five Documentary Hypothesis
Torah duplicates, Header/Index and ancillary site files are not extra books.
The archive and full headers/images remain private. Biblical text is reusable
under the [publisher's license](https://www.tanach.us/License.html); unrelated
site assets carry separate restrictions and are not vendored here.

## Method and failure history

The [protocol](../sources/textual_restoration/discovery/uxlc_wlc_comparison_protocol.v1.json)
was written before the result, after inspecting format documentation and XML
examples. This is not a blind benchmark. Alignment is by exact mapped
book/chapter/verse label; it does not certify semantic equivalence of numbering.

The written lane takes only direct WLC verse words and UXLC w/k elements.
Qere stays separate: WLC variant-note x-qere readings versus UXLC q elements.
Catchwords, alternative accent readings, explanatory notes and descendant word
duplicates do not become additional written text. Large/small/suspended letters
and XML tails survive; annotation codes do not become Hebrew letters.
WLC's separately encoded maqqef, paseq and sof-pasuq are interleaved at their
actual positions for comparison with UXLC's inline punctuation. Paragraph
markers stay annotations. The declared character lanes use Unicode NFD before
and after filtering to separate consonants, pointing, accents/meteg and residual
format. Morphological
slashes are not physical manuscript word divisions.

Qere comparison is an ordered verse-level payload screen through accents,
excluding punctuation; it is not an alignment of individual apparatus units.
Presence/word counts are additionally checked so empty-qere records do not
vanish. Raw local positions, words and annotations remain in flagged rows.
The publisher's changing qere conventions must be checked before assigning
historical significance to these diagnostics.

Two unsuccessful development attempts are retained here: a ZIP member lookup
without `Books/` failed, after which the actual member inventory supplied the
right path; the first comparator run rejected nested WLC words and wrote no
receipt. Inspection found eleven word-internal seg elements of three letter-
decoration types. An explicit allowlist retained their letters and tails;
unknown tags still fail. The subsequent full run produced the counts above.
No failed run is described as a completed comparison, and no input was altered.

The independent judge then **rejected the first saved result**: filtering out
CGJ, slashes or whitespace after NFD could expose a noncanonical combining-mark
order, falsely counted as a textual difference. The corrected normalization
applies NFD again after each lane's filtering. A synthetic blocker/mark-order
regression now covers all three blockers and the pointing/accent/full lanes.
Raw input is unchanged; canonically equivalent order-only differences are not
promoted into textual variants. All 39 books were rerun without tuning to a
target count. The rejected result remains private at SHA-256
`515b365164a135a545f95765bb669cd0efb7c481d00c111b9108c8f181bcb6b8`.
It had 5,356 flagged rows, 824 pointing, 4,277 accent and 197 full-stream first
differences; those counts are superseded by the table above. The repair changes
916 written classifications, of which 824 become equal; qere payload flags
drop from 75 to 67. The five consonant leads are unchanged. This is a parser
repair and review history, not an experiment made to pass by changing evidence.

## Reproduction and next gates

[Comparator](../tools/textual_restoration/compare_uxlc_wlc.py),
[tests](../tests/test_uxlc_wlc_comparison.py), and
[full result](../sources/textual_restoration/discovery/uxlc_wlc_comparison.v1.json).
Run `python tools/textual_restoration/compare_uxlc_wlc.py PATH_TO_PINNED_ZIP`
in the repository environment to reproduce and compare with the saved receipt.
`--write` creates a result only if the destination does not already exist.
The result binds its protocol, comparator, book map, local input files and
five current canonical context files. Later edits require explicit versioning,
not silently revising a historical claim.

Next: check all five against the corresponding codex image and publisher's
change history, then use relevant Masoretic apparatuses and other witnesses
where the question warrants them. Sample pointing/qere classes before prioritizing
translation review. None of this replaces Judean Desert, Samaritan, Greek,
other versional, or quotation work. A same-codex transcription screen cannot
choose the earliest attainable Hebrew/Aramaic text by itself.
