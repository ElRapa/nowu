---
artifact_type: INTAKE_BRIEF
intake_id: intake-007
status: DONE
altitude: DELIVERY
phase: IDEA
epistemic_grade: HYPOTHESIS
created_at: 2026-05-14
appetite: 8h
affected_modules: [core, flow]
use_case_ids: [AP-01, AP-02, AP-06]
workflow_mode: A
source_work_item: W27
s1_validated_at: 2026-05-14T00:00:00Z
---

# Intake Brief: AP Domain Project Bootstrap — Regulatory, Formulation, and Decision Knowledge

## Problem Statement

Launching and running an aperitif business requires tracking a dense, evolving body of
domain knowledge — regulatory requirements with dependencies and deadlines, product
formulations with version histories and rationale, and business decisions that need to be
revisited as conditions change. This information currently lives in scattered notes,
spreadsheets, and memory, with no structured way to query it, trace it, or maintain its
accuracy over time.

## Use Cases

- **AP-01: Track Regulatory Requirements as Living Knowledge**
  - **Stage Target**: v1
  - **Actor**: Human (researcher); Agent (tracker)
  - **Situation**: Multiple Philippine regulatory bodies (FDA, BIR, DTI, LGU, barangay) must be satisfied to legally sell an alcoholic food/beverage product — each with its own requirements, dependencies, and renewal timelines.
  - **Need**: Capture each requirement with source, confidence level, dependency relationships, and status. Surface what is blocking what and alert when something may have changed.
  - **Success**: The human can ask "what do I still need to do to legally sell this product?" and receive a dependency-ordered, accurate answer reflecting current state.
  - **Failure**: A critical dependency is missed or forgotten; launch is delayed because a required permit was not obtained in the correct order.

- **AP-02: Manage Product Formulation as Versioned Knowledge**
  - **Stage Target**: v1
  - **Actor**: Human (formulator); Agent (recorder, searcher)
  - **Situation**: The aperitif recipe evolves through iteration. Each version has specific parameters (ingredients, ratios, maceration time, shelf-life targets), taste outcomes, and cost implications; some are abandoned, one becomes production.
  - **Need**: Record each formulation version with its parameters and rationale, link to test results and cost analysis, and make it easy to compare versions or revisit abandoned approaches.
  - **Success**: The human can ask "why did we abandon version 3?" and receive the decision and rationale. When input conditions change (ingredient cost, regulation), affected formulations are surfaced.
  - **Failure**: Recipes exist as unlinked notes. Version history is lost. A formulation proven to fail is re-tested because the outcome was not recorded.

- **AP-06: Evaluate a Business Decision With Traceability**
  - **Stage Target**: v1
  - **Actor**: Human (decision-maker); Agent (analyst, recorder)
  - **Situation**: The business faces decisions with cost, branding, regulatory, and supply chain implications (e.g., glass bottles vs pouches) that need to be reasoned through systematically and retrievable later.
  - **Need**: Structure the decision — options, criteria, evidence, recommendation, chosen path with rationale — and store it so it can be revisited when conditions change.
  - **Success**: Months later, the original decision is retrieved with full reasoning, and the human can evaluate whether those reasons still hold given new conditions.
  - **Failure**: Decisions are made and forgotten. The same analysis is repeated from scratch, or contradictory decisions are made without awareness of the previous conclusion.

## Acceptance Criteria

1. Representative AP-domain knowledge artifacts (at least one regulatory requirement, one formulation version, one business decision) can be expressed using nowu's existing workflow artifact structures without AP-specific extensions to the framework.
2. Dependency and versioning relationships between AP knowledge items can be represented conceptually (schema or artifact structure proposed); gaps where current structures cannot express them are documented as follow-on work items.
3. At least one AP-06 business decision is walked through the existing S1-S9 workflow, demonstrating structural equivalence to the NF-02 decision pattern — same workflow, same template shape, different domain content.
4. No bespoke AP management system is created; all AP knowledge lives in nowu's existing artifact and workflow structures.
5. Blocking gaps (capabilities required but not yet available) are documented with traceability to specific work items (K3, K9, K13, W19, W20).

## Affected Modules

- **core**: Contracts relevant to representing AP knowledge types within existing schemas.
- **flow**: Pipeline traversal; S1-S9 workflow must process an AP-domain intake without AP-specific logic.

## Appetite

8 hours. This is a domain bootstrap producing first evidence, not a full domain management
implementation. If the work takes longer than 8 hours, scope should be cut to the minimum
required for validation, not time extended. Cut scope, not time.

## Context

W27 is the first domain-specific intake in the nowu project. The v1-core work (W1–W6, K2,
W29, W32, W8) has been completed and the v1-core gate criteria are all met. W27 is the
first v1 work item to be executed.

The strategic significance: if nowu's workflow cannot manage knowledge for a real
non-software domain — an aperitif business in the Philippines, with real regulatory
complexity, real formulation evolution, and real business decisions — the claim that nowu
is a "domain-agnostic framework" is weakened. R3 in the risk register captures this risk.
This intake is the first evidence run against T5 (Domain Agnosticism), T2 (Knowledge
Persistence), and T6 (Observability and Traceability).

