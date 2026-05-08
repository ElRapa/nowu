# Context Loading Strategy: Orchestrator-Aware Bootstrap Architecture

**Date:** 2026-05-08  
**For:** nowu orchestrator implementation session startup

---

## The Problem OmO Identified

**Current state:** Multiple bootstrap files (BOOTSTRAP.md, BOOTSTRAP_lean.md) load context at session start, then individual skills load additional context during execution.

**OmO's insight:** This creates duplication — bootstrap loads docs/DECISIONS.md, then a skill also loads docs/DECISIONS.md. Better to push context loading entirely into skills and make bootstrap files minimal routing documents.

**Your concern:** "I don't really know which files are relevant" for the orchestrator implementation session.

**The deeper issue:** Context scoping should be **altitude-aware**, not just step-aware. The current system optimizes for S1-S9 (DELIVERY/EXECUTION altitude) but doesn't have clear guidance for STRATEGIC/IMPLEMENTATION work like implementing the orchestrator layer.

---

## Three Context-Loading Architectures Evaluated

### Option A: Skill-Only (OmO's Recommendation)

**Structure:**
```
BOOTSTRAP.md            → minimal routing doc (which skill to invoke)
.claude/skills/
  ├── full-cycle.md     → loads intake + S1-S9 context per step
  ├── synthesis.md      → loads vision, goals, UCs, decisions, arch docs
  ├── orchestrator.md   → NEW: loads orchestrator-specific context
  └── ...
```

**Context loading:** 100% in skill files, bootstrap just routes.

**Pros:**
- Eliminates duplication between bootstrap and skills
- Single source of truth for "what context does X work need?"
- Skills can be versioned/evolved independently

**Cons:**
- Bootstrap becomes **too thin** — loses its value as orientation document
- New AI agents don't know which skill to invoke without reading all skill files first
- "Which skill do I need?" becomes a chicken-and-egg problem

**Verdict:** Good for **routine work** (S1-S9 execution), weak for **initial orientation** or **novel work types** (like implementing orchestrator).

---

### Option B: Altitude-Stratified Bootstrap (Recommended)

**Structure:**
```
BOOTSTRAP.md                        → routing index (which bootstrap to use)
BOOTSTRAP-STRATEGIC.md              → loads docs for STRATEGIC/PRODUCT altitude work
BOOTSTRAP-ARCHITECTURE.md           → loads docs for ARCHITECTURE altitude work
BOOTSTRAP-DELIVERY.md               → loads docs for DELIVERY/EXECUTION altitude work
BOOTSTRAP-RETROSPECTIVE.md          → loads docs for GAP/health/learning work

.claude/skills/
  ├── full-cycle.md                 → references BOOTSTRAP-DELIVERY
  ├── synthesis.md                  → references BOOTSTRAP-STRATEGIC + BOOTSTRAP-ARCHITECTURE
  ├── orchestrator-implement.md     → NEW: references BOOTSTRAP-ARCHITECTURE
  └── ...
```

**Context loading:** Bootstrap loads **altitude-common** context (vision, decisions, model), skills load **step-specific** context (task specs, in_scope_files).

**How it works:**
1. User picks altitude: "I'm implementing the orchestrator (ARCHITECTURE altitude)"
2. Read BOOTSTRAP-ARCHITECTURE.md first (loads arch docs, ADRs, DECISIONS, containers.md, MODEL-REFERENCE)
3. Then invoke skill: `orchestrator-implement` (loads only orchestrator-specific context on top)

**Pros:**
- Bootstrap remains meaningful (orientation + common context)
- Skills remain lean (only step-specific context)
- Altitude-aware scoping prevents loading irrelevant context
- AI agents can reason: "I'm doing STRATEGIC work → read BOOTSTRAP-STRATEGIC first"

**Cons:**
- More bootstrap files to maintain (4 instead of 2)
- Requires discipline to keep altitude boundaries clean

**Verdict:** Best balance of orientation value and context precision. Maps directly to the 5×10 model.

