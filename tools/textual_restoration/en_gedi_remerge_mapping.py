#!/usr/bin/env python3
"""Acquire two fixed private assets and inspect their map without editing images."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.dss.inspect_remote_zip import RangeSource, index_archive, write_member

DISCOVERY = ROOT / "sources/textual_restoration/discovery"
PROTOCOL = DISCOVERY / "en_gedi_remerge_mapping_protocol.v1.json"
PROTOCOL_SHA = "06503a1f6bc88a24a8758b06df4d4537ccd28b6da39d359cc8899d1f309b53bd"
ACQUISITION = DISCOVERY / "en_gedi_remerge_acquisition.v1.json"
OUTPUT = DISCOVERY / "en_gedi_remerge_mapping_check.v1.json"
ACQUISITION_TOOL_V1 = DISCOVERY / "en_gedi_remerge_acquisition_tool.v1.txt"
ACQUISITION_TOOL_V1_SHA = "cfc1fae81538634339a29186c86bac5ce148f237d96fa0853c15919965d1cfa3"


def digest(path):
    h, crc, size = hashlib.sha256(), 0, 0
    with path.open("rb") as stream:
        while chunk := stream.read(4 * 1024 * 1024):
            h.update(chunk)
            crc = zlib.crc32(chunk, crc)
            size += len(chunk)
    return h.hexdigest(), f"{crc:08x}", size


def load_plan():
    if digest(PROTOCOL)[0] != PROTOCOL_SHA:
        raise ValueError("frozen mapping protocol drift")
    plan = json.loads(PROTOCOL.read_text())
    if digest(ROOT / plan["prior_triage_path"])[0] != plan["prior_triage_sha256"]:
        raise ValueError("prior development triage drift")
    for size_key, budget in (("bytes", "batch_expanded_zip_budget_bytes"),
                             ("compressed_bytes", "batch_compressed_budget_bytes")):
        if sum(m[size_key] for m in plan["members"]) > plan[budget]:
            raise ValueError("batch budget exceeded")
        if any(m[size_key] > plan["per_member_budget_bytes"] for m in plan["members"]):
            raise ValueError("member budget exceeded")
    if len({tuple(p["xy"]) for p in plan["points"]}) != len(plan["points"]):
        raise ValueError("duplicate fixed sample")
    return plan


def acquire(directory, prior_index):
    plan = load_plan()
    if digest(prior_index)[0] != plan["prior_index_sha256"]:
        raise ValueError("prior index drift")
    prior = json.loads(prior_index.read_text())
    if (prior["url"], prior["archive_bytes"], prior["etag"]) != (plan["archive_url"], plan["archive_bytes"], plan["etag"]):
        raise ValueError("prior archive identity drift")
    for member in plan["members"]:
        if {k: v for k, v in member.items() if k != "local_file"} not in prior["entries"]:
            raise ValueError("member absent from prior index")
    directory = directory.resolve()
    if directory.is_relative_to(ROOT):
        raise ValueError("private assets must remain outside repository")
    directory.mkdir(parents=True, exist_ok=False)
    source = RangeSource(plan["archive_url"], plan["archive_bytes"])
    source.etag = plan["etag"]
    receipt = {"protocol_sha256": PROTOCOL_SHA, "tool_sha256": digest(Path(__file__))[0],
               "archive_url": source.url, "archive_bytes": source.size, "etag": source.etag,
               "full_archive_hash_verified": False, "status": "in_progress",
               "members": [], "http_ranges": source.receipts}
    def save():
        (directory / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    save()
    try:
        indexed = {i.filename: i for i in index_archive(source)}
        for m in plan["members"]:
            i = indexed[m["name"]]
            if (i.file_size, i.compress_size, f"{i.CRC:08x}", i.header_offset, i.is_dir()) != (m["bytes"], m["compressed_bytes"], m["crc32"], m["header_offset"], False):
                raise ValueError("fresh selected index drift")
        for m in plan["members"]:
            sha = write_member(source, indexed[m["name"]], directory / m["local_file"], plan["per_member_budget_bytes"])
            receipt["members"].append({**m, "sha256": sha})
            save()
            print(f"Verified {m['local_file']}: {sha}", flush=True)
        receipt["status"] = "complete"
    except Exception as exc:
        receipt["status"] = "failed"
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        receipt["http_payload_bytes"] = sum(r["length"] for r in source.receipts)
        save()
    return receipt


class CappedText:
    """ASCII bytes equal character count; bound nested gzip expansion."""
    def __init__(self, stream, cap):
        self.stream, self.cap, self.count = stream, cap, 0
    def take(self, text):
        self.count += len(text)
        if self.count > self.cap:
            raise ValueError("expanded mapping text cap exceeded")
        return text
    def read(self, size):
        return self.take(self.stream.read(min(size, self.cap - self.count + 1)))
    def readline(self):
        return self.take(self.stream.readline(min(16385, self.cap - self.count + 1)))


def build(directory, texture):
    import numpy as np
    from PIL import Image
    from tools.textual_restoration import probe_en_gedi_mapping as mapping
    plan = load_plan()
    receipt = json.loads((directory / "receipt.json").read_text())
    if digest(ACQUISITION_TOOL_V1)[0] != ACQUISITION_TOOL_V1_SHA:
        raise ValueError("historical acquisition implementation drift")
    accepted_acquisition_tools = {ACQUISITION_TOOL_V1_SHA, digest(Path(__file__))[0]}
    if receipt["status"] != "complete" or receipt["protocol_sha256"] != PROTOCOL_SHA or receipt["tool_sha256"] not in accepted_acquisition_tools:
        raise ValueError("incomplete acquisition or tool/protocol drift")
    if any(receipt[k] != plan[k] for k in ("archive_url", "archive_bytes", "etag")) or receipt["full_archive_hash_verified"] is not False:
        raise ValueError("acquisition identity or claim drift")
    if len(receipt["members"]) != len(plan["members"]):
        raise ValueError("missing or extra member")
    for m, actual in zip(plan["members"], receipt["members"]):
        if any(actual[k] != v for k, v in m.items()):
            raise ValueError("member metadata drift")
        if digest(directory / m["local_file"]) != (actual["sha256"], m["crc32"], m["bytes"]):
            raise ValueError("payload SHA/CRC/size drift")
    if digest(texture)[0] != plan["texture_sha256"]:
        raise ValueError("selected texture drift")
    points = [tuple(p["xy"]) for p in plan["points"]]
    with gzip.open(directory / "PerPixelMapping.yml.gz", "rt", encoding="ascii", newline="") as stream:
        bounded = CappedText(stream, plan["mapping_expanded_text_cap_bytes"])
        rows, cols, count, samples = mapping.sample_map(bounded, points)
        expanded = bounded.count
    if [cols, rows] != plan["texture_size_xy"]:
        raise ValueError("mapping/texture shape mismatch")
    with Image.open(directory / "PerPixelMask.png") as mask, Image.open(texture) as tex:
        if mask.size != (cols, rows) or mask.mode != "L" or tex.size != mask.size:
            raise ValueError("mask/texture shape or mask type mismatch")
        mask_counts = {str(v): n for n, v in sorted(mask.getcolors(rows * cols), key=lambda pair: pair[1])}
        observations = [{**p, "mask_value": mask.getpixel(tuple(p["xy"])),
                         "texture_value": tex.getpixel(tuple(p["xy"])),
                         "xyz_normal": samples[tuple(p["xy"])]} for p in plan["points"]]
    valid = [o for o in observations if o["mask_value"] == 255]
    xyz = np.array([o["xyz_normal"][:3] for o in valid])
    norms = [float(np.linalg.norm(o["xyz_normal"][3:])) for o in valid]
    return {"schema_version": "1.0.0", "date": plan["date"], "protocol_sha256": PROTOCOL_SHA,
            "implementation_sha256": digest(Path(__file__))[0],
            "mapping_parser_sha256": digest(Path(mapping.__file__))[0],
            "historical_acquisition_tool_path": str(ACQUISITION_TOOL_V1.relative_to(ROOT)),
            "historical_acquisition_tool_sha256": ACQUISITION_TOOL_V1_SHA,
            "expanded_byte_count_policy": "ASCII with newline translation disabled; includes CR and LF bytes separately",
            "acquisition_receipt_sha256": digest(directory / "receipt.json")[0],
            "acquisition": receipt, "texture_sha256": plan["texture_sha256"],
            "size_xy": [cols, rows], "parsed_scalar_count": count, "expanded_ascii_bytes": expanded,
            "mask_value_counts": mask_counts, "points": observations,
            "mask_valid_points": len(valid), "mask_other_points": len(observations) - len(valid),
            "valid_sample_xyz_min": xyz.min(axis=0).tolist() if len(valid) else None,
            "valid_sample_xyz_max": xyz.max(axis=0).tolist() if len(valid) else None,
            "valid_sample_normal_norm_range": [min(norms), max(norms)] if norms else None,
            "limitations": ["Coordinate entries are recorded geometry, not validated ink or exact CT indexing.",
                            "Texture/master/edition-line correspondence remains unaccepted.",
                            "No new CT slices, rendering, letter labels, transcription or English change."],
            "scientific_reading_pass": False, "canonical_change": False}


def publish(path, value):
    raw = json.dumps(value, indent=2) + "\n"
    if path.exists():
        if path.read_text() != raw:
            raise ValueError("refuse to overwrite differing evidence")
    else:
        with path.open("x") as stream:
            stream.write(raw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--acquire", type=Path, metavar="PRIOR_INDEX")
    parser.add_argument("--texture", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.acquire:
        if args.texture or args.write:
            parser.error("acquisition is separate from inspection")
        acquire(args.directory, args.acquire)
    else:
        if not args.texture:
            parser.error("inspection requires --texture")
        result = build(args.directory, args.texture)
        if args.write:
            publish(ACQUISITION, result["acquisition"])
            publish(OUTPUT, result)
        elif result != json.loads(OUTPUT.read_text()) or result["acquisition"] != json.loads(ACQUISITION.read_text()):
            raise ValueError("saved evidence differs from actual inputs")
        print(json.dumps({k: result[k] for k in ("size_xy", "parsed_scalar_count", "expanded_ascii_bytes", "mask_valid_points", "mask_other_points", "valid_sample_xyz_min", "valid_sample_xyz_max", "valid_sample_normal_norm_range", "scientific_reading_pass")}, indent=2))
