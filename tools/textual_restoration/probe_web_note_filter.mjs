#!/usr/bin/env node
// Read-only, isolated execution of the inspected web loader's note-filter block.
// This is not a browser, React-rendering, CDN, or deployment test.
import fs from 'node:fs';
import crypto from 'node:crypto';
import vm from 'node:vm';

const [webDataPath, candidatePath] = process.argv.slice(2);
if (!webDataPath || !candidatePath) {
  throw new Error('Usage: node probe_web_note_filter.mjs WEB_BIBLE_DATA_JS CANDIDATE_JSON');
}
const sourceBytes = fs.readFileSync(webDataPath);
const candidateBytes = fs.readFileSync(candidatePath);
const source = sourceBytes.toString('utf8');
const startMarker = 'const SUPERSCRIPT_DIGITS =';
const endMarker = 'function sanitizeBibleForReader(';
if (source.split(startMarker).length !== 2 || source.split(endMarker).length !== 2) {
  throw new Error('Inspected filter boundaries changed; re-inspect source before probing');
}
const start = source.indexOf(startMarker);
const end = source.indexOf(endMarker);
if (end <= start) throw new Error('Filter boundaries are reversed');
const candidate = JSON.parse(candidateBytes);
const input = {
  verse: Number(candidate.id.split('.').at(-1)),
  text: candidate.translation.text,
  footnotes: candidate.translation.footnotes,
};
const block = source.slice(start, end);
const script = new vm.Script(`${block}
const selected = shouldStripFootnoteMarkers(translationId);
if (selected) stripBibleFootnoteMarkersInPlace(input);
({ selected, record: input });`);
const cases = ['pob', 'kjv'].map(translationId => {
  const result = script.runInNewContext({
    translationId, input: JSON.parse(JSON.stringify(input)),
  }, {timeout: 1000});
  return {
    translation_id: translationId,
    filter_selected: result.selected,
    before_note_count: input.footnotes.length,
    after_note_count: result.record.footnotes?.length ?? 0,
    after_has_note_array: Object.hasOwn(result.record, 'footnotes'),
    text_changed: input.text !== result.record.text,
    after_text: result.record.text,
  };
});
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
console.log(JSON.stringify({
  mode: 'isolated-execution-of-actual-web-note-filter-block',
  web_data_sha256: sha(sourceBytes),
  candidate_sha256: sha(candidateBytes),
  block_sha256: sha(block),
  first_line: source.slice(0, start).split('\n').length,
  last_line: source.slice(0, end).split('\n').length - 1,
  cases,
  entire_sanitizer_executed: false,
  react_rendered: false,
  deployed_reader_checked: false,
}, null, 2));
