---
id: ADR-0007
title: Session Continuity Protocol
date: 2026-05-07
status: PROPOSED
epistemic_grade: HYPOTHESIS
superseded_by: ~
source_synthesis: SYNTHESIS-001
source_themes: [T1, T2, T4]
source_ucs: [NF-01, NF-10, NF-16, PK-03, PK-08, AP-05, RE-06]
depends_on: [ADR-0008]
---

# ADR-0007: Session Continuity Protocol

## Status

PROPOSED (HYPOTHESIS grade) — Derived from SYNTHESIS-001 Theme T1 (Continuity). Depends
on ADR-0008 (session state uses knowledge atoms). Will be validated through first S1-S9
intake (W4). The existing `state/SESSION_STATE.md` bookmark and `SessionSnapshot` contract
provide the starting point.

## Context

SYNTHESIS-001 identifies T1 (Continuity) as a critical theme: the system must answer
"Where are we, what did we decide, and what should we do next?" — instantly, correctly,
without reconstruction. NF-01 (Resume Work After Context Loss) is a v1-core UC that
explicitly depends on session recovery.

Current state:
- `state/SESSION_STATE.md` exists as a human-readable bookmark with YAML fields
  (`current_step`, `current_ids`, `focus_summary`, `next_checkpoint`, `last_updated`).
  It is explicitly labeled "NOT a source of truth."
- `core/contracts/types.py` defines a `SessionSnapshot` frozen dataclass with minimal
  fields: `session_id`, `active_project`, `active_role`, `next_action`, `blockers`.
- `core/contracts/session.py` defines `SessionStore` Protocol with `load()` and `save()`.
- WORKFLOW.md S0 instructs agents to read `SESSION_STATE.md` at session start.
- An archived design note (`docs/archive/adr/ADR-002-wal-and-session-summary-atom-strategy.md`)
  discusses WAL semantics and summary-atom sync to `know`.

What's missing:
- **No defined checkpoint schema** — what fields must survive a crash?
- **No recovery protocol** — what steps does an agent follow to resume?
- **No checkpoint frequency** — when are checkpoints written?
- **No human orientation protocol** — how does NF-10 "maintain the thread" get delivered?
- **No cross-project orientation** — PK-03 "today view" has no checkpoint support.

## Decision

### Two-Layer Checkpoint Architecture

Session continuity operates at two layers, serving different consumers:

| Layer | Format | Consumer | Source of Truth? | Survives Crash? |
|-------|--------|----------|-----------------|-----------------|
| **Machine checkpoint** | `SessionSnapshot` (JSON) | Agents, `SessionStore` | Yes — authoritative recovery state | Yes (file-based) |
| **Human bookmark** | `state/SESSION_STATE.md` (YAML) | Human, S0 orientation | No — convenience view | Yes (file-based) |

Both are written at the same checkpoints. The machine checkpoint is the recovery anchor.
The human bookmark is a formatted view for orientation.

### Machine Checkpoint Schema (Extended SessionSnapshot)

The existing `SessionSnapshot` dataclass is extended for recovery needs:

```
SessionCheckpoint:
  # Identity
  checkpoint_id: str          # UUID, monotonically increasing per session
  session_id: str             # Links to session across checkpoints
  timestamp: str              # ISO 8601

  # Position in workflow
  active_project: str         # Project scope
  active_step: str            # P0-P4 or S1-S9
  active_role: RoleName       # Which agent role is active
  active_ids:                 # References to current artifacts
    intake_id: str | None
    task_id: str | None
    decision_id: str | None

  # Recovery state
  next_action: str            # What should happen next (1-2 sentences)
  blockers: list[str]         # What's preventing progress
  completed_steps: list[str]  # Steps completed in this cycle (e.g., ["S1", "S2", "S3"])
  last_artifact_path: str     # Path to most recent output artifact

  # Epistemic metadata (from ADR-0010)
  checkpoint_grade: EpistemicGrade  # Grade of the checkpoint itself (auto: INFORMED_ESTIMATE)
```

**Storage:** JSON file at `state/sessions/{session_id}/checkpoint-latest.json`.
Previous checkpoints retained as `checkpoint-{checkpoint_id}.json` for audit trail.

### Human Bookmark Schema (Unchanged)

`state/SESSION_STATE.md` retains its current format. It is written as a formatted
projection of the machine checkpoint:

```yaml
current_step: S3
current_ids:
  intake_id: intake-001
  task_id: ~
  decision_id: ~
focus_summary: |
  Evaluating 3 options for knowledge atom storage strategy.
  Waiting for human review of options sheet.
next_checkpoint: |
  Human reviews options sheet at S4 gate.
last_updated: 2026-05-07T14:30:00Z
```

### Checkpoint Frequency

Checkpoints are written at **step boundaries** — not on every operation:

| Event | Checkpoint? | Rationale |
|-------|-------------|-----------|
| Step completion (S1→S2, S5→S6, etc.) | **Yes** | Natural boundary, recovery tolerates re-running one step |
| Human approval gate (S4, S5 gates) | **Yes** | Human decisions must survive crashes |
| Before long LLM calls (>30s expected) | **Yes** | Prevents losing context on timeout/crash |
| Within a step (mid-implementation) | **No** | Recovery re-runs the step; checkpointing mid-step adds complexity without value at v1-core |
| S9 Capture complete | **Yes + rotate** | Cycle complete; archive checkpoint, clear bookmark |

