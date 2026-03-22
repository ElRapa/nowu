# nowu Workflow v4 — Final Unified Specification
## Overview
This document is the complete, unified workflow specification for the nowu framework. It integrates four key additions over v3:

1. **Architecture models formalized per step** — which C4 diagram, CPG layer, or structural model is produced and consumed at each step.
2. **Verification vs. Validation** — the V-Model distinction applied to nowu, closing the gap where the previous workflow only verified ("built it right") but never validated ("built the right thing").[^1][^2]
3. **Consolidated step-by-step reference table** — scope, perspective, task, input, output, model, and gate for every step.
4. **Implementation plan** — exact files to create in the repo, in what order, to make this workflow operational with Claude Code today.

***
## Part I: The Verification-Validation Gap
### The Problem
The previous workflow (v3) had a blind spot. Steps S7 (VBR) and S8 (Review) only performed **verification**: they checked whether the implementation matched its task specification — "did it pass tests, respect architecture, stay in scope?" But no step checked **validation**: "does this task specification actually solve the original problem?"[^2]

The IEEE definition makes this precise:[^3]

- **Verification**: "The process of determining whether the products of a given phase fulfill the requirements established during the previous phase."
- **Validation**: "The process of evaluating software at the end of the software development process to ensure compliance with software requirements."

In other words: verification checks each step against the step before it (local correctness), while validation checks the final result against the original need (global correctness).[^1]
### The V-Model Solution
The V-Model maps each development phase to a corresponding test phase:[^1]

| Development Phase | Test Phase | Type |
|---|---|---|
| Requirements Analysis | Acceptance Testing | **Validation** |
| System Design | System Testing | **Validation** |
| Detailed Design | Integration Testing | **Verification** |
| Implementation | Unit Testing | **Verification** |

The critical insight: validation happens at the **requirements level**, not the code level. Unit tests and code review are verification. Checking whether the software meets the user's actual need is validation — and it must trace back to the original requirements.[^4][^5]
### How nowu v4 Fixes This
Validation is distributed across three points in the workflow rather than concentrated in a single step:

**S4 (Decision) — Primary validation gate.** The human reviews not just "which option is best?" but "does this option actually solve the problem stated in the Intake Brief?" The decision record must explicitly confirm: "This decision addresses use cases [NF-01, NF-04] because [reason]." If the decision doesn't connect to the original need, it fails validation before any code is written.[^4]

**S5 (Shaping) — Secondary validation gate.** The human reviews the task spec and checks: "If every acceptance criterion passes, will the original problem be solved?" This is where wrong abstractions get caught — the task might be technically correct but solve the wrong thing. The shaper must include a `validation_trace` field linking each acceptance criterion back to a use-case ID.

**S8 (Review) — Validation checklist added.** The reviewer now runs two checklists: a **verification checklist** (architecture, scope, tests, style — same as v3) and a **validation checklist** that traces the implementation back through the artifact chain:

```
Validation Checklist:
- [ ] Task traces to decision: task.decision_id → D-NNN exists and is accepted
- [ ] Decision traces to intake: D-NNN.intake_id → intake exists
- [ ] Intake traces to use cases: intake.use_case_ids → all referenced use cases exist
- [ ] Acceptance criteria cover use cases: every use_case_id has ≥1 acceptance criterion
- [ ] No orphan work: nothing was implemented that doesn't trace to a use case
```

This bidirectional traceability — requirements → tests AND tests → requirements — is the core of V-Model compliance.[^5][^6]

***
## Part II: Architecture Models Per Step
### The Model Pyramid
Software representations exist at multiple abstraction levels. The C4 model provides four zoom levels for architecture, while the Code Property Graph (CPG) provides four layers for code structure. Together they form a complete pyramid from system context down to data flow:[^7][^8][^9][^10]

| Level | C4 View | CPG Layer | What It Shows | Who Needs It |
|---|---|---|---|---|
| L1 | System Context | — | Actors + systems, boundaries | Stakeholders, architect |
| L2 | Container | Module Dependency Graph | Modules, their interactions, tech stack | Architect, shaper |
| L3 | Component | Interface/Contract Graph | Classes, protocols, services within a module | Shaper, implementer |
| L4 | Code | AST → CFG → PDG → CPG | Syntax, control flow, data dependencies | Implementer, reviewer |

A Code Property Graph merges three code representations into one queryable supergraph:[^11][^8]

- **AST (Abstract Syntax Tree)**: Captures what the code *says* — syntactic structure, functions, expressions, operators.[^8]
- **CFG (Control Flow Graph)**: Captures the *order of execution* — branches, loops, conditional paths.[^8]
- **PDG (Program Dependence Graph)**: Captures how *data moves* — assignments, parameters, return values.[^8]

