import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.terminology_policy import (
    normalize_bible_verse_text,
    normalize_reader_payload_in_place,
)


class TerminologyPolicyTests(unittest.TestCase):
    def test_normalizes_singular_plural_and_capitalization(self):
        self.assertEqual(
            normalize_bible_verse_text(
                "his slaves and his slave John; SLAVES, Slaves, SLAVE, Slave"
            ),
            "his servants and his servant John; "
            "SERVANTS, Servants, SERVANT, Servant",
        )

    def test_does_not_rewrite_larger_words(self):
        self.assertEqual(
            normalize_bible_verse_text("enslaved people and slavery"),
            "enslaved people and slavery",
        )

    def test_payload_policy_only_changes_verse_text(self):
        payload = {
            "books": [{
                "chapters": [{
                    "verses": [{
                        "verse": 1,
                        "text": "his slaves and his slave John",
                        "footnotes": [{"text": "Historical note about a slave."}],
                    }],
                }],
            }],
        }
        normalize_reader_payload_in_place(payload)
        verse = payload["books"][0]["chapters"][0]["verses"][0]
        self.assertEqual(verse["text"], "his servants and his servant John")
        self.assertEqual(
            verse["footnotes"][0]["text"],
            "Historical note about a slave.",
        )


if __name__ == "__main__":
    unittest.main()
