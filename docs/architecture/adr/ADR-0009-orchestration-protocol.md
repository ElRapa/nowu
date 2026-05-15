---
id: ADR-0009
title: Orchestration Protocol & Agent Handoff Contract
date: 2026-05-07
status: PROPOSED
epistemic_grade: INFORMED_ESTIMATE
epistemic_grade_previous: HYPOTHESIS
epistemic_grade_promoted_at: 2026-05-15
epistemic_grade_promoted_by: W9 ADR promotion pass
superseded_by: ~
source_synthesis: SYNTHESIS-001
source_themes: [T3, T4, T6]
source_ucs: [NF-02, NF-03, NF-04, NF-05, NF-09, NF-13, NF-14, XP-06]
depends_on: [ADR-0007, ADR-0008, ADR-0010]
---

# ADR-0009: Orchestration Protocol & Agent Handoff Contract

## Status

PROPOSED (INFORMED_ESTIMATE grade, promoted 2026-05-15) — Derived from SYNTHESIS-001 Theme
T3 (Workflow Orchestration). Depends on ADR-0007, ADR-0008, and ADR-0010. Promoted from
HYPOTHESIS after three complete S1-S9 intake cycles (intake-001, intake-007, intake-008)
confirmed the orchestration protocol's state machine, artifact-based handoffs, approval gates,
and domain-agnostic pipeline traversal. See "## Supporting Evidence" section.

## Context

SYNTHESIS-001 identifies T3 (Workflow Orchestration) as a critical theme: the coordination
of specialized agents through structured handoffs, quality gates, approval tiers, and
failure recovery.

Existing decisions:
- D-005: Dedicated agent per workflow step (8 agents for S1-S9)
- D-009: Role-driven workflow with VBR and approval tiers
- D-019: Router-based architecture — agents are altitude-agnostic executors, router knows altitude
- WORKFLOW.md: Full S1-S9 step reference with context scoping rules

What these decisions do NOT define:
- **Typed handoff interface** — what is the structured payload between S5 output and S6 input?
- **Failure recovery protocol** — what happens when S6 fails VBR 3 times?
- **Handoff validation** — how does the orchestrator verify a step's output before advancing?
- **Orchestration state machine** — what are the legal transitions?

The `flow` module is designated as the orchestrator (D-003) but has no implementation
beyond contracts. This ADR defines the protocol that `flow` will implement.

## Decision

### Handoff Contract

Every workflow step produces a **handoff artifact** — a structured file that serves as
both the output of the current step and the input to the next. The handoff artifact is
the ONLY interface between steps. Agents never communicate directly.

**Handoff artifact structure (common envelope):**

```yaml
---
artifact_type: HANDOFF
source_step: S3          # Step that produced this
target_step: S4          # Step that consumes this
intake_id: intake-001    # Links to source intake
status: READY            # READY | INVALID | BLOCKED
epistemic_grade: HYPOTHESIS
created_at: 2026-05-07T14:30:00Z
validation_result:       # Filled by orchestrator before advancing
  valid: true
  checks_passed: [schema, required_fields, grade_present]
  checks_failed: []
---

# [Step-specific content below]
```

The body content varies by step (constraints sheet, options sheet, decision record, etc.)
but the YAML envelope is constant and machine-parseable.

### Step-Specific Handoff Payloads

| Transition | Source Artifact | Required Fields in Handoff | Target Reads |
|-----------|----------------|---------------------------|-------------|
| S1 → S2 | `intake-NNN.md` (updated) | `intake_id`, `problem_statement`, `uc_refs`, `grade` | Intake brief |
| S2 → S3 | `intake-NNN-constraints.md` | `constraints[]`, `risks[]`, `decisions_referenced[]`, `grade` | Constraints sheet |
| S3 → S4 | `intake-NNN-options.md` | `options[]` (≥2, each with pros/cons/effort), `grade` | Options sheet |
| S4 → S5 | `intake-NNN-decision.md` | `chosen_option`, `rationale`, `decision_id`, `grade` | Decision record |
| S5 → S6 | `task-NNN.md` | `in_scope_files[]`, `acceptance_criteria[]`, `validation_trace`, `grade` | Task spec |
| S6/S7 → S8 | `changeset` + `vbr-report` | `files_changed[]`, `tests_added[]`, `vbr_result`, `grade` | Implementation + VBR |
| S8 → S9 | `review-task-NNN.md` | `verdict` (APPROVED/REJECTED), `checklists`, `grade` | Review report |
| S9 → exit | `capture-task-NNN.md` | `next_cycle_trigger`, `learnings[]`, `decisions_made[]` | Capture record |