The CPG merges these by connecting nodes through shared identity — a function node in the AST links to its CFG entry point and to the PDG edges that trace data through its parameters. This allows cross-cutting queries like "show all paths from user input to database write" that no single representation can answer alone.[^8]
### Which Models to Formalize at Each Step
Not every step needs every model. The principle: **formalize only the model at your current abstraction level**. Creating a CPG during architecture analysis is waste; drawing a system context diagram during implementation is distraction.

| Step | Model Produced | Format (v1) | Format (v2+ with know) |
|---|---|---|---|
| S1: Intake | None (text only) | — | — |
| S2: Constraints | C4 L1 System Context (if new actors/systems) | Mermaid in constraints.md | `know` SYSTEM atoms |
| S3: Options | C4 L2 Container per option | Mermaid in options.md | `know` MODULE + DEPENDENCY atoms |
| S4: Decision | Chosen C4 L2 becomes reference | Append to ARCHITECTURE.md | Update `know` graph |
| S5: Shaping | C4 L3 Component (file/class map) | File tree + contract list | `know` COMPONENT atoms |
| S6: Implementation | Implicit AST (LLM understands) | Code itself | Code + `know` CODE atoms |
| S7: VBR | AST-based boundary test | `test_architecture_*` | CPG query: "no cross-boundary imports" |
| S8: Review | Diff against C4 L3 expected | Git diff analysis | `know.diff()` against expected graph |
| S9: Capture | Update C4 L2 if boundaries changed | Update ARCHITECTURE.md | Update `know` MODULE atoms |
### Practical Architecture Model for v1
For nowu v1, full CPG tooling (Joern, Fraunhofer CPG library) is unnecessary. The practical equivalent:

- **C4 L2 (Module Map)**: Already exists in `ARCHITECTURE.md` Section 4.1 — the five-module diagram (core, flow, bridge, soul, know). Updated at S4/S9 when module boundaries change.
- **C4 L3 (Contract Graph)**: The `core/contracts/*.py` Protocol files ARE the component graph — they define which interfaces exist and who implements them.
- **CPG L1 (AST boundary check)**: The architecture tests in `tests/unit/core/test_architecture.py` use Python's `ast` module to parse imports and verify no cross-boundary violations. This is a lightweight CPG Layer 1 enforcement.
- **File tree as Component View**: `find src/nowu/<module> -name '*.py'` serves as a live C4 L3 component diagram during shaping.
### Future: `know` as a Semantic CPG
When `know` stores atoms with typed connections, it becomes a lightweight CPG:[^12]

- `MODULE("flow") --DEPENDS_ON--> MODULE("core")` = C4 L2 edge
- `CLASS("SessionOrchestrator") --IMPLEMENTS--> PROTOCOL("FlowProtocol")` = C4 L3 edge
- `FUNCTION("recover()") --CALLS--> FUNCTION("recall()")` = CPG call graph edge
- `VARIABLE("session_state") --FLOWS_TO--> FUNCTION("store()")` = CPG data flow edge

The key advantage: `kb.subgraph(depth=2, from="MODULE:flow")` returns the C4 L2 view, while `kb.subgraph(depth=4, from="FUNCTION:recover")` returns the CPG-level view — same data, different zoom levels. This eliminates the need to maintain separate diagrams at different levels.

***
## Part III: The Complete Workflow — Step by Step
### Consolidated Reference
| Step | Perspective | C4 Level | Task | Producer | Input Artifact | Output Artifact | Model Produced | Gate |
|---|---|---|---|---|---|---|---|---|
| **S1** | System | L1 | Identify problem, tag use cases, estimate appetite | Human / main session | Idea + V1_PLAN | **Intake Brief** | None | None |
| **S2** | System→Module | L1-2 | Analyze constraints, boundaries, risks | `nowu-architect` | Intake Brief + ARCHITECTURE + DECISIONS | **Constraints Sheet** | C4 L1 (if new actors) | None |
| **S3** | Module | L2 | Propose 2-3 options with tradeoffs | `nowu-architect` | Constraints Sheet + contracts | **Options Sheet** | C4 L2 per option | None |
| **S4** | Module | L2 | Evaluate, score, decide, record | `nowu-architect` + **human** | Options Sheet + DECISIONS | **Decision Record** (D-NNN) | Chosen C4 L2 | **🛑 VALIDATION + approval** |
| **S5** | Component | L3 | Break into bounded tasks ≤4h | `nowu-shaper` + **human** | Decision handoff + file tree | **Task Spec(s)** | C4 L3 (file/class map) | **🛑 VALIDATION + scope approval** |
| **S6** | Code | L4 | TDD: test → implement → refactor | Main session | Task Spec (in-scope files only) | **Change Set** | Implicit AST | Tier 1 (auto) |
| **S7** | Code | L4 | Run pytest + mypy + ruff + scope check | Automated / hooks | Change Set + Task Spec | **VBR Report** | AST boundary test | Tier 1 (pass/fail) |
| **S8** | Component→Code | L3-4 | Verify + Validate against chain | `nowu-reviewer` | VBR + Change Set + Task Spec + diff | **Review Report** | Diff vs C4 L3 | Tier 1/2 |
| **S9** | System | L1-2 | Update decisions, progress, lessons | `nowu-curator` | Review Report + DECISIONS + PROGRESS | **Capture Record** | Update C4 L2 (if needed) | Tier 1 (auto) |
### S1: Intake
**Perspective**: Bird's eye — the whole system and its users.

