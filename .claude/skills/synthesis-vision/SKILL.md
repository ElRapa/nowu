---
name: synthesis-vision
version: 1.0
mode: high-altitude
---

# Skill: Synthesis → Architecture Vision Chain

## Purpose

Orchestrate the SYNTHESIS → Architecture Vision pipeline at **ARCHITECTURE
altitude**: extract cross-cutting themes from use cases, then derive a system
Architecture Vision from those themes. This skill glues two agents together
with a human gate between them.

This skill produces the foundational architecture understanding that all
subsequent work (ADR writing, S1-S9 intakes, implementation) builds upon.

Agents in the chain:
- `synthesis-agent` → writes `state/arch/SYNTHESIS-NNN.md`
- `architecture-vision-agent` → writes `docs/architecture/ARCHITECTURE-VISION.md`

## When to use

- When `docs/USE_CASES.md` is ACCEPTED and no SYNTHESIS exists yet
- When `health-sweep` recommends a full architecture pass starting from SYNTHESIS
- When 10+ new UCs are added or a new domain category appears
- After vision refresh (vision.md version change)
- Explicitly requested by human for foundational architecture work

## Prerequisites

- `docs/USE_CASES.md` exists and status is ACCEPTED
- `docs/vision.md` exists and status is APPROVED
- `docs/goals/goal-*.md` exist (at least one)

## Inputs

- `docs/USE_CASES.md` — Full UC catalog (the PRIMARY input)
- `docs/vision.md` — Product vision
- `docs/goals/goal-*.md` — All goals
- `docs/DECISIONS.md` — Existing decisions (constraint)
- `docs/architecture/adr/*.md` — Existing ADRs (constraint)
- `docs/STAGED-PLAN.md` — Where outputs feed (context)
- `state/arch/SYNTHESIS-*.md` — Previous synthesis if exists (compare/extend)

## Outputs

- `state/arch/SYNTHESIS-NNN.md` — Cross-cutting themes + ADR recommendations
- `docs/architecture/ARCHITECTURE-VISION.md` — System classification + principles + priorities
- `state/arch/session-learnings-synthesis-YYYY-MM-DD.md` — Process learnings (optional)

## Orchestration Steps

### SV0 — Prerequisite Check

- Verify `docs/USE_CASES.md` exists and has status: ACCEPTED
- Verify `docs/vision.md` exists and has status: APPROVED
- Verify at least one `docs/goals/goal-*.md` exists
- If any missing → STOP with clear message about what's needed

### SV1 — Run synthesis-agent

- Invoke `synthesis-agent`
- Agent reads ALL UCs, ALL goals, vision, existing decisions
- Agent produces `state/arch/SYNTHESIS-NNN.md`
- Verify output exists and contains: themes table, UC mapping, ADR recommendations

### SV2 — Human review of SYNTHESIS

**⚠️ HUMAN GATE — Do not proceed without approval.**

Present to human:
- Number of themes found
- Summary of each theme (1-line)
- Any NEW themes not predicted
- ADR recommendation order

Human may:
- APPROVE → proceed to SV3
- REQUEST CHANGES → re-run synthesis-agent with feedback
- REJECT → stop and explain why

### SV3 — Run architecture-vision-agent

- Invoke `architecture-vision-agent`
- Agent reads APPROVED SYNTHESIS + vision + goals
- Agent produces `docs/architecture/ARCHITECTURE-VISION.md`
- Verify output contains: classification, principles, quality attributes, risks, ADR roadmap

### SV4 — Human review of Architecture Vision

**⚠️ HUMAN GATE — Do not proceed without approval.**

Present to human:
- System classification statement
- Principle count and summary
- Quality attribute ranking
- Top 3 risks
- ADR roadmap first 4 items

Human may:
- APPROVE → mark both artifacts as REVIEWED
- REQUEST CHANGES → re-run architecture-vision-agent with feedback
- REJECT → stop and explain why

### SV5 — Capture learnings (optional)

If running for the first time or if significant new insights emerged:
- Document process decisions and anti-patterns observed
- Write to `state/arch/session-learnings-synthesis-YYYY-MM-DD.md`
- This informs future runs of this skill

## Constraints

- DO NOT skip the human gates (SV2, SV4) — these are MANDATORY
- DO NOT modify `src/` or `tests/`
- DO NOT modify existing ADRs (ADR-0001..0006) or decisions (D-001..D-012)
- Both artifacts are produced at HYPOTHESIS grade
- The synthesis-agent MUST read ALL UCs — no sampling
- The architecture-vision-agent MUST derive from evidence, not aspiration

## What Comes After

With SYNTHESIS and Architecture Vision complete, the next steps are:
1. Write hypothesis ADRs (W3) — following the roadmap order in the vision
2. Run first S1-S9 intake (W4) — against the hypothesis architecture
3. Validate or revise hypotheses through implementation feedback

## Relationship to Other Skills

- **gap-chain**: GAP operates on EXISTING architecture. synthesis-vision creates
  the INITIAL architecture understanding. GAP validates/updates it later.
- **health-sweep**: May trigger this skill if architecture health is RED and
  no SYNTHESIS exists.
- **architecture-only**: Operates at per-feature level (S1→S4→S9). This skill
  operates at GLOBAL level (all UCs → all themes).
- **full-cycle**: S1-S9 uses the Architecture Vision as context for decision-making.
  This skill produces what full-cycle consumes.
