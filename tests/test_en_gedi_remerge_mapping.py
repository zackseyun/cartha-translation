import gzip
import inspect
import io
from pathlib import Path
import tempfile
import unittest

from tools.textual_restoration import en_gedi_remerge_mapping as m


class RemergeMappingTests(unittest.TestCase):
    def test_frozen_protocol_and_acquisition_code(self):
        plan = m.load_plan()
        self.assertEqual(m.digest(m.ACQUISITION_TOOL_V1)[0], m.ACQUISITION_TOOL_V1_SHA)
        self.assertEqual(len(plan["points"]), 68)
        self.assertEqual(len(plan["members"]), 2)
        self.assertEqual(sum(e["bytes"] for e in plan["members"]), 237811326)
        self.assertEqual(sum(e["compressed_bytes"] for e in plan["members"]), 237731153)
        for p in plan["points"]:
            self.assertTrue(0 <= p["xy"][0] < 2400 and 0 <= p["xy"][1] < 4067)

    def test_ascii_cap_exact_boundary(self):
        stream = m.CappedText(io.StringIO("abc"), 3)
        self.assertEqual(stream.read(100), "abc")
        self.assertEqual(stream.read(100), "")
        self.assertEqual(stream.count, 3)

    def test_ascii_cap_exceeded(self):
        stream = m.CappedText(io.StringIO("abcd"), 3)
        with self.assertRaisesRegex(ValueError, "text cap"):
            stream.read(100)

    def test_readline_is_bounded(self):
        stream = m.CappedText(io.StringIO("x" * 20000), 30000)
        self.assertEqual(len(stream.readline()), 16385)

    def test_crlf_byte_count_regression(self):
        raw = gzip.compress(b"a\r\nb\r\n")
        with gzip.open(io.BytesIO(raw), "rt", encoding="ascii", newline="") as stream:
            bounded = m.CappedText(stream, 6)
            self.assertEqual(bounded.read(100), "a\r\nb\r\n")
            self.assertEqual(bounded.count, 6)
        with gzip.open(io.BytesIO(raw), "rt", encoding="ascii") as stream:
            self.assertEqual(len(stream.read()), 4)  # Original undercount demonstrated.
        self.assertIn('encoding="ascii", newline=""', inspect.getsource(m.build))

    def test_crlf_cap_fail_closed(self):
        raw = gzip.compress(b"a\r\nb\r\n")
        with gzip.open(io.BytesIO(raw), "rt", encoding="ascii", newline="") as stream:
            with self.assertRaisesRegex(ValueError, "text cap"):
                m.CappedText(stream, 4).read(100)

    def test_bare_cr_preserved(self):
        with gzip.open(io.BytesIO(gzip.compress(b"a\rb\r")), "rt", encoding="ascii", newline="") as stream:
            bounded = m.CappedText(stream, 4)
            self.assertEqual(bounded.readline(), "a\r")
            self.assertEqual(bounded.readline(), "b\r")
            self.assertEqual(bounded.count, 4)

    def test_non_ascii_rejected(self):
        with gzip.open(io.BytesIO(gzip.compress(b"\xff")), "rt", encoding="ascii", newline="") as stream:
            with self.assertRaises(UnicodeDecodeError):
                m.CappedText(stream, 4).read(100)

    def test_publish_preserves_existing_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "receipt.json"
            m.publish(path, {"value": 1})
            before = path.read_bytes()
            m.publish(path, {"value": 1})
            with self.assertRaisesRegex(ValueError, "overwrite"):
                m.publish(path, {"value": 2})
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
