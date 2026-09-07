# OT textual-note delivery — 2026-09-07

Outcome: restored three missing links to existing source-difficulty notes.
No Hebrew selection, English wording or note-body change; no deployment.

| Record | New anchor | Existing disclosure |
|---|---|---|
| 2 Kings 15:30 | `Jotham son of Uzziah[b]` | Twentieth regnal year; compare sixteen years in local 15:33 |
| 1 Chronicles 18:4 | `7,000 horsemen[b]` | Local 2 Samuel 8:4 has 1,700; a parallel account, not another copy of Chronicles |
| 1 Chronicles 25:3 | `six[a]` | Five named sons followed by the stated total six |

The initial canonical-OT scan found these three unanchored `textual_variant`
notes. `tools/export_mobile_bible.py:reader_footnotes` excludes unreferenced
notes, so they could not reach its reader payload. The repair attaches each
note to its relevant phrase, not the first convenient punctuation. Historical
revisions also show that earlier wholesale text reverts removed anchors in
2 Kings 15:30 and 1 Chronicles 18:4; their old placements were not reused.

After repair, a normalized-marker scan of all 23,264 canonical OT records
found 248 notes tagged `textual_variant`, all referenced in their verse text,
and no notes tagged `textual_critical`. This verifies anchor presence for those
tags only, not correct placement/content of all 248 notes, exhaustive source
disclosure, other note categories, or deployed-reader coverage.

Read the three source/translation/note records and the two local parallels
above. One independent agent, `ot_note_anchor_review`, checked the exact
placements and found no material note-content blocker. Its pass is scoped to
delivery, not historical priority or comprehensive English review. The proposed
explanations of the discrepancies remain explanations, not recovered wording.

Archived the prior revision/cross-check objects verbatim under historical keys;
current status is draft/needs-review rather than inheriting whole-verse approval.
Original drafting metadata, revisions, lexical/theological decisions and all
note bodies are unchanged. Unrelated lexical notes remain unanchored: this
batch does not claim to repair every footnote or its attachment in the corpus.

Verification: schema passes for all three (one preexisting status error each
before the edit); unchanged source, marker-free English, note arrays and
historical objects; exactly one newly exported textual note per target. Actual
full-book before/after exports preserve all 719 2 Kings and 943 1 Chronicles
verse keys, with only these three output objects changed. Before exports used
the same exporter with the three Git-HEAD records overlaid. Eight existing
reader-footnote tests pass. No exporter or validator was modified.

Canonical SHA256 before → after:

- 2KI.15.30: `83b7ff275459e2c8a334943b30e81bdf223985293d538956c539923001cd0ad1` → `2b6258ba75628ab8a774ca02759d6948232af93d6e9c95e2e056d0495df4dbfe`.
- 1CH.18.4: `84f571650fa5dbf6d579495125946393c15b71fe4c17ff485e19718a3d8cc43d` → `722efea85e0ab34f64bc89226c53df53918855d825e9c057dddcd9e794f10fde`.
- 1CH.25.3: `a97747f5f93b77f71b922884372103f9ebd0b58b7f3a46cdfef589b5cfd763e1` → `61c37d35af9aadedacdf033c9ade834ea2a01fd40a4dfdc6b163f037cf8a9367`.

Stop: these delivery defects are fixed; do not repeat source acquisition or
reopen their textual histories merely because an anchor was repaired. A future
note-content or source-selection change requires its own discriminating evidence.
