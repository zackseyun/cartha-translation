# Genesis and Luke SPOB pilot results

## Outcome

The calibration pilot contains **418 SPOB verses**:

- Genesis 1, 3, 4, 16, and 32: **130 verses**
- Luke 1, 4, 10, 15, 17, and 24: **288 verses**

All 418 records pass structural validation. Terra's first grounding review
approved 303 and requested revisions to 115. Successive Sol revision and Terra
review passes reduced the unresolved set from 115 → 27 → 9 → 3 → 2. The last
two recommendations were applied through recorded editorial adjudications. No
verse was blocked.

The result is meaningfully different from POB rather than a cosmetic wording
swap. Mean POB↔SPOB lexical similarity is **0.727 in Genesis** and **0.724 in
Luke**. Average verse length fell from 27.3 to 25.5 words in the Genesis pilot
and from 22.3 to 21.6 words in Luke, while difficult idioms often became longer
because SPOB explains rather than merely compresses them.

## Representative comparisons

| Passage | POB | SPOB | What changed |
|---|---|---|---|
| Genesis 1:1 | “In the beginning, when God created the heavens and the earth…” | “When God began to create the heavens and the earth…” | Makes the audited dependent-clause reading immediately followable. |
| Genesis 4:7 | “If you do well… sin is crouching at the door; its desire is for you…” | “If you do what is right… sin is crouching at the door like a beast. It desires to have you…” | Explains acceptance and makes the governing image visible without removing its source terms. |
| Luke 1:37 | “For no word from God will be impossible.” | “For no word God speaks will be impossible for him to fulfill.” | Communicates the saying as the unfailing power of God's spoken word. |
| Luke 4:18 | “proclaim release to the captives… send out the oppressed in release” | “announce freedom for captives… set oppressed people free” | Replaces technical repetition with ordinary liberation language while retaining footnotes. |
| Luke 10:6 | “if a son of peace is there” | “If a son of peace is there—someone marked by peace or receptive to the peace you bring…” | Keeps the biblical phrase and immediately explains its contextual sense. |
| Luke 17:21 | “the kingdom of God is in your midst” | “the kingdom of God is already here among you” | Prevents an exclusively private/inward reading while preserving the live alternative in a note. |
| Ecclesiastes 1:2 | “Breath of breaths… all is mere breath.” | “Vapor of vapors… Everything is vapor—brief, impossible to hold onto, and often not what we expect.” | Makes *hevel* and its governing image intelligible without changing it into “nothing matters.” |

## Divergence findings

The lexical reference panel compares POB and SPOB with BSB, WEB, ASV, and KJV;
Brenton is retained as source-tradition context but excluded from consensus.
Highest-priority pilot passages include:

| Genesis | Priority | Luke | Priority |
|---|---:|---|---:|
| Genesis 4:7 | 47.47 | Luke 10:21 | 52.69 |
| Genesis 4:15 | 46.13 | Luke 4:37 | 47.51 |
| Genesis 16:13 | 45.53 | Luke 10:4 | 47.20 |
| Genesis 4:14 | 45.48 | Luke 24:22 | 46.65 |
| Genesis 3:21 | 42.19 | Luke 1:37 | 46.62 |

The average public-reference similarity is lower for SPOB than POB (Genesis
0.648 versus 0.780; Luke 0.650 versus 0.757). This is expected because the
public panel generally preserves traditional/literal wording while SPOB often
makes an audited contextual implication explicit. It is also a useful warning:
large drops should continue to receive grounding review rather than being
treated automatically as improvements.

Luke 17:36 is validated in the pilot but omitted from lexical consensus scoring
because the public reference panel does not supply the same textual/verse unit.

## NKJV, NIV, and NLT status

The report schema and private fetcher now support all three licensed
translations. No authorized commercial corpus was available during this run, so
their score fields correctly remain `null` rather than presenting scraped or
invented results.

| Translation | Adapter | Licensed text loaded | Published result |
|---|---|---|---|
| NKJV | Ready | No | Numeric comparison pending license/configuration |
| NIV | Ready | No | Numeric comparison pending explicit AI-use permission |
| NLT | Ready | No | `pob_nlt_similarity`, `spob_nlt_similarity`, and gain fields pending authorized input |

When authorized text is loaded, the committed reports retain only numeric
similarities and non-sensitive provenance; the licensed wording stays in the
gitignored private cache and does not influence drafting or review priority.
