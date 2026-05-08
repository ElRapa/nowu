
## Create a comprehensive mock workflow walkthrough document showing:

 1. Full 5-altitude × 9-phase traversal from "I want autonomous assistant software" to shipped code
 2. What artifacts are created at each step
 3. Where human interaction is needed
 4. The GOAL→UC→??? gap analysis
 5. Epistemic grades integration
 6. Security phase consideration

---

# nowu Workflow Model: Complete Mock Traversal

**Starting prompt (human):** "I want to make a software which serves as an almost autonomous assistant for everything I want to do. Small tasks and big projects."

---

## Part 1: The Full Altitude Descent (Human Prompt → Shipped Code)

### ALTITUDE 0: GOVERNANCE (one-time, human-approved)

*This altitude exists but is pre-existing for this traversal — vision.md is already APPROVED.*

| Phase | Agent | Input | Output Artifact | Human Gate | Epistemic Grade |
|---|---|---|---|---|---|
| IDEA | (skip — vision exists) | - | - | - | - |
| PROBLEM | (skip — vision exists) | - | - | - | - |
| ... | All phases skipped | - | `vision.md` (existing) | APPROVED | VERIFIED_FACT (ratified) |

**Key artifact:** `vision.md` (already exists, status: APPROVED)

---

### ALTITUDE 1: STRATEGIC

#### Phase 1.1: STRATEGIC/IDEA

**Agent:** `strategic-idea-generator`  
**Input:** Human prompt + `vision.md`  
**Output:** `IDEA-001.md`

```yaml
artifact_class: knowledge
artifact_type: IDEA
origin_altitude: STRATEGIC
origin_phase: IDEA
consumer_altitudes: [STRATEGIC, PRODUCT]
epistemic_grade: SPECULATION
grade_justification: "Raw human prompt; no research or validation yet"
```

**Content:**
- Raw signal: "autonomous assistant for everything"
- Initial interpretation: System that handles both small tasks (todos, reminders) and big projects (software dev, business ops)
- Ambiguities flagged: What is "everything"? What domains? What autonomy level?

**Human gate:** NONE (ideas are captured, not approved)

---

#### Phase 1.2: STRATEGIC/PROBLEM

**Agent:** `strategic-problem-synthesizer`  
**Input:** `IDEA-001.md` + `vision.md` (alignment check)  
**Output:** `PROBLEM-009.md` (new — this is strategic problem)

```yaml
artifact_class: knowledge
artifact_type: PROBLEM
origin_altitude: STRATEGIC
origin_phase: PROBLEM
consumer_altitudes: [STRATEGIC, PRODUCT, ARCHITECTURE]
epistemic_grade: HYPOTHESIS
grade_justification: "Synthesized from vision.md + user prompt; no external validation"
```

**Content:**
- **Problem statement:** "Existing AI tools work well in individual sessions but lose continuity across sessions and projects. Users need a system that maintains direction, decisions, and memory — not just executes tasks."
- **Why this matters strategically:** Aligns with vision.md principle 1 (memory is infrastructure) and 6-month horizon (90%+ AI-handled work ratio)
- **Constraint:** Must work for both software and non-software domains

**Human gate:** REVIEW (lightweight — human confirms this is the right strategic problem)

**→ Human approves. Continue.**

---

#### Phase 1.3: STRATEGIC/ANALYSIS

**Agent:** `strategic-analyst`  
**Input:** `PROBLEM-009.md` + market research trigger  
**Output:** `ANALYSIS-009-strategic.md`

```yaml
artifact_class: workflow_phase
altitude: STRATEGIC
phase: ANALYSIS
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Based on 5 comparable systems (Cursor, Aider, AutoGPT, LangChain, Temporal) + Guo et al. survey; no production usage data for nowu specifically"
```

**Content:**
- **Comparable systems:** Cursor (session-based, no memory), AutoGPT (autonomous but no human direction), LangChain (framework not product)
- **Gap identified:** No existing system combines long-term memory + multi-project tracking + altitude-aware workflow
- **Strategic risk:** Market may consolidate around one big player (GitHub Copilot Workspace) before nowu reaches product-market fit
- **Opportunity:** Non-software use cases are completely unserved

**Human gate:** NONE (analysis informs next phase)

---

#### Phase 1.4: STRATEGIC/OPTIONS

**Agent:** `strategic-options-generator`  
**Input:** `ANALYSIS-009-strategic.md` + `PROBLEM-009.md`  
**Output:** `OPTIONS-009-strategic.md`

```yaml
artifact_class: workflow_phase
altitude: STRATEGIC
phase: OPTIONS
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Options derived from analysis + vision principles; no prototype testing"
```

**Content (3 strategic options):**

**Option A: Framework-first (Ship as installable Python package)**
- 6-month goal: CLI tool + documentation
- Pros: Fastest to ship, developer-friendly, no infrastructure
- Cons: High friction for non-technical users, no GUI

**Option B: Product-first (Ship as hosted service)**
- 6-month goal: Web app + agent orchestration
- Pros: Lowest friction, wider audience
- Cons: Infrastructure cost, deployment complexity

**Option C: Hybrid (CLI in v1-core, web UI in v1)**
- 6-month goal: Working CLI that proves the workflow, GUI comes after
- Pros: Validates workflow before scaling, keeps scope manageable
- Cons: Deferred user experience work

**Human gate:** DECISION REQUIRED (strategic bet)

**→ Human selects Option C (Hybrid approach). Rationale recorded.**

---

#### Phase 1.5: STRATEGIC/DECISION

**Agent:** `strategic-decider`  
**Input:** `OPTIONS-009-strategic.md` + human selection  
**Output:** `GOAL-004.md` (new strategic goal)

```yaml
artifact_class: knowledge
artifact_type: GOAL
origin_altitude: STRATEGIC
origin_phase: DECISION
consumer_altitudes: [PRODUCT, ARCHITECTURE, DELIVERY, EXECUTION]
epistemic_grade: EVIDENCE_BASED
grade_justification: "Decision backed by analysis of 5 comparable systems + vision alignment; Option C selected deliberately over alternatives"
status: ACTIVE
```

**Content:**
```markdown
## Goal: Ship v1-core as functional CLI workflow by 6-month horizon

**What:** A working command-line interface that demonstrates the full nowu workflow (P0-P4, S1-S9, GAP) for software projects.

**Why:** Validates the core workflow model before investing in GUI/hosting infrastructure. Aligns with vision.md 6-month horizon: "90-99% AI-handled work, low friction."

**Success criteria:**
- nowu can build itself using nowu (dogfooding)
- All 9 workflow phases are implemented and testable
- At least one non-software project (AP or RE) runs through the workflow successfully

**Out of scope (deferred to v1):**
- Web interface
- Hosted service
- Multi-user collaboration

**Rejected alternatives:**
- Framework-only: Too high friction for persona (Raphael needs low overhead)
- Product-first: Too much scope for 6 months; workflow must be proven first
```

**Human gate:** APPROVAL (strategic goal must be ratified)

**→ Human approves GOAL-004. Marks `status: APPROVED`.**

---

#### Phase 1.6-1.9: STRATEGIC/EVALUATION, IMPLEMENTATION, VERIFICATION, LEARN

**Skip for strategic altitude** — these phases apply to execution work, not strategic decisions. Strategic decisions are "implemented" by being decomposed into product-level work.

**Downward transition rule:** STRATEGIC/DECISION outputs (`GOAL-004.md`) become inputs to PRODUCT altitude.

