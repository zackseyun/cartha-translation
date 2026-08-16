from tools.bible_visual_aid_map import (
    AID_TYPES,
    primary_type,
    score_verse,
    select_for_book,
    total_score,
)


def test_measured_object_scores_as_object_plate():
    hit = score_verse(
        "exodus", "Exodus", 25, 23,
        "You shall make a table of acacia wood; two cubits its length, "
        "a cubit its width, and a cubit and a half its height.",
    )
    assert hit is not None
    assert primary_type(hit) in {"object", "scale"}
    assert total_score(hit) >= 6


def test_named_geography_scores_as_map():
    hit = score_verse(
        "acts", "Acts", 27, 2,
        "Embarking in a ship of Adramyttium about to sail to the ports of Asia, "
        "we set out, Aristarchus, a Macedonian of Thessalonica, being with us.",
    )
    assert hit is not None
    assert primary_type(hit) == "map"


def test_symbolic_imagery_only_counts_in_visionary_books():
    rev = score_verse(
        "revelation", "Revelation", 13, 1,
        "And I saw a beast rising out of the sea, with ten horns and seven heads.",
    )
    assert rev is not None and "symbol" in rev.scores
    # Same words outside a visionary book are not a symbol explainer.
    ps = score_verse("psalms", "Psalms", 22, 12, "Many bulls have surrounded me; strong beasts of Bashan.")
    assert ps is None or "symbol" not in ps.scores


def test_event_moment_redirects_place_to_birdseye():
    hit = score_verse(
        "mark", "Mark", 6, 48,
        "About the fourth watch of the night he came to them, and they saw him "
        "as he walked on the sea, near the boat by the shore of the sea.",
    )
    assert hit is not None
    assert hit.event_moment
    assert "place" not in hit.scores


def test_pure_doctrine_is_not_forced_into_the_queue():
    hit = score_verse(
        "romans", "Romans", 3, 24,
        "being justified freely by his grace through the redemption that is in "
        "Christ Jesus, whom God set forth as a propitiation through faith.",
    )
    assert hit is None or total_score(hit) < 6


def test_per_chapter_cap_and_spacing_hold():
    hits = []
    for verse in range(1, 21):
        h = score_verse(
            "genesis", "Genesis", 24, verse,
            "The servant took ten camels and gold rings and shekels of silver "
            "and went to the well outside the city of Nahor in Mesopotamia.",
        )
        assert h is not None
        hits.append(h)
    rows = select_for_book(hits, per_chapter_cap=2, min_score=6)
    assert len(rows) == 2
    assert all(r["aid_type"] in AID_TYPES for r in rows)
    assert all("Do NOT depict the events" in r["suggested_prompt"] for r in rows)
