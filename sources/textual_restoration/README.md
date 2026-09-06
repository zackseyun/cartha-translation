# Textual restoration comparison sources

Central history and decision trail:
[research log](../../docs/TEXTUAL_RESTORATION_RESEARCH_LOG.md). Update it for
each substantive pass; detailed evidence stays in the linked case artifacts.

This is the landing zone for the Codex-only Old and New Testament restoration
program defined in
[`../../docs/TEXTUAL_RESTORATION_PRIORITIES.md`](../../docs/TEXTUAL_RESTORATION_PRIORITIES.md).

Start with the [2026-09-04 approach review](../../docs/TEXTUAL_RESTORATION_APPROACH_REVIEW_2026-09-04.md)
and [method 2.0](../../docs/TEXTUAL_ADJUDICATION_METHOD.md). The review distinguishes
what the current work establishes from calibration and publication machinery
still to implement. Existing decision records retain their historical method
version until re-reviewed.

The [OT/NT source coverage audit](../../docs/BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md)
answers which sources belong in the comparison and identifies what is missing.
Its catalogue and edition targets are a work plan, not imported evidence or a
claim to have collated every discovered manuscript.

The [QDR discovery receipt](discovery/README.md) now scans every word-reference
field in the pinned biblical index, distinguishes 266 records from 265 labels,
and links 24 priority anchors through actual WLC source-text matching. It is
one completed index screen, not a completed institutional-catalogue audit.

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

The [Deuteronomy full-record draft](../../docs/APPLICATION_DRAFT_PREFLIGHT_2026-09-05.md)
has a byte-exact baseline snapshot, explicit edit plan, source/English/notes
candidate, archived review metadata, component hashes and an actual local
full-book export probe under `applications/`. It is not an approval or
application receipt; the current schema and disclosure gaps remain open.

The [reader-path trace](../../docs/READER_DISCLOSURE_TRACE_2026-09-05.md)
repairs the local canonical footnote export and preserves preflight v1 alongside
v2. It also identifies the separate website-loader stripping policy; no
deployed-reader or independent editorial gate is thereby completed.

The validated
[`ot_witness_registry.v1.json`](ot_witness_registry.v1.json) is now the
authoritative discovery ledger for the Old Testament track. It records stable
access points, rights state, evidence class, relationship group, corpus-mapping
state, restoration suitability, and the next concrete action. Validate it with:

```bash
.venv/bin/python tools/textual_restoration/validate_ot_witness_registry.py --report
.venv/bin/python -m unittest discover -s tests -p 'test_ot_witness_registry.py'
```

The JSON Schema is
[`../../schemas/ot-witness-registry.schema.json`](../../schemas/ot-witness-registry.schema.json).
The registry is deliberately incomplete while discovery continues; a source is
not treated as corpus-covered until its actual book/page/verse coverage is
mapped.

Passage-level survival is stored separately under [`coverage/`](coverage/).
The first maps resolve three Pentateuch pilot passages to exact Rylands
Samaritan MS 1 canvases and now record seventeen Judean Desert passage entries
across thirteen comparison cases, including disputed and uncertain coverage. They distinguish genuine
reading support from verse coverage whose decisive letters fall in a lacuna. Image locators,
published transcriptions, and acquired pixels have separate status fields. Its schema is
[`../../schemas/ot-passage-coverage.schema.json`](../../schemas/ot-passage-coverage.schema.json).

Edition and reference-text comparisons are stored separately under
[`comparisons/`](comparisons/). The first Pentateuch pass pins its upstream
commits and keeps the WLC, Samaritan, and Rahlfs LXX relationship groups
distinct. Comparison records validate against
[`../../schemas/ot-source-comparison.schema.json`](../../schemas/ot-source-comparison.schema.json).
See the
[human-readable report](../../docs/PENTATEUCH_SOURCE_COMPARISON_PASS_1.md).
The [second pass](../../docs/PENTATEUCH_SOURCE_COMPARISON_PASS_2.md) adds direct
Hebrew evidence from 4Q2, 4Q1, 4Q11, 4Q13, 2Q2, and 4Q14 while counting each
physical manuscript only once.
The [third pass](../../docs/PENTATEUCH_SOURCE_COMPARISON_PASS_3.md) adds
Deuteronomy 27:4 and 32:43, prevents 4Q33's editorially reconstructed mountain
name from being counted as visible evidence, and records the longer Hebrew form
of Deuteronomy 32:43 in 4Q44.
The [fourth pass](../../docs/PENTATEUCH_SOURCE_COMPARISON_PASS_4.md) upgrades
Deuteronomy 32:8 to pinned 4Q37, 4Q45, Samaritan, and Greek controls. It records
4Q37 as support for “sons of God,” 4Q45 as coverage-only, and explains why a
critical Hebrew source and its English rendering must be promoted atomically.
The [first Samuel pass](../../docs/SAMUEL_SOURCE_COMPARISON_PASS_1.md) upgrades
1 Samuel 17:4 to a pinned 4Q51 transcription and Greek control, preserves the
uncertain and supplied-letter boundary, and repairs the POB variant disclosure
without silently changing its WLC-aligned main text.
The [second Samuel pass](../../docs/SAMUEL_SOURCE_COMPARISON_PASS_2.md) checks
1 Samuel 14:41 and 2 Samuel 21:19, withholds positive support from disputed 4Q52
and unassigned 1Q7 traces, and keeps the Chronicles parallel separate from
Samuel manuscript evidence.
The [third Samuel pass](../../docs/SAMUEL_SOURCE_COMPARISON_PASS_3.md) adds
1 Samuel 1:24, preserves the attested age-related word and bread in 4Q51,
records counterarguments, and makes a provisional preference without promoting
a reconstructed source phrase. There are now ten comparison cases and 17
coverage records, not ten completed adjudications.