**What the role needs to work**: The V1 plan (to know what's next), use-case IDs (to tag relevance), and current progress (to avoid duplicate work). The intake role does NOT need to understand implementation details, architecture internals, or code structure. Its job is to translate a human need into a structured problem statement.

**Scope boundary**: Load V1_PLAN.md, USE_CASES.md (by ID reference only), PROGRESS.md. Exclude all source code, tests, architecture docs, and contract files.

**Output**: Intake Brief — problem statement, use-case IDs, affected modules (first guess), appetite, open questions. Contains the handoff header with `status: READY_FOR_ARCH`.

**Model**: None. Intake operates at the idea level, before any structural model is useful.
### S2: Architecture Analysis
**Perspective**: System context zooming into module boundaries.

**What the role needs to work**: The intake brief (the problem), the architecture document (module map), existing decisions (constraints), and contract files (public API surface). The architect needs to understand what modules exist, how they interact, and what decisions constrain the design space. The architect does NOT need source code internals, test implementations, or the V1 plan (already consumed in S1).

**Scope boundary**: Load S1 artifact, ARCHITECTURE.md, DECISIONS.md, `core/contracts/*.py`. Exclude source internals, tests, V1_PLAN.

**Output**: Constraints Sheet — module boundaries (affected/not affected), architectural constraints with D-NNN references, risks with severity, assumptions (validated/not), open questions. Contains `status: READY_FOR_OPTIONS`.

**Model**: If the intake introduces new external actors or systems, produce a C4 Level 1 System Context diagram (Mermaid). Otherwise, reference the existing one in ARCHITECTURE.md.
### S3: Design Options
**Perspective**: Module interaction level — how modules will connect to solve the problem.

**What the role needs to work**: The constraints sheet (what's fixed), the intake brief (appetite), and contract files (current interfaces). The options designer needs enough understanding to sketch 2-3 viable approaches at the module boundary level — not implementation details, but "Module A wraps Module B via Protocol X" level. Does NOT need full architecture docs (constraints already extracted) or source internals.

**Scope boundary**: Load S2 artifact, S1 artifact, contracts, module `__init__.py` files. Exclude source internals, tests, full ARCHITECTURE.md.

**Output**: Options Sheet — 2-3 options each with summary, design sketch (C4 L2), pros/cons, risk mitigation, effort estimate, and migration path. Weighted evaluation with scores and recommendation. Contains `status: READY_FOR_DECISION`.

**Model**: One C4 Level 2 Container diagram per option, showing how modules interact under that approach. Keep them simple — boxes and arrows in Mermaid, not elaborate UML.
### S4: Evaluation and Decision 🛑
**Perspective**: Module level — choosing between architectural approaches.

**What the role needs to work**: The options sheet (with scored evaluation) and existing decisions (to check for contradictions). This is primarily a human judgment step — the architect presents, the human decides.

**Scope boundary**: Load S3 artifact, DECISIONS.md. Exclude source code, tests, contracts.

**Output**: Decision Record (D-NNN) appended to DECISIONS.md, plus a decision handoff artifact with `status: READY_FOR_SHAPING`.

**Model**: The chosen option's C4 L2 diagram becomes the reference for this work. If it changes the module map, ARCHITECTURE.md Section 4.1 is updated at S9.

**🛑 VALIDATION GATE**: The human must confirm:
- Does this decision address the use cases listed in the intake?
- If this option is fully implemented, is the original problem solved?
- Is the effort within the appetite?

This is the primary validation point — "building the right thing" is decided here.[^1][^4]
### S5: Task Shaping 🛑
**Perspective**: Inside a module — component-level file and class structure.

**What the role needs to work**: The decision handoff (what to build), the file tree of affected modules (what exists), contract files (interfaces to implement or use), test directory structure (where tests go), and progress tracking (task numbering, dependencies). The shaper does NOT need architecture docs (decision is settled), vision docs, or unrelated modules' code.

**Scope boundary**: Load S4 handoff, file tree, contracts, test structure, PROGRESS.md. Exclude architecture docs, vision, USE_CASES.md, unrelated modules.

**Output**: 1-5 Task Specs, each with: title, use-case IDs, in-scope files (explicit list), out-of-scope boundaries, acceptance criteria (with named tests), test strategy (write-first order), dependencies, estimated hours (≤4h), and a `validation_trace` field.

The `validation_trace` is the v4 addition:

```yaml
validation_trace:
  - use_case: "NF-01"
    acceptance_criteria: ["AC-1", "AC-3"]
    rationale: "AC-1 tests store, AC-3 tests no direct imports → NF-01 is covered"
  - use_case: "NF-04"
    acceptance_criteria: ["AC-2"]
    rationale: "AC-2 tests recall filtering → NF-04 session recovery is covered"
```

**Model**: C4 Level 3 Component view — the file/class structure within the affected module. Practically, this is the file tree + contract protocols that the implementer will work with.

**🛑 VALIDATION GATE**: The human must confirm:
- If every acceptance criterion passes, is every use-case ID covered?
- Are there use cases in the intake that have NO acceptance criterion? (gap = validation failure)
- Is the scope actually bounded? (no "and related files")

This is the secondary validation point — ensuring the task specification captures the right requirements.[^5]
### S6: Implementation (TDD)
**Perspective**: Code level — functions, classes, type signatures, test assertions.

**What the role needs to work**: The task spec (scope, acceptance criteria, test strategy) and ONLY the in-scope files listed in it. The implementer also needs `pyproject.toml` for tooling config and the specific contract being implemented. **Nothing else.** This is the most aggressively scoped step — loading architecture docs during coding causes re-litigation of settled decisions; loading unrelated modules causes unnecessary coupling.[^12]

**Scope boundary**: Load S5 task spec, in-scope files only, related tests, pyproject.toml. Exclude architecture docs, decisions, vision, plan, USE_CASES.md, other modules.

**Output**: Change Set — list of files changed with change type and summary, acceptance criteria addressed (true/false per criterion), implementation notes.

**Model**: The LLM implicitly understands code at AST level. No explicit model is produced. The code itself IS the Level 4 representation.
### S7: VBR (Verify Before Reporting)
**Perspective**: Code level — mechanical quality checks.

**What the role needs to work**: The change set (what changed), the task spec (scope boundaries for scope check), and pyproject.toml (commands to run). VBR is entirely mechanical — it runs commands and reports results.

**Scope boundary**: Load S6 artifact, S5 task spec (in_scope_files), pyproject.toml. Exclude everything else.

**Output**: VBR Report — pass/fail per check (pytest, mypy, ruff), scope violation check (files in diff vs files allowed), raw output. Contains `status: READY_FOR_REVIEW` if all pass, or `CHANGES_REQUESTED` if any fail.

**Model**: The AST-based architecture test (`test_architecture_*`) is a lightweight CPG Layer 1 check — it uses Python's `ast` module to verify import boundaries. This is the only structural model check that runs automatically.
### S8: Review (Verification + Validation)
**Perspective**: Cross-level — checking code (L4) against component design (L3) and tracing back to requirements.

**What the role needs to work**: The VBR report (evidence), the change set (what changed), the task spec (what should have changed, acceptance criteria), the git diff, and architecture rules (`.claude/rules/architecture.md`). The reviewer has a **fresh context window** — it should NOT carry accumulated context from earlier steps.[^13]

**Scope boundary**: Load S7 VBR, S6 changeset, S5 task spec, git diff, rules. Exclude full architecture docs, vision, plan, upstream intake/constraints/options.

**Output**: Review Report with TWO checklists:

**Verification Checklist** ("built it right"):
- Architecture boundaries respected
- Only in-scope files modified
- Tests written before implementation (TDD)
- Acceptance criteria covered
- Types clean (mypy)
- Style clean (ruff)
- Follows existing decisions

**Validation Checklist** ("built the right thing"):
- Task traces to decision: `task.decision_id` → D-NNN exists
- Decision traces to intake: `D-NNN.intake_id` → intake exists
- Intake traces to use cases: `intake.use_case_ids` → all exist
- Acceptance criteria cover use cases: every `use_case_id` has ≥1 criterion (via `validation_trace`)
- No orphan work: nothing implemented that doesn't trace to a use case

**Model**: The reviewer implicitly checks the implementation against the expected C4 L3 component structure — "were only the expected files/classes created or modified?"
### S9: Capture and Close
**Perspective**: Back to system level — recording what happened for future cycles.

**What the role needs to work**: The review report (lessons, outcome), DECISIONS.md (to check for needed updates), PROGRESS.md (to update status), and git log (for commit message). The curator writes about "what" and "why", never "how" — it should NOT load source code.[^14]

**Scope boundary**: Load S8 review, DECISIONS.md, PROGRESS.md, git log. Exclude source code, tests.

**Output**: Capture Record — progress update, decisions captured, lessons categorized, follow-ups listed, commit message composed. Contains `status: DONE` or `READY_FOR_SHAPING` (next task) or `READY_FOR_ARCH` (next feature).

**Model**: If the work changed module boundaries, update the C4 L2 module map in ARCHITECTURE.md. Otherwise, no model update needed.

***
## Part IV: Implementation — Making This Real
### What to Create in the Repo
The following files turn this specification into a working Claude Code setup. They are listed in creation order — each file depends only on files above it.
### Phase 1: Foundation (do first)
**1. `CLAUDE.md`** (root — ~50 lines)

```markdown
# nowu — AI-Powered Project Management Framework

Python 3.11+ framework using DDD (Domain/Application/Infrastructure/Interface layers).
5 modules: core (contracts + services), flow (orchestration), bridge (human-AI),
soul (identity), know (knowledge graph).

## Commands
- `uv run pytest --tb=short -q` — run tests
- `uv run mypy src/ --strict` — type check
- `uv run ruff check .` — lint
- `uv run ruff format .` — format

## Architecture Rules
Domain layer must NOT import infrastructure. All module interactions go through
contracts in core/contracts/. See docs/ARCHITECTURE.md Section 4.1 for module map.

## Workflow
This project uses a 9-step development workflow (S1-S9).
See docs/WORKFLOW.md for the full specification.
Before coding: read the active task spec in state/tasks/.
Follow TDD: write failing test → make it pass → refactor.
Use conventional commits: feat:, fix:, refactor:, docs:, test: + [use-case IDs]

## What Claude Gets Wrong
- Tends to put infrastructure concerns in domain layer — always check imports
- Forgets to run mypy after changes — always run full quality suite
- Loads too much context — only read files listed in the active task spec
- Re-litigates settled decisions — if a D-NNN exists, follow it, don't question it
```

**2. `.claude/settings.json`** (hooks)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "uv run pytest --tb=short -q && uv run mypy src/ --strict && uv run ruff check ."
          }
        ]
      }
    ]
  }
}
```

**3. `.claude/rules/`** (auto-loaded context rules)

Create four files:
- `architecture.md` — module boundaries, layer rules, import constraints
- `testing.md` — TDD workflow, test naming, fixture patterns
- `code-style.md` — Python standards, naming, function design
- `workflow.md` — 9-step overview, approval tiers, handoff status enum

Each should be ≤30 lines — these are injected on every interaction, so brevity matters.[^15]
### Phase 2: Agents
**4. `.claude/agents/nowu-architect.md`**

```markdown
---
name: nowu-architect
description: Analyzes architecture, identifies constraints, proposes design options,
  and records decisions. Use for S1-S4 of the workflow.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
