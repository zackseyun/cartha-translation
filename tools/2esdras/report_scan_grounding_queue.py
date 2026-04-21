#!/usr/bin/env python3
"""report_scan_grounding_queue.py — list verses still needing scan-grounding.

This is a provenance report based on:

- explicit verse markers visible in the Bensly 1895 chapter candidates
- the Bensly 1875 Missing Fragment coverage for VII 36–105
- explicit manual rescue ranges recorded in chapter headers

Any verse present in `latin/transcribed/` but *not* covered by one of
those scan-grounded sources is queued here for future Bensly-based
manual rescue.
"""
from __future__ import annotations

import json
import pathlib
import re


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
TRANSCRIBED_DIR = REPO_ROOT / "sources" / "2esdras" / "latin" / "transcribed"
MANIFEST_PATH = REPO_ROOT / "sources" / "2esdras" / "latin" / "intermediate" / "bensly1895_chapter_candidates" / "manifest.json"
OUT_JSON = TRANSCRIBED_DIR / "SCAN_GROUNDING_QUEUE.json"
OUT_MD = TRANSCRIBED_DIR / "SCAN_GROUNDING_QUEUE.md"

VERSE_RE = re.compile(r"(?m)^(\d+)\s")
MARKER_RE = re.compile(r"(?<![A-Za-z])(\d{1,3})(?![A-Za-z])")
SUPP_MISSING_RE = re.compile(r"^# Missing verses supplemented from PD digital text: (.+)$")
SUPP_PLACEHOLDER_RE = re.compile(r"^# Placeholder/crop/ellipsis verses replaced from PD digital text: (.+)$")
MANUAL_RESCUE_RE = re.compile(r"^# Manual scan-grounded rescue completed for verses (.+?) from PDF pages")


def parse_range_list(raw: str) -> list[int]:
    raw = raw.replace(" and ", ", ")
    out: list[int] = []
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            a, b = token.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(token))
    return out


def compress_ranges(values: list[int]) -> list[str]:
    if not values:
        return []
    values = sorted(set(values))
    out = []
    start = prev = values[0]
    for v in values[1:]:
        if v == prev + 1:
            prev = v
            continue
        out.append(f"{start}-{prev}" if start != prev else str(start))
        start = prev = v
    out.append(f"{start}-{prev}" if start != prev else str(start))
    return out


def load_page_manifest() -> dict[int, list[int]]:
    raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    out: dict[int, list[int]] = {}
    for row in raw:
        out[int(row["chapter"])] = row["source_pages"]
    return out


def explicit_candidate_verses(chapter: int) -> set[int]:
    path = REPO_ROOT / "sources" / "2esdras" / "latin" / "intermediate" / "bensly1895_chapter_candidates" / f"ch{chapter:02d}.txt"
    if not path.exists():
        return set()
    text = "\n".join(
        ln for ln in path.read_text(encoding="utf-8").splitlines()
        if not ln.startswith("#") and not ln.startswith("=== PAGE")
    )
    nums = [int(m.group(1)) for m in MARKER_RE.finditer(text)]
    seq: list[int] = []
    last = 0
    for n in nums:
        if 1 <= n <= 200 and n >= last:
            if not seq or n != seq[-1]:
                seq.append(n)
                last = n
    return set(seq)


def parse_header(chapter: int) -> tuple[list[int], list[int], list[int], list[int]]:
    path = TRANSCRIBED_DIR / f"ch{chapter:02d}.txt"
    missing: list[int] = []
    placeholder: list[int] = []
    manual: list[int] = []
    present = [int(m.group(1)) for m in VERSE_RE.finditer(path.read_text(encoding="utf-8"))]
    for line in path.read_text(encoding="utf-8").splitlines():
        m = SUPP_MISSING_RE.match(line)
        if m:
            missing.extend(parse_range_list(m.group(1)))
            continue
        m = SUPP_PLACEHOLDER_RE.match(line)
        if m:
            placeholder.extend(parse_range_list(m.group(1)))
            continue
        m = MANUAL_RESCUE_RE.match(line)
        if m:
            manual.extend(parse_range_list(m.group(1)))
    return sorted(set(missing)), sorted(set(placeholder)), sorted(set(manual)), sorted(set(present))


def main() -> int:
    pages = load_page_manifest()
    chapters = []
    for ch in range(1, 17):
        missing, placeholder, manual, present = parse_header(ch)
        explicit = explicit_candidate_verses(ch)
        if ch == 7:
            explicit.update(range(36, 106))
        explicit.update(manual)

        queue = sorted(v for v in present if v not in explicit)
        if not queue and not manual:
            continue
        chapters.append(
            {
                "chapter": ch,
                "source_pages": pages.get(ch, []),
                "manual_rescued": manual,
                "queue": queue,
            }
        )

    payload = {
        "pipeline": "2esdras_scan_grounding_queue",
        "chapters": chapters,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# 2 Esdras scan-grounding queue",
        "",
        "These verses are still present from the PD digital supplement rather than",
        "having been manually re-segmented / re-grounded from Bensly scan material.",
        "",
        "| Chapter | Bensly 1895 pages | Manual rescued | Still not scan-grounded |",
        "|---|---|---|---|",
    ]
    if chapters:
        for row in chapters:
            lines.append(
                f"| {row['chapter']} | "
                f"{'-'.join(map(str, row['source_pages'])) if row['source_pages'] else '—'} | "
                f"{', '.join(compress_ranges(row['manual_rescued'])) or '—'} | "
                f"{', '.join(compress_ranges(row['queue'])) or '—'} |"
            )
    else:
        lines.append("| — | — | — | — |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
