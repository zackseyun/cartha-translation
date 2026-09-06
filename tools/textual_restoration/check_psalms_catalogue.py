#!/usr/bin/env python3
"""Reproduce bounded Psalms label checks; never assess text or physical identity."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.build_catalogue_index import INDEX_SHA, parse_index
from tools.textual_restoration.build_catalogue_reconciliation import reconcile
from tools.textual_restoration.build_qdr_discovery import INPUT_SHA, COMMIT

NONBIBLICAL_SHA = "16edab67449e00ffda01368c78692f3a5bf311d0f0341926c9e2e658bc00d4ac"
TARGETS = ROOT / "sources/textual_restoration/discovery/psalms_catalogue_targets.v1.json"
OUT = TARGETS.with_name("psalms_catalogue_check.v1.json")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned(path, expected):
    raw = path.read_bytes()
    if sha(raw) != expected:
        raise ValueError(f"input pin mismatch: {path.name}")
    return raw


def label_ordinals(corpus, labels):
    """Only explicit labels match; ordinals belong to this corpus, not another."""
    return [{"label": row["scroll"], "source_record_ordinal": i}
            for i, row in enumerate(corpus) if row["scroll"] in labels]


def modern_matches(catalogue, labels):
    return [row for row in catalogue if row["display_label"] in labels]


def build(biblical, nonbiblical, index_html, targets_path=TARGETS):
    bib = json.loads(pinned(biblical, INPUT_SHA))
    nonbib = json.loads(pinned(nonbiblical, NONBIBLICAL_SHA))
    modern = parse_index(pinned(index_html, INDEX_SHA))
    raw_targets = targets_path.read_bytes()
    targets = json.loads(raw_targets)
    if targets["book"] != "Ps":
        raise ValueError("Psalms-only check")
    result = reconcile(bib, targets)
    for source, row in zip(targets["entries"], result["targets"], strict=True):
        row["qdr_biblical_file"] = "data/qdr.1.1.biblical.json"
        row["qdr_nonbiblical_label_check"] = {
            "file": "data/qdr.1.1.non_biblical.json",
            "matches": label_ordinals(nonbib, source["query_labels"]),
            "content_consulted": "scroll labels and record ordinals only",
            "psalm_reference_or_survival_checked": False,
        }
        row["modern_catalogue_matches"] = modern_matches(modern, source["modern_query_labels"])
        row["modern_underlying_transcription_consulted"] = False
    result["summary"].update({
        "target_names_with_nonbiblical_exact_label": sum(bool(r["qdr_nonbiblical_label_check"]["matches"]) for r in result["targets"]),
        "target_names_with_modern_catalogue_label": sum(bool(r["modern_catalogue_matches"]) for r in result["targets"]),
        "historical_provenance_holds_excluded_from_target_counts": len(targets["historical_provenance_holds"]),
        "independent_manuscript_count": None,
    })
    result["inputs"] = {
        "targets_sha256": sha(raw_targets),
        "checker_sha256": sha(Path(__file__).read_bytes()),
        "reconciler_sha256": sha((ROOT / "tools/textual_restoration/build_catalogue_reconciliation.py").read_bytes()),
        "scanner_sha256": sha((ROOT / "tools/textual_restoration/build_qdr_discovery.py").read_bytes()),
        "catalogue_parser_sha256": sha((ROOT / "tools/textual_restoration/build_catalogue_index.py").read_bytes()),
        "qdr_commit": COMMIT,
        "qdr_biblical_sha256": INPUT_SHA,
        "qdr_nonbiblical_sha256": NONBIBLICAL_SHA,
        "qdr_attribution": "Qumran Digital Reader, Michael Muzar; upstream ETCBC/Naaijer and Abegg transcriptions",
        "qdr_rights": "CC BY-NC 4.0; private inputs, metadata-only output",
        "modern_index_sha256": INDEX_SHA,
        "modern_index_url": "https://lexicon.qumran-digital.org/transcription-index/latest/index.html",
        "modern_snapshot_consulted_date": "2026-09-05",
        "catalogue_source_claims": "Agent-consulted publisher/institutional sources recorded in targets; not verified by this label-check program.",
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("biblical", type=Path)
    parser.add_argument("nonbiblical", type=Path)
    parser.add_argument("index_html", type=Path)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.biblical, args.nonbiblical, args.index_html)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.verify_only:
        if args.output.read_text() != encoded:
            raise ValueError("saved Psalms check differs")
    else:
        args.output.write_text(encoded)
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
