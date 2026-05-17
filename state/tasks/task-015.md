---
artifact_type: TASK_SPEC
id: task-015
title: W28 cross-domain GAP classification matrix
created: 2026-05-15
status: DONE
decision_id: D-028
intake_id: intake-008
story_id: raw-intake
estimated_hours: 2
primary_module: none
depends_on: [task-014]
use_case_ids:
  - RE-01
  - RE-06
work_item: W28
altitude: DELIVERY
phase: EVALUATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - None
---

# Task Spec: task-015 — W28 GAP-001..007 classification

## In-Scope Files

- state/arch/w28-gap-comparison.md

## Out of Scope

- src/nowu/**
- tests/**
- S8/S9 review and capture artifacts

## Acceptance Criteria

- id: AC-1
  description: The comparison artifact evaluates all seven gaps (GAP-001..007) against AP (intake-007) and RE (intake-008) evidence with explicit references.
  test_function_name: test_w28_gap_comparison_covers_all_seven_gaps_with_dual_domain_evidence

- id: AC-2
  description: Each gap is labeled exactly one of {systemic, domain-specific} using the binding rule (systemic requires equivalent structural impact in >=2 domains).
  test_function_name: test_w28_gap_labels_follow_systemic_rule_without_ambiguity

- id: AC-3
  description: The artifact includes prioritization implications for K3/K9/K13/W19/W20/ADR-0010 maintenance based on classification outcomes.
  test_function_name: test_w28_gap_comparison_includes_priority_implications

## Test Strategy (TDD order)

1. Build a seven-gap checklist with required evidence columns and classification field.
2. Populate AP and RE evidence rows and confirm AC-1.
3. Apply rule-based labels and confirm AC-2.
4. Add roadmap-priority implications and confirm AC-3.

## Validation Trace

```yaml
validation_trace:
  - use_case: RE-01
    story_ac: AC-001
    criteria: [AC-1, AC-2]
    rationale: "RE-01 evidence is required to test whether process-structure gaps recur cross-domain."
  - use_case: RE-06
    story_ac: AC-001
    criteria: [AC-1, AC-2, AC-3]
    rationale: "RE-06 evidence stress-tests decision-trace gaps and drives follow-on priority implications."
```

---

```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: DONE
```
