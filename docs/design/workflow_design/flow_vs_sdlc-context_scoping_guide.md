# nowu Workflow vs SDLC & Architecture Levels — Context Scoping Guide

## Why This Matters

Your nowu workflow (Intake → Architecture → Design → Evaluation → Shaping → Implementation → VBR → Review → Capture) needs to load different context at each phase.
Loading architecture docs during code writing wastes attention budget. Loading code files during architecture analysis creates noise.

This guide maps each workflow phase to its abstraction level (HLD/LLD/Code) and defines exactly what context an AI agent (or human) should load.

---

## 1. Workflow Comparison

### nowu (Shape Up-based) vs SDLC vs Agile/Scrum

| Dimension | nowu Workflow | SDLC (Waterfall) | Agile/Scrum |
|-----------|--------------|-------------------|-------------|
| **Unit of work** | Shaped task (≤4h) in vertical slices | Phase-gated documents | User story in sprint |
| **Planning** | Architect + Shaper roles (per-task) | Big upfront planning phase | Sprint planning (per sprint) |
| **Design** | Architecture analysis + design options per task | Separate Design phase (SDD) | Emergent within sprint |
| **Scope control** | Fixed appetite + explicit in/out scope | Requirements spec (SRS) | Flexible within sprint goal |
| **Quality gate** | VBR (automated) + Reviewer role | Testing phase after coding | Definition of Done |
| **Knowledge capture** | Curator persists to `know` after each task | Maintenance phase docs | Retro notes (often lost) |
| **AI-native** | Yes — roles map to agents with scoped context | No — designed for human teams | No — ceremonies assume humans |
| **Abstraction management** | Explicit per-phase (this guide) | Implicit (Design→Code transition) | Not addressed |

### Where nowu Improves on Shape Up

Shape Up has three phases: Shaping → Betting → Building. Your workflow adds critical capabilities:

- **Architecture Analysis + Design Options**: Shape Up assumes senior shapers "just know" the right architecture. nowu makes this explicit with structured options and weighted evaluation.
- **VBR**: Shape Up has no built-in verification protocol. Quality is assumed. nowu's VBR makes it machine-checkable.
- **Curator/Capture**: Shape Up produces no durable knowledge artifacts. Lessons die with the cycle. nowu persists everything to `know`.
- **Approval Tiers**: Shape Up's "betting table" is binary (bet or don't). nowu's Tier 1/2/3 model allows low-risk work to flow while high-risk work blocks appropriately.

### Where SDLC Concepts Still Apply

SDLC's strength is its explicit design phases. Your workflow should adopt two SDLC concepts:

1. **HLD before LLD before Code**: The SDLC Design phase explicitly separates high-level design (system architecture) from low-level design (component logic). Your workflow does this implicitly — this guide makes it explicit.
2. **Requirements traceability**: SDLC traces every feature to a requirement. Your use-case IDs (NF-01, PK-03) already do this. Keep it.

---

## 2. Abstraction Levels (C4 Model + HLD/LLD)

### The Four Levels

| Level | C4 Equivalent | HLD/LLD | What It Shows | Who Needs It |
|-------|--------------|---------|---------------|-------------|
| **System Context** | Level 1 | HLD | nowu + `know` + external actors | Architect, stakeholders |
| **Module/Container** | Level 2 | HLD | `core`, `flow`, `bridge`, `soul`, `know` | Architect, Shaper |
| **Component** | Level 3 | LLD | `MemoryService`, `SessionManager`, contracts | Shaper, Implementer |
| **Code** | Level 4 | LLD→Code | Classes, functions, tests | Implementer, Reviewer |

### Key Insight: HLD ↔ LLD is Bidirectional

The testRigor analysis makes a critical point: discoveries during LLD can modify HLD. In your workflow, this means:
- If the Implementer discovers that a shaped task violates a module boundary, it should escalate back to the Shaper (or Architect).
- This is already captured in your Tier system — implementation discoveries that require architecture changes are Tier 3 escalations.