The AP use cases were selected for v1 because they test different knowledge structures:
AP-01 tests structured knowledge with dependencies, AP-02 tests versioned knowledge with
rationale, and AP-06 tests traceable decisions in a non-software domain.

Prior art: intake-001 (NF-01) validated the workflow pipeline itself. W27 validates the
workflow against a domain it was not originally built around.

## Open Questions

1. **Q1 — Minimum viable AP structure**: What is the minimum AP knowledge structure that
   produces useful evidence for T5 without over-engineering? The 8h appetite is the forcing
   function.

2. **Q2 — Dependency modeling for AP-01**: How should regulatory requirement dependencies
   be represented? As structured metadata within artifacts, as relationship references, or
   as something the current model cannot express (documented gap)?

3. **Q3 — Versioning for AP-02**: Can formulation version tracking be expressed using
   existing artifact versioning conventions, or does it require capabilities not yet
   available (K9 territory)?

4. **Q4 — Decision template reuse for AP-06**: AP-06 (business decisions with
   traceability) appears structurally similar to NF-02 (architectural decisions). Can the
   same workflow and template be reused directly?

5. **Q5 — know integration surface**: The current MemoryService Protocol has limited
   methods. Is this intake's scope achievable with artifact-level representation alone, or
   does it require MemoryService expansion (K3 territory)?

---

## S1 Validation Annotations

### UC Confirmation

AP-01, AP-02, and AP-06 are confirmed ACTIVE in docs/USE_CASES.md with stage_target:
v1. All three are listed in ROADMAP-003.md Section 2 under W27. The UC definitions are
internally consistent with the problem statement and acceptance criteria in this intake.

AP-03, AP-04, AP-05, and AP-07 are explicitly out of scope for W27 — their stage
targets are v1.1 or v1.2.

### Field Completeness Check

| Field | Present | Valid |
|---|---|---|
| problem_statement | yes | yes — user-centric, no solution language |
| use_case_ids | yes | yes — AP-01, AP-02, AP-06 confirmed ACTIVE, v1 |
| acceptance_criteria | yes | yes — 5 criteria, evidence-based framing |
| affected_modules | yes | yes — core, flow (know is WATCH) |
| appetite | yes | yes — 8h with explicit scope-cut instruction |
| context | yes | yes — W27 traceability, T5 thesis framed |
| open_questions | yes | yes — 5 questions, each maps to a concrete S2 decision |

### Implicit Assumptions

1. **Existing artifact structures are sufficient to represent AP knowledge at bootstrap
   level.** This is the primary hypothesis being tested. If S2 finds they cannot, gaps
   should be documented as follow-on work (W19, K3, K9).

2. **AP-06 and NF-02 are structurally equivalent at the workflow level.** AC-3 asserts
   this. If S2 finds they are not equivalent, the gap should be documented and scope
   adjusted.

3. **flow module requires no domain-aware logic to process an AP intake.** This is the
   core T5 assumption. If the pipeline requires AP-specific branching, T5 is not
   validated and a gap should be surfaced.

4. **8h appetite is calibrated to evidence gathering, not production.** The acceptance
   criteria are proof-of-concept level. S2 and S5 must resist scope creep.

### Module Dependency Map

```
intake-007 touches:

  core  <-- primary
    - Contracts relevant to AP knowledge representation
    - Existing schemas assessed for AP fit

  flow  <-- validation target
    - Must process AP domain intake without domain-specific logic
    - If flow requires AP-specific branching, T5 is not validated

  bridge  <-- OUT OF SCOPE
  soul   <-- OUT OF SCOPE

  know  <-- WATCH
    - Knowledge persistence (K3) is not yet implemented
    - MemoryService Protocol surface is limited (4 methods)
    - If any AC requires writing to a knowledge store beyond
      current contract surface, it is out of scope for this intake
    - Documented as gap with K3 traceability
```

### Story Boundaries

**IN SCOPE:**

- Express representative AP knowledge artifacts using existing workflow structures.
- Assess whether existing schemas cover AP-01, AP-02, AP-06 knowledge structures.
- Walk one AP-06 decision through S1-S9 workflow to demonstrate domain-agnostic reuse.
- Document gaps where current structures cannot express AP-domain requirements.
- Confirm T5: the S1-S9 workflow processes an AP-domain intake without modifications.

**OUT OF SCOPE (explicitly):**

- Full regulatory requirement tracking system (K13 — v1.1+).
- Full formulation version management (K9 — v1.2 territory).
- Domain extension pack for AP (W19/ADR-0011 — parallel v1 work item).
- Traceability metadata standard implementation (W20 — parallel v1 work item).
- AP-03, AP-04, AP-05, AP-07 — v1.1 and v1.2 stage targets.
- K3 implementation or MemoryService expansion.
- Any bridge or soul work.

**DEFERRED (known future work):**

- W9: Promote hypothesis ADRs based on intake evidence.
- W19: ADR-0011 domain extension model.
- W24: AP/RE domain deepening execution plan (v1.2).

---

```yaml
from_step: S1
to_step: S2
agent: nowu-constraints
status: DONE
```
