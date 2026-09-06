# Unflagged OT English sample: frozen selection contract

Declared 2026-09-05 before running the selection or inspecting selected verse
content. Seed: `POB-unflagged-2026-09-05-v1`. This is one judge's first pass,
not a blinded comparison, independent second review, or publication approval.

## Population and deterministic selection

Enumerate `translation/ot/*/*/*.yaml`, in bytewise relative POSIX path order.
Use the 39-book Protestant OT partitioned according to the Tanakh: Torah =
Genesis, Exodus, Leviticus, Numbers, Deuteronomy; Prophets = Joshua, Judges,
1–2 Samuel, 1–2 Kings, Isaiah, Jeremiah, Ezekiel, and the Twelve; Writings =
Ruth, 1–2 Chronicles, Ezra, Nehemiah, Esther, Job, Psalms, Proverbs,
Ecclesiastes, Song of Songs, Lamentations, Daniel.

An eligible record has nonempty source and English, source edition WLC or
UHB, no footnote signals from the existing `footnote_signals` function in
`tools/textual_restoration/build_variant_inventory.py`, no nonempty source
apparatus, and no editorial source markers `⸀⸁⸂⸃⸄⸅[]<>`.
Additionally require that its source text matches exactly one verse in the
same book's local WLC XML after comparison normalization. That WLC verse must
contain no `note` element. The normalization keeps Hebrew letters, vowel
points, dagesh, shin/sin dots, and their order; ignores accents, meteg,
punctuation, whitespace and segmentation slashes. This is a conservative
content alignment, not an assumption that verse numbering agrees. A source
with a different vocalization is excluded rather than silently reconciled.

For each eligible path compute UTF-8 SHA256 of
`seed + NUL + stratum + NUL + relative_path`, where strata are exactly
`torah`, `prophets`, `writings`. Select the minimum hex digest in each
stratum, breaking any digest tie by relative path. Do not redraw for an
awkward, uninteresting, or uncertain result. Record eligible and excluded
counts, ranked winner, full-corpus path/hash digest, eligible-list digest,
source file hashes, and selection-tool/declaration hashes in the receipt.
No English wording participates in ranking or eligibility beyond nonempty
presence and the declared textual-note screen.

“Source-stable” here means an unflagged, aligned local Masoretic base for a
bounded rendering assessment. It does not mean that an exhaustive critical
apparatus or all manuscripts have established absence of variants.

## Evaluation contract

After freezing the winners, inspect their entire chapters in POB and Hebrew,
and name the relevant paragraph or literary unit before comparison. Pin the
canonical YAMLs, context YAMLs, WLC XML and directly consulted controls by
SHA256. The target source is each record's existing pointed Masoretic text;
do not select another textual reading to improve the English. Record any
source-interpretation issue separately and hold it if unresolved.

Compare the current English, a close source gloss, and (where useful) a
concrete candidate. Apply DOCTRINE.md's optimal-equivalence, modern-English,
name, ambiguity and justified-consistency commitments. Assess in order:
meaning/agency, omitted or unsupported content, preserved ambiguity,
literary function, naturalness, consistency. A change requires an identifiable
gain on one of these dimensions with no known semantic regression; purely
equivalent preference is a tie/retain. Hold unresolved source analysis or
unsettled semantic tradeoffs. For every result retain the strongest
counterargument, bounded qualitative confidence, and reopening condition.

Report the denominator (3), changes, retains/ties and unresolved outcomes,
and any candidate regression found. These are judgments, not accuracy
percentages, publication decisions, or a corpus-wide improvement result.
The evaluator sees current POB and generates candidates: no blind candidate
identity or randomized presentation claim is allowed. Lexicon labels already
in YAML do not count as new consultations. Cite actual consulted resources;
do not copy entire dictionaries or copyrighted corpora.
