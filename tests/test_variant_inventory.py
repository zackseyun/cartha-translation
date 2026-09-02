import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("variant_inventory", ROOT / "tools/textual_restoration/build_variant_inventory.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class VariantInventoryTest(unittest.TestCase):
    def test_saved_artifacts_and_sources_verify(self):
        summary = M.verify_inventory()
        self.assertEqual(summary["totals"]["books_scanned"], 66)
        self.assertGreater(summary["totals"]["verse_files_scanned"], 31000)

    def test_lexical_note_is_not_automatically_a_variant(self):
        record = {"translation": {"footnotes": [{"reason": "lexical_alternative", "text": "The Greek word can also mean servant."}]}}
        self.assertEqual(M.footnote_signals(record), [])

    def test_typed_textual_note_is_a_screening_signal(self):
        record = {"translation": {"footnotes": [{"reason": "textual_variant", "text": "An alternate form is present."}]}}
        self.assertEqual(M.footnote_signals(record)[0]["signal"], "typed-textual-note")

    def test_marginal_reading_is_detected(self):
        record = {"translation": {"footnotes": [{"reason": "alternative_reading", "text": "Following the traditional marginal reading, we are his."}]}}
        self.assertEqual(M.footnote_signals(record)[0]["signal"], "witness-mention-screen")

    def test_multiple_apparatus_entries_and_spans_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "Mark.xml"
            path.write_text('<book><verse>Mark 16:9</verse><note>9–20 text WH ] – RP</note><note>• word WHapp Tregmarg ] alternative NA28</note></book>')
            rows = M.parse_apparatus(path, {})
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0]["requires_span_or_bracket_review"])
        self.assertIsNone(rows[0]["local_reference_match"])
        self.assertIn("WHapp", rows[1]["edition_labels"])
        self.assertIn("Tregmarg", rows[1]["edition_labels"])
        self.assertFalse(rows[1]["adjudicated"])

    def test_unanchored_apparatus_note_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "Mark.xml"
            path.write_text('<book><note>text</note></book>')
            with self.assertRaises(ValueError):
                M.parse_apparatus(path, {})

    def test_qere_is_not_an_independent_manuscript(self):
        qere, _ = M.parse_wlc(ROOT / "sources/ot/wlc/Ps.xml")
        row = next(x for x in qere if x["reference"] == "Ps.100.3")
        self.assertEqual(row["ketiv"], "ו/לא")
        self.assertEqual(row["qere"], ["וְ/ל֣/וֹ"])
        self.assertFalse(row["independent_manuscript_variant"])
        self.assertIn("not automatically POB", row["reference_system"])

    def test_raw_apparatus_notes_are_not_rewritten(self):
        total = 0
        for path in (ROOT / "sources/nt/sblgnt_apparatus/xml").glob("*.xml"):
            upstream = ["".join(x.itertext()).strip() for x in ET.parse(path).getroot().findall("note")]
            rows = [json.loads(line) for line in (M.OUT / "nt_editions" / (path.stem + ".jsonl")).read_text().splitlines()]
            self.assertEqual(upstream, [x["raw_note"] for x in rows])
            self.assertTrue(all(x["evidence_type"] == "critical-edition-comparison-not-manuscript-collation" for x in rows))
            total += len(rows)
        self.assertEqual(total, 6934)  # Exact pinned publisher revision, not older print-edition total.

    def test_edition_silence_is_not_manuscript_unanimity(self):
        rows = [json.loads(x) for x in (M.OUT / "nt_editions/Rev.jsonl").read_text().splitlines()]
        at_verse = [x for x in rows if x["chapter"] == 13 and x["verse"] == 18]
        self.assertEqual(len(at_verse), 2)
        raw = " ".join(x["raw_note"] for x in at_verse)
        self.assertIn("χξϛ", raw)  # 666 is encoded, including a numeral-form variation.
        self.assertNotIn("χιϛ", raw)  # The 616 variant is not covered here.
        self.assertNotIn("616", raw)
        self.assertNotIn("δέκα", raw)
        notes = [json.loads(x) for x in (M.OUT / "local_notes/nt/revelation.jsonl").read_text().splitlines()]
        self.assertTrue(any(x["chapter"] == 13 and x["verse"] == 18 for x in notes))

    def test_priority_cases_are_not_auto_promoted(self):
        rows = [json.loads(x) for x in (M.OUT / "priority_cases.jsonl").read_text().splitlines()]
        self.assertEqual(len(rows), 48)
        self.assertEqual(sum(x["testament"] == "nt" for x in rows), 24)
        self.assertTrue(all(x["canonical_promotion_approved"] is False for x in rows))
        self.assertTrue(all(x["source_list_is_attestation_claim"] is False for x in rows))
        self.assertTrue(all(x["local_snapshot"] is not None for x in rows))

    def test_summary_layer_totals_are_separate(self):
        summary = json.loads((M.OUT / "summary.json").read_text())
        self.assertTrue(summary["not_exhaustive_manuscript_apparatus"])
        self.assertFalse(summary["canonical_text_modified"])
        for field, total in [("flagged_passages", "local_note_flagged_passages"), ("qere_records", "hebrew_qere_records"), ("nt_apparatus_entries", "nt_edition_apparatus_entries")]:
            self.assertEqual(sum(x[field] for x in summary["books"].values()), summary["totals"][total])


if __name__ == "__main__":
    unittest.main()
