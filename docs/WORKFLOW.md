# nowu Workflow v5 — Unified Specification

> Last updated: 2026-03-17 | Replaces: v4

## Overview

The nowu workflow is a 9-step cycle that zooms in from system context to code,
then zooms back out to capture decisions. Each step has a dedicated agent, a
fixed context scope, and a defined output artifact. The workflow enforces both
**verification** (built it right) and **validation** (built the right thing).

The workflow runs in four modes:
- **A: Full Cycle** — S1→S9 (new feature)
- **B: Implement Loop** — S5→[S6-S7]×n→S8-S9 (execute shaped tasks)
- **C: Single Step** — S6-S9 (bug fix, small change)
- **D: Architecture Only** — S1→S4→S9 (design spike)

For a detailed, narrative explanation of each step and the Octahedron model,
see `docs/WORKFLOW-DETAILED.md`.

---

## S0: Session Bookmark (optional)

Before entering S1–S9, the human or main agent may update
`state/SESSION-STATE.md` with:

- current step (S1–S9)
- current `intake_id` / `decision_id` / `task_id`
- brief summary of focus
- next checkpoint

This is a convenience bookmark for session continuity, not a source
of truth. The canonical state always lives in the S1–S9 artifacts.

---

## Step Reference

| Step | Name        | Agent           | C4 Level | Perspective        | Output Artifact            | Gate            |
|------|-------------|-----------------|----------|--------------------|----------------------------|-----------------|
| S1   | Intake      | nowu-intake     | L1       | System context     | Intake Brief               | —               |
| S2   | Constraints | nowu-constraints| L1-2     | System→Module      | Constraints Sheet          | —               |
| S3   | Options     | nowu-options    | L2       | Module interactions| Options Sheet              | —               |
| S4   | Decision    | nowu-decider    | L2       | Module, choosing   | Decision Record (D-NNN)    | 🛑 VALIDATION   |
| S5   | Shaping     | nowu-shaper     | L3       | Component (files)  | Task Spec(s)               | 🛑 VALIDATION   |
| S6+S7| Implement+VBR| nowu-implementer| L4      | Code               | Change Set + VBR Report    | Tier 1 auto     |
| S8   | Review      | nowu-reviewer   | L3-4     | Code←→Component    | Review Report              | Tier 1/2        |
| S9   | Capture     | nowu-curator    | L1-2     | System (zooming out)| Capture Record            | Tier 1 auto     |

---

## Context Scoping Rules

The single most important rule: **each agent loads only context from its C4 level**.
Loading architecture docs during implementation causes re-litigation.
Loading code during architecture analysis causes anchoring bias.

| Agent           | Load                                          | Never Load                         |
|-----------------|-----------------------------------------------|------------------------------------|
| nowu-intake     | V1_PLAN, USE_CASES (by ID), PROGRESS          | src/, tests/, ARCHITECTURE, DECISIONS |
| nowu-constraints| intake, ARCHITECTURE, DECISIONS, contracts/   | src/ internals, tests              |
| nowu-options    | constraints, intake, contracts/, module __init__.py | full ARCHITECTURE, src/ internals |
| nowu-decider    | options, DECISIONS                            | src/, tests, contracts             |
| nowu-shaper     | decision handoff, file tree, contracts/, test structure | ARCHITECTURE, DECISIONS, vision   |
| nowu-implementer| task spec, in_scope_files ONLY, pyproject.toml| everything else                    |
| nowu-reviewer   | VBR, changeset, task spec, git diff, rules    | full arch docs, upstream artifacts |
| nowu-curator    | review, DECISIONS, PROGRESS, git log          | src/, tests/                       |

At a good stopping point in S6–S7 (e.g. after a major test passes), you may
update `state/SESSION-STATE.md` so the next session can resume quickly.

After S9 (Capture), you may clear or reset `state/SESSION-STATE.md` to
indicate that the current cycle is complete.

---

## Verification vs. Validation

**Verification** (S7, S8 checklist A): “Did we build it right?”
- Tests pass, types clean, architecture respected, scope not exceeded.

**Validation** (S4 gate, S5 gate, S8 checklist B): “Did we build the right thing?”
- Implementation traces back through: code → test → AC → use_case → intake → vision.
- No link in this chain may be broken.

The `validation_trace` field in every Task Spec is the machine-readable form of this chain.

---

## Agent Design Rationale

Each step gets its own agent (not a shared “architect” agent) because:

1. Context scope differs — the options designer needs contracts; the decider does not.
2. Cognitive mode differs — constraints analysis is divergent; decision is convergent.
3. Decision methods differ — S3 uses QA-style scoring; S4 uses a weighted matrix.
4. Fresh context windows at S8 prevent accumulated bias from corrupting the review.

Agents are concise (each ≤60 lines). Skills hold the step-by-step orchestration.
The main Claude session handles human communication and Tier 2/3 decisions.

---

## Handoff Status Flow

```text
DRAFT → READY_FOR_ARCH → READY_FOR_OPTIONS → READY_FOR_DECISION
     → READY_FOR_SHAPING → READY_FOR_IMPL → READY_FOR_VBR
     → READY_FOR_REVIEW → READY_FOR_CAPTURE → DONE
                                    ↕
                           CHANGES_REQUESTED (loops back)
                                    ↕
                              BLOCKED (human needed)
```