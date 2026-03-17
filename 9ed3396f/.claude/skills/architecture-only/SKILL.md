# Skill: Architecture Only (Mode D — S1→S4→S9)

Use when: exploring a new problem, doing a design spike, or making an
architectural decision WITHOUT implementing anything yet.
Also use when appetite is 'spike' in the intake.

## Steps

### 1. Intake (S1)
Invoke: `nowu-intake`
Input: the problem or question to explore
Output: `state/intake/<date>-<slug>.md` with appetite = spike

### 2. Constraints Analysis (S2)
Invoke: `nowu-constraints`
Produces: constraints sheet highlighting what is unknown vs. fixed.

### 3. Options Design (S3)
Invoke: `nowu-options`
For spikes: produce options even if effort is uncertain.
Flag open questions that need prototyping to resolve.

### 4. Decision (S4) 🛑 HUMAN APPROVAL REQUIRED
Invoke: `nowu-decider`
STOP: present VALIDATION GATE S4 — wait for human approval.
Options after approval:
  a) Record as ACCEPTED → proceed to shaping in a future session
  b) Record as DEFERRED with rationale → capture and close
  c) Record as REJECTED with rationale → capture and close

### 5. Capture (S9)
Invoke: `nowu-curator`
Even for deferred/rejected decisions: record the reasoning in DECISIONS.md.
Knowledge of dead ends is valuable. Capture it.
