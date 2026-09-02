#!/usr/bin/env python3
"""Fetch a pinned CC-BY SBLGNT apparatus release; never replace the POB base text."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "sources/nt/sblgnt_apparatus"
SHA = "c4d241a9c1c479a55b989ba35a4976c1d0b8052c"
REPO = "Faithlife/SBLGNT"
BOOKS = "Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev".split()
FILES = {f"data/sblgntapp/xml/{book}.xml": f"xml/{book}.xml" for book in BOOKS}
FILES.update({"LICENSE": "LICENSE", "README.md": "UPSTREAM_README.md", "About.md": "UPSTREAM_ABOUT.md"})


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(item: tuple[str, str]) -> dict:
    upstream, local = item
    url = f"https://raw.githubusercontent.com/{REPO}/{SHA}/{upstream}"
    req = urllib.request.Request(url, headers={"User-Agent": "POB-textual-research"})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError(f"Oversize source: {upstream}")
    if upstream == "README.md" and b"Creative Commons Attribution 4.0" not in data:
        raise ValueError("Pinned publisher license declaration not found")
    path = DEST / local
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {"path": local, "upstream_path": upstream, "url": url,
            "bytes": len(data), "sha256": digest(data), "modified": False}


def verify() -> dict:
    manifest = json.loads((DEST / "manifest.json").read_text())
    if manifest["commit"] != SHA or manifest["license"] != "CC-BY-4.0":
        raise ValueError("Unrecognized pinned source or license")
    if {x["path"] for x in manifest["files"]} != set(FILES.values()):
        raise ValueError("Incomplete apparatus source set")
    for file in manifest["files"]:
        data = (DEST / file["path"]).read_bytes()
        if digest(data) != file["sha256"] or len(data) != file["bytes"]:
            raise ValueError(f"Source hash/size mismatch: {file['path']}")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if not args.verify_only:
        # Retrieve the licensing declaration before the apparatus itself.
        first = fetch(("README.md", FILES["README.md"]))
        with ThreadPoolExecutor(max_workers=6) as pool:
            files = [first] + list(pool.map(fetch, [(k, v) for k, v in FILES.items() if k != "README.md"]))
        manifest = {"schema_version": "1.0.0", "repository": f"https://github.com/{REPO}",
                    "commit": SHA, "license": "CC-BY-4.0",
                    "attribution": "SBL Greek New Testament, edited by Michael W. Holmes. Copyright 2010 Society of Biblical Literature and Logos Bible Software.",
                    "evidence_type": "critical-edition-comparison-not-manuscript-collation",
                    "files": sorted(files, key=lambda x: x["path"])}
        (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    manifest = verify()
    print(f"Verified {len(manifest['files'])} pinned files, {sum(f['bytes'] for f in manifest['files']):,} bytes; {len(BOOKS)} NT apparatus books.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
