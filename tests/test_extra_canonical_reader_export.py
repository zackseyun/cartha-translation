from tools.export_mobile_bible import (
    _book_source_metadata,
    _jesus_ranges_for_paragraph,
    _split_reader_paragraphs,
)


def test_editorial_prose_becomes_numbered_paragraph_units() -> None:
    verses = _split_reader_paragraphs(
        'The disciples spoke.\n\nJesus said, “Peace be with you.”\n\nThey left.'
    )
    assert [verse['verse'] for verse in verses] == [1, 2, 3]
    assert all(verse['is_editorial_section'] for verse in verses)
    assert verses[1]['text'][verses[1]['jesus_words'][0]['start']:verses[1]['jesus_words'][0]['end']] == 'Peace be with you.'
    assert 'jesus_words' not in verses[0]
    assert 'jesus_words' not in verses[2]


def test_multi_paragraph_jesus_speech_carries_until_closing_quote() -> None:
    verses = _split_reader_paragraphs(
        'Jesus said, "First paragraph.\n\n"Second paragraph.\n\n"Final paragraph."\n\nJudas answered, "I heard."'
    )
    assert [bool(verse.get('jesus_words')) for verse in verses] == [True, True, True, False]


def test_non_jesus_dialogue_is_not_highlighted() -> None:
    ranges, carry = _jesus_ranges_for_paragraph(
        'Judas said, “Master, tell me.”',
        continuing_jesus_speech=False,
    )
    assert ranges == []
    assert carry is False


def test_judas_exports_exact_manuscript_gallery_metadata() -> None:
    metadata = _book_source_metadata(
        'GJUD',
        [{
            'source': {
                'manuscript': 'Codex Tchacos 3',
                'ancient_language': 'Coptic',
                'witness_url': 'https://www.gospels.net/judas',
            }
        }],
    )
    assert metadata is not None
    assert metadata['manuscript'] == 'Codex Tchacos 3'
    assert metadata['manuscript_images_url'] == 'https://commons.wikimedia.org/wiki/Codex_Tchacos'
    assert 'Codex_Tchacos_p33.jpg' in metadata['manuscript_thumbnail_url']
