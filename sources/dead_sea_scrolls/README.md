# Dead Sea Scrolls source program

This directory is the source landing zone for the
[POB Dead Sea Scrolls and Ancient Witness Project](../../docs/DSS_TEXTUAL_WITNESS_PROJECT.md).
It separates evidence, hypotheses, and teaching media so that a visually
plausible reconstruction can never masquerade as manuscript evidence.

## Contents

- `registry.v1.json` — scroll targets, manuscript IDs, rights gates, URLs,
  local paths, and SHA-256 hashes.
- `comparison_witnesses.v1.json` — Hebrew, Aramaic, Greek, and daughter-version
  witnesses to add to the comparison program.
- `images/original/` — small, lawfully redistributable pilot images exactly as
  downloaded.
- `images/masters/` — full-resolution rehydratable working files; intentionally
  ignored by Git because the four-pilot seed is about 145 MB.
- `images/derived/` — deterministic transcription aids and provenance JSON.
- `transcriptions/` — image-addressable diplomatic records. Empty or queued
  records are preferable to guessed Hebrew.

## Rights status

The four included preview images are from the Library of Congress G. Eric and
Edith Matson Photograph Collection. Their item records state **“No known
restrictions on publication.”** That is not the same as a warranty or a claim
that the LOC owns every underlying right; downstream users remain responsible
for their own rights assessment. Each registry entry links to the item record.

The Israel Antiquities Authority terms checked on 2026-09-02 state that the
website, text, and images are copyrighted and may not be reproduced, displayed,
modified, or distributed beyond a single private-use copy without prior written
permission. Therefore IAA images are **not** downloaded or vendored here.

Creating an AI-generated look-alike would not solve that licensing problem and
could hallucinate letters. Any future educational reconstruction must be stored
outside the evidence lanes, labeled on the pixels, and excluded from OCR,
transcription, collation, and translation.

## Commands

```bash
# Validate registry, local files, and rights gates.
python3 tools/dss/validate_project.py

# Rehydrate or verify the tracked preview seed.
python3 tools/dss/fetch_images.py --quality preview

# Rehydrate full LOC TIFF masters (large and gitignored).
python3 tools/dss/fetch_images.py --quality master

# Create reversible, non-generative transcription views.
python3 tools/dss/enhance_images.py
```

Every derivative receives a JSON sidecar containing the exact input/output
hashes and parameters. A transcription must conform to
`schemas/dss-transcription.schema.json` and must map lines or tokens back to an
image region.
