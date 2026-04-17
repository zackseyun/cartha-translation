# Tools

Python scripts for drafting, cross-checking, verifying, signing, and
linting the Cartha Open Bible.

## Scripts

| Script | Status | Purpose |
|---|---|---|
| `sblgnt.py` | implemented | Parses the MorphGNT SBLGNT text files; exposes `load_verse(book, chapter, verse)`, `iter_verses(book)`, and `morphology_lines(verse)`. |
| `draft.py` | implemented | Produces an AI-drafted verse YAML for a single verse. Reads SBLGNT source, extracts the required DOCTRINE.md sections, drafts with GPT-5.4 via either `codex-cli` (ChatGPT/Codex login) or the OpenAI SDK, validates against `schema/verse.schema.json`, and writes a provenance-complete YAML to `translation/nt/<book>/<chapter>/<verse>.yaml`. Supports `--dry-run` for prompt inspection without a model call. |
| `cross_check.py` | stub | Runs draft against Claude + GPT + Gemini in parallel, scores agreement, flags divergences. Spec in METHODOLOGY.md Stage 3. |
| `verify.py` | not yet written | Re-runs the documented pipeline for a published verse. Confirms AI draft reproduces, cross-check reproduces, signature validates, reviewer is in `REVIEWERS.md`. |
| `consistency_lint.py` | implemented | Checks internal consistency across drafted YAMLs. Flags undocumented lexical variance, contested-term doctrine gaps/overrides, approved verses missing reviewers, and empty source text; writes Markdown reports to `lint_reports/`. |
| `run_phase.py` | implemented | Resumable phase runner. Drafts missing verses for a configured phase, retries failures, records `failed_verses.txt`, supports book subsets and chapter-batch limits, runs `consistency_lint.py`, updates `CHANGELOG.md`, and tags the completed phase. |
| `sign.py` | not yet written | Generates ed25519 signatures for reviewer sign-off. Private key stays local; public key + signature are committed. |
| `wlc.py` | implemented | OT parser scaffold for WLC/OSHB OSIS XML, mirroring `sblgnt.py` so later OT drafting can reuse the same prompt/validation pipeline. |

## Prerequisites

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt
```

Required environment variables:

```bash
CARTHA_DRAFTER_BACKEND=codex-cli   # default when Codex is logged in
OPENAI_API_KEY=...                 # only for openai-sdk backend
ANTHROPIC_API_KEY=...    # for future cross_check.py (Claude)
GOOGLE_API_KEY=...       # for future cross_check.py (Gemini)
```

## Quick start — draft one verse

```bash
# Dry run: inspect the prompt that would be sent, without an API call.
python3 tools/draft.py --ref "Philippians 1:1" --dry-run

# Real run via Codex login tokens: produces translation/nt/philippians/001/001.yaml.
python3 tools/draft.py --ref "Philippians 1:1" --backend codex-cli

# Or, if you explicitly want the API path:
export OPENAI_API_KEY=...
python3 tools/draft.py --ref "Philippians 1:1" --backend openai-sdk
```

Model, temperature, and prompt ID are configurable via CLI flags or
environment variables (`CARTHA_MODEL_ID`, `CARTHA_TEMPERATURE`,
`CARTHA_PROMPT_ID`).

## Run the Philippians pilot

```bash
python3 tools/run_phase.py --phase phase0 --backend codex-cli
```

This is resumable: already-written verse YAMLs are skipped on rerun.

## Start Phase 1 in chapter batches

```bash
# Draft and commit the next Romans chapter only.
python3 tools/run_phase.py --phase phase1 --backend codex-cli --books ROM --max-chapters 1
```

Then rerun to continue the next chapter/book. Completed verses are skipped automatically.
