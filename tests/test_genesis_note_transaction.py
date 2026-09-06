"""Historical Genesis transaction contract, not current-corpus approval."""
import unittest

from tools.textual_restoration.replay_historical_tests import run_suite


class GenesisHistoricalTransactionTests(unittest.TestCase):
    def test_original_28_transaction_checks_in_immutable_snapshot(self):
        result = run_suite("genesis")
        self.assertTrue(result["passed"])
        self.assertEqual(result["tests_run"], 28)
        self.assertFalse(result["current_corpus_validated"])
        self.assertFalse(result["application_approved"])


if __name__ == "__main__":
    unittest.main()
