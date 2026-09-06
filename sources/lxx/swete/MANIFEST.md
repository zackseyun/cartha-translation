# Swete LXX — Source File Manifest

The full scanned PDFs are too large to commit directly to the git
repository (~155 MB total). This manifest points to the authoritative
copies on Internet Archive with SHA-256 hashes so anyone can verify
they are working with the exact files we transcribed from.

## Upstream location

Internet Archive item: https://archive.org/details/theoldtestamenti03swetuoft_202003
Title: *The Septuagint (LXX) — Henry Swete*
Rights statement: the archive item identifies public-domain material.
Edition correction, 2026-09-05: volume III's title/imprint identifies the third
edition (1905), not the former blanket 1909–1930 date. Volumes I/II were not
newly inspected in this pass; this is not a new rights-policy assessment.

## File hashes (SHA-256)

| File | Size | SHA-256 | Archive.org path |
|---|---|---|---|
| `oldtestamentingr01swet.pdf` (Vol. I) | 49,145,251 B | `ed4aeb80dcb83dffaffae8d36b3c8062f76f1cbe21e07583ad04e1526b8eed50` | `theoldtestamenti03swetuoft_202003/oldtestamentingr01swet.pdf` |
| `oldtestamentingr02swet.pdf` (Vol. II) | 48,369,054 B | `945c5b15bf0f9dfc93890b28ee5b66a388acbf4597f1f2be5430ac6cba9c30b0` | `theoldtestamenti03swetuoft_202003/oldtestamentingr02swet.pdf` |
| `theoldtestamenti03swetuoft.pdf` (Vol. III) | 57,077,650 B | `5f0bfffabf0e588fd32e15bdb24b027872616da219e7f02da3dbdc115cf97d85` | `theoldtestamenti03swetuoft_202003/theoldtestamenti03swetuoft.pdf` |

Volume III was reacquired and its hash verified on 2026-09-05: 932 PDF pages;
Isaiah 54:11–13 is on printed p. 202, one-based PDF p. 226. This mapping is
specific to this exact PDF, not a guessed Archive image-service page index.
The [bounded receipt](../../textual_restoration/discovery/isaiah54_swete_review.v1.json)
records visually consulted pages and limits. Full source PDFs stay outside Git.

## Fetch instructions

To obtain local copies of the source PDFs, run from this directory:

```bash
curl -sL -o swete_vol1.pdf "https://archive.org/download/theoldtestamenti03swetuoft_202003/oldtestamentingr01swet.pdf"
curl -sL -o swete_vol2.pdf "https://archive.org/download/theoldtestamenti03swetuoft_202003/oldtestamentingr02swet.pdf"
curl -sL -o swete_vol3.pdf "https://archive.org/download/theoldtestamenti03swetuoft_202003/theoldtestamenti03swetuoft.pdf"

# Verify
shasum -a 256 swete_vol*.pdf
```

The expected hashes are above. If any differ, do not use the file.

## Per-page image access

Individual page scans are available via the archive.org download
endpoint. Pattern:

```
https://archive.org/download/theoldtestamenti03swetuoft_202003/page/n{PAGE}_w{WIDTH}.jpg
```

For example: `.../page/n50_w1500.jpg` for page index 50 at 1500px wide.

## Per-book page ranges (to be populated as we transcribe)

As pages are transcribed, the mapping from scan page → book → chapter →
verse is recorded in `transcribed/page_index.json`.
