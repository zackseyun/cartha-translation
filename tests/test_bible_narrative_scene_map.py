from tools.bible_narrative_scene_map import (
    character_ids_for_text,
    load_character_registry,
    narrative_prompt,
    score_scene,
    select_scenes,
)


def test_john_20_head_and_feet_is_a_high_value_scene():
    hit = score_scene(
        "john", "John", 20, 12,
        "and she sees two angels in white sitting, one at the head and one at "
        "the feet, where the body of Jesus had been lying.",
    )
    assert hit is not None
    assert hit.score >= 7
    assert hit.heavenly
    assert "explicit_positions" in hit.cues
    assert "heavenly_encounter" in hit.cues


def test_epistle_doctrine_is_not_a_narrative_scene():
    assert score_scene(
        "romans", "Romans", 3, 24,
        "being justified freely by his grace through the redemption in Christ Jesus",
    ) is None


def test_symbolic_vision_is_not_literalized():
    assert score_scene(
        "ezekiel", "Ezekiel", 1, 16,
        "In the vision I saw wheels within wheels beside the living creatures.",
    ) is None


def test_sensitive_scene_is_flagged_for_heightened_review():
    hit = score_scene(
        "mark", "Mark", 15, 20,
        "After they had flogged him, they led him out and crucified him.",
        "They mocked him and flogged him, then led him out and crucified him.",
    )
    assert hit is not None
    assert hit.sensitive
    assert "Heightened dignity review" in narrative_prompt(hit)


def test_dialogue_alone_does_not_force_a_scene():
    hit = score_scene(
        "genesis", "Genesis", 12, 1,
        "And Yahweh said to Abram, “Go from your country.”",
    )
    assert hit is None or hit.score < 7


def test_selection_caps_chapter_and_spaces_candidates():
    hits = []
    for verse in (1, 2, 7):
        hit = score_scene(
            "john", "John", 20, verse,
            "She wept and fell at his feet when he appeared to her at the tomb.",
        )
        assert hit is not None
        hits.append(hit)
    rows = select_scenes(hits, min_score=7, per_chapter_cap=2)
    assert len(rows) == 2
    assert rows[1]["verse"] - rows[0]["verse"] >= 4
    assert all(
        row["prompt_version"] == "narrative-reconstruction-v2-character-locked"
        for row in rows
    )


def test_transfiguration_is_a_high_value_heightened_scene():
    hit = score_scene(
        "matthew", "Matthew", 17, 2,
        "He was transfigured before them, and his face shone like the sun, "
        "and his clothes became white as light.",
        "Jesus took Peter, James, and John up a high mountain. He was "
        "transfigured before them. Moses and Elijah appeared to them.",
    )
    assert hit is not None
    assert hit.score >= 8
    assert "transfiguration" in hit.cues


def test_locked_characters_are_attached_to_scene_rows():
    registry = load_character_registry()
    ids = character_ids_for_text(
        "Jesus took Peter with him, and later Paul spoke.", registry
    )
    assert ids == ["jesus", "peter-apostle", "saul-damascus"]
    hit = score_scene(
        "matthew", "Matthew", 17, 2,
        "He was transfigured before them.",
        "Jesus took Peter up the mountain and was transfigured before him.",
    )
    assert hit is not None
    row = select_scenes([hit], 7, 1, registry)[0]
    assert row["characters"] == ["jesus", "peter-apostle"]
    assert row["character_refs"]["jesus"]["status"] == "locked"
    assert "attach the exact locked refs" in row["suggested_prompt"]


def test_adjacent_nonparticipant_name_is_not_locked_into_scene():
    registry = load_character_registry()
    hit = score_scene(
        "matthew", "Matthew", 8, 3,
        "Jesus watched as the man fell at his feet, then stretched out his hand and touched him.",
        "Jesus watched as the man fell at his feet, then stretched out his hand and "
        "touched him. Then he said to offer "
        "the gift Moses commanded.",
    )
    assert hit is not None
    row = select_scenes([hit], 7, 1, registry)[0]
    assert row["characters"] == ["jesus"]
