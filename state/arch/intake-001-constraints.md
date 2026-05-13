---
id: intake-001-constraints
intake_id: intake-001
created: 2026-05-12
status: READY_FOR_OPTIONS
arch_pass_ref: ~
---

# Constraints Sheet: intake-001 — Resume Work After Context Loss

> No pre-workflow arch-pass exists for intake-001. Constraints derived cold from
> intake brief, containers.md, DECISIONS.md, ADR-0007, and contracts/ public surface.

---

## Affected Modules

| Module | Container (C4 L2) | Impact | Confidence |
|---|---|---|---|
| `core` | Shared contracts and domain models | modify — extend `SessionSnapshot` dataclass in `core/contracts/types.py` to match `SessionCheckpoint` schema from ADR-0007 | HIGH |
| `flow` | Pipeline orchestrator | add — implement session state read at pipeline start; write checkpoint at step boundaries | HIGH |
| `know` | Knowledge store | query only — S9 curator promotes decisions to atoms; no new `know` interface required for this intake | MED |
| `bridge` | Interface layer | OUT OF SCOPE — human-facing orientation rendering deferred to F6/v1; bridge untouched by this intake | HIGH |
| `soul` | Agent intelligence | OUT OF SCOPE — pattern detection and analysis not required for the v1-core checkpoint mechanism | HIGH |

**Scope note (from S1 annotation, confirmed):** intake declares only NF-01. NF-02, NF-09,
PK-03, XP-01 are co-listed in ROADMAP-003 Step 02 but deferred to later intakes. Narrow
scope is deliberate for workflow validation.

---

## Binding Decisions

| D-ID | Title | How it constrains this work |
|---|---|---|
| D-001 | File-Based Memory Architecture | Checkpoint artifact MUST be file-based (JSON + Markdown). No database for recovery. `state/sessions/` is the required storage path per ADR-0007. No alternative persistence mechanism may be introduced. |
| D-002 | DDD Layer Architecture | All cross-module dependencies go through `core/contracts/*.py`. `flow` reads/writes session state through `SessionStore` Protocol — not directly. Direct filesystem reads of `state/sessions/` by agents are permitted as filesystem-level coupling (not a Python import). |
| D-003 | 5-Module Structure | No new module may be created. Session continuity is implemented within `core` (schema extension) and `flow` (checkpoint write/read logic). `soul` and `bridge` are out of scope for this intake. |
| D-004 | TDD as Non-Negotiable Constraint | Tests written before implementation. 90%+ coverage enforced. `SessionStore` implementation and checkpoint read/write logic must have tests before code. |
| D-006 | `know` as External Memory System | S9 curator step promotes durable decisions to `know` via `KnowledgeBase` instance methods. This intake does NOT write checkpoint state to `know` — checkpoints are transient operational state (per ADR-0007 distinction). |
| D-007 | Integration-First Modular Monolith | No event-driven or microservice patterns. Checkpoint read at session start is a direct synchronous file read inside `flow`. |
| D-015 | Epistemic Grades with Tiered Enforcement | Level 0 enforcement: checkpoint artifact must carry an `epistemic_grade` field (syntax check only). No blocking enforcement at v1-core. |
| D-017 | Minimum Viable Architecture — Hypothesis ADRs | ADR-0007 is HYPOTHESIS grade. This intake is the evidence run that may validate or surface friction with ADR-0007's design. Friction must be documented in S9 capture — do NOT silently adapt the implementation to fit a broken hypothesis. |
| D-023 | Use Cases Must Not Reference Implementation Artifacts | `state/SESSION_STATE.md` is an implementation artifact. It must not be referenced in UC text. Human bookmark path is an ADR-0007 implementation detail, not a UC concern. |

---

## Binding Contracts

| Contract | Interface | Constraint |
|---|---|---|
| `SessionStore` Protocol (`core/contracts/session.py`) | `load() -> SessionSnapshot \| None` / `save(snapshot: SessionSnapshot) -> None` | `flow`'s session read/write MUST go through this Protocol. Callers may not access the filesystem directly for snapshot I/O — that is the concrete implementation's responsibility. |
| `SessionSnapshot` dataclass (`core/contracts/types.py`) | Frozen dataclass: `session_id`, `active_project`, `active_role`, `next_action`, `blockers` | Current schema is UNDERSPECIFIED for recovery needs. ADR-0007 requires extension with: `active_step`, `active_ids`, `completed_steps`, `last_artifact_path`, `checkpoint_grade`. The extension must remain a frozen dataclass (or be superseded by a new `SessionCheckpoint` type). Breaking `SessionSnapshot`'s existing interface is a Tier 3 action — requires explicit decision in S4. |
| `RoleOrchestrator` Protocol (`core/contracts/session.py`) | `next_role(current: RoleName) -> RoleName` | Relevant to `flow`'s pipeline; does not need modification for this intake but must not be broken by session state changes. |
| `core/contracts/__init__.py` | Currently empty (1-line module) | Any new public contract types introduced by this intake (e.g., `SessionCheckpoint`) must be exported through this surface if consumed by other modules. |

