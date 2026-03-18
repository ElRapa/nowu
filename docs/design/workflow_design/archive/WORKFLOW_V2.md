# The nowu Standardized Development Workflow

**Version**: 2.0 — Unified Model  
**Date**: 2026-03-09  
**Status**: Active reference for Claude Code + future framework implementation

---

## Part I: The Workflow Model

### 1. The 9-Step Loop

Every piece of work in nowu follows a single, repeatable workflow. The key innovation is that each step operates at a specific **C4 abstraction level**, and agents/humans should only load context appropriate to that level.

The workflow is a **zoom-in / zoom-out** pattern:
- Steps 1-4 operate at **system level** (C4 L1-2) — architecture, decisions, constraints
- Step 5 operates at **module level** (C4 L2-3) — contracts, boundaries, task specs
- Steps 6-7 operate at **code level** (C4 L3-4) — files, functions, tests
- Step 8 **crosses levels** — reviews code against architecture
- Step 9 **zooms back out** to system level — captures decisions and lessons

```
       HIGH ABSTRACTION                              LOW ABSTRACTION
       (System Context)                              (Code Level)
       ┌──────────────┐    ┌─────────┐    ┌──────────────────┐    ┌────────┐    ┌─────────┐
       │ S1: Intake    │    │ S5:     │    │ S6: Implement    │    │ S8:    │    │ S9:     │
       │ S2: Arch      │───▶│ Shape   │───▶│ S7: Verify (VBR) │───▶│ Review │───▶│ Capture │
       │ S3: Options   │    │         │    │                  │    │        │    │         │
       │ S4: Decision  │    └─────────┘    └──────────────────┘    └────────┘    └─────────┘
       └──────────────┘                            │    ▲                          │
              ▲                                    │    │ fail                     │
              │                                    └────┘                          │
              └────────────────── next feature ───────────────────────────────────┘
```

### 2. Step Definitions

#### S1: Intake
- **What**: Gather the request, identify use-case IDs, affected modules
- **C4 Level**: 1 (System Context)
- **View**: System context — nowu + `know` + external actors
- **Input**: Idea, feature request, bug report, or next V1 plan step
- **Output**: Problem statement with use-case references and module scope
- **Context to load**: ARCHITECTURE.md (module map), V1_PLAN.md, USE_CASES.md (by ID only)
- **Context to EXCLUDE**: Source code, test files, implementation details
- **Agent**: nowu-architect (or main session for simple intakes)
- **Approval**: None — this is information gathering
- **Can skip if**: Task is already well-defined (go to S5 or S6)

#### S2: Architecture Analysis
- **What**: Define constraints, module boundaries, failure modes, assumptions to validate
- **C4 Level**: 1-2 (System Context → Container)
- **View**: Container diagram — which modules are involved, how they interact
- **Representation**: Module map from ARCHITECTURE.md Section 4.1
- **Input**: Problem statement from S1
- **Output**: Constraints list, affected module boundaries, identified risks
- **Context to load**: ARCHITECTURE.md, DECISIONS.md, `know` usage contract (Section 5)
- **Context to EXCLUDE**: Source code internals, test implementations
- **Agent**: nowu-architect
- **Approval**: None — analysis is informational
- **Can skip if**: Problem clearly falls within existing architecture with no boundary questions

#### S3: Design Options
- **What**: Produce 2-3 viable approaches with tradeoffs and migration implications
- **C4 Level**: 2 (Container) — zooming into module interactions
- **View**: Container diagram + interface contracts between modules
- **Representation**: Module boundaries + `core/contracts/*.py` public APIs
- **Input**: Constraints from S2
- **Output**: Options document (A/B/C) with pros, cons, effort estimates, migration path
- **Context to load**: S2 output + contract protocols + module `__init__.py` files
- **Context to EXCLUDE**: Internal module implementation, test bodies
- **Agent**: nowu-architect
- **Approval**: None — options are proposals, not decisions
- **Can skip if**: Only one viable approach exists (document why, go to S4)

