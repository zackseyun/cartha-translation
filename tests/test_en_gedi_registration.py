"""Development-registration accounting, never historical reading accuracy."""
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from tools.textual_restoration import register_en_gedi_segment as reg


class RegistrationTests(unittest.TestCase):
    def test_protocol_and_code_pins(self):
        saved = json.loads(reg.OUTPUT.read_text())
        self.assertEqual(reg.sha(reg.PROTOCOL), reg.PROTOCOL_SHA)
        self.assertEqual(reg.sha(reg.PRIOR), reg.PRIOR_SHA)
        self.assertEqual(reg.sha(Path(reg.__file__)), saved["builder_sha256"])
        self.assertEqual(saved["protocol"], json.loads(reg.PROTOCOL.read_text()))

    def test_projection_and_residuals_independently(self):
        saved = json.loads(reg.OUTPUT.read_text())
        a, b = saved["affine_original_pixels"]
        for row in saved["pairs"]:
            x, y = row["texture_xy"]
            mx, my = a[0]*x+a[1]*y+a[2], b[0]*x+b[1]*y+b[2]
            self.assertAlmostEqual(mx, row["predicted_master_xy"][0], places=8)
            self.assertAlmostEqual(my, row["predicted_master_xy"][1], places=8)
            residual = ((mx-row["master_xy"][0])**2+(my-row["master_xy"][1])**2)**0.5
            self.assertAlmostEqual(residual, row["residual_master_pixels"], places=8)

    def test_failed_gate_preserved(self):
        saved = json.loads(reg.OUTPUT.read_text())
        result = reg.gate(saved["pairs"],1969,3358,saved["protocol"]["provisional_region_gate"])
        self.assertEqual(result, saved["coarse_registration_gate"])
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["validation_pairs"],124)
        self.assertEqual(result["validation_within_20"],60)
        self.assertFalse(result["checks"]["validation_agreement"])
        self.assertFalse(result["checks"]["y_span"])
        self.assertFalse(saved["reading_benchmark_executed"])
        self.assertFalse(saved["image_outputs_written"])

    def test_empty_evidence_cannot_pass(self):
        p=json.loads(reg.PROTOCOL.read_text())
        self.assertEqual(reg.gate([],1969,3358,p["provisional_region_gate"])["status"],"fail")

    def test_partitions_and_old_targets_not_replaced(self):
        saved=json.loads(reg.OUTPUT.read_text())
        for i,r in enumerate(saved["pairs"]):
            self.assertEqual(r["partition"], "validation" if i%3==2 else "fit")
            if r["partition"]=="validation":
                self.assertIsNone(r["ransac_inlier"])
        prior=json.loads(reg.PRIOR.read_text())
        c=next(c for c in prior["candidates"] if c["radius_parameter"]==7 and c["slice_index_offset"]==0 and c["interpolator"]=="historical-c10-corner")
        expected=[r["point_index"] for r in c["results"] if r["status"]=="evaluated"]
        self.assertEqual([r["prior_point_index"] for r in saved["prior_nineteen_target_projections"]], expected)
        for r in saved["prior_nineteen_target_projections"]:
            self.assertIsNone(r["letter_label"])
            self.assertEqual(r["texture_xy"],prior["points"][r["prior_point_index"]]["texture_xy"])
            np.testing.assert_allclose(reg.project([r["texture_xy"]],saved["affine_original_pixels"])[0],r["projected_master_xy"],rtol=0,atol=1e-8)

    def test_provenance_rejects_wrong_hash_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"invalid.png"
            p.write_bytes(b"not an image")
            with self.assertRaises(ValueError): reg.checked_image(p,"0"*64,(1,1))
            link=Path(tmp)/"link.png"
            link.symlink_to(p)
            with self.assertRaises(ValueError): reg.checked_image(link,reg.sha(p),(1,1))


if __name__ == "__main__":
    unittest.main()