---

### Option C: Modular Bootstrap with Dynamic Includes (Advanced)

**Structure:**
```
BOOTSTRAP.md                        → orchestration logic + skill routing
.claude/bootstrap-modules/
  ├── 00-core-identity.md           → vision, goals (always load)
  ├── 01-workflow-model.md          → MODEL-REFERENCE, WORKFLOW-STANDARDS (always load)
  ├── 02-decisions.md               → DECISIONS.md (always load)
  ├── 10-strategic-context.md       → vision, goals, UCs (STRATEGIC altitude)
  ├── 20-architecture-context.md    → containers, ADRs, SYNTHESIS, Arch Vision (ARCHITECTURE)
  ├── 30-delivery-context.md        → WORKFLOW-DETAILED, state/tasks/ (DELIVERY/EXECUTION)
  ├── 40-retrospective-context.md   → health reports, GAP outputs (RETROSPECTIVE)

.claude/skills/orchestrator-implement.md:
  includes: [00-core-identity, 01-workflow-model, 02-decisions, 20-architecture-context]
```

**Context loading:** Bootstrap is a **module registry**; skills declare which modules they need.

**How it works:**
1. Skill file declares: `includes: [00-core-identity, 20-architecture-context]`
2. AI agent reads those bootstrap modules in sequence
3. Then reads skill-specific instructions

**Pros:**
- Maximum composability (skills mix and match modules)
- No duplication (each doc segment defined once)
- Easy to add new context modules without touching existing files

**Cons:**
- Most complex to implement
- Requires tooling or discipline to enforce `includes` declarations
- Harder for humans to read (context is scattered across many small files)

**Verdict:** Over-engineered for current nowu scale. Consider for v2 when you have 50+ skills.

---

## Recommendation: Option B (Altitude-Stratified Bootstrap)

### Implementation

#### 1. Replace BOOTSTRAP.md with Routing Index

```markdown
# nowu Bootstrap — Session Start Routing

You are helping develop the nowu framework. **Choose the bootstrap that matches your work altitude:**

| Altitude | Bootstrap File | Use When |
|---|---|---|
| **STRATEGIC** | `BOOTSTRAP-STRATEGIC.md` | Vision, goals, roadmap, SYNTHESIS, Architecture Vision |
| **PRODUCT** | `BOOTSTRAP-STRATEGIC.md` | Use case discovery, P0-P4 pre-workflow |
| **ARCHITECTURE** | `BOOTSTRAP-ARCHITECTURE.md` | ADRs, module design, contracts, hypothesis ADRs, orchestrator implementation |
| **DELIVERY** | `BOOTSTRAP-DELIVERY.md` | S1-S9 workflow execution, task shaping, implementation loops |
| **EXECUTION** | `BOOTSTRAP-DELIVERY.md` | Code, tests, S6-S7 implementation, S8 review |
| **RETROSPECTIVE** | `BOOTSTRAP-RETROSPECTIVE.md` | GAP analysis, health checks, session learnings |

If you are unsure which altitude you are in:
- Read `docs/model/MODEL-REFERENCE.md` → "Altitude × Phase Examples" table
- Or start with `BOOTSTRAP-STRATEGIC.md` (most general)

For continuation sessions where you already have full context, see `BOOTSTRAP_lean.md`.
```

#### 2. Create BOOTSTRAP-STRATEGIC.md