#### S4: Evaluation & Decision
- **What**: Score options against criteria, select one, record rationale
- **C4 Level**: 2 (Container)
- **View**: Same as S3 — evaluating at module boundary level
- **Input**: Options from S3
- **Output**: Decision record (D-NNN in DECISIONS.md) with: chosen option, criteria scores, rationale
- **Context to load**: S3 output + existing DECISIONS.md (avoid contradictions)
- **Context to EXCLUDE**: Source code
- **Agent**: nowu-architect → human approval
- **Approval**: **Tier 2** (human reviews decision before implementation proceeds)
- **Can skip if**: No new architecture decision needed (existing decisions cover this)

---

#### S5: Task Shaping
- **What**: Break the decided approach into bounded implementation tasks (≤4h each)
- **C4 Level**: 3 (Component) — zooming into module internals
- **View**: Component diagram — what classes/services/functions exist within each module
- **Representation**: File tree (`src/nowu/<module>/`), existing contracts, test structure
- **Input**: Decision from S4 (or pre-shaped task if entering at S5)
- **Output**: 1-5 task specs, each containing:
  - Title + use-case IDs
  - In-scope files (explicit list)
  - Out-of-scope boundaries
  - Dependencies on other tasks
  - Acceptance criteria (testable)
  - Test strategy (what tests to write first)
  - Estimated time (≤4h)
- **Context to load**: Contracts, file tree, existing tests, PROGRESS.md
- **Context to EXCLUDE**: Architecture docs (decision is settled), vision docs, unrelated modules
- **Agent**: nowu-shaper
- **Approval**: **Tier 2** (human reviews task scope before implementation)
- **Can skip if**: Task is trivial and well-understood (< 1h, go to S6)

---

#### S6: Implementation (TDD)
- **What**: Write tests first, then minimal code to pass, then refactor
- **C4 Level**: 4 (Code) — deepest zoom
- **View**: Code-level — classes, functions, type signatures, test assertions
- **Representation**: AST-level understanding of specific files. Only in-scope files matter.
- **Input**: Single task spec from S5
- **Output**: Code + tests, both passing
- **Context to load**: **ONLY in-scope files** from task spec + related tests + the specific contract being implemented + pyproject.toml (tooling config)
- **Context to EXCLUDE**: Architecture docs, V1 plan, use cases doc (55k chars!), other modules' source, progress tracking, vision docs
- **Agent**: Main Claude Code session (needs iterative control)
- **Approval**: **Tier 1** (auto — proceed if tests pass and follows scope)
- **Can skip if**: Never — every change needs implementation

> **WHY such strict context exclusion?**
> The Guo et al. survey confirms: "the ordering and content of code snippets in the prompt significantly impacts performance."
> Loading architecture docs during coding causes agents to re-litigate settled decisions.
> Loading unrelated modules causes agents to create unnecessary cross-module dependencies.
> The paper calls this "project amnesia in reverse" — too much context creates confusion, just like too little creates forgetting.

#### S7: Verify Before Reporting (VBR)
- **What**: Run automated quality checks. Compare outputs to acceptance criteria.
- **C4 Level**: 4 (Code) — verification happens at code level
- **View**: Test results, lint output, type-check output
- **Input**: Implementation from S6
- **Output**: Pass (proceed to S8) or Fail (return to S6 with specific failures)
- **Commands**:
  ```bash
  uv run pytest --tb=short -q
  uv run mypy src/ --strict
  uv run ruff check .
  ```
- **Context to load**: Test output, acceptance criteria from task spec
- **Context to EXCLUDE**: Everything else — VBR is mechanical
- **Agent**: Automated (hooks in Claude Code) or main session
- **Approval**: **Tier 1** (auto — binary pass/fail)
- **Can skip if**: Never — VBR is non-negotiable

---