---

## Architectural Risks

| Risk | Severity | Mitigation |
|---|---|---|
| **Schema extension breaks `SessionSnapshot` frozen dataclass.** ADR-0007 requires 5 new fields. Extending a frozen dataclass is non-trivial in Python — either migration logic or a new type is needed. If `SessionSnapshot` is already used by `flow` internals, adding required fields without defaults is a breaking change. | HIGH | S3 must evaluate: (a) extend with Optional/defaulted fields, (b) introduce new `SessionCheckpoint` type alongside existing `SessionSnapshot`, or (c) replace `SessionSnapshot` entirely. Option (b) is safest for v1-core. S4 decision required before any contract change. |
| **`state/SESSION_STATE.md` is a template-only file, never populated.** The human bookmark exists as a schema template but has no runtime writer. AC-2 (humans receive clear signal of where things stand) has no current implementation path at all. | HIGH | This intake must implement the writer — either in `flow`'s step-boundary logic or as a side effect of `SessionStore.save()`. The path must be confirmed in S3. |
| **ADR-0007 HYPOTHESIS grade may prescribe over-specified behavior.** The two-layer checkpoint design, step-boundary frequency, and recovery protocol are HYPOTHESIS. Implementing them naively risks building too much for an 8h appetite. | MED | S3 must draw a clear "v1-core slice" from ADR-0007. The minimum to satisfy AC-1, AC-2, AC-3 may be smaller than full ADR-0007 compliance. Flag any friction in S9 capture per D-017. |
| **No hallucination guard (AC-3) has an explicit contract.** "Agent reads from artifact, not from its own inference" is an agent behavioral constraint, not a software contract. It cannot be enforced at runtime in v1-core. | MED | Implementation must ensure the agent prompt at session start explicitly loads the checkpoint artifact content and presents it before any reasoning. This is a prompt-design and flow-orchestration concern, not a data-model concern. S3 should address. |
| **`state/sessions/` directory does not exist.** ADR-0007 specifies `state/sessions/{session_id}/checkpoint-latest.json` as the storage path. This path is not yet present in the repo. | LOW | `flow`'s `SessionStore` implementation creates the directory on first write. S5 shaper must include this in `in_scope_files`. |
| **`docs/PROGRESS.md` does not exist.** S9 curator cannot capture progress to a non-existent file. S1 surfaced this as an open question. | LOW | S9 creates `docs/PROGRESS.md` as part of this intake's capture step. S5 must include it in scope. |

---

## Assumptions

| Assumption | Validated | Notes |
|---|---|---|
| `SessionStore` Protocol exists in `core/contracts/session.py` | TRUE | Confirmed. `load()` and `save()` signatures present. |
| `SessionSnapshot` dataclass exists in `core/contracts/types.py` | TRUE | Confirmed. 5 fields: `session_id`, `active_project`, `active_role`, `next_action`, `blockers`. |
| `state/SESSION_STATE.md` is an existing contract artifact | FALSE | File exists but is a template-only placeholder, explicitly labeled "never populated with real data." It is NOT a source of truth. It IS the human bookmark format from ADR-0007 — but has no runtime writer. |
| "Last verified checkpoint" has a defined schema | PARTIAL | ADR-0007 defines `SessionCheckpoint` schema (HYPOTHESIS). It is not yet implemented in contracts. This intake must either implement the schema or define a scoped subset. |
| `state/sessions/` directory exists for checkpoint storage | FALSE | Directory does not exist. Must be created by `flow`'s `SessionStore` implementation. |
| ADR-0007 is a constraint on this intake | PARTIAL | ADR-0007 is HYPOTHESIS grade (D-017). It is an input, not a mandate. This intake is the evidence run. The schema and protocol in ADR-0007 are the recommended starting point. Deviations must be documented in S9. |
| `know` module integration (S9 atom promotion) is in scope | FALSE | S9 curator atom promotion depends on K3/K4 (v1, not v1-core). For this intake, S9 capture writes to `docs/PROGRESS.md` (file artifact), not to `know`. The `know` integration is out of scope per the intake's in/out-of-scope list. |
| `bridge`/`soul` modules are unaffected | TRUE | Confirmed by containers.md UC mapping: NF-01 is assigned to `flow`. Human-facing orientation rendering (NF-10) is `bridge`/`soul` territory and explicitly deferred. |
| Appetite is 8h | UNVALIDATED | S1 noted this as unresolved. "Small" maps to 8h per workflow rules but was not explicitly confirmed. Given the schema extension risk (HIGH), 8h may be tight. S3 should flag if options exceed this budget. |
| `docs/PROGRESS.md` must be created as part of this intake | TRUE (inferred) | S9 requires a capture destination. No PROGRESS.md exists. S5 must include it in scope. |

