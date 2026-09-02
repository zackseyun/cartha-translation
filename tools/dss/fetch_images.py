#!/usr/bin/env python3
"""Rights-gated, hash-verified image retrieval for the DSS registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "sources/dead_sea_scrolls/registry.v1.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_downloads(registry: dict, quality: str):
    allowed = set(registry["rights_policy"]["allowed_download_statuses"])
    for record in registry["records"]:
        for image in record.get("images", []):
            rights = image.get("rights", {})
            downloads = image.get("downloads", {})
            if quality not in downloads:
                continue
            yield record, image, downloads[quality], rights.get("status") in allowed


def fetch(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "POB-DSS-research/1.0"})
    fd, temporary = tempfile.mkstemp(prefix=destination.name + ".", dir=destination.parent)
    os.close(fd)
    temp_path = Path(temporary)
    try:
        with urllib.request.urlopen(request, timeout=120) as response, temp_path.open("wb") as out:
            while chunk := response.read(1024 * 1024):
                out.write(chunk)
        temp_path.replace(destination)
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--quality", choices=("preview", "master"), default="preview")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    registry = json.loads(args.registry.read_text())
    failures = 0
    count = 0
    for record, image, download, is_allowed in iter_downloads(registry, args.quality):
        label = f"{record['id']}:{image['id']}:{args.quality}"
        destination = ROOT / download["local_path"]
        if not is_allowed:
            print(f"BLOCKED {label}: rights status {image['rights'].get('status')!r}")
            failures += 1
            continue
        if args.force or not destination.exists():
            print(f"FETCH   {label} -> {destination.relative_to(ROOT)}")
            fetch(download["url"], destination)
        actual = sha256(destination)
        if actual != download["sha256"]:
            print(f"FAIL    {label}: sha256 {actual} != {download['sha256']}")
            failures += 1
            continue
        print(f"OK      {label}: {actual}")
        count += 1
    print(f"Verified {count} {args.quality} image(s); failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
