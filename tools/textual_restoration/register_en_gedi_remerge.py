#!/usr/bin/env python3
"""Fixed, spatially partitioned development correspondence; JSON output only."""
import argparse
import json
from pathlib import Path
import sys

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration.register_en_gedi_segment import checked_image, project, gate, sha

DIR = ROOT / "sources/textual_restoration/discovery"
PROTOCOL = DIR / "en_gedi_remerge_registration_protocol.v1.json"
PROTOCOL_SHA = "911e3035ceca727eb8306cb32637978bcdee6193b9b3baa19325287041cc7931"
PRIOR = DIR / "en_gedi_remerge_mapping_check.v1.json"
OUTPUT = DIR / "en_gedi_remerge_registration_check.v1.json"


def lift(xy, scale):
    return ((np.asarray(xy, dtype=np.float64) + 0.5) * scale - 0.5).tolist()


def deduplicate(rows):
    ordered = sorted(rows, key=lambda r: (r["descriptor_distance"], r["second_distance"],
                     r["texture_xy"][1], r["texture_xy"][0], r["master_xy"][1], r["master_xy"][0]))
    seen_t, seen_m, kept, rejected = set(), set(), [], []
    for row in ordered:
        t = tuple(np.floor(row["texture_xy"]).astype(int))
        m = tuple(np.floor(row["master_xy"]).astype(int))
        repeated = [name for name, key, seen in (("texture", t, seen_t), ("master", m, seen_m)) if key in seen]
        if repeated:
            rejected.append({**row, "repeated_retained_endpoint_bins": repeated})
        else:
            seen_t.add(t)
            seen_m.add(m)
            kept.append(row.copy())
    return kept, rejected


def partition(rows, tile_size):
    rows.sort(key=lambda r: (r["texture_xy"][1], r["texture_xy"][0], r["master_xy"][1], r["master_xy"][0]))
    for i, row in enumerate(rows):
        tx, ty = [int(np.floor(v / tile_size)) for v in row["texture_xy"]]
        row.update(index=i, texture_tile=[tx, ty],
                   partition="validation" if (tx + 2 * ty) % 3 == 2 else "fit", ransac_inlier=None)


