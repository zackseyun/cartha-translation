#!/usr/bin/env python3
"""Verify the acquired En-Gedi master and selected segmentation payloads.

No image processing, transcription, or historical-text selection is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources/textual_restoration/discovery/en_gedi_asset_check.v1.json"
MASTER = "EnGedi-MasterView-scale-hires.png"
EXPECTED = {
    "textured.mtl": "3dead275b7451735e9b15d766cc506ca860f52d1a6e0d18ad53b2ee03c2d105a",
    "textured.obj": "9161e2c29639fc31281c54850783821f27b6f91833bac251e4eaef4822ae3667",
    "textured.png": "2899f925fc7be7346772e36b5814e7c5b7efd70c291677e88b68d1a8bce76b9c",
    "PerPixelMask.png": "053e96cb8658e68ab2d62a1ea99947f69115093fd40d93838663a55dd26d9087",
}


def png_dimensions(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("not a PNG with IHDR")
    return list(struct.unpack(">II", data[16:24]))


def build(directory):
    metadata = json.loads((directory / "archive-metadata.json").read_text())
    if metadata["metadata"]["identifier"] != "engedi-scroll":
        raise ValueError("wrong archive item")
    license_url = metadata["metadata"]["licenseurl"]
    if license_url != "http://creativecommons.org/licenses/by-nc/4.0/":
        raise ValueError("license metadata changed; review before proceeding")
    master = (directory / MASTER).read_bytes()
    sha = hashlib.sha256(master).hexdigest()
    md5 = hashlib.md5(master).hexdigest()
    listed = next(f for f in metadata["files"] if f["name"] == MASTER)
    if (sha != "1c2da746935f00b0020daf8d72fb0f3ff81b929811907eb5d75eb06d5a0faf10"
            or md5 != listed["md5"] or len(master) != int(listed["size"])):
        raise ValueError("master checksum or size mismatch")
    audit = directory / "segment-audit"
    receipt = json.loads((audit / "receipt.json").read_text())
    if (receipt["url"] != "https://archive.org/download/engedi-scroll/segmentations.zip"
            or receipt["archive_bytes"] != 1916439877 or receipt["full_archive_hash_verified"]):
        raise ValueError("wrong archive or unsupported whole-archive verification claim")
    members = []
    for member in receipt["member_payloads_verified"]:
        name = member["archive_member"]
        if not name.startswith("segmentations/merge5/"):
            raise ValueError("unexpected segment")
        local = (audit / member["local_file"]).resolve()
        if local.parent != audit.resolve():
            raise ValueError("member path escapes audit directory")
        data = local.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if (digest != EXPECTED[Path(name).name] or digest != member["sha256"]
                or len(data) != member["bytes"] or f"{zlib.crc32(data):08x}" != member["crc32"]):
            raise ValueError("selected payload mismatch")
        row = dict(member)
        if name.endswith(".png"):
            row["dimensions"] = png_dimensions(data)
        members.append(row)
    if len(members) != 4 or {Path(m["archive_member"]).name for m in members} != set(EXPECTED):
        raise ValueError("missing or duplicated selected payload")
    groups = sorted({e["name"].split("/")[1] for e in receipt["entries"]
                     if e["name"].startswith("segmentations/") and e["name"].endswith("/textured.obj")})
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-05",
        "witness_id": "en-gedi-leviticus", "license_url": license_url,
        "storage": "Private research assets outside repository; not relicensed as POB CC BY",
        "scope": "Initial master and four segment payloads only; see volume-probe receipt for later acquisitions",
        "policy": {"full_archive_hash_verified": False, "raw_xray_projections_verified": False,
                   "per_pixel_mapping_verified_by_this_receipt": False, "benchmark_executed": False,
                   "fresh_transcription": False, "generated_images_used": False,
                   "canonical_change_applied": False},
        "master": {"url": f"https://archive.org/download/engedi-scroll/{MASTER}",
                   "bytes": len(master), "md5": md5, "sha256": sha,
                   "dimensions": png_dimensions(master), "role": "published-merged-render-not-raw-scan"},
        "segmentation_archive": {"url": receipt["url"], "bytes": receipt["archive_bytes"],
                                 "etag": receipt["etag"], "entry_count": len(receipt["entries"]),
                                 "file_count": sum(not e["directory"] for e in receipt["entries"]),
                                 "segment_groups": groups, "http_ranges": receipt["http_ranges"]},
        "members": members,
        "next_gate": "Acquire a selected per-pixel mapping and matching raw CT slice region; establish coordinate conventions and segment-to-master alignment before scoring any purported letter recovery.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.directory)
    if args.verify_only:
        if json.loads(OUT.read_text()) != result:
            raise ValueError("saved En-Gedi receipt is stale")
        print("Verified master and four selected payloads; no raw-signal benchmark claimed.")
    else:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
