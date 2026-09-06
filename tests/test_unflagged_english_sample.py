"""Separate frozen experiment replay from current normalization behavior."""
import unittest

from tools.textual_restoration import build_unflagged_english_sample as sample
from tools.textual_restoration.replay_historical_tests import run_suite


class UnflaggedEnglishSampleTests(unittest.TestCase):
    def test_original_four_experiment_checks_in_immutable_snapshot(self):
        result = run_suite("unflagged")
        self.assertTrue(result["passed"])
        self.assertEqual(result["tests_run"], 4)
        self.assertFalse(result["current_corpus_validated"])
        self.assertFalse(result["application_approved"])

    def test_current_pointed_spelling_not_silently_repointed(self):
        self.assertNotEqual(sample.normalized("שָׁב"), sample.normalized("שֵׁב"))
        self.assertNotEqual(sample.normalized("שׁ"), sample.normalized("שׂ"))
        self.assertEqual(sample.normalized("בְּ/רֵאשִׁ֖ית׃"), sample.normalized("בְּרֵאשִׁית"))


if __name__ == "__main__":
    unittest.main()
