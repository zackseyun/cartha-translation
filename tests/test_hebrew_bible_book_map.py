import json
from pathlib import Path
import tempfile
import unittest

from tools.textual_restoration import build_hebrew_bible_book_map as m


def word(text, ref="Gen 1:1"):
    return ["", text, "", "", "", ref]


def record(label, lines):
    return {"scroll": label, "fragments": [{"id": "f1", "lines": [
        {"n": str(i + 1), "words": line} for i, line in enumerate(lines)]}]}


class BookMapTests(unittest.TestCase):
    def test_explicit_reference_spellings_and_numbering(self):
        self.assertEqual(m.reference_kind("Ex 1:1", set()), ("biblical_reference", "Exod.1.1"))
        self.assertEqual(m.reference_kind("Is 54:12", set()), ("biblical_reference", "Isa.54.12"))
        self.assertEqual(m.reference_kind("Josh 5:0", set()), ("biblical_reference", "Josh.5.0"))
        self.assertEqual(m.reference_kind("Isaiah 54:12", set()), ("unresolved", None))

    def test_source_references_never_become_verses(self):
        known = {"1q8", "mur88", "4q1"}
        self.assertEqual(m.reference_kind("1Q8 4:1", known)[0], "source_numeric_locator_reference")
        self.assertEqual(m.reference_kind("4Q1 f6ii:2", known)[0], "source_fragment_line_reference")
        self.assertEqual(m.reference_kind("4Q2 f6:2", known)[0], "unresolved")
        self.assertEqual(m.reference_kind("", known)[0], "empty")

    def test_bracket_state_crosses_verse_and_line_boundaries(self):
        data = m.scan([record("4Q1", [[word("[אב", "Gen 1:1")],
                                      [word("גד", "Ex 1:1"), word("ה]ו", "Ex 1:1")]])])
        self.assertEqual(data["pairs"][("Exod", 0)]["syntax"][m.SYNTAX_KEYS[0]], 1)
        self.assertEqual(data["pairs"][("Exod", 0)]["syntax"][m.SYNTAX_KEYS[1]], 1)

    def test_unbalanced_or_nested_fragments_are_unresolved(self):
        for text in ("אב]", "[אב", "[[אב]]", "]אב["):
            self.assertEqual(m.bracket_classes([word(text)]), [m.SYNTAX_KEYS[3]])
        self.assertEqual(m.bracket_classes([word("אב"), word("[גד")]), [m.SYNTAX_KEYS[3]] * 2)
        self.assertEqual(m.bracket_classes([word("׃")]), [m.SYNTAX_KEYS[4]])

    def test_brackets_reset_between_fragments(self):
        rec = record("4Q1", [[word("[אב")]])
        rec["fragments"].append({"id": "f2", "lines": [{"n": "1", "words": [word("גד]")]}]})
        data = m.scan([rec])
        self.assertEqual(data["pairs"][("Gen", 0)]["syntax"][m.SYNTAX_KEYS[3]], 2)

    def test_duplicate_labels_keep_ordinals_and_do_not_merge(self):
        data = m.scan([record("4Q483", [[word("אב")]]), record("4Q483", [[word("גד")]])])
        self.assertEqual(data["labels"]["4Q483"], 2)
        self.assertEqual(set(data["pairs"]), {("Gen", 0), ("Gen", 1)})
        self.assertEqual(len(data["references"]["Gen"]), 1)

    def test_word_accounting_zero_records_and_source_disagreements(self):
        data = m.scan([record("4Q1", [[word("א"), word("ב", ""), word("ג", "nonsense")]]),
                       record("4Q2", [[word("ד", "4Q1 f1:1")]])])
        self.assertEqual(sum(data["kinds"].values()), 4)
        self.assertEqual(data["totals"]["records_without_biblical_tags"], 1)
        self.assertEqual(data["zero_records"][0]["source_record_index"], 1)
        self.assertEqual(data["mismatches"][("4Q2", "4Q1")], 1)
        self.assertEqual(data["unresolved_values"]["nonsense"], 1)

    def test_malformed_word_and_unpinned_input_fail(self):
        for words in ([["bad"]], [[1, "אב", "", "", "", "Gen 1:1"]]):
            with self.assertRaises(ValueError):
                m.scan([record("4Q1", [words])])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            path.write_text("[]")
            with self.assertRaisesRegex(ValueError, "pinned"):
                m.build(path)

    def test_receipt_all_39_books_and_exact_accounting(self):
        d = json.loads(m.OUT.read_text())
        self.assertEqual([b["wlc_book"] for b in d["books"]], list(m.BOOKS))
        self.assertEqual(d["summary"]["zero_hit_books"], ["1_chronicles", "nehemiah", "esther"])
        self.assertEqual(sum(d["summary"]["reference_kind_counts"].values()), 218217)
        self.assertEqual(d["summary"]["reference_kind_counts"].get("unresolved", 0), 0)
        self.assertEqual(len(d["records_without_biblical_tags"]), 3)
        for b in d["books"]:
            self.assertEqual(b["wlc_verse_anchor_denominator"], b["same_label_wlc_anchor_intersection"] + b["wlc_anchors_without_qdr_reference_tag"])
            self.assertEqual(b["qdr_indexed_reference_anchors"], b["same_label_wlc_anchor_intersection"] + len(b["qdr_anchors_not_in_wlc"]))
            self.assertEqual(b["qdr_source_records"], len(b["source_records"]))
            for r in b["source_records"]:
                self.assertEqual(sum(r["bracket_syntax_word_counts"].values()), r["word_reference_tags"])
                self.assertEqual(r["reading_support"], "not-assessed")

    def test_receipt_holds_roles_and_no_transcriptions(self):
        d = json.loads(m.OUT.read_text())
        rows = [r for b in d["books"] for r in b["source_records"]]
        colliding = [r for r in rows if r["label"] == "4Q483"]
        self.assertEqual({r["source_record_index"] for r in colliding}, {2, 209})
        self.assertTrue(all("4q483-duplicate-records" in r["identity_hold_ids"] for r in colliding))
        self.assertTrue(all("genesis-label-collision" in r["identity_hold_ids"] for r in rows if r["label"] in {"4Q8a", "4Q8b", "4Q8c", "4Q8d"}))
        missing_roles = {r["role"] for r in d["supplemental_catalogue_role_targets_without_qdr_query_label"]}
        self.assertTrue({"quotation", "reworked-pentateuch-genre-review", "pesher-quotation-candidate"} <= missing_roles)
        self.assertNotRegex(m.OUT.read_text(), r"[א-ת]")
        self.assertIsNone(d["policy"]["physical_manuscript_count"])


if __name__ == "__main__":
    unittest.main()
