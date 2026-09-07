# Frozen development controls: image observation

Prepared 2026-09-06. **Four actual-image controls; zero provider runs.** This
is a development smoke test of text-presence observation and false text claims,
not held-out validation, restoration calibration or a character-accuracy test.

## Evidence and labels

The four crops are exact pixels from the registered Library of Congress
Matson photograph of 1QM. This non-biblical Hebrew manuscript is a control for
image observation, not a new biblical textual witness. One crop repeats the
earlier pilot's region-a; the other crops share its photograph and manuscript.
They cannot count as four independent manuscripts or a held-out sample.

The source TIFF was absent locally and was rehydrated once through the existing
hash-verified retrieval code, matching SHA256
`bd13b37adddb7daa709c73652391c4a706d87a86783e991dbfe307ec9ff0bdc2`.
Only this needed master was fetched. The existing preparation script generated
the crops by exact cropping/RGB conversion, without resizing, enhancement,
masking, inpainting or ImageGen. All crops were visually inspected; the wide
third crop's tool display was downsampled, sufficient for text-presence
classification but not used to certify native-scale glyph readings.

The registry's prior rights check records no known publication restrictions,
not a warranty. Attribution: Library of Congress, G. Eric and Edith Matson
Photograph Collection. The [item page](https://www.loc.gov/item/2019705559/)
returned HTTP 403 in this pass; current page contents were not reverified.
The source download succeeded and matched the registered bytes. The large
master stays ignored by Git; the small reproducible crops are retained here.

[Reference labels](reference-labels.json) distinguish two text-present crops
from blue photographic background and an unwritten-looking light surface.
Root labeled the visible regions; an independent agent, shown only the crops
without expected labels, agreed on the four observation classes. That check is
not a second model-family calibration run, paleographic authentication or glyph
ground truth. No uncertain word has been assigned an exact reference spelling.

## Frozen criteria, before provider execution

Run each provider independently with only the frozen prompt, schema and ordered
crops. Do not expose this README, labels, registry, reference, or other model's
response. Use the existing runner's empty-directory/no-tool isolation. Training
contamination remains possible and this development set is not held out.

For **each provider separately**, the smoke-test pass condition is all four
reference observation classes matched: 2/2 text-present and 2/2 no-visible-text,
with zero emitted token objects on either negative crop. A missing, malformed
or failed response is not a correct blank observation. An `unassessable`
response is an abstention, not a pass or invented false-positive reading.

Report raw counts, not only a pass label:

- Correct observation classes / 4; positive classes correct / 2; negative
  classes correct / 2.
- Negative crops with a text-present claim / 2 and number of tokens emitted on
  negatives (even when the output fails semantic validation).
- Abstentions / 4, split by positive/negative class; missing or invalid regions
  separately. Do not drop these from the denominators.
- Pairwise comparison is secondary. Two matching false claims remain errors;
  two matching abstentions do not become blank controls or recovered letters.

A smoke-test failure stops that configuration's use for broader image-reading
acceptance until investigated. Passing only permits continued development; four
selected same-manuscript controls cannot establish an accuracy rate, validate
damage restoration or authorize changes to Hebrew or English. Freeze a new
version before changing images, prompt or thresholds after seeing outputs.

## State and next step

`freeze.json` pins the inputs and reference labels. No `passes/` or comparison
result is fabricated. Actual preparation and `pilot.py validate --pilot` passed
for all four crop hashes. The reference classes were checked, not inferred from
the validator's success message. The repository virtualenv lacks Pillow, so
preparation used the already-bundled Python/Pillow runtime; no package installed.

The second-model access question remains unanswered. Do not rerun the historical
denied request without a legitimate new access route. Once access is available,
use this directory explicitly with `run_pilot.py --pilot` and one provider at a
time; provider compatibility with the new schema is still untested. After the
smoke test, the next calibration requirement is a varied, manuscript-disjoint
evaluation set with defensible character labels, separate real-damage and
artificial-mask strata, and frozen scoring criteria. These four controls do not
replace that requirement.
