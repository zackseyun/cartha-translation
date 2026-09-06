#!/usr/bin/env python3
"""Reconcile catalogue labels, never manuscripts/readings, across two projects."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urljoin, urlsplit

from tools.textual_restoration.build_qdr_discovery import COMMIT, INPUT_SHA, scan, sha

ROOT = Path(__file__).resolve().parents[2]
INDEX_URL = "https://lexicon.qumran-digital.org/transcription-index/latest/index.html"
INDEX_SHA = "e1211f26d0c37ac46bc7c8cdb23587393742abaef80fcce001bb8b90752683f5"
OUT = ROOT / "sources/textual_restoration/discovery/qumran_digital_catalogue_index.v1.json"
CLASSES = {"dss", "dss-biblical", "non-dss"}


class CatalogueParser(HTMLParser):
    """Read the actual item-list schema, including text split by superscripts.

    Unexpected classification, duplicate links, or a truncated list fail closed.
    Other navigation lists are ignored. URL IDs are preserved, not rewritten.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.entries = []
        self.in_list = False
        self.list_seen = False
        self.row = None
        self.in_anchor = False
        self.element_stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "ol" and attrs.get("id") == "item-list":
            if self.list_seen:
                raise ValueError("duplicate catalogue list")
            self.in_list = self.list_seen = True
            self.element_stack = ["ol"]
            return
        if not self.in_list:
            return
        # The observed index schema is ol > li > a > optional sup. Do not
        # silently skip rows if the publisher changes a container or nesting.
        allowed_parent = {"li": "ol", "a": "li", "sup": "a"}
        if tag not in allowed_parent or self.element_stack[-1] != allowed_parent[tag]:
            raise ValueError("unexpected catalogue element or nesting")
        self.element_stack.append(tag)
        if tag == "li":
            if self.row is not None:
                raise ValueError("unclosed catalogue item")
            classes = set(attrs.get("class", "").split())
            genre = classes & CLASSES
            if "list-item" not in classes or len(genre) != 1:
                raise ValueError("unknown or ambiguous catalogue class")
            self.row = {"catalogue_class": genre.pop(), "display_label": ""}
        elif tag == "a" and self.row is not None:
            if "url" in self.row or "text-href-link" not in attrs.get("class", "").split():
                raise ValueError("unexpected or duplicate catalogue anchor")
            url = urljoin(INDEX_URL, attrs.get("href", ""))
            parts = urlsplit(url)
            match = re.fullmatch(r"/transcriptions/([^/]+)/(\d{4}-\d{2}-\d{2})/index\.html", parts.path)
            if parts.scheme != "https" or parts.netloc != "lexicon.qumran-digital.org" or not match or parts.fragment:
                raise ValueError("unexpected transcription URL")
            query = parse_qs(parts.query, keep_blank_values=True, strict_parsing=True)
            if query and query != {"v": [match[2]]}:
                raise ValueError("URL path/query version disagreement")
            self.row.update(url=url, url_identifier=unquote(match[1]), listed_version=match[2])
            self.in_anchor = True

    def handle_data(self, data):
        if self.in_anchor:
            self.row["display_label"] += data
        elif self.in_list and data.strip():
            raise ValueError("unexpected text outside catalogue anchor")

    def handle_endtag(self, tag):
        if not self.in_list:
            return
        if not self.element_stack or self.element_stack[-1] != tag:
            raise ValueError("unclosed or mismatched catalogue element")
        self.element_stack.pop()
        if tag == "a":
            self.in_anchor = False
        elif tag == "li":
            if self.row is None or "url" not in self.row or self.in_anchor:
                raise ValueError("incomplete catalogue item")
            self.row["display_label"] = " ".join(self.row["display_label"].split())
            if not self.row["display_label"]:
                raise ValueError("empty catalogue label")
            self.row["index_ordinal"] = len(self.entries) + 1
            self.entries.append(self.row)
            self.row = None
        elif tag == "ol":
            if self.row is not None:
                raise ValueError("unclosed catalogue item")
            self.in_list = False


def parse_index(raw: bytes) -> list[dict]:
    parser = CatalogueParser()
    parser.feed(raw.decode("utf-8"))
    parser.close()
    if not parser.list_seen or parser.in_list or parser.row is not None or not parser.entries:
        raise ValueError("absent, empty or truncated catalogue")
    for field in ("url", "display_label", "url_identifier"):
        values = [entry[field] for entry in parser.entries]
        if len(values) != len(set(values)):
            raise ValueError(f"duplicate catalogue {field}")
    return parser.entries


def candidate_key(label: str) -> str:
    """Typography-only candidate key; slash, hyphen, digits and suffixes survive."""
    return re.sub(r"[.\s]", "", label.casefold())


