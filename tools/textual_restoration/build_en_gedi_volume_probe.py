#!/usr/bin/env python3
"""Reproduce a bounded CT-coordinate/intensity probe, not a reading benchmark."""
import argparse
import configparser
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import zlib

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.probe_en_gedi_mapping import sample_map, trilinear

OUT = ROOT / "sources/textual_restoration/discovery/en_gedi_volume_probe.v1.json"
POINTS = [(984, 1679), (982, 1677), (986, 1681), (0, 0)]
PINS = {
    "segmentations/merge5/PerPixelMapping.yml.gz": "7ddf1f829ea0ed793728cee4a0f98885ce4425860d54715998d2ced045065240",
    "slices/EnGedi_rec.log": "f4d33064f9bfda7364c66641d03618c263106ac6936e6f4591bd198d68bfe907",
    "slices/1649.tif": "7e3bd9102069670d00c831d5b2aa5772757f585ca58929c021c8f3a906963798",
    "slices/1650.tif": "96ca51ebd0d5fd56c9577c0d942b9459513917d6e44a0319cfc40fbf3a08f876",
    "slices/1651.tif": "c2a6595b1c1be067fe8d03f83fd15f200c4e2923a6b8672d26e36613d1907e69",
    "slices/1652.tif": "06599c31ce5a25eacaae587ad5e6ad960b711840c6fadfcb3ce0942bc2082008",
}


def payloads(directory, audit_name, expected_hashes=None):
    expected_hashes = PINS if expected_hashes is None else expected_hashes
    audit = directory / audit_name
    receipt = json.loads((audit / "receipt.json").read_text())
    result = []
    for member in receipt["member_payloads_verified"]:
        path = (audit / member["local_file"]).resolve()
        if path.parent != audit.resolve():
            raise ValueError("payload path escaped audit directory")
        sha, crc, count = hashlib.sha256(), 0, 0
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                sha.update(chunk)
                crc = zlib.crc32(chunk, crc)
                count += len(chunk)
        if (sha.hexdigest() != expected_hashes[member["archive_member"]]
                or sha.hexdigest() != member["sha256"] or count != member["bytes"]
                or f"{crc:08x}" != member["crc32"]):
            raise ValueError("payload hash/CRC/length mismatch")
        result.append((path, member))
    return result


