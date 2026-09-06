"""Bounded geometry/receipt checks; never acceptance of a historical reading."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import numpy as np

from tools.textual_restoration import register_en_gedi_remerge as reg


class RemergeRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = json.loads(reg.OUTPUT.read_text())
        cls.protocol = json.loads(reg.PROTOCOL.read_text())

    def test_frozen_evidence_and_implementation_pins(self):
        self.assertEqual(reg.sha(reg.PROTOCOL), reg.PROTOCOL_SHA)
        self.assertEqual(self.saved["protocol_sha256"], reg.PROTOCOL_SHA)
        self.assertEqual(self.saved["protocol"], self.protocol)
        self.assertEqual(reg.sha(reg.PRIOR), self.protocol["inputs"]["mapping_receipt_sha256"])
        self.assertEqual(reg.sha(Path(reg.__file__)), self.saved["implementation_sha256"])
        helper = reg.ROOT / "tools/textual_restoration/register_en_gedi_segment.py"
        self.assertEqual(reg.sha(helper), self.saved["helper_sha256"])

    def test_lift_uses_pixel_centers_and_exact_odd_height_ratio(self):
        # The first area-resampled cell averages centers 0,1 or 0,1,2,3.
        self.assertEqual(reg.lift([0, 0], [2, 4]), [0.5, 1.5])
        scales = [2400 / 1200, 4067 / 2033]
        self.assertEqual(self.saved["coordinate_scales"][0], scales)
        # Edges of the analysis image must map to native image edges.
        np.testing.assert_allclose(reg.lift([-0.5, -0.5], scales), [-0.5, -0.5])
        np.testing.assert_allclose(
            reg.lift([1199.5, 2032.5], scales), [2399.5, 4066.5], rtol=0, atol=1e-12
        )
        np.testing.assert_allclose(
            reg.lift([599.5, 1016], scales), [1199.5, 2033], rtol=0, atol=1e-12
        )
        self.assertNotEqual(reg.lift([0, 1000], scales)[1], 2000.5)

    def test_dedup_rejects_either_endpoint_and_does_not_reserve_rejected_bins(self):
        def row(name, texture, master, distance):
            return dict(name=name, texture_xy=texture, master_xy=master,
                        descriptor_distance=distance, second_distance=100)

        rows = [
            row("first", [10.2, 10.3], [20.2, 20.3], 1),
            row("texture-only", [10.8, 10.9], [30.2, 30.3], 2),
            row("master-only", [40.2, 40.3], [20.8, 20.9], 3),
            row("both", [10.4, 10.5], [20.4, 20.5], 4),
            row("unreserved", [40.8, 40.9], [30.8, 30.9], 5),
            row("adjacent", [11, 10.3], [21, 20.3], 6),
        ][::-1]
        original = deepcopy(rows)
        kept, rejected = reg.deduplicate(rows)
        self.assertEqual([r["name"] for r in kept], ["first", "unreserved", "adjacent"])
        self.assertEqual(
            [(r["name"], r["repeated_retained_endpoint_bins"]) for r in rejected],
            [("texture-only", ["texture"]), ("master-only", ["master"]),
             ("both", ["texture", "master"])],
        )
        self.assertEqual(rows, original)

    def test_dedup_distance_tie_uses_second_distance_before_coordinates(self):
        rows = [dict(texture_xy=[1.1, 1.1], master_xy=[2.1, 2.1],
                     descriptor_distance=10, second_distance=30),
                dict(texture_xy=[1.9, 1.9], master_xy=[3.1, 3.1],
                     descriptor_distance=10, second_distance=20)]
        kept, rejected = reg.deduplicate(rows)
        self.assertEqual(kept, [rows[1]])
        self.assertEqual(rejected[0]["master_xy"], rows[0]["master_xy"])

    def test_tile_holdout_keeps_neighbors_together_and_respects_boundaries(self):
        points = [[512, 0], [767.9, 255.9], [511.9, 0], [0, 256], [0, 255.9], [768, 0]]
        rows = [dict(texture_xy=p, master_xy=[i, i]) for i, p in enumerate(points)]
        reg.partition(rows, 256)
        by_point = {tuple(r["texture_xy"]): r for r in rows}
        for p in ([512, 0], [767.9, 255.9], [0, 256]):
            self.assertEqual(by_point[tuple(p)]["partition"], "validation")
        for p in ([511.9, 0], [0, 255.9], [768, 0]):
            self.assertEqual(by_point[tuple(p)]["partition"], "fit")
        self.assertEqual(by_point[(512, 0)]["texture_tile"], [2, 0])
        self.assertEqual(by_point[(767.9, 255.9)]["texture_tile"], [2, 0])
        self.assertTrue(all(r["ransac_inlier"] is None for r in rows))

    def test_saved_pairs_account_for_every_rejection_and_separate_holdout_tiles(self):
        pairs, rejected = self.saved["pairs"], self.saved["rejected_pairs"]
        self.assertEqual((len(pairs), len(rejected)), (957, 108))
        self.assertEqual(self.saved["mutual_ratio_pairs"], len(pairs) + len(rejected))
        self.assertEqual(self.saved["geometric_pairs_retained"], len(pairs))
        self.assertEqual(self.saved["geometric_pairs_rejected"], len(rejected))
        for endpoint in ("texture_xy", "master_xy"):
            bins = [tuple(np.floor(r[endpoint]).astype(int)) for r in pairs]
            self.assertEqual(len(bins), len(set(bins)))
        partitions = {}
        for r in pairs:
            tile = tuple(int(v // 256) for v in r["texture_xy"])
            self.assertEqual(list(tile), r["texture_tile"])
            expected = "validation" if (tile[0] + 2 * tile[1]) % 3 == 2 else "fit"
            self.assertEqual(r["partition"], expected)
            partitions.setdefault(tile, set()).add(r["partition"])
            if expected == "validation":
                self.assertIsNone(r["ransac_inlier"])
        self.assertTrue(all(len(values) == 1 for values in partitions.values()))
        self.assertEqual(sum(r["partition"] == "fit" for r in pairs), 605)
        # Reconstruct all original matches, then replay only geometric dedup.
        kept_again, rejected_again = reg.deduplicate(pairs + rejected)
        identity = lambda r: (r["texture_keypoint_index"], r["master_keypoint_index"])
        self.assertEqual({identity(r) for r in kept_again}, {identity(r) for r in pairs})
        self.assertEqual(
            [(identity(r), r["repeated_retained_endpoint_bins"]) for r in rejected_again],
            [(identity(r), r["repeated_retained_endpoint_bins"]) for r in rejected],
        )

    def test_actual_failed_gate_is_retained(self):
        result = reg.gate(self.saved["pairs"], 2400, 4067, self.protocol["coarse_gate"])
        self.assertEqual(result, self.saved["coarse_registration_gate"])
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["training_inliers"], 116)
        self.assertEqual(result["validation_pairs"], 352)
        self.assertEqual(result["validation_within_20"], 82)
        self.assertAlmostEqual(result["validation_fraction_within_20"], 82 / 352)
        self.assertEqual(result["checks"], dict(training_count=True, validation_count=True,
                                              validation_agreement=False, x_span=False, y_span=False))

    def test_empty_evidence_fails_without_validation_fraction(self):
        result = reg.gate([], 2400, 4067, self.protocol["coarse_gate"])
        self.assertEqual(result["status"], "fail")
        self.assertIsNone(result["validation_fraction_within_20"])
        self.assertFalse(any(result["checks"].values()))

    def test_projections_preserve_prior_points_without_accepting_readings(self):
        prior = json.loads(reg.PRIOR.read_text())["points"]
        projections = self.saved["prior_geometry_projections"]
        self.assertEqual(len(projections), 68)
        self.assertEqual([r["prior_point_index"] for r in projections], list(range(len(prior))))
        for row, original in zip(projections, prior):
            self.assertEqual(row["texture_xy"], original["xy"])
            self.assertEqual(row["mask_value"], original["mask_value"])
            self.assertIsNone(row["accepted_verse_locator"])
            self.assertIsNone(row["accepted_letter_label"])
        for flag in ("reading_benchmark_executed", "image_outputs_written", "canonical_change"):
            self.assertFalse(self.saved[flag])


if __name__ == "__main__":
    unittest.main()
