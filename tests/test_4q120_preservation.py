import hashlib
import json
from pathlib import Path
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "sources/textual_restoration/discovery/4q120_lev2_preservation_review.v1.json"


def normalize(value):
    return "".join(c for c in unicodedata.normalize("NFD", value)
                   if unicodedata.category(c) != "Mn").replace("ϲ", "σ")


class GreekLeviticusPreservationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(RECORD.read_text())

    def test_printed_partial_word_keeps_supply_and_uncertainty(self):
        word = self.data["published_boundary"]
        self.assertEqual(word["terminal_word_as_printed"],
                         word["unbracketed_prefix_as_printed"] + "[" + word["supplied_completion_as_printed"])
        self.assertEqual(word["underdotted_letters"], ["π", "ρ"])
        self.assertFalse(word["person_ending_independently_preserved"])
        self.assertIn("(?)", word["printed_reference"])

    def test_reported_prefix_does_not_discriminate_example_endings(self):
        prefix = normalize(self.data["published_boundary"]["unbracketed_prefix_as_printed"])
        examples = self.data["discrimination_check"]
        self.assertEqual(prefix, "προσ")
        self.assertEqual(len(set(examples["illustrative_forms"])), 2)
        self.assertTrue(all(normalize(form).startswith(prefix) for form in examples["illustrative_forms"]))
        self.assertIn("not-two-attested", examples["forms_status"])
        self.assertEqual(examples["hebrew_retroversion_status"], "not-established")

    def test_image_route_is_not_claimed_as_passage_or_letter_verification(self):
        image = self.data["image_route"]
        self.assertFalse(image["pixels_inspected"])
        self.assertIn("unverified", image["passage_mapping"])
        self.assertIsNone(self.data["published_boundary"]["fragment_and_line_in_primary_edition"])
        self.assertTrue(all(value is False for value in self.data["policy"].values()))

    def test_current_pob_control_is_unchanged(self):
        control = self.data["pob_control"]
        self.assertEqual(hashlib.sha256((ROOT / control["path"]).read_bytes()).hexdigest(), control["sha256"])

    def test_registered_object_is_greek_not_another_hebrew_vote(self):
        registry = json.loads((ROOT / "sources/textual_restoration/ot_witness_registry.v1.json").read_text())
        witness = next(w for w in registry["witnesses"] if w["id"] == self.data["witness_id"])
        self.assertEqual(witness["languages"], ["Greek"])
        self.assertEqual(witness["witness_class"], "ancient-daughter-version")
        self.assertEqual(witness["coverage_status"], "unmapped")
        self.assertIn("inconclusive", witness["textual_role"])


if __name__ == "__main__":
    unittest.main()
