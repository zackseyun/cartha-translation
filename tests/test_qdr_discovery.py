import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("qdr_discovery", ROOT / "tools/textual_restoration/build_qdr_discovery.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def fixture(ref="Gen 1:1", label="4Q-test"):
    return {"scroll": label, "fragments": [{"id": "f1", "lines": [
        {"n": "1", "words": [["", "restricted transcription", "", "", "", ref]]}]}]}


class QdrDiscoveryTests(unittest.TestCase):
    def test_reference_aliases_are_explicit(self):
        self.assertEqual(M.parse_reference("Ex 1:5"), "Exod.1.5")
        self.assertEqual(M.parse_reference("Is 9:2"), "Isa.9.2")
        self.assertIsNone(M.parse_reference("4Q11 f1:7"))
        self.assertIsNone(M.parse_reference("Gen 1:1-2"))

    def test_nested_word_references_are_all_scanned(self):
        record = fixture()
        record["fragments"][0]["lines"][0]["words"].append(["", "text", "", "", "", "Ex 1:5"])
        result = M.scan([record])
        self.assertEqual(set(result["hits"]), {"Gen.1.1", "Exod.1.5"})
        self.assertEqual(result["all_words"], 2)

    def test_duplicate_labels_preserve_record_ordinals_not_extra_votes(self):
        result = M.scan([fixture(), fixture()])
        self.assertEqual(result["labels"]["4Q-test"], 2)
        self.assertEqual({hit[1] for hit in result["hits"]["Gen.1.1"]}, {0, 1})
        self.assertEqual(len(result["book_labels"]["Gen"]), 1)

    def test_unparsed_references_are_accounted_for(self):
        result = M.scan([fixture("4Q11 f1:7"), fixture("")])
        self.assertEqual(sum(result["unparsed"].values()), 2)
        self.assertFalse(result["hits"])

    def test_scanner_does_not_export_transcription_or_morphology(self):
        self.assertNotIn("restricted transcription", repr(M.scan([fixture()])))

    def test_malformed_reference_cannot_be_silently_skipped(self):
        record = fixture()
        record["fragments"][0]["lines"][0]["words"][0] = ["short"]
        with self.assertRaises(ValueError):
            M.scan([record])

    def test_qere_and_comment_text_do_not_enter_source_match(self):
        verse = ET.fromstring(f'<verse xmlns="{M.NS["o"]}"><w>לא</w><note><w>לו</w></note><seg type="x-pe">פ</seg></verse>')
        self.assertEqual(M.verse_keys(verse), {"לא", "לאפ"})
        self.assertNotIn("לופ", M.verse_keys(verse))

    def test_ambiguous_and_empty_source_matches_are_not_unique(self):
        self.assertEqual(M.map_source("", {"": ["Gen.1.1"]}), [])
        self.assertEqual(len(M.map_source("לא", {"לא": ["Gen.1.1", "Gen.1.2"]})), 2)

    def test_saved_screen_keeps_evidence_and_accounting_boundaries(self):
        data = json.loads(M.OUT.read_text())
        total = data["summary"]
        self.assertEqual(total["source_records"], 266)
        self.assertEqual(total["distinct_source_labels"], 265)
        self.assertEqual(total["word_records_scanned"], total["recognized_biblical_word_tags"] + total["unparsed_word_tags"])
        self.assertEqual(len(data["books"]), 39)
        self.assertFalse(data["policy"]["index_hits_are_reading_support"])
        self.assertFalse(data["policy"]["zero_hits_prove_absence"])
        self.assertTrue(all(c["query_scope"] == "single-anchor-only-not-entire-range-or-variant"
                            for c in data["priority_cases"]))
        self.assertTrue(all(w["reading_support"] == "not-assessed" for c in data["priority_cases"] for w in c["candidate_labels"]))

    def test_isaiah_joy_case_uses_actual_pob_anchor(self):
        data = json.loads(M.OUT.read_text())
        case = next(c for c in data["priority_cases"] if c["case_id"] == "ot.isaiah.9.2")
        self.assertEqual(case["wlc_reference"], "Isa.9.2")
        self.assertEqual(case["pob_reference"], "Isaiah 9:2")
        psalm = next(c for c in data["priority_cases"] if c["case_id"] == "ot.psalms.22.16")
        self.assertEqual(psalm["wlc_reference"], "Ps.22.17")

    def test_nonstandard_labels_are_not_all_non_qumran_findspots(self):
        data = M.non_qumran_screen(M.scan([
            fixture(label="Mur1"), fixture(label="Mas1"),
            fixture(label="Xq1"), fixture(label="Pam43113"), fixture(label="4Q51")]))
        self.assertEqual([r["label"] for r in data["labels"]], ["Mas1", "Mur1"])
        self.assertEqual(data["other_nonstandard_labels_not_assigned"], ["Pam43113", "Xq1"])
        self.assertFalse(data["policy"]["label_prefix_proves_findspot"])

    def test_mur88_manuscript_locators_are_not_biblical_anchors(self):
        data = M.non_qumran_screen(M.scan([
            fixture("Mur88 1:1", "Mur88"), fixture("Amos 9:12", "Mur88")]))
        self.assertEqual(data["labels"][0]["indexed_reference_anchors"], 1)
        self.assertEqual(data["labels"][0]["book_labels"], ["Amos"])
        self.assertEqual(data["labels"][0]["source_records"], 2)

    def test_non_qumran_receipt_has_no_transcription_or_full_verse_index(self):
        result = M.non_qumran_screen(M.scan([fixture(label="Mas1")]))
        self.assertNotIn("restricted transcription", json.dumps(result))
        self.assertNotIn("Gen.1.1", json.dumps(result))

    def test_saved_non_qumran_screen_preserves_known_boundaries(self):
        data = json.loads(M.NON_QUMRAN_OUT.read_text())
        self.assertEqual(data["summary"]["selected_labels"], 22)
        self.assertEqual(data["summary"]["other_nonstandard_labels_not_assigned"], 8)
        labels = {r["label"]: r for r in data["labels"]}
        self.assertEqual(labels["Mur88"]["indexed_reference_anchors"], 424)
        self.assertEqual(labels["Arugleviticus"]["indexed_reference_anchors"], 10)
        self.assertFalse(data["policy"]["all_known_non_qumran_sources_covered"])


if __name__ == "__main__":
    unittest.main()
