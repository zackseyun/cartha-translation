#!/usr/bin/env python3
"""Read-only wider numeric check: JSON to stdout, never image output."""
from collections import Counter
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
from tools.textual_restoration.build_en_gedi_renderer_probe import build as prior_build, line_positions, sample_line
from tools.textual_restoration.probe_en_gedi_mapping import sample_map

DISCOVERY = ROOT / "sources/textual_restoration/discovery"
PROTOCOL = DISCOVERY / "en_gedi_wider_renderer_protocol.v1.json"
PROTOCOL_HASH = "52b6f6235f45c17391b3a6f1c9259e113991cb6b155c6b8485355924a2858a4e"
PINS = {
    "sources/textual_restoration/discovery/en_gedi_renderer_probe.v1.json": "ed6373c7490973dea44346cce7fc758c3e1be9c27d2cd253e8e5abaca8937aa2",
    "tools/textual_restoration/build_en_gedi_renderer_probe.py": "7e9084610b9e8ad70890aec4ec5df3b7d733dc25620914fd8554c7a5b5d78dcf",
    "tools/textual_restoration/probe_en_gedi_mapping.py": "f5531876a7c03031c6021da8feed888bc3d9274173229cb575152ba58269a5ac",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_points(protocol, previous):
    known = {tuple(p) for k in ("development_texture_xy", "held_out_texture_xy") for p in previous[k]}
    rows = sorted(set(protocol["whole_height_rows"] + protocol["acquisition_band_rows"]))
    union = [(x, y) for y in rows for x in protocol["columns"]]
    return [p for p in union if p not in known], {
        "nominal_grid_slots": len(protocol["columns"]) * (len(protocol["whole_height_rows"]) + len(protocol["acquisition_band_rows"])),
        "union_grid_points": len(union), "overlap_slots_deduplicated": len(protocol["columns"]) * len(set(protocol["whole_height_rows"]) & set(protocol["acquisition_band_rows"])),
        "previously_observed_points_removed": [list(p) for p in union if p in known],
        "novel_targets": sum(p not in known for p in union),
    }


def preflight(mapping, radius, shift, interval, available_slices, size=(1400, 1400)):
    missing, outside = set(), []
    for distance, point in line_positions(mapping, radius, interval, shift):
        x, y, z = np.floor(point).astype(int)
        missing.update({int(z), int(z + 1)} - available_slices)
        if x < 0 or y < 0 or z < 0 or x + 1 >= size[0] or y + 1 >= size[1]:
            outside.append({"normal_offset": distance, "xyz": point.tolist()})
    if outside:
        return {"status": "outside-volume", "outside_samples": outside, "missing_slice_numbers": sorted(missing)}
    if missing:
        return {"status": "unavailable-slices", "missing_slice_numbers": sorted(missing)}
    return {"status": "evaluable"}


def summarize(results):
    errors = [r["residual"] for r in results if r["status"] == "evaluated"]
    counts = dict(Counter(r["status"] for r in results))
    unavailable = sum(r["status"] in {"unavailable-slices", "outside-volume"} for r in results)
    return {"targets": len(results), "status_counts": counts, "evaluable_count": len(errors),
            "exact_matches": errors.count(0), "nonzero_residuals": sum(e != 0 for e in errors),
            "signed_residual_histogram": {str(e): errors.count(e) for e in sorted(set(errors))},
            "mean_absolute_error": float(np.mean(np.abs(errors))) if errors else None,
            "root_mean_square_error": float(np.sqrt(np.mean(np.square(np.array(errors, dtype=float))))) if errors else None,
            "maximum_absolute_error": max(map(abs, errors)) if errors else None,
            "observed_exact_match": all(e == 0 for e in errors) if errors else None,
            "scope_status": "incomplete" if unavailable or not errors else ("pass" if not any(errors) else "fail")}


def build(directory):
    if sha(PROTOCOL) != PROTOCOL_HASH:
        raise ValueError("frozen wider protocol changed")
    for rel, digest in PINS.items():
        if sha(ROOT / rel) != digest:
            raise ValueError(f"frozen prior evidence changed: {rel}")
    protocol = json.loads(PROTOCOL.read_text())
    previous = json.loads((DISCOVERY / "en_gedi_renderer_protocol.v1.json").read_text())
    points, denominator = select_points(protocol, previous)
    # This revalidates actual payload hashes/CRC/lengths and all nine old results.
    prior = prior_build(directory)
    if prior != json.loads((DISCOVERY / "en_gedi_renderer_probe.v1.json").read_text()):
        raise ValueError("old numeric receipt did not reproduce")
    acquired = {}
    for audit in ("mapping-audit", "ct-probe-audit", "renderer-ct-audit"):
        receipt = json.loads((directory / audit / "receipt.json").read_text())
        for member in receipt["member_payloads_verified"]:
            acquired[member["archive_member"]] = directory / audit / member["local_file"]
    with gzip.open(acquired["segmentations/merge5/PerPixelMapping.yml.gz"], "rt", encoding="ascii") as stream:
        rows, cols, scalar_count, mappings = sample_map(stream, points)
    if (rows, cols, scalar_count) != (3358, 1969, 39671412):
        raise ValueError("unexpected mapping dimensions")
    slices = {}
    for member, path in acquired.items():
        if member.endswith(".tif"):
            with Image.open(path) as image:
                data = np.asarray(image)
                if data.shape != (1400, 1400) or data.dtype != np.uint16:
                    raise ValueError("invalid slice")
                slices[int(Path(member).stem)] = data.copy()
    metadata = []
    with Image.open(directory / "segment-audit/member-03.png") as mask:
        for point in points:
            metadata.append({"texture_xy": list(point), "mask_value": mask.getpixel(point),
                             "spatial_group": "acquisition-band" if point[1] in protocol["acquisition_band_rows"] else "whole-height-grid",
                             "horizontal_quartile": min(3, point[0] * 4 // cols), "xyz_normal": mappings[point]})
    candidates = []
    # All availability decisions finish before any NEW texture value is read.
    for radius in previous["radius_parameters_voxels"]:
        for shift in previous["slice_index_offsets"]:
            for mode in previous["interpolators"]:
                candidate = {"radius_parameter": radius, "slice_index_offset": shift, "interpolator": mode, "results": []}
                for index, row in enumerate(metadata):
                    availability = ({"status": "mask-invalid"} if row["mask_value"] != 255 else
                                    preflight(row["xyz_normal"], radius, shift, previous["sampling_interval_voxels"], set(slices)))
                    candidate["results"].append({"point_index": index, **availability})
                candidates.append(candidate)
    evaluated_indices = {r["point_index"] for c in candidates for r in c["results"] if r["status"] == "evaluable"}
    common = set.intersection(*[{r["point_index"] for r in c["results"] if r["status"] == "evaluable"} for c in candidates])
    with Image.open(directory / "segment-audit/member-02.png") as texture:
        for index in sorted(evaluated_indices):
            metadata[index]["published_texture_value"] = int(texture.getpixel(tuple(metadata[index]["texture_xy"])))
    for candidate in candidates:
        for result in candidate["results"]:
            if result["status"] != "evaluable":
                continue
            row = metadata[result["point_index"]]
            prediction = sample_line(slices, row["xyz_normal"], candidate["radius_parameter"],
                                     previous["sampling_interval_voxels"], candidate["slice_index_offset"], candidate["interpolator"])
            result.update(prediction)
            result["status"] = "evaluated"
            result["residual"] = prediction["prediction"] - row["published_texture_value"]
        candidate["summary"] = summarize(candidate["results"])
        candidate["full_predeclared_sample_status"] = candidate["summary"]["scope_status"]
        candidate["by_spatial_group"] = {group: summarize([r for r in candidate["results"] if metadata[r["point_index"]]["spatial_group"] == group]) for group in ("whole-height-grid", "acquisition-band")}
        candidate["by_horizontal_quartile"] = {str(q): summarize([r for r in candidate["results"] if metadata[r["point_index"]]["horizontal_quartile"] == q]) for q in range(4)}
        candidate["by_texture_row"] = {str(y): summarize([r for r in candidate["results"] if metadata[r["point_index"]]["texture_xy"][1] == y]) for y in sorted({p[1] for p in points})}
        candidate["common_coverage_summary"] = summarize([r for r in candidate["results"] if r["point_index"] in common])
    ties = []
    for index in sorted(common):
        predictions = {}
        for ci, candidate in enumerate(candidates):
            prediction = candidate["results"][index]["prediction"]
            predictions.setdefault(str(prediction), []).append(ci)
        ties.append({"point_index": index, "prediction_candidate_groups": predictions,
                     "exact_matching_candidates": [ci for ci, c in enumerate(candidates) if c["results"][index]["residual"] == 0]})
    return {"schema_version": "1.0.0", "checked_date": "2026-09-05", "protocol": protocol,
            "protocol_sha256": sha(PROTOCOL), "input_pins": PINS,
            "implementation_sha256": sha(Path(__file__).resolve()),
            "prior_receipt_reproduced": True, "input_payloads": prior["input_payloads"],
            "texture_sha256": prior["texture_sha256"], "mask_sha256": "053e96cb8658e68ab2d62a1ea99947f69115093fd40d93838663a55dd26d9087",
            "runtime": {"python": sys.version.split()[0], "numpy": np.__version__},
            "denominator": {**denominator, "mask_invalid": sum(r["mask_value"] != 255 for r in metadata),
                            "mask_valid": sum(r["mask_value"] == 255 for r in metadata),
                            "evaluable_any_candidate": len(evaluated_indices), "evaluable_all_candidates": len(common)},
            "ct_slice_numbers": sorted(slices), "mapping_shape": [rows, cols, 6],
            "complete_mapping_gzip_stream_read": True, "points": metadata, "candidates": candidates,
            "common_coverage_point_indices": sorted(common), "common_coverage_candidate_ties": ties,
            "policy": {"parameters_tuned": False, "contrast_fitted": False, "new_payloads_acquired": False,
                       "multiple_segments_validated": False, "original_renderer_executed": False,
                       "bit_exact_opencv_emulation_verified": False, "master_registration_verified": False,
                       "transcription_benchmark_executed": False, "new_letter_reading_claimed": False,
                       "generated_images_used": False, "canonical_change_applied": False},
            "license": prior["license"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = build(args.directory)
    if args.verify_only:
        if result != json.loads((DISCOVERY / "en_gedi_wider_renderer_check.v1.json").read_text()):
            raise ValueError("wider numeric receipt differs")
        print("Verified wider receipt and previous nine-point receipt against actual inputs.")
    else:
        print(json.dumps(result, ensure_ascii=False))
