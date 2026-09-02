# Initial OCR feasibility pass — 2026-09-02

## Inputs

- Four Library of Congress TIFF masters listed and hashed in
  `registry.v1.json` (two views each of 1QM and 1QpHab).
- Tesseract 5.5.2 with the official `tessdata_fast` modern Hebrew model.
- Whole-image sparse-text mode (`--psm 11`) as a deliberately basic baseline.
- Deterministic grayscale/autocontrast derivatives produced by
  `tools/dss/enhance_images.py`.

## Result

The pass emitted Hebrew-looking character strings for three photographs and no
usable text for one, but the strings were inconsistent between the color and
black-and-white views and included layout artifacts, modern glyph confusions,
punctuation noise, and non-words. The model is not trained for this ancient
scribal hand, and the whole-slide photographs contain borders, labels, missing
parchment, and strong background contrast.

**Accepted words: 0. Restored words: 0.** Nothing from this pass may enter a
diplomatic transcription, comparison apparatus, or translation.

## What the pass established

- Image retrieval and SHA verification work.
- Full-resolution masters are materially better inputs than web previews.
- Deterministic contrast aids can be generated without inventing strokes.
- Generic modern-Hebrew OCR is not a defensible transcription engine for these
  photographs.

## Next gate

Crop and identify exact columns/lines, then run two independent vision passes
that are prompted for ancient Hebrew/Aramaic diplomatic transcription. Freeze
both outputs before reconciliation. A qualified paleographer must approve any
word, and supplied letters remain separately encoded as restoration candidates.

This failed baseline is retained because rejecting fluent-looking garbage is a
core requirement of the project.
