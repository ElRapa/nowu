---
id: 002-decomp
source_idea: idea-002
generated_at: 2026-04-06T00:00:00Z
agent_version: idea-decomposition@2.2
---

# Idea Decomposition: 002

## Classification

size: STORY
recommended_mode: Lite (P0 + P2 + P4)
confidence: HIGH

## Stage Assessment

current_stage: Stage 1 — Foundation (Step 02 Memory Integration Layer, In Progress)
idea_stage_fit: ALIGNED
stage_flag: none — this is a developer/operator experience improvement that directly
  supports dogfooding. nowu's 6-month success horizon explicitly calls out "clear
  feedback, visible progress" and "low friction". Since nowu runs its own development
  using itself, workflow clarity is load-bearing for forward momentum, not a cosmetic
  addition. Shipping it now costs < 1 day and unblocks ongoing use.

## Routing Recommendation

This is a single, bounded story: show the current workflow stage (S1–S9 step or
pre-workflow phase) and what is next/done when the user runs `/workflow status`. It
delivers one outcome for one user (Raphael dogfooding nowu) in one interaction.
Run **Lite mode** (P0 → P2 → P4): P0 confirms alignment with vision and V1_PLAN,
P2 maps the one story with acceptance criteria, P4 produces the intake brief ready
for S1. No architecture spike needed — the `/workflow status` command already exists
in CLAUDE.md; this story enhances its output, not its architecture.

## Human Action Required

Review and set `status: APPROVED` on this decomp, then run `/pre-workflow resume 002 --from P2` to produce the story and intake brief.
