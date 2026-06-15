#!/usr/bin/env python3
"""renumber_psalm_superscriptions.py

Fix psalm verse numbering so it matches the English Bible convention:
superscriptions are headers (verse 0), not verse 1.

Two error patterns exist in the drafted files:

  STANDALONE — verse 001 is entirely a superscription, no content:
    001.yaml: "For the choir director. A psalm of David."     ← pure header
    002.yaml: "Blessed is the one who considers the poor…"   ← actual v1

  FUSED — verse 001 has the superscription prefix fused with the first
  content sentence (the draft model didn't separate them):
    001.yaml: "A psalm of David. Yahweh is my shepherd; I will not lack."

Fix applied:
  STANDALONE:  rename 001 → 000, 002 → 001, 003 → 002, etc.
  FUSED:       split verse 001 text; create 000.yaml (superscription part),
               rewrite 001.yaml (content part only).

Run:
  python3 tools/renumber_psalm_superscriptions.py --dry-run   # list only
  python3 tools/renumber_psalm_superscriptions.py             # apply
  python3 tools/renumber_psalm_superscriptions.py --psalm 41  # one psalm
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from ruamel.yaml import YAML

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PSALMS_DIR = REPO_ROOT / "translation" / "ot" / "psalms"

# ── Content detection ──────────────────────────────────────────────────────
from psalm_numbering import classify_verse1, is_superscription, split_fused

def _update_fields(data: dict, new_verse: int) -> None:
    """Update id, reference, and verse-number fields to new_verse."""
    id_val = str(data.get("id") or "")
    new_id = re.sub(r"(\bPSA\.\d+\.)(\d+)$", lambda m: f"{m.group(1)}{new_verse}", id_val, flags=re.I)
    if new_id != id_val:
        data["id"] = new_id
    ref_val = str(data.get("reference") or "")
    new_ref = re.sub(r"(\bPsalms\s+\d+:)(\d+)\b", lambda m: f"{m.group(1)}{new_verse}", ref_val)
    if new_ref != ref_val:
        data["reference"] = new_ref


def process_psalm(psalm_dir: pathlib.Path, dry_run: bool, yaml: YAML
                  ) -> tuple[str, str] | None:
    """Return (psalm_num, type) if action taken, else None."""
    v1_path = psalm_dir / "001.yaml"
    if not v1_path.exists():
        return None

    raw = v1_path.read_text(encoding="utf-8")
    data = yaml.load(raw)
    if not isinstance(data, dict):
        return None

    tr = data.get("translation") or {}
    v1_text = (tr.get("text") or "").strip()
    kind = classify_verse1(v1_text)
    psalm_num = psalm_dir.name

    if kind == "content":
        return None

    if dry_run:
        preview = v1_text[:70]
        print(f"  Ps {psalm_num} [{kind}]: \"{preview}\"")
        return psalm_num, kind

    if kind == "standalone":
        # Rename 001 → 000, 002 → 001, etc.
        #
        # Some historical runs already created 000.yaml but left the original
        # superscription behind as 001.yaml. In that partially-normalized state
        # 000.yaml is the canonical header, so only remove the duplicate 001 and
        # shift 002+ down by one. Never include 000.yaml in the shift set or it
        # would become -01.yaml.
        existing_v0 = psalm_dir / "000.yaml"
        if existing_v0.exists():
            v1_path.unlink()
            verse_files = sorted(
                (p for p in psalm_dir.glob("*.yaml") if p.stem.isdigit() and int(p.stem) >= 2),
                key=lambda p: int(p.stem),
            )
        else:
            verse_files = sorted(
                (p for p in psalm_dir.glob("*.yaml") if p.stem.isdigit() and int(p.stem) >= 1),
                key=lambda p: int(p.stem),
            )

        # Ascending order is safe because each target slot was just vacated by
        # the previous step (or, for partial-normalization repair, by deleting
        # the duplicate 001.yaml first).
        for vf in verse_files:
            old_num = int(vf.stem)
            new_num = old_num - 1
            vdata = yaml.load(vf.read_text(encoding="utf-8"))
            _update_fields(vdata, new_num)
            if new_num == 0:
                vdata["is_superscription"] = True
            new_path = psalm_dir / f"{new_num:03d}.yaml"
            with new_path.open("w", encoding="utf-8") as fh:
                yaml.dump(vdata, fh)
            vf.unlink()

    elif kind == "fused":
        super_text, content_text = split_fused(v1_text)
        if not super_text or not content_text:
            # Splitting failed — leave for manual review
            print(f"  [SKIP Ps {psalm_num}] split failed: super={repr(super_text[:40])}, "
                  f"content={repr(content_text[:40])}", file=sys.stderr)
            return None

        # Create verse 000 (superscription only)
        super_data = yaml.load(raw)  # copy of v1 as base
        super_data["is_superscription"] = True
        super_data.setdefault("translation", {})["text"] = super_text
        _update_fields(super_data, 0)
        # Remove fields that belong to the content verse only
        for k in ("lexical_decisions", "theological_decisions", "ai_draft", "revision_pass"):
            super_data.pop(k, None)
        v0_path = psalm_dir / "000.yaml"
        with v0_path.open("w", encoding="utf-8") as fh:
            yaml.dump(super_data, fh)

        # Rewrite verse 001 with content text only
        data["translation"]["text"] = content_text
        with v1_path.open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh)

    return psalm_num, kind


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--psalm", type=int, default=None)
    args = ap.parse_args()

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096

    dirs = sorted(PSALMS_DIR.iterdir(), key=lambda d: int(d.name) if d.name.isdigit() else 999)
    if args.psalm:
        dirs = [PSALMS_DIR / f"{args.psalm:03d}"]

    standalone_count = 0
    fused_count = 0
    skipped = 0

    if args.dry_run:
        print("=== STANDALONE (entire v1 is superscription) ===")
    for d in dirs:
        if not d.is_dir():
            continue
        result = process_psalm(d, dry_run=args.dry_run, yaml=yaml)
        if result:
            _, kind = result
            if kind == "standalone":
                standalone_count += 1
            elif kind == "fused":
                fused_count += 1
        elif args.dry_run:
            pass

    if args.dry_run:
        # Second pass for fused
        print(f"\n=== FUSED (superscription prefix + content in v1) ===")
        for d in dirs:
            if not d.is_dir():
                continue
            v1 = d / "001.yaml"
            if not v1.exists():
                continue
            try:
                data = yaml.load(v1.read_text(encoding="utf-8")) or {}
                text = ((data.get("translation") or {}).get("text") or "").strip()
                if classify_verse1(text) == "fused":
                    sup, con = split_fused(text)
                    print(f"  Ps {d.name}: SUPER=\"{sup[:50]}\" | CONTENT=\"{con[:50]}\"")
            except Exception:
                pass

    label = "would fix" if args.dry_run else "fixed"
    if not args.dry_run:
        print(f"\n{label}: {standalone_count} standalone + {fused_count} fused psalms")
    else:
        print(f"\n(dry run — no files written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
