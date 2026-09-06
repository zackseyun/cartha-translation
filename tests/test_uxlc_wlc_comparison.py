import json
from pathlib import Path
import unittest

from tools.textual_restoration import compare_uxlc_wlc as m


def old(body):
    return m.parse_wlc(f'<osis xmlns="urn:test"><verse osisID="Gen.1.1">{body}</verse></osis>'.encode())[(1, 1)]


def new(body):
    return m.parse_uxlc(f'<Tanach><teiHeader><edition><version>UXLC 2.5</version></edition></teiHeader><tanach><book><c n="1"><v n="1">{body}</v></c></book></tanach></Tanach>'.encode())[(1, 1)]


class ComparisonTests(unittest.TestCase):
    def test_decorations_and_tails(self):
        self.assertEqual(old('<w>מִ/יָּ֑<seg type="x-suspended">עַ</seg>ר</w>')['written'][0]['text'], 'מִ/יָּ֑עַר')
        r = new('<w>א<s t="large">ב</s>ג<x>52</x>ד</w>')
        self.assertEqual(r['written'][0]['text'], 'אבגד')
        self.assertEqual(r['annotations'][1]['code'], '52')

    def test_unknown_nested_tags_fail(self):
        for xml, parser in (('<w>א<note>ב</note></w>', old), ('<w>א<z>ב</z></w>', new)):
            with self.assertRaises(ValueError):
                parser(xml)

    def test_no_descendant_double_counting(self):
        r = old('<w type="x-ketiv">אב</w><note type="variant"><catchWord>אב</catchWord><rdg type="x-qere"><w>גד</w></rdg></note><note type="exegesis"><rdg><w>הו</w></rdg></note>')
        self.assertEqual([w['text'] for w in r['written']], ['אב'])
        self.assertEqual([q['text'] for q in r['qere']], ['גד'])
        self.assertEqual(r['other_note_types'], {'exegesis': 1})

    def test_punctuation_interleaving(self):
        a = old('<w>א/ב</w><seg type="x-maqqef">־</seg><w>גד</w><seg type="x-paseq">׀</seg><seg type="x-sof-pasuq">׃</seg><seg type="x-pe">פ</seg>')
        b = new('<w>אב־</w><w>גד ׀׃</w><pe/>')
        self.assertFalse(any(m.comparison(a, b).values()))

    def test_empty_qere_presence_not_silently_lost(self):
        a = old('<w type="x-ketiv">נא</w><note type="variant"><catchWord>נא</catchWord><rdg type="x-qere"/></note>')
        b = new('<k>נא</k>')
        flags = m.comparison(a, b)
        self.assertTrue(flags['qere_presence_or_word_count_difference'])
        self.assertFalse(flags['qere_payload_difference'])

    def test_multiword_qere_not_group_count(self):
        a = old('<w>אב</w><note type="variant"><rdg type="x-qere"><w>ג</w><w>ד</w></rdg></note>')
        b = new('<k>אב</k><q>ג</q><q>ד</q>')
        self.assertFalse(any(m.comparison(a, b).values()))

    def test_insertion_only_qere_retained(self):
        a = old('<w>אב</w><note type="variant"><rdg type="x-qere"><w>צבאות</w></rdg></note>')
        self.assertEqual(a['qere'][0]['catchwords'], [])
        self.assertEqual(a['qere'][0]['text'], 'צבאות')

    def test_normalization_and_layer_order(self):
        self.assertEqual(m.normalized('א/ב\u034f ', 'full'), 'אב')
        self.assertEqual(m.normalized('שׁ', 'pointing'), m.normalized('שׁ', 'pointing'))
        for lhs, rhs, expected in [('אב', 'אג', 'consonants'), ('בָ', 'בַ', 'pointing'), ('בָ֑', 'בָ֔', 'accents'), ('ב־', 'ב', 'full')]:
            self.assertEqual(m.comparison(old(f'<w>{lhs}</w>'), new(f'<w>{rhs}</w>'))['written_difference'], expected)

    def test_boundaries_separate_from_consonants(self):
        r = m.comparison(old('<w>אב</w><w>ג</w>'), new('<w>א</w><w>בג</w>'))
        self.assertIsNone(r['written_difference'])
        self.assertTrue(r['written_token_boundary_or_payload_difference'])

    def test_removed_blockers_cannot_create_mark_order_differences(self):
        for blocker in ('\u034f', '/', ' '):
            for layer in ('pointing', 'accents', 'full'):
                self.assertEqual(m.normalized('בָ' + blocker + 'ִ', layer), m.normalized('בִָ', layer))
        self.assertFalse(m.comparison(old('<w>בָ\u034fִ</w>'), new('<w>בִָ</w>'))['written_difference'])

    def test_duplicate_labels_rejected(self):
        with self.assertRaises(ValueError):
            m.parse_wlc(b'<osis><verse osisID="Gen.1.1"/><verse osisID="Gen.1.1"/></osis>')
        with self.assertRaises(ValueError):
            m.parse_uxlc(b'<Tanach><edition><version>UXLC 2.5</version></edition><tanach><book><c n="1"><v n="1"/><v n="1"/></c></book></tanach></Tanach>')

    def test_member_map_unique_39_no_double_headers(self):
        books = json.loads(m.BOOKMAP.read_text())['books']
        names = {m.member_name(b['book']) for b in books}
        self.assertEqual(len(names), 39)
        self.assertIn('Books/Samuel_2.xml', names)
        self.assertIn('Books/Song_of_Songs.xml', names)
        self.assertFalse(any('.DH.' in n for n in names))

    def test_actual_wlc_structural_edge_cases(self):
        sam = m.parse_wlc((m.ROOT / 'sources/ot/wlc/1Sam.xml').read_bytes())[(20, 2)]
        self.assertEqual(sam['qere'][0]['word_count'], 2)
        kings = m.parse_wlc((m.ROOT / 'sources/ot/wlc/2Kgs.xml').read_bytes())
        self.assertEqual(kings[(5, 18)]['qere'][0]['word_count'], 0)
        self.assertEqual(kings[(19, 31)]['qere'][0]['catchwords'], [])

    def test_saved_receipt_pins_and_partition(self):
        d = json.loads(m.OUTPUT.read_text())
        for path, expected in d['inputs'].items():
            self.assertEqual(m.digest((m.ROOT / path).read_bytes()), expected, path)
        self.assertEqual(d['summary']['books'], 39)
        self.assertEqual(d['summary']['shared_verse_labels'], 23213)
        self.assertEqual(d['unmatched_labels'], [])
        counts = d['summary']['counts']
        self.assertEqual(sum(counts[k] for k in ('written_equal', 'consonants', 'pointing', 'accents', 'full')), 23213)
        self.assertEqual(len(d['pob_joins']), counts['consonants'])
        self.assertEqual(len(d['differences']), d['summary']['difference_rows'])


if __name__ == '__main__':
    unittest.main()
