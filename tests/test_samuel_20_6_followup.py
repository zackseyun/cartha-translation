"""Integrity regressions; these do not decide Hebrew meaning or textual priority."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "samuel_followup", ROOT / "tools/textual_restoration/check_samuel_20_6_followup.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class SamuelFollowupTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / CHECK.RECORD).read_bytes())

    def test_current_bindings(self):
        result = CHECK.validate(self.record)
        self.assertEqual(result["context_files_checked"], 26)
        self.assertEqual(result["frozen_inputs_checked"], 10)
        self.assertFalse(result["scholarly_truth_certified"])

    def test_every_frozen_input_drift_rejected(self):
        for target in self.record["frozen_inputs"]:
            with self.subTest(target=target):
                def read(rel):
                    raw = (ROOT / rel).read_bytes()
                    return raw + b"\nchanged" if rel == target else raw
                with self.assertRaises(ValueError):
                    CHECK.validate(self.record, read=read)

    def test_every_context_drift_rejected(self):
        for target in self.record["baseline"]["context_files"]:
            with self.subTest(target=target):
                def read(rel):
                    raw = (ROOT / rel).read_bytes()
                    return raw + b"\nchanged" if rel == target else raw
                with self.assertRaisesRegex(ValueError, "Canonical context drift"):
                    CHECK.validate(self.record, read=read)

    def test_context_membership_cannot_shrink(self):
        self.record["baseline"]["context_files"].pop(CHECK.TARGET)
        with self.assertRaisesRegex(ValueError, "Context set"):
            CHECK.validate(self.record)

    def test_pointing_cannot_be_normalized_away(self):
        self.record["baseline"]["source"]["text"] = self.record["baseline"]["source"]["text"].replace("מָ֥צָא", "יִמְצָא")
        with self.assertRaisesRegex(ValueError, "Pointed source"):
            CHECK.validate(self.record)

    def test_no_unrecorded_scope_promotion(self):
        for key, value in (("publication_approved", True), ("application_approved", True),
                           ("source_changes", ["emendation"]), ("whole_verse_outcome", "approved")):
            record = copy.deepcopy(self.record)
            record[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                CHECK.validate(record)

    def test_evidence_reference_must_resolve(self):
        self.record["findings"][0]["source_ids"].append("unconsulted-HALOT")
        with self.assertRaisesRegex(ValueError, "Unknown evidence"):
            CHECK.validate(self.record)

    def test_version_not_exact_retroversion(self):
        for source_id in ("greek-rh2006", "syriac-cal62009"):
            record = copy.deepcopy(self.record)
            next(s for s in record["sources"] if s["id"] == source_id)["retroversion_status"] = "attested-Hebrew"
            with self.subTest(source_id=source_id), self.assertRaisesRegex(ValueError, "Retroversion"):
                CHECK.validate(record)

    def test_quoted_distinctions_are_preserved(self):
        sources = {s["id"]: s for s in self.record["sources"]}
        self.assertIn("σκιάσει", sources["greek-rh2006"]["excerpt"])
        self.assertNotIn("σκιάσῃ", sources["greek-rh2006"]["excerpt"])
        self.assertIn("ונקום בהין ונחטט", sources["syriac-cal62009"]["excerpt"])
        self.assertEqual(sources["syriac-cal62009"]["attested_addressee"], "ליואב٠")
        self.assertIn("אֲבִישַׁ֔י", self.record["baseline"]["source"]["text"])

    def test_cannot_claim_blinded_case(self):
        self.record["evaluation_contract"]["blinded"] = True
        with self.assertRaisesRegex(ValueError, "independence"):
            CHECK.validate(self.record)


if __name__ == "__main__":
    unittest.main()
