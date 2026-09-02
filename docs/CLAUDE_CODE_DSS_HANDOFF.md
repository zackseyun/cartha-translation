# Claude Code handoff — independent POB manuscript transcription

**Start here. Do not read the repository overview, other task history, or
Codex's results before completing and freezing your own transcription.**

Zack has asked to run Claude independently after Codex's initial pilot work.
This document is the complete brief for that independent pass. It intentionally
omits manuscript identities, proposed readings, expected line counts, English
translations, and Codex's confidence labels.

## Project context

The People's Open Bible (POB) is building an auditable manuscript project:

**original image → diplomatic transcription → explicitly marked restoration
proposals → Hebrew/Aramaic/Greek witness comparison → reasoned English translation.**

The long-term program covers the Dead Sea Scrolls and other ancient witnesses.
It keeps surviving ink, supplied letters, interpretations, and canonical status
separate. AI-generated illustrations may eventually accompany the work, but
must never replace the original image as transcription evidence.

Codex has completed **the initial pilot preparation and its own first vision
pass**, not the entire corpus project. Source crops, a shared prompt/schema,
provenance, and comparison tooling are saved in the repository. Your job now is
to supply the missing independent reading, not to review or agree with Codex.

## Your task and stop point

Use **Claude Opus 5 (`claude-opus-5`)**, if your authorized session provides it,
to transcribe two supplied ancient Hebrew image crops independently. Save an
unaltered first-pass JSON response and a truthful provenance receipt, then
freeze both with SHA-256 hashes and return their paths to Zack.

**Stop after delivering those files.** Codex will subsequently import the
independent result and compare it with its frozen pass. Do not perform the
comparison, change POB verse text, or revise your reading to match another model
within this first-pass task.

You may work directly in your authorized Claude Code session. You do **not**
need to launch another Claude process. An earlier automated attempt encountered
an organization restriction on Claude Code subscription inference; it returned
no reading. Do not bypass that restriction. If your present session lacks
authorized access, report the access blocker rather than substituting a model
or claiming a completed pass.

## Phase 1 — blind input allowlist

Repository:

`/Users/zackseyun/Documents/GitHub/peoples-open-bible`

Pilot input directory:

`/Users/zackseyun/Documents/GitHub/peoples-open-bible/sources/dead_sea_scrolls/pilots/2026-09-02-dual-vision`

Before your response is frozen, read **only this handoff and these four files**:

1. `prompt.txt` — the exact common transcription instructions. Read in full.
2. `response.schema.json` — the exact result shape. Read in full.
3. `crops/region-a.png` — first image; inspect its pixels directly.
4. `crops/region-b.png` — second image; inspect its pixels directly.

Resolve those four paths against the pilot input directory above. It is
permitted to read these files, obtain the current UTC time, verify their hashes,
and write/hash your output files. Do not rescale, sharpen, inpaint, recrop, or
generate replacement images for this particular matched-input pass.

Expected SHA-256 values:

```text
c19233e907caf4742061f472059875a866757c377464cb5dd2e772a42e317eaa  prompt.txt
7a06f3eebc2cdbe0871c977fe272df1616d41183b84adc69864ba12d76e68e54  response.schema.json
997dcce8ac39c9a76b8eefa5b56556af6edc5b17810219da239f1827b2dafe97  crops/region-a.png
49f5c0ccd6e7f2ddc7367f9a948f2e27fb4f8ef28d3446ce065bf54c9da43a3d  crops/region-b.png
```

If a hash differs, stop and report the mismatch; do not silently regenerate the
input or proceed as if it were the same experiment.

### Do not read until after your response is frozen

- Any `passes/` file, including `passes/openai.json` and `passes/anthropic.json`.
- `RESULTS.md`, `comparison.json`, `attempts.json`, the pilot `README.md`, or
  `regions.json` (which reveals the identities of the manuscript crops).
- Repository overview/source registries, textual-comparison samples, published
  transcriptions, critical editions, English translations, web searches, or
  other task transcripts/memories.
- Git diffs/logs that expose Codex's response, or tests that load saved passes.

Use a fresh session. If prior context, an automatically loaded file, or a tool
has already exposed other readings or results, disclose that in your receipt.
Do not claim that a contaminated session was blind; Zack can restart it with
only the allowed inputs. Respect higher-priority session instructions rather
than pretending they were disabled.