---

### ALTITUDE 2: PRODUCT

#### Phase 2.1: PRODUCT/IDEA

**Agent:** `product-idea-extractor`  
**Input:** `GOAL-004.md` + `vision.md` (persona: Raphael)  
**Output:** `IDEA-010.md`, `IDEA-011.md`, `IDEA-012.md` (multiple product ideas from one strategic goal)

```yaml
artifact_class: knowledge
artifact_type: IDEA
origin_altitude: PRODUCT
origin_phase: IDEA
consumer_altitudes: [PRODUCT, ARCHITECTURE]
epistemic_grade: SPECULATION
grade_justification: "Unpacking strategic goal into product-level signals; no user research yet"
```

**Content (3 product ideas extracted):**
- `IDEA-010`: "Raphael needs to resume work after 3-day gap without re-reading session history"
- `IDEA-011`: "Raphael wants to switch between AP (food) and nowu (software) projects without cross-contamination"
- `IDEA-012`: "Raphael needs to approve/reject AI decisions from his phone while commuting"

**Human gate:** NONE (ideas are input to problem validation)

---

#### Phase 2.2: PRODUCT/PROBLEM

**Agent:** `product-problem-validator`  
**Input:** `IDEA-010`, `IDEA-011`, `IDEA-012` + persona research  
**Output:** `PROBLEM-010.md` (consolidated product problem)

```yaml
artifact_class: knowledge
artifact_type: PROBLEM
origin_altitude: PRODUCT
origin_phase: PROBLEM
consumer_altitudes: [PRODUCT, ARCHITECTURE, DELIVERY]
epistemic_grade: HYPOTHESIS
grade_justification: "Validated against persona (Raphael) and vision.md use cases; no real user interviews yet"
```

**Content:**
```markdown
## Problem: Context loss across sessions and projects

**For whom:** Raphael (primary persona) — runs 3-6 concurrent projects, switches context frequently, uses AI for 80%+ of work

**The pain:** After a 2-3 day gap, resuming a project requires 15-30 minutes of re-reading session artifacts to rebuild context. When switching between projects, there's no fast way to verify "am I working on the right problem at the right altitude?"

**Current workarounds:** 
- Manual note-taking in Obsidian (friction, not AI-readable)
- Re-reading entire SESSION-STATE.md (high cognitive load)
- Asking Claude to "summarize what we were doing" (unreliable, no memory)

**Why it matters:** Breaks flow, wastes AI and human time, increases risk of altitude drift

**Evidence:** Observed in session-review-2026-04-08 (problem-005.md); present in all 3 active projects (nowu, AP, RE)
```

**Human gate:** VALIDATION (human confirms this is a real problem they experience)

**→ Human confirms. Problem validated.**

---

#### Phase 2.3: PRODUCT/ANALYSIS

**Agent:** `product-analyst`  
**Input:** `PROBLEM-010.md` + competitive research  
**Output:** `ANALYSIS-010-product.md`

```yaml
artifact_class: workflow_phase
altitude: PRODUCT
phase: ANALYSIS
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Based on 8 comparable tools (Notion AI, Obsidian+AI plugins, Mem.ai, Rewind, Cursor Projects); no user testing with Raphael yet"
```

**Content:**
- **Existing solutions:** Notion AI (no workflow structure), Mem.ai (memory but no execution), Cursor Projects (single-project, code-only)
- **Gap:** No tool combines structured workflow + cross-project memory + AI execution
- **Key insight:** The "resume context" problem and the "which altitude am I at?" problem are the same problem — both require **machine-readable workflow position**
- **Design implication:** Artifacts need explicit `altitude` + `phase` metadata (connects to idea-004)

**Human gate:** NONE (analysis informs options)

---

#### Phase 2.4: PRODUCT/OPTIONS

**Agent:** `product-options-generator`  
**Input:** `ANALYSIS-010-product.md` + `PROBLEM-010.md`  
**Output:** `OPTIONS-010-product.md`

```yaml
artifact_class: workflow_phase
altitude: PRODUCT
phase: OPTIONS
epistemic_grade: HYPOTHESIS
grade_justification: "Options derived from analysis; no user testing or prototyping"
```

**Content (3 product solutions):**

**Option A: Human-readable resume-context command**
- Command: `nowu resume [project]`
- Output: 5-line plain English summary of current position
- Pros: Minimal implementation, human-friendly
- Cons: AI cannot use this; still requires human interpretation

**Option B: Machine-readable workflow position metadata**
- Every artifact gets `altitude:` + `phase:` frontmatter
- AI reads metadata to know position without parsing content
- Pros: Solves both human and AI context problem; enables validation
- Cons: Requires frontmatter migration for ~55 existing files

**Option C: Hybrid (B + visual status dashboard)**
- Metadata (Option B) + web dashboard showing project health/position
- Pros: Best UX, supports both CLI and future GUI
- Cons: Highest implementation cost; dashboard is out of v1-core scope

**Human gate:** DECISION REQUIRED (product direction)

**→ Human selects Option B (metadata-first). Rationale: solves root cause, aligns with idea-004, dashboard can come later.**

---

#### Phase 2.5: PRODUCT/DECISION

**Agent:** `product-decider`  
**Input:** `OPTIONS-010-product.md` + human selection  
**Output:** `USE-CASE-NF-16.md` (new use case)

```yaml
artifact_class: knowledge
artifact_type: USE_CASE
id: NF-16
origin_altitude: PRODUCT
origin_phase: DECISION
consumer_altitudes: [ARCHITECTURE, DELIVERY, EXECUTION]
epistemic_grade: EVIDENCE_BASED
grade_justification: "Decision backed by problem validation + analysis of 8 tools + alignment with idea-004 (2D altitude/phase model already in draft)"
status: READY_FOR_ARCHITECTURE
```

**Content:**
```markdown
## NF-16: Machine-Readable Workflow Position

**User story:** As an AI agent resuming work on a project, I need to know my current altitude and phase without parsing artifact content, so I can apply the correct reasoning mode and avoid altitude drift.

**Acceptance criteria:**
- Every workflow artifact contains `altitude:` and `phase:` in YAML frontmatter
- Every knowledge artifact contains `origin_altitude:` and `consumer_altitudes:`
- CLI command `nowu status` reads metadata and outputs current position in <2 seconds
- Circuit breaker: agent producing artifact at wrong altitude triggers validation error

**Dependencies:**
- idea-004 (2D altitude/phase model) must be finalized before implementation
- Requires ARCHITECTURE/DECISION to define metadata schema

**Out of scope:**
- Visual dashboard (deferred to v1)
- Retroactive migration of existing artifacts (v1-core only enforces going forward)
```

**Human gate:** APPROVAL (use case must be ratified before architecture work begins)

**→ Human approves NF-16. Marks `status: APPROVED`.**

---

#### Phase 2.6-2.9: PRODUCT/EVALUATION, IMPLEMENTATION, VERIFICATION, LEARN

**Skip** — product altitude doesn't implement; it defines what to build. Transition to ARCHITECTURE altitude.

---

## THE CRITICAL GAP: GOAL → USE CASE → ???

**You asked: "Can we jump directly to epics and todos? Is there a global solution shape needed first?"**

**Answer: NO, you cannot jump from USE-CASE to DELIVERY (epics/todos) for cross-module work.**

### Why the Gap Exists

