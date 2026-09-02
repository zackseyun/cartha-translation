# Pilot results — 2026-09-02

## Observed outcome

| Provider | Exact selected model | Outcome |
|---|---|---|
| OpenAI | `gpt-5.6-sol` | Structured image-only proposal returned; low reasoning effort, 101.45 seconds |
| Anthropic | `claude-opus-5` | Access blocked before a successful transcription; no model reading returned |

The successful GPT run used only the attached image crops and made no tool
calls. It returned **13 line/stroke-group rows**, including partial next-line
strokes at the crop boundaries. These are not 13 complete manuscript lines.

Its **68 token/stroke segments** were labeled:

- 3 clear by the model;
- 49 uncertain;
- 7 unreadable;
- 9 gaps.

The three “clear” labels are model self-assessments, **not independently
verified correct words**. The historical images remain optically soft despite
high pixel dimensions. Region-b is especially blurred, and both crops contain
boundary fragments that the next segmentation pass should distinguish from
complete lines.

## Acceptance

**Two-model accepted tokens: 0. Restored words: 0. Published changes: 0.**

`comparison.json` is explicitly `awaiting-two-successful-passes`. The blocked
Claude event is not counted as agreement, disagreement, or a second model vote.
No English translation or POB source verse was changed.

## Execution record

The first tool-enabled GPT high-effort attempt exceeded 480 seconds without a
final response. A fresh no-tool high-effort attempt exceeded 300 seconds.
Neither unfinished output was reused as a transcription. The final fresh
no-tool low-effort attempt returned the saved result above. This establishes a
working invocation, not that low effort is more accurate than high effort.

The first Claude invocation failed CLI argument validation. The corrected
invocation selected `claude-opus-5`, but the service returned:

> Your organization has disabled Claude subscription access for Claude Code

It suggested an authorized Anthropic API key or administrator-enabled access.
Authentication status alone had misleadingly shown the account as logged in.
The CLI result also used `subtype: success` with `is_error: true`; the parser and
regression test correctly treat that as a blocked run, never a transcription.

Sanitized earlier attempt records are in `attempts.json`. Actual provider
proposals and metadata are in `passes/`. Raw envelopes remain private/local and
are referenced by SHA-256 rather than committed with account/session metadata.

## Resume

1. Enable legitimate Claude inference access through the account administrator
   or an authorized local API-key configuration. Do not paste a key into Git or
   a task message.
2. Run only the Anthropic provider against the unchanged `prompt.txt`, schema,
   and two crops. Do not show it the OpenAI output.
3. Validate and compare the saved responses. Line/token segmentation conflicts
   remain unresolved; matching uncertainty never becomes observed ink.
4. Refine fragment/line regions and benchmark against independently established
   control lines before claiming an accuracy rate or scaling to full scrolls.

The current artifacts demonstrate real image acquisition and a functioning
first vision pass, while preserving the actual access and reading limitations.
