# Diplomatic transcriptions

No Hebrew or Aramaic word has been accepted from the four pilot photographs
yet. The preview images establish the acquisition and enhancement pipeline, but
they do not provide enough controlled detail for a defensible independent
transcription. The full-resolution TIFFs improve the source, but the first
automated pass still requires a stronger ancient Hebrew/Aramaic vision pass and
a second, different model family before any reading can affect POB.

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
