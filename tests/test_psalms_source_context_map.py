import collections
import hashlib
import json
from pathlib import Path
import unittest

import yaml

from tools import wlc
from tools.textual_restoration.compare_uxlc_wlc import normalized

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / 'sources/textual_restoration/inventory/psalms_source_context_map.v1.json'


class PsalmsSourceContextMapTests(unittest.TestCase):
    def test_complete_current_mapping_and_coverage(self):
        data = json.loads(MAP.read_text())
        self.assertEqual([r['chapter'] for r in data['chapters']], list(range(1, 151)))
        self.assertEqual(hashlib.sha256((ROOT / 'sources/ot/wlc/Ps.xml').read_bytes()).hexdigest(), data['source_xml_sha256'])
        base = {(v.chapter, v.verse): v.hebrew_text
                for v in wlc.iter_verses('PSA', ROOT / 'sources')}
        mapped = set()
        usage = collections.Counter()
        for chapter in data['chapters']:
            ch = chapter['chapter']
            for segment in chapter['segments']:
                for v in range(segment['pob_first'], segment['pob_last'] + 1):
                    key = ch, v
                    self.assertNotIn(key, mapped)
                    mapped.add(key)
                    record = yaml.load((ROOT / f'translation/ot/psalms/{ch:03}/{v:03}.yaml').read_text(), Loader=yaml.CSafeLoader)
                    self.assertEqual(record['id'], f'PSA.{ch}.{v}')
                    self.assertEqual(record['source']['edition'], 'WLC')
                    text = record['source']['text']
                    if 'source_span' in segment:
                        self.assertEqual(key, (60, 0))
                        self.assertEqual(segment['source_span'], [1, 2])
                        self.assertEqual(segment['match'], 'pointed_letter_stream')
                        selected = segment['source_span']
                        source_text = ' '.join(base[ch, n] for n in selected)
                        self.assertEqual(normalized(text, 'accents'), normalized(source_text, 'accents'))
                    else:
                        selected = [v + segment['offset']] if 'offset' in segment else [segment['resolved_to']]
                        self.assertEqual(text, base[ch, selected[0]])
                        if 'candidates' in segment:
                            actual = [n for (c, n), t in base.items() if c == ch and t == text]
                            self.assertEqual(actual, segment['candidates'])
                            evidence = next(r for r in data['resolution_evidence'] if r['id'] == record['id'])
                            allowed = [n for n in actual
                                       if (evidence['before'] is None or n >= evidence['before']['source'])
                                       and (evidence['after'] is None or n <= evidence['after']['source'])]
                            self.assertEqual(allowed, selected)
                            for bound in ('before', 'after'):
                                if evidence[bound] is not None:
                                    neighbor = evidence[bound]
                                    p = ROOT / f"translation/ot/psalms/{ch:03}/{neighbor['pob']:03}.yaml"
                                    neighbor_text = yaml.load(p.read_text(), Loader=yaml.CSafeLoader)['source']['text']
                                    self.assertEqual([n for (c, n), t in base.items() if c == ch and t == neighbor_text], [neighbor['source']])
                    usage.update((ch, n) for n in selected)
        actual = {(int(p.parent.name), int(p.stem)) for p in (ROOT / 'translation/ot/psalms').glob('*/*.yaml')}
        self.assertEqual(mapped, actual)
        self.assertEqual(len(mapped), 2578)
        self.assertEqual(set(usage), set(base))
        self.assertEqual(len(base), 2527)
        self.assertEqual(sum(n > 1 for n in usage.values()), 52)
        self.assertEqual(len(data['resolution_evidence']), 13)


if __name__ == '__main__':
    unittest.main()
