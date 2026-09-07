# Provisionally reviewed POB Hebrew critical sources

This directory begins a **partial editorial source corpus**, not a replacement
for WLC and not a claim of recovered autographs. Currently it contains only
[Isaiah 53:11](isaiah/053/011.json). Its selected Hebrew has independent AI
editorial approval; the live POB English verse is still unchanged.

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
and publication approval, which remain false. Do not replace a pending gate
with a matching hash, use ImageGen as evidence, or infer permission to change
English from source-record validation. The existing canonical verse schema and
application mechanism still need a deliberate integration/migration; this new
source format does not silently bypass their restrictions.
