#!/usr/bin/env python3
"""Fixed development registration of immutable PNGs; never outputs edited imagery."""
import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "sources/textual_restoration/discovery/en_gedi_registration_protocol.v1.json"
PROTOCOL_SHA = "824d27f65a5092b3f9aef0504875818bc53dae4292da1f140dd0c8d061128669"
PRIOR = ROOT / "sources/textual_restoration/discovery/en_gedi_distant_rows_check.v1.json"
PRIOR_SHA = "102668ae837f884a1eece4357c548bdeda8095d22c1b1204558b460cda179394"
OUTPUT = ROOT / "sources/textual_restoration/discovery/en_gedi_registration_check.v1.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_image(path, expected, dimensions):
    if path.is_symlink() or sha(path) != expected:
        raise ValueError("Image provenance mismatch")
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None or image.shape[::-1] != dimensions or image.dtype != np.uint8:
        raise ValueError("Unexpected grayscale image dimensions/type")
    return image


def project(points, matrix):
    points = np.asarray(points, dtype=np.float64).reshape(-1, 2)
    return np.column_stack((points, np.ones(len(points)))) @ np.asarray(matrix).T


def gate(rows, width, height, thresholds):
    training = [r for r in rows if r["partition"] == "fit" and r["ransac_inlier"]]
    validation = [r for r in rows if r["partition"] == "validation"]
    near = sum(r["residual_master_pixels"] <= 20 for r in validation)
    fraction = near / len(validation) if validation else None
    xspan = (max(r["texture_xy"][0] for r in training) - min(r["texture_xy"][0] for r in training)) / width if training else 0
    yspan = (max(r["texture_xy"][1] for r in training) - min(r["texture_xy"][1] for r in training)) / height if training else 0
    checks = {
        "training_count": len(training) >= thresholds["minimum_training_inliers"],
        "validation_count": len(validation) >= thresholds["minimum_validation_pairs"],
        "validation_agreement": fraction is not None and fraction >= thresholds["minimum_validation_fraction_within_20_master_pixels"],
        "x_span": xspan >= thresholds["minimum_texture_inlier_x_span_fraction"],
        "y_span": yspan >= thresholds["minimum_texture_inlier_y_span_fraction"],
    }
    return {"status": "pass" if all(checks.values()) else "fail", "checks": checks,
            "training_inliers": len(training), "validation_pairs": len(validation),
            "validation_within_20": near, "validation_fraction_within_20": fraction,
            "training_texture_x_span_fraction": xspan, "training_texture_y_span_fraction": yspan}