```markdown
# nowu Bootstrap — STRATEGIC/PRODUCT Altitude

**Use this for:** Vision, goals, roadmap, SYNTHESIS, Architecture Vision, P0-P4 pre-workflow.

## Read in this exact order

### Core Identity (always)
1. `docs/vision.md`                        — what IS nowu, who is it for
2. `docs/goals/goal-*.md`                  — time-horizoned goals
3. `docs/USE_CASES.md`                     — 50 approved use cases

### Workflow Model (always)
4. `docs/model/MODEL-REFERENCE.md`         — 5×10 altitude-phase model
5. `docs/model/WORKFLOW-STANDARDS.md`      — binding workflow rules

### Decisions (always)
6. `docs/DECISIONS.md`                     — D-001 through D-022 (binding)

### Strategic Context (altitude-specific)
7. `docs/STAGED-PLAN.md` OR `docs/ROADMAP-NNN.md`  — implementation roadmap
8. `CLAUDE.md`                             — commands, approval tiers

### If Doing SYNTHESIS or Architecture Vision
9. `state/arch/SYNTHESIS-NNN.md` (if exists) — prior SYNTHESIS output
10. `state/arch/ARCHITECTURE-VISION.md` (if exists) — prior Arch Vision

### If Doing P0-P4 Pre-Workflow
11. `docs/PRE-WORKFLOW.md`                 — P0-P4 specification
12. `state/ideas/` — run `ls`              — see what ideas exist

## Confirm Understanding
1. What is nowu's product vision and who is it for?
2. What are the 5 altitudes? Which one are you in now?
3. What is the current roadmap stage and what's the critical path?
4. What are the approval tiers (Tier 1/2/3) and give one example of each?

## Then wait for user approval before touching files.
```

#### 3. Create BOOTSTRAP-ARCHITECTURE.md

```markdown
# nowu Bootstrap — ARCHITECTURE Altitude

**Use this for:** ADRs, module design, contracts, hypothesis ADRs, orchestrator implementation.

## Read in this exact order

### Core Identity (minimal)
1. `docs/vision.md`                        — product vision (read Section 1 only)

### Workflow Model (always)
2. `docs/model/MODEL-REFERENCE.md`         — 5×10 altitude-phase model
3. `docs/model/WORKFLOW-STANDARDS.md`      — binding workflow rules

### Decisions (always)
4. `docs/DECISIONS.md`                     — D-001 through D-022 (binding)

### Architecture Context (altitude-specific)
5. `docs/architecture/containers.md`       — module map (C4 L2)
6. `docs/architecture/context.md`          — system context (C4 L1)
7. `docs/architecture/adr/` — run `ls`     — list all ADRs
8. `docs/architecture/adr/ADR-0001..0010.md` — read accepted ADRs (status: ACCEPTED)

### Strategic Context (for alignment)
9. `docs/STAGED-PLAN.md` OR `docs/ROADMAP-NNN.md` — current roadmap
10. `state/arch/SYNTHESIS-001.md` (if exists) — architectural themes
11. `state/arch/ARCHITECTURE-VISION.md` (if exists) — architectural principles, risks

### Tools & Verification
12. `CLAUDE.md`                            — commands, approval tiers
13. `docs/model/VERIFICATION-GUIDE.md`     — how to verify ADRs

## What You NEVER Load at This Altitude
- `src/` or `tests/` — no code during architecture work (prevents anchoring bias)
- `state/tasks/` — no implementation tasks (architecture precedes shaping)
- `state/sessions/` — no session state (architecture is project-level)

## Confirm Understanding
1. What are the 5 modules (core, flow, bridge, soul, know) and their import rules?
2. What are the binding ADRs (ADR-0001 through ADR-0010) and their status?
3. What is the current roadmap stage and what architectural work is on the critical path?
4. What are the approval tiers for architecture work? (Hint: new ADRs are Tier 3)

## Then wait for user approval before touching files.
```

#### 4. Create BOOTSTRAP-DELIVERY.md

```markdown
# nowu Bootstrap — DELIVERY/EXECUTION Altitude

**Use this for:** S1-S9 workflow execution, task shaping, implementation loops, S6-S7 code, S8 review.

## Read in this exact order

### Workflow Model (always)
1. `docs/WORKFLOW.md`                      — S1-S9 reference table
2. `docs/model/MODEL-REFERENCE.md`         — 5×10 altitude-phase model
3. `docs/model/WORKFLOW-STANDARDS.md`      — binding workflow rules

### Architecture Context (alignment only)
4. `docs/architecture/containers.md`       — module map (C4 L2)
5. `docs/DECISIONS.md`                     — D-001 through D-022 (binding)

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
```

