"""Run with the bundled NumPy/Pillow runtime, not the minimal repo venv."""
import io
import unittest
try:
    import numpy as np
    from tools.textual_restoration.probe_en_gedi_mapping import sample_map, trilinear
    from tools.textual_restoration.build_en_gedi_renderer_probe import interpolate_candidate, sample_line
except ModuleNotFoundError as error:
    if error.name not in ("numpy", "PIL"):
        raise
    raise unittest.SkipTest("Mapping tests require the bundled NumPy/Pillow runtime") from error


def mapping(values, rows=1, cols=2):
    return io.StringIO('%YAML:1.0\nPerPixelMapping: !!opencv-matrix\n'
                       f'   rows: {rows}\n   cols: {cols}\n   dt: "6d"\n'
                       '   data: [ ' + values + ' ]\n')


class MappingTests(unittest.TestCase):
    def test_scattered_samples_across_tiny_chunks(self):
        result = sample_map(mapping(', '.join(map(str, range(12)))), [(1, 0), (0, 0)], 3)
        self.assertEqual(result[:3], (1, 2, 12))
        self.assertEqual(result[3][(1, 0)], list(range(6, 12)))

    def test_wrong_scalar_count_and_invalid_token_rejected(self):
        for values in ("1, 2", "1, 2, .Nan", "1, 2, nonsense"):
            with self.assertRaises(ValueError):
                sample_map(mapping(values), [(0, 0)])

    def test_points_must_be_in_bounds(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            sample_map(mapping("0"), [(2, 0)])

    def test_trilinear_linear_field(self):
        slices = {z: np.array([[x + 2*y + 4*z for x in range(3)] for y in range(3)]) for z in range(3)}
        self.assertAlmostEqual(trilinear(slices, [0.2, 0.4, 0.6]), 3.4)

    def test_missing_and_out_of_bounds_are_not_black_voxels(self):
        slices = {0: np.ones((3, 3)), 1: np.ones((3, 3))}
        for point in ([0.2, 0.4, 1.6], [-0.1, 0.5, 0.5], [2.5, 0.5, 0.5]):
            with self.assertRaises(ValueError):
                trilinear(slices, point)

    def test_historical_corner_is_isolated_from_correct_interpolation(self):
        slices = {0: np.zeros((2, 2), dtype=np.uint16), 1: np.zeros((2, 2), dtype=np.uint16)}
        slices[0][1, 1] = 80
        self.assertEqual(interpolate_candidate(slices, [.5, .5, .5], "standard-trilinear"), 10)
        self.assertEqual(interpolate_candidate(slices, [.5, .5, .5], "historical-c10-corner"), 0)
        self.assertEqual(trilinear(slices, [.5, .5, .5]), 10)

    def test_line_endpoints_center_duplication_and_normalization(self):
        slices = {z: np.tile(np.arange(20, dtype=np.uint16), (20, 1)) for z in (0, 1)}
        value = sample_line(slices, [8, 8, .5, 2, 0, 0], 3.5, .5, 0, "standard-trilinear")
        self.assertEqual(value["sample_count"], 14)
        self.assertEqual(value["prediction"], 11)
        self.assertEqual(value["maximizing_normal_offsets"], [3.0])

    def test_candidate_rounding_is_nearest_even(self):
        slices = {z: np.array([[0, 1], [0, 1]], dtype=np.uint16) for z in (0, 1)}
        self.assertEqual(interpolate_candidate(slices, [.5, .5, .5], "standard-trilinear"), 0)
        for a in slices.values():
            a += 1
        self.assertEqual(interpolate_candidate(slices, [.5, .5, .5], "standard-trilinear"), 2)

    def test_candidate_invalid_inputs_fail_closed(self):
        slices = {z: np.ones((20, 20), dtype=np.uint16) for z in (0, 1)}
        for mapping in ([8, 8, .5, 0, 0, 0], [8, 8, .5, float('nan'), 0, 0]):
            with self.assertRaises(ValueError):
                sample_line(slices, mapping, 3.5, .5, 0, "standard-trilinear")
        for radius, interval in ((0, .5), (3.5, 0), (3.5, float('nan'))):
            with self.assertRaises(ValueError):
                sample_line(slices, [8, 8, .5, 1, 0, 0], radius, interval, 0, "standard-trilinear")
        for shift, mode in ((2, "standard-trilinear"), (0, "unknown")):
            with self.assertRaises(ValueError):
                sample_line(slices, [8, 8, .5, 1, 0, 0], 3.5, .5, shift, mode)


if __name__ == "__main__":
    unittest.main()