---

You are the architect agent for the nowu framework.

## Your Scope (C4 Level 1-2: System and Module)
You work at the system and module level. You see module boundaries, contracts,
and decisions. You NEVER see source code internals or test implementations.

## What You Produce
- S2: Constraints Sheet (state/arch/<id>-constraints.md)
- S3: Options Sheet (state/arch/<id>-options.md)
- S4: Decision Record (docs/DECISIONS.md entry + state/arch/<id>-decision.md)

## What You Load
- docs/ARCHITECTURE.md (module map)
- docs/DECISIONS.md (existing constraints)
- core/contracts/*.py (public interfaces only)
- The intake brief (state/intake/<id>.md)

## What You NEVER Load
- Source code inside modules (src/nowu/<module>/<file>.py)
- Test files (tests/)
- V1_PLAN.md (already consumed in intake)
- USE_CASES.md (already tagged in intake)

## Validation Responsibility
At S4, you must confirm: "This decision addresses use cases [IDs] because [reason]."
If you cannot make this statement, the decision is not ready.

## Architecture Models
- If new external actors/systems: produce a C4 L1 Mermaid diagram
- For each option: produce a C4 L2 Mermaid diagram showing module interactions
- Keep diagrams simple: boxes + arrows + labels. No UML class diagrams at this level.

Save patterns you discover to your project memory.
```

**5. `.claude/agents/nowu-shaper.md`**

```markdown
---
name: nowu-shaper
description: Breaks decisions into bounded implementation tasks with explicit scope,
  acceptance criteria, and validation traces. Use for S5 of the workflow.
tools: Read, Grep, Glob, Bash, Write
model: sonnet
memory: project
---

You are the shaper agent for the nowu framework.

## Your Scope (C4 Level 3: Component)
You work at the file/class level within a module. You see file trees, contract
protocols, and test directory structure. You do NOT see architecture docs or
vision docs (the decision is settled — respect it).

## What You Produce
- Task Specs (state/tasks/<id>.md) using templates/task-spec.md

## Key Fields
Every task MUST have:
- in_scope_files: explicit file paths (no wildcards)
- acceptance_criteria: each with a named test function
- validation_trace: mapping use_case_ids → acceptance criteria
- estimated_hours: ≤4h (break down if larger)

## Validation Responsibility
Every use_case_id from the intake must map to ≥1 acceptance criterion.
If a use case has no criterion, the shaping is incomplete.

Save shaping patterns to your project memory.
```

**6. `.claude/agents/nowu-reviewer.md`**

```markdown
---
name: nowu-reviewer
description: Reviews completed implementation for verification (built it right) and
  validation (built the right thing). Use for S8 of the workflow.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
---

You are the reviewer agent for the nowu framework.

## Your Scope (C4 Level 3-4: Component + Code)
You see git diffs, VBR results, task specs, and architecture rules.
You have a FRESH context window — no accumulated bias from earlier steps.

## What You Check

### Verification ("built it right")
1. Architecture: no import boundary violations
2. Scope: only in-scope files modified
3. TDD: tests appear before implementation in git log
4. Acceptance: all criteria have passing tests
5. Types: mypy clean (from VBR)
6. Style: ruff clean (from VBR)
7. Decisions: changes follow D-NNN constraints

### Validation ("built the right thing")
1. task.decision_id → D-NNN exists and is accepted
2. D-NNN.intake_id → intake exists
3. intake.use_case_ids → all referenced use cases exist
4. Every use_case_id has ≥1 acceptance criterion (from validation_trace)
5. No orphan work: nothing implemented outside trace chain

## Output
Review Report (state/reviews/<task-id>.md) with:
- Verification checklist (pass/fail per item with evidence)
- Validation checklist (trace confirmed or broken)
- Critical issues / warnings / suggestions
- Lessons observed

Save recurring review patterns to your project memory.
```

**7. `.claude/agents/nowu-curator.md`**

```markdown
---
name: nowu-curator
description: Updates decisions, progress, and captures lessons after approved work.
  Use for S9 of the workflow.
tools: Read, Write, Grep, Glob
model: haiku
memory: project
---

You are the curator agent for the nowu framework.

## Your Scope (C4 Level 1-2: System)
You work at the system level. You update DECISIONS.md, PROGRESS.md, and capture
lessons. You NEVER read or modify source code or tests.

## What You Produce
- Capture Record (state/capture/<date>-<scope>.md)
- Updated docs/PROGRESS.md
- Updated docs/DECISIONS.md (if new decisions)
- Conventional commit message with use-case IDs

## What You Load
- S8 Review Report
- docs/DECISIONS.md
- docs/PROGRESS.md
- Git log of recent commits

## What You NEVER Load
- Source code, tests, contracts (capture is about "what" and "why", never "how")
```
### Phase 3: Templates and State Directories
**8. `templates/`** — one template per artifact type:

```
templates/
├── intake-brief.md
├── constraints-sheet.md
├── options-sheet.md
├── decision-handoff.md
├── task-spec.md
├── changeset.md
├── vbr-report.md
├── review-report.md
└── capture-record.md
```

Each template contains the YAML schema from the v3 artifact specification with placeholder values and the handoff header. Agents reference these when producing artifacts.

**9. `state/`** — directories for artifact storage:

```
state/
├── intake/
├── arch/
├── tasks/
├── changes/
├── vbr/
├── reviews/
└── capture/
```
### Phase 4: Skills
**10. `.claude/skills/full-cycle/SKILL.md`** — the complete S1→S9 workflow skill that delegates to subagents (as defined in the previous conversation turn, now updated with validation gates and architecture model production).

**11. `.claude/skills/implement-step/SKILL.md`** — the Mode B loop (S5→S9 repeated for shaped tasks).
### Phase 5: Workflow Documentation
**12. `docs/WORKFLOW.md`** — this document, adapted for the repo. Replace the current WORKFLOW.md with this specification.
### Bootstrap Sequence
Run these commands to create the structure:

```bash
# Create directories
mkdir -p .claude/{agents,rules,skills/full-cycle,skills/implement-step}
mkdir -p state/{intake,arch,tasks,changes,vbr,reviews,capture}
mkdir -p templates

# Initialize CLAUDE.md
claude  # then run /init, review, and replace with the content above

# Create files in order
# 1. CLAUDE.md (manual or claude /init + edit)
# 2. .claude/settings.json
# 3. .claude/rules/*.md (4 files)
# 4. .claude/agents/*.md (4 files)
# 5. templates/*.md (9 files)
# 6. .claude/skills/*/SKILL.md (2 files)
# 7. docs/WORKFLOW.md

