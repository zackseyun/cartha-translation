# Provisionally reviewed POB Hebrew critical sources

This directory begins a **partial editorial source corpus**, not a replacement
for WLC and not a claim of recovered autographs. Currently it contains only
[Isaiah 53:11](isaiah/053/011.json). Its selected Hebrew has independent AI
editorial approval. Its exact full-verse candidate has now been applied to the
canonical repository YAML, including English "he will see light" and the
uncertainty note. Downstream reader release has not been verified.

Each record retains the full source text, contrary apparatus, composition
disclosure, original Git baseline, candidate, explicit patch bundle and exact
editorial review. The schema is
[`ot-reviewed-critical-source.schema.json`](../../../schemas/ot-reviewed-critical-source.schema.json).
`POB-critical` means an explicitly composed source, never a verbatim WLC or
single-scroll transcription. The retained-base literary form and analysis
remain the declared context; unchanged words are not freshly adjudicated.

Schema validation alone is insufficient. The read-only verifier recomposes the
source and checks its linked records using review and composition hashes independently supplied
by the caller. For the actually reviewed Isaiah record:

```bash
.venv/bin/python -m tools.textual_restoration.reviewed_critical_source sources/ot/pob_critical/isaiah/053/011.json --trusted-review-sha256 2695236defe6209ccdd7806bd7f9e8696d261125ef09e1a6fd485c837b50043f --trusted-composition-sha256 d7f01021de7d9b3817d1d75799958c6c0e87fca3320e36f74a7417ebb7f72b1e
.venv/bin/python -m unittest tests.test_reviewed_critical_source tests.test_source_composition
```

The base is read from its immutable Git revision, so a future live-verse edit
does not erase the earlier reading. Candidate and review files remain historical
artifacts. The record's source-selection status is separate from application
and publication approval. The historical source-stage record retains false
application/publication flags; the later application receipt below records
canonical adoption only. Do not replace a pending gate
with a matching hash, use ImageGen as evidence, or infer permission to change
English from source-record validation. The existing canonical verse schema is
unchanged. The alternative
[`ot-critical-verse.schema.json`](../../../schemas/ot-critical-verse.schema.json)
reuses its non-source field contracts and requires the strict source and link.
[`critical_verse.compose_record` and `validate`](../../../tools/textual_restoration/critical_verse.py)
compose the full reviewed verse in memory using separately trusted source,
review and composition hashes. They permit no unreviewed English, note,
rationale or historical-metadata change. Both APIs are read-only; the existing
note-only application mechanism remains historical and cannot handle a
source/main-English change. The separate
[`verify_critical_successor`](../../../tools/textual_restoration/verify_critical_successor.py)
checks the entire actual OT against its fixed checkpoint, allowing only the
exact reviewed replacement while preserving previous note applications.
The two predecessor test suites replay their original 19 tests unchanged at
that checkpoint; they do not certify the current corpus.

The [application receipt](../../textual_restoration/applications/isaiah53_11_successor_application.v1.json)
records actual before/after corpus checks and exports. Verify it with the
independently recorded review and receipt hashes:

```bash
.venv/bin/python -m tools.textual_restoration.verify_critical_successor sources/textual_restoration/applications/isaiah53_11_successor_plan.v1.json sources/textual_restoration/applications/isaiah53_11_successor_review.v1.json --trusted-review-sha256 66d8f2fee1d76aa2b0285659d347b1738af6bde8ef620f60c5961638bcb4d34d --application sources/textual_restoration/applications/isaiah53_11_successor_application.v1.json --trusted-application-sha256 0b486ef4d070e9b9d24307ff3c1480b325cb50bb47addd0f154fa40a16543b96
```

Repository adoption is publicly inspectable and may be fetched by the existing
provenance page. It is not a claim that bundled reader assets were synchronized,
the website was deployed, or all words in the retained base were freshly judged.