## Phase 2 — perform the transcription

Follow `prompt.txt` exactly. In particular:

- Return both regions in the supplied order, with lines numbered top to bottom
  and Hebrew tokens in normal logical reading order.
- Transcribe visible consonants and word divisions without translating or
  normalizing spelling. Do not complete a familiar passage from memory.
- Mark every token `clear`, `uncertain`, `unreadable`, or `gap` as specified.
- Use `□` for an unreadable glyph and `[—]` for a gap; do not invent missing
  letters or a gap length. This first pass does **not** restore missing text.
- Describe uncertain shapes and edge fragments in notes. Do not supply a
  polished reading merely because it sounds grammatical.
- Give only the requested JSON in `response.json`, without Markdown fences.

## Phase 3 — save and freeze before seeing other answers

Write outputs outside the repository so they cannot be mistaken for accepted
corpus data:

`/Users/zackseyun/Documents/POB-Claude-Handoff/2026-09-02/<UTC-run-id>/`

Use a fresh UTC run ID such as `YYYYMMDDTHHMMSSZ`. Never overwrite an earlier
run. Produce:

1. **`response.json`** — your original transcription, matching the shared
   schema. Both region IDs must appear exactly once. Preserve this first answer.
2. **`receipt.json`** — record:
   - provider, requested model, actual model ID if available, and reasoning
     setting;
   - how the actual model was established (runtime/session metadata, not an
     unsupported assertion by the model); use `unknown` if not available;
   - UTC start/completion timestamps;
   - the exact input paths and their actual SHA-256 hashes;
   - the response SHA-256;
   - whether prior model outputs/editions were seen, including accidental
     exposure;
   - an accurate list of input/output tool actions and any extra processing;
   - `independence_status`: `declared-blind`, `contaminated`, or `unknown`;
   - `verification_level`: `session-declaration-not-external-audit`;
   - `publication_action`: `none`.
3. **`SHA256SUMS`** — hashes of `response.json` and `receipt.json` after both
   are finalized.

Do not record credentials, account emails, organization identifiers, or private
session transcripts in the deliverables. Retain any relevant runtime evidence
locally and identify it without copying private account data.

You may fix a JSON syntax mistake before freezing, but never consult another
reading to fix the content. Once frozen, any later correction goes in a new
file with a reason; it is no longer the untouched independent first pass.

## Completion checklist

- [ ] The four inputs match their expected hashes.
- [ ] Both original images were actually inspected; no image was generated.
- [ ] Both regions are present and uncertainty is preserved.
- [ ] Model identity/access and any missing provenance are reported honestly.
- [ ] No prior response or edition was used, or exposure is explicitly declared.
- [ ] `response.json`, `receipt.json`, and `SHA256SUMS` are saved and frozen.
- [ ] No repository source text, existing pass, reader export, or deployment was
  changed.
- [ ] Zack receives the three absolute output paths and a brief completion or
  blocker report.

## Project continuation after the independent pass

Only after your own response is frozen may the coordinator read the broader
project files:

- `docs/DSS_TEXTUAL_WITNESS_PROJECT.md` — program charter and evidence layers.
- `docs/DSS_TEXTUAL_WITNESS_TODO.md` — corpus and implementation backlog.
- `docs/TEXTUAL_RESTORATION_PRIORITIES.md` — OT/NT priorities and comparison plan.
- `sources/dead_sea_scrolls/pilots/2026-09-02-dual-vision/README.md` — pilot setup.
- `tools/dss/pilot.py` and `tools/dss/run_pilot.py` — validation, provider
  envelopes, and comparison tooling.

Direct Claude Code file-reading/writing is not identical to the automated
no-tool runner. Its receipt must preserve that distinction. Do not fabricate
an empty tool history or overwrite the saved blocked provider record just to
make the current comparator accept a direct-session response. Import/audit of
the direct-session receipt is the coordinator's next integration step.

The project's working policy accepts exact agreement from two different model
families as model consensus, but not as a measured error rate or proof of the
ancient reading. Supplied text always remains distinct from observed ink.
Future collation, restoration proposals, English translation, and any clearly
labeled ImageGen illustration are separate phases—not part of your blind pass.
