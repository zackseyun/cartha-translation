import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "samaritan_screen", ROOT / "tools/textual_restoration/build_samaritan_screen.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class SamaritanScreenTests(unittest.TestCase):
    def test_presentation_forms_are_decomposed_before_pointing_removed(self):
        self.assertEqual(M.consonants("שָׁלוֹם / שלום"), "שלוםשלום")

    def test_matres_and_final_forms_are_not_harmonized(self):
        self.assertNotEqual(M.consonants("קטרת"), M.consonants("קטורת"))
        self.assertNotEqual(M.consonants("מלך"), M.consonants("מלכ"))

    def test_qere_and_paragraph_signs_do_not_enter_written_text(self):
        verse = ET.fromstring(f'<verse xmlns="{M.NS["o"]}"><w>לא</w><note><w>לו</w></note><seg type="x-pe">פ</seg></verse>')
        self.assertEqual(M.written_wlc(verse), "לא")

    def test_duplicate_and_empty_verses_fail(self):
        data = {}
        M.add_unique(data, "Gen.1.1", "אב")
        with self.assertRaises(ValueError):
            M.add_unique(data, "Gen.1.1", "גד")
        with self.assertRaises(ValueError):
            M.add_unique(data, "Gen.1.2", "---")

    def test_only_encoded_paragraph_signs_are_accepted(self):
        verse = ET.fromstring(f'<verse xmlns="{M.NS["o"]}"><w>לא</w><note><w>לו</w></note><seg type="x-pe">פ</seg></verse>')
        self.assertEqual(M.canonical_wlc_keys(verse), {"לא", "לאפ"})
        plain = ET.fromstring(f'<verse xmlns="{M.NS["o"]}"><w>לא</w></verse>')
        self.assertEqual(M.canonical_wlc_keys(plain), {"לא"})

    def test_anchor_segmentation_is_lossless(self):
        text = "אב גד הו  "
        spans = M.split_by_anchors(text, [("a", "אב"), ("b", "גד"), ("c", "הו")])
        self.assertEqual("".join(s["text"] for s in spans), text)
        self.assertEqual([(s["start"], s["end"]) for s in spans], [(0, 3), (3, 6), (6, 10)])

    def test_invalid_anchor_maps_fail(self):
        for text, anchors in [("אב אב", [("a", "אב")]),
                              ("אב גד", [("a", "הו")]),
                              ("אב גד", [("a", "גד"), ("b", "אב")]),
                              ("אב גד", [("a", "גד")])]:
            with self.assertRaises(ValueError):
                M.split_by_anchors(text, anchors)

    def test_saved_incense_alignment_covers_one_whole_node(self):
        data = json.loads(M.INCENSE_OUT.read_text())
        spans = data["segments"]
        self.assertEqual(len(spans), 11)
        self.assertEqual([s["wlc_reference"] for s in spans], [r for r, _ in M.INCENSE_ANCHORS])
        self.assertEqual({s["sp_reference"] for s in spans}, {"Exod.26.35"})
        self.assertEqual(spans[0]["sp_character_span"][0], 0)
        self.assertEqual(spans[-1]["sp_character_span"][1], data["source"]["sp_character_count"])
        for left, right in zip(spans, spans[1:]):
            self.assertEqual(left["sp_character_span"][1], right["sp_character_span"][0])
        placement = next(s for s in spans if s["wlc_reference"] == "Exod.30.6")
        self.assertEqual(placement["sp_character_span"], [392, 447])
        self.assertLess(placement["sp_consonant_count"], placement["wlc_consonant_count"])
        self.assertTrue(all(value is False for value in data["policy"].values()))

    def test_exodus_note_targets_cover_not_ark(self):
        import yaml
        verse = yaml.safe_load((ROOT / "translation/ot/exodus/030/006.yaml").read_text())
        text = verse["translation"]["text"]
        notes = {n["marker"]: n for n in verse["translation"]["footnotes"]}
        self.assertIn("ark of the testimony[a]", text)
        self.assertIn("mercy seat[b]", text)
        self.assertIn("atonement cover", notes["b"]["text"])
        self.assertNotIn("atonement cover", notes["a"]["text"])
        self.assertEqual(notes["c"]["reason"], "textual_variant")
        self.assertIn("retains the Masoretic", notes["c"]["text"])

    def test_matching_does_not_auto_realign_repeated_text(self):
        data = M.screen({"Gen.1.1": "אב"}, {"Gen.1.1": "גד", "Gen.1.2": "אב", "Gen.1.3": "אב"})
        lead = data["numbering_or_repetition_review"][0]
        self.assertEqual(lead["other_exact_wlc_reference_candidates"], ["Gen.1.2", "Gen.1.3"])
        self.assertEqual(data["summary"]["consonantal_different"], 1)

    def test_unmatched_labels_are_accounted_for(self):
        data = M.screen({"Gen.1.1": "אב"}, {"Gen.1.2": "אב"})
        self.assertEqual(data["sp_only_reference_labels"], ["Gen.1.1"])
        self.assertEqual(data["wlc_only_reference_labels"], ["Gen.1.2"])
        self.assertEqual(data["summary"]["same_label_pairs"], 0)

    def test_metadata_export_has_no_source_text(self):
        data = M.screen({"Gen.1.1": "בראשית"}, {"Gen.1.1": "ראשית"})
        self.assertNotIn("בראשית", json.dumps(data, ensure_ascii=False))
        self.assertNotIn("ראשית", json.dumps(data, ensure_ascii=False))

    def test_saved_counts_partition_all_five_books(self):
        data = json.loads(M.OUT.read_text())
        total = data["summary"]
        self.assertEqual(len(data["books"]), 5)
        self.assertEqual(total["sp_verse_nodes"], 5841)
        self.assertEqual(total["wlc_verses"], 5853)
        self.assertEqual(total["same_label_pairs"], total["consonantal_equal"] + total["consonantal_different"])
        for name in ("sp_verse_nodes", "wlc_verses", "same_label_pairs", "consonantal_equal", "consonantal_different"):
            self.assertEqual(total[name], sum(b[name] for b in data["books"]))
        self.assertEqual(total["wlc_verses"], total["same_label_pairs"] + len(data["wlc_only_reference_labels"]))
        self.assertTrue(all(value is False for value in data["policy"].values()))

    def test_omitted_label_does_not_erase_relocated_incense_altar_lead(self):
        data = json.loads(M.OUT.read_text())
        self.assertIn("Exod.30.1", data["wlc_only_reference_labels"])
        lead = next(r for r in data["largest_length_difference_leads"] if r["reference_label"] == "Exod.26.35")
        self.assertEqual(lead["sp_minus_wlc_letters"], 507)
        self.assertIn("not historical priority", data["lead_selection"])

    def test_modified_provenance_is_rejected_before_loading(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            directory = base / "tf/7.1.3"
            directory.mkdir(parents=True)
            (base / "README.md").write_text("changed")
            with self.assertRaisesRegex(ValueError, "provenance hash mismatch"):
                M.load_sp(directory)


if __name__ == "__main__":
    unittest.main()
