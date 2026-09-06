#!/usr/bin/env python3
"""Metadata-only discovery receipt; no QDR text or reading support is exported."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
COMMIT = "f54f38464e18409eed8286fe24dd24f88d4735dd"
INPUT_SHA = "3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295"
OUT = ROOT / "sources/textual_restoration/discovery/qdr_biblical_screen.v1.json"
NON_QUMRAN_OUT = OUT.with_name("qdr_non_qumran_screen.v1.json")
SITE_PREFIXES = ("Mur", "Sdeir", "5/6hev", "Xhev", "34Se", "Mas", "Arug")
NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
BOOKS = dict(zip(
    "Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal".split(),
    "genesis exodus leviticus numbers deuteronomy joshua judges ruth 1_samuel 2_samuel 1_kings 2_kings 1_chronicles 2_chronicles ezra nehemiah esther job psalms proverbs ecclesiastes song_of_songs isaiah jeremiah lamentations ezekiel daniel hosea joel amos obadiah jonah micah nahum habakkuk zephaniah haggai zechariah malachi".split()))
ALIASES = {**{key: key for key in BOOKS}, "Ex": "Exod", "Is": "Isa"}
REF = re.compile(r"^([A-Za-z0-9]+) ([0-9]+):([0-9]+)$")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def consonants(text: str) -> str:
    return "".join(re.findall(r"[א-ת]", text))


def parse_reference(value: str) -> str | None:
    match = REF.fullmatch(value)
    if not match or match[1] not in ALIASES:
        return None
    return f"{ALIASES[match[1]]}.{int(match[2])}.{int(match[3])}"


def scan(corpus: list[dict]) -> dict:
    if not isinstance(corpus, list):
        raise ValueError("QDR corpus must be a list")
    labels = Counter()
    hits = defaultdict(set)
    unparsed = Counter()
    book_labels = defaultdict(set)
    word_tags = Counter()
    all_words = 0
    for record_index, record in enumerate(corpus):
        label = record.get("scroll")
        if not isinstance(label, str) or not label:
            raise ValueError(f"record {record_index}: missing scroll label")
        labels[label] += 1
        for fragment in record["fragments"]:
            for line in fragment["lines"]:
                for word in line["words"]:
                    if not isinstance(word, list) or len(word) < 6 or not isinstance(word[5], str):
                        raise ValueError(f"record {record_index}: malformed word/reference")
                    all_words += 1
                    ref = parse_reference(word[5])
                    if ref is None:
                        unparsed[word[5]] += 1
                        continue
                    book = ref.split(".")[0]
                    # Record ordinal distinguishes colliding upstream labels/locators.
                    hits[ref].add((label, record_index, str(fragment["id"]), str(line["n"])))
                    book_labels[book].add(label)
                    word_tags[book] += 1
    return {"labels": labels, "hits": hits, "unparsed": unparsed,
            "book_labels": book_labels, "word_tags": word_tags, "all_words": all_words}


def wlc_index(wlc_dir: Path) -> tuple[dict, dict, list]:
    by_text, refs, receipts = {}, {}, []
    for book in BOOKS:
        path = wlc_dir / f"{book}.xml"
        raw = path.read_bytes()
        text_index = defaultdict(list)
        book_refs = set()
        for verse in ET.fromstring(raw).findall(".//o:verse", NS):
            ref = verse.get("osisID")
            if not ref or ref in book_refs:
                raise ValueError(f"{book}: absent or duplicate WLC verse ID")
            book_refs.add(ref)
            for key in verse_keys(verse):
                text_index[key].append(ref)
        by_text[book], refs[book] = text_index, book_refs
        receipts.append({"path": f"sources/ot/wlc/{book}.xml", "sha256": sha(raw)})
    return by_text, refs, receipts


def non_qumran_screen(data: dict) -> dict:
    """Classify label syntax only; do not authenticate a findspot or genre."""
    references = defaultdict(set)
    for reference, hits in data["hits"].items():
        for label, *_ in hits:
            references[label].add(reference)
    selected = sorted(label for label in data["labels"]
                      if label.startswith(SITE_PREFIXES))
    unresolved = sorted(label for label in data["labels"]
                        if label not in selected and not re.match(r"^[0-9]+Q", label))
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-04",
        "scope": "Non-Qumran-associated label syntax in the pinned QDR biblical dataset only",
        "source": {"url": f"https://github.com/evenderekh/qdr/tree/{COMMIT}",
                   "file": "data/qdr.1.1.biblical.json", "sha256": INPUT_SHA,
                   "attribution": "Qumran Digital Reader, Michael Muzar; upstream ETCBC/Naaijer, Abegg transcriptions",
                   "upstream_data_license": "CC BY-NC 4.0",
                   "export_content": "Selected label-level aggregate counts only; no text or full verse index"},
        "selection_prefixes": list(SITE_PREFIXES),
        "policy": {"label_prefix_proves_findspot": False,
                   "label_proves_continuous_bible_manuscript": False,
                   "indexed_anchors_prove_preserved_letters": False,
                   "all_known_non_qumran_sources_covered": False,
                   "canonical_change_applied": False},
        "summary": {"selected_labels": len(selected),
                    "selected_source_records": sum(data["labels"][s] for s in selected),
                    "other_nonstandard_labels_not_assigned": len(unresolved)},
        "labels": [{"label": label, "source_records": data["labels"][label],
                    "indexed_reference_anchors": len(references[label]),
                    "book_labels": [b for b in BOOKS if any(r.startswith(b + ".")
                                                          for r in references[label])],
                    "evidence_status": "discovery-only",
                    "institutional_identity_and_genre": "not-verified-by-this-screen"}
                   for label in selected],
        "other_nonstandard_labels_not_assigned": unresolved,
    }


def build_non_qumran(qdr: Path) -> dict:
    raw = qdr.read_bytes()
    if sha(raw) != INPUT_SHA:
        raise ValueError("QDR hash differs from pinned input; review the snapshot before updating")
    return non_qumran_screen(scan(json.loads(raw)))


def verse_keys(verse: ET.Element) -> set[str]:
    # Some POB fields include explicit paragraph signs; do not strip arbitrary
    # final pe/samekh letters. Match only signs actually encoded in this verse.
    words = []
    with_signs = []
    for child in verse:
        if child.tag == f"{{{NS['o']}}}w":
            text = "".join(child.itertext())
            words.append(text)
            with_signs.append(text)
        elif child.tag == f"{{{NS['o']}}}seg" and child.get("type") in {"x-pe", "x-samekh"}:
            with_signs.append(child.text or "")
    return {key for text in (" ".join(words), " ".join(with_signs))
            if (key := consonants(text))}


def map_source(text: str, index: dict) -> list[str]:
    key = consonants(text)
    return index.get(key, []) if key else []


def build(qdr: Path, root: Path = ROOT) -> dict:
    raw = qdr.read_bytes()
    if sha(raw) != INPUT_SHA:
        raise ValueError("QDR hash differs from pinned input; review the snapshot before updating")
    data = scan(json.loads(raw))
    by_text, wlc_refs, receipts = wlc_index(root / "sources/ot/wlc")
    queue = root / "sources/textual_restoration/inventory/priority_cases.jsonl"
    priority = [json.loads(line) for line in queue.read_text().splitlines() if line]
    mapped = []
    reverse = {value: key for key, value in BOOKS.items()}
    for case in priority:
        if case["testament"] != "ot":
            continue
        baseline = case["local_snapshot"]
        path = root / baseline["repo_path"]
        if sha(path.read_bytes()) != baseline["sha256"]:
            raise ValueError(f"{case['id']}: stale priority snapshot")
        book = reverse[case["book"]]
        matches = map_source(baseline["source_text"], by_text[book])
        matched_ref = matches[0] if len(matches) == 1 else None
        grouped = defaultdict(list)
        if matched_ref:
            for label, ordinal, fragment, line in sorted(data["hits"].get(matched_ref, set())):
                grouped[label].append({"source_record_index": ordinal, "fragment": fragment, "line": line})
        mapped.append({
            "case_id": case["id"], "pob_reference": baseline["reference"],
            "casebook_label": case["reference_label"],
            "query_scope": "single-anchor-only-not-entire-range-or-variant",
            "pob_baseline_sha256": baseline["sha256"], "wlc_reference": matched_ref,
            "reference_mapping": "unique-full-verse-consonantal-match-with-optional-encoded-paragraph-signs" if matched_ref else "unresolved",
            "qdr_reference_alignment": "normalized-reference-label-only-published-confirmation-required",
            "wlc_match_candidates": matches,
            "index_query_status": "hits" if grouped else "no-index-hit" if matched_ref else "not-queried-unresolved-mapping",
            "candidate_labels": [{"label": label, "locators": locators,
                                  "identity_collision": data["labels"][label] > 1,
                                  "reading_support": "not-assessed"}
                                 for label, locators in sorted(grouped.items())],
        })
    books = []
    for book, slug in BOOKS.items():
        refs = {r for r in data["hits"] if r.split(".")[0] == book}
        books.append({"book": slug, "wlc_book": book,
                      "indexed_reference_anchors": len(refs),
                      "distinct_source_labels": len(data["book_labels"][book]),
                      "word_reference_tags": data["word_tags"][book],
                      "anchors_not_in_wlc": sorted(refs - wlc_refs[book]),
                      "coverage_claim": "index-screen-only"})
    unresolved_prefixes = Counter()
    for value, count in data["unparsed"].items():
        unresolved_prefixes[value.split(" ")[0] if value else "(empty)"] += count
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-04",
        "scope": "All word references in one pinned QDR biblical index; not all known manuscripts",
        "source": {"url": f"https://github.com/evenderekh/qdr/tree/{COMMIT}",
                   "file": "data/qdr.1.1.biblical.json", "sha256": INPUT_SHA,
                   "attribution": "Qumran Digital Reader, Michael Muzar; upstream ETCBC/Naaijer, Abegg transcriptions",
                   "upstream_data_license": "CC BY-NC 4.0",
                   "export_content": "aggregate discovery metadata and priority-case locators only; no transcription or morphology",
                   "rights_note": "No full upstream corpus or full verse-to-manuscript index is vendored or relicensed here."},
        "policy": {"index_hits_are_reading_support": False, "zero_hits_prove_absence": False,
                   "distinct_labels_are_authenticated_manuscripts": False,
                   "same_number_pob_wlc_alignment_assumed": False, "canonical_change_applied": False},
        "summary": {"source_records": sum(data["labels"].values()),
                    "distinct_source_labels": len(data["labels"]),
                    "word_records_scanned": data["all_words"],
                    "recognized_biblical_word_tags": sum(data["word_tags"].values()),
                    "unparsed_word_tags": sum(data["unparsed"].values()),
                    "distinct_unparsed_reference_values": len(data["unparsed"]),
                    "indexed_reference_anchors": len(data["hits"]),
                    "canonical_books_with_index_hits": sum(bool(b["indexed_reference_anchors"]) for b in books),
                    "priority_cases": len(mapped),
                    "priority_cases_with_unique_wlc_mapping": sum(c["wlc_reference"] is not None for c in mapped),
                    "priority_cases_with_index_hits": sum(c["index_query_status"] == "hits" for c in mapped)},
        "identity_collisions": [{"label": k, "source_records": v, "status": "unresolved-do-not-count-as-independent"}
                                for k, v in sorted(data["labels"].items()) if v > 1],
        "unparsed_reference_prefix_counts": dict(sorted(unresolved_prefixes.items())),
        "unparsed_reference_examples": sorted(data["unparsed"])[:20],
        "books": books, "priority_cases": mapped,
        "local_inputs": {"priority_queue_sha256": sha(queue.read_bytes()), "wlc_files": receipts},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qdr_json", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--non-qumran", action="store_true",
                        help="Build the separate label-level non-Qumran discovery screen")
    args = parser.parse_args()
    result = build_non_qumran(args.qdr_json) if args.non_qumran else build(args.qdr_json)
    output = NON_QUMRAN_OUT if args.non_qumran else OUT
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.verify_only:
        if not output.exists() or output.read_text() != serialized:
            raise SystemExit("QDR discovery receipt missing or stale")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