**Recovery tolerance:** If a crash occurs mid-step, recovery re-runs the entire step
from its input artifact. This is acceptable because:
- Steps are bounded (< 4 hours each, typically < 30 minutes)
- Input artifacts are immutable once written
- The cost of re-running one step is low vs. the complexity of mid-step checkpointing

### Recovery Protocol

When an agent starts or resumes:

```
1. LOAD checkpoint
   → Try SessionStore.load() for machine checkpoint
   → If missing, parse state/SESSION_STATE.md as fallback
   → If both missing, start fresh (no prior session)

2. VALIDATE checkpoint
   → Verify referenced artifacts exist (intake_id, task_id)
   → If artifact missing/corrupted: flag to human, route to S1
   → Check checkpoint age: if > 7 days, recommend health check first

3. ORIENT (for human)
   → Generate 3-5 sentence summary:
     "We are at [step] of [intake]. Last completed: [step].
      Next action: [next_action]. Blockers: [blockers]."
   → Present to human at S0/S1 for confirmation

4. RESUME
   → Human confirms or redirects
   → Agent picks up from next_action at active_step
```

**Recovery SLA:** Agent proposes next action within 5 minutes of session start
(per QA metric from `qa-elicitation.md`).

### Cross-Project Orientation (NF-10, PK-03)

For multi-project humans, the "today view" aggregates checkpoints across projects:

```
For each project with an active checkpoint:
  → Load checkpoint
  → Extract: project name, active_step, next_action, blockers, last_updated
  → Sort by last_updated (most recent first)
  → Present as "Today View" summary
```

This is a read-only aggregation. Each project's checkpoint is independent — no
cross-project state coupling.

### Integration with `know` (Durable Memory)

At S9 Capture, the session's key decisions and learnings are promoted to knowledge atoms
in `know` (per ADR-0008). The session checkpoint itself is NOT an atom — it is transient
operational state. The distinction:

| Concern | Session Checkpoint | Knowledge Atom |
|---------|-------------------|----------------|
| Purpose | Recovery after crash/interruption | Durable cross-session memory |
| Lifetime | Active session only; archived after S9 | Persists indefinitely (with decay) |
| Consumer | Agents resuming work | Agents reasoning about past work |
| Example | "We're at S3, evaluating options" | "D-021: We chose option B because..." |

The curator (S9) is responsible for extracting durable knowledge from the session
and creating atoms. The checkpoint is discarded (archived) after capture.

## Rationale

1. **Two-layer separation:** Machine checkpoints need to be parseable and small. Human
   bookmarks need to be readable and contextual. Combining them into one format forces
   compromises in both directions.

2. **Step-boundary checkpointing:** Mid-step checkpointing adds complexity (partial state
   serialization, incremental recovery) without proportional value. Steps are short enough
   that re-running from the input artifact is acceptable.

3. **Checkpoint ≠ Atom:** Session checkpoints are operational state (where are we NOW).
   Knowledge atoms are durable memory (what did we LEARN). Conflating them pollutes the
   knowledge graph with transient operational data.

4. **File-based persistence:** Aligns with D-001 (file-based memory). No database
   dependency for recovery. JSON files in `state/sessions/` are version-controllable
   and inspectable.

## Consequences

**Positive:**
- Crash recovery is deterministic: load checkpoint → validate → resume
- Human orientation is instant: read bookmark → understand state
- Cross-project "today view" is an aggregation query over checkpoints
- Existing `SessionStore` Protocol and `SessionSnapshot` contract provide the API surface

**Negative:**
- Two representations (checkpoint + bookmark) must stay synchronized
- Step-boundary checkpointing means losing up to one step's work on crash
- Checkpoint files accumulate in `state/sessions/` — need cleanup policy

**Neutral:**
- `SessionSnapshot` dataclass in `core/contracts/types.py` will need to be extended to
  match the `SessionCheckpoint` schema (add `active_step`, `active_ids`, `completed_steps`,
  `last_artifact_path`, `checkpoint_grade`)
- The archived WAL concept (`docs/archive/adr/ADR-002-*`) is superseded by this ADR's
  step-boundary approach. Fine-grained WAL may be reconsidered at v1.1 if step-boundary
  granularity proves insufficient.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Two-layer checkpoint (recommended) | Serves both agents and humans; file-based; simple recovery | Two representations to sync | **Selected** — serves distinct consumers |
| Single combined checkpoint (YAML only) | One file, simple | Machine parsing of YAML is fragile; human readability constrains schema | Forces compromise between machine and human needs |
| WAL (Write-Ahead Log) with replay | Fine-grained recovery, no lost work | Complex replay logic, event ordering, state reconstruction | Over-engineered for v1-core; steps are short enough to re-run |
| Database-backed session state | Fast queries, structured | Adds DB dependency for recovery; violates D-001 file-first | Recovery should work without DB; file-based is sufficient |
| No formal protocol (current state) | Zero effort | NF-01 is unimplementable; crash recovery is ad-hoc | Fails the fundamental v1-core requirement |

## Related

- synthesis: SYNTHESIS-001 (Theme T1)
- arch_vision: docs/architecture/ARCHITECTURE-VISION.md (Principle P2, QA #1 Continuity)
- decisions: D-001 (file-based memory), D-009 (role-driven workflow)
- adrs: ADR-0008 (session state references atoms), ADR-0006 (soul↔flow via filesystem)
- depends_on: ADR-0008 (session decisions promoted to atoms at S9)
- depended_on_by: ADR-0009 (orchestration needs checkpoint for handoff state)
- supersedes: docs/archive/adr/ADR-002-wal-and-session-summary-atom-strategy.md (design notes)
