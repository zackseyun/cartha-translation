# SPOB GPT-5.6 calibration

Generated: 2026-07-10

## Decision

- **Primary understanding-first drafter: GPT-5.6 Sol**
- **Conservative grounding reviewer: GPT-5.6 Terra**
- **Clarity/expansion challenger: GPT-5.6 Luna**

All three Azure deployments passed the same strict structured-output prompt on
1 Peter 1:13, 4:7, and 5:8. Sol most consistently followed the new SPOB doctrine:
it made warranted contextual meaning explicit, preserved distinct source ideas,
and documented expansions and risks. Terra was accurate but often remained close
to POB. Luna was the fastest and sometimes usefully bold, but in 1 Peter 4:7 it
expanded more aggressively than necessary.

This is a calibration decision, not a claim that one model is always correct.
High-risk verses still require grounding review and human approval.

## 1 Peter 5:8 comparison

POB:

> Be clear-minded; stay alert. Your adversary, the devil, walks around like a
> roaring lion, seeking someone to devour.

Sol:

> **Keep a clear mind and stay spiritually awake. Your enemy, the devil, walks
> around like a roaring lion, looking for someone to devour.**

Terra:

> Keep a clear mind and stay alert. Your enemy, the devil, goes around like a
> roaring lion, looking for someone to devour.

Luna:

> Keep a clear mind and stay alert. Your adversary, the devil, walks around like
> a roaring lion, looking for someone to devour.

Sol alone made the spiritual domain explicit while preserving the two commands:
clear-minded self-possession and wakeful vigilance. Its structured record marked
“spiritually awake” as a high-confidence expansion supported by the immediate
devil/lion context and preserved “stay alert,” “be watchful,” and “keep watch” as
alternatives.

## Other calibration observations

### 1 Peter 1:13

- Sol explained the clothing metaphor in the main line: “prepare your minds for
  action, like someone gathering up loose clothing.” This maximizes access but
  needs review for commentary-like length.
- Terra used the cleanest restrained rendering: “prepare your minds for action.”
- Luna was highly readable: “get your minds ready for action,” but dropped the
  embodied metaphor from the main line.

### 1 Peter 4:7

- Sol clearly expressed purpose: “exercise self-control and keep a clear mind so
  that you can pray.”
- Terra stayed closest to POB.
- Luna separated the paired concepts and added “be spiritually awake.” The POB
  footnote supports spiritual alertness, but this illustrates why Luna is better
  used as a challenger than the sole drafter.

## Azure throughput finding

The first calibration attempt returned HTTP 429 because each deployment had only
1,000 tokens/minute and one request/minute. The strict SPOB prompt itself can be
2,700–4,200 input tokens before output. Deployment capacity was raised from 1 to
20 units for calibration, producing 20,000 tokens/minute and 20 requests/minute
per variant. The pipeline default completion ceiling was reduced from 8,000 to
3,000 tokens and now uses rate-limit-aware backoff.

## Scale policy

1. Draft a focused book-level pilot with Sol.
2. Review high-risk and interpretively expanded verses against Terra and Luna.
3. Check prose consistency, source preservation, and footnotes.
4. Only then scale the same prompt/model configuration across the remaining
   corpus in controlled shards.

## Cost and compact-audit update

The 1 Peter draft-review-revision loop consumed roughly one million tokens across
105 records. A naive linear full-corpus run would therefore approach 400 million
tokens. Azure's public retail meter did not yet return GPT-5.6 Sol/Terra/Luna
prices on 2026-07-10, so a full unattended run must not assume GPT-5.4 pricing.

The draft schema was compacted after the pilot:

- at most three simplification decisions;
- at most two interpretive expansions;
- at most two risk flags;
- short, non-repetitive evidence statements; and
- removal of redundant required narrative fields already represented elsewhere.

On the same three 1 Peter calibration passages, compact Sol reduced completion
tokens by roughly 18–37% while retaining the understanding-first behavior.

GPT-5.4-mini was also tested as a cheaper primary drafter. It produced good
plain English for 1 Peter 1:13, but reverted to “sober-minded” in 1 Peter 4:7 and
kept the less explicit “stay alert” in 1 Peter 5:8 despite the calibration rule.
It is therefore suitable for low-risk assistance, not as the controlling drafter
for doctrine-sensitive passages. Corpus inspection found only about 5–9% of POB
records met a conservative low-risk rule; most records carry footnotes or
theological decisions. Sol remains the primary drafter.