### Orchestrator State Machine

The orchestrator (`flow` module) manages transitions between steps:

```
                    ┌─────────┐
   intake arrives   │         │
  ────────────────►│   S1    │
                    │ INTAKE  │
                    └────┬────┘
                         │ READY
                    ┌────▼────┐
                    │   S2    │
                    │CONSTRAIN│
                    └────┬────┘
                         │ READY
                    ┌────▼────┐
                    │   S3    │
                    │ OPTIONS │
                    └────┬────┘
                         │ READY
                    ┌────▼────┐
                    │   S4    │◄──── 🛑 HUMAN GATE
                    │DECISION │
                    └────┬────┘
                         │ READY
                    ┌────▼────┐
                    │   S5    │◄──── 🛑 HUMAN GATE
                    │ SHAPING │
                    └────┬────┘
                         │ READY
                    ┌────▼────┐
                    │  S6/S7  │◄──── VBR loop (max 3 retries)
                    │IMPLEMENT│
                    └────┬────┘
                         │ VBR PASS
                    ┌────▼────┐
                    │   S8    │
                    │ REVIEW  │──── REJECTED ──► back to S5 or S6
                    └────┬────┘
                         │ APPROVED
                    ┌────▼────┐
                    │   S9    │
                    │CAPTURE  │──── next_cycle_trigger ──► exit/route
                    └─────────┘
```

**Legal transitions:**

| From | To | Condition |
|------|-----|-----------|
| S1 | S2 | Intake brief has required fields |
| S2 | S3 | Constraints sheet complete |
| S3 | S4 | Options sheet has ≥2 options |
| S4 | S5 | Human approved decision |
| S5 | S6 | Human approved task spec; `in_scope_files` set |
| S6/S7 | S8 | VBR passes (tests + types + lint) |
| S6/S7 | S6 | VBR fails (retry, max 3) |
| S6/S7 | BLOCKED | VBR fails 3x → escalate to human |
| S8 | S9 | Review APPROVED |
| S8 | S5 | Review REJECTED (reshape) |
| S8 | S6 | Review CHANGES_REQUESTED (re-implement) |
| S9 | exit | `next_cycle_trigger` determines route |

**Illegal transitions (enforced by orchestrator):**
- Skipping steps (S1 → S5)
- Backward without rejection (S5 → S3 without S8 REJECTED)
- Proceeding past a BLOCKED state without human resolution

### Approval Tier Integration

The orchestrator classifies each transition by approval tier (from D-009):

| Tier | Actions | Gate Behavior |
|------|---------|---------------|
| **Tier 1** (auto) | S1→S2, S2→S3, S6 VBR pass, S9 capture | Orchestrator advances automatically |
| **Tier 2** (batch) | S3→S4, S5→S6 (if not first-time), S8 review | Queued for human; non-blocking |
| **Tier 3** (STOP) | New ADR, breaking change, scope expansion, merge to main | Blocks pipeline until human resolves |

The orchestrator maintains a **pending approvals queue** for Tier 2 items. The human
reviews batched items at natural checkpoints (start of session, after S4, before merge).

### Failure Recovery Protocol

When a step fails:

```
Failure at step SN:
  1. Log failure with error context to state/errors/error-{intake_id}-SN-{timestamp}.md
  2. Increment retry counter for SN
  3. If retries < max_retries (3):
     → Re-run SN from its input artifact
     → Write checkpoint (per ADR-0007)
  4. If retries >= max_retries:
     → Set status to BLOCKED
     → Write human-facing summary: "SN failed 3 times. Error: [summary]. 
        Human action needed: [specific ask]."
     → Checkpoint with blockers = ["SN: {error_summary}"]
     → Wait for human resolution
  5. If failure is architectural (violates ADR, boundary, or constraint):
     → Immediately BLOCKED (no retries for structural violations)
     → Route to S2 for re-constraint analysis, not retry
```

**VBR-specific failure:**
- VBR failure (tests/types/lint) at S7 loops back to S6 for fix
- Max 3 VBR loops per task
- After 3 failures: BLOCKED → human decides whether to reshape (back to S5) or
  accept with known issues (Tier 3 approval required)

