---
artifact_type: INTAKE_BRIEF
intake_id: intake-001
status: READY_FOR_ARCH
created_at: 2026-05-10
s1_validated_at: 2026-05-11T00:00:00Z
workflow_mode: A
use_case_ids: [NF-01, NF-02, NF-09, PK-03, XP-01]
affected_modules: [core, flow, know]
appetite: small
appetite_hours: 8h (to be confirmed)
priority: high
source: docs/ROADMAP-003.md (W4)
---

# Intake Brief: Resume Work After Context Loss

## Problem Statement

When an AI session ends abruptly, critical context is lost. The user must manually reconstruct what was happening, losing momentum. This problem affects both agents and humans, leading to inefficiency and frustration.

## Use Cases

- **NF-01: Resume Work After Context Loss**
  - **Stage Target**: v1-core
  - **Actor**: Any AI agent and Multi-Project Human
  - **Situation**: A new session starts after an abrupt end. Context is missing.
  - **Need**: Reconstruct enough context to continue productive work seamlessly.
  - **Success**: Agents propose the correct next action; humans resume without re-orientation.
  - **Failure**: Agents restart or contradict prior work; humans lose trust.

## Acceptance Criteria

1. Agents must read persisted state, identify the last verified checkpoint, and propose the correct next action.
2. Humans must receive a clear signal of where things stand to confidently resume direction.
3. No hallucination of progress or contradictions with prior decisions.

## Affected Modules

- **core**: Session contracts, `SessionStore` protocol.
- **flow**: Session orchestration, pipeline state.

## Appetite

Small. This is scoped as the first S1-S9 cycle to validate the workflow, not to build the full continuity engine.

## Context

This is the first S1-S9 intake per W4, selected because NF-01 is a v1-core UC in the critical path. It addresses the most fundamental user pain point (context loss) and exercises `core` and `flow` modules.

---

## S1 Validation Annotations

### UC Confirmation

NF-01 is confirmed ACTIVE in docs/USE_CASES.md with stage_target: v1-core. The canonical UC definition maps to Themes T1 (Continuity) and T2 (Knowledge Persistence). The intake's problem statement and acceptance criteria are consistent with the canonical NF-01 need and success conditions.

Note from USE_CASES.md: the Step 02 (In Progress) mapping lists NF-01, NF-02, NF-09, PK-03, and XP-01 together for this work item. The intake declares only NF-01. This is not a validation failure — the intake is intentionally scoped narrowly for workflow validation purposes. The unrepresented UCs (NF-02, NF-09, PK-03, XP-01) are in scope for later intakes in the same W4 work item. S2 should note this and confirm the narrow scope is deliberate.

### PROGRESS.md

docs/PROGRESS.md does not exist. No duplicate work detected. Note surfaced as open question below.

### Field Completeness Check

| Field | Present | Valid |
|---|---|---|
| problem_statement | yes | yes — user-centric, no solution language |
| use_case_ids | yes | yes — NF-01 confirmed ACTIVE, v1-core |
| acceptance_criteria | yes | yes — 3 criteria listed |
| affected_modules | yes | yes — core, flow (first-guess quality, appropriate for S1) |
| appetite | yes | yes — "small" maps to 8h or less per workflow rules |
| context | yes | yes — W4 traceability confirmed |

All required fields are present and non-empty. Intake passes field completeness gate.

### Implicit Assumptions

1. **SessionStore exists or will be created in core.** The intake names `SessionStore` as a protocol in core. This is an assumption about what core exposes. S2 must confirm whether this protocol exists, is planned, or must be created.

2. **"Persisted state" is readable by agents at session start.** The AC requires agents to read persisted state. The intake does not specify what artifact or format constitutes persisted state. The NF-01 open question in USE_CASES.md references `state/SESSION-STATE.md` and WORKFLOW.md §S0 as the resolved approach. S2 should confirm whether `state/SESSION-STATE.md` is an existing contract or a deliverable of this intake.

