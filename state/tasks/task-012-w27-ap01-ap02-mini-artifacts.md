---
artifact_type: TASK_SPEC
id: task-012
title: W27 AP-01/AP-02 minimal representation artifacts
created: 2026-05-15
status: DONE
decision_id: D-027
intake_id: intake-007
story_id: story-v1core-004-s002
estimated_hours: 2
primary_module: none
depends_on: [task-011]
use_case_ids:
  - AP-01
  - AP-02
work_item: W27
altitude: DELIVERY
phase: EVALUATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - None
---

# Task Spec: task-012 — W27 AP-01/AP-02 mini artifacts

## In-Scope Files

- state/arch/intake-007-ap01-mini-graph.md
- state/arch/intake-007-ap02-mini-version-chain.md

## Out of Scope

- src/nowu/**
- tests/**
- Gap register and claim-boundary synthesis (owned by task-013)

## Acceptance Criteria

- id: AC-1
  description: AP-01 artifact contains a mini dependency graph of 2-3 linked regulatory requirements with explicit dependency references and current status markers.
  test_function_name: test_ap01_mini_graph_has_two_to_three_linked_requirements_with_dependencies

- id: AC-2
  description: AP-02 artifact contains a mini version chain with exactly two formulation versions, each documenting change, rationale, outcome, and accept/abandon decision.
  test_function_name: test_ap02_mini_version_chain_has_two_versions_with_rationale_and_outcome

- id: AC-3
  description: Both artifacts explicitly state representational limits under current schemas and reference corresponding future work items where capability expansion is required.
  test_function_name: test_ap01_ap02_artifacts_include_limitations_and_follow_on_work_refs

## Test Strategy (TDD order)

1. Write `test_ap01_mini_graph_has_two_to_three_linked_requirements_with_dependencies` and confirm RED before artifact creation.
2. Write `test_ap02_mini_version_chain_has_two_versions_with_rationale_and_outcome` and confirm RED.
3. Create minimal AP-01/AP-02 artifacts to satisfy structure and trace requirements; confirm GREEN on AC-1/AC-2 checks.
4. Add limitation/follow-on section and run `test_ap01_ap02_artifacts_include_limitations_and_follow_on_work_refs` to GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: AP-01
    story_ac: AC-001
    criteria: [AC-1, AC-3]
    rationale: "AC-1 provides dependency-ordered regulatory representation; AC-3 records known expressiveness limits and ownership for missing capability."
  - use_case: AP-02
    story_ac: AC-002
    criteria: [AC-2, AC-3]
    rationale: "AC-2 proves versioned formulation knowledge with rationale/outcome; AC-3 links unresolved representation gaps to planned work."
  - use_case: AP-02
    story_ac: AC-003
    criteria: [AC-2]
    rationale: "AC-2 requires explicit predecessor linkage between two versions, demonstrating chain navigation rather than flat history."
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: DONE
```
