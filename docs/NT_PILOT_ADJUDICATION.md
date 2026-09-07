# New Testament pilot: Mark 1:41

Checked: 2026-09-02 · Method 1.0.0

Generated from the [decision dataset](../sources/textual_restoration/decisions/nt_pilot.v1.json). These are working editorial choices from published readings, not new image restorations, cross-model-reviewed decisions, or published POB changes.

Older witnesses receive a modest preference; no numerical vote or authenticity percentage is used.

## Mark 1:41

**Working preference:** Provisionally prefer compassion; retain anger as a serious alternative to the current POB wording.
**Priority confidence:** moderate (editorial judgment, not a probability).
**Wording-level outcome:** provisional selection within this unit.

| Candidate | Greek excerpt | English effect |
|---|---|---|
| anger | ὀργισθείς | being angry |
| compassion | σπλαγχνισθείς | moved with compassion |

### Witness matrix

Every non-local row below is a published report; archival pixels were not independently re-read in this pass.

| Witness | Language / role | Reported reading | Date basis | Related evidence group | Source |
|---|---|---|---|---|---|
| Current POB / SBLGNT | Greek / critical-edition | being angry | edition-publication: 2010 edition; not an ancient manuscript | modern-editorial-decision | local-baseline |
| Codex Sinaiticus / 01 | Greek / direct-language | compassion | physical-copy: Fourth century CE | early-greek-compassion | bruehler-2024 |
| Codex Vaticanus / 03 | Greek / direct-language | compassion | physical-copy: Fourth century CE | early-greek-compassion | bruehler-2024 |
| Codex Bezae / 05 | Greek / direct-language | anger | physical-copy: Fifth century CE | bezae-latin-related | bruehler-2024 |
| Old Latin D/I families, as reported | Latin / ancient-version | anger | translation-tradition: Ancient Latin evidence; individual copies not dated in this pilot | bezae-latin-related | bruehler-2024 |
| Ephrem, commentary on the Diatessaron | Syriac / retelling | Combined compassion/anger language reported | work-composition: Fourth-century work, not a fourth-century surviving copy | diatessaron-reception | bruehler-2024 |

Baseline: [translation/nt/mark/001/041.yaml](../translation/nt/mark/001/041.yaml).

- **Why prefer it:** Earlier extant Greek support and broader transmission favor compassion. This is not a count of modern editions.
- **Strongest objection:** Anger is a difficult but contextually plausible reading that could have been softened; Bruehler argues for it despite the external balance.
- **Transmission explanation:** The direction of change remains disputed. External convergence presently outweighs the harder-reading argument; no specific copying mechanism is claimed as proven.
- **Effect of age:** Fourth-century Greek witnesses modestly favor compassion over the surviving fifth-century Greek anger witness. The Latin and Syriac evidence means anger cannot simply be dated to that later copy.
- **Independence caution:** Sinaiticus and Vaticanus can share ancestry. Bezae and related Latin families are not independent votes; commentary is a separate, imperfect evidence type.
- **Publication decision:** Stage compassion as a working alternative for further review. POB still says angry; no automatic canonical replacement.

Still unresolved:
- Inspect exact manuscript regions and correction layers before declaring an image-verified result.
- Compare ECM evidence directly and evaluate the competing internal arguments, including the cited Williams and Johnson studies.

### Direct ECM access check — 2026-09-06

The [INTF database directory](https://www.uni-muenster.de/INTF/datenbanken/index.html)
links [Mark Phase 3.5](https://ntg.uni-muenster.de/mark/ph35). Its public
[application metadata](https://ntg.uni-muenster.de/api/mark/ph35/application.json)
returned `name: Mark Phase 3.5` and `read_access: public`. This identifies the
comparison application, not a passage reading or an ECM publication revision.
The NTVMR ECM page and the Mark application did not render a usable apparatus
in the inspected browser state. Direct passage lookup attempts returned HTTP
500; the cause, including possible parameter mismatch, was not established.
No Mark 1:41 witness list, correction layer, local stemma or editorial decision
was retrieved. Do not cite this access check as consulted ECM evidence for
either reading or as confirmation of the provisional preference above.

The bounded attempt stops here. Do not repeat these failed lookups without a
working passage locator or documented parameter correction. Existing published
arguments remain available for further adjudication; the current POB source
and English and the version-1 decision dataset are unchanged.

Not used to force a result:
- SBLGNT/WH/NA/RP edition agreement is not manuscript corroboration.
- Combined commentary language is not treated as an exact two-word reading of Mark.

## Sources

- **bruehler-2024:** [B. B. Bruehler, study of the anger/compassion variant in Mark 1:41](https://theo.kuleuven.be/apps/press/theologyresearchnews/files/2025/09/Bruehler.pdf) — Ephemerides Theologicae Lovanienses 100/2 (2024), pp. 213–230; external evidence on p. 214; DOI 10.2143/ETL.100.2.3293342.
