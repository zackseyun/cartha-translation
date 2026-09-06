"""Reproduce the bounded 4Q119 Lev26:12 comparison, not paleography.

Private local inputs can be relocated through the named environment variables.
A skipped private-input check is not reported as a source-verified pass.
"""
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "sources/textual_restoration/discovery/4q119_lev26_12_review.v1.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class GreekLeviticusReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RECEIPT.read_text())

    def test_supplied_ending_never_becomes_preserved_text(self):
        r = self.data["readings"]["wevers_collation"]
        self.assertEqual(r["printed_excerpt"], "μοι εθν[ος")
        self.assertEqual(r["preserved_as_reported"], "μοι εθν")
        self.assertEqual(r["supplied_as_reported"], "ος")
        self.assertEqual(r["printed_excerpt"].split("["),
                         [r["preserved_as_reported"], r["supplied_as_reported"]])
        self.assertEqual(r["normalized_editorial_completion"],
                         r["preserved_as_reported"] + r["supplied_as_reported"])
        self.assertEqual(self.data["readings"]["himbaza_table"]["printed"],
                         r["normalized_editorial_completion"])
        self.assertFalse(self.data["readings"]["himbaza_table"]["brackets_printed"])

    def test_retention_does_not_promote_greek_or_physical_claim(self):
        self.assertEqual(self.data["status"], "retain-pob-hebrew-and-english-at-selected-locus")
        for field in ["whole_verse_preservation_claimed", "manuscript_pixels_consulted",
                      "djd_ix_consulted", "canonical_change_applied", "registry_or_case_promotion_applied"]:
            self.assertFalse(self.data["scope"][field])
        self.assertTrue(self.data["assessment"]["earliest_greek_priority"].startswith("unresolved"))
        self.assertEqual(self.data["assessment"]["independent_witness_votes_added"], 0)
        self.assertFalse(self.data["readings"]["rahlfs_control"]["ai_annotations_used"])

    def test_both_pronoun_and_noun_difference_retained(self):
        self.assertEqual(self.data["readings"]["rahlfs_control"]["selected_reading"], "μου λαός")
        self.assertEqual(self.data["readings"]["wevers_collation"]["preserved_as_reported"], "μοι εθν")
        self.assertEqual(self.data["pob_baseline"][1]["selected_english"], "you will be my people.")

    def test_pdf_locators_are_explicit_and_resolve_to_sources(self):
        sources = {s["id"]: s for s in self.data["sources"]}
        self.assertEqual(len(sources), 2)
        for field in ["himbaza_table", "wevers_collation"]:
            self.assertIn(self.data["readings"][field]["source_id"], sources)
        self.assertEqual(sources["himbaza2020"]["visually_consulted_pdf_pages_1based"], [123,124,126,128])
        self.assertEqual(sources["wevers2005"]["visually_consulted_pdf_pages_1based"], [4,5,6])
        self.assertIn("relative line2", self.data["readings"]["wevers_collation"]["manuscript_line_locator"])

    def test_actual_private_pdf_pins(self):
        paths = [(s, Path(os.environ.get("POB_LEV26_" + s["id"].upper(), s["local_path"])))
                 for s in self.data["sources"]]
        if any(not p.is_file() for _, p in paths):
            self.skipTest("one or more private scholarly PDF snapshots unavailable")
        for source, path in paths:
            with self.subTest(source=source["id"]):
                self.assertEqual(digest(path.read_bytes()), source["sha256"])

    def test_actual_pinned_greek_surfaces(self):
        r = self.data["readings"]["rahlfs_control"]
        path = Path(os.environ.get("POB_LEV26_GREEK", r["local_path"]))
        if not path.is_file():
            self.skipTest("private pinned Greek JSON unavailable")
        raw = path.read_bytes()
        self.assertEqual(digest(raw), r["sha256"])
        records = json.loads(raw)
        for control in r["context_surfaces"]:
            rows = [x for x in records if x["ref"] == control["ref"]]
            self.assertEqual(len(rows), 1)
            text = " ".join(w["surface"] for w in rows[0]["words"])
            self.assertEqual(text, control["text"])
            self.assertEqual(digest(text.encode()), control["sha256"])
        self.assertTrue(r["context_surfaces"][1]["text"].endswith(r["selected_reading"]))

    def test_actual_pob_context_baselines(self):
        for row in self.data["pob_baseline"]:
            with self.subTest(ref=row["ref"]):
                raw = (ROOT / row["path"]).read_bytes()
                self.assertEqual(digest(raw), row["sha256"])
                if row["ref"] == "LEV.26.12":
                    self.assertIn(row["selected_hebrew"], raw.decode())
                    self.assertIn(row["selected_english"], raw.decode())


if __name__ == "__main__":
    unittest.main()
