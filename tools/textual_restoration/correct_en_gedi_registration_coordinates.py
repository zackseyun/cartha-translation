#!/usr/bin/env python3
"""Versioned pixel-center correction; no feature search, refit or image output."""
import argparse
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from tools.textual_restoration import register_en_gedi_segment as previous

PREVIOUS_SHA = "f9af202b19413d80234a2721cc9593d3c945014e786a7fe81da590dcef55c6ab"
OUTPUT = ROOT / "sources/textual_restoration/discovery/en_gedi_registration_check.v2.json"


def offsets(scales):
    return (np.asarray(scales,dtype=np.float64)-1)/2


def corrected_matrix(matrix, texture_delta, master_delta):
    m=np.asarray(matrix,dtype=np.float64).copy()
    m[:,2] += master_delta - m[:,:2] @ texture_delta
    return m


def build(evidence):
    if previous.sha(previous.OUTPUT) != PREVIOUS_SHA:
        raise ValueError("Frozen v1 receipt drift")
    old=json.loads(previous.OUTPUT.read_text())
    if previous.build(evidence) != old:
        raise ValueError("Actual v1 run did not reproduce")
    dt,dm=offsets(old["original_per_analysis_pixel"])
    matrix=corrected_matrix(old["affine_original_pixels"],dt,dm)
    rows=copy.deepcopy(old["pairs"])
    for row in rows:
        row["texture_xy"]=(np.asarray(row["texture_xy"])+dt).tolist()
        row["master_xy"]=(np.asarray(row["master_xy"])+dm).tolist()
        pred=previous.project([row["texture_xy"]],matrix)[0]
        row["predicted_master_xy"]=pred.tolist()
        row["residual_master_pixels"]=float(np.linalg.norm(pred-row["master_xy"]))
    projections=copy.deepcopy(old["prior_nineteen_target_projections"])
    for row in projections:
        # These are original integer pixel centers, not analysis coordinates.
        row["projected_master_xy"]=previous.project([row["texture_xy"]],matrix)[0].tolist()
    corrected_gate=previous.gate(rows,1969,3358,old["protocol"]["provisional_region_gate"])
    if corrected_gate["checks"] != old["coarse_registration_gate"]["checks"]:
        raise ValueError("Coordinate repair unexpectedly changes scientific criterion outcome")
    return {"schema_version":"2.0.0", "previous_receipt_sha256":PREVIOUS_SHA,
            "previous_actual_run_reproduced":True, "builder_sha256":previous.sha(Path(__file__)),
            "protocol_sha256":old["protocol_sha256"], "runtime":old["runtime"],
            "correction":"v1 used coordinate*scale; original integer pixel centers require (coordinate+0.5)*scale-0.5. Affine matrix conjugated by domain/codomain translations; no feature search or refit.",
            "texture_center_offset":dt.tolist(), "master_center_offset":dm.tolist(),
            "affine_original_pixel_centers":matrix.tolist(), "pairs":rows,
            "coarse_registration_gate":corrected_gate,
            "prior_nineteen_target_projections":projections,
            "texture_rectangle_in_master":previous.project([[0,0],[1968,0],[1968,3357],[0,3357]],matrix).tolist(),
            "maximum_absolute_residual_change":max(abs(a["residual_master_pixels"]-b["residual_master_pixels"]) for a,b in zip(rows,old["pairs"])),
            "registration_accepted":False, "letter_labels_assigned":False,
            "reading_benchmark_executed":False,"image_outputs_written":False,
            "limits":"Correct coordinate bookkeeping does not repair the failed spatial fit. V1 evidence stays immutable; all unaccepted projections remain development hypotheses, not manuscript locators."}


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("evidence",type=Path)
    p.add_argument("--write",action="store_true")
    args=p.parse_args()
    result=build(args.evidence)
    if args.write:
        with OUTPUT.open("xb") as stream:
            stream.write((json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ("pairs","prior_nineteen_target_projections")},indent=2))
