# Draft: Proper Roadmap

## Requirements (confirmed)
- Current ROADMAP-001 was created as a side-note, doesn't cover all key artifacts
- Missing coverage: SYNTHESIS-001, ARCHITECTURE-VISION, vision.md, USE_CASES.md
- State files may belong to old plan (V1_PLAN era) — need audit
- Need a session-log that captures where we are, what we did, and why
- Session-log doesn't need to be perfect, just useful and gathering relevant info
- Consider unprocessed learnings from state/learnings/INDEX.md

## Current State Analysis

### What exists:
- **ROADMAP-001.md** (v2, ACTIVE) — Areas × Stages tracker, v1-core focused
- **ROADMAP-002.md** (DRAFT) — roadmap-updater agent output, never finalized
- **session-log.md** (ACTIVE) — 10 entries seeded from git history (2026-03-04 to 2026-05-10)
- **state/learnings/INDEX.md** — 8 entries, 2 recurring patterns

### Key upstream artifacts NOT reflected in roadmap:
- **SYNTHESIS-001** (9 themes from 50 UCs) — DRAFT, HYPOTHESIS grade
- **ARCHITECTURE-VISION** (5 principles, quality attributes, ADR roadmap) — DRAFT, HYPOTHESIS
- **vision.md** (v2.0 APPROVED) — product identity, personas, success horizons
- **USE_CASES.md** (v2.5, 50 UCs, all ACTIVE) — complete UC catalog with stage targets
- **goals/ (4 goal briefs)** — UC mapping and phase coverage sections EMPTY
- **4 epics, 17 stories** — from P1-P4 pre-workflow run (2026-04-08)

### Potentially stale state files:
- `state/PROGRESS.md` — already marked SUPERSEDED ✓
- `state/SESSION_STATE.md` — already marked TEMPLATE ONLY ✓
- `state/health/*.md` — stale, predate 5×10 model (acknowledged in ROADMAP-001)
- `state/intake/intake-002..006.md` — need status check, may be from old plan
- `state/epics/` and `state/stories/` — from P1-P4 (2026-04-08), still valid
- `state/problems/` — from pre-workflow, likely still valid
- `state/ideas/` — mixed status per ROADMAP-001

### Unprocessed research:
- 5×10 refactoring proposal (2026-05-10) — No
- Workflow triage update (2026-05-10) — No
- Research-to-Ship Skillset (2026-05-09) — No
- Document Maintenance Strategy (2026-05-08) — No
- Context Loading Strategy (2026-05-08) — No

## Key Discovery: The Orchestrator Layer Design (D-022)

Three meta-agents exist that together form the "living orientation system":
1. **roadmap-creator** — creates initial roadmap from vision/goals/UCs
   - Expects 7 sections: Stage Structure, Area × Stage Grid, UC-to-Stage Mapping,
     Dependency Graph, Stage Gate Criteria, Risk Register, Current Work Item
2. **roadmap-updater** — integrates new evidence (SYNTHESIS, Arch Vision, stage gates)
   - Produces ROADMAP-NNN+1.md with incremented version
3. **work-scheduler** — read-only, decides what to work on next
   - Reads ROADMAP Section 7 (Current Work Item), Section 4 (Dependency Graph),
     Section 5 (Stage Gates)
   - Outputs READY/BLOCKED/NEEDS_VALIDATION

**Critical insight:** The work-scheduler expects the roadmap to have specific sections
(numbered 2, 4, 5, 7). ROADMAP-001 doesn't follow this structure. A rewrite is needed
not just for completeness but for machine-parseability.

## Technical Decisions
- User prefers: Rewrite from scratch OR living orientation system → BOTH:
  - Rewrite roadmap as foundation (machine-parseable for work-scheduler)
  - Enhance session-log as human orientation layer
- Stale artifact cleanup: DEFERRED to separate task

## Recommended Approach: "Rewrite + Living System"

The roadmap IS the living orientation system when paired with:
1. **ROADMAP-003.md** — fresh rewrite following roadmap-creator's 7-section structure,
   incorporating vision → goals → UCs → SYNTHESIS → Arch Vision full traceability
2. **Enhanced session-log** — restructured for better "where are we" orientation
3. **Goal backfill** — populate empty UC Mapping sections in goal-001..004.md
4. **Unprocessed research triage** — decide which of the 5 unprocessed sessions affect priorities

Together these enable the work-scheduler to actually function.

## Confirmed Decisions
- **Scope:** Full orientation system (roadmap + session-log + goal backfill + research triage)
- **Session-log:** Add status dashboard section (human-readable work-scheduler output)
- **Roadmap:** Rewrite as ROADMAP-003.md following 7-section structure from roadmap-creator
- **Stale cleanup:** DEFERRED to separate task

## Scope Boundaries
- INCLUDE:
  - ROADMAP-003.md (fresh rewrite, 7-section structure, full traceability)
  - Session-log enhancement (add status dashboard section at top)
  - Goal backfill (populate UC Mapping, Phase Coverage in goal-001..004.md)
  - Research triage (process 5 unprocessed sessions, note any priority changes)
  - Mark ROADMAP-001 and ROADMAP-002 as SUPERSEDED
- EXCLUDE:
  - Stale state file cleanup (deferred)
  - Agent definition updates (roadmap-creator/updater/scheduler specs stay as-is)
  - Implementation work (S1-S9 execution)
  - Source code changes

## Open Questions
1. Intakes 002-006: audit as part of research triage, or out of scope?
2. Test strategy: N/A (no code changes, all documentation artifacts)
3. For the status dashboard in session-log, should it reference work-scheduler output format?
