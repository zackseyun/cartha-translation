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

When all three licensed targets are present, the targeted review priority is
55% POB-vs-NIV/NKJV divergence, 35% SPOB-vs-NLT divergence, and 10% documented
textual/interpretive risk. Until then, any public-domain ranking must be labeled
provisional rather than presented as the target comparison report.

## Safe operating boundary

1. Obtain a license that expressly covers Cartha's commercial and AI-assisted
   evaluation use.
2. Store retrieved text only in `state/licensed_references/` or another private,
   gitignored location.
3. Run the comparison only after a SPOB draft exists.
4. Commit only the resulting numeric scores and non-sensitive source metadata.
5. Keep licensed translations out of the public-reference consensus and out of
   `review_priority`; agreement is not proof that a rendering is correct.

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