3. **"Last verified checkpoint" has a defined meaning.** AC-1 uses this phrase. It is not defined in the intake. S2 must confirm whether a checkpoint schema exists in any ADR or contract, or whether defining it is within the scope of this cycle.

4. **"Clear signal" for humans (AC-2) is assumed to be a file artifact.** The vision's guiding principle is "artifacts are the API." If the human-facing signal is a display or CLI output rather than a file, this is outside the current scope and should be deferred to bridge/soul modules.

5. **Scope boundary: this intake validates the workflow pipeline, not the full continuity engine.** The appetite note explicitly states this. S2 must not let ADR-0007 (Session Continuity Protocol) scope bleed into this cycle.

### Gaps and Clarifications for S2

1. **Does `state/SESSION-STATE.md` exist as a contract artifact today?** If not, creating or specifying its schema may be in scope for this intake. If it exists, S2 should load it and treat it as a binding input.

2. **Does `SessionStore` protocol exist in core contracts?** S2 should check `contracts/` to confirm presence or absence.

3. **Appetite calibration: "small" is not yet mapped to hours.** Per workflow rules, appetite options are 2h, 4h, 8h, or spike. The intake says "small." S2 should bind this to a specific hour budget (likely 8h for first end-to-end cycle).

4. **ADR-0007 is PROPOSED (hypothesis), not ACCEPTED.** ROADMAP-003 shows ADR-0007 (Session Continuity Protocol) as a hypothesis ADR. S2 must assess whether this intake's implementation is constrained by it or whether this intake is the evidence run that validates or supersedes it.

### Module Dependency Map

```
intake-001 touches:

  core  <-- primary
    - SessionStore protocol (read/write session checkpoint)
    - contracts baseline (F1: DONE per roadmap)

  flow  <-- primary
    - Session orchestration logic
    - Pipeline state tracking

  bridge  <-- OUT OF SCOPE
    - CLI surface or remote surface for human-facing signal
    - Not addressable until F6 (v1 dependency)

  soul  <-- OUT OF SCOPE
    - Human-facing orientation layer
    - NF-10 territory, not NF-01 core

  know  <-- WATCH
    - Knowledge persistence (K3/K4) is v1, not v1-core
    - If any AC requires writing to a knowledge store,
      it is out of scope for this intake
```

### Story Boundaries

**IN SCOPE:**

- Define or confirm the schema of the checkpoint artifact (what survives a session crash).
- Implement or confirm `SessionStore` protocol in core.
- Implement session state read at pipeline start in flow.
- Agent proposes correct next action from checkpoint state (AC-1).
- Structured artifact produced that communicates current state to the human (AC-2).
- No hallucination guard: agent reads from artifact, not from its own inference (AC-3).

**OUT OF SCOPE (explicitly):**

- Full continuity engine (K3, K4 — v1 work items).
- `state/SESSION-STATE.md` becoming a full knowledge atom (ADR-0008 territory — v1).
- Human-facing orientation display or CLI rendering (bridge/soul — F6 dependency).
- Cross-session learning or mistake retention (NF-06 — W4 step 06 territory).
- NF-02 (ADR enforcement), NF-09 (traceability), PK-03 (Today view), XP-01 (cross-project) — all co-listed in Step 02 but not in scope for this intake cycle.
- Epistemic grading of checkpoint artifacts (NF-15 — W29, v1 territory).

**DEFERRED (known future work):**

- Promote ADR-0007 from PROPOSED to ACCEPTED (W9, v1 — requires this intake as evidence).
- Session runtime and write-ahead log (F4 — v1, depends on K3).

### Open Questions

1. Does `state/SESSION-STATE.md` exist today? (blockers for S2)
2. Is `SessionStore` in `contracts/` today, or is it created by this intake?
3. Appetite binding: confirm 8h or adjust.
4. Is ADR-0007 a constraint on this intake or a hypothesis being tested by it?
5. docs/PROGRESS.md does not exist — S9 should create it as part of this cycle's capture, or S2 should flag it as a deliverable gap.
