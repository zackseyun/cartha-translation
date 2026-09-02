# Old and New Testament Textual Restoration Priorities

## Decision

The People's Open Bible will attempt this work independently with **Codex as
the transcription, collation, and textual-reasoning system**. The project will
not depend on commissioning new human diplomatic transcriptions or
paleographic review.

ImageGen may be used after the textual work to create a readable visual
reconstruction, but an ImageGen output is never manuscript evidence. It must
be visibly labeled, stored outside the evidence lanes, and excluded from OCR,
transcription, collation, confidence scoring, and translation decisions.

The target is the **earliest attainable text supported by surviving evidence**,
not a claim that we have recovered a lost autograph. The project keeps four
things separate:

1. ink visible in an archival image;
2. deterministic enhancement of that image;
3. Codex's text-restoration hypothesis based on visible traces and comparison
   witnesses; and
4. ImageGen's non-evidentiary visual reconstruction.

## No-human operating standard

Two Codex passes are useful replication, but they are not two independent
historical witnesses. A reading receives one of these statuses:

| Status | Meaning | May change the POB main text? |
|---|---|---|
| `machine-observed` | Codex consistently identifies visible strokes in multiple deterministic views of the same archival image. | Only when the reading is not materially disputed. |
| `machine-corroborated` | The visible reading also agrees with an independent manuscript, open transcription, critical apparatus, or ancient version whose relationship is documented. | Yes, after the comparison record and rationale are complete. |
| `machine-hypothesis` | A plausible completion based on spacing, grammar, orthography, or a parallel, but the letters are not fully visible. | No. It remains in the apparatus or research record. |
| `lost` | The material is physically absent or no reading survives. | No. Missing text is never presented as recovered ink. |
| `visual-reconstruction` | ImageGen rendering made from an already documented reading or hypothesis. | Never. Display only. |

A novel reading inferred from one damaged image must remain
`machine-hypothesis` unless an independent source corroborates it. Confidence
scores do not override this rule.

## Restoration priority queue

### Priority 0 — Build the comparison system first

This is the highest priority because the current canonical sources are WLC/UHB
for the Old Testament and SBLGNT for the New Testament. Restoring isolated
images without a full comparison apparatus would not reliably improve the
translation.

Create:

- a unified witness registry with shelfmark, language, date, passage coverage,
  textual role, image provenance, rights, and hashes;
- image-addressable diplomatic transcription records;
- normalized Hebrew, Aramaic, and Greek layers mapped back to the diplomatic
  text;
- passage-level alignments and variation units;
- a human-readable and machine-readable critical apparatus;
- a decision record connecting every accepted reading to the POB verse YAML;
- a separate ImageGen visual-reconstruction manifest.

### Priority 1 — Direct Hebrew and Aramaic gaps and major OT variants

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Qumran Tobit 4Q196–4Q200** | Fragmentation, fading, edge loss, and mixed Aramaic/Hebrew witnesses. | Fragment images and metadata; Codex diplomatic text; Greek long and short recensions; Old Latin controls; overlap map by Tobit reference. | Aramaic/Hebrew fragment corpus, ranked restoration candidates, and a Tobit variation apparatus. |
| **Hebrew Ben Sira: Geniza MSS A–F, Masada, and Qumran** | Torn and stained leaves, uncertain letters, scattered witnesses, and differing Hebrew forms. | Existing Geniza photographs and open transcriptions; Masada and Qumran consultation records; Swete/Göttingen Greek; Syriac control; reference alignment. | Witness-separated Hebrew corpus and a verse-level Hebrew/Greek/Syriac apparatus. |
| **4QSam-a** | Fragmentary Hebrew that sometimes represents an older or different textual form. | Qumran image/transcription layer; WLC/UHB; Septuagint/Old Greek; relevant Masoretic codices. | Samuel variation units classified as spelling, copying, expansion, omission, or literary edition. |
| **4QJer-b and 4QJer-d** | Fragmentation plus shorter/longer textual forms and different ordering. | Qumran Hebrew; WLC/UHB; Old Greek Jeremiah; later Hebrew controls. | Jeremiah literary-form alignment without forcing every witness into MT order. |
| **4QDeut-q/n and 4QpaleoExod-m** | Fragmentation, paleo-Hebrew script, harmonization, and overlap with Samaritan/Greek readings. | Qumran witnesses; WLC/UHB; Samaritan Pentateuch; Old Greek; Targum/Peshitta controls where useful. | Pentateuchal variant apparatus with textual-family classification. |
| **11QPs-a / Hebrew Psalm 151** | Fragment order, different psalm sequence, lacunae, and non-Masoretic composition evidence. | Scroll text; WLC Psalms; Swete/Old Greek; other Qumran Psalms witnesses. | Psalms order/composition map and direct Hebrew Psalm 151 comparison. |

