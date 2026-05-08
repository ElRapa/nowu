# nowu Bootstrap — ARCHITECTURE Altitude

**Use this for:** ADRs, module design, contracts, hypothesis ADRs, orchestrator implementation.

## Read in this exact order

### Core Identity (minimal)
1. `docs/vision.md`                        — product vision (read Section 1 only)

### Workflow Model (always)
2. `docs/model/MODEL-REFERENCE.md`         — 5x10 altitude-phase model
3. `docs/model/WORKFLOW-STANDARDS.md`      — binding workflow rules

### Decisions (always)
4. `docs/DECISIONS.md`                     — all D-NNN decisions (binding)

### Architecture Context (altitude-specific)
5. `docs/architecture/containers.md`       — module map (C4 L2)
6. `docs/architecture/context.md`          — system context (C4 L1)
7. `docs/architecture/adr/` — run `ls`     — list all ADRs
8. Read all ADRs with status ACCEPTED (ADR-0001 through ADR-0006)
9. Skim PROPOSED/HYPOTHESIS ADRs (ADR-0007 through ADR-0010) for awareness

### Strategic Context (for alignment)
10. `docs/STAGED-PLAN.md`                  — current implementation roadmap
11. `state/arch/SYNTHESIS-001.md` (if exists) — architectural themes
12. `docs/architecture/ARCHITECTURE-VISION.md` (if exists) — architectural principles, risks

### State (awareness)
13. `state/sessions/` — run `ls`            — checkpoint storage per ADR-0007 (checkpoint storage per ADR-0007, may be empty until first session)

### Tools & Verification
14. `CLAUDE.md`                            — commands, approval tiers
15. `docs/model/VERIFICATION-GUIDE.md`     — how to verify ADRs

## What You NEVER Load at This Altitude
- `src/` or `tests/` — no code during pure architecture work (prevents anchoring bias). Exception: when implementing architectural contracts/types, load only `src/nowu/core/contracts/`.
- `state/tasks/` — no implementation tasks (architecture precedes shaping)
- `state/SESSION_STATE.md` — session bookmark, not relevant to architecture

## Before Proceeding
Verify: ☐ I know the 5 modules and their import rules ☐ I loaded all ACCEPTED ADRs ☐ I know which roadmap stage is active. If any unclear, re-read the relevant file above.
