# Jubilees chapter 1 — run-to-run OCR consistency pilot

Generated 2026-04-22, two independent Gemini 2.5 Pro plaintext-mode
OCR runs on Charles 1895 Ethiopic PDF page 37 (Jubilees chapter 1
opening). No masked_superscripts preprocessing.

## Purpose

As the only PD Ge'ez Jubilees critical edition, Charles 1895 cannot
be cross-validated against an independent second Ge'ez edition (no
such edition exists; Dillmann 1874 is German, Beta maṣāḥǝft does
not include Jubilees, VanderKam 1989 is Zone 2). In the absence of a
separate-source hand-truth benchmark, run-to-run consistency is the
cheapest realistic quality signal: if the OCR produces the same
output on two independent runs, it's at least internally stable. If
it produces materially different output, the OCR is not reliable
enough to ship without human review.

## Inputs

- Same PDF, same page, same model, same prompt, same DPI.
- Different sampling runs (no temperature=0 setting).
- Output files:
  - Run 1: `sources/jubilees/ethiopic/transcribed/charles_1895/pilot_ch01/charles_1895_ethiopic_p0037.txt`
  - Run 2: `sources/jubilees/ethiopic/transcribed/charles_1895/pilot_ch01_run2/charles_1895_ethiopic_p0037.txt`

## Quantitative result

| Metric | Value |
|---|---:|
| Run 1 length | 701 characters |
| Run 2 length | 835 characters |
| Raw Levenshtein distance | 438 |
| Character-level similarity | **~47.5%** |
| Ge'ez-letter-only Levenshtein | 384 over 687 |
| Ge'ez-letter-only similarity | **~44.1%** |
| Self-reported model confidence on both runs | "high" / finish=STOP |

The model's own confidence rating does NOT match observed run-to-run
stability.

## Qualitative diff — what actually differs

Both runs correctly identify the book title `መጽሐፈ፡ ኩፋሌ።` (Mashafa
Kufale) and produce fluent Ge'ez output. The structural differences:

**Run 1** — emits a single block starting with verse numeral `፩`:

> ፩ ዝንቱ፡ ነገረ፡ ክፍለ፡ መዋዕል፡ ወክፍለ፡ ዓመታት፡ በሳብዓተ፡ ሳምንታት፡ ለዓመት፡
> በኢዮቤልዮ፡ ለእለ፡ ተረስተው...

**Run 2** — emits an unnumbered prologue first, then starts verse
numbering at `፩` with a different opening phrase:

> ዝንቱ፡ ነገረ፡ ክፍለተ፡ መዋዕል፡ ወክፍለተ፡ ዓመታት፡ ለክፍለተ፡ አእላፋቲሆሙ፡ ...
> [unnumbered prologue paragraph]
>
> ፩ ወኮነ፡ በዓመታ፡ በሳብእታ፡ በወርኀ፡ በሳልሱ፡ በ፲ወ፮ ...

**Run 2 matches the actual structure of Charles 1895.** Charles's
edition (and all critical editions since Dillmann 1850) prints
Jubilees with an **unnumbered prologue** followed by chapter 1
starting with `ወኮነ` ("And it came to pass..."). Run 1 therefore
committed two errors simultaneously:

1. Merged the unnumbered prologue with verse 1 text.
2. Inserted the Ge'ez numeral `፩` at the top of the prologue, where
   there is no verse number in the source.

A reader comparing Run 1 against Charles 1902 English would notice
the mismatch immediately, but the single-run pipeline output did
not flag it.

## Implication for Jubilees production readiness

- **Spot-checking alone is insufficient** for Ge'ez OCR. Our earlier
  "Jubilees ch 1 pilot looks publication-grade" assessment was
  overconfident — spot-check catches fluency errors, not structural
  errors like verse-boundary misplacement.
- **Jubilees is subject to the same benchmark gate as Enoch.** We
  need either a hand-truth set to measure accuracy, or N-run
  consensus methodology, before scaling Charles 1895 OCR to
  production.

## Recommended next steps

Two tracks, both small but necessary:

1. **Hand-truth benchmark**: produce a scholarly hand-transcription
   of Jubilees 1:1-5 (the same verse scope Enoch uses) against
   Charles 1895 p37. One scholarly pass, ~15-20 Ge'ez words per
   verse, perhaps 2-3 hours of focused reading. This becomes the
   measurement anchor for all future Jubilees OCR methods.

2. **N-run consensus method**: run the same OCR 3 times, compute
   consensus output, measure consensus stability. If 3-run consensus
   gets to ≥85% character agreement across runs, the pipeline is
   stable enough to scale with a review pass. If it doesn't,
   hand-truth validation becomes mandatory.

Both tracks can run in parallel with Phase 11 (Enoch) drafting
preparation.

## What this means for timeline

The earlier timeline ("Jubilees 4-6 weeks once Phase 11 establishes
shared Ethiopic tooling") stands, but adds a **benchmark gate
before Phase 12b full-book OCR**. Skipping that gate ships a
Jubilees text with silent verse-numbering errors. Including it adds
1-2 days.

## Track B (Rönsch Latin fragments) finding

Independent investigation of the Dillmann/Rönsch 1874 composite
volume for the "Rönsch Latin fragments" identified that those
fragments are **not preserved as a continuous Latin critical edition
in this volume**. They appear as Latin lemmata (italicized verse
keywords) embedded in chapter-by-chapter German commentary
(sections XXXIX through XLII visible in the 156-160 printed-page
range). A separate continuous Latin text would need to come from
another source (direct MS publication or a later Rönsch edition),
which would need its own source-acquisition pass.

For translation purposes, the Latin lemmata in the German
commentary are still usable as Zone 1 secondary witness at the
per-verse level, via a mixed-language OCR pass over the commentary
section. That's a separate pipeline task; not in scope for this
benchmark report.
