"""Integrity gates for a bounded catalogue pass, not historical truth tests."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class JudeanGreekCatalogueTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "sources/textual_restoration/discovery/judean_greek_catalogue_followup.v1.json").read_text())
        registry = json.loads((ROOT / "sources/textual_restoration/ot_witness_registry.v1.json").read_text())
        self.registry = {w["id"]: w for w in registry["witnesses"]}
        self.units = {u["id"]: u for u in self.data["units"]}

    def test_units_are_unique_and_new_entries_resolve_without_promotion(self):
        self.assertEqual(len(self.units), len(self.data["units"]))
        self.assertEqual(len(self.units), 7)
        added = [u for u in self.units.values() if u["registry_action"] == "new"]
        self.assertEqual({u["id"] for u in added}, {"4Q119", "4Q121", "4Q122", "7Q1"})
        for unit in self.units.values():
            self.assertFalse(unit["reading_support_established_this_pass"])
            if unit["registry_id"] is not None:
                entry = self.registry[unit["registry_id"]]
                self.assertEqual(entry["languages"], ["Greek"])
                self.assertEqual(entry["witness_class"], "ancient-daughter-version")
        for unit in added:
            entry = self.registry[unit["registry_id"]]
            self.assertEqual(entry["source_state"], "registered")
            self.assertEqual(entry["coverage_status"], "unmapped")
            self.assertIn(unit["catalogue_url"], [a["url"] for a in entry["access"]])

    def test_aliases_have_explicit_consulted_survey_basis(self):
        expected = {"4Q119": "801", "4Q120": "802", "4Q121": "803", "4Q122": "819", "7Q1": "805", "7Q2": "804"}
        for name, alias in expected.items():
            self.assertEqual(self.units[name]["rahlfs"], alias)
            self.assertIn("kraft-early-greek", self.units[name]["rahlfs_basis"])
        for source in self.data["sources"]:
            self.assertTrue(source["url"].startswith("https://"))

    def test_partial_image_lists_and_shared_plate_are_not_collations(self):
        expected = {"4Q119": (9, 9), "4Q121": (48, 12), "4Q122": (13, 12), "7Q1": (4, 4), "7Q2": (2, 2)}
        for name, counts in expected.items():
            unit = self.units[name]
            self.assertEqual((unit["image_results_total"], unit["image_results_seen"]), counts)
            self.assertLessEqual(unit["image_results_seen"], unit["image_results_total"])
            self.assertEqual(len(unit["target_image_candidates"]), 2)
        self.assertIn("not automatically DJD", self.units["4Q122"]["candidate_locator"])
        self.assertFalse(self.data["policy"]["image_listing_is_pixel_consultation"])

    def test_minor_prophets_physical_identity_is_not_forced(self):
        unit = self.units["8HevXIIgr"]
        self.assertIsNone(unit["original_scroll_count"])
        self.assertEqual(unit["scroll_count_hypotheses"], [1, 2])
        self.assertEqual(unit["hands"], ["A", "B"])
        self.assertFalse(unit["catalogue_unit_is_physical_object_count"])
        entry = self.registry[unit["registry_id"]]
        self.assertIn("catalogue umbrella", entry["label"])
        self.assertIn("one-or-two-scroll", entry["next_action"])

    def test_adjacent_and_unidentified_material_cannot_vote(self):
        self.assertIsNone(self.units["7Q2"]["registry_id"])
        self.assertIn("not the canonical Jeremiah", self.units["7Q2"]["passage_lead"])
        self.assertTrue(all(r["direct_continuous_bible_support"] is False for r in self.data["related_leads"]))
        self.assertFalse(self.data["policy"]["canonical_change_applied"])
        self.assertFalse(self.data["policy"]["automatic_retroversion"])
        self.assertEqual(self.data["policy"]["new_physical_coverage_records"], 0)


if __name__ == "__main__":
    unittest.main()
