"""Bound a rationale-only repair; no test claims to adjudicate textual priority."""
import hashlib
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class LeviticusAgencyTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "sources/textual_restoration/decisions/leviticus_2_8_agency_review.v1.json").read_text())
        self.raw = (ROOT / self.record["pob_path"]).read_bytes()

    def test_only_two_exact_rationale_lines_changed(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.record["after_file_sha256"])
        reconstructed = self.raw.decode()
        self.assertEqual(len(self.record["exact_line_replacements"]), 2)
        for change in self.record["exact_line_replacements"]:
            self.assertEqual(reconstructed.splitlines().count(change["after"]), 1)
            reconstructed = reconstructed.replace(change["after"] + "\n", change["before"] + "\n")
        self.assertEqual(hashlib.sha256(reconstructed.encode()).hexdigest(), self.record["before_file_sha256"])

    def test_source_english_notes_and_old_review_are_unchanged(self):
        verse = yaml.safe_load(self.raw)
        for key, digest in self.record["unchanged_component_sha256"].items():
            raw = json.dumps(verse[key], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
        self.assertEqual(verse["cross_check"]["status"], "needs_review")

    def test_hebrew_morphology_control_is_bound_and_locally_present(self):
        source = next(s for s in self.record["sources"] if s["id"] == "uwhb-control")
        raw = (ROOT / source["path"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), source["sha256"])
        chapter = raw.decode().split('\\c 2\n')[1].split('\\c 3\n')[0]
        verse = chapter.split('\\v 8\n')[1].split('\\v 9\n')[0]
        words = re.findall(r'\\w ([^|]+)\|([^\n]+?)\\w\*', verse)
        for expected in self.record["hebrew_verbal_sequence"]:
            hits = [attrs for surface, attrs in words if ''.join(re.findall('[א-ת]', surface)) == expected["form"]]
            self.assertEqual(len(hits), 1)
            self.assertIn('x-morph="' + expected["uwhb_morph"] + '"', hits[0])

    def test_repointing_is_not_promoted_as_english_only(self):
        candidate = next(c for c in self.record["candidates"] if c["id"] == "imperative-repointing")
        self.assertEqual(candidate["status"], "unpromoted")
        self.assertIn("Pointing", candidate["source_effect"])
        self.assertTrue(all(v is False for v in self.record["policy"].values()))

    def test_greek_control_keeps_cross_verse_clause(self):
        control = self.record["greek_clause_controls"]
        self.assertEqual(control["approach_participle"], "προσεγγίσας")
        self.assertEqual(control["next_verse_subject_clause"], "ἀφελεῖ ὁ ἱερεὺς")
        self.assertIn("verse boundary", control["interpretation"])


if __name__ == "__main__":
    unittest.main()
