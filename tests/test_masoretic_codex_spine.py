"""Navigation/encoding integrity, not validation of ancient readings."""
import copy
import json
import unittest
from tools.textual_restoration import build_masoretic_codex_spine as m


class MasoreticSpineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads(m.SOURCES.read_text())
        cls.result = m.build()
        cls.rows = {r["book"]: r for r in cls.result["books"]}

    def test_actual_inputs_reproduce_frozen_receipt(self):
        self.assertEqual(self.result, json.loads(m.OUTPUT.read_text()))

    def test_divisions_are_not_extra_codices(self):
        self.assertEqual(len(self.rows), 39)
        self.assertEqual(len({r["tanakh_navigation_group"] for r in self.rows.values()}), 24)
        self.assertEqual(m.group("1_chronicles"), m.group("2_chronicles"))
        self.assertEqual(m.group("ezra"), m.group("nehemiah"))
        self.assertEqual(len({m.group(b) for b in m.TWELVE}), 1)
        self.assertEqual(self.result["summary"]["named_physical_codex_targets"], 3)
        self.assertFalse(self.result["summary"]["physical_independence_adjudicated"])

    def test_zero_qdr_does_not_remove_masoretic_controls(self):
        for book in ("1_chronicles", "nehemiah", "esther"):
            self.assertEqual(self.rows[book]["qdr_reference_anchors"], 0)
            self.assertIn("leningrad", self.rows[book])
            self.assertFalse(self.rows[book]["sassoon"]["aggregate_percentage_applied_to_book"])

    def test_missing_parchment_does_not_erase_surrogate_evidence(self):
        for book, kind in (("genesis", "pre-loss-photograph-reported"),
                           ("exodus", "recovered-parchment-fragment-reported")):
            row = self.rows[book]["aleppo"]
            self.assertEqual(row["body_status"], "main-body-missing-in-cited-list")
            self.assertEqual(row["special_evidence"][0]["kind"], kind)
            self.assertFalse(row["special_evidence"][0]["freshly_inspected"])

    def test_codex_order_not_assumed_to_be_pob_order(self):
        self.assertEqual(self.rows["nehemiah"]["aleppo"]["body_status"], "main-body-missing-in-cited-list")
        self.assertEqual(self.rows["1_chronicles"]["aleppo"]["body_status"], "not-listed-as-missing-completeness-unverified")
        self.assertEqual(self.rows["2_chronicles"]["aleppo"]["special_evidence"][0]["kind"], "recovered-parchment-leaf-reported")

    def test_extent_never_certifies_complete_ink(self):
        for row in self.rows.values():
            self.assertFalse(row["aleppo"]["direct_reading_collated"])
            self.assertFalse(row["leningrad"]["verse_and_layer_collation_complete"])
            self.assertFalse(row["sassoon"]["verse_and_hand_collation_complete"])

    def test_unknown_overlap_and_promotion_rejected(self):
        for mutate in (lambda d: d["aleppo"]["main_body_absent_books"].append("unknown"),
                       lambda d: d["aleppo"]["main_body_absent_books"].append("psalms"),
                       lambda d: d["policy"].update(canonical_change_applied=True)):
            data = copy.deepcopy(self.sources)
            mutate(data)
            with self.assertRaises(ValueError):
                m.validate_sources(data, list(self.rows))

    def test_probes_distinguish_control_and_supplied_mark_lead(self):
        probes = {p["osis_id"]: p for p in self.result["digital_vs_manuscript_probes"]}
        self.assertEqual(probes["Num.7.13"]["probe_role"], "first-offering-vocalized-control")
        self.assertEqual(probes["Num.7.19"]["probe_role"], "repeated-offering-supplied-vowels-lead")
        self.assertEqual(probes["Josh.21.36"]["wlc_word_element_count"], 10)
        self.assertEqual(probes["Josh.21.37"]["wlc_word_element_count"], 10)
        self.assertEqual(probes["Num.7.19"]["wlc_vowel_codepoint_count"], 59)
        self.assertEqual(m.vowel_count("בְּרֵאשִׁ֖ית"), 3)


if __name__ == "__main__":
    unittest.main()
