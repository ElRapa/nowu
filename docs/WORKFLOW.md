# nowu Workflow — Reference Specification

> Read this file at session start. For full narrative and rationale, see `WORKFLOW-DETAILED.md`.

---

## Overview

The nowu workflow is a 9-step cycle: zoom in from system context to code, then zoom back out
to capture decisions. Every step has one agent, one context scope, and one output artifact.
The cycle enforces both **verification** (built it right) and **validation** (built the right thing).

**Entry point:** `state/intake/intake-NNN.md` with `status: READY_FOR_S1`.
Intakes are produced by the **Pre-Workflow** (P0–P4). See `PRE-WORKFLOW.md`.

**Exit point:** S9 sets `next_cycle_trigger` which routes back into pre-workflow or closes the cycle.

---

## Step Reference

| Step | Name | Agent | C4 Level | Output Artifact | Gate |
|------|------|-------|----------|-----------------|------|
| S0 | Session Bookmark | human / main | — | `state/SESSION-STATE.md` | — |
| S1 | Intake | nowu-intake | Above C4 | `state/intake/intake-NNN.md` (updated) | — |
| S2 | Constraints | nowu-constraints | L1–L2 | `state/arch/intake-NNN-constraints.md` | — |
| S3 | Options | nowu-options | L2 | `state/arch/intake-NNN-options.md` | — |
| S4 | Decision | nowu-decider | L2 | `docs/DECISIONS.md` + `state/arch/intake-NNN-decision.md` | 🛑 VALIDATION |
| S5 | Shaping | nowu-shaper | L3 | `state/tasks/task-NNN.md` | 🛑 VALIDATION |
| S6+S7 | Implement + VBR | nowu-implementer | L4 | `state/changes/` + `state/vbr/` | Tier 1 auto |
| S8 | Review | nowu-reviewer | L3–L4 | `state/reviews/review-task-NNN.md` | Tier 1/2 |
| S9 | Capture | nowu-curator | L1–L2 | `state/capture/capture-task-NNN.md` | Tier 1 auto |

---

## Workflow Modes

| Mode | Steps | When to use |
|------|-------|-------------|
| A — Full Cycle | S1 → S9 | New feature or story from intake |
| B — Implement Loop | S5 → [S6–S7]×n → S8–S9 | Tasks already shaped; execute in sequence |
| C — Single Step | S6 → S9 | Bug fix, small refactor, docs |
| D — Architecture Only | S1 → S4 → S9 | Design spike, no implementation yet |

---

## Context Scoping Rules

**The single most important rule:** each agent loads only context from its C4 level.
Loading architecture docs during implementation causes re-litigation.
Loading code during architecture analysis causes anchoring bias.

| Agent | Load | Never Load |
|-------|------|------------|
| nowu-intake | `intake-NNN.md`, `vision.md`, `V1_PLAN.md`, `USE_CASES.md`, `PROGRESS.md` | `src/`, `tests/`, `ARCHITECTURE.md`, `DECISIONS.md` |
| nowu-constraints | `intake-NNN.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `contracts/`, `arch-pass-NNN.md` (if exists) | `src/` internals, `tests/` |
| nowu-options | `constraints sheet`, `contracts/`, module `__init__.py` surfaces | Full `ARCHITECTURE.md`, `src/` internals |
| nowu-decider | `options sheet`, `DECISIONS.md` | `src/`, `tests/`, `contracts/` |
| nowu-shaper | `decision handoff`, file tree, `contracts/`, test structure, `PROGRESS.md` | `ARCHITECTURE.md`, `DECISIONS.md`, vision |
| nowu-implementer | `task-NNN.md` + `in_scope_files` ONLY, `pyproject.toml` | Everything else |
| nowu-reviewer | `vbr report`, `changeset`, `task-NNN.md`, `git diff`, `.claude/rules/architecture.md`, `story-NNN.md` (via task.story_id) | Full arch docs, upstream artifacts |
| nowu-curator | `review report`, `DECISIONS.md`, `PROGRESS.md`, `intake-NNN.md`, `git log` | `src/`, `tests/` |

---

## Verification vs. Validation

**Verification** (S7, S8 checklist A): "Did we build it right?"
- Tests pass, types clean, linter clean, architecture respected, scope not exceeded.

**Validation** (S4 gate, S5 gate, S8 checklist B): "Did we build the right thing?"
- Implementation traces: `code → test → AC → use_case → intake → vision`
- No link in this chain may be broken.
- The `validation_trace` field in every Task Spec is the machine-readable form of this chain.

---

## S9 Feedback Loop

S9 `next_cycle_trigger` routes back into the pre-workflow:

| Value | Meaning | Re-entry point |
|-------|---------|----------------|
| `CONTINUE` | Next story from same epic | P2.1 (problem-NNN already approved) |
| `ARCH_PIVOT` | Architecture assumptions proved wrong | P3.1 (re-run constraint check) |
| `PRODUCT_PIVOT` | Problem definition changed | P1.1 (new discovery run) |
| `COMPLETE` | Epic / product goal met | Pre-workflow closed for this cycle |

---

## Handoff Status Flow

```
DRAFT → READY_FOR_ARCH → READY_FOR_OPTIONS → READY_FOR_DECISION
      → READY_FOR_SHAPING → READY_FOR_IMPL → READY_FOR_VBR
      → READY_FOR_VBR → READY_FOR_REVIEW → DONE
                                  ↕
                         CHANGES_REQUESTED (loops back to S5 or S6)
                                  ↕
                            BLOCKED (human needed)
```

---

## Health Checks (run anytime)

Run at session start if >7 days since last run, or when something feels misaligned.

| Command | Agent | Output |
|---------|-------|--------|
| `/health-check vision` | `health-vision` | `state/health/vision-YYYY-MM-DD.md` |
| `/health-check architecture` | `health-architecture` | `state/health/arch-YYYY-MM-DD.md` |
| `/health-check goals` | `health-goals` | `state/health/goals-YYYY-MM-DD.md` |
| `/health-check all` | All three | All three reports |

Status: **GREEN** (no issues) / **YELLOW** (minor drift) / **RED** (blocking — address before next cycle).