#### S8: Review
- **What**: Validate architecture compliance, test quality, code standards, scope boundaries
- **C4 Level**: 3-4 (Component + Code) — crosses levels to check alignment
- **View**: Diff view (what changed) + architecture rules (does it comply?)
- **Representation**: Git diff + architecture rules summary + acceptance criteria
- **Input**: Verified implementation from S7
- **Output**: Approve (proceed to S9) or Reject with specific issues (return to S6)
- **Review checklist**:
  1. Architecture: No import boundary violations?
  2. Scope: Only in-scope files modified?
  3. Tests: Written before implementation? Edge cases covered?
  4. Types: mypy clean?
  5. Style: ruff clean?
  6. Decisions: Changes follow existing D-NNN decisions?
- **Context to load**: Git diff, acceptance criteria, `.claude/rules/architecture.md`, test results
- **Context to EXCLUDE**: Full architecture docs (rules summary is sufficient), V1 plan, vision
- **Agent**: nowu-reviewer (separate context window = fresh perspective)
- **Approval**: **Tier 1** (auto for clean reviews) or **Tier 2** (if design concerns surface)
- **Can skip if**: Never for code changes. Can skip for docs-only changes.

#### S9: Capture & Close
- **What**: Persist decisions, update progress, capture lessons
- **C4 Level**: 1-2 (System Context) — zoom back out to capture at system level
- **View**: System-level — what decisions were made, what's the new state of the project
- **Input**: Approved implementation from S8
- **Output**: Updated DECISIONS.md (if new decisions), updated PROGRESS.md, lessons captured
- **Context to load**: DECISIONS.md (check for duplicates), PROGRESS.md, git log of recent commits
- **Context to EXCLUDE**: Source code (decisions capture "what" and "why", not "how")
- **Agent**: nowu-curator
- **Approval**: **Tier 1** (auto — documentation updates)
- **Can skip if**: No decisions were made and progress is trivial (but always update PROGRESS.md)

---

### 3. Architectural Views Per Step

This maps the C4 model, HLD/LLD distinctions, and code representations to each workflow step.

| Step | C4 Level | HLD/LLD | Representation Used | Code Representation |
|------|----------|---------|---------------------|---------------------|
| S1: Intake | L1 | HLD | System context: actors + systems | None |
| S2: Arch Analysis | L1-2 | HLD | Container diagram: module map | None |
| S3: Design Options | L2 | HLD→LLD | Container + interface contracts | Contract protocols (abstract) |
| S4: Decision | L2 | HLD | Container: selected approach | None |
| S5: Task Shaping | L3 | LLD | Component: file tree + test structure | File paths, function signatures |
| S6: Implementation | L4 | Code | Code: classes, functions, tests | AST (implicit via LLM), full source |
| S7: VBR | L4 | Code | Test results + lint output | Execution output |
| S8: Review | L3-4 | LLD+Code | Git diff + rules | AST boundaries (import checks) |
| S9: Capture | L1-2 | HLD | Decision records + progress | None |

### 4. Code Property Graphs and ASTs: When They Matter

The Guo et al. survey identifies a key future direction: moving from flat text representations to structured graph representations (ASTs, CFGs, CPGs) for better agent comprehension.

**For nowu right now (v1)**:
- **AST-based architecture tests** (already in Step 01): Your import boundary tests use AST parsing to verify module dependencies at the code level. This is the most practical CPG-adjacent technique today.
- **File tree as structural memory**: During S5 (Shaping), the file tree serves as a lightweight structural representation — the Shaper "sees" the codebase structure without reading all the code.
- **Contract protocols as interface graph**: Your `core/contracts/*.py` files represent the edges in a module dependency graph. They define what can talk to what.

**For nowu later (v2+)**:
- **`know` as a Code Property Graph**: When `know` stores code atoms with connections (calls, imports, depends-on), it becomes a semantic CPG that agents can query for relevant context without loading raw files.
- **Hierarchical attention**: Instead of loading 55k chars of USE_CASES.md, `know.subgraph()` could return only the atoms relevant to the current task — this is the "tiered memory" the survey calls for.

---

## Part II: Iteration Modes — Running Part of the Workflow

