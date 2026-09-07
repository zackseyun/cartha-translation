"""Public source-comparison notices survive rebuilds without editing frozen verses."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("revision_index", ROOT / "tools/build_revisions_index.py")
index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index)


class RevisionNoticeTests(unittest.TestCase):
    def test_isaiah_notice_matches_applied_wording_and_preserves_uncertainty(self):
        notice, = json.loads((ROOT / "data/revision-notices.json").read_text())
        verse = yaml.safe_load((ROOT / "translation/ot/isaiah/053/011.yaml").read_text())
        self.assertEqual(notice["from"], verse["restoration_draft"]["baseline"]["english_text"])
        self.assertEqual(notice["to"], verse["translation"]["text"])
        self.assertIn("provisional", notice["rationale"].split(".")[0])
        self.assertIn("Masoretic Text lacks", notice["rationale"])
        self.assertEqual(json.loads((ROOT / notice["source_review"]).read_text())["status"], "applied-verified")

    def test_rebuild_includes_notice_once_and_counts_source_review(self):
        notice, = json.loads((ROOT / "data/revision-notices.json").read_text())
        coverage = json.loads((ROOT / "revisions.json").read_text())["review_coverage"]
        with patch.object(index, "walk_verses", return_value=[]), patch.object(index, "walk_review_records", return_value=coverage):
            result = index.build_index()
        self.assertEqual(result["totals"]["total_revisions"], 1)
        self.assertEqual(result["revisions"][0]["proposal_source"], "source_grounded_review")
        with patch.object(index, "walk_verses", return_value=[notice.copy()]), patch.object(index, "walk_review_records", return_value=coverage):
            self.assertEqual(len(index.build_index()["revisions"]), 1)


if __name__ == "__main__":
    unittest.main()
