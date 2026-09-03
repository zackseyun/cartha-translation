# Textual restoration comparison sources

This is the landing zone for the Codex-only Old and New Testament restoration
program defined in
[`../../docs/TEXTUAL_RESTORATION_PRIORITIES.md`](../../docs/TEXTUAL_RESTORATION_PRIORITIES.md).

## Working sample

[`samples/hebrew_comparison.v1.json`](samples/hebrew_comparison.v1.json) records
three published Hebrew variants and their English effects, alongside the
current local POB source snapshot. Read the
[three-passage demonstration](../../docs/HEBREW_COMPARISON_SAMPLE.md). These are
reported witness readings, not new image restorations or approved POB changes.

The next applied pass is
[`decisions/hebrew_pilot.v1.json`](decisions/hebrew_pilot.v1.json), rendered as
the [multi-witness adjudication report](../../docs/HEBREW_PILOT_ADJUDICATION.md).
It adds witness relationships, modest chronological preference, counterarguments,
and separate working choices under the
[adjudication method](../../docs/TEXTUAL_ADJUDICATION_METHOD.md).

The Greek track has its first [Mark 1:41 decision](decisions/nt_pilot.v1.json)
and [rendered report](../../docs/NT_PILOT_ADJUDICATION.md). This is a working
assessment of published attestations, not a new image reading or canonical edit.

The [English impact check](../../docs/ENGLISH_TRANSLATION_IMPACT_CHECK.md)
compares the working choices with ten current local English records and shows
exact draft replacements, possible additions, and unchanged or pending cases.
Its [data](decisions/english_impact_check.v1.json) explicitly distinguish a
proposed English change from a canonical change actually applied.

## Planned packages

The [inventory](inventory/README.md) now contains a canonical corpus-wide note
screen, WLC written/read and editorial annotations, and all 27 books of the
licensed SBLGNT edition apparatus. Inspect the
[book-level map](../../docs/HEBREW_AND_NT_VARIANT_MAP.md) and
[priority casebook](../../docs/TEXTUAL_VARIANT_CASEBOOK.md). These are separate
evidence layers, not a claim to have collated all surviving manuscripts.

The source packages will be created in this order:

1. **OT Masoretic controls:** WLC/UHB mappings, then Aleppo, Sassoon, and
   BHQ/BHS comparison records where lawful.
2. **OT direct ancient witnesses:** Qumran/Judaean Desert Hebrew and Aramaic,
   Samaritan Pentateuch, Hebrew Ben Sira, and Aramaic/Hebrew Tobit.
3. **OT Greek controls:** Swete, major Greek codices, and Göttingen/Rahlfs
   consultation records, with Greek-composed books distinguished from Greek
   translations of Semitic texts.
4. **NT Greek witnesses:** SBLGNT mapping, ECM/UBS/NA apparatus records, early
   papyri, and the major codices.
5. **Ancient versions:** Old Latin, Old Syriac/Peshitta, Coptic, Armenian,
   Georgian, and Geʿez only where they can distinguish competing source-language
   readings.

Every record must identify whether it is a direct-language witness, daughter
translation, modern transcription, critical edition, editorial reconstruction,
or display-only ImageGen reconstruction. Rights-restricted sources remain
metadata or private-consultation records and are not vendored.

ImageGen files belong only under `images/visual_reconstructions/`. They must be
watermarked **RECONSTRUCTED — NOT MANUSCRIPT EVIDENCE** and may never be used as
input to OCR, transcription, collation, or translation.

Until the unified registry and schemas are implemented, the existing
[`../dead_sea_scrolls/`](../dead_sea_scrolls/) registry, image-provenance, and
transcription formats remain the operational model.
