#!/usr/bin/env python3
"""Verify retained acquisition metadata and all six private payloads, not ink."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration import acquire_en_gedi_textures as acquisition

DIRECTORY = ROOT / "sources/textual_restoration/discovery"
RECEIPT = DIRECTORY / "en_gedi_texture_acquisition.v1.json"
TRIAGE = DIRECTORY / "en_gedi_texture_triage.v1.json"


def check(directory):
    plan = json.loads(acquisition.PROTOCOL.read_text())
    acquisition.validate_plan(plan)
    receipt = json.loads(RECEIPT.read_text())
    triage = json.loads(TRIAGE.read_text())
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    require(receipt == json.loads((directory / "receipt.json").read_text()), "private/public receipt drift")
    require(receipt["protocol_sha256"] == acquisition.sha(acquisition.PROTOCOL), "protocol drift")
    require(receipt["tool_sha256"] == acquisition.sha(Path(acquisition.__file__)), "acquisition tool drift")
    require(receipt["status"] == "complete" and len(receipt["members"]) == 6, "incomplete acquisition")
    require(receipt["prior_index_sha256"] == plan["prior_index_sha256"], "prior index binding drift")
    for key in ("archive_url", "archive_bytes", "etag"):
        require(receipt[key] == plan[key], "archive identity drift")
    require(not receipt["full_archive_hash_verified"] and not receipt["scientific_reading_pass"], "overclaimed verification")
    for expected, actual in zip(plan["members"], receipt["members"]):
        require(all(actual[k] == v for k, v in expected.items()), "member metadata drift")
        path = directory / expected["local_file"]
        require(path.stat().st_size == expected["bytes"], "payload length drift")
        require(acquisition.sha(path) == actual["sha256"], "payload hash drift")
        require(acquisition.png_size(path) == actual["size_xy"], "PNG dimension drift")
    require(receipt["http_payload_bytes"] == sum(r["length"] for r in receipt["http_ranges"]), "HTTP accounting drift")
    for r in receipt["http_ranges"]:
        require(0 <= r["start"] < plan["archive_bytes"] and
                0 < r["length"] <= 33554432 and
                r["start"] + r["length"] <= plan["archive_bytes"], "range bounds drift")
    require([o["local_file"] for o in triage["observations"]] ==
            [m["local_file"] for m in plan["members"]], "incomplete triage")
    require(all(not o["accepted_letter_labels"] and o["accepted_verse_locator"] is None
                for o in triage["observations"]), "unreviewed labels")
    require(triage["selection_after_visual_triage"] == "remerge" and
            triage["development_only"] and not triage["blind_evaluation"] and
            not triage["scientific_reading_pass"] and not triage["new_transcription"] and
            not triage["canonical_change"], "triage scope drift")
    return {"members_verified": 6, "expanded_bytes": sum(m["bytes"] for m in plan["members"]),
            "http_payload_bytes": receipt["http_payload_bytes"], "scientific_reading_pass": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    print(json.dumps(check(parser.parse_args().directory), indent=2))
