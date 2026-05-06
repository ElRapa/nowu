# nowu 5×10 Implementation Guide

Version: 1.1  
Date: 2026-05-05  
Status: CANONICAL

See MODEL-REFERENCE.md for full model specification.  
See VERIFICATION-GUIDE.md for verification framework.

## Purpose

This guide is the single implementation playbook for rolling out the nowu 5×10 artifact system.
It consolidates package scope, sequence, outputs, and storage design into one actionable path.
Use it as the source of implementation order and deliverables.

This document intentionally focuses on execution.
It does not restate full conceptual model definitions and does not include verification checklists.

## 1. Overview

Implementation is split into three sequential packages:

1. Metadata Foundation
2. Phase Agents + Skillsets
3. Runtime Circuit Breaker

Execution order is fixed.
Do not start Package 2 before Package 1 deliverables are accepted.
Do not start Package 3 before Package 2 definitions are in place.

Total effort:

- AI implementation: 4-6 hours
- Human review and approval: 90-120 minutes total

Package 1 is standalone and immediately useful.
After Package 1, the repository already has structured storage, normalized metadata, and searchable indexes.

## 2. What Gets Implemented

### Package 1: Metadata Foundation (this delivery)

Inputs:

- Approximately 55 existing artifacts
- Includes ADRs, use cases, goals, and problem/lesson artifacts

Outputs:

1. Directory structure at `state/artifacts/{altitude}/{type}/`
2. Index files:
   - `state/index/artifact-index.json`
   - `state/index/cross-references.json`
   - `state/index/status-index.json`
3. Existing artifacts updated with YAML frontmatter
4. `ALTITUDES.md` v2.0 documenting the 5×10 implementation model
5. 10 agent definition files in `agents/phase-operators/`
6. `SYNTHESIS-001.md` first cross-cutting analysis
7. `WORKFLOW-STANDARDS.md` marked as binding standards

Estimated effort:

- AI: 2-3 hours
- Human review: 30 minutes

### Package 2: Phase Agents + Skillsets

Scope:

- Build 10 phase-agent definitions with altitude-specific skills
- Add prompt templates per phase
- Ensure each agent declares `altitude_applicability`
- Apply multi-altitude rules for shared phases

Estimated effort:

- AI: 2-3 hours
- Human review: 30 minutes

### Package 3: Runtime Circuit Breaker

Scope:

- Implement `core/altitude_guard.py` middleware
- Add runtime health monitoring hooks
- Add violation detection and structured logging
- Enforce circuit-break behavior on repeated violations

Estimated effort:

- AI: 1-2 hours
- Human review: 30 minutes

## 3. Artifact Storage Design

The storage model has two artifact classes with distinct lifecycle rules.

### Knowledge artifacts

Durable and cross-altitude artifacts:

- `GOAL`
- `USE_CASE`
- `ADR`
- `SYNTHESIS`
- `LESSON`
- `SIGNAL`
- `CONSTRAINT`

Rules:

- Must use globally unique IDs
- IDs are never reused
- Stored under `state/artifacts/{altitude}/{type}/`
- Indexed in `artifact-index.json`

### Workflow phase artifacts

Ephemeral, session-scoped working artifacts:

- `OPTIONS`
- `ANALYSIS`
- `EVALUATION`
- `IMPLEMENTATION`
- `REVIEW`

Rules:

- Named by phase and session
- Session-local and short-lived by design
- Not indexed in global artifact indexes

### Canonical storage structure

```text
state/artifacts/
├── strategic/goals/
├── product/use-cases/
├── architecture/
│   ├── adrs/
│   ├── synthesis/
│   └── evaluation/
├── delivery/shapes/
└── execution/
    ├── implementations/
    ├── reviews/
    └── lessons/

state/index/
├── artifact-index.json
├── cross-references.json
└── status-index.json
```

### Naming rules

- Knowledge artifacts: `{TYPE}-{ID}.md` (globally unique)
- Workflow phase artifacts: `{PHASE}-{ID}-{altitude}.md` (session-scoped)

## 4. Metadata Schema

### Knowledge artifact frontmatter

```yaml
---
artifact_class: knowledge
artifact_type: GOAL | USE_CASE | ADR | SYNTHESIS | LESSON
id: GOAL-001
title: "[descriptive title]"
origin_altitude: STRATEGIC
origin_phase: DECISION
consumer_altitudes: [PRODUCT, ARCHITECTURE, DELIVERY, EXECUTION]
epistemic_grade: HYPOTHESIS
grade_justification: "[one sentence WHY]"
status: ACTIVE
created_at: YYYY-MM-DD
last_edited_at: YYYY-MM-DD
related_artifacts: []
promoted_from: null
promotes_to: null
relationships: []
---
```

### Workflow phase artifact frontmatter

```yaml
---
artifact_class: workflow_phase
altitude: ARCHITECTURE
phase: OPTIONS
session_id: session-2026-05-05-alpha
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "[reasoning]"
---
```

### Field rules

- `altitude` and `phase` are required on all newly created artifacts
- `promoted_from` is set at creation when the parent artifact is known
- `promotes_to` is set later by curator action during LEARN
- `relationships` starts as `[]` and is populated by knowledge-graph layer in v1.1+
- `status` allowed values: `ACTIVE`, `SUPERSEDED`, `DEPRECATED`

