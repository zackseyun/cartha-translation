"""Integrity/reproduction checks, not tests of translation truth."""
import importlib.util
import json
from pathlib import Path
import unittest

from tools.textual_restoration import apply_numbers_22_19_note as note_package

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("unflagged", ROOT / "tools/textual_restoration/build_unflagged_english_sample.py")
sample = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sample)
RECEIPTS = ROOT / "sources/textual_restoration/samples"


class UnflaggedEnglishSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selection = json.loads((RECEIPTS / "unflagged_english_sample.selection.v1.json").read_text())
        cls.review = json.loads((RECEIPTS / "unflagged_english_sample.review.v1.json").read_text())

    def test_frozen_selection_reproduces_with_guarded_historical_baseline(self):
        # The selector and original receipts stay frozen. The overlay accepts
        # only the exact baseline, or this package's approved candidate with
        # bound transaction provenance; all unrelated/unknown drift still fails.
        result = note_package.historical_sample_probe()
        self.assertTrue(result["historical_selection_reproduced"])
        self.assertEqual(result["historical_corpus_digest"], self.selection["corpus_digest"])
        self.assertEqual(result["context_files_verified"], 101)
        self.assertEqual(result["overlay_paths"], ["translation/ot/numbers/022/019.yaml"])

    def test_pointed_spelling_not_silently_repointed(self):
        self.assertNotEqual(sample.normalized("שָׁב"), sample.normalized("שֵׁב"))
        self.assertNotEqual(sample.normalized("שׁ"), sample.normalized("שׂ"))
        self.assertEqual(sample.normalized("בְּ/רֵאשִׁ֖ית׃"), sample.normalized("בְּרֵאשִׁית"))

    def test_review_binds_source_and_context(self):
        receipt = RECEIPTS / "unflagged_english_sample.selection.v1.json"
        self.assertEqual(sample.sha(receipt.read_bytes()), self.review["selection_receipt_sha256"])
        for row in self.review["records"]:
            winner = self.selection["strata"][row["stratum"]]["selected"]
            self.assertEqual(row["id"], winner["id"])
            self.assertEqual(row["yaml_sha256"], winner["yaml_sha256"])
            for path, digest in row["context_files"].items():
                self.assertEqual(sample.sha(note_package.historical_bytes(ROOT / path)), digest, path)

    def test_bounded_judgments_and_no_promotion(self):
        self.assertFalse(self.review["canonical_promotion_approved"])
        self.assertFalse(self.review["independent_second_review"])
        self.assertFalse(self.review["blind_candidate_comparison"])
        self.assertEqual(len(self.review["records"]), 3)
        counts = {kind: sum(row["outcome"] == kind for row in self.review["records"])
                  for kind in ("retain", "change", "unresolved")}
        for kind, count in counts.items():
            self.assertEqual(count, self.review["summary"][kind])
        for row in self.review["records"]:
            self.assertTrue(row["strongest_counterargument"])
            self.assertTrue(row["reopen_when"])
            self.assertTrue(row["source_choice"])
            self.assertEqual(set(row["rubric"]), {"meaning", "omissions_additions", "ambiguity", "literary_function", "naturalness", "consistency"})


if __name__ == "__main__":
    unittest.main()
