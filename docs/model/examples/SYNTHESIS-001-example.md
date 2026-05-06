---
artifact_class: knowledge
artifact_type: SYNTHESIS
id: SYNTHESIS-001
title: "Cross-cutting state management needs from NF-01, NF-14, PK-08"
origin_altitude: ARCHITECTURE
origin_phase: SYNTHESIS
consumer_altitudes: [ARCHITECTURE]
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Synthesis of 3 approved use cases; no architectural prototype yet"
status: ACTIVE
created_at: 2026-05-05
last_edited_at: 2026-05-05
related_artifacts: [USE-CASE-NF-01, USE-CASE-NF-14, USE-CASE-PK-08]
promoted_from: null
promotes_to: null
relationships:
  - {edge_type: synthesizes, target_id: USE-CASE-NF-01, target_altitude: PRODUCT, target_phase: DECISION}
  - {edge_type: synthesizes, target_id: USE-CASE-NF-14, target_altitude: PRODUCT, target_phase: DECISION}
  - {edge_type: synthesizes, target_id: USE-CASE-PK-08, target_altitude: PRODUCT, target_phase: DECISION}
---

# Architectural Synthesis: State Management Strategy

## Input Scope

Analyzed 3 approved use cases pending architectural work:

- **USE-CASE-NF-01:** Multi-session memory (requires persistent state across sessions)
- **USE-CASE-NF-14:** Drift detection (requires historical session data + current state comparison)
- **USE-CASE-PK-08:** Remote capture via Telegram (requires async state updates)

## Themes Identified

### Theme 1: Persistent Session State

**Use cases:** NF-01, NF-14, PK-08
**Shared requirement:** All three need durable state that survives process restarts.
**Architectural implication:** Need a state management strategy that separates ephemeral (in-memory) from durable (persisted) state. Current file-based `state/` directory is insufficient for concurrent access.

### Theme 2: Graph Query Needs

**Use cases:** NF-01, NF-14
**Shared requirement:** Both need to query relationships (atoms -> links -> context chains).
**Architectural implication:** Flat file storage cannot express or traverse relationships. Need graph database or graph query layer over structured storage.

### Theme 3: Async State Updates

**Use cases:** PK-08
**Shared requirement:** Telegram adapter receives messages asynchronously; must update state without active CLI session.
**Architectural implication:** State store must support concurrent writes from multiple entry points. File locking is fragile; need SQLite WAL mode or dedicated broker.

## Recommended ADRs

| Theme | Recommended ADR | Priority | Blocking UCs |
|---|---|---|---|
| Persistent Session State | ADR-0008: State management strategy (ephemeral vs. durable separation) | High | NF-01, NF-14, PK-08 |
| Graph Query | ADR-0009: Graph database selection (SQLite FTS + manual graph vs. dedicated graph DB) | High | NF-01, NF-14 |
| Async Access | ADR-0010: Concurrent state access model (file locking vs. SQLite WAL vs. broker) | Medium | PK-08 |

## Out of Scope

- **PK-08 Telegram adapter implementation:** Independent concern; its protocol/API design does not share structural needs with NF-01/NF-14 beyond persistent state
- **Cross-project federation (NF-02):** Not yet approved; defer until UC status changes
- **UI/UX for memory browsing:** Product concern, not architectural

## Human Review Questions

1. Do NF-01 and NF-14 truly need graph query, or can they work with flat file + manual link traversal in v1-core?
2. Should ADR-0008 and ADR-0009 be combined (state + storage in one decision)?
3. Is ADR-0010's priority correct given PK-08 is approved but lower priority than NF-01/NF-14?
