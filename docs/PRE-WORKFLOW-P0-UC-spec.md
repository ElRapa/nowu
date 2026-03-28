---
id: P0.UC
name: Use Case Catalog Maintenance
scope: Above C4 (problem space, jobs-to-be-done)
actor: use-case-agent + human
timebox: 20–40 minutes
---

# P0.UC — Use Case Catalog Maintenance

## Purpose

Keep `docs/USE_CASES.md` **aligned** with:

- The current `docs/vision.md`
- The current `docs/V1_PLAN.md`
- Recent problems, epics, stories, and captures

so that discovery (P1), story mapping (P2), and S1–S9 always operate against
a small, clear list of jobs-to-be-done.

## When to run

- When a new product repo is created (no `docs/USE_CASES.md` yet).
- After a significant vision or plan change.
- When a health-check (goals/vision) or the human suspects UC drift.
- Before starting discovery for a **new stage** of the product.

## Inputs

- `docs/vision.md`
- `docs/V1_PLAN.md` (if exists)
- `docs/USE_CASES.md` (if exists)
- Optionally:
  - `docs/PROGRESS.md`
  - Latest `state/problems/`, `state/epics/`, `state/stories/`, `state/capture/`

## Outputs

- If no UC catalog exists:
  - `docs/USE_CASES.md` (initial catalog, version 1.0)
- If updating:
  - `docs/USE_CASES.proposed.md` (for human review and adoption)

## Steps

1. Human (optional, 2–5 minutes)
   - Skim `docs/vision.md` and `docs/V1_PLAN.md`.
   - Decide whether this run is:
     - **Bootstrap** (first catalog),
     - or **Refresh** (existing catalog).

2. Agent — `use-case-agent` (10–25 minutes wall-clock)
   - Reads inputs.
   - Synthesizes or updates UC catalog per its instructions.
   - Writes `docs/USE_CASES.md` (bootstrap) or `docs/USE_CASES.proposed.md` (update).

3. Human gate (5–10 minutes)
   - If bootstrap:
     - Quickly scan for obviously wrong UCs, then accept as `docs/USE_CASES.md`.
   - If update:
     - Diff `docs/USE_CASES.md` vs `docs/USE_CASES.proposed.md`.
     - Apply, edit, or reject changes.
     - Overwrite `docs/USE_CASES.md` when satisfied.

## Notes

- P0.UC is an **Above C4** phase; it never touches architecture or code.
- Run it **before** P1 for new products or new product stages.
- It is safe to skip when:
  - Vision and plan are stable,
  - UC catalog is < 1 month old,
  - And health checks are GREEN.