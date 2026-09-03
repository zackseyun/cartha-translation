from collections import Counter
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "sources/textual_restoration/decisions/english_impact_check.v1.json"


class TranslationImpactTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DATA.read_text())

    def test_selected_sample_totals(self):
        self.assertEqual(len(self.data["records"]), 10)
        self.assertEqual(dict(Counter(x["status"] for x in self.data["records"])), self.data["counts"])
        self.assertEqual(self.data["counts"]["provisional-main-text-change"], 3)

    def test_drafts_change_only_the_selected_phrase(self):
        for record in self.data["records"]:
            if record["status"] == "provisional-main-text-change":
                self.assertEqual(record["current_english"].count(record["changed_from"]), 1)
                self.assertEqual(record["current_english"].replace(record["changed_from"], record["changed_to"]), record["draft_english"])
                self.assertTrue((ROOT / record["decision_path"]).is_file())

    def test_no_applied_or_publication_ready_changes(self):
        self.assertEqual(self.data["canonical_changes_applied"], 0)
        for record in self.data["records"]:
            self.assertFalse(record["applied"])
            self.assertFalse(record["publication_ready"])
            self.assertRegex(record["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue((ROOT / record["source_path"]).is_file())

    def test_unresolved_psalm_does_not_pretend_to_be_final_wording(self):
        record = next(x for x in self.data["records"] if x["id"] == "PSA.145.13.nun")
        self.assertIsNone(record["draft_english"])
        self.assertTrue(record["not_final_wording_reason"])

    def test_nonadjudicated_controls_have_no_draft_replacement(self):
        for record in self.data["records"]:
            if record["status"] in ("not-yet-adjudicated", "already-represents-supported-edition-reading"):
                self.assertIsNone(record["draft_english"])


if __name__ == "__main__":
    unittest.main()
