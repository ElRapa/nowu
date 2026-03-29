---
id: ADR-006
status: PROPOSED
title: Health metrics collection architecture
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-006)
priority: at Stage 2 gate
---

# ADR-006 — Health metrics collection architecture

## Status

PROPOSED

## Context

NF-08 (Measure and Visualize Framework Health) requires a mechanism for collecting and surfacing health metrics. NF-09 (Ensure Every Deliverable Traces Back to a Use Case) requires that health signals be machine-verifiable — which implies a code path, not just agent-generated Markdown reports.

Currently, health checks are entirely agent-driven (health-sweep, health-vision, health-architecture, health-goals, health-use-cases agents producing `state/health/*.md` files). This is operational and sufficient for Stage 1 solo development, but it is not machine-verifiable: no code path emits or reads health signals, so NF-09's traceability requirement cannot be satisfied automatically for NF-08.

This ADR decides the architectural home for health metric collection and storage.

**Priority:** Needed before Stage 2 begins; not blocking Stage 1 completion.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) Agent-only (current state — VS Code agent workflow, no code path)**
Health checks remain purely operational: agents read files, produce Markdown reports, and the human reviews the status. Zero engineering cost. NF-08 is "verifiable" only by human reading the report. Does not satisfy NF-09 for the health domain. Acceptable for Stage 1; becomes a gap at Stage 2 when automation maturity is expected.

**(B) `bridge health` command that queries `know` for structured metrics**
`bridge` gains a `health` command. After each completed workflow cycle, `flow` (or a `bridge` hook) writes structured health metrics as atoms to `know` (e.g. DECISION atoms tagged `type=health_metric`). `bridge health` queries and displays them. Machine-verifiable; integrates with the existing `know`-as-state-store model. Requires health metric schema design and `know` write hooks in `flow`.

**(C) A metrics-collection hook in `flow` that writes health atoms after each session**
`flow` gains a post-session hook (triggered by S9 curator) that computes and writes health metric atoms to `know`. No new `bridge` command needed for collection, only for display. Cleaner separation: `flow` writes, `bridge` (or later `dash`) reads and displays. More testable than option B; the hook is a first-class part of the session lifecycle.

## Consequences

[HUMAN TO COMPLETE]
