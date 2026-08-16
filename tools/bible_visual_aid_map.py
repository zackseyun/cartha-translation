#!/usr/bin/env python3
"""Build the abundant, canon-wide Bible visual-aid map.

Where ``bible_visual_aid_candidates.py`` was a conservative discovery net for a
rare, reference-figure-only layer, this tool maps *every* verse in the 66-book
canon that a visual could plausibly help, across an expanded taxonomy of aid
types (see ``docs/BIBLE_VISUAL_AIDS.md`` — "Abundant catalog"). It reads the
compiled per-book reader JSON (the same files the website ships), so it runs
in seconds without PyYAML or the heavy translation records.

Output is a per-book JSON map plus a canon summary. Every row is explainable
(matched cues + reasons) and carries a proposed aid type, format, working
title, and a Codex Image Gen prompt in the house style for that type. The map
is an editorial queue: it decides *where* aids go; a human still approves
each asset before publish.

Example:
    python tools/bible_visual_aid_map.py \
      --books-root ../cartha.website/public/bibles/pob/books \
      --out-dir /tmp/bible-visual-aid-map
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# Canon
# --------------------------------------------------------------------------

CANON_66: dict[str, str] = {
    # slug: display name (in canonical order)
    "genesis": "Genesis", "exodus": "Exodus", "leviticus": "Leviticus",
    "numbers": "Numbers", "deuteronomy": "Deuteronomy", "joshua": "Joshua",
    "judges": "Judges", "ruth": "Ruth", "1-samuel": "1 Samuel",
    "2-samuel": "2 Samuel", "1-kings": "1 Kings", "2-kings": "2 Kings",
    "1-chronicles": "1 Chronicles", "2-chronicles": "2 Chronicles",
    "ezra": "Ezra", "nehemiah": "Nehemiah", "esther": "Esther", "job": "Job",
    "psalms": "Psalms", "proverbs": "Proverbs", "ecclesiastes": "Ecclesiastes",
    "song-of-solomon": "Song of Solomon", "isaiah": "Isaiah",
    "jeremiah": "Jeremiah", "lamentations": "Lamentations",
    "ezekiel": "Ezekiel", "daniel": "Daniel", "hosea": "Hosea", "joel": "Joel",
    "amos": "Amos", "obadiah": "Obadiah", "jonah": "Jonah", "micah": "Micah",
    "nahum": "Nahum", "habakkuk": "Habakkuk", "zephaniah": "Zephaniah",
    "haggai": "Haggai", "zechariah": "Zechariah", "malachi": "Malachi",
    "matthew": "Matthew", "mark": "Mark", "luke": "Luke", "john": "John",
    "acts": "Acts", "romans": "Romans", "1-corinthians": "1 Corinthians",
    "2-corinthians": "2 Corinthians", "galatians": "Galatians",
    "ephesians": "Ephesians", "philippians": "Philippians",
    "colossians": "Colossians", "1-thessalonians": "1 Thessalonians",
    "2-thessalonians": "2 Thessalonians", "1-timothy": "1 Timothy",
    "2-timothy": "2 Timothy", "titus": "Titus", "philemon": "Philemon",
    "hebrews": "Hebrews", "james": "James", "1-peter": "1 Peter",
    "2-peter": "2 Peter", "1-john": "1 John", "2-john": "2 John",
    "3-john": "3 John", "jude": "Jude", "revelation": "Revelation",
}

VISIONARY_BOOKS = {"revelation", "ezekiel", "daniel", "zechariah"}

# --------------------------------------------------------------------------
# Aid types — the expanded taxonomy
# --------------------------------------------------------------------------
# Each type carries a house-style prompt frame. Reference-figure types keep the
# annotated matte-reconstruction look; the newer types (bird's-eye scene,
# infographic, timeline, comparison, botanical/zoological plate) add formats
# that are still explanatory rather than dramatic.

@dataclass(frozen=True)
class AidType:
    key: str
    label: str
    format_hint: str
    style: str  # prompt frame


AID_TYPES: dict[str, AidType] = {t.key: t for t in [
    AidType(
        "place", "Place reconstruction",
        "wide or elevated annotated reconstruction",
        "Matte realistic historical-reconstruction painting of the place as it "
        "would appear on an ordinary day, natural daylight, museum-plate quality, "
        "3-5 labeled callouts (dark rounded chips, white text, thin leader lines) "
        "naming parts and functions.",
    ),
    AidType(
        "map", "Map / route",
        "labeled map, route, or terrain profile",
        "Clean cartographic map in a warm parchment-and-ink style with subtle "
        "terrain shading, clearly lettered place names, route arrows, a scale "
        "bar, and a north arrow; no decorative sea monsters or clutter.",
    ),
    AidType(
        "object", "Object plate",
        "museum-style object plate",
        "Museum catalog plate: the object rendered accurately on a neutral "
        "background, exploded or cutaway where useful, 3-6 labeled callouts "
        "naming parts, materials, dimensions, and use.",
    ),
    AidType(
        "how", "How it worked",
        "process plate or step diagram",
        "Explanatory process plate showing the practice step by step "
        "(numbered panels or a single annotated scene), anonymous small figures "
        "only, tools and materials labeled, documentary tone.",
    ),
    AidType(
        "scale", "Scale & measurement",
        "scale diagram / plan view",
        "Clean measured diagram with dimensions converted to modern units, a "
        "human silhouette or familiar object for scale, plan and elevation "
        "where helpful, minimal color, technical-illustration style.",
    ),
    AidType(
        "nature", "Plant / animal / phenomenon plate",
        "naturalist plate",
        "Naturalist field-guide plate of the plant, animal, or natural "
        "phenomenon, accurate to the Levant, with labeled parts, size "
        "reference, and the detail the verse relies on.",
    ),
    AidType(
        "birdseye", "Bird's-eye scene",
        "elevated wide view of the setting with the story's positions marked",
        "High elevated wide view of the setting rendered as a matte "
        "reconstruction, with the narrative's positions and movements marked "
        "by labeled markers and arrows rather than by depicting the people; "
        "no faces, no drama, no divine figures.",
    ),
    AidType(
        "compare", "Side-by-side comparison",
        "two- or three-panel comparison",
        "Two or three labeled panels comparing the things the verse contrasts "
        "(sizes, kinds, before/after, right/wrong practice), consistent lighting "
        "and scale across panels, clear captions under each.",
    ),
    AidType(
        "timeline", "Timeline / sequence",
        "horizontal timeline or sequence strip",
        "Clean horizontal timeline or sequence strip with dated or ordered "
        "nodes, short labels, and small icon vignettes; parchment palette; "
        "no portraits.",
    ),
    AidType(
        "people", "Who's who / relationships",
        "labeled relationship or genealogy chart",
        "Clear relationship chart (family tree, alliance, or succession) with "
        "named nodes and labeled edges; small neutral silhouettes, no faces; "
        "parchment palette.",
    ),
    AidType(
        "structure", "Structure of the passage",
        "diagram of the argument, list, or pattern",
        "Clean infographic diagram of the passage's structure (parallel lines, "
        "numbered list, chiasm, cycle) with short quoted labels; typographic, "
        "restrained color, no imagery of people.",
    ),
    AidType(
        "symbol", "Symbol explainer",
        "labeled diagram of a symbolic image, presented as an explainer, never as a literal scene",
        "Schematic explainer of the symbolic image drawn as a labeled diagram "
        "(icons and callouts explaining what each element stands for), clearly "
        "not a literal depiction; parchment palette; no beasts rendered "
        "realistically, no heavenly beings.",
    ),
]}

# --------------------------------------------------------------------------
# Cue lexicon — (type, weight, terms, reason)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Cue:
    aid_type: str
    weight: int
    pattern: re.Pattern[str]
    reason: str
    terms: tuple[str, ...]


def _cue(aid_type: str, weight: int, words: str, reason: str) -> Cue:
    terms = tuple(w.strip() for w in words.split("|") if w.strip())
    pattern = re.compile(
        r"\b(?:" + "|".join(re.escape(t) for t in terms) + r")\b", re.IGNORECASE
    )
    return Cue(aid_type, weight, pattern, reason, terms)


CUES: tuple[Cue, ...] = (
    # ---- places
    _cue("place", 3,
         "temple|tabernacle|sanctuary|holy place|most holy|portico|colonnade|"
         "courtyard|court of|inner court|outer court|gate of|gatehouse|"
         "synagogue|palace|fortress|citadel|stronghold|tower|city wall|"
         "upper room|guest room|inn|prison|dungeon|cistern|well|pool|"
         "threshing floor|winepress|sheepfold|tomb|sepulcher|cave|"
         "tent|booth|altar|high place|market|marketplace|theater|"
         "stadium|barracks|praetorium|judgment seat|treasury|storehouse|"
         "granary|barn|vineyard|garden|olive grove|watchtower|"
         "house|roof|housetop|threshold|doorpost|lintel|"
         "ship|boat|harbor|road|highway|bridge|aqueduct",
         "A built place or spatial arrangement the text assumes."),
    # ---- geography / travel
    _cue("map", 3,
         "Jerusalem|Judea|Galilee|Samaria|Bethlehem|Nazareth|Capernaum|"
         "Bethany|Jericho|Bethsaida|Tyre|Sidon|Damascus|Antioch|Ephesus|"
         "Corinth|Athens|Rome|Philippi|Thessalonica|Berea|Caesarea|Joppa|"
         "Egypt|Babylon|Assyria|Nineveh|Persia|Media|Ur|Haran|Canaan|"
         "Sinai|Horeb|Kadesh|Moab|Edom|Ammon|Philistia|Gaza|Ashkelon|"
         "Ashdod|Gath|Ekron|Hebron|Beersheba|Dan|Shechem|Bethel|Gilgal|"
         "Shiloh|Ramah|Gibeah|Mizpah|Gibeon|Lachish|Megiddo|Jezreel|"
         "Carmel|Tabor|Gilboa|Hermon|Lebanon|Bashan|Gilead|Jordan|"
         "Sea of Galilee|Dead Sea|Salt Sea|Red Sea|Great Sea|Mediterranean|"
         "Euphrates|Tigris|Nile|Kidron|Hinnom|Mount of Olives|Zion|Moriah|"
         "Cyprus|Crete|Malta|Patmos|Macedonia|Achaia|Asia|Galatia|"
         "Cappadocia|Pontus|Bithynia|Pamphylia|Lycia|Cilicia|Tarsus|"
         "Iconium|Lystra|Derbe|Miletus|Troas|Smyrna|Pergamum|Thyatira|"
         "Sardis|Philadelphia|Laodicea|Colossae|Hierapolis|Tarshish|"
         "Sheba|Ophir|Cush|Ethiopia|Elam|Susa|Ecbatana|"
         "went up to|went down to|journeyed|set out|traveled|traveled|"
         "sailed|crossed over|passed through|the way to|the road to|"
         "wilderness of|valley of|plain of|hill country|"
         "border|boundary|territory|allotment|"
         "day's journey|miles|stadia|furlongs",
         "Geography, a route, or a named place a map would fix."),
    # ---- objects & material culture
    _cue("object", 3,
         "denarius|denarii|talent|talents|shekel|shekels|mina|drachma|"
         "lepta|mite|coin|coins|penny|ephah|omer|hin|bath|homer|cor|seah|"
         "cubit|cubits|span|handbreadth|reed|scroll|scrolls|book|"
         "parchment|papyrus|ink|pen|tablet|seal|signet|ring|"
         "lampstand|lamp|lamps|oil|wick|censer|incense|firepan|"
         "ark of the covenant|mercy seat|cherubim|table of|showbread|"
         "bread of the presence|veil|curtain|screen|"
         "ephod|breastpiece|breastplate|robe|tunic|turban|sash|"
         "phylacteries|tassels|fringe|sandal|sandals|staff|rod|"
         "sling|sword|spear|javelin|bow|arrow|arrows|shield|buckler|"
         "helmet|armor|coat of mail|greaves|chariot|chariots|"
         "yoke|plow|plough|goad|sickle|winnowing fork|shovel|"
         "millstone|hand mill|mortar|pestle|oven|kneading|"
         "wineskin|wineskins|jar|jars|pitcher|basin|bowl|cup|"
         "flask|alabaster|ointment|perfume|spikenard|myrrh|"
         "frankincense|aloes|spices|nard|"
         "net|nets|dragnet|hook|anchor|anchors|rudder|sail|mast|"
         "loom|shuttle|spindle|distaff|needle|"
         "trumpet|shofar|ram's horn|harp|lyre|timbrel|tambourine|"
         "cymbals|flute|pipe|"
         "manger|cradle|bed|couch|table|throne|footstool|"
         "crown|diadem|scepter|"
         "balances|scales|weights|measure|measuring line|plumb line|"
         "cistern|bucket|rope|cord|tent peg|"
         "linen|sackcloth|purple|scarlet|dyed|leather|goatskin|"
         "bricks|mortar|bitumen|pitch|hewn stone|cedar|acacia|"
         "gold|silver|bronze|iron|tin|lead",
         "An object, garment, tool, unit, or material readers cannot picture."),
    # ---- practices / how it worked
    _cue("how", 3,
         "sacrifice|offering|burnt offering|sin offering|grain offering|"
         "peace offering|drink offering|firstfruits|tithe|tithes|"
         "wave offering|laid his hands|lay hands|sprinkle|sprinkled|"
         "anoint|anointed|anointing|circumcis|baptiz|purif|"
         "ceremonially|unclean|clean|wash|washed|washing|"
         "betroth|betrothed|dowry|bride price|wedding|marriage feast|"
         "bridegroom|bridesmaid|"
         "bury|buried|burial|embalm|mourn|mourning|lament|wailing|"
         "harvest|harvesting|reap|reaping|glean|gleaning|sheaves|"
         "thresh|threshing|winnow|winnowing|sow|sowing|sower|"
         "prune|pruning|graft|grafted|tread|treading|press|"
         "shepherd|shepherds|flock|fold|pasture|"
         "fisherman|fishermen|fishing|cast a net|"
         "potter|potter's|clay|kiln|refine|refiner|smelt|furnace|"
         "weav|weaver|spin|spun|dye|"
         "money changer|money changers|tax collector|toll|"
         "bondservant|hired|wages|"
         "vow|Nazirite|fast|fasting|Sabbath|Passover|Pentecost|"
         "Feast of|festival|Booths|Tabernacles|Unleavened|Atonement|"
         "Jubilee|sabbatical|"
         "elders at the gate|"
         "stoning|stoned|flog|flogged|scourg|crucif|"
         "recline|reclining|reclined at table|washed his feet|foot washing|"
         "greet|kiss|"
         "hospitality|lodg|guest",
         "A practice, ritual, trade, or custom that a process plate could unpack."),
    # ---- scale
    _cue("scale", 3,
         "cubits long|cubits wide|cubits high|cubits broad|its length|"
         "its width|its height|the length of|the width of|the height of|"
         "hundred cubits|fifty cubits|thirty cubits|twenty cubits|"
         "ten cubits|measured|measurements|measure the|dimensions|"
         "thousand|ten thousand|hundred thousand|"
         "talents of|shekels of|ephahs of|baths of|cors of|"
         "lived .* years|forty years|seventy years|"
         "forty days|three hundred|six hundred",
         "Numbers, sizes, or durations that a scale diagram makes felt."),
    # ---- nature
    _cue("nature", 2,
         "cedar|cedars|cypress|oak|terebinth|palm|palm tree|"
         "fig|fig tree|figs|olive|olive tree|olives|vine|vines|grape|"
         "grapes|pomegranate|almond|almonds|sycamore|mustard|"
         "wheat|barley|lentil|lentils|beans|millet|spelt|flax|"
         "hyssop|myrtle|acacia|reed|reeds|bulrush|papyrus|thorn|"
         "thorns|thistle|thistles|brier|briers|nettle|"
         "lily|lilies|rose|mandrake|"
         "sheep|lamb|lambs|goat|goats|ox|oxen|bull|calf|heifer|"
         "donkey|colt|mule|horse|horses|camel|camels|"
         "lion|lions|bear|wolf|wolves|leopard|fox|foxes|jackal|"
         "deer|gazelle|hart|hind|wild goat|ibex|"
         "dove|doves|pigeon|sparrow|raven|ravens|eagle|vulture|"
         "owl|stork|hen|rooster|quail|"
         "serpent|snake|viper|adder|scorpion|"
         "locust|locusts|grasshopper|moth|worm|maggot|ant|bee|bees|hornet|"
         "fish|whale|great fish|leviathan|behemoth|"
         "frog|frogs|gnat|gnats|flies|"
         "storm|tempest|whirlwind|hail|hailstones|lightning|thunder|"
         "earthquake|rainbow|dew|drought|famine|flood|"
         "east wind|south wind|north wind|sirocco|"
         "sunrise|sunset|new moon|full moon|stars|constellation|Pleiades|Orion",
         "A plant, animal, or natural phenomenon whose real look carries the meaning."),
    # ---- bird's-eye scene (event geography)
    _cue("birdseye", 2,
         "surrounded|besieged|siege|encamped|camped|pitched|"
         "ambush|lay in wait|pursued|fled|flee|"
         "battle|battle line|array|drew up|marched|"
         "crowd|multitude|thousands|great crowd|"
         "gathered|assembled|ran together|"
         "on the shore|on the mountain|on the roof|from the wall|"
         "in the boat|in the temple|in the court|"
         "went out to|came down to|climbed|descended|ascended",
         "The passage's action has a geography a bird's-eye view can chart without depicting the actors."),
    # ---- comparison
    _cue("compare", 2,
         "greater than|less than|larger than|smaller than|"
         "smallest|greatest|least|"
         "new wine|old wineskins|new cloth|old garment|"
         "wheat and|weeds|tares|darnel|"
         "sheep from the goats|sheep and goats|"
         "wise and foolish|wise man|foolish man|rock|sand|"
         "narrow gate|wide gate|broad way|narrow way|"
         "good tree|bad tree|good fruit|bad fruit|"
         "gold, silver, precious stones|wood, hay, straw|"
         "clean and unclean|holy and common|"
         "first will be last|last will be first|"
         "instead of|rather than|but not|whereas",
         "The verse turns on a contrast that side-by-side panels make immediate."),
    # ---- timeline / sequence
    _cue("timeline", 2,
         "in the year|in the .* year of|the first year|the second year|"
         "the reign of|reigned|began to reign|"
         "on the first day|on the third day|on the seventh day|"
         "the next day|the following day|the day after|"
         "generations of|"
         "seventy weeks|seventy years|four hundred years|"
         "forty years|three years and six months|"
         "at the third hour|at the sixth hour|at the ninth hour|"
         "the first watch|the fourth watch|before dawn|at cockcrow",
         "A sequence, chronology, or hour-of-day scheme a timeline clarifies."),
    # ---- who's who
    _cue("people", 2,
         "son of|daughter of|father of|mother of|brother of|sister of|"
         "wife of|husband of|the sons of|the daughters of|"
         "descendants|descendant|genealogy|begot|fathered|"
         "tribe of|the tribes|clan|clans|house of|"
         "king of|kings of|queen of|governor of|high priest|"
         "the twelve|the apostles|the disciples|Pharisees|Sadducees|"
         "scribes|elders|chief priests|Herod|Herodians|Zealot|Zealots|"
         "Samaritan|Samaritans|Gentiles|Greeks|Romans|Levites|priests",
         "Names, groups, or family lines a relationship chart untangles."),
    # ---- structure of the passage
    _cue("structure", 2,
         "blessed are|woe to|woe unto|"
         "the law and the prophets|"
         "faith, hope|love is|"
         "the fruit of the Spirit|the works of the flesh|"
         "the armor of|the whole armor|"
         "one body|many members|"
         "the ten commandments|"
         "these are the generations",
         "The passage is a list, sequence, or argument a structure diagram lays out."),
    # ---- symbolic imagery (explainer lane only)
    _cue("symbol", 3,
         "vision|visions|I saw|I looked|behold|"
         "beast|beasts|dragon|horns|heads|wings|"
         "living creatures|wheel|wheels|throne|"
         "lampstands|seven|seals|trumpets|bowls|"
         "scroll|book of life|new Jerusalem|"
         "statue|image|gold, silver, bronze|iron and clay|"
         "dry bones|valley of dry bones|"
         "olive trees|branches|flying scroll|measuring line|"
         "the tree|the river|the city|the bride|the lamb|"
         "the harlot|Babylon the great|"
         "sun, moon|stars fell|the moon became|"
         "locusts|scorpions|the abyss|the pit",
         "Dense symbolic imagery — render as a labeled explainer, never a literal scene."),
)

# Cues that mark the passage as the *event itself* — a visual must show the
# setting or a bird's-eye chart, not the moment. Used to redirect, not to
# suppress: abundant mode still wants an aid nearby, in a safe format.
EVENT_MOMENT = re.compile(
    r"\b(?:healed|raised (?:him|her|them) up|rose from the dead|resurrect|"
    r"walked on the (?:water|sea)|calmed|stilled|multiplied|"
    r"transfigured|ascended into heaven|crucified him|"
    r"appeared to them|the Spirit descended|tongues of fire|"
    r"the LORD appeared|God appeared|an angel appeared|"
    r"the glory of the LORD|cloud filled|fire came down)\b",
    re.IGNORECASE,
)

# Passages that are pure discourse/doctrine get a much lower ceiling; abundant
# mode still allows "structure" diagrams there but not scenes.
DISCOURSE_MARKERS = re.compile(
    r"\b(?:therefore|for if|so that|in order that|because|justified|"
    r"righteousness|grace|faith|sin|law|Spirit|flesh|salvation|"
    r"predestin|elect|redeem|reconcil|propitiat|sanctif|glorif)\b",
    re.IGNORECASE,
)

# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

@dataclass
class VerseHit:
    book_slug: str
    book: str
    chapter: int
    verse: int
    text: str
    scores: dict[str, int] = field(default_factory=dict)
    cues: dict[str, list[str]] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    event_moment: bool = False
    discourse: bool = False

    @property
    def reference(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"

    @property
    def verse_id(self) -> str:
        return f"{self.book_slug}-{self.chapter}-{self.verse}"


def score_verse(book_slug: str, book: str, chapter: int, verse: int, text: str) -> VerseHit | None:
    hit = VerseHit(book_slug, book, chapter, verse, text)
    for cue in CUES:
        matches = cue.pattern.findall(text)
        if not matches:
            continue
        # symbol cue is only meaningful in visionary contexts; elsewhere the
        # same words ("throne", "seven") are just objects/numbers.
        if cue.aid_type == "symbol" and book_slug not in VISIONARY_BOOKS:
            continue
        distinct = sorted({m.lower() for m in matches})
        contribution = min(cue.weight + len(distinct) - 1, cue.weight + 3)
        hit.scores[cue.aid_type] = hit.scores.get(cue.aid_type, 0) + contribution
        hit.cues.setdefault(cue.aid_type, []).extend(distinct)
        hit.reasons.append(cue.reason)
    if not hit.scores:
        return None
    hit.event_moment = bool(EVENT_MOMENT.search(text))
    hit.discourse = len(DISCOURSE_MARKERS.findall(text)) >= 3
    # Visionary books: symbol imagery must never be a literal place/nature scene.
    if book_slug in VISIONARY_BOOKS and "symbol" in hit.scores:
        for k in ("place", "nature", "birdseye"):
            hit.scores.pop(k, None)
    # Discourse-heavy verses: keep only structure/people/map/object/scale.
    if hit.discourse:
        for k in ("place", "birdseye", "nature", "how"):
            hit.scores.pop(k, None)
        if not hit.scores:
            return None
    # Event moments: redirect a place/nature score into a bird's-eye chart.
    if hit.event_moment and "place" in hit.scores:
        hit.scores["birdseye"] = max(hit.scores.get("birdseye", 0), hit.scores["place"])
        hit.scores.pop("place", None)
    hit.reasons = list(dict.fromkeys(hit.reasons))
    return hit


def total_score(hit: VerseHit) -> int:
    ranked = sorted(hit.scores.values(), reverse=True)
    if not ranked:
        return 0
    return min(12, ranked[0] + max(0, len(ranked) - 1))


def primary_type(hit: VerseHit) -> str:
    return sorted(hit.scores.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


# --------------------------------------------------------------------------
# Titles + prompts
# --------------------------------------------------------------------------

def _first_cue_phrase(hit: VerseHit, aid_type: str) -> str:
    cues = hit.cues.get(aid_type) or []
    return cues[0] if cues else ""


def working_title(hit: VerseHit, aid_type: str) -> str:
    phrase = _first_cue_phrase(hit, aid_type)
    t = AID_TYPES[aid_type]
    if aid_type == "map":
        return f"Map: {phrase.title()}" if phrase else f"Map for {hit.reference}"
    if aid_type == "object":
        return f"Object plate: {phrase}" if phrase else f"Object plate for {hit.reference}"
    if aid_type == "how":
        return f"How it worked: {phrase}" if phrase else f"How it worked ({hit.reference})"
    if aid_type == "scale":
        return f"To scale: {hit.reference}"
    if aid_type == "nature":
        return f"Field plate: {phrase}" if phrase else f"Field plate ({hit.reference})"
    if aid_type == "birdseye":
        return f"Bird's-eye: {hit.reference}"
    if aid_type == "compare":
        return f"Side by side: {hit.reference}"
    if aid_type == "timeline":
        return f"Timeline: {hit.reference}"
    if aid_type == "people":
        return f"Who's who: {phrase}" if phrase else f"Who's who ({hit.reference})"
    if aid_type == "structure":
        return f"Structure of {hit.reference}"
    if aid_type == "symbol":
        return f"Symbol explainer: {phrase}" if phrase else f"Symbol explainer ({hit.reference})"
    return f"{t.label}: {phrase}" if phrase else f"{t.label} for {hit.reference}"


def prompt_for(hit: VerseHit, aid_type: str) -> str:
    t = AID_TYPES[aid_type]
    cues = ", ".join(dict.fromkeys(hit.cues.get(aid_type, [])))[:200]
    guard = (
        "People: small anonymous figures for scale only — no identifiable "
        "individuals, no Bible characters, no faces in focus, and never Jesus, "
        "God, the Holy Spirit, angels, demons, or any heavenly being. Preserve "
        "human dignity; no gore. No text other than the specified labels; no "
        "watermark. Historically and geographically plausible for the period; "
        "where identification is debated keep details generic and say so in "
        "the caption."
    )
    lead = (
        f"Explanatory visual aid for {hit.reference} ({t.label}). Do NOT depict "
        f"the events of the passage happening; help the reader understand the "
        f"{t.label.lower()} the text assumes."
    )
    return f"{lead} Focus cues: {cues}. Style: {t.style} {guard}"


# --------------------------------------------------------------------------
# Book loading + coverage policy
# --------------------------------------------------------------------------

def load_book(path: Path) -> tuple[str, list[tuple[int, int, str]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    name = str(payload.get("name") or path.stem)
    verses: list[tuple[int, int, str]] = []
    for ch in payload.get("chapters") or []:
        cnum = int(ch.get("chapter") or 0)
        for v in ch.get("verses") or []:
            vnum = int(v.get("verse") or 0)
            text = str(v.get("text") or "")
            if cnum and vnum and text:
                verses.append((cnum, vnum, text))
    return name, verses


def select_for_book(hits: list[VerseHit], per_chapter_cap: int, min_score: int) -> list[dict]:
    """Abundant selection: keep every verse at/above ``min_score``, but cap
    the number of *anchors* per chapter so a dense chapter cannot become a
    picture book. Within a chapter, prefer higher score, then earlier verse,
    and spread across aid types so one chapter isn't five maps."""
    by_chapter: dict[int, list[VerseHit]] = defaultdict(list)
    for h in hits:
        if total_score(h) >= min_score:
            by_chapter[h.chapter].append(h)
    rows: list[dict] = []
    for chapter, chapter_hits in sorted(by_chapter.items()):
        chapter_hits.sort(key=lambda h: (-total_score(h), h.verse))
        chosen: list[VerseHit] = []
        seen_types: Counter[str] = Counter()
        # First pass: one per aid type, best first
        for h in chapter_hits:
            ptype = primary_type(h)
            if seen_types[ptype] == 0 and len(chosen) < per_chapter_cap:
                chosen.append(h)
                seen_types[ptype] += 1
        # Second pass: fill remaining slots by score, min 4 verses apart
        for h in chapter_hits:
            if len(chosen) >= per_chapter_cap:
                break
            if h in chosen:
                continue
            if all(abs(h.verse - c.verse) >= 4 for c in chosen):
                chosen.append(h)
        chosen.sort(key=lambda h: h.verse)
        for h in chosen:
            ptype = primary_type(h)
            secondary = [k for k, _ in sorted(hit_items(h), key=lambda kv: (-kv[1], kv[0]))][1:3]
            rows.append({
                "id": h.verse_id,
                "book": h.book,
                "book_slug": h.book_slug,
                "chapter": h.chapter,
                "verse": h.verse,
                "reference": h.reference,
                "score": total_score(h),
                "aid_type": ptype,
                "aid_type_label": AID_TYPES[ptype].label,
                "format": AID_TYPES[ptype].format_hint,
                "secondary_types": secondary,
                "working_title": working_title(h, ptype),
                "cues": {k: sorted(set(v)) for k, v in h.cues.items()},
                "reasons": h.reasons,
                "event_moment": h.event_moment,
                "verse_text": h.text,
                "suggested_prompt": prompt_for(h, ptype),
                "status": "needs_editorial_review",
            })
    return rows


