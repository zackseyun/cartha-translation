"""Numerical-accounting safeguards; not ancient-letter accuracy tests."""
import json
import unittest
try:
    import numpy as np
    from tools.textual_restoration.build_en_gedi_wider_renderer_check import DISCOVERY, PROTOCOL, select_points, preflight, summarize
except ModuleNotFoundError as error:
    if error.name not in ("numpy", "PIL"):
        raise
    raise unittest.SkipTest("Requires bundled NumPy/Pillow runtime") from error


class WiderRendererTests(unittest.TestCase):
    def test_grid_denominator_and_prior_exclusion(self):
        points, counts = select_points(json.loads(PROTOCOL.read_text()), json.loads((DISCOVERY / "en_gedi_renderer_protocol.v1.json").read_text()))
        self.assertEqual(counts["nominal_grid_slots"], 306)
        self.assertEqual(counts["union_grid_points"], 289)
        self.assertEqual(counts["overlap_slots_deduplicated"], 17)
        self.assertEqual(counts["previously_observed_points_removed"], [[984, 1679]])
        self.assertEqual(len(points), 288)
        self.assertEqual(len(set(points)), 288)

    def test_no_vacuous_pass_for_empty_or_unavailable(self):
        for rows in ([], [{"status": "mask-invalid"}], [{"status": "unavailable-slices"}]):
            report = summarize(rows)
            self.assertIsNone(report["observed_exact_match"])
            self.assertIsNone(report["maximum_absolute_error"])
            self.assertEqual(report["scope_status"], "incomplete")

    def test_signed_residuals_and_missing_denominator(self):
        rows = [{"status": "evaluated", "residual": -3}, {"status": "evaluated", "residual": 0}, {"status": "evaluated", "residual": 4}, {"status": "unavailable-slices"}, {"status": "mask-invalid"}]
        report = summarize(rows)
        self.assertEqual(report["targets"], 5)
        self.assertEqual(report["exact_matches"], 1)
        self.assertEqual(report["maximum_absolute_error"], 4)
        self.assertEqual(report["mean_absolute_error"], 7 / 3)
        self.assertFalse(report["observed_exact_match"])
        self.assertEqual(report["scope_status"], "incomplete")
        self.assertEqual(summarize(rows[:3])["scope_status"], "fail")

    def test_availability_uses_geometry_and_does_not_fill_missing_data(self):
        base = [10, 10, .5, 1, 0, 0]
        self.assertEqual(preflight(base, 7, 0, .5, {0, 1})["status"], "evaluable")
        shifted = preflight(base, 7, 2, .5, {0, 1})
        self.assertEqual(shifted, {"status": "unavailable-slices", "missing_slice_numbers": [2, 3]})
        self.assertEqual(preflight([0, 10, .5, 1, 0, 0], 7, 0, .5, {0, 1})["status"], "outside-volume")

    def test_invalid_normal_fails_instead_of_exclusion(self):
        with self.assertRaises(ValueError):
            preflight([10, 10, .5, 0, 0, 0], 7, 0, .5, {0, 1})

    def test_saved_accounting_and_raw_summaries(self):
        receipt = json.loads((DISCOVERY / "en_gedi_wider_renderer_check.v1.json").read_text())
        self.assertEqual(len(receipt["points"]), receipt["denominator"]["novel_targets"])
        self.assertEqual(len(receipt["candidates"]), 8)
        self.assertFalse(receipt["policy"]["new_letter_reading_claimed"])
        for candidate in receipt["candidates"]:
            self.assertEqual(candidate["summary"], summarize(candidate["results"]))
            self.assertEqual(candidate["full_predeclared_sample_status"], candidate["summary"]["scope_status"])
            self.assertEqual(sum(group["targets"] for group in candidate["by_spatial_group"].values()), 288)
            for row in candidate["results"]:
                if row["status"] == "evaluated":
                    point = receipt["points"][row["point_index"]]
                    self.assertEqual(row["residual"], row["prediction"] - point["published_texture_value"])
                else:
                    self.assertNotIn("residual", row)
                    self.assertNotIn("prediction", row)


if __name__ == "__main__":
    unittest.main()