## 5. Altitude Inference Rules (Package 1)

Use these rules when adding frontmatter to existing artifacts.

| Artifact Pattern | Altitude | Phase |
|---|---|---|
| ADR-NNNN-*.md | ARCHITECTURE | DECISION |
| GOAL-NNN.md | STRATEGIC | DECISION |
| USE-CASE-*.md | PRODUCT | DECISION |
| PROBLEM-NNN.md | Analyze content: user=PRODUCT, arch=ARCHITECTURE, market=STRATEGIC |
| LESSON-NNN.md | EXECUTION | LEARN |
| Future S1 artifacts | DELIVERY | IDEA |
| Future S2 artifacts | ARCHITECTURE | ANALYSIS |
| Future S3 artifacts | ARCHITECTURE | OPTIONS |
| Future S4 artifacts | ARCHITECTURE | DECISION |
| Future S5 artifacts | DELIVERY | EVALUATION |
| Future S6-S8 artifacts | EXECUTION | IMPLEMENTATION/VERIFICATION |
| Future S9 artifacts | EXECUTION | LEARN |

Implementation note:

- For `PROBLEM-NNN.md`, include explicit AI flagging when confidence is low.
- Human reviewer confirms or adjusts ambiguous assignments.

## 6. Package 1 Tasks (Detailed)

Execute Package 1 in this exact order.

### Task 1: Create directory structure

- Create `state/artifacts/` altitude/type directories
- Create `state/index/`
- Ensure paths match canonical structure

### Task 2: Create index files

- Initialize empty JSON files:
  - `artifact-index.json`
  - `cross-references.json`
  - `status-index.json`
- Use valid JSON syntax from first commit

### Task 3: Add frontmatter to existing artifacts

- Apply schema from Section 4
- Infer altitude/phase using Section 5 rules
- Preserve original body content
- Flag ambiguous artifacts for human review

### Task 4: Update indexes for each knowledge artifact

- Add canonical entries to `artifact-index.json`
- Populate initial graph links in `cross-references.json`
- Set current lifecycle value in `status-index.json`

### Task 5: Create ALTITUDES.md v2.0

Must include:

- A zigzag execution diagram
- A phase-to-multi-altitude applicability table
- Implementation-facing guidance for artifact placement

### Task 6: Create 10 agent definitions

- Location: `agents/phase-operators/`
- Coverage: IDEA through LEARN (10 phases)
- Include multi-altitude support where phase spans contexts
- Include `altitude_applicability` in each definition

### Task 7: Create SYNTHESIS-001.md

- Analyze approved use cases
- Identify recurring cross-cutting themes
- Capture implications for architecture and delivery planning

### Task 8: Produce implementation report

Output file:

- `PACKAGE-1-IMPLEMENTATION-REPORT.md`

Report must summarize:

- Completed artifacts and counts
- Ambiguities flagged for review
- Index population status
- Deviations (if any) with rationale

## 7. Human Review Points

Run this review immediately after Package 1 completion.

1. Randomly inspect 5-10 artifacts for altitude/phase inference quality.
2. Resolve all AI-flagged ambiguous artifacts.
3. Review `SYNTHESIS-001.md` for real cross-cutting themes.
4. Review 10 phase-agent definitions for altitude-specific skill alignment.
5. Approve Package 1 or return with revisions.

Expected time: 30 minutes.

## 8. Success Criteria

Package 1 is complete only when all conditions are true:

- Directory structure exists and matches specification.
- All three index files exist and are valid JSON.
- All ~55 existing artifacts contain YAML frontmatter.
- Frontmatter parses as valid YAML in all updated files.
- S1 artifacts are classified at DELIVERY, not EXECUTION.
- S2-S4 artifacts are classified at ARCHITECTURE, not EXECUTION.
- IMPLEMENTATION agent is usable at ARCHITECTURE, DELIVERY, and EXECUTION.
- Epistemic grading permits HYPOTHESIS at STRATEGIC altitude.
- `ALTITUDES.md` v2.0 exists.
- 10 phase-agent definition files exist.
- `SYNTHESIS-001.md` exists.
- Human review has been completed.

## 9. Migration Notes

- Migration strategy is forward-only.
- New artifacts get full metadata fields at creation time.
- Existing artifacts are updated when touched; no global backfill campaign.
- `promoted_from` and `promotes_to` are curator-managed during LEARN.
- `relationships` remains empty until knowledge graph layer implementation (v1.1+).

## 10. After Implementation

After Package 1 acceptance, execute next actions in order:

1. Update ADR-0001 through ADR-0006 to reference altitude-aware implementation.
2. Implement Package 2 (agents + skillsets).
3. Implement Package 3 (runtime circuit breaker).
4. Enable Level 0-2 verification.
5. Run the first altitude-aware workflow end-to-end.

## Implementation Sequence Summary

Use this condensed sequence for execution tracking:

1. Build storage skeleton.
2. Initialize empty indexes.
3. Add frontmatter to all legacy artifacts.
4. Populate knowledge indexes.
5. Author ALTITUDES.md v2.0.
6. Author 10 phase-agent definitions.
7. Author SYNTHESIS-001.md.
8. Produce Package 1 report.
9. Run human review.
10. Move to Package 2, then Package 3.

This is the canonical implementation guide for v1.1 rollout.
