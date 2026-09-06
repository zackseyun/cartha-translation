"""Original Samuel transaction tests run at their immutable checkpoint."""
import unittest

from tools.textual_restoration.verify_corpus_successor import historical_samuel_tests


class SamuelHistoricalTransactionTests(unittest.TestCase):
    def test_original_eleven_tests(self):
        result = historical_samuel_tests()
        self.assertTrue(result["passed"])
        self.assertEqual(result["tests_run"], 11)
        self.assertFalse(result["current_corpus_validated"])


if __name__ == "__main__":
    unittest.main()
