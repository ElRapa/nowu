# nowu Architectural Decisions

<!-- Template for new entries: templates/decision.md -->
<!-- Level values: product | system | module | component | code -->
<!-- Levels map to the Octahedron equator in docs/GLOBAL-MODEL.md -->

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

### Review Trigger: When `know` MemoryService is operational

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

### Review Trigger: Never — this is a foundational constraint

---

## D-003 — 5-Module Structure

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: module
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Decision
Five modules: `core` (shared contracts+services) · `flow` (orchestration) ·
`bridge` (human-AI translation) · `soul` (identity+config) · `know` (knowledge)

### Tradeoff Points
Simplicity vs. granularity. Five modules is lean — avoids over-engineering at v1.
May need splitting when `bridge` grows complex.

### Review Trigger: When any module exceeds 2000 LOC

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

---

## D-005 — Dedicated Agent Per Workflow Step

**Date**: 2026-03-15 | **Status**: ACCEPTED | **Level**: system
**Intake**: — (architecture decision) | **Use Cases**: all

### Context
Previous versions used 4 shared agents (architect used for S2, S3, S4).
Research shows context scope and cognitive mode differ per step, and a single
"architect" agent carries stale context between steps.

### Decision
8 dedicated agents, one per step (S1: nowu-intake, S2: nowu-constraints,
S3: nowu-options, S4: nowu-decider, S5: nowu-shaper, S6+S7: nowu-implementer,
S8: nowu-reviewer, S9: nowu-curator). Each agent is concise (≤60 lines) and
scoped to exactly the context its step needs.

### Tradeoff Points
More agent files vs. cleaner context isolation and specialised prompting.
The benefits (no context bleed, step-appropriate decision methods) outweigh
the maintenance cost of 8 small files over 4 large ones.

### Review Trigger: When agents need to collaborate across steps (future team features)

---

<!-- Add new decisions below this line using templates/decision.md -->
