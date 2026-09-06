"""Numerical and provenance checks; no ancient-letter accuracy claims."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from tools.textual_restoration import build_en_gedi_distant_rows as module


class Texture:
    def __init__(self, value):
        self.value = value

    def getpixel(self, point):
        return self.value


class DistantRowsTests(unittest.TestCase):
    def test_protocol_and_selection_are_frozen(self):
        raw = module.PROTOCOL.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), module.PROTOCOL_HASH)
        p = json.loads(raw)
        self.assertEqual(len(set(p['new_slice_numbers'])), 36)
        self.assertEqual(len(p['selected_texture_xy']), 6)
        self.assertEqual({x for x, y in p['selected_texture_xy']}, {984})
        self.assertLess(p['listed_compressed_bytes'], p['acquisition_cap_compressed_bytes'])
        self.assertLess(p['listed_uncompressed_bytes'], p['acquisition_cap_uncompressed_bytes'])
        self.assertTrue(all(value is False for value in p['policy'].values()))

    def prior(self):
        points = [{'texture_xy':[0,1], 'mask_value':255, 'xyz_normal':[2,2,2,0,0,1], 'spatial_group':'whole-height-grid'},
                  {'texture_xy':[0,2], 'mask_value':0, 'xyz_normal':[0,0,0,0,0,0], 'spatial_group':'acquisition-band'},
                  {'texture_xy':[0,3], 'mask_value':255, 'xyz_normal':[2,2,30,0,0,1], 'spatial_group':'whole-height-grid'}]
        return {'points':points, 'candidates':[{'radius_parameter':1.0, 'slice_index_offset':0,
                                               'interpolator':mode} for mode in ('standard-trilinear','historical-c10-corner')]}

    def test_evaluation_retains_missing_invalid_and_nonzero_errors(self):
        prior = self.prior()
        before = copy.deepcopy(prior)
        slices = {z:np.full((6,6),100,dtype=np.uint16) for z in range(1,5)}
        points, candidates, any_indices, common = module.evaluate(prior, slices, Texture(90), 0.5)
        self.assertEqual(prior, before)
        self.assertEqual(any_indices, [0])
        self.assertEqual(common, [0])
        for c in candidates:
            self.assertEqual([r['status'] for r in c['results']], ['evaluated','mask-invalid','unavailable-slices'])
            self.assertEqual(c['results'][0]['residual'],10)
            self.assertEqual(c['summary']['maximum_absolute_error'],10)
            self.assertFalse(c['summary']['observed_exact_match'])
            self.assertEqual(c['summary']['scope_status'],'incomplete')
            self.assertIsNone(c['by_spatial_group']['acquisition-band']['observed_exact_match'])
            self.assertNotIn('prediction',c['results'][2])

    def test_empty_coverage_is_not_pass(self):
        _, candidates, any_indices, common = module.evaluate(self.prior(), {}, Texture(0), 0.5)
        self.assertEqual(any_indices,[])
        self.assertEqual(common,[])
        for c in candidates:
            self.assertEqual(c['summary']['scope_status'],'incomplete')
            self.assertIsNone(c['summary']['observed_exact_match'])

    def test_corrupt_payload_is_rejected_before_image_decode(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'0381.tif'
            # Test fixture bytes, not image alteration or manuscript data.
            path.write_bytes(b'not an image')
            with self.assertRaisesRegex(ValueError,'hash/CRC/length'):
                module.checked_array(Path(temp),{'local_file':'0381.tif','bytes':12,'sha256':'0'*64,'crc32':'00000000'})
            with self.assertRaisesRegex(ValueError,'unsafe payload'):
                module.checked_array(Path(temp),{'local_file':'../0381.tif'})

    def test_saved_results_keep_all_targets_models_and_anchor_failures(self):
        r=json.loads((module.DISCOVERY/'en_gedi_distant_rows_check.v1.json').read_text())
        self.assertEqual(r['protocol_sha256'],module.PROTOCOL_HASH)
        self.assertEqual(r['implementation_sha256'],hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest())
        self.assertEqual(len(r['points']),288)
        self.assertEqual(len(r['candidates']),8)
        self.assertEqual(len(r['ct_slice_numbers']),42)
        for c in r['candidates']:
            self.assertEqual([v['point_index'] for v in c['results']],list(range(288)))
            evaluated=[v for v in c['results'] if v['status']=='evaluated']
            self.assertEqual(c['summary']['evaluable_count'],len(evaluated))
            for v in evaluated:
                self.assertEqual(v['residual'],v['prediction']-r['points'][v['point_index']]['published_texture_value'])
        for row in r['acquisition_anchor_results']:
            self.assertEqual([v['point_index'] for v in row['results']],r['protocol']['selected_point_indices'])
            self.assertTrue(all(v['status']=='evaluated' for v in row['results']))
        self.assertFalse(r['canonical_change_applied'])


if __name__=='__main__':
    unittest.main()
