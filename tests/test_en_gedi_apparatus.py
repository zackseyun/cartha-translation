"""Record/alignment checks, not new manuscript readings or textual adjudication."""
import hashlib
import json
from pathlib import Path
import unittest

import yaml

from tools.textual_restoration.build_en_gedi_apparatus_check import locate, tokens

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "sources/textual_restoration/discovery"


class EnGediApparatusTests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((DIR / "en_gedi_apparatus_check.v1.json").read_text())

    def test_all_twelve_listed_units_not_whole_column_coverage(self):
        self.assertEqual(self.receipt["summary"], {
            "apparatus_units": 12, "pob_verses": 10,
            "categories": {"orthographic": 4, "linguistic": 5, "content": 3},
            "unbracketed_editorial_units": 10, "partly_supplied_editorial_units": 2,
            "sp_context_differences": 10})
        self.assertEqual(len({u["id"] for u in self.receipt["checks"]}), 12)
        self.assertTrue(all(value is False for value in self.receipt["policy"].values()))

    def test_unit_specification_and_current_pob_are_hash_bound(self):
        spec = (DIR / "en_gedi_apparatus_units.v1.json").read_bytes()
        self.assertEqual(self.receipt["units_sha256"], hashlib.sha256(spec).hexdigest())
        for unit in self.receipt["checks"]:
            raw = (ROOT / unit["pob_path"]).read_bytes()
            self.assertEqual(unit["pob_sha256"], hashlib.sha256(raw).hexdigest())
            pob = yaml.safe_load(raw)
            self.assertEqual(locate(tokens(pob["source"]["text"]), unit["pob_context"]), unit["pob_source_context_span"])
            self.assertIn(unit["english_excerpt"], pob["translation"]["text"])
            self.assertEqual(unit["english_effect"], "no-source-driven-change-selected")

    def test_supplied_prefixes_do_not_become_visible_whole_words(self):
        partial = {u["id"]: u for u in self.receipt["checks"] if u["supplied_prefix"]}
        self.assertEqual(set(partial), {"EG-CONT-01", "EG-CONT-03"})
        self.assertEqual(partial["EG-CONT-01"]["published_unbracketed_remainder"], "ט")
        self.assertEqual(partial["EG-CONT-03"]["published_unbracketed_remainder"], "הבאת")
        for unit in partial.values():
            self.assertEqual(unit["preservation_class"], "partly-supplied-editorial-unit")
            self.assertEqual(unit["supplied_prefix"] + unit["published_unbracketed_remainder"], unit["editorial_form"])

    def test_context_alignment_does_not_match_substrings_or_ambiguous_occurrences(self):
        self.assertEqual(locate(tokens("את הנתחים ואת הראש"), "ואת הראש"),
                         {"start_word_zero_based": 2, "word_count": 2})
        for context, phrase in (("ואת הראש", "את הראש"), ("את את", "את"), ("את הכל", "")):
            with self.assertRaises(ValueError):
                locate(tokens(context), phrase)

    def test_normalization_retains_matres_and_splits_maqqef_not_morphology(self):
        self.assertEqual(tokens("וְ/הֵבֵאתָ֣ אֶת־הַ/מִּנְחָ֗ה"), ["והבאת", "את", "המנחה"])
        self.assertNotEqual(tokens("ניחח"), tokens("ניחוח"))

    def test_qdr_uses_actual_tags_and_does_not_add_an_independent_witness(self):
        controls = self.receipt["qdr_controls"]
        self.assertEqual([c["qdr_reference_tag"] for c in controls], ["Lev 2:8", "Lev 2:9"])
        self.assertEqual([c["line"] for c in controls], ["29", "31"])
        self.assertTrue(all(c["manuscript_id"] == "4Q24" for c in controls))
        self.assertFalse(self.receipt["policy"]["qdr_is_an_independent_manuscript"])


if __name__ == "__main__":
    unittest.main()
