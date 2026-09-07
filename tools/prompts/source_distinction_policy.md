# Source-distinction review contract — v1 (2026-09-06)

Source fidelity is the objective; familiar or merely defensible English is not
proof that we have found the best rendering. Compare the strongest natural,
source-transparent English candidate before accepting the existing wording.

1. Read the source and passage context before treating the existing draft or
   its rationale as an answer key. Check repeated dialogue, changes of verbs,
   different source words collapsed into one English word, repeated source
   words dispersed into different English words, wordplay, emphasis, and
   grammatical contrasts in Greek AND Hebrew.
2. A footnote or prior lexical rationale is evidence to examine, NOT an
   exemption from review. Describing a distinction in a note does not by
   itself preserve it in the English reading text. Distinguish confidence in
   an observation about wording from claims about its theological meaning.
3. For each supplied candidate, return `source_distinction_checks` with:
   `candidate_id`, `disposition` (preserved, propose, retain_after_comparison),
   `source_evidence` (quote actual source forms from the supplied passage),
   `proposed_text` (a FULL English verse, not just a gloss), `alternative_text`
   (a different full-verse candidate when retaining the current rendering;
   otherwise an empty string is allowed), and `rationale`
   (explain what the best candidate preserves and why it is preferable).
   In a revision writer, preserved/retained proposed_text must equal the full
   revised_text you intend to submit; in a review-only call it must equal the
   current text, copied verbatim including footnote markers. Preserve unrelated
   notes and their anchors. A different recommendation is a propose result.
   If you discover another contrast, use a `model-discovery:` candidate_id.
   Return [] only when there are no supplied or discovered candidates.
4. Prefer a natural English distinction where faithful. If English hides the
   source pattern, consider a concise source-qualified or hyphenated rendering
   and explicitly propose the best option. Do not reject a proposal merely
   because it is less conventional, was mentioned in a footnote, or requires
   reconsidering the first drafter's decision.
5. Different inflections can belong to the same lemma; different lexemes can
   overlap in context. Do not invent different meanings merely to force
   different English words. `retain_after_comparison` requires positive source
   and contextual evidence and a concrete alternative_text, not simply
   “standard”, “defensible”, “already footnoted”, or “the drafter chose it”.
   This is an audit record, not a required debate footnote in the reader.
6. `unchanged` describes an editing action, not a completed fidelity check.
   A missing required check is incomplete review, not agreement. A `propose`
   result is a retained recommendation for maintainer review, not permission
   to auto-publish it. Never silently discard that recommendation.
7. Preserve explicit maintainer-approved decisions. John 21:15–17 uses
   agape-love for ἀγαπάω and phileo-love for φιλέω in POB/SPOB. The first two
   questions use agape-love; all Peter's answers and the third question,
   including its narrative repetition, use phileo-love. This is a scoped
   English rendering policy, not a global assertion about levels of love.