---

## 3. Context Scoping Per Workflow Phase

This is the core deliverable. Each phase should load ONLY the context relevant to its abstraction level.

### Phase 1-2: Intake + Architecture Analysis → System Context (C4 Level 1-2)

**Abstraction**: HLD — "What does the system do? How do modules interact?"

**Load**:
- `ARCHITECTURE.md` (module map, drivers, constraints)
- `DECISIONS.md` (existing architecture decisions)
- `V1_PLAN.md` (current step context)
- `WORKFLOW.md` Section 2-3 (loop + approval tiers)

**Do NOT load**:
- Source code files
- Individual test files
- Implementation details of any module

**Why**: The Architect needs the big picture. Loading code creates noise and causes the agent to anchor on existing implementation patterns rather than evaluating options objectively.

**Agent**: `nowu-architect` subagent with Read-only tools (no Write/Edit).

---

### Phase 3-4: Design Options + Evaluation → Module Level (C4 Level 2-3)

**Abstraction**: HLD → LLD transition — "What are the viable approaches? How do modules connect?"

**Load**:
- Everything from Phase 1-2
- `core/contracts/*.py` (interface definitions)
- Module `__init__.py` files (public API surface)
- Relevant ADR / decision entries

**Do NOT load**:
- Internal module implementation files
- Test implementation details
- Unrelated modules' code

**Why**: Design options need to understand the contracts between modules, but not how each module internally works. Loading internal implementations biases toward incremental changes rather than evaluating genuinely different approaches.

**Agent**: Still `nowu-architect`, but may use Grep/Glob to inspect contract files.

---

### Phase 5: Task Shaping → Component Level (C4 Level 3)

**Abstraction**: LLD — "What components need to change? What are the boundaries?"

**Load**:
- `core/contracts/*.py` (what interfaces exist)
- File tree of affected modules (`ls -R src/nowu/<module>/`)
- Existing test structure for affected modules
- `PROGRESS.md` (what's done, what's next)

**Do NOT load**:
- Architecture docs (decisions are already made at this point)
- Vision/soul docs
- Unrelated modules' internals

**Why**: The Shaper needs to understand the codebase structure to create realistic task boundaries. But architecture decisions are already settled — re-loading them invites re-litigation.

**Agent**: `nowu-shaper` subagent. Read-only + Bash for file exploration.

---

### Phase 6-7: Implementation + VBR → Code Level (C4 Level 4)

**Abstraction**: Code — "What classes/functions to write? Do tests pass?"

**Load**:
- ONLY files listed in the task's `scope` / `allowed_files`
- Related test files
- The specific contract being implemented
- `pyproject.toml` (tooling config)

**Do NOT load**:
- Architecture docs
- V1 plan
- Use cases document (55k chars!)
- Other modules' source code
- Progress tracking

**Why**: This is where context discipline matters most. The Implementer's context window should be almost entirely code + tests. Every non-code token displaces a code token. Anthropic's research confirms: "find the smallest possible set of high-signal tokens that maximize the likelihood of your desired outcome."

**Agent**: Main Claude Code session (not a subagent — needs iterative control).

**Implementation Protocol**:
1. Read the shaped task (scope + acceptance criteria)
2. Write failing test
3. Implement minimal code to pass
4. Run VBR: `pytest + mypy + ruff`
5. Refactor while green
6. Do NOT read architecture docs during this phase

---

### Phase 8: Review → Component + Code Level (C4 Level 3-4)

**Abstraction**: LLD + Code — "Does the implementation match the design? Are boundaries respected?"

**Load**:
- Changed files (git diff)
- Acceptance criteria from the shaped task
- `core/contracts/*.py` (verify interface compliance)
- Architecture rules (from `.claude/rules/architecture.md`)
- Test results

**Do NOT load**:
- Full architecture docs (rules summary is sufficient)
- V1 plan
- Unrelated modules

