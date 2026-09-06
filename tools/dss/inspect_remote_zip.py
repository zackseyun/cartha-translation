#!/usr/bin/env python3
"""Bounded ZIP discovery/acquisition without downloading a multi-GB archive.

This verifies HTTP ranges and selected member CRCs, not the full archive hash,
the scientific meaning of a file, or permission to redistribute its contents.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import urllib.request
import zipfile
import zlib

MAX_RANGE = 32 * 1024 * 1024
STREAM_CHUNK = 4 * 1024 * 1024
MAX_MEMBER = 512 * 1024 * 1024


class RangeSource:
    def __init__(self, url: str, size: int):
        if not url.startswith("https://") or size < 22:
            raise ValueError("HTTPS URL and valid archive size required")
        self.url, self.size, self.etag = url, size, None
        self.receipts = []

    def read(self, start: int, length: int) -> bytes:
        if start < 0 or not 0 < length <= MAX_RANGE or start + length > self.size:
            raise ValueError("range outside bounded archive")
        headers = {"Range": f"bytes={start}-{start + length - 1}",
                   "Accept-Encoding": "identity", "User-Agent": "POB-restoration-research/1.0"}
        if self.etag:
            headers["If-Range"] = self.etag
        with urllib.request.urlopen(urllib.request.Request(self.url, headers=headers), timeout=30) as response:
            expected = f"bytes {start}-{start + length - 1}/{self.size}"
            if response.status != 206 or response.headers.get("Content-Range") != expected:
                raise ValueError("server did not return requested partial content")
            etag = response.headers.get("ETag")
            if not etag or etag.startswith("W/") or (self.etag and etag != self.etag):
                raise ValueError("missing, weak, or changed archive ETag")
            self.etag = etag
            data = response.read(length + 1)
            if len(data) != length:
                raise ValueError("partial content length mismatch")
        self.receipts.append({"start": start, "length": length,
                              "sha256": hashlib.sha256(data).hexdigest()})
        return data


def index_archive(source):
    tail_length = min(source.size, 65557)
    tail = source.read(source.size - tail_length, tail_length)
    offset = tail.rfind(b"PK\x05\x06")
    if offset < 0 or offset + 22 > len(tail):
        raise ValueError("missing ZIP end record")
    _, disk, cd_disk, disk_count, count, cd_size, cd_start, comment = struct.unpack_from("<4s4H2IH", tail, offset)
    if (disk or cd_disk or disk_count != count or count == 65535
            or cd_start == 0xFFFFFFFF or cd_size == 0xFFFFFFFF):
        raise ValueError("multi-disk/ZIP64 archive unsupported")
    if offset + 22 + comment != len(tail) or cd_start + cd_size != source.size - tail_length + offset:
        raise ValueError("inconsistent ZIP central directory bounds")
    central = source.read(cd_start, cd_size)
    with zipfile.ZipFile(io.BytesIO(central + tail[offset:])) as zf:
        entries = zf.infolist()
    if len(entries) != count or len({i.filename for i in entries}) != count:
        raise ValueError("duplicate names or directory count mismatch")
    # zipfile offsets refer to our shortened buffer; restore archive offsets.
    for info in entries:
        info.header_offset += cd_start
        if not 0 <= info.header_offset < cd_start:
            raise ValueError("member header outside archive body")
    return entries


def member_chunks(source, info, max_bytes=MAX_RANGE):
    if not 0 < max_bytes <= MAX_MEMBER:
        raise ValueError("invalid explicit member budget")
    if (info.is_dir() or info.flag_bits & 1 or not 0 <= info.file_size <= max_bytes
            or not 0 <= info.compress_size <= max_bytes):
        raise ValueError("directory, encrypted, or oversized member")
    header = source.read(info.header_offset, 30)
    values = struct.unpack("<4s5H3I2H", header)
    if values[0] != b"PK\x03\x04" or values[3] != info.compress_type:
        raise ValueError("local header mismatch")
    flags, name_length, extra_length = values[2], values[-2], values[-1]
    if flags != info.flag_bits:
        raise ValueError("local flags mismatch")
    name = source.read(info.header_offset + 30, name_length)
    if name.decode("utf-8" if flags & 0x800 else "cp437") != info.filename:
        raise ValueError("local filename mismatch")
    if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
        raise ValueError("unsupported compression")
    decoder = zlib.decompressobj(-15) if info.compress_type == zipfile.ZIP_DEFLATED else None
    start = info.header_offset + 30 + name_length + extra_length
    count, crc = 0, 0
    for offset in range(0, info.compress_size, STREAM_CHUNK):
        pending = source.read(start + offset, min(STREAM_CHUNK, info.compress_size - offset))
        while pending:
            if decoder:
                data = decoder.decompress(pending, min(STREAM_CHUNK, info.file_size - count + 1))
                pending = decoder.unconsumed_tail
                if decoder.unused_data:
                    raise ValueError("trailing deflate payload")
            else:
                data, pending = pending, b""
            count += len(data)
            if count > info.file_size:
                raise ValueError("oversized deflate payload")
            crc = zlib.crc32(data, crc)
            yield data
    if decoder and not decoder.eof:
        raise ValueError("incomplete deflate payload")
    if count != info.file_size or crc != info.CRC:
        raise ValueError("member length/CRC mismatch")


def read_member(source, info):
    return b"".join(member_chunks(source, info))


def write_member(source, info, destination, max_bytes=MAX_RANGE):
    """Publish a local payload only after full selected-member verification."""
    if destination.exists():
        raise ValueError("destination already exists")
    temporary = None
    digest = hashlib.sha256()
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix="payload-", delete=False) as out:
            temporary = Path(out.name)
            for chunk in member_chunks(source, info, max_bytes):
                out.write(chunk)
                digest.update(chunk)
        temporary.rename(destination)
        return digest.hexdigest()
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--size", required=True, type=int)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--member", action="append", default=[])
    parser.add_argument("--max-member-bytes", type=int, default=MAX_RANGE,
                        help="Explicit per-member compressed/decompressed ZIP budget, at most 512 MiB; nested gzip remains compressed")
    args = parser.parse_args()
    # A new directory prevents overwriting existing research/user artifacts.
    args.output_dir.mkdir(parents=True, exist_ok=False)
    source = RangeSource(args.url, args.size)
    entries = index_archive(source)
    indexed = {info.filename: info for info in entries}
    acquired = []
    for number, name in enumerate(args.member):
        info = indexed[name]
        filename = f"member-{number:02d}{Path(name).suffix}"
        digest = write_member(source, info, args.output_dir / filename, args.max_member_bytes)
        acquired.append({"archive_member": name, "local_file": filename,
                         "bytes": info.file_size, "crc32": f"{info.CRC:08x}",
                         "sha256": digest})
    receipt = {
        "schema_version": "1.0.0", "url": args.url, "archive_bytes": args.size,
        "etag": source.etag, "full_archive_hash_verified": False,
        "member_payloads_verified": acquired, "http_ranges": source.receipts,
        "entries": [{"name": i.filename, "bytes": i.file_size,
                     "compressed_bytes": i.compress_size, "crc32": f"{i.CRC:08x}",
                     "header_offset": i.header_offset, "directory": i.is_dir()} for i in entries],
    }
    (args.output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Indexed {len(entries)} entries; CRC-verified {len(acquired)} selected members. Full archive NOT verified.")


if __name__ == "__main__":
    main()
