#!/usr/bin/env python3
"""submit_vertex_gap_closure.py — queue the truly-uncovered verses for
a Gemini 3.1 Pro review pass via Vertex AI on cartha-bible-vertex.

Identifies verses with NO independent-eyes evidence anywhere:
  - no record under state/reviews/ for that verse
  - no `revision_pass` block with a non-drafter model in the YAML
  - no `revisions:` entries with a non-drafter adjudicator/reviewer

Submits each as a `vertex_gap_closure_2026_04` review job under model
`gemini-3.1-pro-preview`. Workers consume the queue with the existing
`gemini_review_worker.py` pointed at Vertex via
GOOGLE_APPLICATION_CREDENTIALS=~/.config/cartha/gemini-vertex-cbv.json
and GCP_LOCATION=global.

Usage:
    python3 tools/submit_vertex_gap_closure.py            # dry-run
    python3 tools/submit_vertex_gap_closure.py --commit   # actually insert
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import sqlite3
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANSLATION_ROOT = REPO_ROOT / "translation"
REVIEWS_ROOT = REPO_ROOT / "state" / "reviews"
DB_PATH = REPO_ROOT / "state" / "chapter_queue.sqlite3"

STRATEGY = "vertex_gap_closure_2026_04"
MODEL = "gemini-3.1-pro-preview"

# Drafter model prefixes — these don't count as independent reviewers.
DRAFTER_PREFIXES = ("gpt-5", "gpt-4")


def is_independent(model_name: str | None) -> bool:
    if not model_name:
        return False
    name = model_name.lower()
    return not any(name.startswith(p) for p in DRAFTER_PREFIXES)


def collect_state_review_coverage() -> set[tuple[str, str, int, int]]:
    """Return {(testament, slug, ch, verse)} for every verse with at
    least one state/reviews/ record."""
    out: set[tuple[str, str, int, int]] = set()
    if not REVIEWS_ROOT.exists():
        return out
    for jf in REVIEWS_ROOT.rglob("*.json"):
        parts = jf.parts
        if len(parts) < 5:
            continue
        try:
            verse = int(parts[-1].split(".")[0])
            chap = int(parts[-2])
            slug = parts[-3]
            testament = parts[-4]
            if testament not in ("ot", "nt", "deuterocanon", "extra_canonical"):
                continue
            out.add((testament, slug, chap, verse))
        except (ValueError, IndexError):
            continue
    return out


def find_uncovered_verses() -> list[tuple[str, str, int, int]]:
    state_coverage = collect_state_review_coverage()
    uncovered: list[tuple[str, str, int, int]] = []
    if not TRANSLATION_ROOT.exists():
        return uncovered
    for testament_dir in TRANSLATION_ROOT.iterdir():
        if not testament_dir.is_dir():
            continue
        testament = testament_dir.name
        for book_dir in testament_dir.iterdir():
            if not book_dir.is_dir():
                continue
            slug = book_dir.name
            for chap_dir in book_dir.iterdir():
                if not chap_dir.is_dir() or not chap_dir.name.isdigit():
                    continue
                chap = int(chap_dir.name)
                for yp in chap_dir.glob("*.yaml"):
                    if not yp.stem.isdigit():
                        continue
                    verse = int(yp.stem)
                    key = (testament, slug, chap, verse)
                    if key in state_coverage:
                        continue
                    try:
                        data = yaml.safe_load(yp.read_text(encoding="utf-8"))
                    except Exception:
                        continue
                    if not isinstance(data, dict):
                        continue
                    rp = data.get("revision_pass") or {}
                    rp_model = rp.get("model") if isinstance(rp, dict) else None
                    if is_independent(rp_model):
                        continue
                    independent_in_revs = False
                    for r in (data.get("revisions") or []):
                        if not isinstance(r, dict):
                            continue
                        if is_independent(r.get("adjudicator")) or is_independent(r.get("reviewer_model")):
                            independent_in_revs = True
                            break
                    if independent_in_revs:
                        continue
                    uncovered.append(key)
    return uncovered


def insert_jobs(uncovered: list[tuple[str, str, int, int]], commit: bool) -> int:
    """Use the canonical insert_job from gemini_review_queue so the
    schema (updated_at NOT NULL, etc.) and integrity-error handling
    match exactly what the worker expects."""
    if not uncovered:
        return 0
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    import gemini_review_queue as rq  # noqa: E402
    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    for testament, slug, chap, verse in uncovered:
        if rq.insert_job(
            conn,
            strategy=STRATEGY,
            testament=testament,
            book_slug=slug,
            chapter=chap,
            verse=verse,
            model=MODEL,
        ):
            inserted += 1
    if commit:
        conn.commit()
    conn.close()
    return inserted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true",
                        help="Actually insert rows; default is a dry-run report")
    args = parser.parse_args()

    print("Walking translation/ + state/reviews/ to find uncovered verses…")
    uncovered = find_uncovered_verses()
    by_book = collections.Counter()
    for (t, s, _, _) in uncovered:
        by_book[(t, s)] += 1
    print(f"\nUncovered verses: {len(uncovered)}")
    for (t, s), n in by_book.most_common():
        print(f"  [{t:16s}] {s:30s}  {n}")

    if not args.commit:
        print("\nDRY RUN — pass --commit to insert into review_jobs.")
        return 0

    inserted = insert_jobs(uncovered, commit=True)
    print(f"\nInserted {inserted} new {STRATEGY} jobs (model={MODEL}).")
    print(f"Run workers with:")
    print(
        "  GOOGLE_APPLICATION_CREDENTIALS=~/.config/cartha/gemini-vertex-cbv.json \\\n"
        "  GCP_LOCATION=global \\\n"
        f"  python3 tools/gemini_review_worker.py --worker-id v1 \\\n"
        f"     --strategy {STRATEGY} --stop-when-empty"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
