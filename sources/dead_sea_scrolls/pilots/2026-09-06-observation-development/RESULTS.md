# First actual observation-control result

Run 2026-09-06 local time (2026-09-07 UTC). **OpenAI passes the frozen four-region
observation smoke test; no usable Hebrew transcription or restoration obtained.**
The frozen README's zero-run statement describes preparation history; this file
records the later execution without rewriting the freeze.

One `gpt-5.6-sol` low-effort run finished successfully in 41.58 seconds using
Codex CLI 0.153.4, the existing runner, attached crops, an empty temporary working
directory and the frozen prompt/schema. Expected labels and other model outputs
were not supplied. Raw event types contain one agent-message completion and no
tool calls. The actual result passed local schema and semantic validation.

| Preset measure | Actual result |
|---|---|
| Correct observation classes | 4 / 4 |
| Positive writing regions correctly identified | 2 / 2 |
| Negative regions correctly identified | 2 / 2 |
| Negative regions with a text-present claim | 0 / 2 |
| Tokens emitted on negative regions | 0 |
| Region-level abstentions | 0 / 4; zero in each class |
| Missing or invalid regions | 0 |

On the two writing regions, the model emitted 43 unreadable square placeholders
and two gap placeholders, with no Hebrew letters and no clear tokens. It could
detect writing but declined to transcribe blurred letter shapes. Region-level
classification success must not conceal that complete lack of usable word
readings. Line/word segmentation and the two gap assignments have no reference
labels here and are not certified correct.

The [saved pass](passes/openai.json) and [scoring record](openai-score.v1.json)
bind actual output and frozen inputs. Raw CLI counters: 13,511 input tokens,
1,266 output tokens and 436 reasoning-output tokens, reported separately without
inferring dollar cost or adding the reasoning counter again. Private raw envelopes
remain Git-ignored; the sanitized pass retains a hash for traceability.

Independent `observation_run_score_check` verified the frozen hashes, model and
effort, schema, class scores and token counts without opening images or raw
logs. It passed the scoring claim only. All 32 focused input/protocol tests and
the actual four-crop pilot validation also passed; neither is a glyph benchmark.

OpenAI Docs prompted verification against the actual
[official non-interactive-mode documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
and local CLI help before running. The existing read-only, ephemeral invocation
was used without changing model, prompt, thresholds or tools after seeing outputs.
The documentation establishes invocation behavior, not this experiment's accuracy.

This is one development result on four selected crops from an already-used
photograph. It does not prove general false-positive rates, glyph accuracy,
historical priority or restoration reliability. No Anthropic call occurred; no
two-family agreement or critical-text promotion is claimed. The next productive
reading step needs better optical evidence and defensible character labels,
not repeated attempts on these crops until a model supplies letters. The
second-provider pass still awaits a legitimate access change.