def build(directory):
    acquired = {}
    records = []
    for name in ("mapping-audit", "scan-log-audit", "ct-probe-audit"):
        for path, member in payloads(directory, name):
            acquired[member["archive_member"]] = path
            records.append({k: v for k, v in member.items() if k != "local_file"})
    if set(acquired) != set(PINS) or len(records) != len(PINS):
        raise ValueError("missing/duplicate probe payloads")
    mapping = acquired["segmentations/merge5/PerPixelMapping.yml.gz"]
    with gzip.open(mapping, "rt", encoding="ascii") as stream:
        rows, cols, count, samples = sample_map(stream, POINTS)
    if (rows, cols, count) != (3358, 1969, 39671412):
        raise ValueError("unexpected mapping dimensions")
    segment = directory / "segment-audit"
    for filename, digest in (("member-02.png", "2899f925fc7be7346772e36b5814e7c5b7efd70c291677e88b68d1a8bce76b9c"),
                             ("member-03.png", "053e96cb8658e68ab2d62a1ea99947f69115093fd40d93838663a55dd26d9087")):
        if hashlib.sha256((segment / filename).read_bytes()).hexdigest() != digest:
            raise ValueError("texture or mask changed")
    with Image.open(segment / "member-03.png") as mask, Image.open(segment / "member-02.png") as texture:
        if mask.size != (cols, rows) or texture.size != mask.size or mask.mode != "L":
            raise ValueError("mapping/mask/texture mismatch")
        sampled = [{"texture_xy": list(p), "mask_value": mask.getpixel(p),
                    "xyz_normal": v} for p, v in samples.items()]
        if mask.getpixel(POINTS[0]) != 255:
            raise ValueError("selected probe has no valid mapping")
        texture_value = int(texture.getpixel(POINTS[0]))
        texture_mode = texture.mode
    slices, tif_records = {}, []
    for name in PINS:
        if not re.fullmatch(r"slices/[0-9]{4}\.tif", name):
            continue
        with Image.open(acquired[name]) as image:
            data = np.asarray(image)
            if image.size != (1400, 1400) or data.dtype != np.uint16:
                raise ValueError("unexpected CT slice shape/dtype")
            slices[int(Path(name).stem)] = data.copy()
            tif_records.append({"member": name, "width": 1400, "height": 1400,
                                "bits_per_sample": list(image.tag_v2[258]),
                                "compression_tag": image.tag_v2[259]})
    index = json.loads((directory / "slice-index/receipt.json").read_text())
    slice_numbers = [int(Path(e["name"]).stem) for e in index["entries"]
                     if re.fullmatch(r"slices/[0-9]{4}\.tif", e["name"])]
    if slice_numbers != list(range(4504)):
        raise ValueError("numbered CT index not consecutive")
    log = configparser.ConfigParser(interpolation=None)
    log.optionxform = str
    log.read_string(acquired["slices/EnGedi_rec.log"].read_text(encoding="latin-1"))
    fields = ("Reconstruction Program", "Program Version", "First Section", "Last Section",
              "Sections Count", "Result Image Width (pixels)", "Result Image Height (pixels)",
              "Pixel Size (um)", "Smoothing", "Ring Artifact Correction", "Beam Hardening Correction (%)")
    log_values = {key: log["Reconstruction"][key].strip() for key in fields}
    if log_values["Sections Count"] != "4504" or log_values["First Section"] != "2":
        raise ValueError("reconstruction indexing metadata changed")
    xyz, normal = np.array(samples[POINTS[0]][:3]), np.array(samples[POINTS[0]][3:])
    if not np.isclose(np.linalg.norm(normal), 1.0, atol=1e-9, rtol=0):
        raise ValueError("normal not unit length; no implicit normalization")
    profiles = [{"slice_index_offset_hypothesis": shift,
                 "offsets_along_recorded_normal_voxels": [-4, -2, 0, 2, 4],
                 "trilinear_intensities": [round(trilinear(slices, xyz + normal * d + [0, 0, shift]), 6)
                                          for d in (-4, -2, 0, 2, 4)]} for shift in (0, 2)]
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-05",
        "witness_id": "en-gedi-leviticus", "stage": "coordinate-and-intensity-probe",
        "policy": {"full_archive_hash_verified": False, "raw_xray_projections_acquired": False,
                   "published_renderer_reproduced": False, "coordinate_origin_resolved": False,
                   "master_registration_verified": False, "transcription_benchmark_executed": False,
                   "new_letter_reading_claimed": False, "generated_images_used": False,
                   "canonical_change_applied": False},
        "license": "Archive dataset declares CC BY-NC 4.0; source payloads remain outside Git",
        "payloads": records, "ct_tiff_metadata": tif_records,
        "reconstruction_log_selected_fields": log_values,
        "ct_index": {"entries": len(index["entries"]), "numbered_slices": len(slice_numbers),
                     "first": "slices/0000.tif", "last": "slices/4503.tif",
                     "sidecars_counted_as_slices": False},
        "mapping": {"rows": rows, "cols": cols, "channels": 6, "scalar_count": count,
                    "complete_gzip_stream_read": True, "samples": sampled},
        "intensity_probe": {"texture_xy": list(POINTS[0]), "selection_basis": "preselected geometric interior point, not a glyph label",
                            "published_texture_mode": texture_mode, "published_texture_value": texture_value,
                            "normal_length": round(float(np.linalg.norm(normal)), 9), "profiles": profiles,
                            "preferred_index_offset": None},
        "interpretation": "Intensity changes with sampling position. Neither a single trilinear sample nor matching brightness would establish ink, a letter, correct origin, or reconstruction of the published texturing method. The log starts at reconstruction section 2 while archive names start at 0000; both offset hypotheses remain unselected.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.directory)
    if args.verify_only:
        if result != json.loads(OUT.read_text()):
            raise ValueError("saved volume probe differs from acquired data")
        print("Verified coordinate/intensity receipt; no transcription claim.")
    else:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
