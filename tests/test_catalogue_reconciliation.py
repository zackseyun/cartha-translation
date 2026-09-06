import json
from pathlib import Path
import tempfile
import unittest

from tools.textual_restoration import build_catalogue_reconciliation as M


def record(label="legacy", references=("Lev 2:8",), fragment="f1"):
    return {"scroll": label, "fragments": [{"id": fragment, "lines": [
        {"n": "1", "words": [["", "PRIVATE-TEXT", "", "", "", r] for r in references]}]}]}


def targets():
    return {"book": "Lev", "checked_date": "2026-09-05", "scope": "test",
            "mapping_policy": {"canonical_change_applied": False},
            "entries": [
                {"id": "part-a", "query_labels": ["legacy"], "query_chapters": [1, 2, 3],
                 "reported_status": "published", "role": "test"},
                {"id": "part-b", "query_labels": ["legacy"], "query_chapters": [21, 22, 23, 24, 25],
                 "reported_status": "published", "role": "test"}]}


class CatalogueReconciliationTests(unittest.TestCase):
    def test_two_scopes_do_not_become_two_legacy_labels(self):
        result = M.reconcile([record(references=("Lev 2:8", "Lev 21:17"))], targets())
        self.assertEqual(result["summary"]["target_names_with_scoped_index_hits"], 2)
        self.assertEqual(result["summary"]["distinct_matched_legacy_labels"], 1)
        self.assertIsNone(result["shared_legacy_records"][0]["independent_witness_count"])

    def test_untagged_fragment_cannot_be_assigned(self):
        result = M.reconcile([record(references=("4Q24 f29:1", ""))], targets())
        frag = result["shared_legacy_records"][0]["fragments"][0]
        self.assertEqual(frag["assignment_status"], "unresolved-no-book-anchor")
        self.assertEqual(frag["candidate_target_ids_by_chapter_tags"], [])
        self.assertEqual(frag["non_book_or_unparsed_word_tags"], 2)

    def test_mixed_fragment_not_forced_into_one_scope(self):
        result = M.reconcile([record(references=("Lev 2:8", "Lev 22:3"))], targets())
        self.assertEqual(result["shared_legacy_records"][0]["fragments"][0]["assignment_status"],
                         "ambiguous-multiple-scopes")

    def test_no_label_and_no_book_anchor_are_different(self):
        absent = M.reconcile([], targets())["targets"][0]
        no_anchor = M.reconcile([record(references=("Gen 1:1",))], targets())["targets"][0]
        self.assertEqual(absent["index_status"], "label-not-in-pinned-index")
        self.assertEqual(no_anchor["index_status"], "label-present-no-scoped-book-anchor")

    def test_unknown_label_and_out_of_scope_anchor_stay_visible(self):
        result = M.reconcile([record("unknown"), record(references=("Lev 10:1",))], targets())
        self.assertEqual(result["unmatched_book_labels"], ["unknown"])
        self.assertEqual(result["summary"]["book_anchor_locator_pairs_outside_query_scopes"], 2)

    def test_duplicate_records_keep_ordinals_and_collision_flag(self):
        result = M.reconcile([record(), record()], targets())
        self.assertEqual(result["targets"][0]["source_record_ordinals"], [0, 1])
        self.assertTrue(result["targets"][0]["identity_collision"])
        self.assertEqual(len(result["shared_legacy_records"][0]["fragments"]), 2)

    def test_no_text_or_full_verse_index_export(self):
        encoded = json.dumps(M.reconcile([record()], targets()))
        self.assertNotIn("PRIVATE-TEXT", encoded)
        self.assertNotIn("Lev 2:8", encoded)
        self.assertNotIn("Lev.2.8", encoded)

    def test_duplicate_ids_and_empty_scope_rejected(self):
        duplicate = targets()
        duplicate["entries"][1]["id"] = "part-a"
        with self.assertRaises(ValueError):
            M.reconcile([], duplicate)
        invalid = targets()
        invalid["entries"][0]["query_chapters"] = []
        with self.assertRaises(ValueError):
            M.reconcile([], invalid)

    def test_reference_aliases_use_same_parser_in_shared_fragments(self):
        spec = targets()
        spec["book"] = "Exod"
        result = M.reconcile([record(references=("Ex 2:8",))], spec)
        self.assertEqual(result["targets"][0]["indexed_anchor_count"], 1)
        self.assertEqual(result["shared_legacy_records"][0]["fragments"][0]["indexed_anchor_count"], 1)

    def test_wrong_qdr_hash_rejected_before_processing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("[]")
            with self.assertRaisesRegex(ValueError, "QDR differs"):
                M.build(path, Path(directory) / "missing.pdf")

    def test_unknown_book_is_rejected_not_silently_empty(self):
        spec = targets()
        spec["book"] = "Leviticus"
        with self.assertRaisesRegex(ValueError, "invalid book"):
            M.reconcile([record()], spec)

    def test_saved_receipt_fingerprints_and_complete_target_accounting(self):
        source = json.loads(M.TARGETS.read_text())
        result = json.loads(M.OUT.read_text())
        self.assertEqual(len(source["entries"]), 30)
        self.assertEqual([r["id"] for r in source["entries"]],
                         [r["catalogue_id"] for r in result["targets"]])
        self.assertEqual(result["inputs"]["targets_sha256"], M.sha(M.TARGETS.read_bytes()))
        self.assertEqual(result["inputs"]["builder_sha256"], M.sha(Path(M.__file__).read_bytes()))
        self.assertEqual(result["inputs"]["scanner_sha256"],
                         M.sha((M.ROOT / "tools/textual_restoration/build_qdr_discovery.py").read_bytes()))
        summary = result["summary"]
        self.assertEqual(summary["catalogue_reported_published_targets"], 27)
        self.assertEqual(summary["catalogue_reported_unpublished_targets"], 3)
        self.assertEqual(summary["target_names_with_scoped_index_hits"], 18)
        self.assertEqual(summary["target_names_without_index_labels"], 12)
        self.assertEqual(summary["distinct_matched_legacy_labels"], 17)
        self.assertEqual(summary["pinned_index_book_anchors"], 484)
        self.assertEqual(summary["book_anchor_locator_pairs_outside_query_scopes"], 0)
        self.assertFalse(result["policy"]["all_current_witnesses_reconciled"])
        self.assertTrue(all(r["reading_support"] == "not-assessed" for r in result["targets"]))

    def test_real_4q24_unassigned_fragments_and_chapter_counts(self):
        result = json.loads(M.OUT.read_text())
        shared = result["shared_legacy_records"][0]
        self.assertEqual(shared["legacy_label"], "4Q24")
        self.assertEqual([f["fragment"] for f in shared["fragments"]
                          if f["assignment_status"] == "unresolved-no-book-anchor"], ["f29", "f30"])
        rows = {r["catalogue_id"]: r for r in result["targets"]}
        self.assertEqual(rows["4Q24a"]["indexed_anchor_count"], 31)
        self.assertEqual(rows["4Q24b"]["indexed_anchor_count"], 101)
        self.assertEqual(rows["Mur/HevLev"]["matched_labels"], ["4Q26c"])
        for key in ["4Q119", "4Q120", "4QpaptgLev", "4Q365", "4Q366", "4Q367", "EGLev"]:
            self.assertEqual(rows[key]["index_status"], "label-not-in-pinned-index")


if __name__ == "__main__":
    unittest.main()
