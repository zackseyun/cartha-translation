# Diplomatic transcriptions

No Hebrew or Aramaic word has been accepted by two-model consensus yet. A
[fresh GPT-5.6 Sol vision proposal](../pilots/2026-09-02-dual-vision/RESULTS.md)
now exists for two original-resolution TIFF crops. Most readings are marked
uncertain. Claude Code's service blocked inference because organization access
is disabled, so there is no second reading and no published POB change.

The saved pilot includes the exact blind inputs, first-pass data, failed-attempt
history, provider rerun tool, and fail-closed comparison tests. The ordinary
Tesseract baseline remains a separate historical result, not evidence that all
vision-model transcription is unusable.

This is a deliberate **no-guess** result, not missing provenance. A future
record must:

1. validate against `schemas/dss-transcription.schema.json`;
2. identify the exact source image and rectangular region;
3. preserve line endings and lacunae;
4. tag every supplied character by method;
5. keep blinded passes from different model families separate until
   reconciliation;
6. promote exact agreement to `machine-consensus-accepted` for visible text or
   `machine-consensus-restored` for supplied text;
7. preserve brackets and restoration provenance even after acceptance; and
8. keep model disagreements out of the main translation until another
   independent pass resolves them.

See `initial_pilot.json` for the queued regions and the reason no word was
promoted from the initial feasibility pass.