`USE-CASE-NF-16` says **what** (machine-readable workflow position) but not **how** (which modules change, what data structures, what new contracts).

For **single-module changes** (e.g., add a field to one agent's prompt), you could skip ARCHITECTURE and go straight to DELIVERY/SHAPING.

For **cross-module changes** (this affects `core`, `flow`, `know`, all agents), you **must** pass through ARCHITECTURE altitude to:
1. Decide structural approach (where does the metadata live? Who validates it?)
2. Create ADRs (binding decisions about module boundaries)
3. Generate C4 diagrams (communication model between modules)
4. Define contracts (Protocol definitions in `core/contracts.py`)

### The Missing Layer: ARCHITECTURE/PROBLEM → ARCHITECTURE/DECISION

Let me continue the traversal to show what happens...

---

### ALTITUDE 3: ARCHITECTURE

#### Phase 3.1: ARCHITECTURE/IDEA

**Agent:** `architecture-idea-generator`  
**Input:** `USE-CASE-NF-16` + existing architecture docs (ARCHITECTURE.md, ADRs 1-6)  
**Output:** `IDEA-013.md`

```yaml
artifact_class: knowledge
artifact_type: IDEA
origin_altitude: ARCHITECTURE
origin_phase: IDEA
consumer_altitudes: [ARCHITECTURE, DELIVERY]
epistemic_grade: SPECULATION
grade_justification: "Initial architectural intuition; no structured tradeoff analysis yet"
```

**Content:**
- Metadata could live in: (a) artifact frontmatter, (b) separate index file, (c) database
- Validation could be: (a) git pre-commit hook, (b) agent-side check, (c) orchestrator enforcement
- This affects: `core` (contracts), `flow` (orchestration), `bridge` (CLI command), all agents (must read/write metadata)

**Human gate:** NONE

---

#### Phase 3.2: ARCHITECTURE/PROBLEM

**Agent:** `architecture-problem-framer`  
**Input:** `IDEA-013` + `USE-CASE-NF-16` + existing ADRs  
**Output:** `PROBLEM-011.md`

```yaml
artifact_class: knowledge
artifact_type: PROBLEM
origin_altitude: ARCHITECTURE
origin_phase: PROBLEM
consumer_altitudes: [ARCHITECTURE, DELIVERY]
epistemic_grade: HYPOTHESIS
grade_justification: "Architectural problem framing; validated against existing ADR constraints but not prototyped"
```

**Content:**
```markdown
## Architectural Problem: No Formal Workflow Position Contract

**Context:** USE-CASE-NF-16 requires altitude+phase metadata on every artifact. Currently this is informal (some artifacts have it, most don't; no validation).

**The architectural tension:**
1. Metadata must be readable by all agents → suggests `core/contracts.py` (ADR-0001)
2. Metadata must be validated at workflow gates → suggests `flow` orchestrator
3. Validation must not require code changes when adding new phases → suggests data-driven schema

**Constraints (from existing ADRs):**
- ADR-0001: Cross-module contracts belong in `core/contracts.py`
- ADR-0006: `flow` and `soul` communicate via artifacts, not runtime calls
- Metadata must work in v1-core (CLI-only, no orchestrator yet)

**Why this is hard:** v1-core has no orchestrator — agents are invoked manually by human via CLI. Validation must be opt-in (so it doesn't block work) but loud (so violations are visible).
```

**Human gate:** REVIEW (human confirms this is the right architectural problem to solve)

**→ Human confirms. Continue.**

---

#### Phase 3.3: ARCHITECTURE/ANALYSIS

**Agent:** `architecture-analyst`  
**Input:** `PROBLEM-011` + research on metadata validation patterns  
**Output:** `ANALYSIS-011-architecture.md`

```yaml
artifact_class: workflow_phase
altitude: ARCHITECTURE
phase: ANALYSIS
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Based on 4 comparable patterns (LangChain state, Temporal workflow metadata, OpenTelemetry spans, Palantir Ontology provenance); no nowu-specific prototype"
```

**Content:**
- **Pattern 1 (LangChain):** State dictionary passed between agents; validated at orchestrator
- **Pattern 2 (Temporal):** Workflow metadata attached to every activity; queryable via API
- **Pattern 3 (OpenTelemetry):** Span attributes; validation via semantic conventions
- **Pattern 4 (Palantir):** Ontology object metadata propagates automatically via lineage

**Key insight:** All production systems with multi-agent workflows use **typed metadata contracts** + **runtime validation at gates** + **explicit propagation rules** (what happens when metadata is missing?)

**Tradeoff:** Strong validation (blocks invalid work) vs weak validation (warns but allows). For v1-core (no orchestrator), weak validation is only option.

**Human gate:** NONE

---

#### Phase 3.4: ARCHITECTURE/OPTIONS

**Agent:** `architecture-options-generator`  
**Input:** `ANALYSIS-011-architecture.md` + `PROBLEM-011`  
**Output:** `OPTIONS-011-architecture.md`

```yaml
artifact_class: workflow_phase
altitude: ARCHITECTURE
phase: OPTIONS
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Options backed by analysis of 4 comparable systems + ADR constraints; no prototype testing"
```

**Content (3 architectural options):**

**Option A: Frontmatter + Manual Validation (v1-core only)**
- Metadata in YAML frontmatter
- CLI command `nowu validate` checks all artifacts, exits 0/1
- Agents do not enforce; human runs validate before commit
- Pros: Minimal code change; no orchestrator required; human in the loop
- Cons: Opt-in validation is easy to forget; no runtime enforcement

**Option B: Frontmatter + Pydantic Models + Agent-Side Validation**
- Metadata schema in `core/contracts.py` as Pydantic models
- Every agent reads/writes metadata via typed API
- Agent fails if metadata is invalid (hard block)
- Pros: Type-safe; catches errors at creation time; works in v1-core
- Cons: Higher implementation cost; agents need metadata read/write library

**Option C: Frontmatter + Gate Validation + Deferred Enforcement (staged rollout)**
- Level 1 (v1-core): Frontmatter, no validation
- Level 2 (v1.0): `flow` orchestrator validates at phase transitions
- Level 3 (v1.1): LangGraph state machine enforces metadata contract
- Pros: Incremental; matches current reality (idea-004 proposes 3-level rollout)
- Cons: Delayed enforcement; Level 1 can't prevent violations

**Human gate:** DECISION REQUIRED (architectural bet)

**→ Human selects Option C (staged rollout). Rationale: matches idea-004 implementation plan; Level 1 is cheapest path to v1-core dogfooding.**

---

#### Phase 3.5: ARCHITECTURE/DECISION

**Agent:** `architecture-decider`  
**Input:** `OPTIONS-011-architecture.md` + human selection  
**Output:** `ADR-0007-workflow-position-metadata.md` (new architecture decision record)

```yaml
artifact_class: knowledge
artifact_type: ADR
id: ADR-0007
origin_altitude: ARCHITECTURE
origin_phase: DECISION
consumer_altitudes: [DELIVERY, EXECUTION]
epistemic_grade: EVIDENCE_BASED
grade_justification: "Decision backed by analysis of 4 production systems + alignment with ADR-0001/0006 + idea-004 3-level enforcement model"
status: ACCEPTED
```

**Content:**
```markdown
# ADR-0007: Workflow Position Metadata Schema

## Status
ACCEPTED — 2026-05-05

## Context
USE-CASE-NF-16 requires machine-readable altitude+phase metadata on all workflow and knowledge artifacts to prevent altitude drift and enable context resumption.

## Decision

**Three-level implementation (staged):**

### Level 1 (v1-core): Frontmatter Metadata (no enforcement)
- All new workflow artifacts include:
  ```yaml
  artifact_class: workflow_phase | knowledge
  altitude: STRATEGIC | PRODUCT | ARCHITECTURE | DELIVERY | EXECUTION
  phase: IDEA | PROBLEM | ANALYSIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN
  ```
- Knowledge artifacts additionally include:
  ```yaml
  origin_altitude: [altitude]
  origin_phase: [phase]
  consumer_altitudes: [list of altitudes]
  ```
- No validation in v1-core; agents are responsible for writing correct metadata
- CLI command `nowu status` reads metadata from current session artifacts

### Level 2 (v1.0): Gate Validation
- `flow` orchestrator validates metadata at phase transitions
- Circuit breaker: if agent produces artifact with wrong altitude, workflow pauses and prompts human review
- Invalid metadata logged to `state/health/altitude-violations.md`

### Level 3 (v1.1): Runtime Enforcement
- PydanticAI/LangGraph state machine enforces metadata contract
- Agents cannot produce artifacts without valid metadata (hard block)
- Metadata schema defined in `core/contracts.py` as `WorkflowPosition` and `KnowledgeProvenance` types

## Consequences

**Positive:**
- Solves USE-CASE-NF-16 (context resumption)
- Enables circuit breaker validation (idea-004 §6.4)
- Forward-compatible with orchestrator enforcement

**Negative:**
- ~55 file frontmatter edits for Level 1
- Metadata schema must be stable before Level 2 (breaking changes are expensive)

**Neutral:**
- Level 1 relies on agent discipline; Level 2+ provides runtime guarantees

## Related
- USE-CASE-NF-16 (origin)
- idea-004 (2D altitude/phase model)
- ADR-0001 (contracts belong in `core`)
```

**Human gate:** APPROVAL (ADR must be ratified)

**→ Human approves ADR-0007. Marks `status: ACCEPTED`.**

---

#### Phase 3.6: ARCHITECTURE/EVALUATION

**Agent:** `architecture-evaluator` (ATAM-lite)  
**Input:** `ADR-0007` + quality attributes (maintainability, performance, security, AI-buildability)  
**Output:** `EVALUATION-011-architecture.md`

```yaml
artifact_class: workflow_phase
altitude: ARCHITECTURE
phase: EVALUATION
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "ATAM-lite evaluation against 4 quality attributes; no prototype performance testing"
```

**Content:**
```markdown
## ATAM-Lite Evaluation: ADR-0007 (Workflow Position Metadata)

### Quality Attributes Tested

**QA-1: Maintainability**
- Scenario: Adding a new phase (e.g., SECURITY)
- Impact: Level 1 (add to schema), Level 2 (no code change), Level 3 (Pydantic model update)
- **Result: PASS** — new phases are data-driven; no agent rewrite needed

**QA-2: AI-Buildability**
- Scenario: AI agent reads ADR-0007 and implements Level 1 (frontmatter edits)
- Impact: Mechanical task (YAML edits); clear acceptance criteria; no ambiguous decisions
- **Result: PASS** — suitable for AI implementation

**QA-3: Performance**
- Scenario: `nowu status` reads metadata from 50 artifacts
- Impact: File I/O only (no LLM calls); <100ms expected
- **Result: PASS** — metadata read is fast

**QA-4: Security (data provenance)**
- Scenario: Malicious agent writes artifact at wrong altitude
- Impact: Level 1 (undetected), Level 2 (detected at gate), Level 3 (blocked at creation)
- **Result: CONDITIONAL PASS** — Level 1 is vulnerable; Levels 2-3 provide security

### Risks Identified
- **Risk 1:** If Level 2 is delayed, altitude violations in v1-core go undetected
  - **Mitigation:** Manual `nowu validate` command before key transitions
- **Risk 2:** Frontmatter schema changes between Level 1 and Level 3 require migration
  - **Mitigation:** Schema must be stable before Level 1 ships (rely on idea-004 draft)

### Recommendation
**APPROVED for implementation.** ADR-0007 passes all quality attribute scenarios. Risk 1 is acceptable for v1-core dogfooding phase.
```

**Human gate:** REVIEW (human confirms evaluation is sound)

**→ Human confirms. ADR-0007 passes ATAM-lite. Ready for delivery scoping.**

---

#### Phase 3.7-3.9: ARCHITECTURE/IMPLEMENTATION, VERIFICATION, LEARN

**Skip** — architecture altitude produces decisions (ADRs), not code. Transition to DELIVERY altitude.

---

### ALTITUDE 4: DELIVERY

#### Phase 4.1: DELIVERY/IDEA

**Skip** — delivery altitude receives fully-defined architectural decisions, not raw ideas.

---

#### Phase 4.2: DELIVERY/PROBLEM

**Agent:** `delivery-problem-framer`  
**Input:** `ADR-0007` + `USE-CASE-NF-16` + current sprint capacity  
**Output:** `PROBLEM-012.md`

```yaml
artifact_class: knowledge
artifact_type: PROBLEM
origin_altitude: DELIVERY
origin_phase: PROBLEM
consumer_altitudes: [DELIVERY, EXECUTION]
epistemic_grade: HYPOTHESIS
grade_justification: "Scoping problem; validated against ADR-0007 but not implemented yet"
```

**Content:**
```markdown
## Delivery Problem: How to Scope ADR-0007 Level 1 for v1-core

**Context:** ADR-0007 requires ~55 file edits to add frontmatter metadata. This is a v1-core blocker (USE-CASE-NF-16 is Tier 1).

**The scoping tension:**
- All 55 files? (High cost, low risk of incomplete implementation)
- Critical path only? (Low cost, risk of missing files that break `nowu status`)
- Forward-only? (New artifacts only; no migration of existing files)

**Constraint:** v1-core 6-month deadline is 4 weeks away. Must prioritize.

**Appetite:** 2-3 days for one human or AI agent to complete Level 1 implementation.
```

**Human gate:** NONE (scoping problem is input to options)

---

#### Phase 4.3: DELIVERY/ANALYSIS

**Agent:** `delivery-analyst`  
**Input:** `PROBLEM-012` + file inventory  
**Output:** `ANALYSIS-012-delivery.md`

```yaml
artifact_class: workflow_phase
altitude: DELIVERY
phase: ANALYSIS
epistemic_grade: EVIDENCE_BASED
grade_justification: "File inventory from nowu repository; scope estimate based on real file count"
```

**Content:**
- **File inventory:** 55 total artifacts
  - 14 ADRs (already have frontmatter; need `altitude:` + `phase:` added)
  - 18 workflow artifacts (OPTIONS.md, DECISION.md, etc.; need full schema)
  - 15 knowledge artifacts (GOAL-NNN.md, USE-CASE-NNN.md, etc.; need `origin_altitude` + `consumer_altitudes`)
  - 8 agent definition files (need `altitude:`, `phase:`, `operator:`)
- **Critical path:** Agent definitions + current session artifacts (required for `nowu status`)
- **Deferrable:** Historical artifacts (don't affect active workflows)

**Human gate:** NONE

---

#### Phase 4.4: DELIVERY/OPTIONS

**Agent:** `delivery-options-generator` (Shape Up shaping)  
**Input:** `ANALYSIS-012-delivery.md` + `PROBLEM-012`  
**Output:** `OPTIONS-012-delivery.md`

```yaml
artifact_class: workflow_phase
altitude: DELIVERY
phase: OPTIONS
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Scoping options based on file inventory + 2-3 day appetite; no implementation spike yet"
```

**Content (3 delivery scopes):**

**Option A: All Files (Complete Migration)**
- Scope: All 55 files get metadata
- Effort: 2 days (mechanical edits)
- Risk: Low (nothing is missed)
- Appetite fit: YES (fits 2-3 day budget)

**Option B: Critical Path Only (Agent Definitions + Current Session)**
- Scope: 8 agent files + ~12 current session artifacts = 20 files
- Effort: 6 hours
- Risk: Medium (historical artifacts stay untagged; may break `nowu validate` later)
- Appetite fit: YES (under budget)

**Option C: Forward-Only (New Artifacts Only, Zero Migration)**
- Scope: 0 existing files; new artifacts get metadata going forward
- Effort: 2 hours (update templates only)
- Risk: High (`nowu status` cannot read historical context; NF-16 partially broken)
- Appetite fit: YES (minimal effort)

**Human gate:** DECISION REQUIRED (scope bet)

**→ Human selects Option A (complete migration). Rationale: Level 1 is foundation for Level 2/3; incomplete migration creates debt. 2 days is acceptable.**

---

#### Phase 4.5: DELIVERY/DECISION

**Agent:** `delivery-decider`  
**Input:** `OPTIONS-012-delivery.md` + human selection  
**Output:** `EPIC-003.md` + `SHAPE-003.md`

```yaml
# EPIC-003.md
artifact_class: knowledge
artifact_type: EPIC
id: EPIC-003
title: "Implement ADR-0007 Level 1 (Frontmatter Metadata)"
origin_altitude: DELIVERY
origin_phase: DECISION
consumer_altitudes: [EXECUTION]
epistemic_grade: EVIDENCE_BASED
grade_justification: "Scope backed by file inventory + appetite fit + ADR-0007 decision"
status: READY_FOR_SHAPING
appetite: 2 days
```

```yaml
# SHAPE-003.md
artifact_class: workflow_phase
altitude: DELIVERY
phase: DECISION
epistemic_grade: EVIDENCE_BASED
grade_justification: "Shape derived from ADR-0007 specification + file inventory"
```

**SHAPE-003.md content:**
```markdown
## Shape: ADR-0007 Level 1 Implementation

### Appetite
2 days (one human or AI agent working full-time)

### Problem
55 existing artifacts lack machine-readable altitude/phase metadata. USE-CASE-NF-16 requires this for context resumption and altitude drift prevention.

### Solution Boundaries

**In scope:**
1. Add frontmatter to 14 ADRs:
   ```yaml
   altitude: ARCHITECTURE
   phase: DECISION
   ```
2. Add frontmatter to 18 workflow artifacts:
   ```yaml
   artifact_class: workflow_phase
   altitude: [STRATEGIC|PRODUCT|ARCHITECTURE|DELIVERY|EXECUTION]
   phase: [IDEA|PROBLEM|ANALYSIS|OPTIONS|DECISION]
   ```
3. Add frontmatter to 15 knowledge artifacts:
   ```yaml
   artifact_class: knowledge
   origin_altitude: [altitude]
   consumer_altitudes: [list]
   ```
4. Add frontmatter to 8 agent definitions:
   ```yaml
   operator: [IDEA|PROBLEM|ANALYSIS|etc]
   altitude: [applicable altitudes]
   ```
5. Update `ALTITUDES.md` to document the metadata schema
6. Create `nowu status` CLI command (reads metadata, outputs current position)

**Out of scope:**
- Validation (Level 2)
- Runtime enforcement (Level 3)
- Metadata for non-workflow files (README.md, etc.)

### Rabbit Holes
- **Don't** try to infer missing metadata from content — ask human if ambiguous
- **Don't** implement validation yet (that's Level 2)
- **Don't** refactor file structure (just add frontmatter)

### No-Gos
- Breaking existing artifact references (file names stay the same)
- Changing artifact content (only frontmatter changes)
```

**Human gate:** APPROVAL (shape must be confirmed before implementation)

**→ Human approves SHAPE-003. Ready for execution.**

---

### ALTITUDE 5: EXECUTION

#### Phase 5.1-5.4: EXECUTION/IDEA, PROBLEM, ANALYSIS, OPTIONS

**Skip** — execution altitude receives fully-shaped work, not open-ended exploration.

---

#### Phase 5.5: EXECUTION/DECISION

**Skip** — no decision needed; implementation follows the shape directly.

---

#### Phase 5.6: EXECUTION/EVALUATION

**Skip for now** — evaluation happens after implementation (VERIFICATION phase)

---

#### Phase 5.7: EXECUTION/IMPLEMENTATION

**Agent:** `nowu-implementer` (S6 in old model)  
**Input:** `SHAPE-003.md` + `ADR-0007`  
**Output:** 
- 55 modified files (frontmatter added)
- `nowu status` command implementation
- `ALTITUDES.md` schema documentation
- `IMPLEMENTATION-NOTES-003.md` (what was done, any deviations from shape)

```yaml
# IMPLEMENTATION-NOTES-003.md
artifact_class: workflow_phase
altitude: EXECUTION
phase: IMPLEMENTATION
epistemic_grade: VERIFIED_FACT
grade_justification: "Implementation complete; all 55 files modified; git diff available"
```

**Human gate:** NONE (agent implements; human reviews at VERIFICATION phase)

---

#### Phase 5.8: EXECUTION/VERIFICATION

**Agent:** `nowu-reviewer` (S7) + `VBR` loop (S8)  
**Input:** `IMPLEMENTATION-NOTES-003.md` + git diff + `SHAPE-003.md` (acceptance criteria)  
**Output:** `REVIEW-003.md`

```yaml
artifact_class: workflow_phase
altitude: EXECUTION
phase: VERIFICATION
epistemic_grade: EVIDENCE_BASED
grade_justification: "Verified by diff review + manual testing of `nowu status` command"
```

**Content:**
```markdown
## Verification Report: EPIC-003 (ADR-0007 Level 1)

### Acceptance Criteria Check

✅ **AC-1:** All 55 files have frontmatter  
✅ **AC-2:** Metadata schema matches ADR-0007 specification  
✅ **AC-3:** `nowu status` command works (tested on 3 projects)  
✅ **AC-4:** No breaking changes to file references  
⚠️  **AC-5:** ALTITUDES.md updated (minor: schema examples need formatting fix)  

### Issues Found
- **Issue 1 (minor):** 3 ADRs had ambiguous altitude (STRATEGIC vs PRODUCT); resolved by cross-referencing related use cases
- **Issue 2 (cosmetic):** ALTITUDES.md code blocks need syntax highlighting

### VBR (Verify-By-Running)
- Tested `nowu status` on nowu, AP, RE projects
- Tested git hooks (no conflicts with existing hooks)
- Tested metadata read performance (<50ms for 55 files)

### Recommendation
**ACCEPT with minor fixes.** Issue 2 (formatting) is non-blocking; can be fixed in post-ship polish.
```

**Human gate:** APPROVAL (human confirms implementation meets acceptance criteria)

**→ Human reviews diff + runs `nowu status`. Approves. Marks EPIC-003 as SHIPPED.**

---

#### Phase 5.9: EXECUTION/LEARN

**Agent:** `nowu-curator` (S9 in old model)  
**Input:** `REVIEW-003.md` + session artifacts  
**Output:** 
- `LESSON-007.md` (new lesson learned)
- Knowledge atoms created in `know` (if integrated)
- `CAPTURE-003.md` (session summary)

```yaml
# LESSON-007.md
artifact_class: knowledge
artifact_type: LESSON
origin_altitude: EXECUTION
origin_phase: LEARN
consumer_altitudes: [DELIVERY, EXECUTION]
epistemic_grade: EVIDENCE_BASED
grade_justification: "Lesson validated by successful EPIC-003 implementation"
```

**Content:**
```markdown
## Lesson: Frontmatter Migration Is Mechanical and Fast

**Context:** EPIC-003 required adding frontmatter to 55 files. Initial estimate: 2 days. Actual: 4 hours.

**What we learned:**
- AI agents can handle mechanical edits faster than humans (batch processing)
- The hard part was schema design (ADR-0007), not implementation
- Ambiguous cases (3 ADRs with unclear altitude) were rare and resolvable by cross-referencing

**Transferable pattern:** 
- For any "add structured metadata to N files" task:
  1. Design schema first (slow, needs human judgment)
  2. Prototype on 3-5 files to catch edge cases
  3. Batch-process remaining files (fast, AI-suitable)

**Apply to:** Future ADR implementations, template updates, knowledge artifact migrations
```

**Human gate:** REVIEW (human confirms lesson is accurate and worth preserving)

**→ Human confirms. Lesson captured.**

---

## Part 2: What Happens at Each Phase (Summary Table)

| Altitude | Phase | Agent | Input Artifacts | Output Artifacts | Human Gate | Epistemic Grade |
|---|---|---|---|---|---|---|
| **STRATEGIC** | IDEA | strategic-idea-generator | Human prompt, vision.md | IDEA-NNN.md | NONE | SPECULATION |
| | PROBLEM | strategic-problem-synthesizer | IDEA-NNN.md, vision.md | PROBLEM-NNN.md | REVIEW | HYPOTHESIS |
| | ANALYSIS | strategic-analyst | PROBLEM-NNN.md, market research | ANALYSIS-NNN.md | NONE | INFORMED_ESTIMATE |
| | OPTIONS | strategic-options-generator | ANALYSIS-NNN.md | OPTIONS-NNN.md | NONE | INFORMED_ESTIMATE |
| | DECISION | strategic-decider | OPTIONS-NNN.md, human choice | GOAL-NNN.md | APPROVAL | EVIDENCE_BASED |
| **PRODUCT** | IDEA | product-idea-extractor | GOAL-NNN.md, persona | IDEA-NNN.md (multiple) | NONE | SPECULATION |
| | PROBLEM | product-problem-validator | IDEA-NNN.md, persona research | PROBLEM-NNN.md | VALIDATION | HYPOTHESIS |
| | ANALYSIS | product-analyst | PROBLEM-NNN.md, competitive research | ANALYSIS-NNN.md | NONE | INFORMED_ESTIMATE |
| | OPTIONS | product-options-generator | ANALYSIS-NNN.md | OPTIONS-NNN.md | NONE | HYPOTHESIS |
| | DECISION | product-decider | OPTIONS-NNN.md, human choice | USE-CASE-NNN.md | APPROVAL | EVIDENCE_BASED |
| **ARCHITECTURE** | IDEA | architecture-idea-generator | USE-CASE-NNN.md, existing ADRs | IDEA-NNN.md | NONE | SPECULATION |
| | PROBLEM | architecture-problem-framer | IDEA-NNN.md, USE-CASE-NNN.md | PROBLEM-NNN.md | REVIEW | HYPOTHESIS |
| | ANALYSIS | architecture-analyst | PROBLEM-NNN.md, pattern research | ANALYSIS-NNN.md | NONE | INFORMED_ESTIMATE |
| | OPTIONS | architecture-options-generator | ANALYSIS-NNN.md | OPTIONS-NNN.md | NONE | INFORMED_ESTIMATE |
| | DECISION | architecture-decider | OPTIONS-NNN.md, human choice | ADR-NNNN.md | APPROVAL | EVIDENCE_BASED |
| | EVALUATION | architecture-evaluator | ADR-NNNN.md, QA scenarios | EVALUATION-NNN.md | REVIEW | INFORMED_ESTIMATE |
| **DELIVERY** | PROBLEM | delivery-problem-framer | ADR-NNNN.md, capacity | PROBLEM-NNN.md | NONE | HYPOTHESIS |
| | ANALYSIS | delivery-analyst | PROBLEM-NNN.md, file inventory | ANALYSIS-NNN.md | NONE | EVIDENCE_BASED |
| | OPTIONS | delivery-options-generator | ANALYSIS-NNN.md, appetite | OPTIONS-NNN.md | NONE | INFORMED_ESTIMATE |
| | DECISION | delivery-decider | OPTIONS-NNN.md, human choice | EPIC-NNN.md, SHAPE-NNN.md | APPROVAL | EVIDENCE_BASED |
| **EXECUTION** | IMPLEMENTATION | nowu-implementer | SHAPE-NNN.md | Code changes, IMPL-NOTES-NNN.md | NONE | VERIFIED_FACT |
| | VERIFICATION | nowu-reviewer, VBR | IMPL-NOTES-NNN.md, git diff | REVIEW-NNN.md | APPROVAL | EVIDENCE_BASED |
| | LEARN | nowu-curator | REVIEW-NNN.md, session artifacts | LESSON-NNN.md, CAPTURE-NNN.md | REVIEW | EVIDENCE_BASED |

---

## Part 3: Where Is Human Interaction Needed?

### Always Required (6 gates)
1. **STRATEGIC/PROBLEM** — human confirms this is the right strategic problem
2. **STRATEGIC/DECISION** — human selects strategic option + approves goal
3. **PRODUCT/PROBLEM** — human validates product problem against their experience
4. **PRODUCT/DECISION** — human selects product option + approves use case
5. **ARCHITECTURE/DECISION** — human approves ADR (architectural commitment)
6. **DELIVERY/DECISION** — human approves shape (scope/appetite fit)
7. **EXECUTION/VERIFICATION** — human reviews implementation + approves ship

### Sometimes Required (4 optional gates)
8. **ARCHITECTURE/PROBLEM** — lightweight review (can be auto-approved if problem is clear)
9. **ARCHITECTURE/EVALUATION** — review ATAM-lite report (can be auto-approved if all QAs pass)
10. **EXECUTION/LEARN** — review lessons (can be auto-approved if grade is EVIDENCE_BASED)

### Never Required (automated)
- IDEA phases (captured, not approved)
- ANALYSIS phases (inform next phase, no decision)
- OPTIONS phases (generate alternatives, don't select)
- IMPLEMENTATION phase (agent implements according to shape)

### Human Effort Estimate (per traversal)
- **STRATEGIC gates:** 15-30 min (problem + options review + decision)
- **PRODUCT gates:** 15-30 min (problem validation + options review + decision)
- **ARCHITECTURE gates:** 30-45 min (ADR review + ATAM-lite review)
- **DELIVERY gates:** 10-15 min (shape review + approval)
- **EXECUTION gates:** 20-40 min (code review + VBR)

**Total human time per full traversal:** 90-160 minutes (1.5-2.5 hours)

**AI agent time:** 4-8 hours (depending on research depth and implementation complexity)

**Ratio:** 85-95% AI-handled work (aligns with vision.md 6-month goal: 90-99%)

---

## Part 4: The GOAL→UC→??? Gap (Detailed)

### The Question
"After USE-CASE is decided, can we jump to EPIC/TODO? Or do we need a global solution shape?"

### The Answer
**It depends on scope:**

| Use case scope | Path | Why |
|---|---|---|
| **Single-module change** | PRODUCT→DELIVERY (skip ARCHITECTURE) | No cross-module coordination needed; shape directly defines scope |
| **Cross-module change (new feature)** | PRODUCT→ARCHITECTURE→DELIVERY | Need ADR to define contracts, protocols, and module boundaries |
| **Cross-module change (refactor)** | PRODUCT→ARCHITECTURE→EVALUATION→DELIVERY | Need ATAM-lite to verify quality attributes before committing |

### When You MUST Pass Through ARCHITECTURE

1. **New cross-module protocol** (e.g., USE-CASE-NF-16 affects `core`, `flow`, `know`, all agents)
2. **Breaking change to existing contract** (e.g., changing `AdapterProtocol` signature)
3. **New module introduction** (e.g., adding a `security` module)
4. **Quality attribute trade-off** (e.g., "fast sync vs. eventual consistency" — requires ATAM)

### The "Global Solution Shape" Question

**Yes, you need a solution shape before DELIVERY — but it's called an ADR, not a shape.**

The confusion is naming:
- **ARCHITECTURE/DECISION output = ADR** (the "what" and "why" of the structural solution)
- **DELIVERY/DECISION output = SHAPE** (the "how much" and "how long" of the implementation scope)

The ADR is the global solution pattern. The SHAPE is the per-epic scoping artifact.

### Multi-Module Example: USE-CASE-NF-16

```
PRODUCT/DECISION (NF-16: machine-readable workflow position)
        ↓
ARCHITECTURE/PROBLEM (no formal contract exists)
        ↓
ARCHITECTURE/OPTIONS (frontmatter vs database vs index file)
        ↓
ARCHITECTURE/DECISION (ADR-0007: frontmatter + 3-level enforcement) ← GLOBAL SOLUTION
        ↓
ARCHITECTURE/EVALUATION (ATAM-lite: passes all QA scenarios)
        ↓
DELIVERY/PROBLEM (how to scope 55-file migration?)
        ↓
DELIVERY/OPTIONS (all files vs critical path vs forward-only)
        ↓
DELIVERY/DECISION (SHAPE-003: complete migration, 2-day appetite) ← EPIC SCOPE
        ↓
EXECUTION/IMPLEMENTATION
```

**The ADR (0007) is the global solution.** It says: "We will use frontmatter metadata with staged enforcement."

**The SHAPE (003) is the local scope.** It says: "We will edit 55 files in 2 days."

---

## Part 5: Iterations and Epistemic Grades (idea-005)

### The Question
"Should we use epistemic grades to drive iteration? Does low confidence trigger a research sub-loop?"

### The Answer
**Yes — and you should formalize it as a phase.**

### Proposed Addition: "Confidence Sub-Loop" at OPTIONS Phase

**Current flow:**
```
ANALYSIS → OPTIONS → DECISION
```

**With confidence sub-loop:**
```
ANALYSIS (produces grade) 
   ↓
   ↓ if grade < EVIDENCE_BASED
   ↓ ↘
   ↓   RESEARCH SUB-LOOP (agent gathers evidence)
   ↓     ↓
   ↓     ANALYSIS (re-grade with new evidence)
   ↓   ↗
   ↓ ↗
OPTIONS → DECISION
```

### When to Trigger Research Sub-Loop

| Altitude | Minimum grade to proceed | Rationale |
|---|---|---|
| STRATEGIC | EVIDENCE_BASED | Strategic bets are expensive to reverse |
| PRODUCT | INFORMED_ESTIMATE | Product decisions need validation but can iterate |
| ARCHITECTURE | EVIDENCE_BASED | Architecture decisions are hard to change |
| DELIVERY | HYPOTHESIS | Scoping is cheap to revise; ship and learn |
| EXECUTION | HYPOTHESIS | Code changes are cheap to revert |

### How to Enforce

**Level 1 (v1-core):** Agent outputs grade + justification; human decides whether to trigger research

**Level 2 (v1.0):** `flow` orchestrator checks grade at DECISION gate; if below threshold, offers "Research" option to human

**Level 3 (v1.1):** Orchestrator auto-triggers research sub-loop for grades below threshold; requires explicit human override to skip

### Example: Low-Confidence Option Triggers Research

```yaml
# OPTIONS-010-product.md (initial)
epistemic_grade: HYPOTHESIS
grade_justification: "Based on analysis of 3 tools; no user testing"

options:
  - Option A: Human-readable resume command
  - Option B: Machine-readable metadata
  - Option C: Hybrid (B + dashboard)
```

**Orchestrator detects:** Grade is HYPOTHESIS, threshold is INFORMED_ESTIMATE.

**Action:** Trigger research sub-loop.

**Research agent:**
- Prototype Option B (add metadata to 5 files, test `nowu status`)
- Interview Raphael (validate that metadata solves his context-loss problem)
- Benchmark performance (metadata read time <50ms confirmed)

**Output:** `ANALYSIS-010-product-v2.md`

```yaml
epistemic_grade: EVIDENCE_BASED
grade_justification: "Prototype tested; user validated; performance benchmarked"
grade_delta: "HYPOTHESIS → EVIDENCE_BASED via prototype + user interview"
```

**Result:** OPTIONS phase re-runs with higher confidence; DECISION proceeds.

---

### Where Epistemic Grades Live in Artifacts

Every artifact that makes a claim should carry a grade:

| Artifact type | Grade field | Who assigns |
|---|---|---|
| IDEA | `epistemic_grade` | Capturing agent |
| PROBLEM | `epistemic_grade` | Validating agent |
| ANALYSIS | `epistemic_grade` | Analysis agent (based on research depth) |
| OPTIONS | `epistemic_grade` (per option) | Options agent |
| DECISION | `epistemic_grade` | Decider agent (based on input quality) |
| ADR | `epistemic_grade` | Architecture decider (based on analysis + evaluation) |
| SHAPE | `epistemic_grade` | Delivery decider (based on appetite fit) |
| LESSON | `epistemic_grade` | Curator (based on validation in practice) |

---

## Part 6: Security as a Phase? (Palantir Model)

### The Question
"Should we make SECURITY a separate phase like Palantir does?"

### Research: What Palantir Actually Does

Palantir **does not have a separate security phase**. Instead, security is:

1. **A system property** — markings propagate automatically via data lineage[cite:479]
2. **Enforced at every layer** — infrastructure, platform, enterprise, application[cite:480]
3. **Baked into the architecture** — security is a core development philosophy, not an afterthought[cite:476]
4. **Validated at deployment** — zero-trust model with continuous monitoring[cite:484]

**Key insight from Palantir blog:**[cite:484]
> "Building Software for a Zero Trust World" — security is not a workflow phase; it's a **mandatory control that propagates** with data.

### OWASP Secure-by-Design Framework

The OWASP SbD process[cite:488] has these steps:
1. Capture security requirements (PLANNING phase)
2. Draft architecture with trust zones (DESIGN phase)
3. Apply SbD checklist (DESIGN phase)
4. Internal peer review (DESIGN phase)
5. Risk triage (escalate if High/Critical risk)
6. AppSec review (for High/Critical risk only)

**Key insight:** Security is not a separate phase — it's **embedded in ARCHITECTURE/DECISION and ARCHITECTURE/EVALUATION phases**.

### Recommendation: Embed Security, Don't Add a Phase

**Do NOT add SECURITY as a 10th phase.** Instead:

#### Option A: Embed Security in Existing Phases

| Altitude | Phase | Security Integration |
|---|---|---|
| STRATEGIC | PROBLEM | Identify regulatory/compliance requirements (GDPR, HIPAA, etc.) |
| PRODUCT | PROBLEM | Identify data sensitivity (PII, PHI, financial data) |
| ARCHITECTURE | ANALYSIS | Threat modeling, trust zone analysis |
| ARCHITECTURE | OPTIONS | Security trade-offs per option (e.g., encryption at rest vs performance) |
| ARCHITECTURE | DECISION | ADR must include "Security Considerations" section |
| ARCHITECTURE | EVALUATION | Security is a quality attribute (ATAM-lite includes "QA-Security") |
| DELIVERY | SHAPE | Acceptance criteria include security requirements |
| EXECUTION | VERIFICATION | VBR includes security checklist (authentication, authorization, input validation, etc.) |

#### Option B: Add Security Gate at ARCHITECTURE/EVALUATION (Conditional)

**Trigger:** If ADR introduces:
- New data storage
- New external API
- New authentication/authorization logic
- PII or sensitive data handling

**Action:** ARCHITECTURE/EVALUATION must include a "Security Review Checklist" (based on OWASP SbD checklist[cite:488])

**Blocker:** If checklist has unresolved "No" items flagged as High/Critical risk, ARCHITECTURE/DECISION cannot proceed to DELIVERY until mitigated.

---

### Concrete Proposal: Security Review Checklist (ARCHITECTURE/EVALUATION)

Add this to `EVALUATION-NNN.md` when triggered:

```markdown
## Security Review Checklist (OWASP SbD)

**Trigger:** This ADR introduces [new data storage / new API / PII handling / etc.]

### Checklist

- [ ] **Authentication:** How is user identity verified?
- [ ] **Authorization:** How are permissions enforced? (RBAC, ABAC, etc.)
- [ ] **Data at rest:** Is sensitive data encrypted in storage?
- [ ] **Data in transit:** Are all connections TLS 1.2+?
- [ ] **Input validation:** Are all external inputs validated and sanitized?
- [ ] **Secrets management:** Are API keys/tokens stored securely (not hardcoded)?
- [ ] **Audit logging:** Are security-relevant actions logged?
- [ ] **Dependency scanning:** Are all dependencies CVE-free?
- [ ] **Least privilege:** Does each component have minimum required permissions?
- [ ] **Fail-secure:** Does the system default to deny on error?

### Risk Assessment

- **Risk level:** [Low / Normal / High / Critical]
- **Unresolved High/Critical items:** [list or "NONE"]

### Recommendation

- [ ] APPROVED — proceed to DELIVERY
- [ ] BLOCKED — must resolve [item] before proceeding
```

**If blocked:** ADR loops back to ARCHITECTURE/OPTIONS to generate a security-compliant alternative.

---

## Part 7: Final Summary

### What Gets Created at Each Altitude

| Altitude | Artifacts Created | Durability |
|---|---|---|
| STRATEGIC | GOAL-NNN.md | Permanent (until retired) |
| PRODUCT | USE-CASE-NNN.md | Permanent (until retired) |
| ARCHITECTURE | ADR-NNNN.md, EVALUATION-NNN.md | Permanent (ADR), Session (EVALUATION) |
| DELIVERY | EPIC-NNN.md, SHAPE-NNN.md | Permanent (EPIC), Session (SHAPE) |
| EXECUTION | Code changes, REVIEW-NNN.md, LESSON-NNN.md | Permanent (code, lesson), Session (review) |

### What Is Sufficient to Proceed

| Transition | Sufficient Artifact(s) | Gate | Can Skip If... |
|---|---|---|---|
| STRATEGIC → PRODUCT | GOAL-NNN.md (APPROVED) | Human approval | Never — goals are strategic commitments |
| PRODUCT → ARCHITECTURE | USE-CASE-NNN.md (APPROVED) | Human approval | Single-module change (skip to DELIVERY) |
| ARCHITECTURE → DELIVERY | ADR-NNNN.md (APPROVED) + EVALUATION (PASS) | Human approval + QA pass | Never — ADR is binding contract |
| DELIVERY → EXECUTION | SHAPE-NNN.md (APPROVED) | Human approval | Never — shape defines scope |
| EXECUTION → LEARN | REVIEW-NNN.md (APPROVED) | Human approval | Never — review validates correctness |

### Human Interaction Points (Total: 7 required, 3 optional)

**Always Required:**
1. STRATEGIC/DECISION (approve goal)
2. PRODUCT/DECISION (approve use case)
3. ARCHITECTURE/DECISION (approve ADR)
4. ARCHITECTURE/EVALUATION (confirm QA pass) — **can be automated if all checks pass**
5. DELIVERY/DECISION (approve shape)
6. EXECUTION/VERIFICATION (approve code review)
7. EXECUTION/LEARN (confirm lesson) — **can be automated if grade is EVIDENCE_BASED**

**Sometimes Required:**
8. STRATEGIC/PROBLEM (confirm problem framing) — **can skip if problem is clear**
9. PRODUCT/PROBLEM (validate problem against experience) — **can skip if synthesized from validated use case**
10. ARCHITECTURE/PROBLEM (confirm architectural problem framing) — **can skip if problem is straightforward**

---

### Iterations and Epistemic Grades

**Yes, integrate epistemic grades:**
- Every artifact carries `epistemic_grade` field
- Grades below altitude-specific thresholds trigger "Research Sub-Loop" at ANALYSIS phase
- Research sub-loop: agent gathers evidence → re-analyzes → upgrades grade → proceeds to OPTIONS
- Level 1 (v1-core): human decides whether to research
- Level 2 (v1.0): orchestrator offers research option
- Level 3 (v1.1): orchestrator auto-triggers research (human can override)

**Altitude-specific grade thresholds:**
- STRATEGIC: EVIDENCE_BASED minimum
- ARCHITECTURE: EVIDENCE_BASED minimum
- PRODUCT: INFORMED_ESTIMATE minimum
- DELIVERY: HYPOTHESIS acceptable
- EXECUTION: HYPOTHESIS acceptable

---

### Security as a Phase

**No, don't add SECURITY as a 10th phase.**

**Instead:**
1. Embed security in ARCHITECTURE/EVALUATION as a conditional gate
2. Add "Security Review Checklist" (OWASP SbD) to EVALUATION-NNN.md when triggered
3. Blocker: unresolved High/Critical security issues prevent transition to DELIVERY
4. All ADRs include "Security Considerations" section

**Trigger conditions:**
- New data storage
- New external API
- PII/PHI/financial data handling
- New authentication/authorization logic

---

### Does It Work?

**Yes.** The 5×9 grid handles the full traversal from human prompt to shipped code with:
- Clear artifact boundaries
- Explicit human gates
- Sufficient information at each phase to proceed
- No missing layers between GOAL and EPIC (ARCHITECTURE fills the gap)
- Security embedded (not separate phase)
- Epistemic grades as quality control (not workflow blocker)

**The model is sound. Implement it.**

