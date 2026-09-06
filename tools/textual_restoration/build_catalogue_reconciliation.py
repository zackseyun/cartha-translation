#!/usr/bin/env python3
"""Reconcile explicit catalogue targets with QDR metadata, never reading support."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.build_qdr_discovery import BOOKS, INPUT_SHA, COMMIT, parse_reference, scan

TARGETS = ROOT / "sources/textual_restoration/discovery/leviticus_catalogue_targets.v1.json"
OUT = TARGETS.with_name("leviticus_catalogue_check.v1.json")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def validate_targets(targets: dict) -> None:
    if targets.get("book") not in BOOKS:
        raise ValueError("invalid book identifier")
    entries = targets.get("entries", [])
    if not entries or len({r["id"] for r in entries}) != len(entries):
        raise ValueError("empty or duplicate catalogue target IDs")
    for row in entries:
        labels = row["query_labels"]
        if not labels or len(set(labels)) != len(labels) or not all(isinstance(s, str) and s for s in labels):
            raise ValueError("empty, duplicate or invalid query labels")
        chapters = row["query_chapters"]
        if chapters is not None and (not chapters or len(set(chapters)) != len(chapters)
                                    or not all(type(c) is int and c > 0 for c in chapters)):
            raise ValueError("invalid chapter scope")
        if row["reported_status"] not in {"published", "unpublished-as-of-catalogue"}:
            raise ValueError("unrecognized catalogue publication category")


def reconcile(corpus: list[dict], targets: dict) -> dict:
    validate_targets(targets)
    indexed = scan(corpus)  # Reuse complete validated word-reference traversal.
    book = targets["book"]
    relevant = {r: h for r, h in indexed["hits"].items() if r.startswith(book + ".")}
    label_records = defaultdict(list)
    for ordinal, record in enumerate(corpus):
        label_records[record["scroll"]].append(ordinal)
    results, all_selected, matched_labels = [], set(), set()
    for row in targets["entries"]:
        found = sorted(set(row["query_labels"]) & set(label_records))
        matched_labels.update(found)
        chapters = row["query_chapters"]
        selected = {(reference, hit) for reference, hits in relevant.items()
                    if chapters is None or int(reference.split(".")[1]) in chapters
                    for hit in hits if hit[0] in found}
        all_selected.update(selected)
        refs = {r for r, _ in selected}
        per_chapter = Counter(int(r.split(".")[1]) for r in refs)
        status = ("label-not-in-pinned-index" if not found else
                  "label-present-no-scoped-book-anchor" if not selected else
                  "scoped-index-hits")
        results.append({
            "catalogue_id": row["id"], "reported_status": row["reported_status"],
            "role": row["role"], "query_chapters": chapters,
            "matched_labels": found,
            "source_record_ordinals": sorted({i for label in found for i in label_records[label]}),
            "index_status": status, "indexed_anchor_count": len(refs),
            "chapter_anchor_counts": {str(k): v for k, v in sorted(per_chapter.items())},
            "identity_collision": any(indexed["labels"][label] > 1 for label in found),
            "identity_status": "candidate-crosswalk-not-physical-verification",
            "reading_support": "not-assessed",
        })
    # Shared upstream records are inspected without counting each proposed part
    # as another object. Untagged and mixed-scope fragments remain explicit.
    shared = []
    for label in sorted(label_records):
        rows = [r for r in targets["entries"] if label in r["query_labels"]]
        if len(rows) < 2:
            continue
        fragments = []
        for ordinal in label_records[label]:
            for fragment_ordinal, fragment in enumerate(corpus[ordinal]["fragments"]):
                fragment_id = str(fragment["id"])
                # Ordinal is retained even if upstream IDs collide. Reference
                # discovery alone cannot decide whether such IDs are one object.
                local_refs = set()
                non_book_tags = 0
                for line in fragment["lines"]:
                    for word in line["words"]:
                        reference = parse_reference(word[5])
                        if reference is not None and reference.startswith(book + "."):
                            _, chapter, verse = reference.split(".")
                            local_refs.add((int(chapter), int(verse)))
                        else:
                            non_book_tags += 1
                hits = [r["id"] for r in rows if any(
                    r["query_chapters"] is None or chapter in r["query_chapters"]
                    for chapter, _ in local_refs)]
                fragments.append({
                    "source_record_ordinal": ordinal, "fragment_ordinal": fragment_ordinal,
                    "fragment": fragment_id, "indexed_anchor_count": len(local_refs),
                    "indexed_chapters": sorted({c for c, _ in local_refs}),
                    "non_book_or_unparsed_word_tags": non_book_tags,
                    "candidate_target_ids_by_chapter_tags": hits,
                    "assignment_status": "unresolved-no-book-anchor" if not hits else
                        "ambiguous-multiple-scopes" if len(hits) > 1 else "chapter-candidate-only",
                    "physical_assignment_verified": False,
                })
        shared.append({"legacy_label": label, "target_ids": [r["id"] for r in rows],
                       "independent_witness_count": None, "fragments": fragments})
    unmatched = sorted(indexed["book_labels"].get(book, set()) - matched_labels)
    all_hits = {(reference, hit) for reference, hits in relevant.items() for hit in hits}
    return {
        "schema_version": "1.0.0", "checked_date": targets["checked_date"],
        "book": book, "scope": targets["scope"],
        "policy": {**targets["mapping_policy"], "full_verse_index_exported": False,
                   "transcription_exported": False, "all_current_witnesses_reconciled": False},
        "summary": {
            "catalogue_target_names": len(results),
            "catalogue_reported_published_targets": sum(r["reported_status"] == "published" for r in results),
            "catalogue_reported_unpublished_targets": sum(r["reported_status"] != "published" for r in results),
            "target_names_with_scoped_index_hits": sum(r["index_status"] == "scoped-index-hits" for r in results),
            "target_names_without_index_labels": sum(r["index_status"] == "label-not-in-pinned-index" for r in results),
            "distinct_matched_legacy_labels": len(matched_labels),
            "pinned_index_book_labels": len(indexed["book_labels"].get(book, set())),
            "pinned_index_book_anchors": len(relevant),
            "unmatched_book_labels": len(unmatched),
            "book_anchor_locator_pairs_outside_query_scopes": len(all_hits - all_selected),
        },
        "targets": results, "shared_legacy_records": shared,
        "unmatched_book_labels": unmatched,
    }


def build(qdr: Path, catalogue_pdf: Path, targets_path: Path = TARGETS) -> dict:
    raw = qdr.read_bytes()
    if sha(raw) != INPUT_SHA:
        raise ValueError("QDR differs from pinned input")
    target_raw = targets_path.read_bytes()
    targets = json.loads(target_raw)
    if sha(catalogue_pdf.read_bytes()) != targets["catalogue"]["pdf_sha256"]:
        raise ValueError("catalogue PDF differs from inspected source")
    result = reconcile(json.loads(raw), targets)
    result["inputs"] = {
        "targets_sha256": sha(target_raw), "builder_sha256": sha(Path(__file__).read_bytes()),
        "scanner_sha256": sha((ROOT / "tools/textual_restoration/build_qdr_discovery.py").read_bytes()),
        "qdr": {"sha256": INPUT_SHA, "commit": COMMIT,
                "attribution": "Qumran Digital Reader, Michael Muzar; upstream ETCBC/Naaijer, Abegg transcriptions",
                "license": "CC BY-NC 4.0; private corpus, metadata-only output"},
        "catalogue": targets["catalogue"],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qdr_json", type=Path)
    parser.add_argument("catalogue_pdf", type=Path)
    parser.add_argument("--targets", type=Path, default=TARGETS)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.qdr_json, args.catalogue_pdf, args.targets)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.verify_only:
        if args.output.read_text() != encoded:
            raise ValueError("saved catalogue reconciliation differs from current inputs")
    else:
        args.output.write_text(encoded)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
