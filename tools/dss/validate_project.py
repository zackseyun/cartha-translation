#!/usr/bin/env python3
"""Validate the DSS project registry, hashes, and rights boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "sources/dead_sea_scrolls/registry.v1.json"
COMPARATORS = ROOT / "sources/dead_sea_scrolls/comparison_witnesses.v1.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"FAIL: {message}")


def main() -> int:
    registry = json.loads(REGISTRY.read_text())
    comparators = json.loads(COMPARATORS.read_text())
    errors: list[str] = []
    allowed = set(registry["rights_policy"]["allowed_download_statuses"])
    blocked = set(registry["rights_policy"]["blocked_download_statuses"])

    record_ids: set[str] = set()
    image_ids: set[str] = set()
    for record in registry.get("records", []):
        record_id = record.get("id")
        if not record_id or record_id in record_ids:
            fail(f"missing or duplicate record id: {record_id!r}", errors)
        record_ids.add(record_id)
        for image in record.get("images", []):
            status = image.get("rights", {}).get("status")
            if status not in allowed | blocked:
                fail(f"{record_id}: unknown rights status {status!r}", errors)
            image_id = image.get("id")
            if image_id:
                if image_id in image_ids:
                    fail(f"duplicate image id {image_id}", errors)
                image_ids.add(image_id)
            downloads = image.get("downloads", {})
            if downloads and status in blocked:
                fail(f"{record_id}: blocked image exposes download configuration", errors)
            for quality, download in downloads.items():
                expected = download.get("sha256", "")
                if len(expected) != 64:
                    fail(f"{record_id}:{image_id}:{quality}: missing sha256", errors)
                path = ROOT / download["local_path"]
                if download.get("tracked") and not path.exists():
                    fail(f"{record_id}:{image_id}:{quality}: tracked file missing", errors)
                if path.exists() and sha256(path) != expected:
                    fail(f"{record_id}:{image_id}:{quality}: sha256 mismatch", errors)

    comparator_ids = [item.get("id") for item in comparators.get("witnesses", [])]
    if len(comparator_ids) != len(set(comparator_ids)):
        fail("comparison witness IDs are not unique", errors)
    if "wlc-oshb" not in comparator_ids or "lxx-old-greek" not in comparator_ids:
        fail("comparison registry must retain current Hebrew and Greek anchors", errors)

    if errors:
        print(f"DSS project validation failed with {len(errors)} error(s)")
        return 1
    print(
        f"DSS project validation passed: {len(record_ids)} records, "
        f"{len(image_ids)} downloadable images, {len(comparator_ids)} comparison witnesses"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
