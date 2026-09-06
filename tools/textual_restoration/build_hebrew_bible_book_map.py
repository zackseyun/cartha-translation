#!/usr/bin/env python3
"""All-39-book, metadata-only QDR map; labels and brackets are not ink evidence."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from tools.textual_restoration.build_qdr_discovery import BOOKS, ALIASES, COMMIT, INPUT_SHA, NS, sha

ROOT = Path(__file__).resolve().parents[2]
DIR = "sources/textual_restoration/discovery/"
OUT = ROOT / (DIR + "hebrew_bible_book_map.v1.json")
REPORT = ROOT / "docs/HEBREW_BIBLE_BOOK_WITNESS_MAP_2026-09-05.md"
INPUTS = [
    DIR + "qumran_digital_catalogue_index.v1.json",
    DIR + "catalogue_identity_holds.v1.json",
    DIR + "qumran_catalogue_identity_followup.v1.json",
    DIR + "leviticus_catalogue_targets.v1.json",
    DIR + "isaiah_catalogue_targets.v1.json",
    "sources/textual_restoration/ot_witness_registry.v1.json",
]
SYNTAX_KEYS = ["all_hebrew_letters_inside_square_brackets",
               "hebrew_letters_both_inside_and_outside_square_brackets",
               "no_hebrew_letters_inside_square_brackets",
               "unresolved_fragment_bracket_syntax", "no_hebrew_letters"]


def label_key(label):
    return re.sub(r"[\s.]", "", label).casefold()


def reference_kind(value, labels):
    """No numbering correction or source-locator-to-Bible inference."""
    m = re.fullmatch(r"([A-Za-z0-9]+) ([0-9]+):([0-9]+)", value)
    if m and m[1] in ALIASES:
        return "biblical_reference", f"{ALIASES[m[1]]}.{int(m[2])}.{int(m[3])}"
    if not value:
        return "empty", None
    parts = value.split(" ", 1)
    if (len(parts) == 2 and label_key(parts[0]) in labels
            and re.fullmatch(r"f[^\s:]+:[0-9]+", parts[1])):
        return "source_fragment_line_reference", None
    if (len(parts) == 2 and label_key(parts[0]) in labels
            and re.fullmatch(r"[0-9]+:[0-9]+", parts[1])):
        return "source_numeric_locator_reference", None
    return "unresolved", None


def bracket_classes(words):
    """Syntactic diagnostics only. Reject unmatched/nested bracket fragments.

    State crosses words, references, and lines within each source fragment.
    Neither balanced syntax nor outside-bracket letters prove surviving ink.
    """
    depth, valid = 0, True
    for word in words:
        for ch in word[1]:
            if ch == "[":
                depth += 1
                if depth > 1:
                    valid = False
            elif ch == "]":
                depth -= 1
                if depth < 0:
                    valid = False
    valid = valid and depth == 0
    depth = 0
    result = []
    for word in words:
        inside = outside = 0
        for ch in word[1]:
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
            elif "א" <= ch <= "ת":
                if depth:
                    inside += 1
                else:
                    outside += 1
        if not inside + outside:
            result.append(SYNTAX_KEYS[4])
        elif not valid:
            result.append(SYNTAX_KEYS[3])
        else:
            result.append(SYNTAX_KEYS[1 if inside and outside else 0 if inside else 2])
    return result


def scan(corpus):
    if not isinstance(corpus, list) or not corpus:
        raise ValueError("nonempty QDR record array required")
    labels = Counter()
    for record in corpus:
        if not isinstance(record.get("scroll"), str) or not record["scroll"]:
            raise ValueError("missing source label")
        labels[record["scroll"]] += 1
    known = {label_key(s) for s in labels}
    pairs, references, spellings = {}, defaultdict(set), defaultdict(Counter)
    kinds, other, source_local_mismatches = Counter(), defaultdict(Counter), Counter()
    totals = Counter()
    zero_records, unresolved_values = [], Counter()
    for ri, record in enumerate(corpus):
        record_books = set()
        for fi, fragment in enumerate(record["fragments"]):
            words = []
            locations = []
            for li, line in enumerate(fragment["lines"]):
                for wi, word in enumerate(line["words"]):
                    if (not isinstance(word, list) or len(word) != 6
                            or not all(isinstance(s, str) for s in word)):
                        raise ValueError(f"malformed word in record {ri}")
                    words.append(word)
                    locations.append({"fragment_index": fi, "fragment": str(fragment["id"]),
                                      "line_index": li, "line": str(line["n"]), "word_index": wi})
            for word, location, syntax in zip(words, locations, bracket_classes(words)):
                totals["word_records"] += 1
                kind, reference = reference_kind(word[5], known)
                kinds[kind] += 1
                if reference is None:
                    prefix = word[5].split(" ")[0] if word[5] else "(empty)"
                    other[prefix][kind] += 1
                    if kind == "unresolved":
                        unresolved_values[word[5]] += 1
                    if kind.startswith("source_") and label_key(prefix) != label_key(record["scroll"]):
                        source_local_mismatches[(record["scroll"], prefix)] += 1
                    continue
                book = reference.split(".")[0]
                record_books.add(book)
                spellings[book][word[5].split(" ")[0]] += 1
                references[book].add(reference)
                key = book, ri
                if key not in pairs:
                    pairs[key] = {"label": record["scroll"], "source_record_index": ri,
                                  "references": set(), "syntax": Counter(), "word_tags": 0,
                                  "first_locator": {**location, "source_reference": word[5]},
                                  "hash_or_question_marker_word_tags": 0}
                row = pairs[key]
                row["references"].add(reference)
                row["word_tags"] += 1
                row["syntax"][syntax] += 1
                row["hash_or_question_marker_word_tags"] += bool(re.search(r"[#?]", word[1]))
        totals["records_without_biblical_tags"] += not record_books
        if not record_books:
            zero_records.append({"source_record_index": ri, "label": record["scroll"],
                                 "status": "no-biblical-reference-tag-book-unassigned"})
    return dict(labels=labels, pairs=pairs, references=references, spellings=spellings,
                kinds=kinds, other=other, totals=totals, mismatches=source_local_mismatches,
                zero_records=zero_records, unresolved_values=unresolved_values)


def load_inputs(root):
    loaded, receipts = {}, []
    for name in INPUTS:
        raw = (root / name).read_bytes()
        loaded[Path(name).name] = json.loads(raw)
        receipts.append({"path": name, "sha256": sha(raw)})
    return loaded, receipts


def build(qdr, root=ROOT):
    raw = qdr.read_bytes()
    if sha(raw) != INPUT_SHA:
        raise ValueError("QDR differs from pinned snapshot")
    corpus = json.loads(raw)
    data = scan(corpus)
    inputs, receipts = load_inputs(root)
    index = inputs["qumran_digital_catalogue_index.v1.json"]
    candidates = defaultdict(list)
    for entry in index["entries"]:
        for label in entry["qdr_labels"]:
            candidates[label].append({k: entry[k] for k in
                                     ("display_label", "catalogue_class", "url", "match_status")})
    roles = defaultdict(list)
    supplemental_no_label = []
    for filename in ("leviticus_catalogue_targets.v1.json", "isaiah_catalogue_targets.v1.json"):
        target = inputs[filename]
        for row in target["entries"]:
            if not any(label in data["labels"] for label in row["query_labels"]):
                supplemental_no_label.append({"book_scope": target["book"], "target": row["id"],
                                              "role": row["role"], "query_labels": row["query_labels"],
                                              "source": DIR + filename,
                                              "status": "no-query-label-in-pinned-QDR-not-physical-absence"})
            for label in row["query_labels"]:
                roles[label].append({"target": row["id"], "role": row["role"],
                                     "source": DIR + filename, "book_scope": target["book"]})
    follow = inputs["qumran_catalogue_identity_followup.v1.json"]
    holds = defaultdict(set)
    for row in follow["content_crosswalks"]:
        holds[row["qdr_label"]].add("genesis-label-collision")
    for row in follow["decisions"]:
        for ri in row.get("qdr_record_indices", []):
            holds[corpus[ri]["scroll"]].add(row["id"])
    holds["4Q24"].add("leviticus-proposed-split-not-physical-crosswalk")
    holds["4Q29"].add("4q54a-4q47a-published-challenge")
    holds["Arugleviticus"].add("XLeviticus-bibliographic-identity-pending")
    books = []
    for book, slug in BOOKS.items():
        path = root / f"sources/ot/wlc/{book}.xml"
        wraw = path.read_bytes()
        wrefs_list = [v.get("osisID") for v in ET.fromstring(wraw).findall(".//o:verse", NS)]
        if not all(wrefs_list) or len(set(wrefs_list)) != len(wrefs_list):
            raise ValueError("missing or duplicate WLC verse ID")
        wrefs = set(wrefs_list)
        refs = data["references"][book]
        rows, syntax_total = [], Counter()
        for (b, ri), row in sorted(data["pairs"].items()):
            if b != book:
                continue
            label = row["label"]
            syntax_total.update(row["syntax"])
            rows.append({"source_record_index": ri, "label": label,
                         "label_occurrences_in_corpus": data["labels"][label],
                         "indexed_reference_anchors": len(row["references"]),
                         "word_reference_tags": row["word_tags"],
                         "bracket_syntax_word_counts": {k: row["syntax"][k] for k in SYNTAX_KEYS},
                         "hash_or_question_marker_word_tags": row["hash_or_question_marker_word_tags"],
                         "one_discovery_locator": row["first_locator"],
                         "catalogue_label_candidates": candidates[label],
                         "source_reported_role_candidates": [r for r in roles[label] if r["book_scope"] == book],
                         "identity_hold_ids": sorted(holds[label]),
                         "reading_support": "not-assessed"})
        books.append({"book": slug, "wlc_book": book,
                      "wlc_verse_anchor_denominator": len(wrefs),
                      "qdr_indexed_reference_anchors": len(refs),
                      "same_label_wlc_anchor_intersection": len(refs & wrefs),
                      "wlc_anchors_without_qdr_reference_tag": len(wrefs - refs),
                      "qdr_anchors_not_in_wlc": sorted(refs - wrefs),
                      "qdr_source_records": len(rows),
                      "qdr_distinct_labels": len({r["label"] for r in rows}),
                      "labels_without_raw_catalogue_candidate": sorted({r["label"] for r in rows if not r["catalogue_label_candidates"]}),
                      "source_reference_spelling_counts": dict(data["spellings"][book]),
                      "bracket_syntax_word_counts": {k: syntax_total[k] for k in SYNTAX_KEYS},
                      "index_status": "hits" if rows else "zero-hits-in-pinned-QDR-only",
                      "primary_family_gaps": ["masoretic-codices-and-critical-apparatus",
                                              "judean-desert-identity-and-preservation",
                                              "old-greek-and-revisions-apparatus",
                                              "syriac-and-other-versional-manuscripts",
                                              "quotations-and-liturgical-excerpts"]
                      + (["samaritan-manuscripts-and-critical-apparatus"] if book in list(BOOKS)[:5] else []),
                      "source_records": rows})
        receipts.append({"path": str(path.relative_to(root)), "sha256": sha(wraw)})
    kinds = data["kinds"]
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-05",
        "scope": "All 39 canonical OT books against one pinned QDR biblical dataset and saved catalogue metadata; not all known witnesses",
        "source": {"commit": COMMIT, "sha256": INPUT_SHA,
                   "url": f"https://github.com/evenderekh/qdr/tree/{COMMIT}",
                   "file": "data/qdr.1.1.biblical.json",
                   "attribution": "Qumran Digital Reader, Michael Muzar; ETCBC/Naaijer/Abegg-derived data",
                   "license": "CC BY-NC 4.0", "export": "Aggregate factual metadata and one source locator per book-record pair; no text, morphology or full verse index"},
        "policy": {"count_unit": "source records and labels, never authenticated independent manuscripts",
                   "record_index_basis": "zero-based pinned top-level ordinal; fragment, line and word indices also zero-based",
                   "anchor_denominator": "WLC OSIS verse elements, including heading/numbering conventions; same-label overlap only, not text alignment or surviving verse percentage",
                   "bracket_diagnostics": "Mechanical square-bracket syntax across all words/lines of each fragment; entire unbalanced/nested fragment unresolved. No outside-bracket word is certified direct, complete, legible or ancient. Supplied/partial wording needs edition and image checks.",
                   "hash_question_diagnostics": "Literal # or ? present; not an independently validated uncertainty classification",
                   "source_local_references": "Unassigned biblical location; a manuscript-like prefix is not mapped to a book from neighboring words or manuscript name",
                   "catalogue_classes": "Pragmatic source classes only; biblical class does not distinguish continuous copy from tefillin/mezuzot; non-biblical class does not prove absence of biblical quotation",
                   "zero_hits_prove_absence": False, "all_source_completeness": False,
                   "physical_manuscript_count": None, "canonical_change_applied": False},
        "summary": {"canonical_book_denominator": 39, "source_records": sum(data["labels"].values()),
                    "distinct_source_labels": len(data["labels"]), **dict(data["totals"]),
                    "reference_kind_counts": dict(kinds), "book_record_pairs": sum(b["qdr_source_records"] for b in books),
                    "books_with_hits": sum(bool(b["qdr_source_records"]) for b in books),
                    "zero_hit_books": [b["book"] for b in books if not b["qdr_source_records"]],
                    "wlc_verse_anchor_denominator": sum(b["wlc_verse_anchor_denominator"] for b in books)},
        "nonbiblical_reference_prefix_accounting": [
            {"prefix": prefix, "word_tag_counts": dict(counts)} for prefix, counts in sorted(data["other"].items())],
        "records_without_biblical_tags": data["zero_records"],
        "unresolved_reference_values": [{"value": value, "word_tags": n}
                                        for value, n in sorted(data["unresolved_values"].items())],
        "supplemental_catalogue_role_targets_without_qdr_query_label": supplemental_no_label,
        "source_local_prefix_disagreements": [
            {"record_label": pair[0], "reference_prefix": pair[1], "word_tags": n,
             "status": "retain-source-spelling-no-physical-join"} for pair, n in sorted(data["mismatches"].items())],
        "identity_collision_records": [{"label": label, "source_records": n,
                                        "independent_manuscript_count": None}
                                       for label, n in sorted(data["labels"].items()) if n > 1],
        "catalogue_discrepancy_queue": {
            "labels_without_candidate": index["qdr_labels_without_exact_or_typography_candidate"],
            "biblical_class_without_candidate": index["biblical_class_entries_without_label_candidate"],
            "matches_outside_biblical_class": index["exact_matches_outside_biblical_class"],
            "hold_sources": [DIR + "catalogue_identity_holds.v1.json", DIR + "qumran_catalogue_identity_followup.v1.json"],
            "warning": "Syntax queues are frozen prior results, not new or absent physical manuscripts. 4Q54b/4Q69c share a held evidence unit; 4Q54a/4Q47a face a 4Q29-fragment-3 reassignment challenge; XAmos authenticity is held. No automatic joins."},
        "family_gap_basis": "Coverage audit 2026-09-04 and saved OT registry: these families still need systematic book/object/variation-unit maps. Existing selected-case consultation is not denied; the current pass does not certify whole-book collation. Targum applicability must be assigned book-specifically, not presumed across all Writings.",
        "books": books, "local_inputs": receipts,
    }


def report(result):
    s = result["summary"]
    syntax = Counter()
    for book in result["books"]:
        syntax.update(book["bracket_syntax_word_counts"])
    lines = ["# Hebrew Bible: all-39-book witness discovery map — 2026-09-05", "",
             "This is an executed corpus-wide **discovery map**, not a count of ancient manuscripts or a preserved-text coverage percentage. It makes every canonical OT book explicit, including zero hits. It supplements the frozen prior receipts and changes no source or English text.", "",
             f"The pinned QDR corpus contains {s['source_records']} records / {s['distinct_source_labels']} labels and {s['word_records']:,} word records. There are {s['book_record_pairs']} book–record pairs across {s['books_with_hits']} books. Zero-hit books: **{', '.join(s['zero_hit_books'])}**. A zero means no biblical reference tag in this file, not no surviving witness or no project base text.", "",
             "[JSON receipt](../sources/textual_restoration/discovery/hebrew_bible_book_map.v1.json) records every contributing label and record ordinal, one exact nested locator per book–record pair, source reference spellings, catalogue label candidates, role candidates and inherited holds. It exports neither transcription nor a full verse-to-manuscript index. QDR remains CC BY-NC 4.0.", "",
             "| Book | WLC anchors | QDR anchors | Same-label overlap | Records / labels |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for b in result["books"]:
        lines.append(f"| {b['book']} | {b['wlc_verse_anchor_denominator']} | {b['qdr_indexed_reference_anchors']} | {b['same_label_wlc_anchor_intersection']} | {b['qdr_source_records']} / {b['qdr_distinct_labels']} |")
    lines += ["", "The WLC denominator is verse-element count, including its headings and numbering conventions. QDR/WLC intersection is a same-label comparison: it does not verify reference alignment, continuous preservation, literary order, or the decisive letters. Book/record totals are not additive independent-witness totals, because one source record can index multiple books.", "",
              "## Reference and preservation accounting", "",
              f"All {s['word_records']:,} word records partition into {s['reference_kind_counts']['biblical_reference']:,} biblical tags, {s['reference_kind_counts']['source_fragment_line_reference']:,} source fragment/line tags, {s['reference_kind_counts']['source_numeric_locator_reference']:,} source numeric locator tags, and {s['reference_kind_counts']['empty']} empty references. There are {s['reference_kind_counts'].get('unresolved', 0)} unresolved reference values. Only explicit book spellings are normalized (`Ex` → `Exod`, `Is` → `Isa`); manuscript/fragment/line tags stay unassigned to a biblical passage. The numeric locators occur under 1Q8 and Mur88; their missing `f` is retained, not silently repaired. The receipt accounts for every nonbiblical prefix and all source-prefix disagreements.", "",
              "Three entire source records have no biblical tag: **Pam43113, Pam43124 and X4**. They remain book-unassigned instead of disappearing from the 266-record denominator. The sole recognized tag outside the WLC anchor set is **Josh 5:0** (19 word tags); it is retained as a numbering/alignment issue.", "",
              "The bracket diagnostics distinguish all Hebrew letters inside square brackets, mixed inside/outside letters, no letters inside, no Hebrew letters, and unresolved fragment syntax. State crosses verse and line boundaries within each fragment. Any unbalanced or nested fragment is wholly unresolved for letter classification. These are **syntax bins**, not directly preserved / supplied / partial manuscript counts: even balanced brackets cannot establish damaged ink, omitted brackets, correction hands, authenticity, or continuity across physical fragments. The first locator is a discovery example only and may point wholly into supplied wording.", "",
              f"Among biblical-tagged word records, {syntax[SYNTAX_KEYS[0]]:,} have all Hebrew letters inside balanced square brackets, {syntax[SYNTAX_KEYS[1]]:,} mix inside/outside letters, {syntax[SYNTAX_KEYS[2]]:,} have none inside, {syntax[SYNTAX_KEYS[4]]:,} have no Hebrew letters, and **{syntax[SYNTAX_KEYS[3]]:,} remain unresolved because their source fragment has unbalanced/nested bracket syntax**. This large unresolved remainder is a reason to acquire edition-context evidence before counting direct-word coverage.", "",
              "## Identity, genre and acquisition queues", "",
              "The six index matches outside the biblical class (2Q29, 4Q88, 4Q249j, 4Q483, 11Q5, 11Q6) remain visible. Biblical-class membership does not distinguish continuous copies from liturgical excerpts. Existing Leviticus/Isaiah catalogue role reports are linked with their book scope; quoted, cryptic, reworked and pesher targets remain separate from continuous-copy claims. No genre is inferred from a verse hit.", "",
              "4Q8a/4Q8b have known cross-project content conflicts; 4Q8c/4Q8d have candidate content crosswalks, not verified physical aliases. 4Q483 ordinals 2 and 209 remain distinct records under one colliding label, with no independent manuscript count. The 4Q24 proposed split remains held. 4Q54b/4Q69c must not supply two independent votes; 4Q54a/4Q47a face the 4Q29 fragment 3 challenge. XAmos authenticity and XLeviticus/Arugleviticus identity remain held. See the [identity follow-up](QUMRAN_CATALOGUE_IDENTITY_FOLLOWUP_2026-09-05.md) and linked receipts.", "",
              "The 13 unmatched catalogue names and nine unmatched QDR labels remain acquisition/identity queues, not 22 missing manuscripts. The present index provides no book assignment for every unmatched label; this map deliberately does not invent one. The already published 4Q103a is a concrete example of why an absent index label is not an absent source.", "",
              "The QDR-side raw label mismatches now have an explicit book queue: Genesis — 4Q8c, 4Q8d, 4Q12a; Leviticus — 4Q26c, Arugleviticus; Deuteronomy — 4Q38c, 4Q38d; Proverbs — 4Q103a; book-unassigned — X4. Known content crosswalks and holds qualify these queues; they do not erase the original syntax mismatch. The receipt separately exports all 18 target rows without QDR query labels from the held Leviticus/Isaiah catalogues, including Greek, Aramaic, quoted, rewritten and pesher lanes. These selected source lists are not expanded into an invented all-book quotation census.", "",
              "For 1 Chronicles, Nehemiah and Esther, start from the extant Masoretic controls and book-specific critical apparatus, then independent catalogue discovery; QDR cannot provide positive book tags here. For every other book, resolve its per-record identity/genre and exact-word preservation before claiming support. All 39 rows retain primary-family gaps: Masoretic codices/apparatus, broader Judean Desert census and physical mapping, Greek/revision apparatus, Syriac/other versions, and quotations. All five Torah books additionally retain Samaritan manuscript/critical-apparatus gaps despite the completed reference-edition screen. Aramaic portions remain Aramaic. Targum applicability requires book-specific investigation.", "",
              "These family flags are the prior audit's remaining systematic work, not a claim that no selected passages have been consulted. The map does not yet close the audit's all-institutional-catalogue criterion. This pass reads saved authoritative receipts and pinned data; it does not claim a fresh online catalogue or apparatus consultation.", "",
              "## Reproduce", "", "```sh",
              ".venv/bin/python -m tools.textual_restoration.build_hebrew_bible_book_map --qdr /private/tmp/pob-qdr/data/qdr.1.1.biblical.json --check",
              ".venv/bin/python -m unittest tests.test_hebrew_bible_book_map", "```", "",
              "The builder rejects a changed QDR hash, saves the hashes of all 39 WLC files and every local evidence input, and regenerates this report and the bounded JSON. Private upstream bytes must be retained separately for offline reproduction. Tests verify accounting and conservative boundaries, not ancient textual truth.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qdr", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.qdr)
    outputs = {OUT: json.dumps(result, ensure_ascii=False, indent=2) + "\n", REPORT: report(result)}
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f"stale or missing output: {path}")
        else:
            path.write_text(content)
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
