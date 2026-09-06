#!/usr/bin/env python3
"""Read-only integrity checks, not automated validation of scholarly truth."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
RECORD = "sources/textual_restoration/comparisons/samuel_20_6_source_english_followup.v1.json"
SELECTION = "sources/textual_restoration/samples/unflagged_english_sample.selection.v1.json"
REVIEW = "sources/textual_restoration/samples/unflagged_english_sample.review.v1.json"
TARGET = "translation/ot/2_samuel/020/006.yaml"
FIXED = {
    SELECTION: "c1ac793d6837896fb4fcd64e39adf4c70ea9527cae0bbced6036c5da8768074f",
    REVIEW: "b124e7b20876ea771f75c0a9d7c91b34cd9782ab8412c440e092f2b73c65a3f6",
    "docs/UNFLAGGED_ENGLISH_SAMPLE_2026-09-05.md": "b7f54461aa934a71e4ba294e8b0fc143748f9eb646124cb83dbb197cbf82b0e1",
    "sources/ot/wlc/2Sam.xml": "e7793e141ed94eadbd2dfb23936abbb4062e81a7dcd41114a6e36644f50b8333",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(record: dict, root: Path = ROOT, check_external: bool = False,
             read=None) -> dict:
    read = read or (lambda rel: (root / rel).read_bytes())
    for path, digest in FIXED.items():
        require(sha(read(path)) == digest, f"Frozen fixed input changed: {path}")
    selection = json.loads(read(SELECTION))
    expected = {**selection["protocol_inputs"], **FIXED}
    require(record["frozen_inputs"] == expected, "Incomplete or altered frozen input binding")
    for path, digest in expected.items():
        require(sha(read(path)) == digest, f"Frozen input changed: {path}")
    frozen = next(v for v in json.loads(read(REVIEW))["records"] if v["id"] == "2SA.20.6")
    baseline = record["baseline"]
    require(baseline["path"] == TARGET, "Wrong target")
    require(baseline["sha256"] == frozen["yaml_sha256"], "Baseline digest changed")
    require(baseline["context_files"] == frozen["context_files"], "Context set changed")
    require(len(baseline["context_files"]) == 26, "Incomplete chapter context")
    for path, digest in baseline["context_files"].items():
        require(sha(read(path)) == digest, f"Canonical context drift: {path}")
    current = yaml.safe_load(read(TARGET))
    require(baseline["source"] == frozen["source"] == current["source"], "Pointed source changed")
    require(baseline["current_pob"] == frozen["current_pob"] == current["translation"], "English changed")
    require(record["source_changes"] == record["canonical_changes"] == [], "Research-only scope violated")
    require(record["application_approved"] is False and record["publication_approved"] is False,
            "Research is not application/publication approval")
    require(record["whole_verse_outcome"] == "unresolved", "Unexpected promotion of held decision")
    contract = record["evaluation_contract"]
    require(contract["prior_exposure"] is True and contract["blinded"] is False
            and contract["fresh_held_out_measurement"] is False, "False independence/held-out claim")
    sources = {s["id"]: s for s in record["sources"]}
    require(len(sources) == len(record["sources"]), "Duplicate source ID")
    for finding in record["findings"]:
        require(set(finding["source_ids"]) <= set(sources), "Unknown evidence reference")
        require(bool(finding["strongest_counterargument"]), "Missing counterargument")
    for key in ("greek-rh2006", "syriac-cal62009"):
        source = sources[key]
        require(source["kind"] == "published-version-edition", "Edition is not a manuscript")
        require(source["retroversion_status"] == "unadopted-hypothesis", "Retroversion promoted to attestation")
        require(source["manuscript_apparatus_collated"] is False, "Unperformed apparatus claim")
    external = []
    if check_external:
        for source in sources.values():
            if "local_pdf" in source:
                path = Path(source["local_pdf"])
                require(path.is_file(), f"External source unavailable: {path}")
                require(sha(path.read_bytes()) == source["sha256"], f"External PDF changed: {path}")
                external.append(source["id"])
    return {"status": "integrity-pass", "canonical_changes": [],
            "frozen_inputs_checked": len(expected), "context_files_checked": 26,
            "source_text_sha256": sha(current["source"]["text"].encode()),
            "external_pdfs_checked": external, "scholarly_truth_certified": False,
            "publication_approved": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-external-pdfs", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(json.loads((ROOT / RECORD).read_bytes()),
                              check_external=args.check_external_pdfs), indent=2))


if __name__ == "__main__":
    main()
