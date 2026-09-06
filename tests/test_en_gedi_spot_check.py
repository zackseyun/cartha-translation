"""Receipt integrity checks, not independent validation of historical readings."""
import hashlib
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class EnGediSpotCheckTests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((ROOT / "sources/textual_restoration/discovery/en_gedi_published_spot_check.v1.json").read_text())

    def test_checks_are_bound_to_current_source_words_not_notes(self):
        self.assertEqual(len(self.receipt["checks"]), 3)
        for check in self.receipt["checks"]:
            with self.subTest(reference=check["reference"]):
                raw = (ROOT / check["pob_path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), check["pob_sha256"])
                source = yaml.safe_load(raw)["source"]["text"]
                words = ["".join(re.findall(r"[א-ת]", w)) for w in source.split()]
                self.assertEqual(words.count(check["published_consonantal_word"]), check["source_word_matches"])
                self.assertEqual(check["source_word_matches"], 1)

    def test_narrow_publication_basis_is_not_promoted(self):
        self.assertTrue(all(value is False for value in self.receipt["policy"].values()))
        self.assertTrue(all(c["preservation_basis"] == "unbracketed-in-published-transcription"
                            for c in self.receipt["checks"]))
        self.assertTrue(all(c["edition_locator"] for c in self.receipt["checks"]))

    def test_asset_receipt_does_not_claim_raw_signal_recovery(self):
        asset = json.loads((ROOT / "sources/textual_restoration/discovery/en_gedi_asset_check.v1.json").read_text())
        self.assertTrue(all(value is False for value in asset["policy"].values()))
        self.assertEqual(asset["master"]["dimensions"], [12100, 5373])
        self.assertEqual(len(asset["members"]), 4)
        archive = asset["segmentation_archive"]
        self.assertEqual(archive["entry_count"], 29285)
        self.assertEqual(archive["file_count"], 29259)
        self.assertEqual(len(archive["segment_groups"]), 7)
        self.assertIn("by-nc", asset["license_url"])

    def test_volume_probe_is_not_a_transcription_benchmark(self):
        probe = json.loads((ROOT / "sources/textual_restoration/discovery/en_gedi_volume_probe.v1.json").read_text())
        self.assertTrue(all(value is False for value in probe["policy"].values()))
        self.assertEqual(probe["ct_index"]["numbered_slices"], 4504)
        self.assertEqual(probe["mapping"]["scalar_count"], 3358 * 1969 * 6)
        self.assertIsNone(probe["intensity_probe"]["preferred_index_offset"])
        self.assertEqual(len(probe["intensity_probe"]["profiles"]), 2)
        exterior = next(s for s in probe["mapping"]["samples"] if s["texture_xy"] == [0, 0])
        self.assertEqual(exterior["mask_value"], 0)
        self.assertEqual(len(probe["ct_tiff_metadata"]), 4)

    def test_new_objects_keep_language_and_identity_boundaries(self):
        registry = json.loads((ROOT / "sources/textual_restoration/ot_witness_registry.v1.json").read_text())
        witnesses = {w["id"]: w for w in registry["witnesses"]}
        eg = witnesses[self.receipt["witness_id"]]
        greek = witnesses["8hev-greek-minor-prophets"]
        self.assertEqual(eg["languages"], ["Hebrew"])
        self.assertEqual(greek["languages"], ["Greek"])
        self.assertEqual(greek["witness_class"], "ancient-daughter-version")
        self.assertEqual(greek["coverage_status"], "unmapped")
        self.assertNotEqual(eg["relationship_group"], greek["relationship_group"])

    def test_renderer_probe_keeps_frozen_protocol_and_unpromoted_scope(self):
        folder = ROOT / "sources/textual_restoration/discovery"
        probe = json.loads((folder / "en_gedi_renderer_probe.v1.json").read_text())
        protocol = (folder / "en_gedi_renderer_protocol.v1.json").read_bytes()
        self.assertEqual(probe["protocol_sha256"], hashlib.sha256(protocol).hexdigest())
        self.assertEqual(probe["protocol_sha256"], "39da0c620750511462a1a76d28edaa42bf507d11e0b7dac14d912b986bc13d14")
        self.assertEqual(probe["protocol"], json.loads(protocol))
        self.assertTrue(all(value is False for value in probe["policy"].values()))
        self.assertIsNone(probe["selected_candidate"])
        self.assertEqual(len(probe["points"]), 9)
        self.assertEqual(len(probe["candidates"]), 8)
        self.assertEqual(len(probe["input_payloads"]), 8)
        for path, digest in probe["implementation_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)

    def test_renderer_residuals_and_summary_are_not_accuracy_rates(self):
        probe = json.loads((ROOT / "sources/textual_restoration/discovery/en_gedi_renderer_probe.v1.json").read_text())
        points = {tuple(p["texture_xy"]): p for p in probe["points"]}
        for candidate in probe["candidates"]:
            self.assertEqual({tuple(r["texture_xy"]) for r in candidate["results"]}, set(points))
            self.assertEqual(len(candidate["results"]), len(points))
            for result in candidate["results"]:
                point = points[tuple(result["texture_xy"])]
                self.assertEqual(result["group"], point["group"])
                self.assertEqual(result["residual"], result["prediction"] - point["published_texture_value"])
                self.assertEqual(result["sample_count"], 2 * int(candidate["radius_parameter"] / .5))
            for group, summary in candidate["summary"].items():
                errors = [r["residual"] for r in candidate["results"] if r["group"] == group]
                self.assertEqual(summary["count"], 1 if group == "development" else 8)
                self.assertEqual(summary["exact_matches"], errors.count(0))
                self.assertEqual(summary["mean_absolute_error"], sum(map(abs, errors)) / len(errors))
                self.assertEqual(summary["maximum_absolute_error"], max(map(abs, errors)))


if __name__ == "__main__":
    unittest.main()
