"""Historical note-only contract; current source successors have separate checks."""
import unittest

from tools.textual_restoration.replay_source_predecessor_tests import CHECKPOINT, replay


class CorpusSuccessorHistoricalTests(unittest.TestCase):
    def test_original_12_checks_in_shared_19_test_archival_replay(self):
        # Both archival wrappers share one cached run, not 19 executions each.
        result = replay()
        self.assertEqual(result["checkpoint"], CHECKPOINT)
        self.assertEqual(result["suite_test_counts"]["corpus_successor"], 12)
        self.assertEqual(result["tests_run"], 19)
        self.assertTrue(result["passed"])
        self.assertEqual((result["skipped"], result["expected_failures"]), (0, 0))
        self.assertFalse(result["current_corpus_validated"])
        self.assertFalse(result["application_approved"])


if __name__ == "__main__":
    unittest.main()
