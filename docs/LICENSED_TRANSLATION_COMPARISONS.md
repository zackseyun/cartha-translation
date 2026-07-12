# Licensed NKJV, NIV, and NLT comparison inputs

The divergence system is ready to compare POB and SPOB with NKJV, NIV, and NLT,
but those translations are copyrighted. Their complete wording must not be
committed, scraped from public websites, or placed in the SPOB drafting prompt.

## Comparison targets

- **POB:** NIV and NKJV are the primary modern-English comparison targets.
- **SPOB:** NLT is the primary understanding-first comparison target.
- POB-to-SPOB similarity remains an internal descriptive metric only. It does
  not rank the public "Most divergent verses" report.
- Rows shorter than eight POB tokens, or rows whose verse segmentation does not
  align with at least three reference texts, are excluded from public rankings.

POB and SPOB are ranked separately. POB uses mean divergence from NIV and NKJV;
SPOB uses divergence from NLT. Documented textual or interpretive risk stays in
the internal editor queue and never boosts the public headline score. Until the
licensed inputs are configured, the POB list uses a clearly labeled provisional
public-domain score: `novelty × sqrt(reference consensus)`. SPOB has no public
target ranking until NLT is present.

## Versification safety

POB follows source-oriented Hebrew/MT numbering in the Old Testament and
NA/SBLG-style numbering at the small set of New Testament differences, while
the comparison APIs use standard English numbering.
`tools/sync_stepbible_versification.py` derives a shared mapping from
STEPBible's CC BY 4.0 TVTMS dataset. Both the public reference panel and the
API.Bible fetcher pass every source reference through this map before
comparison. Psalm titles receive an additional normalization because POB
stores them as verse 0.

The divergence build also runs a unanimous-neighbor verifier. A row is
quarantined if at least three reference panels all match the same neighboring
verse materially better, and a normal build fails while any such offset
survives. `--allow-alignment-quarantine` is only for diagnosis.

## Safe operating boundary

1. Obtain a license that expressly covers Cartha's commercial and AI-assisted
   evaluation use.
2. Store retrieved text only in `state/licensed_references/` or another private,
   gitignored location.
3. Run the comparison only after a SPOB draft exists.
4. Commit only the resulting numeric scores and non-sensitive source metadata.
5. Keep licensed translations out of the public-reference consensus and out of
   `review_priority`; agreement is not proof that a rendering is correct.
6. If licensed wording is displayed in the product rather than analyzed
   privately, implement the provider's required copyright attribution, cache
   limits, and FUMS reporting. The static analysis bundle intentionally cannot
   satisfy those runtime display requirements by itself.

Official routes to evaluate:

- **[API.Bible](https://docs.api.bible/)** advertises NKJV, NIV, and NLT under one API/license framework;
  availability and commercial rights depend on the account plan and selected
  licenses.
- **[NLT API](https://api.nlt.to/)** provides NLT directly; anonymous access is non-commercial, so
  Cartha needs an appropriate key and written terms for this use.
- **[NIV](https://www.biblica.com/permissions/)** licensing is controlled by Biblica. AI/ML use requires a license that
  expressly permits it.
- **[NKJV](https://www.thomasnelson.com/about-us/permissions/)** permissions are administered by Thomas Nelson; uses outside its
  quotation guidelines require permission.

The pending Tyndale request is documented in `outreach/tyndale_email.md`.

## API.Bible private fetch

Create a gitignored config with each translation's Bible ID and the internal
agreement or plan reference that authorizes the use:

```json
{
  "translations": {
    "nkjv": {"bible_id": "account-specific-id", "license_reference": "agreement-id"},
    "niv": {"bible_id": "account-specific-id", "license_reference": "agreement-id"},
    "nlt": {"bible_id": "account-specific-id", "license_reference": "agreement-id"}
  }
}
```

Then fetch the pilot scope without printing verse text:

```bash
export API_BIBLE_KEY='...'
python3 tools/fetch_api_bible_licensed_references.py \
  --config state/licensed_references/api-bible-config.json \
  --output state/licensed_references/english-commercial.json \
  --books genesis luke \
  --acknowledge-license
```

The acknowledgement is intentional: having an API key alone does not prove that
the selected plan permits this comparison use.

## Private bundle format

Create `state/licensed_references/english-commercial.json`:

```json
{
  "schema_version": 1,
  "translations": {
    "nkjv": {
      "display_name": "NKJV",
      "provider": "authorized provider",
      "license_reference": "private agreement identifier",
      "verses": {"GEN.1.1": "licensed text supplied privately"}
    },
    "niv": {
      "display_name": "NIV",
      "provider": "authorized provider",
      "license_reference": "private agreement identifier",
      "verses": {}
    },
    "nlt": {
      "display_name": "NLT",
      "provider": "authorized provider",
      "license_reference": "private agreement identifier",
      "verses": {}
    }
  }
}
```

Then run:

```bash
python3 tools/build_translation_divergence.py \
  --books genesis luke \
  --licensed-references state/licensed_references/english-commercial.json
```

The report exposes per-translation `pob_similarity`, `spob_similarity`, and
`spob_minus_pob`, but never the licensed verse text. NLT additionally appears in
the convenience fields `pob_nlt_similarity`, `spob_nlt_similarity`, and
`spob_nlt_similarity_gain`.

Before fetching, regenerate or verify the current mapping:

```bash
python3 tools/sync_stepbible_versification.py
python3 tests/test_translation_divergence.py
```