**Why**: The Reviewer needs fresh eyes on the code with just enough architectural context to catch boundary violations. Loading the full architecture document would be wasteful — the summarized rules in `.claude/rules/` are sufficient.

**Agent**: `nowu-reviewer` subagent (separate context window = fresh perspective).

---

### Phase 9: Capture & Close → System Context (C4 Level 1-2)

**Abstraction**: Back to HLD — "What did we decide? What did we learn?"

**Load**:
- `DECISIONS.md` (to check for duplicates before adding)
- `PROGRESS.md` (to update status)
- Git log of recent commits (what changed)
- The shaped task's acceptance criteria (what was the goal)

**Do NOT load**:
- Source code (decisions are about "what" and "why", not "how")
- Test files
- Architecture docs (unless a new decision contradicts existing ones)

**Why**: Curation operates at the system level. It captures decisions and lessons, not code. Loading code during curation causes the agent to write overly technical decision records that aren't useful for future architectural reasoning.

**Agent**: `nowu-curator` subagent (Write access to docs only, not source code).

---

## 4. The Context Scoping Principle

> **Load the minimum context at the right abstraction level for the current phase.**
> **If it's not relevant NOW, it's noise.**

This is consistent with three independent sources:

1. **Anthropic (official)**: "Find the smallest possible set of high-signal tokens that maximize the likelihood of your desired outcome." Context rot degrades performance as tokens increase.
2. **Chkk (Minimal Relevant Context)**: "Less but sharper beats more but messy every single time. Context quality determines outcome quality."
3. **C4 Model principle**: Different abstraction levels serve different audiences and decision points. Don't show code diagrams to the person making system-level decisions.

### Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Loading ARCHITECTURE.md during implementation | Agent re-litigates settled decisions | Architecture is decided in Phase 2, not Phase 6 |
| Loading USE_CASES.md (55k chars) into every phase | Consumes 40%+ of context budget with mostly irrelevant text | Reference by ID only (e.g., "implements NF-01") |
| Loading all source files during architecture analysis | Anchors on existing patterns, prevents novel solutions | Load only contracts and module boundaries |
| Loading vision/soul docs during code review | Reviewer starts philosophizing instead of checking tests | Load rules summary, not vision docs |
| Never clearing context between phases | Accumulated context from Phase 1 pollutes Phase 6 | Use subagents (fresh context) or explicit `/clear` |

---

## 5. Implementing This in Claude Code

### Subagent Context Isolation (Already Built)

Your Claude Code subagents naturally enforce context scoping because each runs in its own context window:

- `nowu-architect`: only has Read/Grep/Glob → can't accidentally edit code during analysis
- `nowu-shaper`: only has Read/Grep/Glob/Bash → explores structure but doesn't implement
- `nowu-reviewer`: only has Read/Grep/Glob/Bash → reviews but doesn't fix (separate concern)
- `nowu-curator`: only has Read/Write/Edit/Grep/Glob → writes docs but not source code

### Progressive Disclosure (Anthropic's Recommendation)

Don't pre-load everything. Let agents discover context through exploration:

```
# Instead of loading all architecture docs upfront:
"Read ARCHITECTURE.md Section 4.1 (Module Map) to understand the current module boundaries."

# Instead of loading all source code:
"Use Grep to find all imports of MemoryService across the codebase."

# Instead of loading the full use-cases doc:
"This task implements NF-01 (session recovery after context loss)."
```

### Future: `know` as Context Engine

When your MemoryService (Step 02) is implemented, `know` becomes the context scoping engine:

```python
# Phase-appropriate context retrieval
context = kb.subgraph(
    project="nowu",
    types=["DECISION", "TASK"],  # Only decisions and tasks, not code
    related_to="session-recovery",
    max_depth=2
).to_prompt(max_tokens=2000)
```

This is the endgame: `know` serves the right atoms at the right abstraction level, and `flow` orchestrates which level to request based on the current workflow phase.
