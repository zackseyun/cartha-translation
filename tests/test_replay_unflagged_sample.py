import io
from pathlib import Path
import tarfile
import tempfile
import unittest

from tools.textual_restoration.replay_unflagged_sample import extract_regular, replay


def archive(entries):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as tar:
        for name, kind in entries:
            info = tarfile.TarInfo(name)
            info.type = kind
            if kind == tarfile.REGTYPE:
                info.size = 3
                tar.addfile(info, io.BytesIO(b"old"))
            else:
                info.linkname = "outside"
                tar.addfile(info)
    return buffer.getvalue()


class HistoricalReplayTests(unittest.TestCase):
    def test_regular_bytes_extracted_exactly(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            extract_regular(archive([("a/b.txt", tarfile.REGTYPE)]), root)
            self.assertEqual((root / "a/b.txt").read_bytes(), b"old")

    def test_reject_traversal_absolute_and_links_before_any_extraction(self):
        for bad, kind in [("../escape", tarfile.REGTYPE), ("/escape", tarfile.REGTYPE),
                          ("link", tarfile.SYMTYPE), ("hard", tarfile.LNKTYPE),
                          ("device", tarfile.CHRTYPE)]:
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as folder:
                with self.assertRaises(ValueError):
                    extract_regular(archive([("safe", tarfile.REGTYPE), (bad, kind)]), Path(folder))
                self.assertEqual(list(Path(folder).iterdir()), [])

    def test_duplicate_members_rejected(self):
        with tempfile.TemporaryDirectory() as folder, self.assertRaises(ValueError):
            extract_regular(archive([("a", tarfile.REGTYPE)] * 2), Path(folder))

    def test_mutable_refs_rejected(self):
        for ref in ["HEAD", "main", "574f204", "--help"]:
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                replay(commit=ref)


if __name__ == "__main__":
    unittest.main()
