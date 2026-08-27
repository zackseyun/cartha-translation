from tools.audit_bible_visual_aid_semantics import literary_risks, runtime_anchor


def test_runtime_anchor_uses_the_end_of_a_verse_range():
    entry = {"book": "Mark", "chapter": 9, "verse_start": 2, "verse_end": 4}
    assert runtime_anchor(entry) == ("Mark", 9, 4)


def test_parable_caption_must_identify_parable():
    verse = "He spoke to them in a parable: a sower went out to sow."
    assert "parable_not_identified" in literary_risks(verse, "A farmer scatters seed.")
    assert literary_risks(verse, "In Jesus' parable, a farmer scatters seed.") == []


def test_comparison_caption_must_not_present_image_as_event():
    verse = "He is like a tree planted beside streams of water."
    assert "comparison_not_identified" in literary_risks(verse, "An irrigated tree stays green.")
    assert literary_risks(verse, "The psalm compares the faithful person to an irrigated tree.") == []


def test_vision_caption_must_identify_visual_form():
    verse = "In the vision I saw a measuring reed."
    assert "vision_not_identified" in literary_risks(verse, "A six-cubit reed.")
    assert literary_risks(verse, "A schematic organizes the vision's stated measure.") == []
