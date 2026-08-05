from tools.bible_visual_aid_candidates import score_verse


def verse(verse_id, reference, text, footnotes=None):
    return {
        "id": verse_id,
        "reference": reference,
        "translation": {"text": text, "footnotes": footnotes or []},
    }


def test_solomons_portico_is_high_confidence_architecture_candidate():
    candidate = score_verse(
        verse(
            "ACT.3.11",
            "Acts 3:11",
            "All the people ran together at the portico called Solomon's.",
            [{"reason": "cultural_note", "text": "A covered colonnade in the temple precincts."}],
        )
    )
    assert candidate is not None
    assert candidate["category"] == "architecture"
    assert candidate["score"] >= 4
    assert "reconstruction from certainty" in candidate["suggested_prompt"]


def test_beautiful_gate_and_healing_actions_are_candidates():
    gate = score_verse(
        verse("ACT.3.2", "Acts 3:2", "They carried a man and laid him daily at the gate of the temple.")
    )
    healing = score_verse(
        verse("ACT.3.7", "Acts 3:7", "Taking him by the right hand, he raised him; he stood and walked.")
    )
    assert gate is not None and gate["category"] == "architecture"
    assert healing is not None and healing["category"] == "event"


def test_abstract_prose_is_not_forced_into_the_queue():
    assert score_verse(
        verse("JHN.3.16", "John 3:16", "For God so loved the world that he gave his only Son.")
    ) is None
