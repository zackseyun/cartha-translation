#!/usr/bin/env python3
"""Score wording divergence among POB, SPOB, and public-domain Bibles.

This is a review-priority indicator, not a claim that the majority wording is
correct. It intentionally measures lexical/rendering divergence and combines it
with POB's documented ambiguity signals so editors can find passages worth
examining first.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import itertools
import json
import math
import pathlib
import re
from statistics import mean
from typing import Any

import yaml

import build_reference_panel as refs


ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANSLATION_ROOT = ROOT / "translation"
SPOB_ROOT = ROOT / "translation_simplified"
OUTPUT_ROOT = ROOT / "analysis" / "translation_divergence"
SUMMARY_PATH = ROOT / "translation-divergence-summary.json"
CONSENSUS_PANELS = ("bsb", "web", "asv", "kjv")
LICENSED_TARGETS = ("nkjv", "niv", "nlt")
MIN_RANKING_TOKENS = 8

ARCHAIC_NORMALIZATION = {
    "thou": "you", "thee": "you", "ye": "you", "thy": "your", "thine": "your",
    "hath": "has", "doth": "does", "didst": "did", "art": "are", "wast": "were",
    "shalt": "will", "wilt": "will", "canst": "can", "unto": "to", "saith": "says",
}


def normalize_tokens(text: str) -> list[str]:
    text = re.sub(r"\[[^\]]+\]", " ", str(text).lower())
    tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)
    return [ARCHAIC_NORMALIZATION.get(token, token) for token in tokens]


def wording_similarity(a: str, b: str) -> float:
    left, right = normalize_tokens(a), normalize_tokens(b)
    if not left or not right:
        return 0.0
    sequence = difflib.SequenceMatcher(None, left, right).ratio()
    character_sequence = difflib.SequenceMatcher(None, " ".join(left), " ".join(right)).ratio()
    left_set, right_set = set(left), set(right)
    jaccard = len(left_set & right_set) / max(1, len(left_set | right_set))
    length_balance = min(len(left), len(right)) / max(len(left), len(right))
    # Character similarity keeps harmless transliteration differences such as
    # Pathrusites/Pathrusim from outranking genuine rendering disagreements.
    return max(
        0.0,
        min(1.0, 0.35 * sequence + 0.20 * jaccard + 0.40 * character_sequence + 0.05 * length_balance),
    )


def pairwise_consensus(renderings: dict[str, str]) -> float:
    values = [renderings[name] for name in CONSENSUS_PANELS if renderings.get(name)]
    pairs = list(itertools.combinations(values, 2))
    return mean(wording_similarity(a, b) for a, b in pairs) if pairs else 0.0


def similarity_panel(text: str, renderings: dict[str, str]) -> dict[str, float]:
    return {
        name: round(wording_similarity(text, rendering), 4)
        for name, rendering in renderings.items()
        if name in CONSENSUS_PANELS
    }


def load_licensed_references(path: pathlib.Path | None) -> dict[str, Any]:
    """Load private licensed text; callers must only serialize derived scores."""
    if path is None:
        return {"translations": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    translations = payload.get("translations") if isinstance(payload, dict) else None
    if not isinstance(translations, dict):
        raise ValueError("licensed reference bundle must contain a translations object")
    normalized: dict[str, Any] = {}
    for raw_name, raw_entry in translations.items():
        name = str(raw_name).lower().strip()
        if name not in LICENSED_TARGETS:
            raise ValueError(f"unsupported licensed translation: {raw_name}")
        if not isinstance(raw_entry, dict) or not isinstance(raw_entry.get("verses"), dict):
            raise ValueError(f"licensed translation {raw_name} must contain a verses object")
        normalized[name] = {
            "display_name": str(raw_entry.get("display_name") or name.upper()),
            "provider": str(raw_entry.get("provider") or "private licensed source"),
            "license_reference": str(raw_entry.get("license_reference") or "private"),
            "verses": {
                str(verse_id).upper(): str(text).strip()
                for verse_id, text in raw_entry["verses"].items()
                if str(text).strip()
            },
        }
    return {"translations": normalized}


def licensed_reference_metadata(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        name: {
            "display_name": entry["display_name"],
            "provider": entry["provider"],
            "license_confirmed": bool(entry["license_reference"]),
            "verse_count": len(entry["verses"]),
            "text_included_in_report": False,
        }
        for name, entry in (bundle.get("translations") or {}).items()
    }


def licensed_comparisons(
    verse_id: str,
    pob_text: str,
    spob_text: str | None,
    bundle: dict[str, Any],
) -> dict[str, dict[str, float | None]]:
    comparisons: dict[str, dict[str, float | None]] = {}
    for name, entry in (bundle.get("translations") or {}).items():
        licensed_text = entry["verses"].get(verse_id.upper())
        if not licensed_text:
            continue
        pob_similarity = wording_similarity(pob_text, licensed_text)
        spob_similarity = wording_similarity(spob_text, licensed_text) if spob_text else None
        comparisons[name] = {
            "pob_similarity": round(pob_similarity, 4),
            "spob_similarity": round(spob_similarity, 4) if spob_similarity is not None else None,
            "spob_minus_pob": round(spob_similarity - pob_similarity, 4) if spob_similarity is not None else None,
        }
    return comparisons


def ranking_alignment(text: str, renderings: dict[str, str]) -> dict[str, Any]:
    """Reject tiny or badly segmented rows from public-facing rankings."""
    pob_tokens = len(normalize_tokens(text))
    reference_tokens = {
        name: len(normalize_tokens(rendering))
        for name, rendering in renderings.items()
        if name in CONSENSUS_PANELS and rendering
    }
    comparable = [
        name for name, count in reference_tokens.items()
        if pob_tokens
        and count >= MIN_RANKING_TOKENS
        and 0.5 <= count / pob_tokens <= 2.0
    ]
    reasons: list[str] = []
    if pob_tokens < MIN_RANKING_TOKENS:
        reasons.append("pob_fragment_too_short")
    if len(comparable) < 3:
        reasons.append("reference_segmentation_mismatch")
    return {
        "ranking_eligible": not reasons,
        "confidence": "high" if not reasons else "low",
        "pob_token_count": pob_tokens,
        "comparable_reference_count": len(comparable),
        "reasons": reasons,
    }


def licensed_target_metrics(
    comparisons: dict[str, dict[str, float | None]],
) -> dict[str, float | None]:
    """Score POB against NIV/NKJV and SPOB against NLT, never each other."""
    pob_target_values = [
        float(comparisons[name]["pob_similarity"])
        for name in ("niv", "nkjv")
        if name in comparisons and comparisons[name].get("pob_similarity") is not None
    ]
    nlt = comparisons.get("nlt") or {}
    spob_nlt_similarity = nlt.get("spob_similarity")
    pob_target_similarity = mean(pob_target_values) if len(pob_target_values) == 2 else None
    pob_target_divergence = 100 * (1 - pob_target_similarity) if pob_target_similarity is not None else None
    spob_target_divergence = 100 * (1 - float(spob_nlt_similarity)) if spob_nlt_similarity is not None else None
    return {
        "pob_niv_nkjv_similarity": round(pob_target_similarity, 4) if pob_target_similarity is not None else None,
        "pob_niv_nkjv_divergence": round(pob_target_divergence, 2) if pob_target_divergence is not None else None,
        "spob_nlt_similarity": round(float(spob_nlt_similarity), 4) if spob_nlt_similarity is not None else None,
        "spob_nlt_divergence": round(spob_target_divergence, 2) if spob_target_divergence is not None else None,
    }

def public_headline_metrics(text: str, renderings: dict[str, str]) -> dict[str, Any]:
    similarities = similarity_panel(text, renderings)
    if not similarities: return {}
    nearest_name, nearest_similarity = max(similarities.items(), key=lambda item: item[1])
    consensus = pairwise_consensus(renderings)
    novelty = 1 - nearest_similarity
    return {"nearest_reference": nearest_name, "nearest_reference_similarity": round(nearest_similarity, 4), "novelty": round(novelty, 4), "headline_divergence": round(100 * novelty * math.sqrt(max(0.0, consensus)), 2)}

def surviving_neighbor_offset(text: str, panels: dict[str, dict], book: str, chapter: int, verse: int, radius: int = 12) -> dict[str, Any] | None:
    code_map, offsets, gains = refs.PANEL_CODES.get(book, {}), [], []
    for panel in CONSENSUS_PANELS:
        code = code_map.get(panel)
        if not code or panel not in panels: continue
        mapped_chapter, mapped_verse = refs.panel_reference(book, panel, chapter, verse)
        aligned = panels[panel].get((code, mapped_chapter, mapped_verse))
        if not aligned: continue
        aligned_score = wording_similarity(text, aligned)
        candidates = [(wording_similarity(text, panels[panel][(code, mapped_chapter, mapped_verse + off)]), off) for off in range(-radius, radius + 1) if off and mapped_verse + off >= 1 and (code, mapped_chapter, mapped_verse + off) in panels[panel]]
        if not candidates: continue
        best_score, best_offset = max(candidates)
        offsets.append(best_offset); gains.append(best_score - aligned_score)
    if len(offsets) < 3 or len(set(offsets)) != 1 or mean(gains) < .20 or min(gains) < .10: return None
    return {"offset": offsets[0], "mean_gain": round(mean(gains), 4), "panel_count": len(offsets)}

def surviving_segmentation_merge(text: str, panels: dict[str, dict], book: str, chapter: int, verse: int) -> dict[str, Any] | None:
    """Detect a POB row that contains its aligned English verse plus a neighbor."""
    code_map, directions, gains = refs.PANEL_CODES.get(book, {}), [], []
    for panel in CONSENSUS_PANELS:
        code = code_map.get(panel)
        if not code or panel not in panels: continue
        mapped_chapter, mapped_verse = refs.panel_reference(book, panel, chapter, verse)
        aligned = panels[panel].get((code, mapped_chapter, mapped_verse))
        if not aligned: continue
        base = wording_similarity(text, aligned)
        candidates = []
        previous = panels[panel].get((code, mapped_chapter, mapped_verse - 1))
        following = panels[panel].get((code, mapped_chapter, mapped_verse + 1))
        if previous: candidates.append((wording_similarity(text, f"{previous} {aligned}"), "previous+aligned"))
        if following: candidates.append((wording_similarity(text, f"{aligned} {following}"), "aligned+next"))
        if not candidates: continue
        best, direction = max(candidates)
        directions.append(direction); gains.append(best - base)
    # Even partial spillover can materially distort a lexical score; this
    # verifier only runs when POB is already >35% longer than the panel.
    if len(directions) < 3 or len(set(directions)) != 1 or mean(gains) < .035 or min(gains) < .01: return None
    return {"direction": directions[0], "mean_gain": round(mean(gains), 4), "panel_count": len(directions)}


def documented_risk(record: dict[str, Any]) -> tuple[float, list[str]]:
    translation = record.get("translation") or {}
    footnotes = translation.get("footnotes") or []
    theological = record.get("theological_decisions") or []
    lexical = record.get("lexical_decisions") or []
    source = record.get("source") or {}
    text_blob = " ".join(
        str(item.get("rationale") or "")
        for item in [*lexical, *theological]
        if isinstance(item, dict)
    ).lower()
    signals: list[str] = []
    score = 0.0
    if footnotes:
        score += min(30, 10 + 5 * len(footnotes))
        signals.append("pob_footnotes")
    if theological:
        score += min(30, 15 + 5 * len(theological))
        signals.append("theological_decision")
    if re.search(r"ambig|disput|debate|variant|uncertain|contested", text_blob):
        score += 25
        signals.append("documented_ambiguity")
    if re.search(r"figur|idiom|metaphor|wordplay|double meaning", text_blob):
        score += 15
        signals.append("figurative_or_idiomatic")
    if isinstance(source, dict) and any(key in source for key in ("variants", "apparatus", "alternate")):
        score += 20
        signals.append("source_variant")
    return min(100.0, score), signals


def score_band(score: float) -> str:
    if score >= 55:
        return "very_high"
    if score >= 40:
        return "high"
    if score >= 25:
        return "moderate"
    return "low"


def verse_paths(book: str) -> list[pathlib.Path]:
    roots = [TRANSLATION_ROOT / testament / book for testament in ("ot", "nt")]
    paths: list[pathlib.Path] = []
    for root in roots:
        if root.exists():
            paths.extend(root.glob("[0-9][0-9][0-9]/[0-9][0-9][0-9].yaml"))
    return sorted(paths)


def spob_path_for(pob_path: pathlib.Path) -> pathlib.Path:
    return SPOB_ROOT / pob_path.relative_to(TRANSLATION_ROOT)


def score_verse(
    path: pathlib.Path,
    panels: dict[str, dict],
    book: str,
    licensed_bundle: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        return None
    text = str(((record.get("translation") or {}).get("text") or "")).strip()
    if not text:
        return None
    chapter, verse = int(path.parent.name), int(path.stem)
    renderings = refs.panel_lookup(panels, book, chapter, verse)
    consensus_refs = {name: value for name, value in renderings.items() if name in CONSENSUS_PANELS}
    if len(consensus_refs) < 3:
        return None
    consensus = pairwise_consensus(consensus_refs)
    pob_panel = similarity_panel(text, consensus_refs)
    pob_mean = mean(pob_panel.values())
    spob_path = spob_path_for(path)
    spob_text = None
    spob_panel: dict[str, float] = {}
    pob_spob = None
    if spob_path.exists():
        spob_record = yaml.safe_load(spob_path.read_text(encoding="utf-8")) or {}
        spob_text = str(((spob_record.get("translation") or {}).get("text") or "")).strip() or None
        if spob_text:
            spob_panel = similarity_panel(spob_text, consensus_refs)
            pob_spob = wording_similarity(text, spob_text)
    licensed = licensed_comparisons(
        str(record.get("id") or ""), text, spob_text, licensed_bundle or {"translations": {}}
    )
    risk_score, risk_signals = documented_risk(record)
    alignment = ranking_alignment(text, consensus_refs)
    if verse == 0:
        alignment["ranking_eligible"] = False; alignment["confidence"] = "low"; alignment["reasons"].append("superscription_not_comparable")
    if book == "psalms" and verse == 1 and refs._psalm_title_verse_count(chapter):
        alignment["ranking_eligible"] = False; alignment["confidence"] = "low"; alignment["reasons"].append("reference_title_merged")
    target_metrics = {
        name: value
        for name, value in licensed_target_metrics(licensed).items()
        if value is not None
    }
    pob_headline = public_headline_metrics(text, consensus_refs)
    spob_headline = public_headline_metrics(spob_text, consensus_refs) if spob_text else {}
    neighbor_offset = None
    if verse != 0 and max(pob_panel.values(), default=0.0) < .55:
        neighbor_offset = surviving_neighbor_offset(text, panels, book, chapter, verse)
    if neighbor_offset:
        alignment["ranking_eligible"] = False; alignment["confidence"] = "low"; alignment["reasons"].append("unanimous_neighbor_offset")
    segmentation_merge = None
    reference_token_counts = [len(normalize_tokens(value)) for value in consensus_refs.values()]
    if verse != 0 and reference_token_counts and len(normalize_tokens(text)) > 1.35 * mean(reference_token_counts):
        segmentation_merge = surviving_segmentation_merge(text, panels, book, chapter, verse)
    if segmentation_merge:
        alignment["ranking_eligible"] = False; alignment["confidence"] = "low"; alignment["reasons"].append("unanimous_segmentation_merge")
    reference_divergence = 100 * (1 - consensus)
    pob_distinctiveness = 100 * (1 - pob_mean)
    spob_distinctiveness = None
    if spob_panel:
        spob_distinctiveness = 100 * (1 - mean(spob_panel.values()))
    priority = 0.50 * reference_divergence + 0.30 * pob_distinctiveness + 0.20 * risk_score
    signals = [*risk_signals, *alignment["reasons"]]
    if reference_divergence >= 45:
        signals.append("high_reference_wording_divergence")
    if pob_distinctiveness >= 55:
        signals.append("pob_wording_outlier")
    if spob_distinctiveness is not None and spob_distinctiveness >= 55:
        signals.append("spob_wording_outlier")
    return {
        "id": record.get("id"),
        "reference": record.get("reference"),
        "chapter": chapter,
        "verse": verse,
        "scores": {
            "reference_consensus_similarity": round(consensus, 4),
            "reference_wording_divergence": round(reference_divergence, 2),
            "reference_wording_divergence_band": score_band(reference_divergence),
            "pob_reference_similarity": round(pob_mean, 4),
            "pob_nearest_reference": pob_headline.get("nearest_reference"),
            "pob_nearest_reference_similarity": pob_headline.get("nearest_reference_similarity"),
            "pob_novelty": pob_headline.get("novelty"),
            "pob_headline_divergence": pob_headline.get("headline_divergence"),
            "pob_distinctiveness": round(pob_distinctiveness, 2),
            "pob_distinctiveness_band": score_band(pob_distinctiveness),
            "spob_reference_similarity": round(mean(spob_panel.values()), 4) if spob_panel else None,
            "spob_nearest_reference": spob_headline.get("nearest_reference"),
            "spob_nearest_reference_similarity": spob_headline.get("nearest_reference_similarity"),
            "spob_novelty": spob_headline.get("novelty"),
            "spob_public_provisional_divergence": spob_headline.get("headline_divergence"),
            "spob_distinctiveness": round(spob_distinctiveness, 2) if spob_distinctiveness is not None else None,
            "spob_distinctiveness_band": score_band(spob_distinctiveness) if spob_distinctiveness is not None else None,
            "pob_spob_similarity": round(pob_spob, 4) if pob_spob is not None else None,
            "pob_nlt_similarity": (licensed.get("nlt") or {}).get("pob_similarity"),
            "spob_nlt_similarity": (licensed.get("nlt") or {}).get("spob_similarity"),
            "spob_nlt_similarity_gain": (licensed.get("nlt") or {}).get("spob_minus_pob"),
            **target_metrics,
            "ranking_eligible": alignment["ranking_eligible"],
            "alignment_neighbor_offset": neighbor_offset.get("offset") if neighbor_offset else None,
            "alignment_neighbor_gain": neighbor_offset.get("mean_gain") if neighbor_offset else None,
            "alignment_segmentation_direction": segmentation_merge.get("direction") if segmentation_merge else None,
            "alignment_segmentation_gain": segmentation_merge.get("mean_gain") if segmentation_merge else None,
            "documented_risk": round(risk_score, 2),
            "review_priority": round(priority, 2),
            "review_priority_band": score_band(priority),
        },
        "signals": sorted(set(signals)),
        "pob": {"text": text, "similarity_by_reference": pob_panel},
        "spob": {"text": spob_text, "similarity_by_reference": spob_panel} if spob_text else None,
        "public_domain_references": renderings,
        "licensed_comparisons": licensed,
    }


def add_percentiles(rows: list[dict[str, Any]]) -> None:
    ordered = sorted(rows, key=lambda row: row["scores"]["review_priority"])
    denominator = max(1, len(ordered) - 1)
    for index, row in enumerate(ordered):
        row["scores"]["review_priority_percentile"] = round(index / denominator * 100, 2)


def build_book(
    book: str,
    panels: dict[str, dict],
    licensed_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    licensed_bundle = licensed_bundle or {"translations": {}}
    rows = [
        row for path in verse_paths(book)
        if (row := score_verse(path, panels, book, licensed_bundle))
    ]
    add_percentiles(rows)
    rows.sort(key=lambda row: (row["chapter"], row["verse"]))
    return {
        "schema_version": 1,
        "book": book,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "method": {
            "description": "Lexical/rendering divergence indicator; not a doctrinal truth score or majority vote.",
            "consensus_references": list(CONSENSUS_PANELS),
            "reference_divergence_weight": 0.50,
            "pob_distinctiveness_weight": 0.30,
            "documented_risk_weight": 0.20,
            "normalization": "case, punctuation, footnote markers, and common KJV archaisms normalized",
            "licensed_references_affect_review_priority": False,
            "public_ranking_guard": f"minimum {MIN_RANKING_TOKENS} POB tokens and three length-compatible references",
            "targeted_ranking": {
                "pob_targets": ["niv", "nkjv"],
                "spob_targets": ["nlt"],
                "ranked_separately": True,
                "requires_private_licensed_inputs": True,
            },
            "public_headline": "POB novelty × square-root(reference consensus); documented risk is excluded",
        },
        "sources": {name: refs.PANEL_CITATIONS[name] for name in refs.PANEL_FILES},
        "licensed_reference_sources": licensed_reference_metadata(licensed_bundle),
        "verse_count": len(rows),
        "spob_verse_count": sum(row.get("spob") is not None for row in rows),
        "verses": rows,
    }


def compact_summary(books: list[dict[str, Any]], top: int) -> dict[str, Any]:
    rows = [
        {"book": book["book"], **row}
        for book in books
        for row in book["verses"]
    ]
    eligible = [row for row in rows if row["scores"].get("ranking_eligible")]
    licensed_pob = [row for row in eligible if row["scores"].get("pob_niv_nkjv_divergence") is not None]
    licensed_spob = [row for row in eligible if row["scores"].get("spob_nlt_divergence") is not None]
    pob_ranked = sorted(
        licensed_pob or eligible,
        key=lambda row: row["scores"][
            "pob_niv_nkjv_divergence" if licensed_pob else "pob_headline_divergence"
        ],
        reverse=True,
    )
    spob_ranked = sorted(licensed_spob, key=lambda row: row["scores"]["spob_nlt_divergence"], reverse=True)
    def compact_row(row):
        return {"book":row["book"],"id":row["id"],"reference":row["reference"],"scores":row["scores"],"signals":row["signals"],"pob_text":row["pob"]["text"],"spob_text":(row.get("spob") or {}).get("text"),"public_domain_references":row["public_domain_references"],"licensed_comparisons":row["licensed_comparisons"]}
    return {
        "schema_version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "description": "Highest-priority wording-divergence review candidates. Scores identify where to investigate; they do not identify the correct translation.",
        "ranking_mode": {"pob":"niv_nkjv" if licensed_pob else "public_domain_provisional","spob":"nlt" if licensed_spob else "awaiting_nlt"},
        "ranking_targets": {"pob": ["NIV", "NKJV"], "spob": ["NLT"]},
        "scope": {"scored":len(rows),"ranking_eligible":len(eligible),"quarantined":len(rows)-len(eligible),"surviving_neighbor_offsets":sum("unanimous_neighbor_offset" in (row.get("signals") or []) for row in rows)},
        "books": [
            {"book": book["book"], "verse_count": book["verse_count"], "spob_verse_count": book["spob_verse_count"]}
            for book in books
        ],
        "licensed_reference_sources": books[0].get("licensed_reference_sources", {}) if books else {},
        "top_review_candidates": [compact_row(row) for row in pob_ranked[:top]],
        "pob_top_candidates": [compact_row(row) for row in pob_ranked[:top]],
        "spob_top_candidates": [compact_row(row) for row in spob_ranked[:top]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--books", nargs="+", default=["genesis", "luke"])
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--top", type=int, default=100)
    parser.add_argument("--allow-alignment-quarantine", action="store_true")
    parser.add_argument("--output-root", type=pathlib.Path, default=OUTPUT_ROOT)
    parser.add_argument("--summary", type=pathlib.Path, default=SUMMARY_PATH)
    parser.add_argument(
        "--licensed-references",
        type=pathlib.Path,
        help="gitignored private JSON bundle for licensed NKJV/NIV/NLT text; report stores scores only",
    )
    args = parser.parse_args()
    if args.fetch:
        refs.fetch_corpora()
    panels = {name: refs.load_vpl(path) for name, path in refs.PANEL_FILES.items() if path.exists()}
    missing = [name for name in CONSENSUS_PANELS if name not in panels]
    if missing:
        raise SystemExit(f"Missing reference corpora {missing}; rerun with --fetch")
    licensed_bundle = load_licensed_references(args.licensed_references)
    args.output_root.mkdir(parents=True, exist_ok=True)
    books: list[dict[str, Any]] = []
    empty_books: list[str] = []
    for book in args.books:
        payload = build_book(book, panels, licensed_bundle)
        books.append(payload)
        if verse_paths(book) and payload["verse_count"] == 0:
            empty_books.append(book)
        output = args.output_root / f"{book}.json"
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{book}: scored={payload['verse_count']} spob={payload['spob_verse_count']} -> {output}")
    if empty_books:
        raise SystemExit(
            "Reference-panel mapping produced zero scored verses for: "
            + ", ".join(empty_books)
        )
    summary = compact_summary(books, args.top)
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"summary -> {args.summary}")
    survivors = summary["scope"]["surviving_neighbor_offsets"]
    if survivors and not args.allow_alignment_quarantine:
        raise SystemExit(f"Alignment verifier found {survivors} unanimous neighboring-verse offsets; fix the versification map or rerun explicitly with --allow-alignment-quarantine")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
