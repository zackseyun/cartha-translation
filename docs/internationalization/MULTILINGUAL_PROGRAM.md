# POB multilingual translation program

## Scope

The program currently tracks 33 unique languages: English as the source POB,
Spanish and Korean as existing corpora entering independent revision, and 30
new translation projects. Duplicate requests (notably Polish and several of the
priority languages) are represented once.

The machine-readable language and register definitions live in
`config/multilingual_languages.yaml`.

## Method

This is not a mechanical English localization project.

1. **Source-facing draft — GPT-5.6 Sol on Azure.** Each record receives the
   original-language source packet, the English POB rendering, lexical and
   theological decisions, and recent revision history. The original source is
   primary; English is consult-only.
2. **Independent revision — GPT-5.6 Terra on Azure.** A separate model checks
   source fidelity, modern naturalness, register, names, theological terms, and
   footnote anchors. Safe revisions are applied and preserved in an audit trail.
3. **Human calibration gates.** A language begins with a small shared verse set.
   Native readers should approve its register and glossary before canon-wide
   generation. High-risk or disputed records are marked for human review rather
   than silently resolved.
4. **No named-interpreter doctrine.** The translation preserves source ambiguity
   and POB decisions but does not import denominational or named-interpreter
   distinctives.
5. **Azure only.** `tools/multilingual_pipeline.py` has no Vertex or Gemini path.

## Current phases

- **Existing source:** English.
- **Revision:** Spanish and Korean.
- **Calibration pilot (30 languages):** Portuguese, Mandarin Chinese, French, Russian,
  Swahili, Tagalog, Indonesian, Hindi, Arabic, Tamil, Telugu, Yoruba, Igbo,
  Amharic, Vietnamese, Romanian, Polish, Ukrainian, Italian, Malayalam,
  Kannada, Marathi, Bengali, Japanese, Thai, Lingala, Zulu, Hausa, Nepali, and
  Burmese.

## Commands

```bash
# Show all projects and generated/reviewed record counts
python3 tools/multilingual_pipeline.py status

# Draft + independently review the first shared calibration verse in all new languages
python3 tools/multilingual_pipeline.py pilot --language all --limit-verses 1 --concurrency 8

# Expand the calibration set after inspection
python3 tools/multilingual_pipeline.py pilot --language all --limit-verses 3 --concurrency 8

# Begin/resume a bounded corpus wave after a language passes calibration
python3 tools/multilingual_pipeline.py wave --language pt --limit-records 100 --concurrency 8

# Validate every generated pilot record
python3 tools/multilingual_pipeline.py validate --language all
```

Scaling beyond the pilot requires a recorded native-speaker/register decision
for the language and a bounded Azure token budget. Corpus-wide waves should be
resumable and should never overwrite reviewed records unless `--force` is used
deliberately.

## First calibration checkpoint — 2026-07-12

- All 30 new language projects produced and independently reviewed Genesis 1:1.
- Portuguese also completed a reviewed whole-library wave probe on 1 Esdras 1:1.
- Every resulting YAML record passed structural and footnote-anchor validation.
- Spanish completed 304 GPT-5.6 Terra reviews in this checkpoint after repair of
  malformed legacy review YAML. 281 are publication-ready; 23 remain explicitly
  blocked for footnote-anchor/human review rather than being applied unsafely.
- Korean completed 110 GPT-5.6 Terra revisions, all applied and validated, with
  safe per-record locking for resumable parallel waves.
- The source tree currently contains 43,402 records across the full Cartha
  library. New-language waves are designed to target this entire source tree,
  not only the 66-book Protestant canon.
