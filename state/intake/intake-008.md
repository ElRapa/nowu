---
artifact_type: INTAKE_BRIEF
intake_id: intake-008
status: DONE
altitude: DELIVERY
phase: IDEA
epistemic_grade: HYPOTHESIS
created_at: 2026-05-15
appetite: 8h
affected_modules: [core, flow]
use_case_ids: [RE-01, RE-06]
workflow_mode: A
source_work_item: W28
s1_validated_at: 2026-05-15T00:00:00Z
---

# Intake Brief: RE Domain Bootstrap — Process Inventory and Long-Horizon Decision Tracking

## Problem Statement

The RE domain currently depends on undocumented institutional knowledge for process execution
and investment reasoning. Core operating processes (listing, tenant onboarding, contract
management, maintenance handoffs) and long-term investment assumptions are difficult to trace,
audit, or revisit after time passes, which creates repeated analysis and avoidable decision drift.

## Use Cases

- **RE-01: Inventory Existing Processes Before Digitalization**
  - **Stage Target**: v1
  - **Actor**: Human (business analyst); Agent (documenter)
  - **Situation**: Process execution is distributed across memory, paper, and ad-hoc communication.
  - **Need**: Capture process steps, participants, handoffs, inputs/outputs, and bottlenecks.
  - **Success**: A reusable process map exists for prioritizing digitalization by impact.
  - **Failure**: Digitalization starts from intuition, creating disconnected silos.

- **RE-06: Support Long-Term Investment Decision Tracking**
  - **Stage Target**: v1
  - **Actor**: Human (investor/owner); Agent (analyst)
  - **Situation**: Multi-year investment outcomes cannot be reliably compared to original assumptions.
  - **Need**: Preserve assumptions, options, rationale, confidence, and outcome links for retrospectives.
  - **Success**: Later reviews can compare projected vs actual outcomes and extract patterns.
  - **Failure**: Decisions are remembered as conclusions without retrievable reasoning.

## Acceptance Criteria

1. Representative RE-domain knowledge artifacts (one RE-01 process inventory and one RE-06 decision evidence artifact) can be represented using existing nowu workflow artifacts without RE-specific framework code.
2. Relationship structures needed by RE-01 and RE-06 (handoffs, assumption→outcome links, dependency chains) are representable conceptually; structural limits are documented with follow-on ownership.
3. One RE-06 investment decision is mapped through the existing S1-S9 decision pattern (structural equivalence check against NF-02 style decision flow).
4. No bespoke RE management subsystem is created; all outputs remain in current nowu artifact/workflow structures.
5. GAP-001..007 are classified using cross-domain evidence (AP from intake-007 and RE from intake-008) as systemic or domain-specific using the W28 rule.

## Affected Modules

- **core**: Contract fit validation for RE decision/process representations.
- **flow**: Domain-agnostic workflow traversal validation (RE as second non-software domain run).

## Appetite

8 hours. This is a comparative evidence cycle (RE vs AP), not capability implementation.
If scope exceeds appetite, cut breadth before depth.

## Context

W27 completed AP-domain bootstrap evidence and documented GAP-001..007. W28 runs the second
domain validation on RE-01 and RE-06 to test whether those gaps are AP-specific or systemic.
The core validation goal from ROADMAP-004 is cross-domain classification quality, not feature
delivery in `src/`.

## Open Questions

1. Can RE-01 process inventory structure be represented with current artifact conventions without introducing domain-specific contract types?
2. Can RE-06 long-horizon decision evidence be represented with current `DecisionRecord` shape plus supplementary artifact sections?
3. Which W27 gaps recur with equivalent structural impact in RE evidence (systemic) versus remain AP-only (domain-specific)?
4. Is the existing MemoryService surface sufficient for machine-queryable RE evidence, or does RE confirm the same K3 pressure seen in AP?

---

## S1 Validation Annotations (D-SESS-01 Guardrail Applied)

### Problem-level framing check

This intake is intentionally problem-scoped only: no ADR/module-solution proposals are used in
framing language. Architecture choices are deferred to S2/S3.

### UC Confirmation

RE-01 and RE-06 are confirmed ACTIVE in `docs/USE_CASES.md` with `stage_target: v1`.

### Scope Boundaries

**In scope:** RE process/decision representation evidence + gap classification.

**Out of scope:** Any Python implementation in `src/` or `tests/`, protocol expansion, runtime feature rollout.

---

```yaml
from_step: S1
to_step: S2
agent: nowu-constraints
status: READY_FOR_ARCH
```