#### 5. Create BOOTSTRAP-RETROSPECTIVE.md

```markdown
# nowu Bootstrap — RETROSPECTIVE Altitude

**Use this for:** GAP analysis (G0-G2), health checks, session learnings, drift detection.

## Read in this exact order

### Workflow Model (always)
1. `docs/model/MODEL-REFERENCE.md`         — 5×10 altitude-phase model (focus on RETROSPECTIVE)
2. `docs/model/WORKFLOW-STANDARDS.md`      — epistemic grades, artifact standards

### Strategic Context (for alignment)
3. `docs/vision.md`                        — product vision (reference for drift detection)
4. `docs/DECISIONS.md`                     — D-001 through D-022 (check for violations)

### Retrospective Context (altitude-specific)
5. `state/health/` — run `ls`              — health check reports
6. `state/arch/gap-*.md` — run `ls`        — prior GAP analysis outputs
7. `state/learnings/INDEX.md`              — running index of session learnings

### Evidence Gathering (for pattern detection)
8. `state/tasks/` — run `ls`               — task statuses (for blocked/deferred patterns)
9. `state/sessions/` — run `ls`            — session bookmarks (for handoff quality)
10. `git log --oneline -20`                — recent commits (for drift detection)

### Tools
11. `CLAUDE.md`                            — commands (especially /health-check)

## Confirm Understanding
1. What is the RETROSPECTIVE altitude and how does it differ from EXECUTION?
2. What are the three GAP steps (G0, G1, G2)?
3. What health check categories exist? (architecture, workflow, knowledge, quality)
4. What is the epistemic grade scale and when does grade improve?

## Then wait for user approval before touching files.
```

#### 6. Update BOOTSTRAP_lean.md to Reference Altitude-Stratified Bootstraps

```markdown
# nowu Bootstrap — Lean Session Start Prompt

> Use this for follow-up sessions on a project where you already have full context.
> For a brand-new session, use altitude-specific bootstrap (see BOOTSTRAP.md routing index).

---

You are continuing work on the nowu framework. **If you need to refresh context, read the altitude-specific bootstrap:**
- STRATEGIC/PRODUCT: `BOOTSTRAP-STRATEGIC.md`
- ARCHITECTURE: `BOOTSTRAP-ARCHITECTURE.md`
- DELIVERY/EXECUTION: `BOOTSTRAP-DELIVERY.md`
- RETROSPECTIVE: `BOOTSTRAP-RETROSPECTIVE.md`

Otherwise, proceed directly to your skill invocation.

## Minimal Refresh (if needed)

1. `CLAUDE.md`                           — commands, approval tiers
2. `docs/model/MODEL-REFERENCE.md`       — 5×10 altitude-phase model
3. `docs/DECISIONS.md`                   — check for new decisions since last session
4. `docs/STAGED-PLAN.md` OR `docs/ROADMAP-NNN.md` — current roadmap

## Health Check (if unsure)
```
/health-check all
```

If any returns RED, tell me before proceeding.

## Confirm Understanding
1. What altitude are you working in? (STRATEGIC, ARCHITECTURE, DELIVERY, RETROSPECTIVE)
2. What is the current roadmap stage and active work item?
3. Are there any BLOCKED or CHANGES_REQUESTED items in state/tasks/?

## Then wait for user approval before touching files.
```

---

## How to Start the Orchestrator Implementation Session

### Step 1: Choose the Right Bootstrap

You are implementing the orchestrator layer (3 meta-agents + ROADMAP versioning). This is **ARCHITECTURE altitude** work — you are defining new agents, new artifact types, and new contracts. You are NOT executing S1-S9 workflow or writing code yet.

**Read:** `BOOTSTRAP-ARCHITECTURE.md`

### Step 2: Invoke the Right Skill

