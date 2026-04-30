---
id: 001-decomp
source_idea: idea-001
generated_at: 2026-04-06T00:00:00Z
agent_version: idea-decomposition@2.2
---

# Idea Decomposition: 001

## Classification

size: EPIC
recommended_mode: Full (P0 + P1 + P2 + P3 + P4)
confidence: MEDIUM
confidence_note: The idea bundles three distinct concerns (context scoping, data
  governance / rights, and index compliance). Each could be a story in one epic, but
  the governance dimension — access rights and enforcement — may grow into its own epic
  once discovery clarifies scope. P1 discovery is needed to bound it properly.

## Stage Assessment

current_stage: Stage 1 — Foundation (Step 02 Memory Integration Layer, In Progress)
idea_stage_fit: PREMATURE
stage_flag: |
  Scoping and data governance sit comfortably in Stage 2 (Core Loop) or Stage 3
  (Hardening), not Stage 1. The core session runtime, memory layer, and WAL are not
  yet complete. Implementing access rights before the core read/write surface is stable
  risks re-work and premature API lock-in.

  The "Why Now?" note in the idea itself confirms this: "Implementation should happen
  later as we don't address data-restriction yet."

  RECOMMENDED ACTION BEFORE PROCEEDING:
  Run this idea through **architecture-only mode (Mode D: S1→S4+S9)** instead of
  a full implementation workflow. The goal is to record an ADR that names the
  scoping and governance principles as architectural constraints — so future
  implementation steps cannot contradict them — without writing any code or tests now.
  No intake brief needed; an architecture-only spike produces a decision record that
  binds Stage 2+ work.

## Routing Recommendation

Do not queue this idea for implementation now. Instead, run an architecture-only spike
(Mode D) to answer one question: what are the non-negotiable scoping and governance
principles that Stage 2 and Stage 3 implementation must honour? The output is a single
ADR in docs/architecture/adr/, not a task spec. This takes < half a day and closes
the risk of accidental architectural contradiction as Stage 1 continues. When Step 03
(Session Runtime) is done and Stage 2 begins, revisit this decomp and promote the idea
to FULL mode for proper epic shaping and implementation.

## Human Action Required

Decide: run architecture-only spike (Mode D) now to lock in scoping/governance
principles as a binding ADR, or park this idea until Stage 2 begins. Set
status: APPROVED or status: PARKED on this decomp before proceeding.
