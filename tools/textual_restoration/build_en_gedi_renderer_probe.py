#!/usr/bin/env python3
"""Compare fixed candidate line samplers with actual archived texture values.

Numerical emulation only: no image output, original renderer execution or glyph
inference. The standard interpolator is unchanged; isolate the historical
corner discrepancy here. Requires NumPy/Pillow and the verified private assets.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.build_en_gedi_volume_probe import build as build_volume, payloads
from tools.textual_restoration.probe_en_gedi_mapping import sample_map, trilinear

DISCOVERY = ROOT / "sources/textual_restoration/discovery"
PROTOCOL = DISCOVERY / "en_gedi_renderer_protocol.v1.json"
OUT = DISCOVERY / "en_gedi_renderer_probe.v1.json"
PROTOCOL_SHA256 = "39da0c620750511462a1a76d28edaa42bf507d11e0b7dac14d912b986bc13d14"
EXTRA_PINS = {
    "slices/1648.tif": "64457e8ae413f97ec51dd47028297455ffe28c258b33a7032a8b054bd6efe54d",
    "slices/1653.tif": "e663d3cfbb5913fa6b2ae1f001c3d9a5fa5519d24fa6594a203ce87046c59821",
}


def interpolate_candidate(slices, xyz, mode):
    """Nearest-even candidate rounding, not a claim about all cvRound builds."""
    value = trilinear(slices, xyz)  # Also validates the complete neighborhood.
    if mode == "historical-c10-corner":
        x, y, z = map(float, xyz)
        x0, y0, z0 = map(int, np.floor(xyz))
        dx, dy, dz = x - x0, y - y0, z - z0
        # The pinned revision repeats (x1,y0,z0) in c10 instead of (x1,y1,z0).
        a = slices[z0]
        delta = float(a[y0, x0 + 1]) - float(a[y0 + 1, x0 + 1])
        value += dx * dy * (1 - dz) * delta
    elif mode != "standard-trilinear":
        raise ValueError("unknown interpolation candidate")
    if not np.isfinite(value) or not 0 <= value <= 65535:
        raise ValueError("invalid unsigned 16-bit interpolation result")
    return int(np.rint(value))


def line_positions(mapping, radius, interval, shift):
    values = np.asarray(mapping, dtype=np.float64)
    if values.shape != (6,) or not np.isfinite(values).all():
        raise ValueError("invalid position/normal")
    if not np.isfinite([radius, interval, shift]).all() or interval <= 0 or radius < interval:
        raise ValueError("invalid radius/interval/shift")
    count = int(radius / interval)
    if count > 1000:
        raise ValueError("too many candidate samples")
    center = np.array(values[:3] + [0, 0, shift], dtype=np.float32)
    normal = np.array(values[3:], dtype=np.float32)
    length = float(np.linalg.norm(normal.astype(np.float64)))
    if length == 0 or not np.isfinite(length):
        raise ValueError("zero/invalid normal")
    normal = (normal.astype(np.float64) / length).astype(np.float32)
    positions = []
    for i in range(count):
        delta = (normal.astype(np.float64) * (i * interval)).astype(np.float32)
        for sign in (1, -1):
            point = center + delta if sign == 1 else center - delta
            positions.append((sign * i * interval, point))
    return positions


def sample_line(slices, mapping, radius, interval, shift, mode):
    samples = [(d, interpolate_candidate(slices, point, mode))
               for d, point in line_positions(mapping, radius, interval, shift)]
    maximum = max(v for _, v in samples)
    return {"prediction": maximum, "sample_count": len(samples),
            "maximizing_normal_offsets": sorted(set(float(d) for d, v in samples if v == maximum))}


def build(directory):
    protocol_bytes = PROTOCOL.read_bytes()
    if hashlib.sha256(protocol_bytes).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("frozen protocol changed; create a new explicitly dated protocol")
    protocol = json.loads(protocol_bytes)
    base = build_volume(directory)
    if base != json.loads((DISCOVERY / "en_gedi_volume_probe.v1.json").read_text()):
        raise ValueError("prior volume receipt no longer reproduces")
    acquired = {}
    for name in ("mapping-audit", "ct-probe-audit"):
        acquired.update({m["archive_member"]: p for p, m in payloads(directory, name)})
    extra = payloads(directory, "renderer-ct-audit", EXTRA_PINS)
    if len(extra) != len(EXTRA_PINS) or {m["archive_member"] for _, m in extra} != set(EXTRA_PINS):
        raise ValueError("missing/duplicate extra CT payloads")
    acquired.update({m["archive_member"]: p for p, m in extra})
    records = base["payloads"] + [{k: v for k, v in m.items() if k != "local_file"} for _, m in extra]
    groups = {tuple(p): group for group, key in (("development", "development_texture_xy"),
                                               ("held-out", "held_out_texture_xy"))
              for p in protocol[key]}
    if len(groups) != sum(len(protocol[k]) for k in ("development_texture_xy", "held_out_texture_xy")):
        raise ValueError("duplicate/overlapping candidate coordinates")
    with gzip.open(acquired["segmentations/merge5/PerPixelMapping.yml.gz"], "rt", encoding="ascii") as stream:
        rows, cols, count, mappings = sample_map(stream, list(groups))
    if (rows, cols, count) != (3358, 1969, 39671412):
        raise ValueError("mapping shape changed")
    slices, tif_metadata = {}, []
    for name, path in acquired.items():
        if name.endswith(".tif"):
            with Image.open(path) as image:
                data = np.asarray(image)
                if image.size != (1400, 1400) or data.dtype != np.uint16:
                    raise ValueError("unexpected CT slice shape/dtype")
                slices[int(Path(name).stem)] = data.copy()
                tif_metadata.append({"member": name, "width": 1400, "height": 1400,
                                     "bits_per_sample": list(image.tag_v2[258]),
                                     "compression_tag": image.tag_v2[259]})
    needed = set()
    for mapping in mappings.values():
        for radius in protocol["radius_parameters_voxels"]:
            for shift in protocol["slice_index_offsets"]:
                for _, point in line_positions(mapping, radius, protocol["sampling_interval_voxels"], shift):
                    z0 = int(np.floor(point[2]))
                    needed.update((z0, z0 + 1))
    if not needed.issubset(slices):
        raise ValueError(f"Missing predeclared CT neighborhoods: {sorted(needed - set(slices))}; all required: {sorted(needed)}")
    points = []
    # base already verifies mask and texture hashes. Read only after the frozen
    # protocol and full prior receipt have been checked; do not tune parameters.
    with Image.open(directory / "segment-audit/member-03.png") as mask, \
            Image.open(directory / "segment-audit/member-02.png") as texture:
        for point, group in groups.items():
            if mask.getpixel(point) != 255:
                raise ValueError(f"predeclared coordinate has no valid mapping: {point}")
            points.append({"texture_xy": list(point), "group": group,
                           "xyz_normal": mappings[point], "mask_value": 255,
                           "published_texture_value": int(texture.getpixel(point))})
    candidates = []
    for radius in protocol["radius_parameters_voxels"]:
        for shift in protocol["slice_index_offsets"]:
            for mode in protocol["interpolators"]:
                results = []
                for point in points:
                    predicted = sample_line(slices, point["xyz_normal"], radius,
                                            protocol["sampling_interval_voxels"], shift, mode)
                    results.append({"texture_xy": point["texture_xy"], "group": point["group"],
                                    **predicted, "residual": predicted["prediction"] - point["published_texture_value"]})
                summaries = {}
                for group in ("development", "held-out"):
                    errors = [r["residual"] for r in results if r["group"] == group]
                    summaries[group] = {"count": len(errors), "exact_matches": errors.count(0),
                                        "mean_absolute_error": sum(map(abs, errors)) / len(errors),
                                        "maximum_absolute_error": max(map(abs, errors))}
                candidates.append({"radius_parameter": radius, "slice_index_offset": shift,
                                   "interpolator": mode, "results": results, "summary": summaries})
    return {"schema_version": "1.0.0", "checked_date": "2026-09-05",
            "witness_id": "en-gedi-leviticus", "stage": "candidate-renderer-numerical-check",
            "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
            "implementation_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in (Path(__file__).resolve(), ROOT / "tools/textual_restoration/probe_en_gedi_mapping.py",
                                                ROOT / "tools/textual_restoration/build_en_gedi_volume_probe.py")},
            "protocol": protocol, "input_payloads": records, "ct_tiff_metadata": tif_metadata,
            "prior_volume_receipt_sha256": hashlib.sha256((DISCOVERY / "en_gedi_volume_probe.v1.json").read_bytes()).hexdigest(),
            "texture_sha256": "2899f925fc7be7346772e36b5814e7c5b7efd70c291677e88b68d1a8bce76b9c",
            "points": points, "candidates": candidates, "selected_candidate": None,
            "policy": {"exact_export_revision_known": False, "original_renderer_executed": False,
                       "bit_exact_opencv_emulation_verified": False, "published_renderer_reproduced": False,
                       "coordinate_origin_resolved": False, "master_registration_verified": False,
                       "transcription_benchmark_executed": False, "new_letter_reading_claimed": False,
                       "generated_images_used": False, "canonical_change_applied": False},
            "license": base["license"],
            "interpretation": "Candidate numeric comparison only. Adjacent points are correlated and unlabeled for ink/text. Residuals do not establish a unique renderer, correct registration, glyph identity or textual priority."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.directory)
    if args.verify_only:
        if result != json.loads(OUT.read_text()):
            raise ValueError("saved renderer probe differs from acquired inputs/protocol")
        print("Verified all fixed candidate results; no restoration claim.")
    else:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(f"Wrote {OUT}")
    for c in result["candidates"]:
        print(c["radius_parameter"], c["slice_index_offset"], c["interpolator"], c["summary"])


if __name__ == "__main__":
    main()
