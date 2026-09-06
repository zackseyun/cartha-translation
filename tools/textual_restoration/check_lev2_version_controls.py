#!/usr/bin/env python3
"""Verify bounded observations and POB bindings, not textual priority.

The private inputs are explicitly observation transcripts, not raw source pages.
No fetching, corpus redistribution, registry changes, or receipt regeneration.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "sources/textual_restoration/discovery/lev2_version_controls.v1.json"


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_local(record, root=ROOT):
    for relative, expected in record["local_file_sha256"].items():
        if sha256((root / relative).read_bytes()) != expected:
            raise ValueError(f"local file changed: {relative}")
    verse = yaml.safe_load((root / "translation/ot/leviticus/002/008.yaml").read_text())
    if verse["source"]["edition"] != "WLC":
        raise ValueError("source edition changed")
    text = verse["translation"]["text"]
    if not all(s in text for s in ("you shall bring", "he shall present it to the priest", "he shall bring it near")):
        raise ValueError("English agency changed")
    usfm = (root / "sources/ot/uwhb/03-LEV.usfm").read_text()
    target = usfm.split("\\c 2\n")[1].split("\\v 8\n")[1].split("\\v 9\n")[0]
    words = re.findall(r"\\w ([^|]+)\|([^\n]+?)\\w\*", target)
    for word, morph in (("והבאת", "He,C:Vhq2ms"), ("והקריבה", "He,C:Vhq3ms:Sp3fs"), ("והגישה", "He,C:Vhq3ms:Sp3fs")):
        hits = [a for s, a in words if "".join(re.findall("[א-ת]", s)) == word]
        if len(hits) != 1 or f'x-morph="{morph}"' not in hits[0]:
            raise ValueError(f"stored morphology changed: {word}")


def verify_private(record, directory):
    for source in record["source_observations"]:
        path = directory / source["snapshot_file"]
        raw = path.read_bytes()  # Missing input is an error, never a silent skip.
        if sha256(raw) != source["snapshot_sha256"]:
            raise ValueError(f"observation transcript changed: {path.name}")
        text = raw.decode("utf-8")
        if source["url"] not in text:
            raise ValueError("observation URL missing")
        for excerpt in source["required_excerpts"]:
            if excerpt not in text:
                raise ValueError(f"recorded observation missing: {excerpt}")
    return len(record["source_observations"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_directory", type=Path)
    args = parser.parse_args()
    record = json.loads(RECEIPT.read_text())
    verify_local(record)
    count = verify_private(record, args.private_directory)
    print(f"PASS: {len(record['local_file_sha256'])} local bindings and {count} private observation transcripts; no historical adjudication")


if __name__ == "__main__":
    main()
