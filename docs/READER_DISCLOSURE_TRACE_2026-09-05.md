# Reader disclosure: local export repaired, web-loader gap identified

Date: 2026-09-05. The local canonical OT/NT exporter now preserves referenced
footnote bodies. No Bible wording, research selection, reader application or
deployment was changed. The publication gate remains pending.

The [machine receipt](../sources/textual_restoration/applications/reader_disclosure_review.v1.json)
pins six consulted source files in three related repositories and distinguishes
static inspection from executed probes. Repository names and file-relative
paths identify these sources without embedding private workspace paths.

## What the actual paths do

| Path | Evidence | Result |
|---|---|---|
| POB local `export_mobile_bible.py` | Executed before/after full-book Deuteronomy export | Previously omitted notes; now carries referenced note bodies and optional reasons |
| `CarthaCdkService` publisher | Inspected extraction and compile code | Already retains referenced marker/text pairs; no publisher execution claimed |
| Native mobile parser and rendering | Inspected typed parsing, runtime normalization, fallback loading and note display | Has paths for note bodies and optional reasons; not a device/render test |
| Website renderer | Inspected marker lookup and note-rendering helpers | Can display supplied notes |
| Website POB loader | Inspected caller and executed the isolated actual filter block | Removes markers and deletes note arrays before rendering |

The final row corrects the tempting inference that renderer support alone means
notes reach readers. The web code explicitly selects its stripping branch for
`pob`; executing that block with the unchanged research candidate reduced two
notes to zero and removed their markers. The identical input with the `kjv`
identifier retained both. That second case is only a control for the conditional
branch, not a claim to have changed or tested KJV translation content.

This execution uses the exact file's lines 213-251 in an isolated JavaScript
context. It is not a copied reimplementation, but neither is it a full loader,
React or deployed-reader test. The caller at 252-261 was inspected separately.
The website's explicit translation-specific policy may reflect an earlier
design choice; this pass does not infer its intent or alter it across multiple
translations. A reader-disclosure change there requires a separate scoped
implementation and UI verification.

## Local repair

[`reader_footnotes`](../tools/export_mobile_bible.py) filters note bodies to
markers actually referenced in the exported text, normalizes a surrounding
marker bracket like the publisher, preserves the optional reason accepted by
both clients, and leaves source text and translation strings untouched.
It does not manufacture notes for manuscript brackets or publish unreferenced
archival rationale. Malformed/empty note bodies are omitted; this is not a
general corpus cleanup or a resolution of duplicate/conflicting notes.

The ordinary canonical book exporter now uses the same verse helper as Psalms,
so this fix applies to canonical OT and NT paths, including Psalm headers.
Separate deuterocanonical/extra-canonical export paths were not changed or
certified in this pass. No new consumer JSON shape was invented: the existing
`footnotes: [{marker, text, reason?}]` structure is used. No full source object
was added to the lightweight export.

The original [failed preflight v1](../sources/textual_restoration/applications/deut32_8_preflight.v1.json)
is preserved. [Preflight v2](../sources/textual_restoration/applications/deut32_8_preflight.v2.json)
records the repaired actual export, with the same candidate hash and baseline.
All other exported Deuteronomy content remains identical between baseline and
one-record-overlay runs of the **new** exporter. That does not mean the new
exporter is byte-identical to its earlier output: it now adds existing notes to
other verses as intended. The source-schema gap and all review gates remain.

## Verification and reproduction

```bash
.venv/bin/python tools/textual_restoration/build_application_draft.py --write
.venv/bin/python -m unittest tests.test_reader_footnote_export tests.test_application_draft
node tools/textual_restoration/probe_web_note_filter.mjs PATH_TO_WEB_BIBLE_DATA_JS sources/textual_restoration/applications/deut32_8_candidate.v1.json
```

The last command requires Node and an explicit path to the inspected website
file. It only reads those files and prints a receipt. Its recorded input and
extracted-block hashes must match before treating the output as reproduction
of this dated observation. No AWS invocation, publisher script, auth operation,
network fetch or application mutation is part of the probe.

Tests cover referenced/background/malformed notes, marker normalization,
non-mutation, absent-note compatibility, ordinary OT and NT book paths, Psalm
headers and all thirteen actual comparison baselines. The real full-book
candidate probe still runs, and the old failing receipt is explicitly retained
as historical evidence. Passing these checks does not approve a source reading.

Next: return to the outstanding manuscript/source adjudication; before an
approved textual change reaches readers, resolve the web stripping policy,
verify its actual display, finalize critical-source provenance, and complete
the hash-bound application transaction. This local export fix alone cannot
close that publication gate. See the [research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md).
