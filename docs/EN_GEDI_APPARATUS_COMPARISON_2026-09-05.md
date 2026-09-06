# En-Gedi: all twelve published apparatus units checked against POB

Date: 2026-09-05. This advances textual comparison beyond the previous three
selected words. It covers every comparison item explicitly listed on pp. 10-11
of the 2016 preliminary edition, not every surviving letter of both columns.
It is an edition-based comparison, not fresh CT decipherment or a selection
of a new Hebrew reading.

## Evidence and inspection

The private copy of [Segal et al., *An Early Leviticus Scroll from En-Gedi*,
Textus 26 (2016), preliminary PDF with internal pp. 1-30](https://openscholar.huji.ac.il/sites/default/files/he_bible_project/files/m._segal1.1.pdf)
matches SHA256 `23cee43ef796528b1376fc3e2fba0ac8e066604523fa7db3f0086f892945e425`.
Page locators below refer to that PDF's internal pagination, not the final
journal pagination (29-58 as cited by Himbaza 2020, p. 1 n. 2).
Rendered pages 8-11 were visually inspected in full: the two-column
transcription, reading qualifications, comparative apparatus and footnote 19.
Text extraction dropped substantial bracketed Hebrew and is not a diplomatic
transcription. The PDF skill's visual-review requirement therefore materially
informed preservation classification. A fresh institutional web fetch timed
out; the previously acquired, checksum-matching PDF remained usable.

The [unit specification](../sources/textual_restoration/discovery/en_gedi_apparatus_units.v1.json)
retains comparison labels, supplied prefixes, exact edition locators, bounded
POB/SP contexts and English-impact observations. These labels do not reproduce
every printed certainty dot. Unbracketed editorial wording is not independently
verified manuscript legibility. The
[reproducible receipt](../sources/textual_restoration/discovery/en_gedi_apparatus_check.v1.json)
binds the checks to current POB files, the edition, the pinned SP inputs and QDR.

The SP control is the previously authenticated DT-UCPH Text-Fabric 7.1.3
snapshot, including its source-manuscript and noncommercial-use boundaries;
see [provenance](SAMARITAN_CORPUS_SCREEN_2026-09-04.md#provenance-and-reproducibility).
Here it is a directly consulted digital text, not all Samaritan manuscripts
or a second independent witness for each edition that prints it.

## Complete set of printed comparison units

EG labels below follow the editors' normalized readings, not a new diplomatic
transcription. Brackets mark supplied prefixes in the two affected labels.
Object markers are shown with enough context to avoid confusing repeated words.

| Reference | Published EG comparison label | Pinned SP local control | Immediate English consequence |
|---|---|---|---|
| 2:2 | לבנתה | לבונתה | Spelling alone does not change frankincense. |
| 2:4 | מצת, in the cakes phrase | מצות | Spelling alone does not change unleavened cakes. |
| 2:4 | בלולת | בללות | Spelling alone does not change mixed with oil. |
| 2:9 | ניחח | ניחח; edition reports 4QLevb ניחוח | Spelling alone does not change aroma. |
| 1:2 | קרבנכם | קרבניכם | Singular/plural could matter; POB already has singular offering. |
| 1:4 | וסמך ידו | וסמך את ידו | The object marker requires no different action/object in English. |
| 1:8 | את, before the head | ואת הראש | A conjunction difference does not automatically dictate English punctuation. |
| 1:9 | את, before all | הכהן הכל, without that את | The missing object marker does not remove all. |
| 2:7 | מנחת | מנחה | Construct/absolute syntax needs separate review; pan terminology is not decided. |
| 1:6 | [והפשי]ט | והפשיטו | He/they could matter; the supplied verb stem is not visible evidence. |
| 2:2 | משם | ממנה | From there/from it could matter; POB already has from there. |
| 2:8 | [ו]הבאת | והבאת | You/he could matter; POB's opening verb is second person. |

All twelve editorial forms align with bounded contexts in POB's current WLC
source across ten verses. Ten units are unbracketed editorial labels; two have
supplied prefixes. The SP control differs in ten of the twelve contexts.
These are **local comparison counts**, not twelve fully preserved words,
twelve independent witnesses, ten proven copying errors, or whole-verse
agreement. The published comparison categories are four orthographic, five
linguistic and three content units; these categories are not automatic
translation-impact scores.

In 1:6, only final ט of the printed verb stands outside the supplied prefix,
followed by את in the line. This supports a local ending/boundary comparison
under the editors' reading, not independent verification of the reconstructed
stem. In 2:8, prefix ו is supplied; the editors also discuss an additional
stroke between aleph and tav as a probable imaging artifact. We do not accept
an additional ancient letter from it. This is a concrete future artifact-control
candidate, not an already independently labeled or scored CT region.

## Other witnesses and apparatus limits

The edition reports Greek and Syriac alignments for several units, including
the number of offerings (1:2), skinning verb (1:6), deictic wording (2:2), and
person of the opening verb (2:8). Footnote 19 explicitly makes that versional
reporting selective: it records alignments with Hebrew alternatives rather
than a comprehensive Greek/Syriac apparatus. Silence here must not be counted
as agreement, and a translation is not an exact Hebrew back-translation.
Those full versional apparatuses were not independently collated in this pass.

The pinned QDR snapshot (`3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`)
provides a further digital-transcription check of the edition's 4QLevb reports:
4Q24, fragment group f1_7, line 29 has the normalized comparison form והביא
at Lev 2:8; line 31 has ניחוח at Lev 2:9. Surrounding lines 27-32 were consulted
to retain awareness of cross-line bracket state. This does not replace primary
4Q24 edition/image inspection or add a second manuscript vote.
[Pinned QDR source](https://github.com/evenderekh/qdr/tree/f54f38464e18409eed8286fe24dd24f88d4735dd).

Later identity qualification: the [4Q24 reassessment review](LEVITICUS_WITNESS_IDENTITY_REVIEW_2026-09-05.md)
associates Leviticus 1-3 with proposed 4Q24a, distinct from 4Q24b's later
chapters. Our legacy locators remain unchanged pending fragment-level review.
Do not count these labels as additional support or transfer one hand's date
to the other. This warning does not alter the recorded local comparison forms.

The initial lookup used POB-style `Lev.2.8` / `Lev.2.9` and returned no hits.
Checking the actual source tags (`Lev 2:8` / `Lev 2:9`) found the passages.
That failed lookup was a format mismatch, not manuscript absence. An overbroad
diagnostic dump was truncated; the decisive follow-up was explicitly restricted
to the relevant lines. The receipt stores correct tags, locators and line
hashes, not the full outside corpus.

## POB English outcome and outstanding work

No source-driven English change is selected from these twelve checks. POB
already uses the singular offering, he shall skin, from there, and you shall
bring associated with the relevant published En-Gedi/MT labels. That does not
approve every English clause or settle historical priority among witnesses.
Affiliation with the Masoretic tradition is not an automatic earliest-reading
rule, and En-Gedi's date does not make it the preferred witness in every unit.

There is a **separate, source-stable agency-review lead in Leviticus 2:8**.
POB's later clauses use he, and its lexical rationale assigns priestly handling
to a clause about presenting the offering to the priest. The opening-verb
comparison does not establish the subjects of those later clauses. Review the
Hebrew sequence and ritual context before changing pronouns or making agents
explicit. The verse already has a `needs_review` / `major-issues` cross-check
flag, but the referenced review JSON is absent at its recorded local path;
the flag is not a consulted independent explanation of this particular issue.
No source, main English, reader note or lexical rationale was changed here.

Next: inspect the primary 4Q24 apparatus/images for the two discriminating
units; consult the relevant Greek/Syriac apparatus and translation practice;
complete a line-and-loss map of both EG columns; resolve the English agency
lead separately. For restoration, retain wider renderer tests and register
the specific ghost-shape region against measured data before any reading trial.
The three-word and numeric-renderer receipts remain intact as earlier stages.

## Reproduction

```bash
.venv/bin/python tools/textual_restoration/build_en_gedi_apparatus_check.py /path/to/private/edition.pdf /path/to/sp/tf/7.1.3 /path/to/qdr.1.1.biblical.json --verify-only
.venv/bin/python -m unittest tests.test_en_gedi_apparatus
```

The builder checks actual PDF/SP/QDR hashes and current source/English contexts.
The tests check records, preservation boundaries and alignment, not the
historical reading or the legitimacy of a recovered letter. Source payloads
remain outside Git with their existing rights; no commit or About update is
performed in this pass. The [central research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md)
records this expansion and its limits.

## Later agency follow-up

The [Leviticus 2:8 review](LEVITICUS_2_8_AGENCY_REVIEW_2026-09-05.md) subsequently
corrected two lexical rationales, retaining the Hebrew, English and reader
notes. It separates contextual agent clarification from a proposed imperative
repointing and records the Greek cross-verse clause. The twelve-unit receipt
was regenerated to bind to the metadata-repaired verse file; comparison labels,
source contexts and English outcomes did not change. The prior file hash and
exact two-line repair are retained in that follow-up's decision record.
