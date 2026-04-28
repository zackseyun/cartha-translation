#!/usr/bin/env python3
"""adjudicate_doctrine_aware.py — process swarm findings using
DOCTRINE.md and METHODOLOGY.md as the policy framework.

Successor to the heuristic-only `auto_apply_gemini.py`. Same
tier-classification idea, but the rules know about:

  - Yahweh policy (DOCTRINE.md table line 96 — "יְהוָה → Yahweh")
  - Original-language primacy (DOCTRINE.md §1)
  - Don't undersell the text's gravity / no euphemism (§5)
  - Consistency of key terms or documented exception (§4)
  - Preserve theological tension rather than resolve it (§3)
  - Translate titles, transliterate names (§2)

Decisions:
  APPLY     — clear-cut case the doctrine answers, edit lands now
  ESCALATE  — actually requires a human policy decision (rare)
  SKIP      — no-op, hedged reviewer, or wholesale-rewrite-too-risky

Run after a swarm completes:
    python3 tools/adjudicate_doctrine_aware.py --strategy STRATEGY [--commit]
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import sqlite3
import sys

import yaml as pyyaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "state" / "chapter_queue.sqlite3"
TRANSLATION_ROOT = REPO_ROOT / "translation"

DRAFTER_PREFIXES = ("gpt-5", "gpt-4")

# Doctrine-driven rewrites that ALWAYS apply when seen in any field
# (translation text, lexical_decisions[].chosen, lexical_decisions[].rationale,
# footnotes[].text). Keys are case-sensitive substrings to find;
# values are replacement strings.
ALWAYS_REWRITE = {
    # Yahweh policy (DOCTRINE.md table line 96, METHODOLOGY.md L321):
    # "the LORD" anywhere it stands for יהוה in the OT/deuterocanon
    # should be "Yahweh". The canonical exception is NT verses
    # quoting the OT via Kyrios — those keep "Lord". The reviewer
    # has already evaluated this in context, so trust the suggestion.
}


def is_independent(model_name: str | None) -> bool:
    if not model_name:
        return False
    name = model_name.lower()
    return not any(name.startswith(p) for p in DRAFTER_PREFIXES)


def _yaml_path(testament, slug, ch, v):
    return TRANSLATION_ROOT / testament / slug / f"{ch:03d}" / f"{v:03d}.yaml"


def doctrine_decision(f: dict) -> tuple[str, str]:
    cat = (f["category"] or "").lower()
    sev = (f["severity"] or "").lower()
    rat = f["rationale"].lower()
    cur = (f["current"] or "").strip()
    sug = (f["suggest"] or "").strip()

    # Empty-suggest with chunking signals → ESCALATE for re-drafter
    if not sug and any(k in rat for k in ["verse boundar", "chunk", "truncat", "splitting", "split", "belongs to verse", "belongs to v", "actually contain"]):
        return ("ESCALATE_CHUNK", "verse-boundary chunking error — needs redraft_chunked_verses.py")
    if not cur or not sug or cur == sug:
        return ("SKIP", "no-op or empty")
    # Wholesale rewrites still risky
    if len(sug) > len(cur) * 4 and len(cur) > 50:
        return ("SKIP", "wholesale rewrite (>4x), too risky")

    # Yahweh policy: any finding that swaps "the LORD" for "Yahweh"
    # is doctrine, not policy-debate. APPLY.
    if "lord" in cur.lower() and "yahweh" in sug.lower():
        return ("APPLY", "Yahweh policy (DOCTRINE.md table line 96)")
    # Reverse direction: replacing "Yahweh" with "LORD" is policy
    # violation — SKIP unless it's an NT Kyrios quote of an OT verse.
    if "yahweh" in cur.lower() and "lord" in sug.lower() and "kyrios" not in rat:
        return ("SKIP", "would reintroduce 'LORD' against doctrine")

    # Theological-weight: doctrine §1 + §5 say apply when source is
    # more direct and tradition softens. Otherwise escalate.
    if cat == "theological_weight":
        if any(k in rat for k in ["literal", "directly invok", "biblical idiom", "echo of", "established metaphor", "obscur", "euphemis"]):
            return ("APPLY", "doctrine §1 original-language primacy + §5 don't undersell")
        return ("ESCALATE", "theological policy decision")

    # Consistency: §4 says preserve consistency unless documented exception
    if cat == "consistency":
        if any(k in rat for k in ["repeats the exact same word", "same word in", "parallelism", "same lemma", "consistency"]):
            return ("APPLY", "doctrine §4 consistency of key terms")
        return ("ESCALATE", "needs cross-verse view")

    # Hedged language → SKIP
    if any(p in rat for p in ["could be either", "either/or", "might be", "arguably", "or possibly"]):
        return ("SKIP", "reviewer hedged")

    # Mistranslation with source citation → APPLY
    if cat == "mistranslation":
        if any(p in rat for p in [
            "greek", "hebrew", "syriac", "ge'ez", "geez", "aramaic", "lxx", "mt",
            "bdag", "halot", "bdb", "lsj", "louw-nida",
            "verb", "noun", "participle", "aorist", "imperative", "imperfect",
            "literal", "idiom", "omit", "missing", "preposition", "conjunction",
            "feminine", "masculine", "singular", "plural", "tense", "voice",
            "hallucina", "absent from", "not in the", "added", "doesn't appear",
        ]):
            return ("APPLY", "mistranslation with source-language evidence")
        return ("SKIP", "mistranslation without source anchor")

    # Missing nuance: §1 favors source content
    if cat == "missing_nuance":
        if any(p in rat for p in [
            "omit", "missing", "lost", "absent", "should include", "adds", "reflects",
            "accurately", "pronominal", "suffix", "agreement", "feminine", "masculine",
            "singular", "plural", "syriac", "greek", "hebrew", "ge'ez", "geez",
            "parallel", "subject", "object",
        ]):
            return ("APPLY", "doctrine §1 — restore source-text content")
        return ("SKIP", "unclear missing-nuance")

    # Awkward English: §5 favors readable modern English
    if cat == "awkward_english":
        return ("APPLY", "doctrine §5 readable modern English")

    # Grammar: clear-cut almost always
    if cat == "grammar":
        return ("APPLY", "grammar fix")

    # Lexical: §1 + §4
    if cat == "lexical":
        if any(p in rat for p in [
            "bdag", "halot", "bdb", "lsj", "louw-nida", "lexicon",
            "greek", "hebrew", "syriac", "ge'ez", "geez", "aramaic",
            "literal", "idiom", "verb", "noun", "tense", "voice",
        ]):
            return ("APPLY", "lexical with source-language evidence")
        return ("SKIP", "lexical without source citation")

    # 'other' bucket
    if cat == "other":
        if any(p in rat for p in ["duplicat", "punctuation", "footnote", "marker", "truncat", "comma", "period", "capitaliz"]):
            return ("APPLY", "clear bug fix")
        if any(p in rat for p in ["verse boundar", "chunk", "belongs to verse"]):
            return ("ESCALATE_CHUNK", "verse-boundary issue")
        return ("SKIP", "other-category, unclear")

    return ("SKIP", f"no rule for cat={cat}")


def text_present_in_yaml(f: dict) -> bool:
    p = _yaml_path(f["testament"], f["slug"], f["ch"], f["v"])
    if not p.exists():
        return False
    try:
        d = pyyaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        return False
    text = ((d.get("translation") or {}).get("text") or "")
    return f["current"] in text


def collect_findings(strategy: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    findings = []
    for row in conn.execute("""
        SELECT id, testament, book_slug, chapter, verse, review_path
        FROM review_jobs
        WHERE strategy=? AND status='completed' AND applied=0
    """, (strategy,)):
        job_id, t, slug, ch, v, rp = row
        if not rp:
            continue
        p = pathlib.Path(rp)
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for i, issue in enumerate(d.get("issues") or []):
            findings.append({
                "job_id": job_id, "testament": t, "slug": slug, "ch": ch, "v": v,
                "review_path": rp, "issue_index": i,
                "category": issue.get("category"),
                "severity": issue.get("severity"),
                "current": issue.get("current_rendering","") or "",
                "suggest": issue.get("suggested_rewrite","") or "",
                "rationale": issue.get("rationale","") or "",
                "span": issue.get("span","") or "",
            })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", default="vertex_full_book_qc_2026_04",
                        help="review_jobs strategy to process")
    parser.add_argument("--commit", action="store_true",
                        help="Actually apply (default: dry-run, prints decisions)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Cap applies (0 = unlimited)")
    parser.add_argument("--escalations-out", default="/tmp/cob_escalations.json",
                        help="Where to write the ESCALATE list for human review")
    args = parser.parse_args()

    print(f"Strategy: {args.strategy}")
    findings = collect_findings(args.strategy)
    print(f"Total unapplied findings: {len(findings)}")

    decisions = collections.Counter()
    plan = []
    for f in findings:
        decision, reason = doctrine_decision(f)
        # Verify text presence for APPLY (unless we'll edit metadata
        # which we don't currently support inline — those route ESCALATE)
        if decision == "APPLY" and not text_present_in_yaml(f):
            decision, reason = "SKIP", "current text not present in verse translation field"
        decisions[decision] += 1
        plan.append({**f, "decision": decision, "reason": reason})

    print("\nDecisions:")
    for d, n in decisions.most_common():
        print(f"  {d}: {n}")

    # Write escalations file (regardless of --commit so user can act
    # on them out-of-band)
    escalations = [f for f in plan if f["decision"].startswith("ESCALATE")]
    pathlib.Path(args.escalations_out).write_text(json.dumps(escalations, indent=2))
    print(f"\nEscalations written to: {args.escalations_out} ({len(escalations)} items)")

    if not args.commit:
        print("\nDRY RUN — pass --commit to apply.")
        return 0

    # Apply
    sys.path.insert(0, str(pathlib.Path("tools").resolve()))
    import apply_gemini_revision as agr
    applied_jobs = set()
    applied = errors = 0
    targets = [f for f in plan if f["decision"] == "APPLY"]
    if args.limit:
        targets = targets[:args.limit]
    for f in targets:
        try:
            path = agr.yaml_path_for(f["testament"], f["slug"], f["ch"], f["v"])
            agr.apply_revision(
                path=path,
                find=f["current"],
                replace=f["suggest"],
                rationale=f["rationale"],
                review_path=f["review_path"],
                issue_category=f["category"] or "mistranslation",
            )
            applied += 1
            applied_jobs.add(f["job_id"])
            if applied % 25 == 0:
                print(f"  ✓ {applied}/{len(targets)} applied")
        except Exception as e:
            errors += 1
            if errors <= 10:
                print(f"  ✗ {f['slug']} {f['ch']}:{f['v']}: {str(e)[:140]}")

    # Mark applied jobs in DB
    conn = sqlite3.connect(DB_PATH)
    n = 0
    for jid in applied_jobs:
        cur = conn.execute(
            "UPDATE review_jobs SET applied=1, apply_summary='doctrine-aware adjudicator' WHERE id=?",
            (jid,),
        )
        n += cur.rowcount
    conn.commit()
    print(f"\nApplied {applied} edits, marked {n} jobs as applied, {errors} errors.")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
