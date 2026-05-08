# nowu Bootstrap — DELIVERY/EXECUTION Altitude

**Use this for:** S1-S9 workflow execution, task shaping, implementation loops, S6-S7 code, S8 review.

## Read in this exact order

### Workflow Model (always)
1. `docs/WORKFLOW.md`                      — S1-S9 reference table
2. `docs/model/MODEL-REFERENCE.md`         — 5x10 altitude-phase model
3. `docs/model/WORKFLOW-STANDARDS.md`      — binding workflow rules

### Architecture Context (alignment only)
4. `docs/architecture/containers.md`       — module map (C4 L2)
5. `docs/DECISIONS.md`                     — all D-NNN decisions (binding)

### Execution Context (altitude-specific)
6. `docs/WORKFLOW-DETAILED.md`             — full narrative spec (read relevant S1-S9 sections)
7. `state/tasks/` — run `ls`               — see what tasks exist and their statuses
8. `state/tasks/.active-scope`             — current scope (if filled)

### Tools & Rules
9. `CLAUDE.md`                             — commands, approval tiers
10. `.claude/rules/workflow.md`            — statuses, tiers, iteration modes
11. `.claude/rules/architecture.md`        — layer and module boundaries
12. `.claude/rules/testing.md`             — TDD and coverage rules
13. `.claude/rules/code-style.md`          — style, naming, imports

## Context Scoping (CRITICAL)
Each workflow step loads ONLY its C4-level context:
- **S1-S5 (shaping):** Load architecture docs, decisions, constraints. NEVER load src/ or tests/.
- **S6-S7 (implementation):** Load ONLY task-NNN.md + in_scope_files. Nothing else.
- **S8 (review):** Load ONLY VBR report + changeset + task spec + diff. No full architecture docs.

Violating context scoping causes anchoring bias or re-litigation.

## Confirm Understanding
1. What is the S1-S9 workflow and which step are you in now?
2. What are the context scoping rules for your current step?
3. What are the approval tiers and which tier does your current work fall into?
4. What quality gates must pass before S8 review? (pytest, mypy, ruff)

## Then wait for user approval before touching files.