### Priority 2 — High-value Greek palimpsest and papyrus restoration

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Codex Ephraemi Rescriptus, OT and NT** | Erased biblical undertext beneath later writing, incomplete survival, and difficult layer separation. | Gallica color images; deterministic channel/rotation/contrast derivatives; existing editions as non-copying controls; Vaticanus, Sinaiticus, Alexandrinus, papyri, and current critical apparatus. | Line-addressable Greek undertext hypotheses, with observed and supplied characters kept separate. |
| **P45** | Abraded and highly fragmentary Gospel/Acts papyrus. | Images from all holding institutions; existing transcriptions; ECM/UBS apparatus; major Gospel and Acts witnesses. | Unified virtual-fragment registry and Greek variation units. |
| **P46** | Damaged edges, missing leaves, corrections, and distributed holdings. | Dublin/Michigan images and metadata; independent existing transcriptions; Pauline witnesses and current ECM preparation/critical apparatus. | Virtual codex order, hand/correction layers, and edge-reading candidates. |
| **P66** | Fragmentation and extensive scribal/self-correction layers. | Images, hand-separated transcription, P75/Vaticanus/Sinaiticus, and Johannine critical apparatus. | First-hand and correction-layer apparatus rather than a flattened consensus text. |
| **P75** | Localized edge loss and fragmentary Gospel coverage. | Vatican images; existing diplomatic text; P66 and major codices; current Luke/John apparatus. | Targeted verification of consequential readings; no unnecessary wholesale restoration. |
| **Oxyrhynchus NT fragments** | Scattered ownership, variable images, abrasion, and inconsistent identifiers. | Gregory-Aland-to-shelfmark registry; IIIF/archive links; passage mappings; current apparatus. | Searchable fragment registry and prioritized unresolved reading list. |

### Priority 3 — Major codex layers and the current gallery problem

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Codex Vaticanus, OT and NT** | Original ink, later retracing, corrections, and marginal signs need to be distinguished. | Vatican IIIF images and metadata; targeted deterministic derivatives; Sinaiticus/Alexandrinus; Old Greek and NT critical apparatus. | Layer-aware diplomatic records and a list of readings where the earlier hand can be distinguished. |
| **Codex Sinaiticus, OT and NT** | Numerous correctors and erasures; POB currently has a printed Tischendorf facsimile rather than manuscript photographs in the gallery. | Official standard/raking/multispectral images; official linked transcription; hand/corrector metadata; other major codices. | Replace or relabel the gallery source and import only unresolved correction-layer units for new analysis. |
| **Aleppo Codex** | Missing leaves and localized torn or faded surviving areas. Lost leaves cannot be recovered photographically. | Surviving images; recovered fragments; historical notes/descriptions; Leningrad and Sassoon comparisons. | Diplomatic surviving text plus clearly labeled documentary reconstruction of missing Masoretic information. |
| **Codex Sassoon 1053 and Leningrad** | Primarily collation, Masorah, vocalization, and localized-damage questions rather than large-scale physical recovery. | High-resolution images or lawful transcriptions; Aleppo; WLC/UHB; BHQ/BHS apparatus. | Masoretic comparison layer and transcription-error audit of the current POB base. |

### Priority 4 — Ancient versional witnesses

These can preserve early readings, but they are translations. Codex must restore
the Latin or Syriac witness first and must not silently turn it into certain
Greek.

