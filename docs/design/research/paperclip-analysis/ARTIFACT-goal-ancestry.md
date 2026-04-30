# Goal Ancestry Chain — nowu Implementation

**Inspired by**: Paperclip's Goal Alignment model (Mission → Objective → Role → Task)

## Purpose

Every artifact in nowu traces back to the vision. This document defines the canonical chain and explains how each level maps to nowu artifacts.

---

## The Chain

```
Vision (docs/vision.md)
  └─ Use Case (docs/USECASES.md · UC-NNN)
       └─ Epic (state/epics/epic-NNN.md)
            └─ Story (state/stories/story-NNN.md)
                 └─ Intake (state/intake/intake-NNN.md · READY_FOR_S1)
                      └─ Task (state/tasks/task-NNN.md)
                           └─ Code / Test (src/ + tests/)
```

## Traceability Rule

No artifact may exist without a parent in the chain above. The `validation_trace` field in every task spec is the machine-readable enforcement of this rule.

```yaml
validation_trace:
  - ac: AC-001
    uc: UC-007
    persona: "Developer working across multiple projects"
    success_criterion: "Session resumes within 30s with full context restored"
```

## How to Check Goal Ancestry

Run `health-check goals` to verify:
1. All active stories trace to a UC-NNN
2. All UC-NNNs trace to a vision success horizon
3. No task exists without a parent story

This mirrors Paperclip's "Goal Ancestry Chain" — every task carries the full lineage so agents know not just *what* to do but *why*.

---

## Paperclip → nowu Mapping

| Paperclip concept | nowu equivalent |
|---|---|
| Company mission | `docs/vision.md` → One-Liner + Success Horizons |
| Objective | `state/epics/epic-NNN.md` |
| Role / Agent | S1–S9 agent + `state/tasks/task-NNN.md` role field |
| Task / Issue | `state/tasks/task-NNN.md` |
| Goal ancestry chain | `validation_trace` in task-spec |

---

## Usage

Feed this file to any agent at session start alongside `docs/vision.md` when you need it to stay goal-aware. It replaces the need to re-explain "why" at every step.
