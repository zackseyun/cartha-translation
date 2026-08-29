# Ancient church orders: source and publication plan

The reader includes these four works as **historical early-Christian texts**, not
as an expanded New Testament canon. Their requested reader order is:

1. Didascalia Apostolorum
2. Apostolic Tradition
3. Apostolic Church Order
4. Apostolic Constitutions

This order is a discovery sequence, not a claim that every work directly
depends on the one immediately before it. In particular, the dating and unity
of the material called *Apostolic Tradition* remain disputed.

## Current complete witness bridges

| Work | Reader units | Public-domain English witness | Ancient-language basis still to review |
|---|---:|---|---|
| Didascalia Apostolorum | 26 chapters | R. Hugh Connolly, *Didascalia Apostolorum* (Oxford, 1929), proofed HTML at Early Christian Writings | Lost Greek original; complete Syriac version; Verona Latin fragments |
| Apostolic Tradition | 38 numbered units | Burton Scott Easton, *The Apostolic Tradition of Hippolytus* (1934), Project Gutenberg ebook 61614 | Latin, Sahidic, Arabic, Ethiopic, and surviving Greek fragments; competing reconstructions must not be silently blended |
| Apostolic Church Order | 30 chapters | Henry Tattam, *The Apostolical Constitutions, or Canons of the Apostles, in Coptic* (1848), Internet Archive | Greek and the ancient Latin, Syriac, Sahidic, Bohairic, Arabic, and Ethiopic versions; current bridge follows Tattam's Bohairic witness |
| Apostolic Constitutions | 8 books | James Donaldson in *Ante-Nicene Fathers* VII (1886), CCEL public-domain text | Greek manuscript tradition; dependencies on the Didascalia, Didache, and earlier church-order/liturgical material must remain visible |

Every generated YAML preserves the complete English witness, edition,
translator, URL, license statement, manuscript description, and an explicit
`source_language_review: pending` gate. The initial reader text intentionally
does **not** pretend that mechanical modernization is a new translation.

## Composition plan

1. Establish a source-language packet for each reader unit, preserving lacunae,
   variant recensions, and edition-specific supplements.
2. Compose clear modern English directly from that packet, using the public-
   domain English only as an audit witness.
3. Run an independent grounding review against every available ancient
   witness; do not normalize church offices, liturgical language, or disputed
   theology to a modern denomination.
4. Replace `provisional_source_bridge` only after the direct review is complete.

The import is reproducible with:

```bash
python3 tools/church_orders/import_public_domain_witnesses.py
python3 tools/extra_texts/validate_catalog.py --all
```
