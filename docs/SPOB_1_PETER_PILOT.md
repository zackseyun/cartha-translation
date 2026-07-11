# SPOB understanding-first pilot: 1 Peter

Completed: 2026-07-10

## Result

The complete book of 1 Peter is now drafted as SPOB under the
understanding-first doctrine.

- **105 / 105 records drafted**
- **105 / 105 records schema-valid**
- **61 records contain an explicit interpretive expansion**
- **80 interpretive expansions are individually documented**
- **45 records received at least one grounding-driven revision**
- **55 revision events are preserved in the public YAML audit trail**
- **0 blocked verses**
- **0 low-confidence expansions allowed into the text**

GPT-5.6 Sol drafted and revised the text. GPT-5.6 Terra independently
reviewed the full book for faithfulness, clarity, ambiguity preservation, and
doctrinal overreach. The latest full-book review produced 77 direct approvals
and 28 change requests. Twenty-seven of those requests were applied in a second
revision pass. The remaining request—1 Peter 5:8—was explicitly adjudicated by
the project editor rather than silently accepted or ignored.

## Adjudicated calibration verse

Final SPOB, 1 Peter 5:8:

> **Keep a clear mind and stay spiritually awake. Your adversary, the devil,
> walks around like a roaring lion, looking for someone to devour.**

Terra's conservative review preferred “stay alert,” arguing that “spiritually”
narrows a broadly applicable vigilance command. The project editor retained
“stay spiritually awake” because:

1. the immediate context explicitly identifies the devil as the threat;
2. the lion image depicts spiritual attack;
3. the POB lexical record already describes wakeful vigilance in that setting;
4. the two source commands remain distinct: clear-mindedness is not merged with
   spiritual wakefulness; and
5. “stay alert,” “be watchful,” and “keep watch” remain documented alternatives.

The YAML records the reviewer dissent and editorial basis under
`editorial_adjudications`. This is the intended SPOB governance pattern: models
surface the danger, evidence is recorded, and a contested choice remains visible.

## Examples of understanding-first improvements

### 1 Peter 1:13

> Therefore, get your minds ready for action. Be fully clear-minded, and set
> your hope completely on the grace being brought to you when Jesus the Messiah
> is revealed.

The unfamiliar “gird up the loins of your mind” idiom becomes its documented
meaning while a footnote preserves the embodied source image.

### 1 Peter 2:1

> Therefore, having left behind every kind of ill will and deceit, every form of
> hypocrisy and envy, and all harmful talk against others,

“Malice” and “slanders” become immediate modern English without weakening the
ethical command.

### 1 Peter 4:7

> But the end of all things is near. So control yourselves and keep your minds
> clear, so that you can pray.

The purpose of the paired commands is made explicit from the POB lexical audit:
they prepare believers for prayer.

## What the review caught

The grounding pass corrected issues such as:

- turning a source purpose clause into a prediction;
- making two related Greek phrases more identical than the source warrants;
- adding a contextual implication too confidently;
- moving a footnote marker away from the phrase it explains;
- retaining wording that was technically accurate but still unclear;
- weakening a command into advice; and
- losing a meaningful ambiguity in explanatory prose.

No review issue was high severity. The second pass also exposed a pipeline bug:
a failed revised record could be written before validation. Revision writes are
now validated in a temporary file and atomically replace the verse only after
passing.

## Scale decision

The pilot supports scaling with this role separation:

1. **Sol drafts** understanding-first SPOB.
2. **Terra reviews** source grounding and interpretive risk.
3. **Sol revises** accepted review findings.
4. **Human adjudication** resolves genuine philosophy disputes rather than
   averaging model outputs.
5. **Luna challenges clarity** selectively when a passage remains too close to
   POB or when Sol and Terra converge on wording that is still hard to understand.

Full-corpus scaling should continue in book-sized checkpoints so cost, style,
and doctrinal drift remain observable.