| Target | Restoration problem | Comparison sources to create or assemble | Intended output |
|---|---|---|---|
| **Codex Bobiensis** | Fire, damp, fragmentation, shrinkage, and old restoration. | Modern color images; older photographs/facsimiles; Old Latin comparison; Greek Mark/Matthew variation units. | Fresh Latin diplomatic layer and constrained Greek-reading implications. |
| **Codex Vercellensis Evangeliorum** | Severe deterioration and faded/erased text; multispectral work already exists. | Existing color/MSI derivatives if accessible; Old Latin witnesses; Greek Gospel apparatus. | Machine re-evaluation of recovered Latin letters without repeating imaging unnecessarily. |
| **Sinai Syriac 30** | Palimpsest undertext already substantially recovered by spectral imaging. | Published spectral images; existing Syriac editions; Curetonian Syriac; Greek Gospel apparatus. | New machine-readable Syriac diplomatic comparison, not a fresh-image-first project. |
| **Other Old Latin, Syriac, Coptic, Armenian, Georgian, and Geʿez witnesses** | Translation ambiguity and uneven digitization. | Book-specific version corpora and explicit translation-character profiles. | Targeted controls only where they can distinguish competing Hebrew/Aramaic/Greek readings. |

### Priority 5 — Lower-yield or tightly bounded targets

- **P52:** verify visible strokes and margins, but do not attempt to recreate its
  lost context.
- **Codex Washingtonianus:** target only consequential faded or corrected
  readings.
- **Well-preserved Leningrad passages:** use as transcription controls rather
  than image-restoration targets.
- **Physically missing Aleppo leaves:** documentary reconstruction only.
- **Sinaiticus passages already securely transcribed from official images:** no
  duplicate restoration work.

## Comparison-source packages to create

The source layout should extend the existing
`sources/dead_sea_scrolls/` evidence model rather than create an incompatible
second system:

```text
sources/textual_restoration/
├── registry.v1.json
├── images/
│   ├── original/                 # lawful archival pixels only
│   ├── derived/                  # deterministic Codex aids + sidecars
│   └── visual_reconstructions/   # ImageGen, watermarked and excluded
├── transcriptions/
│   ├── diplomatic/              # line/image-addressable readings
│   ├── normalized/              # mapped Hebrew/Aramaic/Greek text
│   └── passes/                  # frozen blinded Codex outputs
├── comparisons/
│   ├── ot_masoretic/
│   ├── ot_judean_desert/
│   ├── ot_old_greek/
│   ├── nt_greek/
│   └── ancient_versions/
├── alignments/                      # passage and fragment mappings
├── apparatus/                       # machine + reader-facing variants
├── restoration_candidates/          # never merged into observed ink
└── decisions/                       # POB adoption/non-adoption records
```

Each comparison package must say whether its source is:

- a direct Hebrew, Aramaic, or Greek witness;
- a daughter translation;
- a modern diplomatic transcription;
- a critical edition or apparatus;
- an editorial reconstruction; or
- an ImageGen visual reconstruction.

## Codex execution loop

For each target:

1. Register the object, image, rights, hash, passage coverage, and comparison
   witnesses.
2. Preserve the archival image unchanged.
3. Generate only deterministic evidence derivatives: crop, registration,
   grayscale, contrast, channel separation, threshold, denoise, and permitted
   spectral combinations.
4. Run at least two blinded Codex transcription passes over different useful
   derivatives and freeze both outputs.
5. Reconcile at glyph level while preserving disagreements.
6. Compare against independent manuscripts, open transcriptions, critical
   apparatuses, and ancient versions.
7. Assign `machine-observed`, `machine-corroborated`, `machine-hypothesis`, or
   `lost` at token level.
8. Emit the apparatus and a POB decision record. Never auto-promote a novel,
   uncorroborated restoration into the main text.
9. Optionally ask ImageGen to create a complete-looking educational image from
   the already documented text. Watermark it **RECONSTRUCTED — NOT MANUSCRIPT
   EVIDENCE**, store the prompt and source IDs, and prevent the image from
   re-entering step 3.

## Completion standard

A target is complete when its source provenance, image regions, frozen Codex
passes, diplomatic/normalized text, comparison sources, variant apparatus,
uncertainty statuses, and POB decision are stored and validated. ImageGen output
is optional and never raises textual confidence.

Without human review, the public claim must remain **machine-restored and
source-compared**, not human-verified or definitive. The project should favor
an explicit unresolved reading over a fluent invented one.
