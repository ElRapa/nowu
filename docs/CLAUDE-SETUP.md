# nowu + Claude — Workflow, C4 Model, and Setup Guide

## TL;DR for humans

- Always start a new Claude Code session by pasting `BOOTSTRAP.md`, then let Claude read the listed docs.
- Pick a **mode** (Full cycle, Architecture-only, Implement loop) from the skills and follow it step-by-step.
- Each workflow step has its own **agent** and C4 **zoom level**; only load the files that level needs.
- All important decisions live in `docs/DECISIONS.md`; all in-progress work lives under `state/`.

---

nowu is an AI-powered project management framework. You and Claude follow the
same 9-step workflow to design, implement, and review changes.

This document explains:
- How the 9-step workflow and C4 model work together for humans.
- How the Claude setup (agents, skills, rules, hooks, state files) is structured.
- How to copy this setup to another repository.

---

## 1. Core ideas

- 9-step workflow (S1–S9) from problem → architecture → tasks → code → capture.
- C4 levels (L1–L4) define the zoom for each step (system → modules → components → code).
- Dedicated agent per step (`nowu-intake` … `nowu-curator`).
- Skills orchestrate common modes (full cycle, architecture-only, implement loop).
- Strict context scoping: each step only loads the minimum context for its C4 level.
- Decisions are recorded as D-NNN in `docs/DECISIONS.md` and must be followed.

---

## 2. C4 model and step mapping

`docs/GLOBAL-MODEL.md` defines how C4 levels map to nowu artifacts and steps.

### 2.1 C4 levels

| Level | Name              | Question                           | nowu main artifact             |
|-------|-------------------|-------------------------------------|--------------------------------|
| L1    | System Context    | What does the system do? Who uses it? | `ARCHITECTURE.md` §1        |
| L2    | Container/Modules | How do modules interact?            | `ARCHITECTURE.md` §4.1      |
| L3    | Component         | What files/classes exist?           | `core/contracts/*.py`, file tree |
| L4    | Code              | How does it work internally?        | Source code and tests        |

### 2.2 Which step uses which level

- S1–S2: L1 (system boundary, actors, high-level constraints).
- S3–S4: L2 (module interactions, options, decisions).
- S5 and S8: L3 (files/classes, task shaping, code review vs intent).
- S6–S7: L4 (code and tests with AST/import boundary checks).

The context-scoping guides reinforce this: **never load code during architecture analysis**, and **never load full architecture docs during implementation**.

---

## 3. Files you should know

### 3.1 High-level docs

| File / Dir                  | Purpose                                     |
|----------------------------|---------------------------------------------|
| `CLAUDE.md`                | Rules and commands for Claude.              |
| `BOOTSTRAP.md`             | Prompt you paste at the start of a session. |
| `BOOTSTRAP_lean.md`        | Minimal variant of the bootstrap prompt.    |
| `docs/WORKFLOW.md`         | High-level description of S1–S9.            |
| `docs/WORKFLOW-DETAILED.md`| Full spec: inputs/outputs per step.         |
| `docs/GLOBAL-MODEL.md`     | C4 model and Code Property Graph overview.  |
| `docs/ARCHITECTURE.md`     | Module map and architecture rules.          |
| `docs/DECISIONS.md`        | Accepted architecture decisions (D-NNN).    |
| `docs/V1_PLAN.md`          | Current v1 steps and tasks.                 |
| `docs/PROGRESS.md`         | Execution status of v1 steps.               |

### 3.2 State and session tracking

| File / Dir                | Purpose                                      |
|---------------------------|----------------------------------------------|
| `state/SESSION-STATE.md`  | Current step + focus bookmark.               |
| `state/intake/`           | Intake briefs (S1 outputs).                  |
| `state/arch/`             | Constraints, options, decisions (S2–S4).     |
| `state/tasks/`            | Task specs (S5 outputs).                     |
| `state/changes/`          | Implementation notes / diffs (S6).           |
| `state/vbr/`              | VBR reports (S7).                            |
| `state/reviews/`          | Review reports (S8).                         |
| `state/capture/`          | Capture records (S9).                        |

---

## 4. Claude configuration: agents, skills, rules, settings

### 4.1 Agents (.claude/nowu-*.md)

The `.claude` directory holds agent definitions for each workflow step.

| Step | Agent name        | Role                        | Config file               |
|------|-------------------|-----------------------------|---------------------------|
| S1   | `nowu-intake`     | Intake briefs               | `.claude/nowu-intake.md`  |
| S2   | `nowu-constraints`| Constraints analysis        | `.claude/nowu-constraints.md` |
| S3   | `nowu-options`    | Design options              | `.claude/nowu-options.md` |
| S4   | `nowu-decider`    | Record decision D-NNN       | `.claude/nowu-decider.md` |
| S5   | `nowu-shaper`     | Shape tasks                 | `.claude/nowu-shaper.md`  |
| S6+7 | `nowu-implementer`| Implement + VBR             | `.claude/nowu-implementer.md` |
| S8   | `nowu-reviewer`   | Review (verify + validate)  | `.claude/nowu-reviewer.md`|
| S9   | `nowu-curator`    | Capture + progress update   | `.claude/nowu-curator.md` |

Each agent file defines its C4 scope, what it may load, what it must never load, and which artifact it produces.

### 4.2 Skills (orchestration docs)

Skills describe how to string agents together for common modes.