# Test the setup
claude
> "Use the nowu-architect agent to analyze: [your next V1 step]"
```
### Verification of the Setup
After creating all files, verify the workflow is operational:

1. **Agent isolation test**: Ask `nowu-architect` about implementation details — it should refuse or redirect (it can only read architecture docs and contracts).
2. **Template test**: Ask `nowu-shaper` to create a task — it should produce a file matching `templates/task-spec.md` schema including `validation_trace`.
3. **Hook test**: Try to `git commit` without running tests — the pre-commit hook should block it.
4. **Traceability test**: After one full cycle, verify that `task → decision → intake → use case` chain is unbroken.

***
## Part V: The Model Pyramid — Connecting Everything
### How It All Fits Together
```
                    Human Understanding
                         ▲
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │   C4 L1: System    │   "What does the   │  S1-S2, S9
    │   Context          │    system DO?"      │  (Intake, Arch, Capture)
    │                    │                    │
    ├────────────────────┼────────────────────┤
    │                    │                    │
    │   C4 L2: Container │   "How do modules   │  S3-S4
    │   (Module Map)     │    INTERACT?"       │  (Options, Decision)
    │                    │                    │
    ├────────────────────┼────────────────────┤
    │                    │                    │
    │   C4 L3: Component │   "What classes/    │  S5, S8
    │   (Contracts)      │    files EXIST?"    │  (Shaping, Review)
    │                    │                    │
    ├────────────────────┼────────────────────┤
    │                    │                    │
    │   C4 L4 / CPG:     │   "How does the     │  S6-S7
    │   Code (AST→PDG)   │    code WORK?"      │  (Implement, VBR)
    │                    │                    │
    └────────────────────┼────────────────────┘
                         ▼
                    Machine Understanding