The full 9-step workflow is the **reference model**. In practice, you'll often run only part of it. The workflow is designed for this — each step has clear inputs and outputs, so you can enter at any step if you have the required input.

### Mode A: Full Cycle (new feature or V1 step)
**Run**: S1 → S2 → S3 → S4 → S5 → [S6 → S7]×n → S8 → S9  
**When**: New feature, new V1 plan step, cross-module change  
**Human touchpoints**: S4 (decision approval), S5 (scope approval)

### Mode B: Implementation Loop (shaped tasks ready)
**Run**: S5 → [S6 → S7]×n → S8 → S9 → (next task) → S5...  
**When**: Tasks are already shaped, need to execute them  
**Human touchpoints**: S5 (scope approval), periodic S8 reviews

### Mode C: Single Step (quick fix, small change)
**Run**: S6 → S7 → S8 → S9  
**When**: Bug fix, documentation update, small refactor within existing scope  
**Human touchpoints**: None (Tier 1 auto-approve if tests pass)

### Mode D: Architecture Only (research, planning)
**Run**: S1 → S2 → S3 → S4 → S9  
**When**: Evaluating an approach, making a decision, not yet implementing  
**Human touchpoints**: S4 (decision approval)

### Mode E: Partial Iteration (step-and-stop)
**Run**: Any single step, then stop  
**When**: "Just help me shape this task" or "Just review this code"  
**Human touchpoints**: Depends on step

**Trigger prompts for Claude Code**:

```
# Mode A: Full Cycle
"Use the full-cycle skill for: [feature description]"

# Mode B: Implementation Loop  
"Use the implement-step skill to execute Step 02 from V1_PLAN.md"

# Mode C: Quick Fix
"Fix [specific bug/issue] using TDD. Follow the workflow rules."

# Mode D: Architecture Only
"Use the nowu-architect agent to evaluate: [architecture question]"

# Mode E: Single Step
"Use the nowu-shaper agent to break down: [goal]"
"Use the nowu-reviewer agent to review recent changes"
```

---

## Part III: Standardizing Software Development

### Can every software project use this workflow?

**Yes, with flexibility in granularity.** The research from Guo et al. (150+ papers on LLM-based software engineering) reveals that the sequence is nearly universal — requirements → design → implementation → verification → capture — but the **depth** at each step varies dramatically by project type and complexity.

The key principle:

> **The workflow is always the same. The steps are always available. But for any given piece of work, some steps are thin (minutes) and some are thick (hours). None are ever zero — but some can be a single sentence.**

### Step Thickness by Project Type

| Step | Framework (nowu) | Business App (aperitif) | Quick Script | Bug Fix |
|------|------------------|------------------------|-------------|---------|
| S1: Intake | Thick — identify NF/PK IDs | Medium — business context | Thin — "I need X" | Thin — bug report |
| S2: Arch Analysis | Thick — module boundaries | Medium — data model | Thin — single file | Thin — affected area |
| S3: Design Options | Thick — 2-3 options scored | Medium — 1-2 options | Skip | Skip |
| S4: Decision | Thick — ADR recorded | Medium — decision noted | Skip | Skip |
| S5: Task Shaping | Thick — explicit scope | Medium — task list | Thin — 1 task | Thin — 1 task |
| S6: Implementation | Thick — TDD, contracts | Medium — TDD | Medium — write it | Medium — fix it |
| S7: VBR | Thick — full quality checks | Medium — tests + lint | Thin — run it | Thin — test passes |
| S8: Review | Thick — arch compliance | Medium — code review | Thin — self-review | Thin — self-review |
| S9: Capture | Thick — decisions + lessons | Medium — progress | Thin — commit | Thin — commit |

### What makes this standardizable?

