---
artifact_type: TASK_SPEC
id: task-011
title: W27 fit-assessment and AP-06 artifact-shape proof
created: 2026-05-15
status: DONE
decision_id: D-027
intake_id: intake-007
story_id: story-v1core-004-s003
estimated_hours: 2
primary_module: none
depends_on: []
use_case_ids:
  - AP-06
work_item: W27
altitude: DELIVERY
phase: EVALUATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - None
---

# Task Spec: task-011 — W27 fit-assessment + AP-06 proof

## In-Scope Files

- state/arch/intake-007-fit-assessment.md
- state/arch/intake-007-ap06-proof.md

## Out of Scope

- src/nowu/**
- tests/**
- AP-01/AP-02 artifacts and gap register content (owned by other W27 tasks)

## Acceptance Criteria

- id: AC-1
  description: A fit-assessment artifact maps AP evidence needs to existing contracts/schemas (TaskSpec, DecisionRecord, SessionCheckpoint, MemoryService) with explicit coverage and limitation notes.
  test_function_name: test_fit_assessment_maps_ap_needs_to_existing_contracts

- id: AC-2
  description: The AP-06 proof artifact demonstrates one business decision through S1-S4 decision-shape artifact mirrors using existing structures only, with options, chosen path, rejected alternatives, rationale, and context conditions. Includes explicit NF-02 structural equivalence crosswalk.
  test_function_name: test_ap06_proof_contains_s1_s4_decision_shape_walkthrough

- id: AC-3
  description: Both artifacts include required frontmatter fields (artifact_type, status, created_at) and explicit trace links to D-027 and intake-007.
  test_function_name: test_w27_fit_and_ap06_artifacts_have_required_frontmatter_and_trace_links

## Test Strategy (TDD order)

1. Write `test_fit_assessment_maps_ap_needs_to_existing_contracts` validation checklist and confirm initial RED against empty/nonexistent artifact.
2. Write `test_ap06_proof_contains_s1_s9_artifact_shape_walkthrough` validation checklist and confirm RED.
3. Implement minimal artifact content to satisfy AC-1 and AC-2; run both checks to GREEN.
4. Run `test_w27_fit_and_ap06_artifacts_have_required_frontmatter_and_trace_links` and confirm GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: AP-06
    story_ac: AC-001
    criteria: [AC-1, AC-2]
    rationale: "AC-1 constrains AP decision evidence to existing schemas; AC-2 proves AP-06 decision traceability using S1-S9 artifact shapes."
  - use_case: AP-06
    story_ac: AC-003
    criteria: [AC-2, AC-3]
    rationale: "AC-2 preserves full decision reasoning in artifact form; AC-3 enforces durable trace metadata for later retrieval."
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: DONE
```