```

Each step operates at its level. The validation chain runs vertically through all levels — from use cases (L1) through decisions (L2) through task specs (L3) to acceptance tests (L4) and back. If any link in the chain breaks, the reviewer catches it at S8.[^5]

The architecture models (C4 diagrams, contract protocols, AST boundary tests) are not separate deliverables maintained in isolation — they are **produced as natural byproducts of each step** and consumed by the next step that needs them. This prevents the common failure mode of architecture diagrams that diverge from code, because the same workflow that writes code also updates the models.

---

## References

1. [V-Model: Verification & Validation in SDLC - Teaching Agile](https://teachingagile.com/sdlc/models/v-model) - Master the V-Model with our comprehensive guide. Learn verification and validation strategies, imple...

2. [Software verification and validation - Wikipedia](https://en.wikipedia.org/wiki/Software_verification_and_validation)

3. [[PDF] IEEE Standard for Software Verification and Validation Plans](https://www.cs.utep.edu/isalamah/courses/5387/VVPlanIEEE.pdf) - If V&V is performed by an independent group, then the SVVP should specify the criteria for maintaini...

4. [Validation and Verification in the V-Model: How to Successfully ...](https://www.reqsuite.io/en/blog/validation-and-verification-v-models) - A fundamental principle of an effective validation and verification process is traceability between ...

5. [Understanding the V-Model in Testing](https://mastersoftwaretesting.com/testing-fundamentals/v-model-in-software-testing) - Master the V-Model testing methodology with our comprehensive guide. Learn implementation strategies...

6. [V Model in System Engineering - Visure Solutions](https://visuresolutions.com/alm-guide/v-model-systems-engineering) - Understand the V-Model development model and enhance your development process. Sign up for a free 30...

7. [Code property graph - Wikipedia](https://en.wikipedia.org/wiki/Code_property_graph) - A code property graph (CPG) is a computer program representation that captures syntactic structure, ...

8. [Code Property Graph | Apiiro - Apiiro](https://apiiro.com/glossary/code-property-graph/) - What is a code property graph (CPG)? Learn how it unifies AST, CFG, and data flow for advanced secur...

9. [What is C4 Model? Complete Guide for Software Architecture](https://miro.com/diagramming/c4-model-for-software-architecture/) - What the C4 model is: a hierarchical framework for visualizing software architecture through four ab...

10. [The C4 Model for Software Architecture](https://www.infoq.com/articles/C4-architecture-model/) - C4 stands for context, containers, components, and code — a set of hierarchical diagrams that you ca...

11. [Home - Code Property Graph - GitHub Pages](https://fraunhofer-aisec.github.io/cpg/) - A Code Property Graph (CPG) is a graph-based representation of code which unites several concepts su...

12. [Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LL.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/67744cb3-570d-4a0e-9547-4e0af858b4d2/Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LLM-Empowered-Agentic.pdf?AWSAccessKeyId=ASIA2F3EMEYEU5GMI4PD&Signature=Ry4JorCDT7inFzUJI9Iju15f9Hs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEI7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIDOF7XeoXrF6Z4j3SM9GW7Br5HHEKn7gv4bS7ZF2DoUJAiEAgdNfAG7N0DxoMMDlX6U0sMFVnygFdUUj7dYa5eszBbsq8wQIVxABGgw2OTk3NTMzMDk3MDUiDKUu9FbwnxRlNj9HXyrQBNJht%2BYc4%2Fo1SHQCKedbQMMHqCoiNCtyhntYE579KlrXnALMdkjDNhZHSY5%2BsbklfAv4gGVhsMXEe661EH1eoAEL%2FomfB1e%2F1hDi%2BnCedwBU9LZMkMzLZDv%2FBBqhzldGFrM9nvgly%2B8mB14%2BI6YPk4bX0tjCJgtQ%2Bh5Yb9vG3bRDFMmBDd1zaWJRt%2BtRxRl39530v7WOxG0wF0KOzLc5hByuAbkHwDVwCKjk8RpgT6k3wouRBtnCbIcciVi3iZO1%2B5k40aUXV0CzXTia%2Bo4uV4zmZaVjnUbgLuH0jPY1fO0fiV7NkK7M7eN%2F8Vf2Vt1jCRbnAP3xQc8WThzgoJyuvezKXTI5YsufuhxAhsuduAEVeenUbE5Yg2h9nJLhixGsqWQKzk8%2B32cNufDGqQ2FGOM9cwzPbe8a1fscaz%2ByCoBeUoFQVFqEB4TOD6JwRn4JohkvHJcYJJvriN78Eb5lFTLlQGaxbn7IRuRaa6CHmIO4wkJfBeyqNVImy7dgl%2BWBab3QqbcRCKrNMpLTLbx3SFDFpbuMajgUAdqWxsohtuqBn46iKv1QyQDHaaanlbxgT3LgIQY%2FjfSjtJ7r9OiLWn%2BNfhSiChuSHA698mUyZhNqiTKwpmi1axGKTX15LX7DsDIqNixUeXAjggUo%2FN49RkDSPK%2Fr9XYNuNrZEZ%2BKiDKIePkUdkSLk5NZBF9nzkHPXX529%2FdDU4UXj2iCA6%2BZw9sA9or%2BHIlE0rzjKRZdkUMLxAO%2BnE45ttwdtWuQchYk7JjSPXfJPO%2Fnucc3JuJox%2FUw8YXEzQY6mAGJv5zzTgicMpUznP%2F1szZXluzimxQkpxyZMIHiNBYJEANBXxxhX9Wy65TLbnwRL0oD%2B9vcuMWt2tOow2Dn1fGdYHGR0eYrX2QdPiU4Yphl5ajXnExi878HSVs5mv5qFeaKVdQN%2F%2BFxLLUgmtXz9OcoUTPs0g5bMkmqov369ksZquq0bwbTQOD1Ec2E38SCUI%2F%2F7PFz70sziQ%3D%3D&Expires=1773213675) - A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic ...

13. [Agent Handoff Patterns: A Case Study in Multi-Step Workflows](https://getathenic.com/blog/agent-handoff-patterns-case-study) - Real-world analysis of agent handoff patterns from Athenic's multi-agent system -when to handoff, ho...

14. [Artifact-First Engineering: The Workflow That Replaced "Vibe Coding"](https://www.linkedin.com/pulse/artifact-first-engineering-workflow-replaced-vibe-coding-john-kehoe-ufgvc) - Stop calling it Vibe Coding! It's an immature, flippant nomenclature that is doing a disservice. Eig...

15. [Creating the Perfect CLAUDE.md for Claude Code - Dometrain](https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/) - In this guide, you'll learn how the CLAUDE.md file works, why it matters, and how to structure an ef...

