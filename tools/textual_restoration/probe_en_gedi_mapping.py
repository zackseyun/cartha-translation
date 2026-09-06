#!/usr/bin/env python3
"""Read bounded coordinate samples from the legacy En-Gedi OpenCV YAML map.

Read-only scientific data inspection; does not edit or reconstruct an image.
Requires NumPy and Pillow. Parse the complete gzip stream to verify its end/CRC
and scalar count, but retain only requested points, not the entire matrix.
"""
import argparse
import gzip
import json
from pathlib import Path
import re

import numpy as np
from PIL import Image


def trilinear(slices, xyz):
    """Interpolate recorded voxels only; missing/out-of-volume data is an error."""
    if len(xyz) != 3 or not np.isfinite(xyz).all():
        raise ValueError("invalid volume coordinate")
    x, y, z = map(float, xyz)
    x0, y0, z0 = map(int, np.floor([x, y, z]))
    if x0 < 0 or y0 < 0 or z0 < 0 or z0 not in slices or z0 + 1 not in slices:
        raise ValueError("unavailable volume neighborhood")
    a, b = slices[z0], slices[z0 + 1]
    if a.shape != b.shape or a.ndim != 2 or y0 + 1 >= a.shape[0] or x0 + 1 >= a.shape[1]:
        raise ValueError("outside or inconsistent slice dimensions")
    dx, dy, dz = x - x0, y - y0, z - z0
    value = 0.0
    for iz, wz in ((0, 1 - dz), (1, dz)):
        for iy, wy in ((0, 1 - dy), (1, dy)):
            for ix, wx in ((0, 1 - dx), (1, dx)):
                value += float(slices[z0 + iz][y0 + iy, x0 + ix]) * wz * wy * wx
    return value


def sample_map(stream, points, chunk_size=1024 * 1024):
    header = ""
    while "data: [" not in header:
        line = stream.readline()
        if not line or len(header) + len(line) > 16384:
            raise ValueError("invalid/big mapping header")
        header += line
    prefix, pending = header.split("data: [", 1)
    if not prefix.startswith("%YAML:1.0\nPerPixelMapping: !!opencv-matrix\n"):
        raise ValueError("unsupported mapping header")
    rows = int(re.search(r"rows:\s*(\d+)", prefix)[1])
    cols = int(re.search(r"cols:\s*(\d+)", prefix)[1])
    if not re.search(r'dt:\s*"6d"', prefix) or not 0 < rows * cols <= 20_000_000:
        raise ValueError("unsupported mapping dimensions/type")
    targets = {}
    for x, y in points:
        if not 0 <= x < cols or not 0 <= y < rows:
            raise ValueError("sample outside mapping")
        targets[(x, y)] = (y * cols + x) * 6
    sampled = {p: [] for p in targets}
    count, closed = 0, False
    while True:
        chunk = stream.read(chunk_size)
        pending += chunk
        if not chunk:
            if not pending.rstrip().endswith("]"):
                raise ValueError("mapping closing bracket missing")
            body = pending.rstrip()[:-1]
            closed = True
        else:
            cut = pending.rfind(",")
            if cut < 0:
                if len(pending) > chunk_size * 2:
                    raise ValueError("oversized mapping token")
                continue
            body, pending = pending[:cut], pending[cut + 1:]
        if body.strip():
            if not re.fullmatch(r"[0-9eE+.,\s-]+", body):
                raise ValueError("unexpected mapping token")
            values = np.fromstring(body, sep=",")
            if len(values) != body.count(",") + 1 or not np.isfinite(values).all():
                raise ValueError("malformed/nonfinite mapping values")
            for point, start in targets.items():
                lo, hi = max(start, count), min(start + 6, count + len(values))
                if lo < hi:
                    sampled[point].extend(values[lo - count:hi - count].tolist())
            count += len(values)
            if count > rows * cols * 6:
                raise ValueError("too many mapping values")
        if closed:
            break
    if count != rows * cols * 6 or any(len(v) != 6 for v in sampled.values()):
        raise ValueError("mapping scalar count mismatch")
    return rows, cols, count, sampled


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("--point", action="append", required=True, help="x,y in unmodified segment texture")
    args = parser.parse_args()
    points = [tuple(map(int, p.split(","))) for p in args.point]
    with gzip.open(args.mapping, "rt", encoding="ascii") as stream:
        rows, cols, count, samples = sample_map(stream, points)
    with Image.open(args.mask) as mask:
        if mask.size != (cols, rows) or mask.mode != "L":
            raise ValueError("mask shape/type mismatch")
        data = [{"texture_xy": list(p), "mask_value": mask.getpixel(p),
                 "xyz_normal": v} for p, v in samples.items()]
    print(json.dumps({"rows": rows, "cols": cols, "scalar_count": count,
                      "samples": data, "historical_reading_claimed": False}, indent=2))


if __name__ == "__main__":
    main()
