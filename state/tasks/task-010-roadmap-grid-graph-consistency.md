---
artifact_type: TASK_SPEC
id: task-010
title: Roadmap grid↔graph consistency fitness test
created: 2026-05-14
status: READY_FOR_IMPL
intake_id: none
story_id: none
estimated_hours: 3
primary_module: none
depends_on: []
use_case_ids:
  - NF-09
work_item: W-log
altitude: ARCHITECTURE
phase: VERIFICATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - docs/ROADMAP-003.md
---

# Task Spec: task-010 — Roadmap Grid↔Graph Consistency Fitness Test

## Purpose

The ROADMAP-003 work grid (Section 2) and dependency graph (Section 4) independently
track work item statuses and dependencies. They drift apart within a single session
(RP-004, 6 inconsistencies found in W8+W29 session). This task adds an automated
fitness test that detects drift.

## Design Decision

**The dependency graph YAML (Section 4) is canonical for status.** The work grid
table (Section 2) must be derivable from and consistent with the dep graph.

## Acceptance Criteria

1. A pytest test in `tests/architecture/test_roadmap_consistency.py` that:
   a. Parses the ROADMAP-003.md work grid table (Section 2) to extract
      `{work_item_id: status}` pairs.
   b. Parses the dependency graph YAML block (Section 4) to extract
      `{work_item_id: status}` pairs.
   c. Asserts that every work item appearing in both sections has matching
      status (accounting for format differences: "✅ DONE" in grid = "✅ complete" in YAML).
   d. Asserts that every `depends_on` reference in the dep graph points to
      a work item that exists in the work grid.

2. The test passes against the current ROADMAP-003.md (no pre-existing violations).

3. The test uses the same pattern as `test_epistemic_enforcement.py` (parse files,
   collect violations, assert none).

## In-Scope Files

- `tests/architecture/test_roadmap_consistency.py` (new)
- `docs/ROADMAP-003.md` (read-only for test; fix any pre-existing violations first)

## Out of Scope

- Auto-generating the work grid from the dep graph (future optimization)
- Validating dep graph dependency ordering (topological sort)
- Checking Section 7 against Section 4 (could be added as follow-up)

## Validation Trace

- NF-09 (traceability) → work items must be consistently tracked
- RP-004 (recurring pattern) → Section 7 + dashboard staleness
- Session learnings 2026-05-14 → Insight 1 (two sources of truth that drift)