| Skill doc                        | Mode and purpose                             |
|----------------------------------|----------------------------------------------|
| `skills/full-cycle/SKILL.md`         | Mode A — S1→S9 full development cycle.   |
| `skills/architecture-only/SKILL.md`  | Mode D — S1→S4→S9 architecture-only.     |
| `skills/implement-loop/SKILL.md`     | Mode B — S5→[S6–S7]×n→S8–S9.             |

Skills encode entry conditions, which agents to invoke, validation gates, retries, and stopping conditions.

### 4.3 Rules (architecture / workflow / code / testing)

The `.claude/rules` directory captures hard rules for Claude to follow.

| Rule file              | Purpose                                            |
|------------------------|----------------------------------------------------|
| `.claude/rules/architecture.md` | Enforces layer and module boundaries and step scoping. |
| `.claude/rules/workflow.md`     | 9-step cycle, statuses, approval tiers, modes. |
| `.claude/rules/code-style.md`   | Python style, naming, imports, docstrings. |
| `.claude/rules/testing.md`      | TDD order, test naming, structure, coverage gate. |

These rules compress the important parts of long docs (like `flow_vs_sdlc-*`) into short, enforceable checks.

### 4.4 settings.json (hooks and external tools)

`settings.json` wires hooks and external MCP servers into Claude Code.

- **PreToolUse hooks**:
  - `Bash(git commit*)`: before any `git commit`, run VBR: `pytest`, `mypy --strict`, `ruff`.
  - `Write(*)`: before writing a file, enforce scope via `state/tasks/.active-scope`; block writes outside allowed files.

- **MCP servers**:
  - `know`: `know-mcp --data-dir ~/.know`, future external memory / CPG engine.

This makes VBR and scope enforcement automatic instead of relying on agents remembering.

---

## 5. How to run a normal feature with Claude

### 5.1 Start the session

1. Open a new Claude Code session.
2. Paste `BOOTSTRAP.md` (or `BOOTSTRAP_lean.md` for a smaller load).
3. Let Claude read the listed files and answer the bootstrap questions.

### 5.2 Choose a skill mode

Use the skill docs to choose the right mode:

- New feature from scratch → **Mode A** (Full Cycle: S1→S9).  
- Architecture/design spike only → **Mode D** (S1→S4→S9).  
- Tasks already shaped → **Mode B** (S5→[S6–S7]×n→S8–S9).  
- Single bugfix or small change → **Mode C** (Single Step S6–S9, per workflow rules).

Ask Claude to follow the chosen skill step-by-step and invoke the right agents.

### 5.3 S1–S4: problem and architecture (L1–L2)

- S1 `nowu-intake` (L1): intake brief in `state/intake/…`.
- S2 `nowu-constraints` (L1–L2): constraints sheet from ARCHITECTURE + DECISIONS + contracts.
- S3 `nowu-options` (L2): options sheet with module-level designs and tradeoffs.
- S4 `nowu-decider` (L2): D-NNN decision in `docs/DECISIONS.md` + handoff; validation gate.

### 5.4 S5: shaping (L3)

- S5 `nowu-shaper` (L3): task specs with `in_scope_files`, acceptance criteria, and `validation_trace`; human approval required.

### 5.5 S6–S7: implementation + VBR (L4)

- S6/S7 `nowu-implementer` (L4):
  - Load only `task-NNN` + `in_scope_files` + tests + `pyproject.toml`.
  - Follow TDD rules from `.claude/rules/testing.md`.
  - VBR enforced automatically via `settings.json` on commit and via the skill loop.

### 5.6 S8–S9: review + capture (L3–L1)

- S8 `nowu-reviewer` (L3–L4): fresh context review with architecture rules, diff, task spec, and VBR evidence.
- S9 `nowu-curator` (L1–L2): update PROGRESS, DECISIONS if needed, write capture record, suggest commit message.

---

## 6. Approval tiers

From `.claude/rules/workflow.md`:

- **Tier 1** — auto:
  - Tests, docs, refactors following ADRs, within shaped scope.
- **Tier 2** — batch:
  - Feature implementation, design changes, new dependencies.
- **Tier 3** — block:
  - Merge to main, breaking change, new ADR, delete, architecture boundary violations.

When unsure, treat a change as Tier 2.

---

## 7. How to copy this setup to another repo

To replicate the nowu + Claude + C4 workflow elsewhere:

1. Copy and adapt docs:
   - `CLAUDE.md`, `BOOTSTRAP*.md`
   - `docs/WORKFLOW.md`, `docs/WORKFLOW-DETAILED.md`
   - `docs/GLOBAL-MODEL.md` (update system description and module mapping)
   - `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`
   - `docs/V1_PLAN.md`, `docs/PROGRESS.md`

2. Copy agents, skills, settings:
   - `.claude/nowu-*.md`, adjust module names and paths.
   - Skill `SKILL.md` files for modes A/B/D.
   - `.claude/rules/*.md` and `settings.json`, adjusting commands and paths.

3. Create the state skeleton:
   - `state/intake/`, `state/arch/`, `state/tasks/`,
     `state/changes/`, `state/vbr/`, `state/reviews/`, `state/capture/`,
     plus a `state/SESSION-STATE.md` template.

4. Start using it:
   - Start a Claude Code session, paste `BOOTSTRAP.md`.
   - Choose a mode and follow the skills and rules.

