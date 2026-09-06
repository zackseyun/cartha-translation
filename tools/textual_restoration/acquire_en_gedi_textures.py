#!/usr/bin/env python3
"""Acquire the six preselected textures, with fail-closed ZIP and batch checks.

Private progress receipts survive interruptions. An existing output directory
is deliberately not resumed or overwritten; inspect its receipt first.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.dss.inspect_remote_zip import RangeSource, index_archive, write_member

PROTOCOL = ROOT / "sources/textual_restoration/discovery/en_gedi_texture_triage_protocol.v1.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_plan(plan):
    members = plan["members"]
    if len(members) != 6 or len({m["name"] for m in members}) != 6:
        raise ValueError("exactly six unique members required")
    expected = {f"segmentations/{s}/textured.png" for s in
                ("merge0", "merge1", "merge2", "merge3", "merge4", "remerge")}
    if {m["name"] for m in members} != expected:
        raise ValueError("unexpected selection")
    for m in members:
        if m["local_file"] != Path(m["name"]).parent.name + ".png":
            raise ValueError("unsafe or ambiguous local filename")
        if not all(0 < m[k] <= plan["per_member_budget_bytes"] <= 33554432
                   for k in ("bytes", "compressed_bytes")):
            raise ValueError("member budget exceeded")
    for key, budget in (("bytes", "batch_expanded_budget_bytes"),
                        ("compressed_bytes", "batch_compressed_budget_bytes")):
        if not sum(m[key] for m in members) <= plan[budget] <= 67108864:
            raise ValueError("batch budget exceeded")
    if not plan["etag"].startswith('"') or not plan["etag"].endswith('"'):
        raise ValueError("strong ETag required")


def match_index(plan, entries):
    indexed = {i.filename: i for i in entries}
    for m in plan["members"]:
        i = indexed[m["name"]]
        actual = (i.file_size, i.compress_size, f"{i.CRC:08x}", i.header_offset, i.is_dir())
        expected = (m["bytes"], m["compressed_bytes"], m["crc32"], m["header_offset"], False)
        if actual != expected:
            raise ValueError("fresh archive index differs from frozen selection")
    return indexed


def png_size(path):
    with path.open("rb") as f:
        head = f.read(24)
    if len(head) != 24 or head[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR":
        raise ValueError("invalid PNG header")
    return list(struct.unpack(">II", head[16:24]))


def acquire(output, prior_index):
    plan = json.loads(PROTOCOL.read_text())
    validate_plan(plan)
    if sha(prior_index) != plan["prior_index_sha256"]:
        raise ValueError("prior index changed")
    old = json.loads(prior_index.read_text())
    if old["etag"] != plan["etag"] or old["archive_bytes"] != plan["archive_bytes"] or old["url"] != plan["archive_url"]:
        raise ValueError("prior archive identity mismatch")
    for m in plan["members"]:
        expected = {k: v for k, v in m.items() if k != "local_file"}
        expected["directory"] = False
        if expected not in old["entries"]:
            raise ValueError("frozen selection absent from prior index")
    output.mkdir(parents=True, exist_ok=False)
    source = RangeSource(plan["archive_url"], plan["archive_bytes"])
    source.etag = plan["etag"]
    receipt = {"schema_version": "1.0.0", "protocol_sha256": sha(PROTOCOL),
               "tool_sha256": sha(Path(__file__)), "prior_index_sha256": sha(prior_index),
               "archive_url": source.url, "archive_bytes": source.size,
               "etag": source.etag, "full_archive_hash_verified": False,
               "scientific_reading_pass": False, "status": "in_progress",
               "members": [], "http_ranges": source.receipts}

    def save():
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")

    save()
    try:
        indexed = match_index(plan, index_archive(source))
        for m in plan["members"]:
            path = output / m["local_file"]
            digest = write_member(source, indexed[m["name"]], path, plan["per_member_budget_bytes"])
            receipt["members"].append({**m, "sha256": digest, "size_xy": png_size(path)})
            save()
            print(f"Verified {m['local_file']}: {digest}", flush=True)
        receipt["status"] = "complete"
    except Exception as exc:
        receipt["status"] = "failed"
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        receipt["http_payload_bytes"] = sum(r["length"] for r in source.receipts)
        save()
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prior-index", type=Path, required=True)
    args = parser.parse_args()
    acquire(args.output_dir, args.prior_index)