1. **Fixed step order**: Even when steps are thin, they happen in the same sequence. This prevents the #1 failure mode identified in the survey: "jumping to code without understanding the problem."
2. **Defined inputs/outputs**: Each step has a clear input and output. If the input exists, the step can run. If the input is missing, the previous step was incomplete.
3. **C4-aligned context scoping**: Each step knows its abstraction level. This prevents the #2 failure mode: "context pollution from loading irrelevant information."
4. **Iteration modes**: You don't have to run the full cycle every time. Mode C (single step) and Mode E (step-and-stop) handle small work without ceremony.

### Evidence from Research

The Guo et al. survey confirms three patterns that validate this approach:

1. **Design-first improves outcomes**: "Generating a high-level plan or design before writing code significantly improves outcomes" (DRCodePilot, Codes framework). This maps to S2-S4 happening before S6.
2. **Static pipelines can be sufficient**: The Agentless approach (localize → repair → validate) — a simple fixed pipeline — performs competitively with complex dynamic planning. This validates that a standardized step order works.
3. **Multi-layer sketch generation**: The Codes framework generates repo structure → file sketches → implementations. This is exactly the C4 zoom-in pattern: L2 → L3 → L4.

---

## Part IV: Context Engineering — Preventing Drift

### The Core Problem

Both AI agents and humans suffer from the same failure modes:
- **Too much context** → lose focus on what matters now (context rot)
- **Too little context** → miss critical constraints or repeat past mistakes (project amnesia)
- **Wrong-level context** → architecture docs during coding causes decision re-litigation; code during architecture causes anchoring on existing patterns

### The Solution: Level-Locked Context

Each workflow step has a **context boundary**. The rule is simple:

> **Load only what's needed for the current C4 level. If it's from a different level, it's noise.**

### Context Anti-Patterns

| Anti-Pattern | Failure Mode | Which Step | Fix |
|-------------|-------------|------------|-----|
| Loading USE_CASES.md (55k chars) into implementation | 40% of context budget wasted | S6 | Reference by ID: "implements NF-01" |
| Loading all source code during architecture analysis | Anchoring on existing patterns | S2-S3 | Load only contracts and module boundaries |
| Loading ARCHITECTURE.md during coding | Re-litigating settled decisions | S6 | Decision is settled at S4, not revisited at S6 |
| Loading vision/soul docs during code review | Reviewer philosophizes instead of checking tests | S8 | Load rules summary only |
| Never clearing context between steps | Phase 1-4 context pollutes Phase 6 | All | Use subagents (fresh context) or /clear |
| Loading code during curation | Overly technical decision records | S9 | Curator writes docs, never reads code |

### How Claude Code Enforces This

Your Claude Code setup already enforces level-locked context through three mechanisms:

1. **Subagents**: Each agent (architect, shaper, reviewer, curator) runs in its own context window. The architect never sees code. The implementer never sees architecture docs. Context isolation is structural, not behavioral.

2. **Tool restrictions**: The architect has Read/Grep/Glob only (can't edit code). The curator has Read/Write for docs only (can't modify source). Tool access physically prevents wrong-level actions.

3. **Hooks**: The PreToolUse hook on `git commit` forces VBR (pytest + mypy + ruff) before any commit can happen. This is machine-enforced, not honor-system.

---

## Part V: Claude Code Setup (Current)

### File Structure

```
nowu/
├── CLAUDE.md                           # Root config (~50 lines, routing file)
├── .claude/
│   ├── settings.json                   # Hooks (VBR before commits)
│   ├── rules/                          # Auto-loaded rules
│   │   ├── architecture.md             # Module boundaries (S2-S4 context)
│   │   ├── testing.md                  # TDD workflow (S6-S7 context)
│   │   ├── code-style.md              # Python standards (S6 context)
│   │   └── workflow.md                 # 9-step loop, approval tiers
│   ├── agents/                         # Subagents (own context windows)
│   │   ├── nowu-architect.md           # S1-S4: HLD, system level
│   │   ├── nowu-shaper.md             # S5: LLD, component level
│   │   ├── nowu-reviewer.md           # S8: Cross-level review
│   │   └── nowu-curator.md            # S9: System-level capture
│   └── skills/                         # Reusable workflows
│       ├── full-cycle/SKILL.md        # Mode A: S1→S9
│       └── implement-step/SKILL.md    # Mode B: S5→S9 loop
├── docs/
│   ├── ARCHITECTURE.md                 # Architect reads this (S1-S4)
│   ├── V1_PLAN.md                     # Shaper reads this (S5)
│   ├── DECISIONS.md                    # Architect + Curator read this
│   ├── WORKFLOW.md                     # → Replace with this document
│   ├── PROGRESS.md                     # Shaper + Curator read this
│   └── USE_CASES.md                    # Referenced by ID only, never loaded in full
└── src/nowu/...
```

