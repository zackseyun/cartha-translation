# Image-only observation protocol 2.0

This opt-in protocol enables negative controls and explicit abstentions in future
pilots. It is **not a completed benchmark** or a measured improvement in model
accuracy. No new provider inference has been executed with it.

The [prompt](observation-v2.prompt.txt) and [response schema](observation-v2.schema.json)
separate these image observations:

| Observation | Required response | Comparison treatment |
|---|---|---|
| `text-present` | Nonempty consecutive lines, each with tokens | Existing clear-token agreement rules; agreement is not proof of legibility. |
| `no-visible-text` | Empty lines and a nonempty explanation | Record matching observations or disagreement; never add accepted letters. |
| `unassessable` | Empty lines and a nonempty explanation | Remain unresolved, even when both models abstain. |

Both JSON-schema validation and `validate_result` semantic validation are
required; the existing runner and saved-pilot validator perform both. The
latter enforces observation/line consistency, explanatory notes
for abstentions, and exact ordered region coverage. Schema acceptance alone
does not establish those conditions. Missing regions, missing responses,
provider failures and unsupported protocol versions are not blank observations.
The comparator refuses mixed protocol versions. Its version-2 report includes
region observations separately from token counts. Zero compared tokens is not
an accuracy score; blank-control false positives and abstentions need separate
denominators in the eventual benchmark.

## Use in a new, frozen pilot

Create a new pilot directory rather than replacing historical artifacts. Freeze
the source/crop manifest, neutral IDs `region-1`, `region-2`, etc. in attachment
order, this prompt as `prompt.txt`, and this schema as `response.schema.json`.
Reference labels, damage strata, development/evaluation split and acceptance
criteria must be frozen separately before evaluation; do not show answer labels
to either model. Use the existing runner's explicit `--pilot` selection only
when legitimate provider access is available. Verify provider schema support
before claiming successful execution; local schema tests do not prove it.

The old `2026-09-02-dual-vision` prompt, schema, passes and comparison remain
unchanged. Its old-format results still validate; they are not silently upgraded
to protocol 2.0. No repeat of the saved access failure was attempted here.

Validation: `python -m unittest tests.test_dss_pilot tests.test_dss_project
tests.test_dss_observation_protocol` (one command, on one line). The 31 passing
tests exercise parser/comparison behavior and saved-pilot integrity, not actual
image-reading accuracy. No synthetic or generated image is manuscript evidence.