After reading the architecture bootstrap, invoke:

**Skill:** `orchestrator-implement` (NEW — create this skill)

**Or fall back to:** `architecture-only` skill (if it exists) with explicit focus on orchestrator

### Step 3: Context the Skill Should Load (On Top of Bootstrap)

The skill should load:
1. **Orchestrator research report** (the one I just created in this session)
2. **Orchestrator agent definitions** (roadmap-creator.md, roadmap-updater.md, work-scheduler.md)
3. **MODEL-REFERENCE orchestrator update section** (what to add to MODEL-REFERENCE.md)
4. **Current STAGED-PLAN.md** (to understand what becomes ROADMAP-002.md)

**What the skill should NOT load:**
- `src/` or `tests/` (no code — orchestrator is agent/artifact work, not Python modules)
- `state/tasks/` (no implementation tasks — orchestrator is project-level, not task-level)
- `state/sessions/` (not relevant to architecture work)

---

## Answer to "Which Files Are Relevant?"

For implementing the orchestrator layer specifically:

### Required Context (Read First)
1. `docs/vision.md` — Section 1 only (product identity)
2. `docs/model/MODEL-REFERENCE.md` — 5×10 model (you are adding orchestrator layer to this)
3. `docs/model/WORKFLOW-STANDARDS.md` — artifact standards, epistemic grades
4. `docs/DECISIONS.md` — D-001 through D-022 (binding)
5. `docs/architecture/containers.md` — module map (orchestrator is NOT a module, it's external)
6. `docs/architecture/adr/ADR-0007..0010.md` — session continuity, atom model, orchestration, grades
7. `docs/STAGED-PLAN.md` — current roadmap (will become ROADMAP-002.md)

### Orchestrator-Specific Context (Read Second)
8. Orchestrator research report (from this Perplexity session)
9. Orchestrator agent definitions (3 files)
10. MODEL-REFERENCE orchestrator update section
11. Orchestrator package README

### NOT Relevant (Skip These)
- `src/`, `tests/` — no code changes for orchestrator implementation
- `state/tasks/` — orchestrator is project-level, not task-level
- `state/sessions/` — not relevant to architecture work
- `docs/WORKFLOW-DETAILED.md` — S1-S9 narrative (orchestrator is external to S1-S9)
- `.claude/rules/code-style.md` — no code being written
- `.claude/rules/testing.md` — no tests being written yet

---

## Final Recommendation: Hybrid Approach

**For this specific session (orchestrator implementation):**

1. **Start prompt:** "Read BOOTSTRAP-ARCHITECTURE.md, then I will give you orchestrator-specific context."
2. **After bootstrap confirmation:** Attach the 5 orchestrator files (research report + 3 agents + update section + README) `docs/research/sessions/2026-05-08_1_perplexity_orchestrator/` and say "Now read these files for your orchestrator implementation work."
3. **Then say:** "Your work: integrate the orchestrator layer into nowu. This means:
   - Create 3 agent definitions in `.claude/agents/orchestrator/`
   - Update `docs/model/MODEL-REFERENCE.md` with orchestrator section
   - Add D-022 to `docs/DECISIONS.md`
   - Rename `STAGED-PLAN.md` → `ROADMAP-002.md` with proper frontmatter
   - Update `AGENTS.md` session entry table to include `orchestrator-implement` skill"

**For future sessions (general pattern):**

1. Implement altitude-stratified bootstraps (Option B) as described above
2. Update `.claude/skills/` to reference altitude-specific bootstraps
3. Create skill-specific context loading in each skill file (only step-specific context on top of bootstrap)

This gives you:
- ✅ Meaningful bootstraps (orientation + altitude-common context)
- ✅ Lean skills (only step-specific context)
- ✅ Clear routing ("I'm doing architecture work → read BOOTSTRAP-ARCHITECTURE")
- ✅ No duplication (bootstrap loads common, skill loads specific)
- ✅ AI-buildable (clear rules for what to load when)
