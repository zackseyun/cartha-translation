import json
from pathlib import Path
import unittest
import numpy as np
from tools.textual_restoration import correct_en_gedi_registration_coordinates as fix


class CoordinateCorrectionTests(unittest.TestCase):
    def test_pixel_centers_not_pixel_edges(self):
        np.testing.assert_array_equal(fix.offsets([2,4]),[0.5,1.5])
        # Four original unit-width pixel cells have centers0,1,2,3;
        # their first averaged cell is centered1.5, not0.
        self.assertEqual(float(fix.offsets([4])[0]),sum(range(4))/4)

    def test_conjugation_matches_direct_coordinate_conversion(self):
        m=np.array([[2,0.1,30],[-0.2,3,50]],dtype=float)
        dt=np.array([0.5,0.5]); dm=np.array([1.5,1.6])
        p=np.array([[2,5],[8,13]],dtype=float)
        corrected=fix.corrected_matrix(m,dt,dm)
        np.testing.assert_allclose(fix.previous.project(p+dt,corrected),fix.previous.project(p,m)+dm,rtol=0,atol=1e-12)

    def test_preserved_failure_and_no_refit(self):
        old=json.loads(fix.previous.OUTPUT.read_text()); new=json.loads(fix.OUTPUT.read_text())
        self.assertEqual(fix.previous.sha(fix.previous.OUTPUT),fix.PREVIOUS_SHA)
        self.assertEqual(fix.previous.sha(Path(fix.__file__)),new["builder_sha256"])
        self.assertEqual(new["coarse_registration_gate"]["status"],"fail")
        self.assertEqual(new["coarse_registration_gate"]["checks"],old["coarse_registration_gate"]["checks"])
        self.assertLess(new["maximum_absolute_residual_change"],1e-8)
        self.assertEqual(len(new["pairs"]),372)
        for a,b in zip(old["pairs"],new["pairs"]):
            for k in ("index","partition","ransac_inlier","descriptor_distance","second_distance"):
                self.assertEqual(a[k],b[k])
        for flag in ("registration_accepted","letter_labels_assigned","reading_benchmark_executed","image_outputs_written"):
            self.assertFalse(new[flag])

    def test_original_targets_are_not_shifted_with_features(self):
        old=json.loads(fix.previous.OUTPUT.read_text()); new=json.loads(fix.OUTPUT.read_text())
        self.assertEqual(len(new["prior_nineteen_target_projections"]),19)
        for a,b in zip(old["prior_nineteen_target_projections"],new["prior_nineteen_target_projections"]):
            self.assertEqual(a["texture_xy"],b["texture_xy"])
            self.assertIsNone(b["letter_label"])
            np.testing.assert_allclose(fix.previous.project([b["texture_xy"]],new["affine_original_pixel_centers"])[0],b["projected_master_xy"],rtol=0,atol=1e-8)


if __name__ == "__main__": unittest.main()
