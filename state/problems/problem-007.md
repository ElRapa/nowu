---
id: problem-007
source_idea: idea-v1core
source_discovery: disc-v1core
created: 2026-04-07
status: APPROVED
authored_by: perspective-interview@P1.2
reviewed_at:
---

# Problem Statement: problem-007

## Core Problem

Knowledge that accumulates within one project is invisible when working in another. The human is the only connection layer — relying entirely on their own memory to transfer relevant facts, observations, or lessons across project boundaries. Obvious connections are systematically missed: a coconut plantation in the real-estate project that could supply the aperitif business; a scoping lesson learned in software work that applies directly to business planning. Projects grow in isolation rather than compounding from each other.

## Validated Personas

**Primary:** Raphael (the multi-project human) — the value of running multiple projects is supposed to compound; instead, each project is informationally siloed and the human carries the entire cross-project awareness burden alone.

## Confirmed Outcome Goals

1. When working within one project's context, the system surfaces relevant knowledge from other projects — entities, facts, and decisions that overlap semantically — without the human needing to remember the connection exists.
2. The human evaluates each suggested cross-project connection and either links it deliberately or dismisses it (low cost); connections are never forced.
3. The multi-project knowledge base becomes meaningfully richer than the sum of its individual project knowledge bases — cross-project compounding is observable, not just possible.

## Flagged Assumptions (resolved)

| Assumption | Resolution | Impact |
|---|---|---|
| Cross-project connections will be valuable more often than they are distracting | Needs investigation — this is the primary adoption risk. Mitigation: surfacing must be relevance-gated with a dismissible UI (not interrupting work flow). Signal-to-noise ratio must be tracked and surfacing reduced if dismissal rate is high. | Highest-risk assumption; monitored post-delivery; noise threshold must be set conservatively |
| Semantic similarity is sufficient to detect meaningful cross-project connections | Partially accepted — entity overlap (same supplier, same ingredient, same domain concept) is likely more reliable than pure semantic similarity for v1-core. The approach decision is deferred to P3/S2. | Affects P3 architecture signal: entity-matching approach vs. embedding-based approach |

## Appetite

- [ ] Tiny (< 2 h)
- [x] Small (< 1 day)
- [ ] Medium (2-3 days)
- [ ] Large (up to 1 week)

**Rationale:** XP-01 is a single, well-defined capability: discover and surface cross-project connections. The complexity is in the detection mechanism (which is an architecture decision, not a problem-level concern) and the UI for surfacing (which is minimal in v1-core — a suggestion the human can act on or dismiss). This is achievable as a Small problem.

## Out of Scope (explicit)

1. Automated lesson transfer between projects (XP-03 — v1.1 scope).
2. Handling conflicting high-confidence knowledge across projects (XP-04 — v1.1 scope).
3. Proactively surfacing knowledge without the human being in a relevant context (PK-02 — v1.1 scope).
4. Performance at scale beyond the first 6 months of knowledge accumulation (XP-05 — v2 scope).
5. Creating explicit, permanent cross-project links — v1-core surface is suggestive, not structural.

## Success Criteria

1. While working in one project, the system surfaces at least one semantically relevant item from another project in a context where the connection is genuinely useful — verified across at least 3 distinct cross-project scenarios from the AP, RE, and NF projects.
2. The human can act on a suggested cross-project connection (link it, explore it, or dismiss it) within their current session without switching project contexts.
3. The dismissal rate for surfaced cross-project connections stays below 70% (i.e., more than 30% of surfaced connections are acted on as useful) — measured over the first month of active multi-project use.

## Dependencies

Requires: problem-005 to be resolved first. Cross-project discovery requires at least two independent projects to exist with their own knowledge stores. The bootstrap mechanism (problem-005 / NF-07) must be operational before multiple projects can be active simultaneously. This problem is further in natural sequence than problems 001–005 but does not require problem-006 (personal capture) to be complete.

## Prior Art — `know` library

A knowledge layer implementation already exists in the `know` workspace (`/Projects/know`). It covers graph-based atom storage, subgraph queries, and entity-level relationships. Before P3 makes any architecture decisions for XP-01, the constraint-check agent and architecture-design agent **must** review:

- The `know` ADRs (`docs/adr/`) — especially ADR-0001 (task vs action), ADR-0003 (subgraph serialisation), ADR-0004 (know adapter scope).
- The existing adapter interface (`src/know/adapter.py`) and its nowu integration contracts (`docs/framework/NOWU_KNOW_USAGE_CONTRACTS.md`).
- Any prior analysis of entity-matching vs. semantic similarity approaches in the `know` codebase.

P3 must treat `know` as the primary candidate implementation for XP-01's detection layer, and either adopt, extend, or explicitly reject it with rationale in a new ADR.

## UC Coverage

- XP-01: Discover Connections Across Projects Automatically
