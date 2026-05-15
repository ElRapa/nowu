---
artifact_type: CONSTRAINTS_SHEET
id: intake-007-constraints
intake_id: intake-007
created_at: 2026-05-14
status: READY_FOR_OPTIONS
altitude: ARCHITECTURE
phase: ANALYSIS
epistemic_grade: HYPOTHESIS
arch_pass_ref: ~
source_work_item: W27
---

# Constraints Sheet: intake-007

> If `arch-pass-NNN` exists from pre-workflow, this sheet extends it — do not replace it.
> Document divergences from arch-pass in the section below.

## Affected Modules

| Module | Container (C4 L2) | Impact | Confidence |
|---|---|---|---|
| core | Core Contracts | query (assess schema fit) | HIGH |
| flow | Workflow Orchestrator | validation target (domain-agnostic proof) | HIGH |
| know | Knowledge Store (`../know`) | WATCH — not in scope unless S3 promotes | MED |

## Primary Constraint: Contract Surface Gap

The `know` sibling module supports generic atom CRUD (`create_atom`, `query_atoms`,
`add_connection`, `subgraph`, `get_atom_versions`). However, nowu's `MemoryService`
Protocol exposes only 4 methods: `record_decision`, `create_task`, `task_overview`,
`recall_context`. These are task/decision-skewed, not general-purpose.

**Implication**: W27 cannot honestly claim "AP atoms created, stored, queried through
nowu's knowledge model" because the integration surface doesn't support it. The revised
intake (v2) scopes W27 to artifact-level representation and gap documentation, with
know integration deferred to K3.

## Binding Decisions

| D-ID | Title | How it constrains this work |
|---|---|---|
| D-001 | File-Based Memory Architecture | AP validation evidence must be representable as Markdown+YAML artifacts in `state/`. |
| D-002 | DDD Layer Architecture | Any AP memory access from nowu must remain behind `core/contracts` Protocol boundaries. |
| D-003 | 5-Module Structure | Scope constrained to `core`/`flow` concerns; `bridge` and `soul` not required. `know` is WATCH. |
| D-006 | Treat `know` as external memory system of record | AP domain knowledge must eventually align with `know`'s atom model, but W27 demonstrates artifact-level fit only. |
| D-009 | Standardize role-driven workflow with VBR and approval tiers | Pulling forward K3/W19 implementation requires explicit Tier-2+ escalation, not silent expansion. |
| D-013 | 5×10 Altitude-Phase Workflow Model | W27 architecture artifacts must carry ARCHITECTURE/ANALYSIS framing. |
| D-015 | Epistemic Grades with Tiered Enforcement | AP-derived artifacts must carry explicit epistemic grades. |
| D-017 | Minimum Viable Architecture (Hypothesis ADRs + Feedback Loop) | ADR-0008/0009/0010 are hypothesis-grade constraints under validation, not to be re-litigated within S2. |
| D-020 | Staged Plan: Areas × Stages | W27 is a staged validation slice; must preserve appetite-bound scope. |
| ADR-0008 | Knowledge Atom Model & Lifecycle | Canonical atom schema is binding; AP UCs must map to existing types unless extension is designed via W19/ADR-0011. |
| ADR-0010 | Epistemic Grade Assignment & Propagation | AP artifacts must include grade semantics; composite outputs inherit uncertainty. |

## Binding Contracts

| Contract | Interface | Constraint |
|---|---|---|
| `TaskSpec` | `core/contracts/types.py::TaskSpec` | Shaping must preserve explicit scope boundaries; AP bootstrap cannot blur into open-ended domain build-out. |
| `DecisionRecord` | `core/contracts/types.py::DecisionRecord` | AP-06 decisions should conform to existing structure. Note: `DecisionRecord` has 5 fields (title, rationale, risks, mitigations, use_case_ids) — may be insufficient for full AP-06 evidence/options/criteria needs. Gap should be documented if confirmed. |
| `MemoryService` | `record_decision`, `create_task`, `task_overview`, `recall_context` | Protocol surface is minimal and task/decision-skewed. No general atom CRUD exposed. W27 does NOT depend on expanding this — gaps documented for K3. |

## Architectural Risks

| Risk | Severity | Mitigation |
|---|---|---|
| W27 evidence is mistaken for capability completion — downstream work assumes AP knowledge is fully integrated when only artifact-level representation was proven. | HIGH | AC-5 explicitly requires blocking gaps to be documented with work item traceability. Constraints sheet and S5 shaping must reinforce "evidence run, not capability delivery." |
| `DecisionRecord` may be too narrow for AP-06 full evidence chain (options, criteria, weighted scoring, revisitation logic). | MED | Document the gap if confirmed. Do not extend `DecisionRecord` within W27 — that's K3/W19 territory. Use supplementary artifact fields if needed for the demonstration. |
| 8h appetite can trigger scope creep from "domain bootstrap validation" into "full AP management system." | MED | Enforce AC boundaries. AP-06 is the primary proof point (cheapest to demonstrate). AP-01/AP-02 are secondary — minimal representation + gap documentation. |
| AP-01 dependency ordering may exceed what existing artifact structures can express. | MED | Limit claim to representability. If traversal requires graph semantics beyond current structures, document as gap for K3/K13. |
| ADR-0010 decay semantics (medium=90d in spec vs 180d in `know` implementation) may affect AP-01 regulatory freshness claims. | LOW | Note the discrepancy. Do not attempt to resolve within W27 — it's ADR-0010 maintenance. |

## Divergences from arch-pass (if applicable)

| arch-pass says | This analysis says | Rationale |
|---|---|---|
| N/A | No pre-workflow arch-pass — constraints derived cold. | intake-007 enters S2 without a prior `arch-pass-NNN`. |

## Open Questions for S3

1. What is the minimum artifact structure that demonstrates AP-01 regulatory requirements can be expressed using existing schemas? Is a single representative artifact sufficient, or do we need a small graph (2-3 requirements with dependency relationships)?
2. For AP-02 formulation versioning: can existing artifact conventions (supersedes, version numbering) express the iterative recipe evolution pattern, or is this a documented gap?
3. What is the minimal equivalence criterion between AP-06 and NF-02 using existing `DecisionRecord`? If `DecisionRecord` fields are insufficient, what supplementary structure demonstrates the pattern without extending contracts?
4. Should S3 options be scoped as (a) pure artifact validation, (b) artifact validation + thin schema proposal, or (c) artifact validation + minimal code change? The revised intake AC favors (a) with gap documentation.
5. How should blocking gaps be structured as deliverables? As a gap register artifact, as entries in the intake's acceptance output, or as individual follow-on intake briefs?

***
```yaml
from_step: S2
to_step: S3
agent: nowu-options
status: READY_FOR_OPTIONS
```