### Quick Start

```bash
# Install and subscribe
npm install -g @anthropic/claude-code
# Get Max plan ($100/month) for sustained development

# First session
cd /path/to/nowu
claude

# Mode A: Full cycle for next step
> Use the full-cycle skill for Step 02 from V1_PLAN.md

# Mode D: Architecture question
> Use the nowu-architect agent to evaluate: should MemoryService cache know queries?

# Mode C: Quick fix
> Fix the failing test in tests/unit/core/test_contracts.py using TDD
```

---

## Part VI: Future / TODOs

### Near-term (during v1 implementation)

- [ ] Replace docs/WORKFLOW.md with this document as the workflow reference
- [ ] Update CLAUDE.md to reference the 9-step model and iteration modes
- [ ] Add step-specific skills: `.claude/skills/architecture-analysis/SKILL.md`, `.claude/skills/shape-task/SKILL.md`
- [ ] Evolve "What Claude Gets Wrong" section in CLAUDE.md based on actual observed failures
- [ ] Add `.copilotignore` equivalent for Claude Code context exclusion

### Medium-term (v1 Steps 03-06)

- [ ] Implement `flow/orchestrator.py` that executes the 9-step loop programmatically (Step 04)
- [ ] Implement structured role payloads matching the input/output spec of each step (Step 04)
- [ ] `MemoryService.recall_context()` with abstraction-level filtering: "give me C4 L2 context for this module" (Step 02)
- [ ] VBR as a `flow` service, not just a shell command (Step 03)
- [ ] Approval queue in `bridge` with tier classification from WORKFLOW rules (Step 05)

### Long-term (v2+)

- [ ] `know` atoms as a lightweight Code Property Graph (store: imports, calls, depends-on connections between code elements)
- [ ] `know.subgraph()` replaces raw file loading — returns only atoms at the right abstraction level for the current step
- [ ] Agent memory in `know` instead of `.claude/agent-memory/` — each agent's learned patterns become queryable atoms
- [ ] Replaceable agent backends: Claude Code subagents now → OpenDevin / custom LLM agents later → same workflow, same context boundaries, different execution engine
- [ ] Non-code project types: aperitif business, real-estate — same 9-step workflow, different "implementation" step (S6 produces docs/analysis instead of code)
- [ ] Multi-project context scoping via `know` project namespaces — prevent cross-project contamination while enabling XP discovery (XP-01)

---

## Appendix: Research Foundation

This workflow design is informed by:

1. **Guo et al. (2025)**: "A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System" — 150+ papers on agent-based SE. Key findings: design-first improves outcomes, static pipelines work, multi-layer sketch generation matches C4 zoom, memory mechanisms are critical for repo-level tasks.

2. **C4 Model (Simon Brown)**: Four-level abstraction hierarchy for software architecture visualization. The insight that "different levels serve different audiences" maps directly to "different steps serve different context."

3. **Basecamp Shape Up**: Fixed appetite, shaping before building, no backlog. nowu extends this with architecture analysis, VBR, curation, and approval tiers.

4. **Anthropic Context Engineering**: "Find the smallest possible set of high-signal tokens." Context rot is real — more tokens means less precision. Progressive disclosure beats pre-loading.

5. **Code Property Graphs (Yamaguchi et al. 2014)**: Unified representation of AST + CFG + PDG. Relevant as future direction for `know` as structural code memory.
