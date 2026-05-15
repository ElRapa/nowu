---
artifact_type: AP_EVIDENCE
status: ACCEPTED
created_at: 2026-05-15
intake_id: intake-007
decision_id: D-027
use_case_id: AP-06
---

# AP-06 S1-S4 Decision-Shape Proof — Packaging Decision (Glass Bottles vs Pouches)

## Proof Objective

Demonstrate that a concrete AP-06 business decision can be represented using existing
nowu S1-S4 decision artifact shapes (domain-agnostic workflow reuse), while explicitly marking
where `DecisionRecord` (5 fields) is insufficient and supplementary artifact structure
is required.

---

## S1-Style Intake Mirror (mirrors: `INTAKE_BRIEF` problem framing)

**Decision question:** Should the first Philippine production run use glass bottles or
pouches for a calamansi-herbal aperitif?

**Problem statement:** Packaging choice affects unit economics, FDA compliance execution,
brand perception in Metro Manila specialty retail, shelf-life integrity in humid storage,
and lead-time risk from local packaging suppliers.

**Why this matters now:** First run is planned at ~600 units; wrong packaging choice can
either over-commit cash (too premium too early) or undercut brand-position fit (too
commodity for target channels).

**Trace link:** `use_case_id: AP-06`.

---

## S2-Style Constraints Mirror (mirrors: `constraints` artifact shape)

1. **Cost constraint**
   - Target landed packaging cost should remain within gross-margin guardrails for
     introductory SRP assumptions.
2. **Branding constraint**
   - Product must present as craft/premium enough for curated stores and bar placements.
3. **Regulatory constraint (Philippines FDA)**
   - Label must support required food labeling disclosures (product identity, net content,
     ingredients, allergen declarations where applicable, importer/manufacturer details,
     lot/batch traceability fields) in a compliant, legible format.
4. **Supply-chain constraint**
   - Packaging must be procurable with predictable lead times from local vendors.
5. **Shelf-life/quality constraint**
   - Packaging barrier/performance must protect product quality through intended shelf life
     under typical Philippine heat/humidity handling conditions.

---

## S3-Style Options Mirror (mirrors: `options` artifact shape)

### Option A — Glass bottles only
- Strong premium shelf presence, easier perceived quality signaling.
- Higher per-unit packaging + freight weight cost; higher breakage handling risk.

### Option B — Pouches only
- Lower packaging and logistics cost, lightweight for test distribution.
- Weaker premium signal in some channels; label real estate/layout constraints.

### Option C — Both (glass for premium channels, pouches for market test)
- Portfolio split: glass in premium outlets; pouches for sampling/early-market learning.
- Operational complexity: dual SKUs, dual procurement streams, higher coordination overhead.

---

## S4-Style Decision Mirror (mirrors: `decision` artifact shape)

### Criteria and Weights

| Criterion | Weight |
|---|---:|
| Unit economics at 600-unit launch scale | 30% |
| Brand fit for premium positioning | 25% |
| FDA labeling practicality/compliance confidence | 20% |
| Supply reliability and lead-time resilience | 15% |
| Shelf-life/quality protection confidence | 10% |

### Weighted Scoring (1–5)

| Option | Econ (30) | Brand (25) | FDA (20) | Supply (15) | Shelf-life (10) | Weighted Total |
|---|---:|---:|---:|---:|---:|---:|
| A: Glass only | 2 | 5 | 4 | 3 | 4 | 3.50 |
| B: Pouch only | 5 | 2 | 3 | 4 | 3 | 3.50 |
| C: Both | 3 | 4 | 4 | 2 | 4 | 3.40 |

### Chosen Path

**Choose Option C (Both), with phased bias:**
- Month 1–2: glass prioritized for premium channel validation.
- Controlled pouch batch for market-testing price elasticity and repeat behavior.

### Rationale for choosing C despite slightly lower weighted score

Option C is selected as a **risk-hedging strategy**: it preserves premium brand signal
while generating early demand-learning data at lower pouch cost in parallel. In this
stage, learning value and strategic flexibility are prioritized over single-path score
maximization.

### Rejected Alternatives

- **A only rejected:** concentration risk on cost and breakage before demand certainty.
- **B only rejected:** risks diluting early premium positioning objective.

---

## Evidence Section (supplementary structure; not in DecisionRecord)

1. **Cost evidence**
   - Quotations from at least two local bottle suppliers and two pouch converters
     (unit + MOQ + lead time + freight assumptions).
2. **Regulatory evidence**
   - FDA Philippines labeling requirement checklist mapped to each format's printable area
     and lot traceability implementation.
3. **Competitor/channel evidence**
   - Shelf scan of comparable local craft liqueur/aperitif products by package type,
     price point, and channel placement (specialty retail vs general trade).
4. **Quality evidence**
   - Basic accelerated storage observations and closure integrity checks by packaging type.

---

## Revisitation Trigger (supplementary structure; not in DecisionRecord)

Revisit this decision when any of the following occurs:

1. Production volume exceeds **1000 units/month**.
2. FDA labeling rules materially change for applicable product category.
3. Packaging cost changes by **>20%** for glass or pouch supply.

---

## Crosswalk Anchor

## NF-02 Structural Equivalence Crosswalk

| NF-02 Decision Shape (from templates/decision.md) | AP-06 Section | Status |
|---|---|---|
| Context (situation requiring decision) | S1 Problem Framing | ✅ Met |
| Decision (one clear sentence) | S4 Chosen Path | ✅ Met |
| Rationale (why this over alternatives, QA scoring) | S4 Weighted Scoring + Rationale | ✅ Met |
| Alternatives Considered (option, pros, cons, rejected because) | S3 Options A/B/C | ✅ Met |
| Consequences (positive, negative, neutral) | [supplementary — not in DecisionRecord contract] | ⚠️ Supplementary |
| Evidence catalog | Evidence section | ⚠️ Supplementary (not in contract) |
| Revisitation trigger | Revisitation section | ⚠️ Supplementary (not in contract) |

## Mapping to Existing Contracts vs Supplementary Needs

### What existing contracts can carry directly

- **`DecisionRecord.title`** → "First production run packaging path"
- **`DecisionRecord.rationale`** → summary rationale for chosen path
- **`DecisionRecord.risks` / `mitigations`** → major downside handling
- **`DecisionRecord.use_case_ids`** → `["AP-06"]`
- **`TaskSpec.use_case_ids`** → task-level AP-06 traceability

### What required supplementary artifact structure

The following AP-06 proof elements are required by business-decision traceability but are
not first-class fields in `DecisionRecord`:

- Structured option set (`A/B/C`) with explicit rejected alternatives.
- Multi-criteria table + weighting + score math.
- Evidence links/catalog (quotes, regulatory checklist, competitor scan, test logs).
- Recommendation vs chosen path distinction.
- Revisit conditions/thresholds.

This confirms structural workflow reuse is possible, but evidence-complete AP decisions
need an expanded decision artifact shape around (not replacing) the current 5-field
contract.
