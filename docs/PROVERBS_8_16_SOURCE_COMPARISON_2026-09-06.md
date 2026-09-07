# Proverbs 8:16 — justice or earth?

**Application update:** the scoped disclosure is now applied to the repository
verse, retaining the lexical alternatives, Hebrew and main English. The earlier
unapplied language below records the research stage, not current status. See the
[application receipt](../sources/textual_restoration/applications/proverbs8_16_disclosure_application.v1.json)
for the exact change, bounded review and export checks. This is not a new source
selection or a deployed-reader claim.

Checked 2026-09-06 against repository `80edc42da2`. Published-source comparison;
no new manuscript transcription, reconstructed ink or canonical change.

## Result and English consequence

Propose a source-variant disclosure; retain the declared Hebrew and main English
provisionally. [Current POB](../translation/ot/proverbs/008/016.yaml) has “all who
judge justly,” with a note giving justice/righteousness alternatives. Those are
interpretations of `צדק`. They do not disclose the attested alternative `ארץ`,
which would instead characterize the judges by their domain, “of the earth.”
This is a source-word difference, not just a choice of English synonyms.

## Evidence actually consulted

1. **Local Hebrew:** [OSHB/WLC Proverbs](../sources/ot/wlc/Prov.xml), `Prov.8.16`,
   ends `כל שפטי צדק`; no qere is encoded at this verse. The target YAML agrees.
   These are linked digital representations, not independent manuscript votes.
