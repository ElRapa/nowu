---
name: health-sweep
version: 2.1
mode: health
---

# Skill: Health Sweep (Vision, Goals, Architecture, Use Cases)

## Purpose

Run all strategic health checks in one pass and suggest the best starting
point for the next work cycle (P0.VISION, P0.UC, P1, or P3).

This skill is **read-only**. It invokes health agents, aggregates their
findings, and produces a single routing recommendation.

## When to use

- Before starting a new pre-workflow run for a product.
- After a major release or architecture change.
- When work feels misaligned but it is unclear **where**.

## Agents invoked

- `health-vision`          # checks docs/vision.md
- `health-goals`           # checks goals vs stories/intakes
- `health-architecture`    # checks ARCHITECTURE/DECISIONS vs recent work
- `health-use-cases`       # checks USE_CASES vs vision/plan/work

Each agent writes its own report under `state/health/`.

## Inputs

- Product-level docs and state, as required by each health agent.
- No S1–S9 implementation details beyond what the health agents
  already consume.

## Outputs

1. Individual reports (from agents):

   - `state/health/health-vision-YYYY-MM-DD.md`
   - `state/health/health-goals-YYYY-MM-DD.md`
   - `state/health/health-architecture-YYYY-MM-DD.md`
   - `state/health/health-use-cases-YYYY-MM-DD.md`

2. Aggregated sweep result:

   - `state/health/health-sweep-YYYY-MM-DD.md`

## Orchestration steps

### 1. Run individual health agents

Invoke, in any order:

- `health-vision`
- `health-goals`
- `health-architecture`
- `health-use-cases`

Wait for all four reports to be written to `state/health/`.

### 2. Aggregate results

Read the latest health files for today (or most recent date):

- `state/health/health-vision-*.md`
- `state/health/health-goals-*.md`
- `state/health/health-architecture-*.md`
- `state/health/health-use-cases-*.md`

Extract from each:

- `overall_status`
- Any explicit “Recommended Actions” sections.

### 3. Classify overall health

Apply this rule:

- If any report is `RED` → sweep `overall_status = RED`.
- Else if any report is `YELLOW` → sweep `overall_status = YELLOW`.
- Else → sweep `overall_status = GREEN`.

### 4. Suggest starting point for next cycle

Use this decision table:

- If `health-vision` is YELLOW/RED → recommend **start at P0.VISION**.
- Else if `health-use-cases` is YELLOW/RED → recommend **start at P0.UC**.
- Else if `health-goals` is YELLOW/RED → recommend **start at P1**
  (discovery + problem reframe).
- Else if `health-architecture` is YELLOW/RED → recommend **start at P3**
  (constraint-check + architecture-bootstrap).
- Else → recommend **start directly at P2/P4 or S1**, depending on
  backlog state (describe briefly in notes).

### 5. Write aggregated sweep file

Create `state/health/health-sweep-YYYY-MM-DD.md` with this schema:

```markdown
# Health Sweep — YYYY-MM-DD

overall_status: GREEN | YELLOW | RED

## Component Status

- vision:          GREEN | YELLOW | RED
- goals:           GREEN | YELLOW | RED
- architecture:    GREEN | YELLOW | RED
- use_cases:       GREEN | YELLOW | RED

## Recommended Entry Point

entry_point: P0.VISION | P0.UC | P1 | P3 | DIRECT-IMPLEMENT

rationale:
- [short bullets explaining why this entry point was chosen]

## Notable Findings

Summarize key findings from each report (3–8 bullets total), with
references to specific health files and artifacts where helpful.

## Follow-up Actions

List 3–7 specific, actionable steps, e.g.:

1. "Run P0.VISION to update docs/vision.md based on X"
2. "Run P0.UC / use-case-agent to refresh docs/USE_CASES.md"
3. "Re-run P3 architecture-bootstrap for problem-NNN/epic-NNN"
