"""Guard source/observation boundaries and fail-closed receipt verification."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from tools.textual_restoration.check_lev2_version_controls import RECEIPT, sha256, verify_local, verify_private


class LeviticusVersionControlsTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECEIPT.read_text())

    def test_current_pob_and_context_are_bound(self):
        verify_local(self.record)

    def test_local_drift_is_rejected(self):
        changed = copy.deepcopy(self.record)
        key = "translation/ot/leviticus/002/008.yaml"
        changed["local_file_sha256"][key] = "0" * 64
        with self.assertRaisesRegex(ValueError, "local file changed"):
            verify_local(changed)

    def test_missing_private_evidence_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                verify_private(self.record, Path(directory))

    def test_tampered_private_observation_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            source = self.record["source_observations"][0]
            (Path(directory) / source["snapshot_file"]).write_text("changed")
            with self.assertRaisesRegex(ValueError, "transcript changed"):
                verify_private(self.record, Path(directory))

    def test_excerpt_assertions_are_checked_after_hash(self):
        record = copy.deepcopy(self.record)
        record["source_observations"] = record["source_observations"][:1]
        source = record["source_observations"][0]
        raw = source["url"].encode()
        source["snapshot_sha256"] = sha256(raw)
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / source["snapshot_file"]).write_bytes(raw)
            with self.assertRaisesRegex(ValueError, "observation missing"):
                verify_private(record, Path(directory))

    def test_cross_verse_and_versional_boundaries(self):
        self.assertIn("following verse", self.record["greek"]["approach"]["analysis"])
        self.assertEqual(self.record["greek"]["following_subject"], "ἀφελεῖ ὁ ἱερεὺς")
        clauses = {c["clause"]: c for c in self.record["syriac"]}
        self.assertIn("second masculine", clauses["delivery"]["analysis"])
        self.assertIn("third masculine", clauses["altar"]["analysis"])
        self.assertTrue(all("not a CAL person tag" in clauses[c]["analysis_basis"] for c in ("opening", "delivery")))

    def test_aroma_variant_is_not_hebrew_orthographic_evidence(self):
        control = self.record["aroma_control"]
        self.assertEqual(control["cal_display"], "ܣܘܬܐ/ܢܝܚܐ#2#/")
        self.assertIn("jointly", control["cal_warning"])
        self.assertIn("not established", control["siglum_2_identity"])
        self.assertIn("do not recover", control["conclusion"])
        self.assertTrue(all(value is False for value in self.record["policy"].values()))
        self.assertTrue(all(s["independent_physical_witness_count"] is None for s in self.record["source_observations"]))


if __name__ == "__main__":
    unittest.main()
