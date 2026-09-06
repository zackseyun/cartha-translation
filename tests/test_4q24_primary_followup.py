"""Bounded source provenance checks; passing does not close the DJD/pixel gate."""
import hashlib
import html
import json
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "sources/textual_restoration/discovery/4q24_lev2_primary_followup.v1.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def selected_row(raw, row_id):
    rows = re.findall(r'<tr id="' + re.escape(row_id) + r'"[^>]*>.*?</tr>', raw)
    if len(rows) != 1:
        raise ValueError("missing or duplicate exact target row")
    return rows[0]


class FourQ24PrimaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(RECEIPT.read_text())

    def test_gate_remains_open_even_after_identity_argument_is_read(self):
        g = self.r["gates"]
        self.assertTrue(g["full_reassessment_argument_consulted"])
        self.assertTrue(g["editorial_fragment_number_retention_verified_from_paper"])
        for k in ["djd_target_pages_or_plate_inspected", "target_word_pixels_inspected",
                  "target_words_bound_to_individual_physical_fragment",
                  "physical_identity_independently_adjudicated",
                  "canonical_change_applied", "registry_change_applied"]:
            self.assertFalse(g[k])
        self.assertEqual(g["gate_completion"], "not-complete")
        self.assertEqual(g["new_independent_witness_votes"], 0)

    def test_edition_and_museum_numbers_are_not_collapsed(self):
        i = self.r["iaa_consultation"]["article_referenced_image"]
        self.assertEqual(i["article_fragment"], 1)
        self.assertEqual(i["iaa_fragment"], 2)
        self.assertEqual(i["plate"], 1079)
        self.assertEqual([u["legacy_line"] for u in self.r["selected_units"]], ["29", "31"])

    def test_actual_downloaded_pdf_and_html_hashes(self):
        paths = [(s, Path(os.environ.get("POB_4Q24_" + ("PDF" if s["id"].startswith("tigchelaar") else "HTML"),
                                        s["local_path"]))) for s in self.r["sources"]]
        if any(not p.is_file() for s, p in paths):
            self.skipTest("private PDF or dated HTML unavailable")
        for source, path in paths:
            self.assertEqual(digest(path.read_bytes()), source["sha256"])

    def test_actual_qd_selected_words_and_adjacent_supply(self):
        source = self.r["sources"][1]
        p = Path(os.environ.get("POB_4Q24_HTML", source["local_path"]))
        if not p.is_file():
            self.skipTest("private dated HTML unavailable")
        raw = p.read_bytes()
        self.assertEqual(digest(raw), source["sha256"])
        text = raw.decode()
        for unit in self.r["selected_units"]:
            row = selected_row(text, unit["qd_row_id"])
            words = re.findall(r'<span id="' + unit["qd_word_id"] + r'"[^>]*>(.*?)</span>', row)
            self.assertEqual(words, [unit["qd_word"]])
            plain = html.unescape(re.sub(r"<[^>]+>", "", row))
            self.assertIn(unit["qd_bounded_context"], plain)
            self.assertNotIn("[", unit["qd_word"])
            self.assertNotIn("\u05af", unit["qd_word"])
        # The preceding rows close their supplied spans: selected words do not inherit an open gap.
        for row_id in ["c296705-i296893", "c296705-i296918"]:
            plain = html.unescape(re.sub(r"<[^>]+>", "", selected_row(text, row_id)))
            self.assertTrue(plain.rstrip().endswith("]"))
            self.assertEqual(plain.count("["), plain.count("]"))

    def test_exact_row_lookup_rejects_missing_or_duplicate_ids(self):
        sample = '<tr id="wanted"><td>והביא</td></tr>'
        self.assertEqual(selected_row(sample, "wanted"), sample)
        with self.assertRaises(ValueError):
            selected_row(sample, "absent")
        with self.assertRaises(ValueError):
            selected_row(sample + sample, "wanted")

    def test_actual_qdr_context_hashes_and_selected_reference_tags(self):
        q = self.r["qdr"]
        p = Path(os.environ.get("POB_4Q24_QDR", q["local_path"]))
        if not p.is_file():
            self.skipTest("private pinned QDR unavailable")
        raw = p.read_bytes()
        self.assertEqual(digest(raw), q["sha256"])
        r = json.loads(raw)[q["record_index"]]
        self.assertEqual(r["scroll"], q["label"])
        fs = [f for f in r["fragments"] if f["id"] == q["fragment"]]
        self.assertEqual(len(fs), 1)
        lines = {l["n"]: l for l in fs[0]["lines"]}
        for expected in q["lines"]:
            line = lines[expected["n"]]
            self.assertEqual(digest(json.dumps(line, ensure_ascii=False, sort_keys=True,
                                              separators=(",", ":")).encode()), expected["sha256"])
        for u in self.r["selected_units"]:
            words = [lines[u["legacy_line"]]["words"][i] for i in u["qdr_word_indices"]]
            self.assertEqual("".join(w[0] for w in words), u["qdr_normalized"])
            self.assertEqual({w[5] for w in words}, {"Lev " + u["ref"].split(".", 1)[1].replace(".", ":")})

    def test_actual_pob_files_and_bounded_source_english(self):
        for baseline, unit in zip(self.r["pob_baseline"], self.r["selected_units"]):
            raw = (ROOT / baseline["path"]).read_bytes()
            self.assertEqual(digest(raw), baseline["sha256"])
            self.assertIn(unit["pob_source_selected"], raw.decode())
            self.assertIn(unit["pob_english_selected"], raw.decode())


if __name__ == "__main__":
    unittest.main()
