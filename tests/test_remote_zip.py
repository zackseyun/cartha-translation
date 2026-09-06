import io
import struct
import tempfile
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch
import zipfile

from tools.dss.inspect_remote_zip import index_archive, read_member, write_member, MAX_RANGE, RangeSource


class MemorySource:
    def __init__(self, data):
        self.data, self.size = data, len(data)

    def read(self, start, length):
        if start < 0 or length > MAX_RANGE or start + length > self.size:
            raise ValueError("range outside bounded archive")
        return self.data[start:start + length]


def fixture():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("segment/", b"")
        archive.writestr("segment/mesh.obj", b"v 1 2 3\n")
        archive.writestr("segment/mask.png", b"fixture, not a real image")
    return MemorySource(buffer.getvalue())


class RemoteZipTests(unittest.TestCase):
    def response(self, status=206, etag='"pinned"', content_range="bytes 0-2/30"):
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = status
        response.headers = {"ETag": etag, "Content-Range": content_range}
        response.read.return_value = b"abc"
        return response

    def test_range_response_must_be_partial_and_exact(self):
        source = RangeSource("https://example.org/archive.zip", 30)
        for response in (self.response(status=200), self.response(content_range="bytes 1-3/30")):
            with patch("urllib.request.urlopen", return_value=response):
                with self.assertRaisesRegex(ValueError, "partial content"):
                    source.read(0, 3)

    def test_changed_archive_or_weak_etag_rejected(self):
        source = RangeSource("https://example.org/archive.zip", 30)
        with patch("urllib.request.urlopen", return_value=self.response()):
            self.assertEqual(source.read(0, 3), b"abc")
        for etag in ('"changed"', 'W/"pinned"', None):
            with patch("urllib.request.urlopen", return_value=self.response(etag=etag)):
                with self.assertRaisesRegex(ValueError, "ETag"):
                    source.read(0, 3)

    def test_out_of_bounds_rejected_before_network(self):
        source = RangeSource("https://example.org/archive.zip", 30)
        with patch("urllib.request.urlopen") as network:
            with self.assertRaises(ValueError):
                source.read(0, MAX_RANGE + 1)
            with self.assertRaises(ValueError):
                source.read(29, 2)
            network.assert_not_called()

    def test_index_and_selected_payload(self):
        source = fixture()
        entries = index_archive(source)
        self.assertEqual(len(entries), 3)
        self.assertEqual(read_member(source, entries[1]), b"v 1 2 3\n")

    def test_directory_and_oversized_rejected(self):
        source = fixture()
        entries = index_archive(source)
        with self.assertRaises(ValueError):
            read_member(source, entries[0])
        entries[1].file_size = MAX_RANGE + 1
        with self.assertRaises(ValueError):
            read_member(source, entries[1])

    def test_bad_crc_rejected(self):
        source = fixture()
        info = index_archive(source)[1]
        info.CRC ^= 1
        with self.assertRaisesRegex(ValueError, "CRC"):
            read_member(source, info)

    def test_local_header_name_must_match(self):
        source = fixture()
        info = index_archive(source)[1]
        info.filename = "different.obj"
        with self.assertRaisesRegex(ValueError, "filename"):
            read_member(source, info)

    def test_directory_bounds_must_match(self):
        source = fixture()
        data = bytearray(source.data)
        struct.pack_into("<I", data, len(data) - 6, 1)
        with self.assertRaisesRegex(ValueError, "bounds"):
            index_archive(MemorySource(bytes(data)))

    def test_streaming_is_chunk_independent_and_crc_gated(self):
        source = fixture()
        info = index_archive(source)[1]
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "mesh.obj"
            with patch("tools.dss.inspect_remote_zip.STREAM_CHUNK", 2):
                write_member(source, info, destination, 100)
            self.assertEqual(destination.read_bytes(), b"v 1 2 3\n")
            with self.assertRaisesRegex(ValueError, "already exists"):
                write_member(source, info, destination)
            info.CRC ^= 1
            failed = Path(directory) / "bad.obj"
            with self.assertRaisesRegex(ValueError, "CRC"):
                write_member(source, info, failed)
            self.assertFalse(failed.exists())
            self.assertEqual(list(Path(directory).iterdir()), [destination])


if __name__ == "__main__":
    unittest.main()