### Context Scoping Enforcement

The orchestrator enforces context scoping (from WORKFLOW.md) at each transition:

```
Before invoking agent for step SN:
  1. Load the handoff artifact from S(N-1) — this is the agent's primary input
  2. Load ONLY the files listed in WORKFLOW.md's "Load" column for SN
  3. Explicitly EXCLUDE files listed in "Never Load" column
  4. Pass to agent: handoff artifact + scoped context files
  5. After agent completes: validate output against handoff schema
```

This prevents context bleed (implementation details leaking into architecture decisions,
or architecture re-litigation during implementation).

### Traceability (T6 Integration)

Every handoff artifact carries a `validation_trace` that builds progressively:

```
S1: validation_trace = {uc_refs: ["NF-01", "NF-10"]}
S2: validation_trace = {uc_refs: ["NF-01", "NF-10"], constraints: ["C-001", "C-002"]}
S5: validation_trace = {uc_refs: [...], constraints: [...], 
     acceptance_criteria: ["AC-001", "AC-002"]}
S8: validation_trace = {uc_refs: [...], constraints: [...],
     acceptance_criteria: [...], tests: ["test_resume_after_crash"]}
```

At S8, the reviewer validates the trace is complete: every AC links to a UC,
every test links to an AC. Broken chains are review failures.

## Rationale

1. **Artifacts as interface:** Agents communicating through structured files (not
   conversations or function calls) aligns with P2 (artifacts are the interface) and
   makes handoffs inspectable, version-controllable, and recoverable.

2. **Explicit state machine:** Without defined legal transitions, the workflow devolves
   into ad-hoc step selection. The state machine prevents skipping gates and ensures
   every transition is intentional.

3. **Failure recovery is planned, not improvised:** Defining retry limits and escalation
   before the first failure prevents shotgun debugging and ensures humans are engaged
   at the right moment — not too early (agent can fix it) and not too late (3 failures
   means structural issue).

4. **Context scoping is orchestrator-enforced:** Relying on agents to self-scope is
   fragile. The orchestrator controls what each agent sees, making context bleed
   architecturally impossible rather than just discouraged.

## Consequences

**Positive:**
- Typed handoffs make integration testable (validate payload schema at each transition)
- Failure recovery is deterministic: retry → escalate → block
- Traceability chain is built progressively, not reconstructed retroactively
- Context scoping prevents the most common agent failure mode (re-litigation)

**Negative:**
- Handoff envelope adds metadata overhead to every artifact
- State machine requires implementation in `flow` module (currently empty)
- Strict transitions may feel rigid for exploratory work (mitigated by Mode D:
  Architecture Only, and pre-workflow P0-P4 which is intentionally flexible)

**Neutral:**
- Existing agent definitions (`.claude/agents/nowu-*.md`) don't need changes — they
  already follow the scoping rules. The orchestrator formalizes what's currently informal.
- The `RoleOrchestrator` Protocol in `core/contracts/session.py` provides the API surface
  but will need extension to support the full state machine.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Artifact-based handoff with state machine (recommended) | Typed, inspectable, recoverable, enforceable | Implementation effort; rigid transitions | **Selected** — T3 theme + D-005/D-009 require it |
| Event-driven pipeline (publish/subscribe) | Loose coupling, async-capable | Event ordering complexity, harder to debug, overkill for single-user | Over-engineered for v1-core; events can be added at v2 |
| Conversation-based handoff (agent-to-agent chat) | Natural language flexibility | Not inspectable, not recoverable, not version-controllable | Violates P2 (artifacts as interface) |
| Free-form file passing (no envelope) | Less boilerplate | No validation, no traceability, handoff failures are silent | Fails NF-09 (traceability) and NF-04 (VBR) |

## Related

- synthesis: SYNTHESIS-001 (Theme T3)
- arch_vision: docs/architecture/ARCHITECTURE-VISION.md (Principle P4)
- decisions: D-005 (dedicated agent per step), D-009 (role-driven workflow with VBR),
  D-019 (router-based agent architecture)
- adrs: ADR-0001 (module boundaries), ADR-0006 (soul↔flow via filesystem),
  ADR-0007 (checkpoints at step boundaries), ADR-0008 (atom references in artifacts),
  ADR-0010 (grades at gates)
