# nowu Architectural Decisions

<!-- Template for new entries: templates/decision.md -->
<!-- Template for new entries: templates/decision.md
     Level values (decision zoom): product | system | module | component | code -->

---

## D-001 — File-Based Memory Architecture

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Context
AI agents and humans both lose context. A persistent, readable, recoverable
memory system is required before any other feature can work reliably.

### Decision
Use file-based memory (Markdown + YAML frontmatter) with three tiers:
1. Active working state (`state/`) — per-artifact files
2. Architecture decisions (`docs/DECISIONS.md`) — this file
3. Long-term knowledge (`know` module) — future semantic graph

### Consequences
- **Good**: version-controllable, human-readable, no external deps
- **Bad**: files grow; need compaction strategy later (know handles this)

### Review Trigger
When `know` MemoryService is operational.

---

## D-002 — DDD Layer Architecture

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Context
Without enforced layer boundaries, infrastructure concerns leak into domain
logic, making testing difficult and coupling inevitable.

### Decision
Four-layer DDD: Domain (pure logic) → Application (use cases) →
Infrastructure (I/O, AI) → Interface (CLI, API).  
Domain must not import from any other layer.  
All cross-module dependencies go through `core/contracts/*.py` Protocols.

### Consequences
- **Good**: domain is testable in isolation, layers are swappable
- **Bad**: more boilerplate (mitigated by Protocol pattern)

### Review Trigger
Never — this is a foundational constraint.

---

## D-003 — 5-Module Structure

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: module  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Decision
Five modules: `core` (shared contracts+services) · `flow` (orchestration) ·
`bridge` (human-AI translation) · `soul` (identity+config) · `know` (knowledge).

### Tradeoff Points
Simplicity vs. granularity. Five modules is lean — avoids over-engineering at v1.
May need splitting when `bridge` grows complex.

### Review Trigger
When any module exceeds 2000 LOC.

---

## D-004 — TDD as Non-Negotiable Constraint

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: component  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Decision
Tests written BEFORE implementation. 90%+ coverage enforced in CI.
VBR hook prevents commits when tests fail.

### Consequences
- **Good**: code quality, safe refactoring, verified acceptance criteria
- **Bad**: slower initial velocity (worthwhile tradeoff for a self-developing system)

### Review Trigger
When coverage or quality targets need adjustment.

---

## D-005 — Dedicated Agent Per Workflow Step

**Date**: 2026-03-15 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (architecture decision) | **Use Cases**: all

### Context
Previous versions used 4 shared agents (architect used for S2, S3, S4).
Research shows context scope and cognitive mode differ per step, and a single
“architect” agent carries stale context between steps.

### Decision
8 dedicated agents, one per step (S1: nowu-intake, S2: nowu-constraints,
S3: nowu-options, S4: nowu-decider, S5: nowu-shaper, S6+S7: nowu-implementer,
S8: nowu-reviewer, S9: nowu-curator). Each agent is concise (≤60 lines) and
scoped to exactly the context its step needs.

### Tradeoff Points
More agent files vs. cleaner context isolation and specialised prompting.
The benefits (no context bleed, step-appropriate decision methods) outweigh
the maintenance cost of 8 small files over 4 large ones.

### Review Trigger
When agents need to collaborate across steps (future team features).

---

## D-006 — Treat `know` as the external memory system of record

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: system  
**Intake**: V1 planning | **Use Cases**: all

### Context
The original nowu draft planned to implement a local `know` module from scratch.

### Decision
Reuse the existing sibling project `know` (v0.4.0) through `KnowledgeBase` class API and `KnowAdapter(kb)`.
No internal reimplementation in nowu.

### Consequences
- Faster delivery, lower risk, and tighter contract boundaries.
- nowu modules must not bypass `know`.
- `know.init()` and flat module functions are gone; use `KnowledgeBase` instance methods.
- `today()` removed; use `kb.query_atoms(type=KnowledgeType.TASK, ...)` + date filtering.

---

## D-007 — Choose integration-first modular monolith for v1

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: system  
**Intake**: V1 architecture | **Use Cases**: all

### Context
Evaluated three options: modular monolith, event-driven internal bus,
and early microservices.

### Decision
Use an integration-first modular monolith for v1, with explicit interfaces
to allow future event-driven evolution.

### Consequences
- Best speed/reliability tradeoff for solo + AI development.
- Scale/distribution concerns deferred beyond v1.

---

## D-008 — Rebase v1 planning around integration slices, not component reinvention

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: product  
**Intake**: V1 planning | **Use Cases**: all

### Context
Prior `V1_PLAN.md` did not reflect current repository reality and lacked
architecture decision gates per step.

### Decision
Replace with seven incremental steps: contracts, memory integration,
session/WAL, role pipeline, bridge/approvals, learning/curation,
bootstrap/cross-project context.

### Consequences
Each step now includes architecture analysis, design options, evaluation,
detailed plan, and implementation verification.

---

## D-009 — Standardize role-driven workflow with VBR and approval tiers

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: system  
**Intake**: Workflow design | **Use Cases**: all

### Context
Existing workflow text was tied to a tool-specific issue pattern and did not
define strict AI handoffs.

### Decision
Adopt a role loop (Architect, Shaper, Implementer, Reviewer, Curator) with
Verify Before Reporting, Tier 1/2/3 approvals, and clear escalation.

### Consequences
Reduced scope drift, higher review quality, and clearer escalation behavior.

---

## D-010 — Prioritize NF core use cases for v1 and treat full set as direction

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: product  
**Intake**: V1 scope | **Use Cases**: NF-01..NF-07, PK-01, PK-03, XP-01

### Context
`USE_CASES.md` contains 35 use cases across NF/AP/RE/PK/XP and is intentionally broad.

### Decision
Focus v1 on NF-01..NF-07 plus PK-01/PK-03 and XP-01 as enabling coverage.

### Consequences
Keeps v1 achievable while preserving expansion path for domain-specific capabilities.

---

<!-- Add new decisions below this line using templates/decision.md -->
