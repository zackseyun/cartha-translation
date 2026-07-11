import pathlib
import re
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PublicDomainBridgeCorpusTests(unittest.TestCase):
    def test_philip_and_mary_records_are_complete_and_reviewed(self):
        for slug, expected in (("gospel_of_philip", 18), ("gospel_of_mary", 5)):
            files = sorted(
                (ROOT / "translation" / "extra_canonical" / slug).glob("*.yaml")
            )
            self.assertEqual(len(files), expected)
            for path in files:
                record = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertEqual(record["status"], "provisional_source_bridge")
                self.assertEqual(record["source_language_review"], "pending")
                self.assertTrue(record["source"]["english_witness"].strip())
                self.assertTrue(record["translation"]["text"].strip())
                self.assertIn(
                    record["grounding_review"]["verdict"], {"accept", "revise"}
                )

    def test_philip_folio_markers_do_not_leak_into_rendering(self):
        folio_number = re.compile(r"(?<!\w)(?:5[1-9]|6[0-9]|7[0-9]|8[0-6])(?!\w)")
        for path in sorted(
            (ROOT / "translation" / "extra_canonical" / "gospel_of_philip").glob(
                "*.yaml"
            )
        ):
            record = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertIsNone(
                folio_number.search(record["translation"]["text"]), path.name
            )


if __name__ == "__main__":
    unittest.main()
