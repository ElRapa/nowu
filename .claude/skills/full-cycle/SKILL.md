# Skill: Full Development Cycle (Mode A — S1→S9)

Use when: a new feature idea arrives and needs the complete workflow.
Stop points: S4 (validation gate) and S5 (scope approval) require human approval.

## Orchestration Steps

### 1. Intake (S1)
Invoke: `nowu-intake`
Input: the idea/feature description from the human
Output: `state/intake/<date>-<slug>.md`
Proceed when: status = READY_FOR_ARCH

### 2. Constraints Analysis (S2)
Invoke: `nowu-constraints`
Input: the intake file path
Output: `state/arch/<intake-id>-constraints.md`
Proceed when: status = READY_FOR_OPTIONS

### 3. Options Design (S3)
Invoke: `nowu-options`
Input: the constraints file path
Output: `state/arch/<intake-id>-options.md`
Proceed when: status = READY_FOR_DECISION

### 4. Decision (S4) 🛑 HUMAN APPROVAL REQUIRED
Invoke: `nowu-decider`
Input: the options file path
STOP: agent outputs VALIDATION GATE S4 block — wait for human approval
After approval: D-NNN appended to DECISIONS.md
Output: `state/arch/<intake-id>-decision.md`
Proceed when: human approves AND status = READY_FOR_SHAPING

### 5. Shaping (S5) 🛑 HUMAN APPROVAL REQUIRED
Invoke: `nowu-shaper`
Input: the decision handoff file path
STOP: agent outputs VALIDATION GATE S5 block — wait for human approval
After approval: task specs written, .active-scope set
Output: `state/tasks/task-<NNN>.md` (1-5 files)
Proceed when: human approves AND status = READY_FOR_IMPL

### 6-7. Implementation + VBR Loop (S6+S7)
For each task spec (in dependency order):
  Invoke: `nowu-implementer`
  Input: task spec path
  Loop until: VBR Report status = READY_FOR_REVIEW (fix and retry on CHANGES_REQUESTED)
  Output: `state/changes/<task-id>.md`, `state/vbr/<task-id>.md`

### 8. Review (S8)
Invoke: `nowu-reviewer`
Input: VBR report path + task spec path
If verdict = CHANGES_REQUESTED: return to S6 for that task
Output: `state/reviews/<task-id>.md`
Proceed when: verdict = APPROVED

### 9. Capture (S9)
Invoke: `nowu-curator`
Input: review report path
Output: `state/capture/<date>-<task-id>.md`, updated PROGRESS.md, commit message
Done when: status = DONE | READY_FOR_SHAPING | READY_FOR_ARCH
