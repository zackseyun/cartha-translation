# Simplified People's Open Bible (SPOB) pipeline

SPOB is a **plain-language English derivative** of the People's Open Bible. It exists for the modern common reader: clearer sentences, less academic friction, and more immediate understanding — while keeping POB's source-grounded choices and reasoning layers intact.

## What SPOB is

- **Derivative of POB, not a replacement source translation.** POB remains the controlling base text.
- **Modern common English.** Clear, direct, dignified, not childish or slangy.
- **Real readability rewrite.** SPOB should not merely preserve POB's structure
  with a few synonym swaps; opaque words, dense clauses, idioms, measures,
  currency, legal phrasing, and inherited church terms should become immediately
  understandable in the main text when the meaning can be preserved.
- **Faithful compression.** SPOB may compress or simplify wording, but it must preserve the main POB decision, important ambiguities, source-language images, and theological tensions.
- **Still auditable.** Each SPOB record points back to the POB YAML and carries simplification decisions explaining what was compressed and what reasoning layer protected the meaning.

## Output layout

SPOB records live under:

```text
translation_simplified/<testament>/<book>/<chapter>/<verse>.yaml
```

Each record stores:

- `source` copied from the POB record as an audit guardrail
- `base_translation` with the POB YAML path, current POB text, footnotes, and revision metadata
- `translation.language: en` and the simplified English `translation.text`
- `simplification_decisions` describing POB phrase → simplified phrase, preserved meaning, and rationale
- `retained_terms` for terms intentionally not flattened
- `source_grounding.pob_role: primary_derivative_base`
- `ai_draft.usage.estimated_cost_usd`

## Commands

Estimate draft cost:

```bash
python3 tools/simplified_pob_pipeline.py estimate --limit 250 --model gpt-5.4-mini
```

Draft a pilot batch:

```bash
python3 tools/simplified_pob_pipeline.py draft --book john --limit 5 \
  --model gpt-5.4-mini \
  --deployment "$AZURE_OPENAI_MINI_DEPLOYMENT_ID"
```

Validate existing SPOB records:

```bash
python3 tools/simplified_pob_pipeline.py validate --only-existing
```

Summarize progress and observed costs:

```bash
python3 tools/simplified_pob_pipeline.py summary
```

Scale with shards:

```bash
python3 tools/simplified_pob_pipeline.py draft --limit 0 --shard-count 8 --shard-index 0 --keep-going
python3 tools/simplified_pob_pipeline.py draft --limit 0 --shard-count 8 --shard-index 1 --keep-going
# ...
```

## Reader/export naming note

Historically, some reader code and metadata used `spob` / `spob-preview` for the **Spanish** People's Open Bible. Going forward, **SPOB means Simplified People's Open Bible**. Spanish should be displayed as **Spanish POB** (or `ES POB` in very tight UI), and any future asset/id migration should move Spanish toward an `espob` / `spanish-pob` style id. The Simplified edition can then safely use the public short name **SPOB** while using a stable internal id such as `simplified-pob-preview`.

## Review rule

A SPOB verse is acceptable only if a reviewer can answer “yes” to all three:

1. Does the simplified wording preserve the POB meaning?
2. Does it preserve documented ambiguity or theological tension where POB preserved it?
3. Would a normal modern reader understand it more easily than POB without being misled?

If a verse still leaves words like `quadrans` in the main sentence without a
plain equivalent such as “last small coin,” it should be treated as
under-simplified and regenerated or revised.