def reconcile(entries: list[dict], data: dict) -> dict:
    labels = data["labels"]
    by_key = defaultdict(list)
    for label in labels:
        by_key[candidate_key(label)].append(label)
    rows = []
    matched = set()
    candidates = set()
    for entry in entries:
        label = entry["display_label"]
        exact = [label] if label in labels else []
        possible = sorted(by_key[candidate_key(label)]) if not exact else []
        # Biblical-labelled entries are the primary scope; also retain exact
        # matches and typography-only candidates anywhere else in the index.
        if entry["catalogue_class"] != "dss-biblical" and not exact and not possible:
            continue
        matched.update(exact)
        candidates.update(possible)
        selected = exact or possible
        rows.append({**entry,
                     "match_status": "exact-label-only" if exact else "typography-alias-candidate" if possible else "no-label-match",
                     "qdr_labels": selected,
                     "qdr_source_records": sum(labels[l] for l in selected),
                     "qdr_label_collision": any(labels[l] > 1 for l in selected),
                     "physical_identity_verified": False,
                     "underlying_transcription_consulted_by_this_pass": False})
    biblical = [r for r in rows if r["catalogue_class"] == "dss-biblical"]
    return {
        "summary": {
            "catalogue_entries_parsed": len(entries),
            "catalogue_class_counts": dict(sorted(Counter(e["catalogue_class"] for e in entries).items())),
            "qdr_distinct_labels_scanned": len(labels),
            "qdr_source_records_scanned": sum(labels.values()),
            "exported_catalogue_entries": len(rows),
            "biblical_class_entries": len(biblical),
            "biblical_class_exact_label_matches": sum(r["match_status"] == "exact-label-only" for r in biblical),
            "biblical_class_typography_candidates": sum(r["match_status"] == "typography-alias-candidate" for r in biblical),
            "biblical_class_without_label_candidate": sum(r["match_status"] == "no-label-match" for r in biblical),
            "exact_qdr_labels_any_catalogue_class": len(matched),
            "qdr_labels_with_typography_candidate_but_no_exact_match": len(candidates - matched),
            "qdr_labels_without_exact_or_typography_candidate": len(set(labels) - matched - candidates),
        },
        "entries": rows,
        "qdr_labels_without_exact_match": sorted(set(labels) - matched),
        "qdr_labels_without_exact_or_typography_candidate": sorted(set(labels) - matched - candidates),
        "biblical_class_entries_without_exact_match": [r["display_label"] for r in biblical if r["match_status"] != "exact-label-only"],
        "biblical_class_entries_without_label_candidate": [r["display_label"] for r in biblical if r["match_status"] == "no-label-match"],
        "exact_matches_outside_biblical_class": [r["display_label"] for r in rows if r["catalogue_class"] != "dss-biblical" and r["match_status"] == "exact-label-only"],
        "qdr_identity_collisions": [{"label": label, "source_records": count} for label, count in sorted(labels.items()) if count > 1],
    }


def build(index_path: Path, qdr_path: Path) -> dict:
    raw, qdr_raw = index_path.read_bytes(), qdr_path.read_bytes()
    if sha(raw) != INDEX_SHA:
        raise ValueError("catalogue differs from pinned snapshot; review before updating")
    if sha(qdr_raw) != INPUT_SHA:
        raise ValueError("QDR differs from pinned snapshot; review before updating")
    entries = parse_index(raw)
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-05",
        "scope": "Entire one-project catalogue index reconciled against one legacy biblical dataset, not all known OT manuscripts",
        "sources": {
            "catalogue": {"url": INDEX_URL, "sha256": sha(raw), "bytes": len(raw),
                          "attribution": "Qumran-Digital, DFG project 465277421, with predecessor Qumran-Wörterbuch",
                          "content_consulted": "index labels, CSS class, link identifier and listed version only; no bulk transcriptions or images",
                          "rights_note": "Only factual catalogue metadata exported; no source transcription, apparatus or image is vendored or relicensed."},
            "qdr": {"url": f"https://github.com/evenderekh/qdr/tree/{COMMIT}", "file": "data/qdr.1.1.biblical.json", "sha256": sha(qdr_raw),
                    "attribution": "Qumran Digital Reader, Michael Muzar; upstream ETCBC/Naaijer and Abegg transcriptions",
                    "upstream_data_license": "CC BY-NC 4.0", "content_exported": "label-level discovery metadata only; no text or full verse index"},
            "classification_documentation": {"url": "https://lexicon.qumran-digital.org/faq/v1/en/index.html", "sections": ["3.7", "3.9"],
                                           "sha256": "84ca2de5c5f5542189ff157d517a32d38680015855e4173ea6e714ae6ee8e706",
                                           "meaning": "Italic biblical classification is pragmatic; default transcription is current version."},
            "css": {"url": "https://lexicon.qumran-digital.org/transcription-index/v1/styles/style.css",
                    "sha256": "a9ab746af1af354d995e262a7112911fc6919cb226219afdba5b727cb5299c1d",
                    "observed_rule": "li.dss-biblical { font-style: italic; }"},
        },
        "policy": {"projects_are_the_same": False, "exact_label_proves_physical_identity": False,
                   "typography_candidate_is_verified_alias": False, "genre_class_is_final_textual_classification": False,
                   "missing_label_proves_manuscript_absence": False, "listed_version_proves_text_consultation": False,
                   "all_known_ot_sources_covered": False, "canonical_change_applied": False,
                   "candidate_rule": "casefold and remove whitespace/periods only; no prefix/suffix deletion, fuzzy matching or numeric reassignment",
                   "next_gate": "Resolve identity and genre against institutional catalogues/editions before passage-level preserved-text comparison."},
        **reconcile(entries, scan(json.loads(qdr_raw))),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--qdr", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.index, args.qdr)
    if args.check:
        if json.loads(args.out.read_text()) != result:
            raise SystemExit("catalogue receipt is stale")
    else:
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
