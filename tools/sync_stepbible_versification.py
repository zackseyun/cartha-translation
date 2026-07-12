#!/usr/bin/env python3
"""Build a Hebrew/MT -> standard-English verse map from STEPBible TVTMS."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "sources" / "versification" / "hebrew_to_english.json"
SOURCE_URL = "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Versification/TVTMS%20-%20Translators%20Versification%20Traditions%20with%20Methodology%20for%20Standardisation%20for%20Eng%2BHeb%2BLat%2BGrk%2BOthers%20-%20STEPBible.org%20CC%20BY.txt"

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "cartha-versification-sync/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response: return response.read()

def parse_expanded(raw: bytes) -> dict[str, str]:
    mappings, conflicts, active = {}, {}, False
    for line in raw.decode("utf-8-sig").splitlines():
        if line.startswith("#DataStart(Expanded)"): active = True; continue
        if line.startswith("#DataEnd(Expanded)"): break
        if not active: continue
        fields = line.split("\t")
        if len(fields) < 3 or "Hebrew" not in fields[0]: continue
        source, standard = fields[1].strip(), fields[2].strip()
        if not source or not standard or any(mark in source for mark in ("!", "-")) or any(mark in standard for mark in (";", "-")): continue
        if source in mappings and mappings[source] != standard:
            conflicts.setdefault(source, {mappings[source]}).add(standard); continue
        mappings[source] = standard
    for source in conflicts: mappings.pop(source, None)
    return {k: v for k, v in sorted(mappings.items()) if k != v}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, default=OUTPUT)
    args = parser.parse_args()
    raw = args.source.read_bytes() if args.source else fetch(SOURCE_URL)
    mappings = parse_expanded(raw)
    # TVTMS separately lists the small NA/SBLG -> English/KJV NT set. POB's
    # integer-verse schema can safely represent these whole-verse mappings;
    # subverse-only cases remain quarantined by the alignment verifier.
    mappings.update({
        "2Co.13:13": "2Co.13:14",
        "Php.1:16": "Php.1:17",
        "Php.1:17": "Php.1:16",
        "Rev.12:18": "Rev.13:1",
        "Rev.13:1": "Rev.13:1",
    })
    payload = {"schema_version": 1, "source": "STEPBible TVTMS", "source_url": SOURCE_URL, "license": "CC BY 4.0", "source_sha256": hashlib.sha256(raw).hexdigest(), "mapping_direction": "POB source-tradition SourceRef to standard English StandardRef", "mappings": dict(sorted(mappings.items()))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(payload['mappings'])} changed mappings -> {args.output}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
