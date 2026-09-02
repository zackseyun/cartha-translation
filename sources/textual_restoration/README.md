# Textual restoration comparison sources

This is the landing zone for the Codex-only Old and New Testament restoration
program defined in
[`../../docs/TEXTUAL_RESTORATION_PRIORITIES.md`](../../docs/TEXTUAL_RESTORATION_PRIORITIES.md).

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