def build(evidence):
    if sha(PROTOCOL) != PROTOCOL_SHA or sha(PRIOR) != PRIOR_SHA:
        raise ValueError("Frozen protocol/prior receipt drift")
    p = json.loads(PROTOCOL.read_text())
    a = p["algorithm"]
    if cv2.__version__ != a["opencv_version"]:
        raise ValueError("Unreviewed OpenCV version")
    cv2.setNumThreads(1)
    cv2.setRNGSeed(a["rng_seed"])
    master = checked_image(evidence / "EnGedi-MasterView-scale-hires.png", p["inputs"]["master_sha256"], (12100, 5373))
    texture = checked_image(evidence / "segment-audit/member-02.png", p["inputs"]["texture_sha256"], (1969, 3358))
    mask = checked_image(evidence / "segment-audit/member-03.png", p["inputs"]["mask_sha256"], (1969, 3358))
    images, masks, scales = [], [], []
    for img, divisor, valid in ((texture, 2, mask), (master, 4, None)):
        h, w = img.shape
        size = (w // divisor, h // divisor)
        images.append(cv2.resize(img, size, interpolation=cv2.INTER_AREA))
        masks.append(cv2.resize(valid, size, interpolation=cv2.INTER_NEAREST) if valid is not None else None)
        scales.append([w / size[0], h / size[1]])
    sift = cv2.SIFT_create(nfeatures=a["sift_nfeatures"], contrastThreshold=a["sift_contrast_threshold"])
    (kt, dt), (km, dm) = [sift.detectAndCompute(im, mask) for im, mask in zip(images, masks)]
    pairs = []
    if dt is not None and dm is not None and len(dm) >= 2:
        matcher = cv2.BFMatcher(cv2.NORM_L2)
        forward = matcher.knnMatch(dt, dm, k=2)
        reverse = {m.queryIdx: m.trainIdx for m in matcher.match(dm, dt)}
        for first, second in forward:
            if first.distance < 0.75 * second.distance and reverse.get(first.trainIdx) == first.queryIdx:
                tx, ty = np.asarray(kt[first.queryIdx].pt) * scales[0]
                mx, my = np.asarray(km[first.trainIdx].pt) * scales[1]
                pairs.append({"texture_xy": [float(tx), float(ty)], "master_xy": [float(mx), float(my)],
                              "descriptor_distance": float(first.distance), "second_distance": float(second.distance)})
    pairs.sort(key=lambda r: (r["texture_xy"][1], r["texture_xy"][0], r["master_xy"][1], r["master_xy"][0]))
    for i, row in enumerate(pairs):
        row.update(index=i, partition="validation" if i % 3 == 2 else "fit", ransac_inlier=None)
    fitting = [r for r in pairs if r["partition"] == "fit"]
    matrix, inliers = None, None
    if len(fitting) >= 3:
        matrix, inliers = cv2.estimateAffine2D(np.array([r["texture_xy"] for r in fitting]),
            np.array([r["master_xy"] for r in fitting]), method=cv2.RANSAC,
            ransacReprojThreshold=a["ransac_reprojection_threshold"], maxIters=a["max_iterations"],
            confidence=a["confidence"], refineIters=a["refine_iterations"])
    if matrix is None or not np.isfinite(matrix).all():
        raise ValueError("No finite affine fit; do not claim registration or tune frozen protocol")
    for row, is_inlier in zip(fitting, inliers.ravel()):
        row["ransac_inlier"] = bool(is_inlier)
    for row, pred in zip(pairs, project([r["texture_xy"] for r in pairs], matrix)):
        row["predicted_master_xy"] = pred.tolist()
        row["residual_master_pixels"] = float(np.linalg.norm(pred - row["master_xy"]))
    prior = json.loads(PRIOR.read_text())
    candidates = [c for c in prior["candidates"] if c["radius_parameter"] == 7 and c["slice_index_offset"] == 0 and c["interpolator"] == "historical-c10-corner"]
    if len(candidates) != 1:
        raise ValueError("Primary candidate identity mismatch")
    targets = [r for r in candidates[0]["results"] if r["status"] == "evaluated"]
    if len(targets) != 19:
        raise ValueError("Expected original nineteen measured targets")
    projections = []
    for r in targets:
        xy = prior["points"][r["point_index"]]["texture_xy"]
        projections.append({"prior_point_index": r["point_index"], "texture_xy": xy,
                            "projected_master_xy": project([xy], matrix)[0].tolist(),
                            "letter_label": None})
    return {"schema_version": "1.0.0", "protocol_sha256": PROTOCOL_SHA, "protocol": p,
            "builder_sha256": sha(Path(__file__)), "prior_receipt_sha256": PRIOR_SHA,
            "runtime": {"opencv": cv2.__version__, "numpy": np.__version__, "opencv_threads": cv2.getNumThreads()},
            "image_dimensions": {"texture": [1969, 3358], "master": [12100, 5373]},
            "analysis_dimensions": [list(im.shape[::-1]) for im in images], "original_per_analysis_pixel": scales,
            "keypoints": {"texture": len(kt), "master": len(km)}, "pair_count": len(pairs),
            "affine_original_pixels": matrix.tolist(), "pairs": pairs,
            "coarse_registration_gate": gate(pairs, 1969, 3358, p["provisional_region_gate"]),
            "texture_rectangle_in_master": project([[0,0],[1968,0],[1968,3357],[0,3357]], matrix).tolist(),
            "prior_nineteen_target_projections": projections,
            "interpretation": "Numeric correspondence only; edition-based region identification recorded separately. No letter or blank-pixel labels assigned by this tool.",
            "reading_benchmark_executed": False, "image_outputs_written": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build(args.evidence)
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.write:
        with OUTPUT.open("xb") as stream:
            stream.write(raw)
    print(json.dumps({k:v for k,v in result.items() if k not in ("pairs", "protocol")}, indent=2))