The same report now records a partial, context-informed check of the
edition-cited IAA historical infrared photograph for 1 Samuel 1:24. Coverage
schema 1.3.0 permits a private acquired-pixel receipt without declaring image
verification complete. It stores provenance, two target-tile hashes, and
explicit review/rights limitations; the image bytes remain outside this repo.
Normal validation checks the receipt, not the private bytes or reading accuracy.
When the private consultation directory is available, verify its hashes with:

```bash
.venv/bin/python tools/textual_restoration/validate_ot_witness_registry.py --private-image-root /absolute/path/to/research_sources
```

The root contains the receipt's `private_copy_key` directory and its original
opaque asset filenames. This command neither downloads nor publishes images.

The versional follow-up to the same Samuel case now consults the Larger
Cambridge apparatus and CAL's Leiden-derived Syriac text. The Syriac supports
an age-related singular bull without bread in a short narrative; the Greek
Hexaplaric apparatus preserves an opposing three-bull rendering attributed to
Symmachus. These are separate evidence layers, not an expanded manuscript vote
count. The registry now has 16 source/object/family entries, including the two
new edition-access records. Ten comparison cases and 17 coverage records remain
the scope; no additional manuscript-image collation or canonical promotion is
implied. CAL direct downloads returned its home page and are not frozen text
snapshots; dated consulted URLs and limited excerpts are recorded instead.

The subsequent [non-Qumran audit](../../docs/NON_QUMRAN_SOURCE_RECONCILIATION_2026-09-04.md)
brings the registry to 18 entries by adding En-Gedi and the Greek Minor Prophets
scroll. It also generates a 22-label discovery screen and three narrowly scoped
published-word retention checks. These do not increase the ten formal comparison
dossiers or 17 coverage records, and no CT-restoration experiment has run.

Atomic source-and-English bundles are stored separately under
[`selections/`](selections/). The [Psalm 22 pass](../../docs/PSALM_22_SOURCE_COMPARISON_PASS_1.md)
subsequently adds an eleventh formal case and two coverage records (19 total),
with published spelling distinguished from meaning and supplied letters.
Its note/reasoning corrections do not select new Hebrew or English main text.
The same case's versional follow-up adds directly consulted CAL Syriac and
Aramaic edition controls: an injury action versus biting with lion imagery.
The expanded Peshitta record and new Targum Psalms entry bring the registry to
19 mixed entries, without adding physical-manuscript coverage records or
changing the canonical verse. See the pass report for lexical and source URLs.
The subsequent [whole-Torah screen](../../docs/SAMARITAN_CORPUS_SCREEN_2026-09-04.md)
compares all 5,841 nodes of the pinned Samaritan reference with WLC and exposes
passage relocation as well as spelling/wording leads. Registering the existing
SP and Rahlfs controls plus the not-yet-accessible OHB sample brings the mixed
registry to 22 entries; formal case/coverage counts remain 11 and 19.

The first source-selection pilot binds the Deuteronomy 32:8
working Hebrew selection, English candidate, retained controls, baseline hash,
and open review gates without altering the canonical verse. Its schema is
[`../../schemas/ot-critical-source-selection.schema.json`](../../schemas/ot-critical-source-selection.schema.json).
The validator cross-checks every selected direct reading against the comparison
case and adjudication record. The current pilot rejects promotion claims even
if all flags are marked complete: review receipts and source/English/export
application checks are still to implement. Required review gates cannot be
removed to bypass review.

Use [`../../tools/textual_restoration/extract_qdr_passages.py`](../../tools/textual_restoration/extract_qdr_passages.py)
for licensed local QDR snapshots. It searches the reference carried by every
nested word so a fragmentary verse spanning multiple lines is not mistaken for
no coverage.

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

The [September 5 Latin follow-up](../../docs/PSALM_145_SOURCE_COMPARISON_2026-09-05.md)
adds three distinct Psalter edition controls: registry 25 entries, comparison
ledger 13 cases, physical coverage ledger 20 records. Harden and Weber–Gryson
disagree within the Hebrew-based Latin Psalter; the pilot now preserves that
edition distinction and Harden's explicit omission report. No new physical
collation, Hebrew selection, or English main-text change is claimed.

ImageGen files belong only under `images/visual_reconstructions/`. They must be
watermarked **RECONSTRUCTED — NOT MANUSCRIPT EVIDENCE** and may never be used as
input to OCR, transcription, collation, or translation.

The [4Q119 clause dossier](../../docs/4Q119_LEVITICUS_26_12_REVIEW_2026-09-05.md)
now links an actual published Greek comparison and supplied-letter check;
it adds no physical coverage or canonical change. The
[distant-row measurement dossier](../../docs/EN_GEDI_DISTANT_ROWS_CHECK_2026-09-05.md)
links the frozen acquisition protocol and expanded 288-target numeric receipt.
Only metadata/results are tracked here; its 36 additional licensed CT slices
remain private outside the repository. Numeric agreement is not letter recovery.

The subsequent [region-grounding check](../../docs/EN_GEDI_REGION_GROUNDING_2026-09-05.md)
preserves a failed fixed registration experiment and unaccepted projected
locators; no reading benchmark follows. New
[4Q24](../../docs/4Q24_LEVITICUS_2_PRIMARY_FOLLOWUP_2026-09-05.md) and
[Samuel](../../docs/SAMUEL_20_6_SOURCE_ENGLISH_FOLLOWUP_2026-09-05.md) dossiers
add actually consulted reassessment and versional/grammar evidence without
canonical changes or new independent manuscript counts.

For image-level restoration records, the existing
[`../dead_sea_scrolls/`](../dead_sea_scrolls/) registry, image-provenance, and
transcription formats remain the operational model.
