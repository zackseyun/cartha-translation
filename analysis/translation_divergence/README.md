# Translation divergence indicators

These files compare POB and available SPOB wording with legally reusable English
reference translations. They answer two practical questions:

1. Where do common English renderings differ enough that editors should inspect
   the verse?
2. Where are POB or SPOB wording outliers relative to that reference panel?

They do **not** decide which translation is correct. Majority wording is not source
evidence, and old translations can agree because they share a textual tradition or
depend on one another.

## Reference panel

- Berean Standard Bible (public domain / CC0)
- World English Bible (public domain)
- American Standard Version (public domain)
- King James Version (public domain in the United States)
- Brenton's Septuagint translation (public domain; OT context only, excluded from
  the four-version consensus score)

The source texts are downloaded from eBible.org by
`tools/build_reference_panel.py`. Only public-domain/CC0 text is committed.

NKJV, NIV, and NLT can be added as private, licensed post-draft comparison
inputs. Their wording is never serialized into these reports; only numerical
POB/SPOB similarity values and non-textual provenance are retained. They do not
affect the public-reference consensus or `review_priority` score.

## Scores

- `reference_wording_divergence` — how much the four consensus references differ
  from one another after basic normalization.
- `pob_distinctiveness` — how unlike POB wording is from those references.
- `spob_distinctiveness` — the same indicator for SPOB when that verse exists.
- `pob_spob_similarity` — wording continuity between the two Cartha editions.
- `documented_risk` — POB footnotes, theological decisions, ambiguity language,
  metaphors/idioms, and source variants.
- `review_priority` — 50% reference divergence, 30% POB distinctiveness, and 20%
  documented risk.

Common KJV archaisms, punctuation, case, and footnote markers are normalized.
Character similarity reduces false alarms caused only by transliteration spelling.
Known source-oriented versification differences are aligned before scoring.

## Regeneration

```bash
python3 tools/build_translation_divergence.py --fetch --books genesis luke
```

With an authorized local bundle:

```bash
python3 tools/build_translation_divergence.py \
  --books genesis luke \
  --licensed-references state/licensed_references/english-commercial.json
```

When NLT is available, each verse also receives `pob_nlt_similarity`,
`spob_nlt_similarity`, and `spob_nlt_similarity_gain`. A positive gain means
SPOB is lexically closer to NLT than POB is; it is not a quality or truth score.

Per-book files contain the reference renderings and all component scores.
`translation-divergence-summary.json` contains the highest-priority candidates for
fast review and future website/app indicators.
