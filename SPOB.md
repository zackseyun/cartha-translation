# Simplified People's Open Bible (SPOB)

The **Simplified People's Open Bible (SPOB)** is a plain-language English edition derived from the People's Open Bible.

POB remains the fully auditable translation layer: original source text, lexical decisions, theological decisions, footnotes, revision history, and public review. SPOB is the readability layer: it keeps that reasoning intact while making the wording easier for modern readers to understand.

## Why SPOB exists

Some readers want maximum source-language pressure in the main sentence. That is what POB is for.

Other readers need the same meaning in clearer, more immediate English. SPOB is for them.

SPOB aims to be:

- **clear** — common modern English, fewer academic turns of phrase;
- **actually simpler** — difficult main-text wording should be rewritten into
  an understandable representation, not merely lightly polished;
- **faithful** — no flattening of POB's documented source decisions;
- **dignified** — readable without becoming casual, childish, or devotional paraphrase;
- **auditable** — every simplified verse points back to its POB source record.

## What SPOB is not

- Not a replacement for POB.
- Not a new independent original-language translation pass.
- Not a paraphrase that invents meaning beyond the source.
- Not a study Bible or commentary folded into the text.

## Relationship to POB

POB is the controlling base. SPOB may compress, clarify, or split difficult wording, but it must preserve:

- the core POB rendering;
- important source-language images;
- documented lexical and theological decisions;
- meaningful alternate readings and textual variants;
- tension that POB intentionally leaves unresolved.

The result should read like a separate English Bible edition, but one whose public audit trail remains anchored in POB.

## Translation doctrine

The operational rules for understanding-first rendering, interpretive expansion,
and the use of named teachers or traditions are defined in
[SPOB_DOCTRINE.md](SPOB_DOCTRINE.md).

The reader-facing summary of the edition's translation philosophy and production
method is in [SPOB_PHILOSOPHY.md](SPOB_PHILOSOPHY.md).

The short version is: SPOB may express a passage's contextual meaning more
directly than POB, but every interpretive addition must be warranted and recorded.
No individual teacher or denomination controls the main text.

## Corpus status

As of July 12, 2026, the repository contains **43,105 schema-valid SPOB
records**, covering every current POB source record across the canonical,
deuterocanonical, and extra-canonical collections. Every record completed the
canon-wide Azure review pass:

- 43,065 received a substantive GPT-5.6 Terra grounding verdict;
- all 17,137 substantive `revise` or `block` recommendations were applied and
  revalidated through GPT-5.6 Sol;
- 40 passages that Azure's content policy would not inspect were separately
  adjudicated against their POB base and preserved without an automated
  doctrinal guess.

The completion and editorial-block audit is recorded in
[docs/SPOB_CANON_WIDE_REVIEW_2026-07-12.md](docs/SPOB_CANON_WIDE_REVIEW_2026-07-12.md).
