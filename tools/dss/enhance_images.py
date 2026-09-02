#!/usr/bin/env python3
"""Create deterministic, non-generative transcription aids with provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "sources/dead_sea_scrolls/registry.v1.json"
OUTPUT = ROOT / "sources/dead_sea_scrolls/images/derived"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text())
    created = 0
    for record in registry["records"]:
        for image in record.get("images", []):
            preview = image.get("downloads", {}).get("preview")
            if not preview:
                continue
            source = ROOT / preview["local_path"]
            if not source.exists():
                raise FileNotFoundError(f"Run fetch_images.py first: {source}")
            with Image.open(source) as original:
                gray = ImageOps.grayscale(original)
                enhanced = ImageOps.autocontrast(gray, cutoff=(1, 1))
                enhanced = enhanced.filter(ImageFilter.MedianFilter(size=3))
                enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1.5, percent=160, threshold=3))
                out_dir = OUTPUT / image["id"]
                out_dir.mkdir(parents=True, exist_ok=True)
                output = out_dir / "transcription_contrast.png"
                enhanced.save(output, format="PNG", optimize=True)
            provenance = {
                "schema_version": "1.0.0",
                "method": "deterministic-non-generative",
                "warning": "Transcription aid only. No pixels or letters were generated; verify against the original.",
                "source_path": str(source.relative_to(ROOT)),
                "source_sha256": sha256(source),
                "output_path": str(output.relative_to(ROOT)),
                "output_sha256": sha256(output),
                "operations": [
                    {"name": "grayscale"},
                    {"name": "autocontrast", "cutoff_percent": [1, 1]},
                    {"name": "median_filter", "size": 3},
                    {"name": "unsharp_mask", "radius": 1.5, "percent": 160, "threshold": 3}
                ]
            }
            (out_dir / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
            print(output.relative_to(ROOT))
            created += 1
    print(f"Created {created} deterministic transcription aid(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
