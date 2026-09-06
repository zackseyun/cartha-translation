#!/usr/bin/env python3
"""Reproducible, metadata-only SP/WLC screening; not an adjudicated apparatus."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources/textual_restoration/discovery/samaritan_wlc_screen.v1.json"
INCENSE_OUT = OUT.with_name("exodus_incense_alignment.v1.json")
GREEK_SHA = "c5a775d14720b26c70dfcdb72c3c473ac21c33894714ebd85d03f132ebf45267"
INCENSE_ANCHORS = [
    ("Exod.26.35", "ושמת את השלחן"),
    ("Exod.30.1", "ועשית מזבח"),
    ("Exod.30.2", "אמה ארכו"),
    ("Exod.30.3", "וצפית אתו"),
    ("Exod.30.4", "ושתי טבעות"),
    ("Exod.30.5", "ועשית את הבדים"),
    ("Exod.30.6", "ונתתה אתו לפני"),
    ("Exod.30.7", "והקטיר עליו"),
    ("Exod.30.8", "ובהעלות אהרן"),
    ("Exod.30.9", "לא תעלו עליו"),
    ("Exod.30.10", "וכפר אהרן"),
]
COMMIT = "2f2120286ac48d4ff3d04e0107e33efd864aa9e1"
VERSION = "7.1.3"
README_SHA = "b3b586ed7aa7e9eade7b3f5e1f1aba4dacd93c9f6748f2a65a0ef428602c0f18"
BOOKS = dict(zip("Genesis Exodus Leviticus Numbers Deuteronomy".split(),
                 "Gen Exod Lev Num Deut".split()))
NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
PINNED = {
    "book.tf": "d01865eaac0289b1589ea73e48cbd778bf8970c8c2cc3a41c265143326641ae3",
    "chapter.tf": "c904a65aa2ccc47ce42d17993c3951f9d02e8cb3645e09c05eb8c95b0990f560",
    "verse.tf": "61ec892fe706627282d19195c921e04c1cef50bc5eb054cc3be0a9eb1ade3c32",
    "sign.tf": "8acf12f037619a2f265f57a9a416c9ec1dd129034f2967d9afc7b79144d4065c",
    "otype.tf": "c20a375b21b61809f155abb277fb8fd38a85ba426f3924cbd631119b1ecf7f35",
    "oslots.tf": "7a8f07d9f8a315eda697a89904cdfbfdb9359bd713db18075f6ccd8d4f571917",
    "otext.tf": "d6c71cdcc1b90377fa14037899aadb319c563384dfbfede52a34b651407238fc",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def consonants(text: str) -> str:
    # Decompose Hebrew presentation forms before removing pointing. Preserve
    # matres and final letter forms; neither is silently harmonized.
    return "".join(re.findall(r"[א-ת]", unicodedata.normalize("NFKD", text)))


def written_wlc(verse: ET.Element) -> str:
    # Only direct word children: qere/note text and paragraph signs excluded.
    return " ".join("".join(child.itertext()) for child in verse
                    if child.tag == f"{{{NS['o']}}}w")


def canonical_wlc_keys(verse: ET.Element) -> set[str]:
    """Accept only paragraph signs actually encoded in this written verse."""
    with_signs = " ".join("".join(child.itertext()) for child in verse
                          if child.tag == f"{{{NS['o']}}}w"
                          or (child.tag == f"{{{NS['o']}}}seg"
                              and child.get("type") in {"x-pe", "x-samekh"}))
    return {consonants(written_wlc(verse)), consonants(with_signs)}


def add_unique(index: dict, ref: str, text: str) -> None:
    if ref in index:
        raise ValueError(f"duplicate verse reference: {ref}")
    if not consonants(text):
        raise ValueError(f"empty consonantal verse: {ref}")
    index[ref] = text


def load_sp(directory: Path) -> tuple[dict, list]:
    if sha((directory.parent.parent / "README.md").read_bytes()) != README_SHA:
        raise ValueError("SP README: pinned provenance hash mismatch")
    for name, expected in PINNED.items():
        if sha((directory / name).read_bytes()) != expected:
            raise ValueError(f"SP {name}: pinned input hash mismatch")
    from tf.fabric import Fabric
    api = Fabric(locations=str(directory), silent="deep").load(
        "book chapter verse sign", silent="deep")
    if not api:
        raise ValueError("Text-Fabric could not load the pinned dataset")
    verses, covered_slots = {}, set()
    for node in api.F.otype.s("verse"):
        book, chapter, verse = api.T.sectionFromNode(node)
        if book not in BOOKS:
            raise ValueError(f"unexpected SP book: {book}")
        # The pinned dataset's slots are signs, not words. Read them directly
        # rather than mistaking morphology nodes or separators for the text.
        slots = api.L.d(node, otype="sign")
        if covered_slots.intersection(slots):
            raise ValueError("SP sign slots overlap between verses")
        covered_slots.update(slots)
        signs = [api.F.sign.v(slot) for slot in slots]
        if any(not sign or (sign != " " and not re.fullmatch(r"[א-ת]", sign)) for sign in signs):
            raise ValueError("SP sign alphabet changed; review before filtering")
        text = "".join(signs)
        add_unique(verses, f"{BOOKS[book]}.{chapter}.{verse}", text)
    if covered_slots != set(api.F.otype.s("sign")):
        raise ValueError("Some SP sign slots are not assigned to a screened verse")
    return verses, [{"path": "README.md", "sha256": README_SHA}] + [
        {"path": f"tf/{VERSION}/{name}", "sha256": digest}
        for name, digest in PINNED.items()]


def load_wlc(directory: Path) -> tuple[dict, list]:
    verses, receipts = {}, []
    for book in BOOKS.values():
        raw = (directory / f"{book}.xml").read_bytes()
        receipts.append({"path": f"sources/ot/wlc/{book}.xml", "sha256": sha(raw)})
        for verse in ET.fromstring(raw).findall(".//o:verse", NS):
            ref = verse.get("osisID")
            if not ref or not ref.startswith(book + "."):
                raise ValueError(f"invalid WLC verse ID: {ref}")
            add_unique(verses, ref, written_wlc(verse))
    return verses, receipts


def ref_key(ref: str) -> tuple:
    book, chapter, verse = ref.split(".")
    return (list(BOOKS.values()).index(book), int(chapter), int(verse))


def screen(sp: dict, wlc: dict) -> dict:
    left = {r: consonants(t) for r, t in sp.items()}
    right = {r: consonants(t) for r, t in wlc.items()}
    exact_elsewhere = defaultdict(list)
    for ref, text in right.items():
        exact_elsewhere[(ref.split(".")[0], text)].append(ref)
    records = []
    for ref in sorted(left.keys() & right.keys(), key=ref_key):
        a, b = left[ref], right[ref]
        records.append({
            "reference_label": ref,
            "classification": "consonantal-equal" if a == b else "consonantal-difference",
            "sp_letters": len(a), "wlc_letters": len(b),
            "sp_minus_wlc_letters": len(a) - len(b),
            "other_exact_wlc_reference_candidates": sorted(
                (r for r in exact_elsewhere[(ref.split(".")[0], a)] if r != ref), key=ref_key)
                if a != b else [],
        })
    unequal = [r for r in records if r["classification"] == "consonantal-difference"]
    suspects = [r for r in unequal if r["other_exact_wlc_reference_candidates"]]
    books = []
    for book in BOOKS.values():
        selected = [r for r in records if r["reference_label"].startswith(book + ".")]
        counts = Counter(r["classification"] for r in selected)
        books.append({"book": book,
                      "sp_verse_nodes": sum(r.startswith(book + ".") for r in sp),
                      "wlc_verses": sum(r.startswith(book + ".") for r in wlc),
                      "same_label_pairs": len(selected),
                      "consonantal_equal": counts["consonantal-equal"],
                      "consonantal_different": counts["consonantal-difference"]})
    # Limit exported leads; no external transcription or full verse index.
    largest = sorted(unequal, key=lambda r: (-abs(r["sp_minus_wlc_letters"]),
                                           ref_key(r["reference_label"])))[:20]
    return {
        "summary": {"sp_verse_nodes": len(sp), "wlc_verses": len(wlc),
                    "same_label_pairs": len(records),
                    "consonantal_equal": len(records) - len(unequal),
                    "consonantal_different": len(unequal),
                    "different_pairs_with_other_exact_wlc_candidates": len(suspects)},
        "books": books,
        "sp_only_reference_labels": sorted(left.keys() - right.keys(), key=ref_key),
        "wlc_only_reference_labels": sorted(right.keys() - left.keys(), key=ref_key),
        "numbering_or_repetition_review": suspects,
        "largest_length_difference_leads": largest,
        "lead_selection": "20 largest absolute consonantal-length deltas at shared labels, ties in canonical order; not historical priority or English-impact ranking",
    }


def build(directory: Path, root: Path = ROOT) -> dict:
    sp, sp_inputs = load_sp(directory)
    wlc, wlc_inputs = load_wlc(root / "sources/ot/wlc")
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-04",
        "scope": "All five books in one pinned Samaritan transcription versus vendored WLC; same-reference-label consonantal screen only",
        "source": {"url": f"https://github.com/DT-UCPH/sp/tree/{COMMIT}",
                   "version": VERSION, "attribution": "Hojgaard, Naaijer and Schorch, Text-Fabric Dataset of the Samaritan Pentateuch; Samaritanus project",
                   "upstream_license": "CC BY-NC 4.0; private research input, not relicensed or vendored",
                   "manuscript_basis": "Dublin Chester Beatty Library 751 through Deut 32:36; Garizim 1 from Deut 32:36b; boundary verse is composite",
                   "input_integrity": "All sign slots assigned exactly once to screened verses; expected Hebrew-letter/space alphabet checked; all required feature files and README hash-pinned",
                   "sp_inputs": sp_inputs, "wlc_inputs": wlc_inputs},
        "normalization": "NFKD, Hebrew consonants U+05D0..U+05EA only; exclude WLC qere/notes/paragraph signs; ignore word division, vowels, accents and punctuation; preserve matres and final forms",
        "policy": {"same_label_proves_alignment": False,
                   "difference_proves_source_error": False,
                   "equal_consonants_prove_equal_meaning": False,
                   "all_samaritan_manuscripts_collated": False,
                   "all_ot_sources_covered": False,
                   "canonical_change_applied": False,
                   "export_contains_source_text": False},
        **screen(sp, wlc),
    }


def split_by_anchors(text: str, anchors: list[tuple[str, str]]) -> list[dict]:
    starts = []
    for ref, anchor in anchors:
        if text.count(anchor) != 1:
            raise ValueError(f"{ref}: alignment anchor absent or ambiguous")
        starts.append(text.index(anchor))
    if not starts or starts[0] != 0 or starts != sorted(set(starts)):
        raise ValueError("alignment must cover from the start in strict source order")
    ends = starts[1:] + [len(text)]
    return [{"reference": ref, "start": start, "end": end,
             "text": text[start:end]}
            for (ref, _), start, end in zip(anchors, starts, ends)]


def build_incense(directory: Path, greek_path: Path, root: Path = ROOT) -> dict:
    sp, sp_inputs = load_sp(directory)
    wlc, wlc_inputs = load_wlc(root / "sources/ot/wlc")
    canonical_keys = {v.get("osisID"): canonical_wlc_keys(v)
                      for v in ET.parse(root / "sources/ot/wlc/Exod.xml").findall(".//o:verse", NS)}
    raw = greek_path.read_bytes()
    if sha(raw) != GREEK_SHA:
        raise ValueError("Greek Exodus differs from pinned input")
    greek = {}
    for verse in json.loads(raw):
        if verse["ref"] in greek:
            raise ValueError("duplicate Greek reference")
        greek[verse["ref"]] = " ".join(word["surface"] for word in verse["words"])
    text = sp["Exod.26.35"]
    segments = []
    import yaml
    for span in split_by_anchors(text, INCENSE_ANCHORS):
        ref = span["reference"]
        book, chapter, verse = ref.split(".")
        greek_ref = f"{book} {chapter}:{verse}"
        if greek_ref not in greek or ref not in wlc:
            raise ValueError(f"missing comparison reference: {ref}")
        relative = f"translation/ot/exodus/{int(chapter):03d}/{int(verse):03d}.yaml"
        canonical_raw = (root / relative).read_bytes()
        canonical = yaml.safe_load(canonical_raw)
        canonical_key = consonants(canonical["source"]["text"])
        if canonical_key not in canonical_keys[ref]:
            raise ValueError(f"POB-to-WLC source alignment changed: {ref}")
        segments.append({
            "wlc_reference": ref, "greek_reference": greek_ref,
            "sp_reference": "Exod.26.35",
            "sp_character_span": [span["start"], span["end"]],
            "sp_segment_sha256": sha(span["text"].encode()),
            "sp_consonant_count": len(consonants(span["text"])),
            "wlc_consonant_count": len(consonants(wlc[ref])),
            "consonantal_comparison": "equal" if consonants(span["text"]) == consonants(wlc[ref]) else "different",
            "greek_surface_sha256": sha(greek[greek_ref].encode()),
            "pob_baseline": {"repo_path": relative, "sha256": sha(canonical_raw),
                             "alignment": "written-consonants" if canonical_key == consonants(wlc[ref]) else "written-consonants-with-encoded-paragraph-signs"},
            "historical_selection": "not-adjudicated",
        })
    return {
        "schema_version": "1.0.0", "checked_date": "2026-09-05",
        "scope": "Lossless editor-defined segmentation of one extended SP verse node against WLC/Greek 26:35 and 30:1-10; not a universal alignment algorithm",
        "source": {"sp_commit": COMMIT, "sp_version": VERSION,
                   "sp_inputs": sp_inputs, "wlc_inputs": wlc_inputs,
                   "greek_commit": "c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2",
                   "greek_file": "db/seeds/lxx_morph/exodus.json",
                   "greek_file_sha256": GREEK_SHA,
                   "sp_reference": "Exod.26.35", "sp_sign_text_sha256": sha(text.encode()),
                   "sp_character_count": len(text)},
        "alignment_basis": "Manually identified Hebrew instruction boundaries; each anchor unique in the pinned SP sign text. Zero-based half-open character spans include trailing spaces and reassemble the whole node exactly. Greek references checked for presence and read separately; no automatic Greek-to-Hebrew retroversion.",
        "policy": {"alignment_is_historical_selection": False,
                   "same_order_proves_same_wording": False,
                   "missing_verse_label_proves_missing_text": False,
                   "all_samaritan_witnesses_collated": False,
                   "generated_images_used": False,
                   "export_contains_source_text": False,
                   "canonical_wording_changed": False},
        "segments": segments,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sp_tf_directory", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--incense-alignment", action="store_true")
    parser.add_argument("--greek-json", type=Path)
    args = parser.parse_args()
    if args.incense_alignment != bool(args.greek_json):
        parser.error("--incense-alignment and --greek-json must be supplied together")
    result = build_incense(args.sp_tf_directory, args.greek_json) if args.incense_alignment else build(args.sp_tf_directory)
    output = INCENSE_OUT if args.incense_alignment else OUT
    if args.verify_only:
        if json.loads(output.read_text()) != result:
            raise SystemExit("Saved Samaritan screen differs from recomputation")
        print(f"Verified {output.name} against all pinned inputs and current baselines")
    else:
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(result.get("summary", {"aligned_segments": len(result.get("segments", []))})))


if __name__ == "__main__":
    main()
