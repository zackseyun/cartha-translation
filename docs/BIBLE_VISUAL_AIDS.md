# Bible visual aids

Bible visual aids are a supplemental, opt-in layer. They never replace the
Scripture text and must not present an AI reconstruction as archaeological
certainty.

## Pipeline

1. **Discover:** run `tools/bible_visual_aid_candidates.py` across the canonical
   verse records. The JSONL output is a review queue, not a publishing catalog.
2. **Review:** an editor confirms that a visual would clarify the passage,
   chooses a type (reconstruction, map, diagram, object, nature, or symbolic),
   and adds historical/source constraints.
3. **Generate:** use Codex Image Gen with the approved prompt. One approved
   concept produces one final asset; discarded variants do not enter the
   catalog.
4. **Verify:** check historical plausibility, human dignity, unwanted text,
   misleading certainty, and whether the image actually clarifies the verse.
5. **Publish:** upload the final image plus a per-book versioned JSON manifest
   under `bible-visual-aids/v1/`. Mobile and web fetch the same public catalog.

Generated queues and image binaries are production artifacts and must not be
committed to this translation repository.

```bash
python tools/bible_visual_aid_candidates.py \
  --translation-root translation \
  --out /tmp/bible-visual-aid-candidates.jsonl
```

Each published manifest entry includes a verse range, title, alt text, caption,
image URL, visual type, historical-certainty label, prompt version, generator,
and review timestamp. The reader displays a **Visual aid** pill only when an
approved entry exists, then opens a dismissible full-image sheet with the
caption and reconstruction disclaimer.
