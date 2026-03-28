---
name: architecture-only
version: 2.1
mode: D
steps: S1-S4-S9
---

# Skill: Architecture Only (Mode D — S1→S4→S9)

Use when: you want to run an architecture/design spike without implementation.
Outputs are decisions and updated architecture docs, not code.

Entry condition:
- `state/intake/intake-NNN.md` with `status: READY_FOR_S1`

Stop points:
- S4 decision requires human approval

## Orchestration Steps

### 1. Intake (S1)

Invoke: `nowu-intake`  
Input: `state/intake/intake-NNN.md`  
Output: same file, `status: READY_FOR_ARCH`

Proceed when:
- `status = READY_FOR_ARCH`

### 2. Constraints (S2)

Invoke: `nowu-constraints`  
Input: `state/intake/intake-NNN.md`  
Output: `state/arch/intake-NNN-constraints.md`

Proceed when:
- `constraints.status = READY_FOR_OPTIONS`

### 3. Options (S3)

Invoke: `nowu-options`  
Input: `state/arch/intake-NNN-constraints.md`  
Output: `state/arch/intake-NNN-options.md`

Proceed when:
- `options.status = READY_FOR_DECISION`

### 4. Decision (S4) 🛑 HUMAN APPROVAL REQUIRED

Invoke: `nowu-decider`  
Input: `state/arch/intake-NNN-options.md`

Agent drafts:

- `state/arch/intake-NNN-decision.md`
- D-NNN block for `docs/DECISIONS.md`

STOP for human:

- Review and adjust decision.
- Append D-NNN to `docs/DECISIONS.md`.
- Set `decision.status = ACCEPTED`.

### 5. Capture (S9)

Invoke: `nowu-curator`  
Input:
- `state/arch/intake-NNN-decision.md`
- `docs/DECISIONS.md`
- `docs/PROGRESS.md`

Output:
- `state/capture/capture-intake-NNN.md`
- Updated `docs/PROGRESS.md`

Done when:
- `capture.status = DONE`

Next:

- If this decision enables implementation work, switch to Mode A or B with this intake.
