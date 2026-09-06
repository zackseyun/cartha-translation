import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from tools.textual_restoration import acquire_en_gedi_textures as a
from tools.textual_restoration import check_en_gedi_textures as c


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(a.PROTOCOL.read_text())

    def test_actual_plan_totals(self):
        a.validate_plan(self.plan)
        self.assertEqual(sum(m["bytes"] for m in self.plan["members"]), 62316462)
        self.assertEqual(sum(m["compressed_bytes"] for m in self.plan["members"]), 62301068)

    def test_selection_and_paths(self):
        for key, value in (("name", "segmentations/merge5/textured.png"),
                           ("local_file", "../payload.png")):
            plan = copy.deepcopy(self.plan)
            plan["members"][0][key] = value
            with self.assertRaises(ValueError):
                a.validate_plan(plan)

    def test_member_and_batch_budgets(self):
        for key, value in (("per_member_budget_bytes", 100),
                           ("batch_compressed_budget_bytes", 10),
                           ("batch_expanded_budget_bytes", 10)):
            plan = copy.deepcopy(self.plan)
            plan[key] = value
            with self.assertRaises(ValueError):
                a.validate_plan(plan)

    def test_weak_etag(self):
        self.plan["etag"] = 'W/"weak"'
        with self.assertRaises(ValueError):
            a.validate_plan(self.plan)

    def test_fresh_index_drift(self):
        entries = []
        for m in self.plan["members"]:
            i = zipfile.ZipInfo(m["name"])
            i.file_size, i.compress_size = m["bytes"], m["compressed_bytes"]
            i.CRC, i.header_offset = int(m["crc32"], 16), m["header_offset"]
            entries.append(i)
        self.assertEqual(len(a.match_index(self.plan, entries)), 6)
        entries[3].CRC += 1
        with self.assertRaises(ValueError):
            a.match_index(self.plan, entries)


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        plan = json.loads(a.PROTOCOL.read_text())
        receipt = json.loads(c.RECEIPT.read_text())
        self.triage = json.loads(c.TRIAGE.read_text())
        png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + struct.pack(">II", 2, 3)
        for m, actual in zip(plan["members"], receipt["members"]):
            m["bytes"] = m["compressed_bytes"] = len(png)
            actual.update(m)
            actual["sha256"] = hashlib.sha256(png).hexdigest()
            actual["size_xy"] = [2, 3]
            (self.root / m["local_file"]).write_bytes(png)
        self.protocol_path = self.root / "protocol.json"
        self.protocol_path.write_text(json.dumps(plan))
        receipt["protocol_sha256"] = a.sha(self.protocol_path)
        self.public_path = self.root / "public.json"
        self.public_path.write_text(json.dumps(receipt))
        self.private_path = self.root / "receipt.json"
        self.private_path.write_text(json.dumps(receipt))
        self.triage_path = self.root / "triage.json"
        self.triage_path.write_text(json.dumps(self.triage))
        for target, value in (("PROTOCOL", self.protocol_path),):
            p = patch.object(a, target, value)
            p.start()
            self.addCleanup(p.stop)
        for target, value in (("RECEIPT", self.public_path), ("TRIAGE", self.triage_path)):
            p = patch.object(c, target, value)
            p.start()
            self.addCleanup(p.stop)

    def test_fixture_pass_is_not_reading_pass(self):
        result = c.check(self.root)
        self.assertEqual(result["members_verified"], 6)
        self.assertFalse(result["scientific_reading_pass"])

    def test_missing_payload(self):
        (self.root / "merge0.png").unlink()
        with self.assertRaises(FileNotFoundError):
            c.check(self.root)

    def test_changed_payload(self):
        path = self.root / "merge1.png"
        path.write_bytes(path.read_bytes()[:-1] + b"x")
        with self.assertRaisesRegex(ValueError, "payload hash drift"):
            c.check(self.root)

    def test_receipt_and_protocol_drift(self):
        self.private_path.write_text("{}")
        with self.assertRaisesRegex(ValueError, "receipt drift"):
            c.check(self.root)
        self.private_path.write_bytes(self.public_path.read_bytes())
        self.protocol_path.write_text(self.protocol_path.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "protocol drift"):
            c.check(self.root)

    def test_scope_and_label_rejections(self):
        for key in ("blind_evaluation", "scientific_reading_pass", "new_transcription", "canonical_change"):
            triage = copy.deepcopy(self.triage)
            triage[key] = True
            self.triage_path.write_text(json.dumps(triage))
            with self.assertRaisesRegex(ValueError, "scope drift"):
                c.check(self.root)
        triage = copy.deepcopy(self.triage)
        triage["observations"][0]["accepted_verse_locator"] = "Lev 1:1"
        self.triage_path.write_text(json.dumps(triage))
        with self.assertRaisesRegex(ValueError, "unreviewed labels"):
            c.check(self.root)


if __name__ == "__main__":
    unittest.main()