---

## Open Questions for S3

1. **`SessionCheckpoint` vs `SessionSnapshot` extension strategy.** Which option does S3 evaluate: (a) extend existing `SessionSnapshot` with defaulted fields, (b) introduce new `SessionCheckpoint` alongside it, or (c) replace? Option (b) avoids breaking the existing contract surface. This is the most load-bearing design decision in this intake.

2. **Minimum viable slice of ADR-0007 for 8h appetite.** ADR-0007 specifies the full two-layer architecture. What is the minimum subset that satisfies AC-1 (agent reads checkpoint, proposes next action), AC-2 (human receives clear signal), and AC-3 (no hallucination)? S3 must bound this explicitly — the full recovery protocol, cross-project orientation, and `know` integration are all out of scope for v1-core.

3. **Where is the step-boundary checkpoint writer in `flow`?** ADR-0007 says checkpoints are written at step boundaries. `flow` manages pipeline steps. S3 must identify which `flow` function/hook triggers `SessionStore.save()` and whether this requires new pipeline infrastructure or can hook into existing step dispatch.

4. **Human bookmark writer path.** `state/SESSION_STATE.md` needs a runtime writer. Options: (a) `SessionStore.save()` writes both JSON checkpoint and Markdown bookmark atomically, (b) separate bookmark writer in `flow`, (c) human bookmark is deferred to v1. S3 must decide — AC-2 requires it for v1-core.

5. **Hallucination guard (AC-3) implementation.** This is a prompt-design constraint, not a data-model constraint. S3 must specify what "agent reads from artifact" means operationally: is it enforced by prompt structure, by `flow`'s session-start logic, or by both?

---

## C4 L1 Update Needed

`c4_l1_update_needed: false`

No new external actors or system boundaries introduced. NF-01 is fully within the existing
nowu system boundary. All changes are internal to `core` and `flow`. The existing C4 L1/L2
diagrams in `docs/architecture/containers.md` remain accurate.

---

## Arch Pass Divergences

No pre-workflow arch-pass exists for intake-001. Constraints derived cold.

Key findings that would have appeared in an arch-pass:
- `SessionStore` and `SessionSnapshot` exist in contracts (validates S1 assumption #1 as TRUE)
- `state/SESSION_STATE.md` is a template placeholder, not a live artifact (S1 assumption #2 was PARTIAL — the file exists but is unpopulated)
- ADR-0007's `SessionCheckpoint` schema is HYPOTHESIS-grade and not yet in contracts (S1 assumption #3 confirmed — checkpoint schema must be defined or scoped by this intake)
- `know` integration at S9 is out of scope for v1-core (K3/K4 dependency)

---

## S2 Conflict Protocol

No prior arch-pass conflicts to address. No CONFLICT flags against crosscutting.md
(file is a placeholder — not yet populated).

One near-conflict noted for S3 awareness: intake-001's AC-2 ("humans must receive a clear
signal") and D-023 (use cases must not reference implementation artifacts) are in tension
at the boundary. AC-2 is satisfied by `state/SESSION_STATE.md` as the human bookmark —
this is an ADR-0007 implementation detail (acceptable), not a UC-level reference (which
D-023 forbids). No CONFLICT raised; tension is resolved by the ADR-0007/D-023 layering.

---

```yaml
from_step: S2
to_step: S3
agent: nowu-options
intake_id: intake-001
status: READY_FOR_OPTIONS
```
