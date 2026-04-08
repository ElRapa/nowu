---
id: story-v1core-003-s002
source_epic: epic-v1core-003
source_problem: problem-005
source_use_cases:
  - NF-07
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-003-s002 — Single-Session Project Bootstrap

## Story Statement

As Raphael (the multi-project human),
I want to promote an explored idea (or create from scratch) into a fully operational project context — with its own namespace-separated memory space, own decision journal, and agent-ready state — in a single session and any domain,
So that starting a new project requires no manual directory construction, no configuration editing, and no risk of contaminating existing project state.

## Appetite

Small — project bootstrap applies the existing framework scaffolding to a new project context. The domain-agnostic scaffold is the deliverable; domain-specific configuration layers are deferred to problem-008.

## Acceptance Criteria

- **AC-001:** Given Raphael initiates a project bootstrap (from an explored idea or from scratch), when the bootstrap completes within a single session, then a new project context exists with: its own isolated state space, its own decision journal, and a confirmed agent-ready status — without Raphael having manually created any directory or configuration file.
- **AC-002:** Given the new project context has been bootstrapped, when Raphael works within it, then project state is namespace-separated — no accidental cross-contamination occurs during normal project operations. Deliberate cross-project access (e.g., XP-01 discovery queries) remains possible and is not blocked by this story.
- **AC-003:** Given the bootstrap is initiated for a non-software domain (specifically the AP food business or RE real-estate business), when the bootstrap completes, then the resulting project context is fully functional for that domain — own memory, own decision journal, agent-ready — with no manual domain-specific configuration required beyond what the bootstrap session captures.

## Out of Scope (story-level)

1. Domain-specific knowledge type definitions for AP or RE (e.g., regulatory fields, formulation schemas) — those are delivered in epic-004.
2. Collaborator onboarding or multi-user access for new projects (AP-07 — v1.2 scope).
3. Template layers per domain — the bootstrap mechanism is domain-agnostic in v1-core.
4. Automated project promotion based on idea maturity signals.

## Architecture Signals

- Likely touches: core (project context schema; namespace separation enforcement; decision journal initialisation)
- Likely touches: bridge (CLI bootstrap command; project namespace creation)
- Likely touches: soul (bootstrap session agent that gathers the minimum context needed to initialise the project)
- May require: a project registry or index so the today view and cross-project features can discover all active projects
- Unknown whether: namespace separation is enforced at the file-system level (directory boundary) or at the state-query level (project ID namespace filter) — P3 decision

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-07 | Raphael (multi-project human) | New project initialised in one session — no manual directory construction or configuration editing |
| AC-002 | NF-07 | Raphael (multi-project human) | Project state is namespace-separated — no accidental cross-contamination; deliberate cross-project access (XP-01) is not blocked |
| AC-003 | NF-07 | Raphael (multi-project human) | Works for AP and RE (non-software) domains — fully operational without manual domain-specific setup |