2. **Critical edition:** Michael V. Fox, *Proverbs: An Eclectic Edition with
   Introduction and Textual Commentary* (SBL, 2015),
   [publisher PDF](https://www.sbl-site.org/wp-content/uploads/2024/11/Proverbs_Fox_SBL.pdf),
   printed pp. 154–155 (PDF pages 176–177), visually checked. Fox selects `ארץ`
   and reports it within Hebrew transmission, including the 1525 Rabbinic Bible
   and manuscript collections. The Hilleli attribution is mediated by an
   annotation in Rossi 314, not a surviving Proverbs leaf read here. Aleppo and
   Leningrad are reported for `צדק`; Syriac evidence is divided. Fox argues for
   a universal scope and interprets the rival as an ideological alteration.
   These are his reports and judgment, not our fresh witness collation.
3. **Counterargument:** [NET Proverbs 8:14–17, textual note 5](https://classic.net.bible.org/passage.php?passage=Pro+8:14-17)
   recognizes Hebrew earth-readings but retains righteousness as the harder
   expression. It reports Toy's comparison with Psalm 148:11 as a possible
   explanation for assimilation. Toy's original page was not consulted.
4. **Greek control:** the existing [OpenScriptorium digital text](https://github.com/OpenScriptorium/lxx-morph/blob/c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2/db/seeds/lxx_morph/proverbs.json),
   `Prov 8:16`, ends `κρατοῦσι γῆς`, concerning ruling earth. Only its surface
   text was used. This derivative Rahlfs-labeled dataset is an edition control,
   not a Greek manuscript or independent authority for a Hebrew retroversion.

Fox's conventions matter: ceilings mark departure from Leningrad, not missing
ink; the apparatus separator places his preferred reading first (printed
p. xiii). His agreement/support distinction (p. 78) prevents counting related
translations as independent witnesses. The printed title/copyright identifies
2015; a newer PDF file timestamp does not identify a revised textual edition.

## Competing explanations tested locally

The unchanged Hebrew at Psalm 148:11 has the close sequence of princes and all
judges of earth; Psalm 2:10 and Isaiah 40:23 also contain judges-of-earth language.
These confirm that `ארץ` is idiomatic. They also make assimilation possible:
parallel wording cannot simultaneously be treated as proof of originality while
its copying influence is ignored.

Conversely, Proverbs 8:15 already ends in `צדק`, so influence from the preceding
line could account for that word in 8:16. But purposeful repetition is also
possible. Proverbs 8:4 addresses humanity broadly, while 8:8 and 8:20 emphasize
righteousness and justice. Our inference: universal address and moral governance
coexist in this chapter; neither thematic label settles the direction of change.
In particular, “judging justly” need not mean only Israelite officeholders, and
“judges of earth” need not endorse every ruler's conduct. The current theological
metadata must not become an argument for selecting the source that best fits it.

## Bounded decision

An apparatus-based Hebrew alternative merits disclosure now; earliest priority
remains unresolved. Proposed note, **research-only and unapplied**:

> The retained Hebrew describes judging with justice. Other Hebrew witnesses,
> reported in the critical edition, read “all judges of the earth”; the Greek
> version likewise refers to ruling the earth. Which Hebrew reading came first
> remains uncertain.

This proposal does not approve an exact YAML edit. Preserve the existing lexical
note or integrate its distinct information during a scoped application review.
Do not silently combine both readings in the main text. To reopen source choice,
verify the named Hebrew variant evidence and the relevant versional apparatus,
then test assimilation in both directions; a larger count of dependent editions
or another model's agreement is insufficient. No new restoration images or
per-verse application framework are needed to report this published variant.

## Norzi's correction reports — follow-up, 2026-09-06

The [Minchat Shai unit at 8:16](https://www.sefaria.org/Minchat_Shai_on_Proverbs.8.16?lang=he)
was read directly in Sefaria's original-language digital edition, rather than
only through Fox's summary. The [source snapshot](../sources/textual_restoration/discovery/proverbs8_16_minchat_shai.v1.json)
preserves both Aramaic/Hebrew segments, version metadata and retrieval hash.
The API's community English translation contains only the first segment; it
was not used as evidence. No identified print exemplar is given in the returned
version source, so this is not a verified edition-to-manuscript collation.

The first segment reports copies altered from `צדק` to `ארץ`, others altered
the other way, copies combining `ארץ צדק`, and inner/outer placement of the two
readings. It does not give us photographs, shelfmarks or datable hands for these
interventions. The second segment continues the preceding lexical-reference
list, then describes earth erased and justice written in the Or Torah author's
book. In the quoted discussion, Hilleli is invoked for a correction to earth,
but justice is preferred, with a mnemonic linking the endings of adjacent
verses. The abbreviation `בס"ס` is retained without speculative expansion.

**Effect on adjudication:** bidirectional correction is now a directly consulted
historical report, not merely our hypothetical pair of copying explanations.
It does not establish which reading is earliest, why a particular scribe changed
it, or whether the combined form was original. Norzi's report and Fox's use of
that report must not be counted twice as independent witness support. The
two digital segments likewise form one commentary unit, not two witnesses.
Retain the existing source and the unapplied disclosure proposal. For source
selection, the remaining discriminator is identified witness/hand evidence and
its transmission relationship—not more copies of this same report.

The web reader could not open the Sefaria page/API; direct API retrieval
succeeded. Original-language contents are labeled public domain by that API.
No website composition date or medieval-category label was adopted. This pass
does not verify Rossi 314, the Hilleli attribution, the 1525 printed Bible or any
physical erasure; the narrower documentary finding must retain that boundary.

## Reproduction and limits of the initial comparison

- Target YAML SHA256: `eb4426f203a6b05bc79c4b7ef0ae1b82ea50e622a05babcae73c54b6a4a87148`.
- `Prov.xml`: `964f99c00239b53b854c4686c99490c8d1ac7664784a30afdfc23781a3abb161`.
- `Ps.xml`: `fe55eef316a65fb0f46d833d526ca2fd722e86ff7339f1a39f0c5b7f9062ced2`.
- `Isa.xml`: `0807678de609bdef284bed5400b94ddab570d101b593c7f59ae1939015572fa2`.
- Greek JSON at the linked commit: `7791907ce0c410bdb99502db909bd417d3dc26261b4959aa1f6f02033d8e5de5`.
- Publisher PDF: `1953e00d7275c1bda5031378b347fba65348bc08855ec0f8757841ca6cdc1c39`.

The PDF's relevant sigla, source descriptions and policy sections were also read
(pp. xiii–xxii, 17, 36, 78, 81–82); no complete-book review is claimed. Web PDF
retrieval returned 403; direct download succeeded. Missing `pdftotext` was
handled by bundled `pypdf`, with the decisive pages checked as rendered images.
No full PDF or new external corpus is vendored. Credit OSHB for its annotations;
its vendored licensing distinguishes them from the public-domain WLC text.

A bounded publisher/edition-status search found no consulted passage-specific
erratum; this is not exhaustive later-literature clearance. The Göttingen
publication page yielded no Proverbs match, and its catalogue page returned no
readable body through the web reader: no newer full Greek apparatus was verified
or consulted. No BHQ apparatus, original Rossi/Hilleli evidence, Syriac manuscript,
or new Judean Desert coverage was inspected. These access/coverage limits must
not be converted into evidence of agreement or absence.
