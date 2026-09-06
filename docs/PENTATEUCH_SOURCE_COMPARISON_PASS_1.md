# Pentateuch source comparison — pass 1

Checked: 2026-09-04

Continued in [pass 2](PENTATEUCH_SOURCE_COMPARISON_PASS_2.md), which adds
individually identified Judean Desert Hebrew manuscripts. The statements below
describe the edition-control stage before that evidence was added.

This pass compares three POB casebook passages against pinned machine-readable
WLC, Samaritan Pentateuch, and Rahlfs Septuagint controls. It is a source-text
comparison, not a manuscript-image transcription or a decision about the
earliest attainable reading.

The Samaritan reference dataset is based on Dublin Chester Beatty Library 751
through Deuteronomy 32:36 and MS Garizim 1 thereafter. It must not be described
as a transcription of the separately mapped Rylands Samaritan MS 1 images.
The Greek control is an edited Rahlfs text and remains a daughter-version
witness, not surviving Hebrew ink.

## Results

| Passage | Masoretic control | Samaritan control | Old Greek control | Current English effect |
|---|---|---|---|---|
| Genesis 4:8 | Cain's speech is introduced but no words are recorded | Adds `נלכה השדה`, “Let us go to the field” | Adds `διέλθωμεν εἰς τὸ πεδίον`, the comparable invitation | Material variant already footnoted; longer text still requires adjudication |
| Exodus 1:5 | Seventy | Seventy | Seventy-five; Joseph clause precedes the total | Main text remains seventy pending genealogical and manuscript review |
| Exodus 12:40 | Israel's residence in Egypt | Israel and the fathers in Canaan and Egypt | Israel in Egypt and Canaan, without “the fathers” in the Rahlfs control | Main text remains WLC-based; footnote repaired to distinguish the two longer forms |

## English POB finding

The comparison produced one immediate publication-quality correction without
selecting a new source text. Exodus 12:40 previously gave a composite footnote
that blended the Samaritan addition of “their fathers” with the Old Greek
geographical order. The footnote now reports the Samaritan and Septuagint forms
separately.

No main-text wording was changed. The three source decisions remain
`not-adjudicated`, because edition-level controls alone do not establish
priority. The next step is to add actual manuscript attestations, coverage,
relationships, and competing transmission explanations.

## Machine-readable record

The exact readings, source roles, pinned upstream commits, baseline hashes, and
English effects are stored in
[`../sources/textual_restoration/comparisons/pentateuch_controls.v1.json`](../sources/textual_restoration/comparisons/pentateuch_controls.v1.json).
