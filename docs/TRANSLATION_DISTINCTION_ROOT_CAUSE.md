# Source-distinction review: John 21 root cause and pipeline correction

Date: 2026-09-06. Scope: translation/review tooling and policy, not a new corpus
revision or publication. The approved John 21 wording was committed separately.

## What actually happened

The first draft **noticed the Greek distinction**. The pre-revision John
21:15–17 records contain the source forms, alternatives, and notes deliberately
rendering both verbs as “love” in the English text. The failure was not failure
to recognize the words; it was failure to elevate a source-visible main-text
alternative into a recommendation under the maintainer's intended objective.

The records in Git snapshot `7c66ac88e1` preserve this history:

| Evidence | Observation |
| --- | --- |
| John 21:15 `ai_draft` | GPT-5.4 draft dated 2026-04-18, prompt ID `nt_draft_v1`; both verbs and alternatives were documented. |
| Archived `high_scrutiny` review `015.job-7630.json` | Gemini 3.1 Pro, 2026-04-21; prompt version `gemini_translation_review_v1_2026-04-21`; **zero context verses**, score **1.0**, verdict **agree**, no issues. |
| That review's explanation | Called the shared “love” rendering with a footnote the “standard and most defensible approach” for optimal equivalence. |
| John 21:15 `revision_pass` | GPT-5.4, 2026-04-23; unchanged, “No changes needed.” |

The archived review is local under
`state/reviews/gemini/high_scrutiny/nt/john/021/015.job-7630.json` in the
maintainer's translation working copy. The original three source records are
also captured in `tests/fixtures/source_distinctions_john21_original.json`.

**Provenance limit:** the historic review stores a prompt version, not the
assembled system-prompt bytes. We can verify its recorded behavior and inputs
listed above. We cannot prove that every line of today's template was identical
in the original April request. The additional current-code defects below are
verified recurrence risks, not invented historical prompt transcripts.

## Why the workflow permitted this

1. **The objective rewarded defensibility too easily.** Drafting described
   optimal equivalence as balanced formal/dynamic translation. The generic
   reviewer exempted already-footnoted lexical alternatives and preferred few
   issues. That could treat a defensible English rendering as the optimum.
2. **Prior rationale could become an answer key.** Revision policy treated
   the draft as finished, instructed reviewers to default to unchanged, and
   equated an unchanged decision with validation. The evidence requirement
   was useful, but it needed a separate requirement to propose source-visible
   alternatives rather than suppress exploration.
3. **The actual generic review lacked passage context.** `high_scrutiny`
   used v1, which received one verse, unlike later v2/v3 strategies. There was
   no enforced comparison of the complete three-question exchange.
4. **Current bulk-review context was incomplete.** Azure and Gemini bulk
   revision paths capped lexical decisions at six and clipped rationales and
   notes. Peter's `φιλῶ` decision in John 21:15 is the eighth entry. Even a
   reviewer trying to compare both choices could receive an incomplete packet.
5. **There was no machine-enforced visibility checkpoint.** An empty issue
   list could produce full agreement without a recorded main-text alternative.
   Existing word-policy guards did not protect the approved John 21 pattern.

## What changed

- `DOCTRINE.md` and the drafting prompt now define optimal equivalence as the
  **most faithful intelligible English representation** of source meaning,
  wording patterns, literary form, and rhetorical force—not a midpoint between
  formal and dynamic translation. Readability serves fidelity; familiarity is
  not a substitute for it.
- `tools/prompts/source_distinction_policy.md` is loaded into drafting, generic
  and enhanced Gemini review, Azure/Gemini bulk revision, and agentic revision.
  A note or old rationale no longer exempts a source-visible difference from
  comparison with the best English candidate.
- Drafts receive neighboring original-language verses where available. Generic
  `high_scrutiny` reviews now receive passage context too. Bulk paths retain
  all lexical entries and their full rationales/notes instead of the first six.
- New responses must provide `source_distinction_checks`. First-draft
  discoveries are bound to detector IDs from their quoted source forms; models
  are not required to predict hashes of lexical choices they have not written.
  Original model IDs and deterministic bindings remain in the audit trail. For each detected
  lead they record source evidence, a full proposed verse, disposition, and
  rationale. Retaining a collapsed rendering requires a different full-verse
  `alternative_text`; it cannot close with only “already footnoted”.
- Missing checks fail validation rather than becoming an “agree” result.
  Proposal reviews retain their full issues in `held_issues` and have an empty
  automatic issue list. They are not sent through ordinary auto-application.
  Held findings remain counted for queue discovery. The auto-apply worker
  additionally marks them `manual_review_required`; CLI summaries report them
  separately rather than counting them as unchanged.
- Direct drafting/revision writers retain unresolved proposals under
  `state/source_distinction_proposals/`, outside publishable translation trees,
  rather than overwriting Scripture. Agentic proposals remain approval-gated.
- Audit receipts identify the policy version/hash and source/input/output text
  hashes. Gemini review receipts also fingerprint the assembled system and
  user prompts. Editing the text invalidates an old receipt.
- John 21:15–17's approved agape-love/phileo-love sequence is guarded in the
  drafter, primary automatic revision writers, approved agentic application,
  SPOB generation/validation, and the regression checker.

This does **not** assume that every different form is a different lemma or
that every different lemma demands a different English meaning. Inflection,
phrase-level decisions, and overlapping usage need actual contextual review.
The important change is that a concrete English alternative is considered and
recorded—not dismissed merely because conventional English is defensible.
No universal “higher/lower love” rule or required reader debate note was added.

## Verification and rollout boundaries

- **43 focused offline tests passed** (27 new audit/pipeline tests, 7 existing
  regression guards, 4 SPOB pipeline tests, and 5 John-wording/history tests).
  The regression suite replays the old John records against the new checks:
  the original no-check/100%-agreement response fails; complete alternatives
  are retained; approved current wording passes; regressions are blocked.
- Tests cover Greek, Hebrew, inflection controls, phrase-level false positives,
  concrete English alternatives, pending-proposal retention, schema wiring,
  original-source context, automatic-writer protection, and stale receipts.
- Read-only corpus triage scanned **31,220 Greek/Hebrew verse records** and found
  **394 candidate verses**, with no parse errors. These are **review leads,
  not confirmed translation mistakes**. One unrelated, uncommitted Genesis 6:6
  change was skipped. The report includes source/code/policy fingerprints.
- Live Gemini replay was blocked **before a model call**: the configured API
  key is unset and the repository's configured AWS Secrets Manager key was
  not found under the current AWS credentials. No fresh model-quality
  improvement is claimed from offline tests.
- No corpus text, public Bible payload, or release was changed by this task.
  Existing completed reviews are not retroactively relabeled as passing the
  new check. Already-running workers need a fresh process to load the new
  prompts; no active workers were interrupted or restarted here.

### Repeatable checks

```sh
CARTHA_DRAFTER_BACKEND=openai-sdk python3 -m unittest discover -s tests -p 'test_source_distinction_audit.py'
python3 tools/source_distinction_audit.py --output /tmp/pob-source-distinction-leads.json
# Optional: narrow the read-only scan with --book john or --book genesis.
```

No API key is needed for these offline checks. A credential-enabled, bounded
model replay is a separate validation step—not permission for a corpus-wide
rewrite or automatic publication of candidate renderings.

Engineering references: [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
and [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
These support explicit instructions and evaluation discipline, not a claim
that a translation's superiority has been established.
