---
artifact_type: AP_EVIDENCE
status: ACCEPTED
created_at: 2026-05-15
intake_id: intake-007
decision_id: D-027
---

# AP-02 Mini Formulation Version Chain (Philippine Aperitif)

## Scope

This artifact captures a two-version formulation chain for a coconut-pili aperitif concept, including explicit supersession, outcome notes, and change rationale.

## Version Chain

### FORM-AP02-v1 — Initial Coconut-Pili Aperitif

- **version_id**: FORM-AP02-v1
- **created_at**: 2026-04-18
- **status**: ABANDONED
- **parameters**:
  - **ingredients_ratios**:
    - Coconut water base: 60%
    - Pili nut infusion: 15%
    - Calamansi citrus: 10%
    - Local honey: 8%
    - Botanical blend: 7%
  - **process**:
    - Maceration time: 72 hours
    - Filtration: single-pass fine mesh
    - Batch size: 20 L pilot
  - **shelf_life_target**: 6 months
- **outcome**:
  - Taste notes: approachable nose; finish perceived as too sweet; pili character too subtle
  - Shelf-life observations: stable at 4-week accelerated ambient observation; no visible separation
  - Cost: ₱85 per 250ml bottle (pilot-scale estimate)
- **rationale_for_change**: Baseline prototype to test local ingredient harmony and market-fit for aperitif profile.
- **supersedes**: null
- **decision**: Abandoned as base formula due to excessive sweetness and insufficient pili expression for target aperitif profile.

### FORM-AP02-v2 — Reduced Sweetness, Enhanced Pili

- **version_id**: FORM-AP02-v2
- **created_at**: 2026-04-29
- **status**: ACTIVE
- **parameters**:
  - **ingredients_ratios**:
    - Coconut water base: 55%
    - Pili nut infusion: 22%
    - Calamansi citrus: 12%
    - Local honey: 4%
    - Botanical blend: 7%
  - **process**:
    - Maceration time: 96 hours
    - Filtration: dual-pass (fine mesh + paper)
    - Batch size: 20 L pilot
  - **shelf_life_target**: 6 months
- **outcome**:
  - Taste notes: better balance and stronger pili identity; calamansi perceived as slightly sharp on finish
  - Shelf-life observations: no haze formation by week 5 ambient check; sensory profile stable but still under observation
  - Cost: ₱92 per 250ml bottle (pilot-scale estimate)
- **rationale_for_change**: Taste panel feedback on v1: "too sweet for an aperitif, needs more character"; reformulated to reduce sweetness and amplify pili signature.
- **supersedes**: FORM-AP02-v1
- **decision**: Selected as current active baseline for next iteration; retain while tuning citrus sharpness in future candidate version.

## Lineage Summary

- `FORM-AP02-v1` → `FORM-AP02-v2`
- v2 is intentionally linked to v1 through explicit `supersedes` and rationale narrative for traceable iteration history.

## Representational Limits

### What CAN be expressed with current nowu artifact structure

- Frontmatter-level version evidence linkage (`intake_id`, `decision_id`, draft state).
- Explicit version IDs and predecessor linkage using `supersedes`.
- Structured formulation parameters, process settings, outcomes, and change rationale in Markdown.

### What CANNOT be expressed with current structure

- No automated diff/comparison engine between formulation versions.
- No automatic cost-impact alerts when parameter changes increase unit cost.
- No ingredient-level machine-traceable change history beyond manual narrative fields.
- No retrieval/query surface in `MemoryService` to fetch, compare, or traverse versions programmatically (K3 gap in addition to K9 semantics).
- Lineage model is linear (`v1 -> v2`) and does not represent branching formulation paths (e.g., `v1 -> v2a` and `v1 -> v2b`).
- No immutable version-identity/effective-date semantics beyond simple `created_at` stamps.
- No first-class linkage fields to tie each version to test evidence or cost-analysis artifacts despite intake requirement to link those proofs.

### Follow-on work references

- **K9**: Formulation/version management capability needed for deeper version semantics and comparison workflows.
- **W19**: Domain extension model work needed to standardize AP-specific version metadata and evolution patterns.
