#!/usr/bin/env python3
"""Bounded private acquisition and JSON-only measurement check; no image edits."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import zlib

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.dss.inspect_remote_zip import RangeSource, index_archive, write_member
from tools.textual_restoration.build_en_gedi_wider_renderer_check import build as wider_build, preflight, summarize
from tools.textual_restoration.build_en_gedi_renderer_probe import sample_line

DISCOVERY = ROOT / 'sources/textual_restoration/discovery'
PROTOCOL = DISCOVERY / 'en_gedi_distant_rows_protocol.v1.json'
PROTOCOL_HASH = '14b6f640f385370f34eec0342b20f32ab7879ac7d08ce77b1fcd5e390289eb5b'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_plan(directory):
    raw = PROTOCOL.read_bytes()
    if sha(raw) != PROTOCOL_HASH:
        raise ValueError('frozen acquisition protocol changed')
    plan = json.loads(raw)
    prior_raw = (ROOT / plan['prior_receipt']).read_bytes()
    index_raw = (directory / 'slice-index/receipt.json').read_bytes()
    if sha(prior_raw) != plan['prior_receipt_sha256'] or sha(index_raw) != plan['private_index_sha256']:
        raise ValueError('prior measurement or archive index drift')
    prior, index = json.loads(prior_raw), json.loads(index_raw)
    selected = []
    for y in sorted({p['texture_xy'][1] for p in prior['points'] if p['spatial_group'] == 'whole-height-grid'}):
        rows = [(i, p) for i, p in enumerate(prior['points']) if p['texture_xy'][1] == y and p['mask_value'] == 255]
        if rows:
            selected.append(min(rows, key=lambda ip: (abs(ip[1]['texture_xy'][0] - 984), ip[1]['texture_xy'][0]))[0])
    needed = sorted({z for i in selected for c in prior['candidates'] for z in c['results'][i].get('missing_slice_numbers', [])})
    if (selected != plan['selected_point_indices'] or needed != plan['new_slice_numbers']
            or [prior['points'][i]['texture_xy'] for i in selected] != plan['selected_texture_xy']):
        raise ValueError('geometry-selected acquisition did not reproduce')
    indexed = {e['name']: e for e in index['entries']}
    names = [f'slices/{z:04d}.tif' for z in needed]
    entries = [indexed[name] for name in names]
    compressed, expanded = sum(e['compressed_bytes'] for e in entries), sum(e['bytes'] for e in entries)
    if (len(entries) != plan['member_count'] or compressed != plan['listed_compressed_bytes']
            or expanded != plan['listed_uncompressed_bytes']
            or compressed > plan['acquisition_cap_compressed_bytes']
            or expanded > plan['acquisition_cap_uncompressed_bytes']):
        raise ValueError('acquisition budget or index mismatch')
    return plan, prior, entries


def acquire(directory, destination):
    plan, _, entries = load_plan(directory)
    destination = destination.resolve()
    if destination.is_relative_to(ROOT) or destination.exists():
        raise ValueError('use a new private output directory outside repository')
    source = RangeSource(plan['archive_url'], plan['archive_bytes'])
    source.etag = plan['archive_etag']
    current = {i.filename: i for i in index_archive(source)}
    for entry in entries:
        info = current[entry['name']]
        if (info.file_size != entry['bytes'] or info.compress_size != entry['compressed_bytes']
                or info.CRC != int(entry['crc32'], 16) or info.header_offset != entry['header_offset']):
            raise ValueError('fresh selected ZIP entry differs from pinned index')
    destination.mkdir(parents=True, exist_ok=False)
    payloads = []
    for entry in entries:
        info = current[entry['name']]
        local = Path(info.filename).name
        digest = write_member(source, info, destination / local)
        payloads.append({'archive_member': info.filename, 'local_file': local,
                         'bytes': info.file_size, 'compressed_bytes': info.compress_size,
                         'crc32': f'{info.CRC:08x}', 'sha256': digest})
        print(f'Verified {len(payloads)}/{len(entries)}: {info.filename}', flush=True)
    receipt = {'protocol_sha256': PROTOCOL_HASH, 'url': source.url, 'archive_bytes': source.size,
               'etag': source.etag, 'full_archive_hash_verified': False,
               'member_payloads_verified': payloads, 'http_ranges': source.receipts}
    (destination / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt


def checked_array(folder, member):
    name = member['local_file']
    if Path(name).name != name or (folder / name).is_symlink():
        raise ValueError('unsafe payload path')
    path = folder / name
    raw = path.read_bytes()
    if (len(raw) != member['bytes'] or sha(raw) != member['sha256']
            or f'{zlib.crc32(raw):08x}' != member['crc32']):
        raise ValueError('payload hash/CRC/length mismatch')
    with Image.open(path) as im:
        array = np.asarray(im).copy()
    if array.shape != (1400, 1400) or array.dtype != np.uint16:
        raise ValueError('CT shape/type mismatch')
    return array


def evaluate(prior, slices, texture, interval):
    """All old targets and models retained; no parameters selected from results."""
    points = copy.deepcopy(prior['points'])
    candidates = []
    for old in prior['candidates']:
        candidate = {key: old[key] for key in ('radius_parameter', 'slice_index_offset', 'interpolator')}
        candidate['results'] = []
        for i, row in enumerate(points):
            available = ({'status': 'mask-invalid'} if row['mask_value'] != 255 else
                         preflight(row['xyz_normal'], candidate['radius_parameter'], candidate['slice_index_offset'], interval, set(slices)))
            candidate['results'].append({'point_index': i, **available})
        candidates.append(candidate)
    # Availability is complete before any newly available target is inspected.
    any_indices = {r['point_index'] for c in candidates for r in c['results'] if r['status'] == 'evaluable'}
    common = set.intersection(*[{r['point_index'] for r in c['results'] if r['status'] == 'evaluable'} for c in candidates])
    for i in sorted(any_indices):
        points[i]['published_texture_value'] = int(texture.getpixel(tuple(points[i]['texture_xy'])))
    for c in candidates:
        for r in c['results']:
            if r['status'] != 'evaluable':
                continue
            point = points[r['point_index']]
            prediction = sample_line(slices, point['xyz_normal'], c['radius_parameter'], interval, c['slice_index_offset'], c['interpolator'])
            r.update(prediction)
            r['status'] = 'evaluated'
            r['residual'] = prediction['prediction'] - point['published_texture_value']
        c['summary'] = summarize(c['results'])
        c['by_spatial_group'] = {g: summarize([r for r in c['results'] if points[r['point_index']]['spatial_group'] == g]) for g in ('whole-height-grid', 'acquisition-band')}
        c['by_texture_row'] = {str(y): summarize([r for r in c['results'] if points[r['point_index']]['texture_xy'][1] == y]) for y in sorted({p['texture_xy'][1] for p in points})}
        c['common_coverage_summary'] = summarize([r for r in c['results'] if r['point_index'] in common])
    return points, candidates, sorted(any_indices), sorted(common)


def build(directory, acquired_dir):
    plan, prior, expected = load_plan(directory)
    if wider_build(directory) != prior:
        raise ValueError('frozen wider receipt failed actual-input reproduction')
    raw = (acquired_dir / 'receipt.json').read_bytes()
    receipt = json.loads(raw)
    if (receipt['protocol_sha256'] != PROTOCOL_HASH or receipt['url'] != plan['archive_url']
            or receipt['archive_bytes'] != plan['archive_bytes'] or receipt['etag'] != plan['archive_etag']
            or receipt['full_archive_hash_verified'] is not False):
        raise ValueError('acquisition provenance mismatch')
    payloads = receipt['member_payloads_verified']
    if [m['archive_member'] for m in payloads] != [e['name'] for e in expected]:
        raise ValueError('missing/extra/duplicate acquired member')
    slices = {}
    for audit in ('ct-probe-audit', 'renderer-ct-audit'):
        older = json.loads((directory / audit / 'receipt.json').read_text())
        for member in older['member_payloads_verified']:
            if member['archive_member'].endswith('.tif'):
                slices[int(Path(member['archive_member']).stem)] = checked_array(directory / audit, member)
    for member, entry in zip(payloads, expected):
        if any(member[k] != entry[j] for k, j in (('bytes','bytes'), ('compressed_bytes','compressed_bytes'), ('crc32','crc32'))):
            raise ValueError('acquired payload does not match pinned ZIP entry')
        number = int(Path(member['archive_member']).stem)
        if number in slices:
            raise ValueError('duplicate CT slice')
        slices[number] = checked_array(acquired_dir, member)
    with Image.open(directory / 'segment-audit/member-02.png') as texture:
        old_protocol = json.loads((DISCOVERY / 'en_gedi_renderer_probe.v1.json').read_text())['protocol']
        points, candidates, any_indices, common = evaluate(prior, slices, texture, old_protocol['sampling_interval_voxels'])
    return {'schema_version':'1.0.0', 'checked_date':'2026-09-05', 'protocol':plan, 'protocol_sha256':PROTOCOL_HASH,
            'implementation_sha256':sha(Path(__file__).read_bytes()), 'prior_receipt_reproduced':True,
            'acquisition_receipt_sha256':sha(raw), 'acquisition':receipt,
            'points':points, 'candidates':candidates, 'ct_slice_numbers':sorted(slices),
            'evaluable_any_candidate_indices':any_indices, 'common_coverage_point_indices':common,
            'acquisition_anchor_results':[{k:c[k] for k in ('radius_parameter','slice_index_offset','interpolator')} | {'results':[c['results'][i] for i in plan['selected_point_indices']]} for c in candidates],
            'policy':plan['policy'], 'canonical_change_applied':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    parser.add_argument('acquired', type=Path)
    parser.add_argument('--acquire', action='store_true')
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--write', action='store_true', help='Write only the fixed generated numerical receipt; never overwrite differing evidence')
    args = parser.parse_args()
    if sum((args.acquire, args.verify_only, args.write)) > 1:
        parser.error('acquire, verify-only and write are exclusive')
    if args.acquire:
        acquire(args.original, args.acquired)
    else:
        result = build(args.original, args.acquired)
        if args.verify_only:
            if result != json.loads((DISCOVERY / 'en_gedi_distant_rows_check.v1.json').read_text()):
                raise ValueError('saved expanded receipt differs from actual-input result')
            print('Verified expanded and frozen wider receipts against actual inputs.')
        elif args.write:
            output = DISCOVERY / 'en_gedi_distant_rows_check.v1.json'
            raw = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
            if output.is_symlink() or (output.exists() and output.read_text() != raw):
                raise ValueError('refuse to overwrite different frozen result')
            if not output.exists():
                with output.open('x') as stream:
                    stream.write(raw)
            print(json.dumps({'receipt_sha256':sha(output.read_bytes()), 'ct_slices':len(result['ct_slice_numbers']),
                              'candidates':[{k:c[k] for k in ('radius_parameter','slice_index_offset','interpolator','summary')} for c in result['candidates']]}, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