def hit_items(h: VerseHit):
    return list(h.scores.items())


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--books-root", required=True, type=Path,
                    help="Directory of compiled per-book reader JSON (e.g. cartha.website/public/bibles/pob/books)")
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--min-score", type=int, default=4,
                    help="Minimum verse score to include (default 4 = clear signal)")
    ap.add_argument("--per-chapter-cap", type=int, default=4,
                    help="Max anchors per chapter (default 4)")
    ap.add_argument("--books", nargs="*", help="Restrict to these slugs")
    ap.add_argument("--exclude-ids", type=Path,
                    help="JSON array of anchor ids (book-slug-chapter-verse) already "
                         "published; verses within 2 of any are skipped so the "
                         "queue only proposes new placements")
    args = ap.parse_args()

    published: set[str] = set()
    if args.exclude_ids and args.exclude_ids.exists():
        published = set(json.loads(args.exclude_ids.read_text(encoding="utf-8")))

    def near_published(slug: str, chapter: int, verse: int) -> bool:
        return any(f"{slug}-{chapter}-{v}" in published for v in range(verse - 2, verse + 3))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "books").mkdir(exist_ok=True)

    summary_books = []
    canon_total = 0
    canon_verses = 0
    type_counter: Counter[str] = Counter()
    wanted = args.books or list(CANON_66.keys())

    for slug in wanted:
        if slug not in CANON_66:
            continue
        path = args.books_root / f"{slug}.json"
        if not path.exists():
            print(f"missing: {path}")
            continue
        name, verses = load_book(path)
        display = CANON_66[slug]
        hits = []
        for cnum, vnum, text in verses:
            if published and near_published(slug, cnum, vnum):
                continue
            h = score_verse(slug, display, cnum, vnum, text)
            if h:
                hits.append(h)
        rows = select_for_book(hits, args.per_chapter_cap, args.min_score)
        chapters = max((c for c, _, _ in verses), default=0)
        for r in rows:
            type_counter[r["aid_type"]] += 1
        book_payload = {
            "version": 1,
            "book": display,
            "book_slug": slug,
            "chapters": chapters,
            "verses": len(verses),
            "anchors": len(rows),
            "aids": rows,
        }
        (args.out_dir / "books" / f"{slug}.json").write_text(
            json.dumps(book_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        summary_books.append({
            "book": display, "slug": slug, "chapters": chapters,
            "verses": len(verses), "anchors": len(rows),
            "anchors_per_chapter": round(len(rows) / chapters, 2) if chapters else 0,
            "types": dict(Counter(r["aid_type"] for r in rows)),
        })
        canon_total += len(rows)
        canon_verses += len(verses)
        print(f"{display:<18} ch={chapters:>3} verses={len(verses):>5} anchors={len(rows):>4}")

    summary = {
        "version": 1,
        "min_score": args.min_score,
        "per_chapter_cap": args.per_chapter_cap,
        "canon_verses": canon_verses,
        "canon_anchors": canon_total,
        "coverage": round(canon_total / canon_verses, 4) if canon_verses else 0,
        "by_type": dict(type_counter.most_common()),
        "books": summary_books,
    }
    (args.out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"\nTOTAL anchors={canon_total} of {canon_verses} canon verses "
          f"({summary['coverage']:.1%}); by type: {dict(type_counter.most_common())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
