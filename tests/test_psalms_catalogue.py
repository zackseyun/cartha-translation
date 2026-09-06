"""Bounded regression checks for Psalms discovery metadata, not readings."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.textual_restoration.check_psalms_catalogue import ROOT, label_ordinals, modern_matches, pinned


class PsalmsCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = ROOT / "sources/textual_restoration/discovery"
        cls.targets_raw = (folder / "psalms_catalogue_targets.v1.json").read_bytes()
        cls.targets = json.loads(cls.targets_raw)
        cls.check = json.loads((folder / "psalms_catalogue_check.v1.json").read_bytes())
        cls.by_id = {r["catalogue_id"]: r for r in cls.check["targets"]}

    def test_label_matching_is_exact_and_keeps_duplicate_records(self):
        corpus = [{"scroll": "4Q173"}, {"scroll": "4Q173a"}, {"scroll": "4q173"}, {"scroll": "4Q173"}]
        self.assertEqual(label_ordinals(corpus, ["4Q173"]), [
            {"label": "4Q173", "source_record_ordinal": 0},
            {"label": "4Q173", "source_record_ordinal": 3}])

    def test_modern_match_does_not_filter_literary_class_or_strip_suffix(self):
        rows = [{"display_label": "11Q11", "catalogue_class": "dss"},
                {"display_label": "4Q173a", "catalogue_class": "dss"}]
        self.assertEqual(modern_matches(rows, ["11Q11"]), rows[:1])
        self.assertEqual(modern_matches(rows, ["4Q173"]), [])

    def test_pin_failure_is_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input"
            path.touch()
            with self.assertRaisesRegex(ValueError, "pin mismatch"):
                pinned(path, "0" * 64)

    def test_saved_receipt_targets_hash_and_bookmap_agree(self):
        self.assertEqual(self.check["inputs"]["targets_sha256"], hashlib.sha256(self.targets_raw).hexdigest())
        bookmap = json.loads((ROOT / "sources/textual_restoration/discovery/hebrew_bible_book_map.v1.json").read_bytes())
        ps = next(r for r in bookmap["books"] if r["wlc_book"] == "Ps")
        actual = {(r["matched_labels"][0], r["source_record_ordinals"][0], r["indexed_anchor_count"])
                  for r in self.check["targets"] if r["matched_labels"]}
        expected = {(r["label"], r["source_record_index"], r["indexed_reference_anchors"])
                    for r in ps["source_records"]}
        self.assertEqual(actual, expected)
        self.assertEqual(self.check["summary"]["pinned_index_book_anchors"], 1261)

    def test_cross_file_ordinals_and_overlap_are_not_independent_witnesses(self):
        row = self.by_id["11Q5"]
        self.assertEqual(row["source_record_ordinals"], [233])
        self.assertEqual(row["qdr_nonbiblical_label_check"]["matches"], [{"label": "11Q5", "source_record_ordinal": 668}])
        overlap = [r["catalogue_id"] for r in self.check["targets"]
                   if r["matched_labels"] and r["qdr_nonbiblical_label_check"]["matches"]]
        self.assertEqual(overlap, ["4Q88", "11Q5", "11Q6"])
        self.assertIsNone(self.check["summary"]["independent_manuscript_count"])

    def test_unmatched_suffix_and_historical_names_are_not_forced(self):
        row = self.by_id["4Q173a"]
        self.assertEqual(row["source_record_ordinals"], [])
        self.assertEqual(row["qdr_nonbiblical_label_check"]["matches"], [])
        self.assertEqual(row["modern_catalogue_matches"], [])
        self.assertNotIn("1Q173", self.by_id)
        self.assertNotIn("4Q382", self.by_id)
        self.assertEqual(len(self.targets["historical_provenance_holds"]), 3)
        self.assertTrue(all(not r["accepted_for_reading_support"] for r in self.targets["historical_provenance_holds"]))

    def test_masada_discrepancy_is_retained_not_filled(self):
        self.assertEqual(self.by_id["Mas1e"]["chapter_anchor_counts"], {"81": 16, "82": 8, "83": 19, "84": 13, "85": 6})
        self.assertIn("masada-psalm18", {r["id"] for r in self.targets["source_discrepancies"]})

    def test_no_reading_support_or_transcription_consultation_claim(self):
        self.assertEqual(len(self.check["targets"]), 53)
        for row in self.check["targets"]:
            self.assertEqual(row["reading_support"], "not-assessed")
            self.assertFalse(row["modern_underlying_transcription_consulted"])
            self.assertFalse(row["qdr_nonbiblical_label_check"]["psalm_reference_or_survival_checked"])
        self.assertFalse(self.check["policy"]["canonical_change_applied"])


if __name__ == "__main__":
    unittest.main()
