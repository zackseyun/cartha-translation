# Deuteronomy 32:8: full-record draft and publication preflight

Date: 2026-09-05. Status: **unapproved research draft, not a canonical change**.
This pass constructs a concrete full-verse candidate for joint source/English
review and exercises an actual downstream exporter. It does not adjudicate the
remaining Hebrew/Greek evidence or complete any existing promotion gate.

Later same-day update: the [reader trace and local repair](READER_DISCLOSURE_TRACE_2026-09-05.md)
supersede the missing local-note result below. Preflight v1 remains a historical
snapshot; the builder now produces [v2](../sources/textual_restoration/applications/deut32_8_preflight.v2.json).
The full critical-source schema and website-loader disclosure gaps remain open.

## Review artifacts

- [Explicit edit plan](../sources/textual_restoration/applications/deut32_8_draft_plan.v1.json)
- [Byte-exact baseline snapshot](../sources/textual_restoration/applications/deut32_8_baseline.v1.yaml)
- [Complete candidate record](../sources/textual_restoration/applications/deut32_8_candidate.v1.json)
- [Original preflight receipt](../sources/textual_restoration/applications/deut32_8_preflight.v1.json)
- [Builder](../tools/textual_restoration/build_application_draft.py) and
  [regression tests](../tests/test_application_draft.py)

The source draft is the baseline WLC verse with vowel points, accents and
source-token separators removed, plus one explicitly proposed replacement:
`בני ישראל` → `בני אלוהים`. It retains the baseline's other consonants and
final punctuation. This is a provisional editorial composite, not a complete
4Q37 transcription, a recovered vocalization or a quotation of WLC. The draft
edition label is deliberately `POB-critical-draft`. The OHB El conjecture and
contrary MT/SP/Greek controls remain separately identified in its apparatus.

The English replaces only “the sons of Israel” with “the sons of God.” Both
existing note markers remain attached, the unrelated humankind note is retained,
and the textual note is rewritten to disclose alternatives. The affected lexical
and theological rationales follow the candidate instead of still defending
Israel as the current reading. Other lexical decisions are carried forward,
not newly verified. This candidate does not settle interpretation of “sons,”
the divine designation, or the wider poetic context.

## Review provenance is not inherited approval

The baseline's `cross_check` and `revision_pass` values are preserved in draft
`review_history`, with the hash of the canonical snapshot from which they were
archived. That is **not** claimed to be the input hash of the original review:
its historical input binding remains unverified. Neither entry certifies the
candidate. The current candidate has only `cross_check.status: needs_review`
and `status: draft`, with no reused agreement score or new invented timestamp.
Original `ai_draft` data remains explicitly historical.

All six selection gates stay pending. The selection's full-verse field
is still null; materializing this draft does not fill or certify it. The
builder cannot mark approval or write canonical verse files. This is not yet
the reviewed application transaction required by the method.

## Actual integration checks

| Check | Observed result | Consequence |
|---|---|---|
| Canonical file binding | Exact pinned baseline matched before and after preflight | No canonical drift or write during this run |
| Current verse schema on baseline | Existing `status: revised` fails its draft-only enum | Pre-existing schema/lifecycle mismatch; not introduced by the candidate |
| Current verse schema on candidate | `POB-critical-draft` is not an accepted source edition | A deliberate critical-source representation is needed; do not mislabel the draft WLC to make it pass |
| Actual mobile full-book export with a one-record memory overlay | New English survives; all other exported Deuteronomy content is identical | Demonstrates bounded local export behavior, not textual correctness |
| Exported disclosure | Markers survive, but note bodies and source object are absent | Export success alone does not satisfy reader-disclosure requirements |

The export test calls `tools/export_mobile_bible.py`'s `export_book('DEU')`
first against the real files and then with only its loader result for 32:8
replaced in memory. The rest of the book is compared after restoring the
baseline verse in the draft output. It does not replace the exporter with a
mock result, write an app bundle, inspect a deployed reader, or exercise a
website/CDN path. We have not established whether another consumer supplies
notes separately. The source need not appear in every lightweight reader
payload, but an actual accessible disclosure path must be verified before
counting the publication gate complete.

The receipt pins the baseline, selection, edit plan, four relevant research
records, canonical schema, exporter and builder. It hashes the serialized
candidate and each before/after top-level component. Those hashes establish
input identity and transformation reproducibility, not manuscript accuracy or
independent approval. No new external source was consulted in this software pass.

## Reproduce

From the repository root:

```bash
.venv/bin/python tools/textual_restoration/build_application_draft.py
.venv/bin/python tools/textual_restoration/build_application_draft.py --write
.venv/bin/python -m unittest tests.test_application_draft
```

The first command only prints the receipt. The second preserves a byte-exact
baseline snapshot and regenerates two fixed JSON research outputs, never a
canonical or deployed file. A different existing baseline snapshot or symlink
output is rejected rather than overwritten. Tests cover
baseline drift, source/selection mismatch, missing metadata targets, duplicate
note markers, generated-evidence rejection, archival review boundaries and
actual export behavior. The current snapshot's schema/disclosure gaps are
explicit assertions, not claims that those gaps are desirable. Revise the
receipt and assertions deliberately when those integrations are implemented.
An exit code of zero means draft generation succeeded; `publication_ready`
remains false. It is not a successful publication-readiness check.

## Next work

1. Finish the source decision and independent source/English review using this
   full candidate alongside the unchanged baseline and serious alternatives.
2. Design a production critical-source representation with unit-level origin,
   normalization/vocalization policy and review bindings. Do not merely add a
   permissive edition string or treat a draft as an approved source corpus.
3. Trace actual website/mobile consumers and verify how notes and source
   provenance reach readers; then implement and test the missing path.
4. Implement a reviewed, hash-bound application transaction and before/after
   receipts, including stale-review handling and synchronized exports. Research
   tests passing must never be used as authorization or editorial approval.

The [central log](TEXTUAL_RESTORATION_RESEARCH_LOG.md) records this pass. No
commit, About integration, deployment, main-text change or image recovery occurred.
