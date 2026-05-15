
## [2026-05-15T21:00:00Z] Task: W9-adr-promotion

- D-017 threshold (2 intakes → INFORMED_ESTIMATE) was met by all 4 ADRs (0007–0010) with the 3-intake corpus.
- "Implementation gap ≠ design contradiction" is the key distinction for ADR-0008: GAP-001..005 confirm demand for the atom model, not flaws in it.
- ADR promotion = frontmatter metadata + Status section (first paragraph) + new "## Supporting Evidence" EOF section. Everything else is frozen.
- GAP-007 (ADR-0010 decay semantics: MEDIUM=90d vs know baseline 180d) is maintenance-only, not a demotion trigger — document as residual risk in evidence section.
- All 4 ADRs should be promoted simultaneously when a dependent cluster (0007 depends on 0008; 0009 depends on all three) meets the threshold — asymmetric promotion creates epistemic graph inconsistency.