def build(evidence, textures, mapping):
    if sha(PROTOCOL) != PROTOCOL_SHA:
        raise ValueError("frozen protocol drift")
    p = json.loads(PROTOCOL.read_text())
    if sha(PRIOR) != p["inputs"]["mapping_receipt_sha256"]:
        raise ValueError("prior geometry drift")
    a = p["algorithm"]
    if cv2.__version__ != a["opencv_version"]:
        raise ValueError("unreviewed OpenCV version")
    cv2.setNumThreads(1)
    cv2.setRNGSeed(a["rng_seed"])
    texture = checked_image(textures / "remerge.png", p["inputs"]["texture_sha256"], (2400, 4067))
    mask = checked_image(mapping / "PerPixelMask.png", p["inputs"]["mask_sha256"], (2400, 4067))
    master = checked_image(evidence / "EnGedi-MasterView-scale-hires.png", p["inputs"]["master_sha256"], (12100, 5373))
    arrays, masks, scales = [], [], []
    for im, divisor, valid in ((texture, a["texture_divisor"], mask), (master, a["master_divisor"], None)):
        h, w = im.shape
        size = (w // divisor, h // divisor)
        arrays.append(cv2.resize(im, size, interpolation=cv2.INTER_AREA))
        masks.append(cv2.resize(valid, size, interpolation=cv2.INTER_NEAREST) if valid is not None else None)
        scales.append([w / size[0], h / size[1]])
    sift = cv2.SIFT_create(nfeatures=a["sift_nfeatures"], contrastThreshold=a["sift_contrast_threshold"])
    (kt, dt), (km, dm) = [sift.detectAndCompute(im, valid) for im, valid in zip(arrays, masks)]
    raw = []
    if dt is not None and dm is not None and len(dm) >= 2:
        matcher = cv2.BFMatcher(cv2.NORM_L2)
        forward = matcher.knnMatch(dt, dm, k=2)
        reverse = {m.queryIdx: m.trainIdx for m in matcher.match(dm, dt)}
        for first, second in forward:
            if first.distance < a["match_ratio"] * second.distance and reverse.get(first.trainIdx) == first.queryIdx:
                raw.append({"texture_keypoint_index": first.queryIdx, "master_keypoint_index": first.trainIdx,
                            "texture_xy": lift(kt[first.queryIdx].pt, scales[0]),
                            "master_xy": lift(km[first.trainIdx].pt, scales[1]),
                            "descriptor_distance": float(first.distance), "second_distance": float(second.distance)})
    pairs, rejected = deduplicate(raw)
    partition(pairs, a["tile_size"])
    fitting = [r for r in pairs if r["partition"] == "fit"]
    matrix = None
    if len(fitting) >= 3:
        matrix, inliers = cv2.estimateAffine2D(np.array([r["texture_xy"] for r in fitting]),
            np.array([r["master_xy"] for r in fitting]), method=cv2.RANSAC,
            ransacReprojThreshold=a["ransac_reprojection_threshold"], maxIters=a["max_iterations"],
            confidence=a["confidence"], refineIters=a["refine_iterations"])
    finite_fit = matrix is not None and np.isfinite(matrix).all()
    if finite_fit:
        for row, keep in zip(fitting, inliers.ravel()):
            row["ransac_inlier"] = bool(keep)
        for row, predicted in zip(pairs, project([r["texture_xy"] for r in pairs], matrix)):
            row["predicted_master_xy"] = predicted.tolist()
            row["residual_master_pixels"] = float(np.linalg.norm(predicted - row["master_xy"]))
        outcome = gate(pairs, 2400, 4067, p["coarse_gate"])
    else:
        outcome = {"status": "fail", "reason": "no finite affine fit; no retuning"}
    prior = json.loads(PRIOR.read_text())
    projections = [{"prior_point_index": i, "texture_xy": row["xy"], "mask_value": row["mask_value"],
                    "projected_master_xy": project([row["xy"]], matrix)[0].tolist() if finite_fit else None,
                    "accepted_verse_locator": None, "accepted_letter_label": None} for i, row in enumerate(prior["points"])]
    return {"schema_version": "1.0.0", "protocol_sha256": PROTOCOL_SHA, "protocol": p,
            "implementation_sha256": sha(Path(__file__)),
            "helper_sha256": sha(ROOT / "tools/textual_restoration/register_en_gedi_segment.py"),
            "runtime": {"opencv": cv2.__version__, "numpy": np.__version__, "opencv_threads": cv2.getNumThreads()},
            "analysis_sizes": [list(im.shape[::-1]) for im in arrays], "coordinate_scales": scales,
            "keypoint_counts": [len(kt), len(km)], "mutual_ratio_pairs": len(raw),
            "geometric_pairs_retained": len(pairs), "geometric_pairs_rejected": len(rejected),
            "pairs": pairs, "rejected_pairs": rejected,
            "affine_original_pixels": matrix.tolist() if finite_fit else None,
            "coarse_registration_gate": outcome,
            "texture_corners_projected": project([[0,0],[2399,0],[2399,4066],[0,4066]], matrix).tolist() if finite_fit else None,
            "prior_geometry_projections": projections,
            "interpretation": "Coarse development correspondence only. No projected target is an accepted letter or verse locator.",
            "reading_benchmark_executed": False, "image_outputs_written": False, "canonical_change": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("textures", type=Path)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build(args.evidence, args.textures, args.mapping)
    if args.write:
        with OUTPUT.open("x") as out:
            out.write(json.dumps(result, indent=2) + "\n")
    elif result != json.loads(OUTPUT.read_text()):
        raise ValueError("actual inputs do not reproduce saved result")
    print(json.dumps({k: result[k] for k in ("mutual_ratio_pairs", "geometric_pairs_retained", "geometric_pairs_rejected", "coarse_registration_gate", "texture_corners_projected")}, indent=2))