- depends_on: ADR-0007, ADR-0008, ADR-0010
- depended_on_by: ADR-0012 (traceability standard built on validation_trace)

## Supporting Evidence

Grade promoted from HYPOTHESIS to INFORMED_ESTIMATE on 2026-05-15 (W9 ADR promotion pass).
Promotion rule: D-017 requires ≥2 S1-S9 intakes confirming the hypothesis. Three complete
S1-S9 intake cycles now confirm ADR-0009's core decisions.

### Evidence from intake-001 (W4 — NF-01, First End-to-End Cycle)

**Files:** `state/intake/intake-001.md`, `state/capture/capture-intake-001.md`

- intake-001 was the first complete S1-S9 run, validating the orchestration protocol
  end-to-end. `capture-intake-001.md`: "This cycle also validates the S1-S9 workflow
  end-to-end for the first time."
- The artifact-based handoff pattern (each step produces an artifact consumed by the next)
  was confirmed: 5 tasks completed in sequence (task-001 through task-005), with artifact
  handoffs at each step boundary.
- Human gates (S4, S5) functioned as designed — D-024 decision was made and recorded at
  the S4 gate, then consumed by S5 for task shaping.
- VBR loop (S6/S7) was confirmed: "43 tests, 98.54% coverage; mypy --strict clean; ruff
  clean" — the Generate-Test-Repair pattern in ADR-0009's S6/S7 section was exercised.
- S8 review: "Review APPROVED with no architectural surprises" — approval tier gate confirmed.
- S9 capture: `next_cycle_trigger: CONTINUE` — legal exit transition confirmed.

**Confirmation:** All S1-S9 transitions confirmed as legal. No orchestration protocol
violations. Artifact-based handoffs, VBR loop, approval gates all functioned as specified.

### Evidence from intake-007 (W27 — AP Domain Bootstrap, Domain-Agnostic T5 Test)

**Files:** `state/intake/intake-007.md`, `state/capture/capture-intake-007.md`,
`state/arch/intake-007-gap-register.md`

- intake-007 ran a full S1-S9 cycle on an AP-domain intake. `intake-007-gap-register.md`
  Part 3: "Flow can process AP-domain intake artifacts without AP-specific workflow logic
  changes (T5 validated at workflow level)."
- This directly validates ADR-0009's context scoping enforcement: the orchestrator prevented
  domain content from bleeding into architecture decisions — the flow module processed AP
  intake without domain-specific branching.
- Three tasks (task-011, task-012, task-013) completed, with artifact handoffs at each step.
- `capture-intake-007.md`: "S8 verdict is APPROVED" — approval gate confirmed for AP domain.

**Confirmation:** T5 (domain agnosticism) validated. Orchestration protocol works across
domain boundaries without modification.

### Evidence from intake-008 (W28 — RE Domain Bootstrap, Cross-Domain Confirmation)

**Files:** `state/intake/intake-008.md`, `state/capture/capture-intake-008.md`

- intake-008 ran a second cross-domain S1-S9 cycle (RE domain). `capture-intake-008.md`:
  "W28 completed with APPROVED review and no architecture pivot."
- Two tasks (task-014, task-015) completed, confirming artifact-based handoffs and approval
  gates for a third distinct domain.
- `capture-intake-008.md` Why It Matters: "converts W27's single-domain gap list into a
  comparative domain signal" — the orchestration protocol's domain-agnostic design is
  confirmed by independent AP and RE evidence.

**Confirmation:** Three distinct domain sessions (NF, AP, RE) confirm orchestration
protocol stability. No illegal transitions, no protocol violations, no context bleed.

### Promotion Justification

D-017 threshold: HYPOTHESIS → INFORMED_ESTIMATE after ≥2 S1-S9 intakes confirming the
hypothesis. Three intakes confirm:
- intake-001: First full cycle confirms state machine, VBR loop, approval gates.
- intake-007: Confirms domain-agnostic traversal (T5).
- intake-008: Cross-domain confirmation with equivalent structural outcome.

Note: ADR-0009's full programmatic orchestration (formal state machine in `flow` module,
pending approvals queue) has not yet been implemented — current confirmation is of the
process semantics (the WHAT), not the programmatic implementation (the HOW). EVIDENCE_BASED
requires ≥5 intakes including implementation evidence (D-017).
