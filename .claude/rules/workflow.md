# Workflow Rules

## 9-Step Cycle (see docs/WORKFLOW.md for full spec)
S1 Intake → S2 Constraints → S3 Options → S4 Decision →
S5 Shape  → S6 Implement   → S7 VBR     → S8 Review   → S9 Capture

## Handoff Status Enum
DRAFT | READY_FOR_ARCH | READY_FOR_OPTIONS | READY_FOR_DECISION |
READY_FOR_SHAPING | READY_FOR_IMPL | READY_FOR_VBR | READY_FOR_REVIEW |
READY_FOR_CAPTURE | DONE | CHANGES_REQUESTED | BLOCKED

## Approval Tiers
- **Tier 1** (auto): tests, docs, refactors following ADRs — just do it
- **Tier 2** (batch): feature impl, design changes, new deps — create pending/ entry
- **Tier 3** (block): merge to main, breaking change, new ADR, delete — STOP + ask

## Execution Modes
A: Full Cycle (S1→S9)  |  B: Implement Loop (S5→[S6-S7]×n→S8-S9)
C: Single Step (S6-S9)  |  D: Architecture Only (S1→S4→S9)
