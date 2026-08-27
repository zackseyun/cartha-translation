#!/usr/bin/env python3
"""Build an editorial queue for text-grounded Bible narrative reconstructions.

This is deliberately separate from ``bible_visual_aid_map.py``.  The original
map discovers reference figures (objects, places, maps, processes, and
diagrams).  This tool finds passages where seeing the *described moment* can
materially clarify people, positions, movement, or explicit emotion.

The output is still only an editorial queue.  A match never authorizes an
image by itself: every row must be checked against the narrative lane in
``docs/BIBLE_VISUAL_AIDS.md`` before generation and publication.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

try:
    from tools.bible_visual_aid_map import CANON_66, load_book
except ModuleNotFoundError:  # direct ``python tools/...py`` execution
    from bible_visual_aid_map import CANON_66, load_book


# Books whose primary mode contains narrated events.  Prophetic books with
# substantial narrative episodes remain eligible, while poetry, wisdom,
# epistles, and apocalyptic books are omitted by default rather than forcing
# literal scenes onto discourse or symbolic imagery.
NARRATIVE_BOOKS = {
    "genesis", "exodus", "numbers", "deuteronomy", "joshua", "judges",
    "ruth", "1-samuel", "2-samuel", "1-kings", "2-kings",
    "1-chronicles", "2-chronicles", "ezra", "nehemiah", "esther", "job",
    "isaiah", "jeremiah", "ezekiel", "daniel", "hosea", "jonah", "amos",
    "haggai", "zechariah", "matthew", "mark", "luke", "john", "acts",
}

# Symbolic/apocalyptic passages should remain diagrams, not narrative scenes.
VISION_RE = re.compile(
    r"\b(?:vision|visions|in a dream|I saw in the night|four beasts|living "
    r"creatures|wheels within wheels|seven heads|ten horns|flying scroll|"
    r"measuring basket|woman clothed with the sun)\b",
    re.IGNORECASE,
)

# Pure speeches, laws, measurements, and lists can contain common action words
# but rarely benefit from a narrative reconstruction.
NON_SCENE_RE = re.compile(
    r"\b(?:these are the generations|the sons of|the descendants of|according "
    r"to their clans|its length was|its width was|its height was|you shall "
    r"make|this is the law|these are the statutes|the following are the "
    r"measurements)\b",
    re.IGNORECASE,
)

SENSITIVE_RE = re.compile(
    r"\b(?:rape|violated|lay with her by force|dismembered|beheaded|impaled|"
    r"hanged him|struck him dead|killed him|slew him|blood flowed|bowels|"
    r"burned them|stoned him|crucified|scourged|flogged)\b",
    re.IGNORECASE,
)

HEAVENLY_RE = re.compile(
    r"\b(?:angel|angels|messenger of (?:Yahweh|the Lord)|the Lord appeared|"
    r"Yahweh appeared|Jesus|the Son of Man|Holy Spirit)\b",
    re.IGNORECASE,
)

DEFAULT_CHARACTER_REGISTRY = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "bible_visual_aid_character_registry.json"
)


@dataclass(frozen=True)
class SceneCue:
    key: str
    weight: int
    pattern: re.Pattern[str]
    reason: str


def _cue(key: str, weight: int, pattern: str, reason: str) -> SceneCue:
    return SceneCue(key, weight, re.compile(pattern, re.IGNORECASE), reason)


SCENE_CUES = (
    _cue(
        "explicit_positions", 5,
        r"\b(?:one at the head|one at the feet|at (?:his|her|their) feet|"
        r"at the right hand|at the left hand|between them|in their midst|"
        r"behind him|before him|opposite (?:him|her|them)|beside (?:him|her|them)|"
        r"leaned back|reclining beside|stood around|sat around)\b",
        "The verse depends on where participants are positioned.",
    ),
    _cue(
        "encounter", 4,
        r"\b(?:met him|met her|met them|came to meet|ran to meet|approached him|"
        r"approached her|appeared to|stood before|stood beside|entered the room|"
        r"entered the house|came into the house|came into the tomb|looked into|"
        r"turned around and saw|lifted (?:his|her) eyes and saw)\b",
        "A face-to-face encounter or threshold moment is central.",
    ),
    _cue(
        "embodied_emotion", 4,
        r"\b(?:wept|weeping|cried aloud|embraced|kissed|fell on (?:his|her) neck|"
        r"fell at (?:his|her) feet|bowed to the ground|knelt|tore (?:his|her) "
        r"clothes|covered (?:his|her) face|beat (?:his|her) breast|rejoiced|"
        r"was astonished|were astonished|was amazed|were amazed|trembled|"
        r"was afraid|were afraid|grieved deeply)\b",
        "The text gives visible emotion or bodily response.",
    ),
    _cue(
        "meaningful_action", 3,
        r"\b(?:washed (?:his|her|their) feet|broke the bread|broke bread|"
        r"poured .* oil|anointed|touched (?:him|her)|took (?:him|her) by the hand|"
        r"laid (?:his|her|their) hands on|carried him|carried her|lowered him|"
        r"lifted him|lifted her|spread .* cloak|covered him|wrapped him|"
        r"opened the door|rolled away the stone|drew water|gave him a drink|"
        r"placed .* in (?:his|her) arms|sat down together)\b",
        "A concrete human action carries the meaning of the moment.",
    ),
    _cue(
        "sensitive_action", 5,
        r"\b(?:flogged|scourged|crucified|stoned him|stoned her|beheaded|"
        r"impaled|struck him dead|struck her dead)\b",
        "A consequential action may warrant a restrained, heightened-care reconstruction.",
    ),
    _cue(
        "movement", 2,
        r"\b(?:ran|hurried|fled|followed|went out|came out|entered|departed|"
        r"crossed over|climbed|descended|ascended|stooped|turned around|"
        r"walked beside|walked ahead|walked behind)\b",
        "Movement through the setting helps the reader follow the scene.",
    ),
    _cue(
        "heavenly_encounter", 5,
        r"\b(?:an angel appeared|the angel of (?:Yahweh|the Lord) appeared|"
        r"two angels|angels in white|messengers in shining garments|"
        r"Jesus appeared|Jesus came and stood|the Lord stood beside him)\b",
        "A passage-described heavenly encounter is essential to the scene.",
    ),
    _cue(
        "transfiguration", 8,
        r"\b(?:transfigured|appearance of his face became different|"
        r"his clothes became (?:white|dazzling|radiant))\b",
        "The visible change and the participants' positions are central to the passage.",
    ),
    _cue(
        "shared_setting", 2,
        r"\b(?:at the table|in the upper room|inside the house|at the well|"
        r"by the well|at the tomb|inside the tomb|in the boat|on the shore|"
        r"on the road|at the gate|in the courtyard|before the king|"
        r"before the governor|in the synagogue|in the temple)\b",
        "A shared physical setting organizes the participants.",
    ),
    _cue(
        "direct_exchange", 1,
        r"[“\"]|\b(?:said to him|said to her|said to them|answered him|"
        r"answered her|asked him|asked her|called to him|called to her)\b",
        "The scene contains a direct exchange between participants.",
    ),
)


@dataclass
class SceneHit:
    book_slug: str
    book: str
    chapter: int
    verse: int
    verse_text: str
    context_text: str
    score: int = 0
    cues: dict[str, list[str]] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    sensitive: bool = False
    heavenly: bool = False

    @property
    def id(self) -> str:
        return f"{self.book_slug}-{self.chapter}-{self.verse}"

    @property
    def reference(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"


def score_scene(
    book_slug: str,
    book: str,
    chapter: int,
    verse: int,
    verse_text: str,
    context_text: str | None = None,
) -> SceneHit | None:
    if book_slug not in NARRATIVE_BOOKS:
        return None
    context = context_text or verse_text
    if VISION_RE.search(context) or NON_SCENE_RE.search(verse_text):
        return None

    hit = SceneHit(book_slug, book, chapter, verse, verse_text, context)
    for cue in SCENE_CUES:
        matches = [m.group(0) for m in cue.pattern.finditer(context)]
        if not matches:
            continue
        distinct = list(dict.fromkeys(m.lower() for m in matches))
        # Repeated dialogue marks should not overpower concrete scene evidence.
        contribution = cue.weight if cue.key == "direct_exchange" else min(
            cue.weight + len(distinct) - 1, cue.weight + 2
        )
        hit.score += contribution
        hit.cues[cue.key] = distinct[:5]
        hit.reasons.append(cue.reason)

    if not hit.cues:
        return None
    # A quotation or generic movement alone is not enough for an illustration.
    concrete = set(hit.cues) - {"direct_exchange", "movement", "shared_setting"}
    if not concrete and hit.score < 6:
        return None
    hit.score = min(hit.score, 15)
    hit.reasons = list(dict.fromkeys(hit.reasons))
    hit.sensitive = bool(SENSITIVE_RE.search(context))
    hit.heavenly = bool(HEAVENLY_RE.search(context))
    return hit


def load_character_registry(path: Path = DEFAULT_CHARACTER_REGISTRY) -> dict:
    return json.loads(path.read_text())


def character_ids_for_text(text: str, registry: dict) -> list[str]:
    found = []
    for character_id, entry in registry.get("characters", {}).items():
        aliases = entry.get("aliases", [])
        if any(re.search(rf"\b{re.escape(alias)}\b", text, re.IGNORECASE) for alias in aliases):
            found.append(character_id)
    return found


def character_ids_for_hit(hit: SceneHit, registry: dict) -> list[str]:
    # Normally lock only names in the anchor verse; nearby explanatory mentions
    # (for example "the gift Moses commanded") are not scene participants.
    # The transfiguration is the narrow exception because the adjacent verses
    # deliberately distribute its named participants across the scene.
    text = hit.context_text if "transfiguration" in hit.cues else hit.verse_text
    return character_ids_for_text(text, registry)


def character_reference_block(character_ids: list[str], registry: dict) -> str:
    if not character_ids:
        return ""
    parts = []
    for character_id in character_ids:
        entry = registry["characters"][character_id]
        refs = entry.get("reference_images", [])
        if entry.get("status") == "locked" and not refs:
            raise ValueError(f"Locked character {character_id} has no reference images")
        if refs:
            parts.append(
                f"{character_id}: attach the exact locked refs " + ", ".join(refs)
            )
        else:
            parts.append(
                f"{character_id}: use {entry['card']} and save the approved first "
                "appearance as this lane's stable visual reference before reuse"
            )
    identity_isolation = registry.get("policy", {}).get(
        "identity_isolation_rule", ""
    ).strip()
    isolation_text = (
        f" Identity isolation: {identity_isolation}" if identity_isolation else ""
    )
    return (
        " Character continuity lock: " + "; ".join(parts) + "." + isolation_text
    )


def narrative_prompt(hit: SceneHit, registry: dict | None = None) -> str:
    registry = registry or load_character_registry()
    character_ids = character_ids_for_hit(hit, registry)
    continuity = character_reference_block(character_ids, registry)
    care = []
    if hit.heavenly:
        care.append(
            "Depict only heavenly participants explicitly described by the text; "
            "do not invent wings, halos, glow, or supernatural effects."
        )
    if hit.sensitive:
        care.append(
            "Heightened dignity review: no gore, nudity, sexualized framing, or "
            "suffering as spectacle. Prefer aftermath, distance, or implied action."
        )
    care_text = " ".join(care) or "Preserve human dignity and avoid spectacle."
    return (
        f"Narrative reconstruction for {hit.reference}. Passage context: "
        f"{hit.context_text} Show the passage-described moment in a restrained, "
        "historically plausible way. Make the participants' positions, movement, "
        "or explicit emotion immediately understandable. Keep faces "
        "non-authoritative and do not add people, actions, symbols, or doctrinal "
        "claims absent from the text. Matte realistic historical reconstruction, "
        "natural light, documentary realism, 16:9 landscape. No baked-in text, "
        f"labels, title, quotation, or watermark.{continuity} {care_text}"
    )


def select_scenes(
    hits: list[SceneHit],
    min_score: int,
    per_chapter_cap: int,
    character_registry: dict | None = None,
) -> list[dict]:
    character_registry = character_registry or load_character_registry()
    by_chapter: dict[int, list[SceneHit]] = defaultdict(list)
    for hit in hits:
        if hit.score >= min_score:
            by_chapter[hit.chapter].append(hit)

    rows: list[dict] = []
    for chapter, candidates in sorted(by_chapter.items()):
        candidates.sort(key=lambda h: (-h.score, h.verse))
        chosen: list[SceneHit] = []
        for hit in candidates:
            if len(chosen) >= per_chapter_cap:
                break
            if all(abs(hit.verse - other.verse) >= 4 for other in chosen):
                chosen.append(hit)
        for hit in sorted(chosen, key=lambda h: h.verse):
            character_ids = character_ids_for_hit(hit, character_registry)
            character_refs = {
                character_id: character_registry["characters"][character_id]
                for character_id in character_ids
            }
            rows.append({
                "id": hit.id,
                "book": hit.book,
                "book_slug": hit.book_slug,
                "chapter": hit.chapter,
                "verse": hit.verse,
                "reference": hit.reference,
                "score": hit.score,
                "aid_type": "scene",
                "aid_type_label": "Narrative reconstruction",
                "format": "text-free narrative reconstruction",
                "working_title": f"Narrative moment: {hit.reference}",
                "cues": hit.cues,
                "reasons": hit.reasons,
                "sensitive": hit.sensitive,
                "heavenly": hit.heavenly,
                "verse_text": hit.verse_text,
                "context_text": hit.context_text,
                "characters": character_ids,
                "character_refs": character_refs,
                "suggested_prompt": narrative_prompt(hit, character_registry),
                "prompt_version": "narrative-reconstruction-v3-identity-isolated",
                "status": "needs_editorial_review",
            })
    return rows


def _chapter_context(verses: list[tuple[int, int, str]]) -> dict[tuple[int, int], str]:
    by_chapter: dict[int, list[tuple[int, str]]] = defaultdict(list)
    for chapter, verse, text in verses:
        by_chapter[chapter].append((verse, text))
    context: dict[tuple[int, int], str] = {}
    for chapter, chapter_verses in by_chapter.items():
        chapter_verses.sort()
        for i, (verse, _) in enumerate(chapter_verses):
            start = max(0, i - 1)
            end = min(len(chapter_verses), i + 2)
            context[(chapter, verse)] = " ".join(
                f"v{v}: {text}" for v, text in chapter_verses[start:end]
            )
    return context


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--books-root", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--min-score", type=int, default=7)
    ap.add_argument("--per-chapter-cap", type=int, default=1)
    ap.add_argument("--books", nargs="*")
    ap.add_argument("--exclude-ids", type=Path)
    ap.add_argument(
        "--exclude-dispositions", type=Path,
        help="JSON editorial-disposition array; rejected and published rows are skipped",
    )
    ap.add_argument(
        "--exclude-radius", type=int, default=2,
        help="Skip verses this many positions from an existing placement (default 2)",
    )
    ap.add_argument(
        "--character-registry", type=Path,
        default=DEFAULT_CHARACTER_REGISTRY,
        help="Persistent named-character registry used to lock recurring identities",
    )
    args = ap.parse_args()
    character_registry = load_character_registry(args.character_registry)

    published: set[str] = set()
    if args.exclude_ids and args.exclude_ids.exists():
        published = set(json.loads(args.exclude_ids.read_text()))
    editorial_rejections: set[str] = set()
    if args.exclude_dispositions and args.exclude_dispositions.exists():
        editorial_rejections = {
            row["id"] for row in json.loads(args.exclude_dispositions.read_text())
            if row.get("disposition") in {"reject", "published"} and row.get("id")
        }

    def near_published(slug: str, chapter: int, verse: int) -> bool:
        return any(
            f"{slug}-{chapter}-{v}" in published
            for v in range(max(1, verse - args.exclude_radius), verse + args.exclude_radius + 1)
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "books").mkdir(exist_ok=True)
    wanted = args.books or [slug for slug in CANON_66 if slug in NARRATIVE_BOOKS]
    summary_books = []
    total = 0
    flags: Counter[str] = Counter()

    for slug in wanted:
        if slug not in NARRATIVE_BOOKS:
            continue
        path = args.books_root / f"{slug}.json"
        if not path.exists():
            continue
        _, verses = load_book(path)
        context = _chapter_context(verses)
        hits = []
        for chapter, verse, text in verses:
            if published and near_published(slug, chapter, verse):
                continue
            if f"{slug}-{chapter}-{verse}" in editorial_rejections:
                continue
            hit = score_scene(
                slug, CANON_66[slug], chapter, verse, text,
                context.get((chapter, verse), text),
            )
            if hit:
                hits.append(hit)
        rows = select_scenes(
            hits, args.min_score, args.per_chapter_cap, character_registry
        )
        for row in rows:
            if row["sensitive"]:
                flags["sensitive"] += 1
            if row["heavenly"]:
                flags["heavenly"] += 1
        chapters = max((c for c, _, _ in verses), default=0)
        payload = {
            "version": 1,
            "lane": "narrative-reconstruction-v1",
            "book": CANON_66[slug],
            "book_slug": slug,
            "chapters": chapters,
            "verses": len(verses),
            "anchors": len(rows),
            "aids": rows,
        }
        (args.out_dir / "books" / f"{slug}.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        )
        summary_books.append({
            "book": CANON_66[slug], "slug": slug, "anchors": len(rows),
        })
        total += len(rows)

    summary = {
        "version": 1,
        "lane": "narrative-reconstruction-v2-character-locked",
        "character_registry": str(args.character_registry),
        "min_score": args.min_score,
        "per_chapter_cap": args.per_chapter_cap,
        "exclude_radius": args.exclude_radius,
        "editorial_exclusions": len(editorial_rejections),
        "canon_anchors": total,
        "flags": dict(flags),
        "books": summary_books,
    }
    (args.out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
