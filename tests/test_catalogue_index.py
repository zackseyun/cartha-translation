import json
from collections import Counter
from pathlib import Path
import unittest

from tools.textual_restoration.build_catalogue_index import (
    INDEX_SHA, OUT, candidate_key, parse_index, reconcile,
)


def item(label, identifier, category="dss-biblical", date="2026-05-21"):
    return (f'<li class="list-item {category}"><a class="text-href-link" '
            f'href="/transcriptions/{identifier}/{date}/index.html?v={date}">{label}</a></li>')


def page(*items):
    return ('<html><ol id="item-list">' + ''.join(items) + '</ol></html>').encode()


class CatalogueIndexTests(unittest.TestCase):
    def test_superscript_display_and_url_identity_remain_separate(self):
        result = parse_index(page(item('1QIsa<sup>a</sup>', '1QIsa^a^')))[0]
        self.assertEqual(result['display_label'], '1QIsaa')
        self.assertEqual(result['url_identifier'], '1QIsa^a^')
        self.assertEqual(result['listed_version'], '2026-05-21')
        self.assertEqual(result['index_ordinal'], 1)

    def test_html_entities_whitespace_and_navigation(self):
        raw = b'<ol><li><a>Ignore me</a></li></ol>' + page(item('Mur.&nbsp; 1', 'Mur._1'))
        self.assertEqual(parse_index(raw)[0]['display_label'], 'Mur. 1')

    def test_truncated_absent_empty_and_unclosed_items_rejected(self):
        for raw in (b'<html/>', page(), page(item('4Q1', '4Q1'))[:-12],
                    b'<ol id="item-list"><li class="list-item dss"></ol>'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_index(raw)

    def test_unexpected_or_conflicting_classes_rejected(self):
        for category in ('mystery', 'dss dss-biblical'):
            with self.subTest(category=category), self.assertRaises(ValueError):
                parse_index(page(item('4Q1', '4Q1', category)))

    def test_duplicates_and_multiple_links_rejected(self):
        for raw in (page(item('4Q1', '4Q1'), item('4Q1', '4Q2')),
                    page(item('4Q1', '4Q1'), item('other', '4Q1')),
                    page(item('4Q1', '4Q1').replace('</li>', '<a>bad</a></li>'))):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_index(raw)

    def test_foreign_urls_and_version_disagreement_rejected(self):
        good = page(item('4Q1', '4Q1'))
        for raw in (good.replace(b'href="/transcriptions', b'href="https://evil.example/transcriptions'),
                    good.replace(b'?v=2026-05-21', b'?v=2025-08-25')):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_index(raw)

    def test_changed_row_container_or_orphan_anchor_cannot_silently_drop_entry(self):
        good = item('4Q1', '4Q1')
        other = item('4Q2', '4Q2')
        for malformed in (other.replace('<li ', '<div ').replace('</li>', '</div>'),
                          other[other.index('<a '):-len('</li>')],
                          other.replace('<a ', '<span><a ').replace('</a>', '</a></span>')):
            with self.subTest(malformed=malformed), self.assertRaises(ValueError):
                parse_index(page(good, malformed))

    def test_blank_unknown_duplicate_and_malformed_queries_rejected(self):
        good = page(item('4Q1', '4Q1'))
        for query in ('v=', 'mystery=', 'v=2026-05-21&mystery=',
                      'v=2026-05-21&v=2026-05-21', 'v=2026-05-21&', 'v'):
            with self.subTest(query=query), self.assertRaises(ValueError):
                parse_index(good.replace(b'v=2026-05-21', query.encode()))
        # A versioned path without a query is unambiguous and remains allowed.
        self.assertEqual(parse_index(good.replace(b'?v=2026-05-21', b''))[0]['listed_version'], '2026-05-21')

    def test_superscript_and_anchor_nesting_must_be_balanced(self):
        for label in ('1QIsa<sup>a', '1QIsa</sup>a', '1QIsa<sup><sup>a</sup></sup>',
                      '1QIsa<sup>a</a></sup>'):
            with self.subTest(label=label), self.assertRaises(ValueError):
                parse_index(page(item(label, '1QIsa^a^')))

    def test_alias_key_is_deliberately_narrow(self):
        self.assertEqual(candidate_key('PAM 43.113'), candidate_key('Pam43113'))
        self.assertEqual(candidate_key('1QIsaa'), candidate_key('1Qisaa'))
        for first, second in [('4Q8', '4Q8a'), ('4Q12', '4Q12a'),
                              ('XHev/Se 2', 'XHevSe2'), ('4Q223-224', '4Q223224')]:
            self.assertNotEqual(candidate_key(first), candidate_key(second))

    def test_match_categories_missing_and_collision_not_physical_identity(self):
        entries = parse_index(page(item('4Q1', '4Q1'), item('1QIsaa', '1QIsa^a^'),
                                   item('4Q8', '4Q8'), item('11Q5', '11Q5', 'dss'),
                                   item('Unrelated', 'Unrelated', 'dss')))
        result = reconcile(entries, {'labels': Counter({'4Q1': 2, '1Qisaa': 1, '11Q5': 1, '4Q8a': 1})})
        self.assertEqual(len(result['entries']), 4)
        self.assertEqual(result['exact_matches_outside_biblical_class'], ['11Q5'])
        self.assertEqual(result['biblical_class_entries_without_label_candidate'], ['4Q8'])
        self.assertEqual(result['qdr_labels_without_exact_or_typography_candidate'], ['4Q8a'])
        self.assertTrue(result['entries'][0]['qdr_label_collision'])
        self.assertEqual(result['entries'][1]['match_status'], 'typography-alias-candidate')
        self.assertTrue(all(not row['physical_identity_verified'] for row in result['entries']))

    def test_ambiguous_alias_candidates_not_collapsed(self):
        entries = parse_index(page(item('Mur. 1', 'Mur._1')))
        result = reconcile(entries, {'labels': Counter({'Mur1': 1, 'MUR1': 1})})
        self.assertEqual(result['entries'][0]['qdr_labels'], ['MUR1', 'Mur1'])
        self.assertEqual(result['entries'][0]['match_status'], 'typography-alias-candidate')

    def test_published_receipt_accounting_and_nonclaims(self):
        receipt = json.loads(OUT.read_text())
        self.assertEqual(receipt['sources']['catalogue']['sha256'], INDEX_SHA)
        summary = receipt['summary']
        self.assertEqual(summary['catalogue_entries_parsed'], 1173)
        self.assertEqual(sum(summary['catalogue_class_counts'].values()), 1173)
        self.assertEqual(summary['qdr_distinct_labels_scanned'], 265)
        self.assertEqual(summary['biblical_class_entries'], 263)
        self.assertEqual(len(receipt['entries']), summary['exported_catalogue_entries'])
        self.assertEqual(sum(summary[k] for k in ('biblical_class_exact_label_matches',
                         'biblical_class_typography_candidates', 'biblical_class_without_label_candidate')), 263)
        self.assertEqual(sum(summary[k] for k in ('exact_qdr_labels_any_catalogue_class',
                         'qdr_labels_with_typography_candidate_but_no_exact_match',
                         'qdr_labels_without_exact_or_typography_candidate')), 265)
        self.assertEqual(receipt['exact_matches_outside_biblical_class'], ['2Q29', '4Q88', '4Q249j', '4Q483', '11Q5', '11Q6'])
        self.assertFalse(receipt['policy']['all_known_ot_sources_covered'])
        self.assertTrue(all(not r['physical_identity_verified'] and not r['underlying_transcription_consulted_by_this_pass'] for r in receipt['entries']))
        allowed_row_fields = {'catalogue_class', 'display_label', 'url', 'url_identifier',
                              'listed_version', 'index_ordinal', 'match_status', 'qdr_labels',
                              'qdr_source_records', 'qdr_label_collision', 'physical_identity_verified',
                              'underlying_transcription_consulted_by_this_pass'}
        self.assertTrue(all(set(row) == allowed_row_fields for row in receipt['entries']))


if __name__ == '__main__':
    unittest.main()
