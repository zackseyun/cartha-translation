# Psalms of Solomon — scope and source strategy

This document covers the Cartha Open Bible's dedicated track for the
**Psalms of Solomon** — an 18-psalm Greek pseudepigraphal collection
preserved in Swete vol. III and already adjacent to our existing Swete
transcription pipeline.

It complements:

- [`EXTRA_CANONICAL.md`](EXTRA_CANONICAL.md) — the broader roadmap for
  extra-canonical texts
- [`REFERENCE_SOURCES.md`](REFERENCE_SOURCES.md) — the three-zone
  source policy
- [`sources/lxx/swete/README.md`](sources/lxx/swete/README.md) — the
  underlying Swete source corpus

> **Status: source-transcription phase.** The full Swete page span for
> Psalms of Solomon has now been transcribed page-by-page from vol. III.
> The next task is book-specific parsing / verse structuring, not a new
> OCR pipeline.

## Why Psalms of Solomon

1. **It is the cheapest high-value extra-canonical Greek book in the
   roadmap.** Unlike 2 Esdras, Enoch, or Jubilees, it does **not**
   require a new Latin, Ethiopic, or Coptic pipeline. It sits directly
   inside the existing Swete transcription workflow.
2. **It is historically important Second Temple Jewish literature.**
   The collection is a major witness to late pre-Christian Jewish hope,
   repentance language, anti-Hasmonean critique, and messianic
   expectation.
3. **Psalm 17 especially matters for messianic studies.** It is one of
   the clearest pre-Christian Jewish royal-messianic texts and belongs
   in any transparent broader-canon project.
4. **Open modern access is thin.** Scholarly translations exist, but an
   auditable CC-BY 4.0 source-grounded English version is still a real
   contribution.

## Textual situation

- **Original language:** almost certainly Hebrew
- **Primary surviving witness:** Greek
- **Secondary witness:** Syriac fragments / Syriac transmission
- **Collection size:** 18 psalms

For COB's first release, the translation anchor is the **Greek** text
as printed in Swete vol. III. Syriac can be introduced later as
additional textual-critical context, but it is not required to begin
translation work.

## Swete source coverage

The Swete vol. III appendix contains the collection at:

- **Volume:** III
- **Scan pages:** **788–810**
- **Running head:** `ΨΑΛΜΟΙ ΣΟΛΟΜΩΝΤΟΣ`

Important boundary note:

- **p. 788** begins Psalm 1
- **p. 810** ends Psalm 18
- **p. 811** is the transition away from Psalms of Solomon and into the
  Enoch appendix material, so it is **not** part of the book's source
  range for COB

## Source editions

### Zone 1 (vendored / transcribed)

| Edition | Role | Status |
|---|---|---|
| Swete, *The Old Testament in Greek*, vol. III | **Primary Greek source** | Full page span transcribed (`vol3_p0788`–`vol3_p0810`) |

### Zone 2 (consult, not reproduced)

| Edition | Role |
|---|---|
| Ryle & James, *The Psalms of the Pharisees, commonly called the Psalms of Solomon* (1891) | PD Greek + English scholarly edition; useful for verse structure cross-check and introduction |
| Charlesworth / OTP translation | Modern interpretive context |
| Later critical Syriac/Greek studies | Consult for textual cruxes once verse parsing is stable |

## Why this is a different kind of task from 2 Esdras / Enoch

Psalms of Solomon is the opposite of the harder extra-canonical tracks:

- **No new OCR backend**
- **No new script**
- **No new source-family architecture**
- **No multi-witness daughter-translation reconstruction problem**

That makes the work sequence:

1. finish Swete transcription ✅
2. build a book-specific parser
3. assemble a book-specific prompt builder
4. draft + revise

## Planned components

| Component | Status | Purpose |
|---|---|---|
| `sources/lxx/swete/transcribed/vol3_p0788`–`vol3_p0810` | ✓ | Full per-page Greek source coverage |
| `tools/psalms_of_solomon.py` | ✓ scaffold | Page-range + coverage helper for the dedicated book track |
| book-specific parser | ⏳ pending | Extract Psalm / verse structure cleanly from the page corpus |
| prompt builder | ⏳ pending | Assemble the Psalms of Solomon translation prompt |

## Immediate next steps

1. **Stabilize the page map** in `page_index.json` and related docs
2. **Build the parser** for Psalms 1–18 from the Swete page corpus
3. **Cross-check verse structure** against Ryle & James 1891
4. **Begin drafting** once the verse skeleton is stable

## Why this is worth prioritizing now

Among the extra-canonical books currently on the roadmap, Psalms of
Solomon offers one of the best effort-to-value ratios:

- the source is Greek
- the source is public domain
- the source already sits inside our Swete stack
- the text is historically rich
- the remaining work is mostly **structuring and translation**, not
  source acquisition

That makes it an ideal focused follow-on extra-canonical target.
