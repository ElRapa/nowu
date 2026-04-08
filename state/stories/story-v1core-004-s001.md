---
id: story-v1core-004-s001
source_epic: epic-v1core-004
source_problem: problem-007
source_use_cases:
  - XP-01
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-004-s001 — Cross-Project Connection Discovery

## Story Statement

As Raphael (the multi-project human),
I want the system to surface relevant items from other projects when a semantic or entity connection exists with my current work — and to let me act on, link, or dismiss each suggestion without interrupting my flow,
So that cross-project knowledge compounds without relying on my own memory to notice the connections.

## Appetite

Small — connection surfacing is a single capability: detect and present relevant cross-project items when working within a project context. Acting on suggestions (link/dismiss) is a lightweight UI response. The detection mechanism approach is an architecture decision for P3 — the `know` library (Projects/know) must be reviewed as the primary candidate before any alternatives are evaluated.

## Acceptance Criteria

- **AC-001:** Given Raphael is working in one project and another active project contains a semantically or entity-connected item, when the cross-project detection runs, then at least one relevant item from another project is surfaced to Raphael as a dismissible suggestion — without interrupting the current task flow.
- **AC-002:** Given a cross-project suggestion is surfaced, when Raphael acts on it, then he can choose from: link the suggestion to the current context, explore it within the current session, or dismiss it — all without switching project contexts or losing his current working state.
- **AC-003:** Given the system has been operating across at least two active projects (AP, RE, and NF), when cross-project surface events are tracked over the first month, then the dismissal rate remains below 70% — meaning more than 30% of surfaced connections are acted on as useful.
- **AC-004:** Given cross-project detection runs, when suggestions are presented, then they never appear as blocking prompts or modal interruptions — any suggestion can be deferred or dismissed with a single action.

## Out of Scope (story-level)

1. Automated lesson transfer between projects (XP-03 — v1.1 scope).
2. Creating permanent structural cross-project links — v1-core surfacing is suggestive, not structural.
3. Proactive surfacing of knowledge without Raphael being in a relevant working context (PK-02 — v1.1 scope).
4. Performance at scale beyond the first 6 months of knowledge accumulation (XP-05 — v2 scope).

## Architecture Signals

- Likely touches: know (primary candidate for detection layer — P3 must review `know` ADRs 0001/0003/0004, adapter.py, and NOWU_KNOW_USAGE_CONTRACTS.md before evaluating alternatives)
- Likely touches: core (cross-project query interface; connection suggestion schema)
- Likely touches: bridge (CLI suggestion presentation; act/dismiss interaction)
- May require: an entity or keyword index across all active projects to support efficient cross-project matching
- Unknown whether: entity-based matching or embedding-based semantic similarity is the right detection approach for v1-core — P3 architecture decision required. As additional context: look at sibling-project `know` (is has search capabilities that could be leveraged?); review literature on cross-document entity/semantic linking for relevant approaches.

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | XP-01 | System / Raphael (multi-project human) | At least 1 relevant cross-project item surfaced per working session — verified across 3 distinct cross-project scenarios |
| AC-002 | XP-01 | Raphael (multi-project human) | Raphael can act on (link, explore, or dismiss) a suggestion within the current session without switching project contexts |
| AC-003 | XP-01 | Raphael (multi-project human) | Dismissal rate below 70% over first month — more than 30% of suggestions acted on as useful |
| AC-004 | XP-01 | Raphael (multi-project human) | Suggestions never interrupt current flow — always dismissible with a single action |
