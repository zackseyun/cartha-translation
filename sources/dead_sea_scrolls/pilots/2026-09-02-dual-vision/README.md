# Original-image vision pilot — 2026-09-02

## Scope

Two neutral-labeled crops were extracted from the registered LOC TIFF masters:

| Label | Source | Region in original pixels (x, y, width, height) |
|---|---|---|
| region-a | 1QM, LOC matpc.22899 | 1740, 685, 1450, 490 |
| region-b | 1QpHab, LOC matpc.22898 | 810, 1190, 615, 475 |

`regions.json` connects every crop to its master, dimensions, software version,
and SHA-256 hashes. Only an exact pixel crop and RGB conversion were performed.
There was **no ImageGen, resizing, denoising, sharpening, or generative repair**
in these input files. Some letter tops/tails and edge words are clipped; the
second photograph is visibly blurrier. These constraints must not be silently
filled from a known edition.

The two model requests use the same `prompt.txt`, crop order, and strict
`response.schema.json`. No book title, passage reference, other model response,
or modern edition is supplied. Each provider starts in a separate empty
temporary directory. Model recognition from training cannot be ruled out; the
prompt explicitly prohibits replacing visible ink with remembered wording.

## Results and limits

See `RESULTS.md` for the observed run outcome and counts. Sanitized provider
records live in `passes/`; raw CLI envelopes are gitignored because they may
contain account/session metadata. Failed provider runs have `result: null` and
cannot create consensus, even if the CLI misleadingly labels the event subtype
as `success`.

This is a **transcription proposal pilot**, not an accepted critical edition.
The pass envelope is distinct from `schemas/dss-transcription.schema.json`;
promotion into that corpus format is a separate step. Matching clear tokens can
receive the project's research-consensus status after both actual model outputs
exist. Matching uncertainty, gap markers, or segmentation disagreements cannot
become observed ink. This first pass does not propose restorations.

No file under `translation/`, reader export, or production asset is changed by
the pilot commands. Agreement rates must not be described as measured accuracy
without an independently established control transcription.

## Repeatable commands

Run from the POB repository root:

```bash
python3 tools/dss/pilot.py prepare
python3 tools/dss/pilot.py validate
python3 -m unittest discover -s tests -p 'test_dss*.py' -v

# Only after the relevant account is authorized; these consume model usage.
python3 tools/dss/run_pilot.py --provider openai --executable "$CODEX_CLI_PATH"
python3 tools/dss/run_pilot.py --provider anthropic

python3 tools/dss/pilot.py compare
```

Existing passes are protected by default. Add `--replace` only when deliberately
rerunning a pass, and preserve the previous record in version history first.
There is no model substitution, authorization bypass, or automatic retry of an
account restriction. The exact selected model IDs are `gpt-5.6-sol` and
`claude-opus-5`.

The installed npm Codex wrapper was unusable, but the already installed
`/Applications/ChatGPT.app/Contents/Resources/codex` executable works. The pilot
uses it explicitly without modifying or reinstalling the global CLI.

## Next gate

Claude Code returned: “Your organization has disabled Claude subscription access
for Claude Code”. Its suggestion is to use an authorized Anthropic API key or
have the administrator enable access. Authentication alone is not proof of
permission to make an inference call. Do not retry this branch until access is
legitimately enabled.

After that gate, rerun only the Anthropic provider on the unchanged blind inputs,
validate both responses, and run `compare`. Preserve alternate readings rather
than asking either model merely to agree with the other.
