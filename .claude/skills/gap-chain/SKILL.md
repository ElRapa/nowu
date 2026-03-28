---
name: gap-chain
version: 1.0
mode: high-altitude
---

# Skill: GAP Chain (Global Architecture Pass Automation)

## Purpose

Orchestrate the Global Architecture Pass (GAP) at the **HIGH altitude**:
detect when a GAP is needed, analyse the global architecture, and apply
approved changes to the canonical architecture docs via a controlled,
human-gated chain.

This skill glues three agents together:

- `gap-detector`  → writes/updates `state/arch/gap-trigger.md`
- `gap-analyst`   → writes `state/arch/global-pass-YYYY-MM-DD.md`
- `gap-writer`    → applies APPROVED global-pass to context/containers/ADRs

## When to use

- After `health-sweep` reports architecture or vision as RED and suggests P3.
- After a product stage change in `docs/V1_PLAN.md`.
- When you explicitly suspect global architecture drift or scope expansion.

## Inputs

- `docs/vision.md`
- `docs/V1_PLAN.md`
- `docs/USE_CASES.md`
- `docs/architecture/context.md` (if exists)
- `docs/architecture/containers.md` (if exists)
- `docs/architecture/adr/*.md` (if exists)
- `docs/DECISIONS.md` (if exists)
- `state/health/health-*.md`
- `state/arch/gap-trigger.md` (if exists)
- `state/arch/global-pass-*.md` (if exists)

## Outputs

- `state/arch/gap-trigger.md`          # OPEN or CLEAR, RECOMMENDED/NOT_RECOMMENDED
- `state/arch/global-pass-YYYY-MM-DD.md`  # PROPOSED → APPROVED → APPLIED
- Updated:
  - `docs/architecture/context.md`
  - `docs/architecture/containers.md`
  - `docs/architecture/adr/ADR-NNN-*.md`
- Updated statuses in `gap-trigger.md` and `global-pass-YYYY-MM-DD.md`.

## Orchestration steps

1. **G0 — Run gap-detector**

   - Invoke `gap-detector` once for this product.
   - It reads vision/plan/health and writes/updates `state/arch/gap-trigger.md`.

2. **Human review of gap-trigger**

   - Open `state/arch/gap-trigger.md`.
   - If `status: CLEAR` or `verdict: NOT_RECOMMENDED` → stop; no GAP.
   - If `status: OPEN` and `verdict: RECOMMENDED` → proceed to G1.

3. **G1 — Run gap-analyst**

   - Invoke `gap-analyst` once, with scope inferred from gap-trigger.
   - It reads vision/plan/UCs/architecture/ADRs and writes
     `state/arch/global-pass-YYYY-MM-DD.md` with `status: PROPOSED`.

4. **Human review of global-pass**

   - Read `global-pass-YYYY-MM-DD.md` carefully.
   - Optionally, author ADRs for each ADR candidate.
   - If acceptable, change `status: PROPOSED` → `status: APPROVED`.

5. **G2 — Run gap-writer**

   - Invoke `gap-writer` for that date.
   - It verifies `status: APPROVED`, then:
     - Updates `context.md` and `containers.md` (deltas or FULL_RESET).
     - Drafts ADR stubs for any remaining ADR candidates.
     - Sets `gap-trigger.md status: CLOSED`.
     - Marks `global-pass-YYYY-MM-DD.md status: APPLIED`.

6. **Post-GAP health check**

   - Run `health-check architecture` to confirm architecture is GREEN.
   - Optionally run `health-sweep` again to recompute entry point.

## Hard constraints

- This skill never bypasses human gates:
  - Human must explicitly proceed from G0→G1 and approve before G2.
- Never run `gap-writer` while `global-pass-*` has `status: PROPOSED`.
- Never attempt a GAP if `docs/vision.md` is missing or not APPROVED:
  run `P0.VISION` first.
- GAP is a HIGH altitude operation; do not load `src/`, `tests/`,
  `state/problems`, `state/stories`, or `state/tasks` here.
