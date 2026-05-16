---
version: 1.0
generated_from: global-pass-2026-04-06
status: DRAFT
last_gap: 2026-04-06
---

# nowu — C4 L2 Container Map

## Table of Contents

1. [`core`](#core--shared-contracts-and-domain-models) — Shared contracts and domain models (0 UCs)
2. [`flow`](#flow--pipeline-orchestrator) — Pipeline orchestrator (9 UCs)
3. [`soul`](#soul--agent-intelligence) — Agent intelligence (7 UCs)
4. [`know`](#know--knowledge-store) — Knowledge store (27 UCs)
5. [`bridge`](#bridge--interface-layer) — Interface layer (4 UCs)

Supporting sections:
- [UC-to-Container Matrix](#uc-to-container-matrix)
- [Cross-Cutting Concerns](#cross-cutting-concerns)
- [Dependencies Diagram](#dependencies-diagram)

---

## `core` — Shared Contracts and Domain Models

| Field | Value |
|---|---|
| **Purpose** | Shared Python types, domain models, and inter-module contracts. Every module depends on `core`. `core` depends on nothing else. |
| **Technology** | Python module (no database, no I/O) |
| **UC ownership** | None — this is enabling infrastructure, not a behavior owner |
| **Dependencies** | None (foundational) |

`core` defines the interfaces through which `flow`, `soul`, `know`, and `bridge` communicate.
No module may call another module's internals directly — all cross-module communication goes
through types and protocols defined in `core/contracts.py`.

Key types in `core/contracts.py`:
- `KnowledgeStoreProvider` — Protocol defining the `know` module's public API. No database
  imports or I/O in `core`; `know` provides the sole concrete implementation.
- `LLMClientConfig` — Shared configuration type for LLM API clients. Both `flow` and `soul`
  instantiate independent LLM clients from this shared config type; no credential duplication.

`core` is the only Python module that all other modules are permitted to import. Direct imports
between `flow`, `soul`, `know`, and `bridge` are forbidden (see ADR-0001).

---

## `flow` — Pipeline Orchestrator

| Field | Value |
|---|---|
| **Purpose** | Implements and orchestrates all named execution pipelines: pre-workflow (P0–P4), implementation cycle (S1–S9), Global Architecture Pass (G0–G2), and periodic health checks. Manages session state, approval routing, project bootstrapping, task scoping, traceability enforcement, and the VBR gate. |
| **Technology** | Python module; persists state as Markdown/YAML files in `state/` |
| **UC ownership** | NF-01, NF-02, NF-03, NF-04, NF-05, NF-07, NF-09, NF-12, XP-09 |
| **Dependencies** | `core` (contracts), `know` (reads decision atoms and project knowledge), `soul` (reads insight artifacts — file-level only, no runtime call), LLM API (for workflow agent steps) |

`flow` is the pipeline orchestrator for all named execution chains. Each chain
(pre-workflow P0–P4, implementation S1–S9, GAP G0–G2, health checks) is a concrete
pipeline implementation inside `flow` — not a configurable plugin. `flow` owns all
workflow artifacts (`state/tasks/`, `state/intake/`, `state/arch/`, `state/sessions/`,
`state/health/`). It calls the LLM directly for pipeline agent steps and does not call
`soul` at runtime — instead it reads insight artifacts that `soul` has produced into
`state/health/` and `state/arch/` (artifact-based coupling — see ADR-0006).

At the close of every S9 (curator) step, `flow`'s S9 orchestration invokes `nowu soul run`
as an OS-level subprocess via `bridge`'s CLI entry point. Soul runs to completion, writes
its artifacts, and exits. S9 treats soul failure as non-fatal: on failure, S9 logs the error,
writes `state/soul-error.yaml`, and completes normally. S3 on the next cycle checks for soul
artifact presence and raises an explicit error if an artifact is absent or the sentinel is present.

**NF-04 implementation note:** VBR gate requires subprocess execution of `pytest`. `flow`
manages the gate; actual test invocation is a subprocess call, not an internal function.

**NF-14 note:** Work ratio instrumentation requires `flow` to emit gate-event records
(timestamps, actor type) that `soul` reads for measurement. Format of gate-event records
must be agreed before NF-14 is implemented.

---

## `soul` — Agent Intelligence

| Field | Value |
|---|---|
| **Purpose** | AI-powered analytical reasoning: pattern detection, health metrics, drift detection, options generation, lesson transfer, work ratio measurement, and conflict surfacing. |
| **Technology** | Python module; calls LLM API; reads `state/` artifacts from `flow`; writes insight artifacts to `state/health/` and `state/arch/`; reads atoms from `know` |
| **UC ownership** | NF-06, NF-08, NF-11, NF-13, NF-14, XP-03, XP-04 |
| **Dependencies** | `core` (contracts), `know` (reads knowledge atoms for analysis; writes lessons as atoms), LLM API (reasoning calls) |

`soul` is artifact-coupled to `flow`: it reads `state/` directories and produces new
artifacts that `flow` picks up on the next cycle. There is no runtime function call from
`flow` to `soul`. This preserves the "artifacts are the API" principle and keeps soul
independently triggerable (e.g., as a scheduled curator run at S9).

`soul` calls the LLM API directly using an independent client instantiated from
`LLMClientConfig` in `core`. It does not route calls through `flow`. This is the Q4
resolution (D-012 corollary): dual independent LLM clients, shared config type only.

**NF-13 note:** Options sheet generation at S3 depends on a soul artifact being present
from the previous S9 run. S3 validates artifact presence (and checks the staleness sentinel)
before proceeding. This one-cycle staleness is a known, bounded tradeoff of artifact-based
coupling (ADR-0006).

---

## `know` — Knowledge Store

| Field | Value |
|---|---|
| **Purpose** | Atomic knowledge storage: atoms, confidence grades, temporal metadata, sensitivity tags, relationship graph, cross-project federation, ingestion pipeline, and export. |
| **Technology** | Python module + SQLite database (local, per-project file) |
| **UC ownership** | AP-01, AP-02, AP-03, AP-04, AP-05, AP-06, AP-07, RE-01, RE-02, RE-03, RE-04, RE-05, RE-06, RE-07, PK-02, PK-04, PK-05, PK-06, PK-07, XP-01, XP-02 (PENDING), XP-05, XP-06, XP-07, XP-08, XP-10, XP-11 |
| **Dependencies** | `core` (contracts); no dependency on `flow`, `soul`, or `bridge` — all calls go inward |

`know` is the most loaded container (27 UCs). This is by design: all domain knowledge — for
the AP business, the RE operation, personal knowledge, and cross-project connections — is
data within a generic model, not code in separate modules. Domain projects (AP, RE) are
namespaced data in `know`, not separate containers. No `ap/` or `re/` Python package may
ever be created.

**Persistence model (D-011 / ADR-0004):** Per-project SQLite database file. One file per
project in a user-controlled directory. A federation query layer inside `know` — not a new
module — fans out XP-01 cross-project queries across all project files and merges results.
The fan-out is acceptable at ≤ 20 concurrent active projects for v1-core; if that threshold
is exceeded before v1.1, a `know`-internal materialized-index fallback (`federation-index.db`,
refreshed on every write) is activated.

**Sensitivity model (ADR-0003 / PK-06):** Per-atom sensitivity classification. PK-06 is
the foundation for AP-07 (collaborator briefing), RE-07 (audience reports), and XP-10
(v2 multi-user access control). PK-06 must be implemented before any story touching these
downstream UCs is scoped.

**Export (XP-08):** `know` owns the atom/connection export. Because isolation is per-file,
a full project export for XP-08 is a file copy — semantically complete by design, with no
edge-ownership rules or stub references. `flow` workflow artifacts (`state/` directories)
are included in a full project snapshot; coordination between `know` and `flow` for XP-08
must be defined in the export API contract in `core`.

---

## `bridge` — Interface Layer

| Field | Value |
|---|---|
| **Purpose** | Primary user-facing surface. CLI commands, today view, fast capture input, orientation rendering. Extensible adapter layer for PK-08's non-CLI interfaces. |
| **Technology** | Python module + Typer CLI; v1 adds a messaging-platform adapter (Telegram / python-telegram-bot) implementing `AdapterProtocol` |
| **UC ownership** | PK-01, PK-03, PK-08, NF-10 |
| **Dependencies** | `core` (contracts), `flow` (reads project state for orientation and today view), `know` (reads atoms for today view; routes captures) |

`bridge` is the human's entry point. At v1-core, it is only a Typer CLI. At v1, PK-08
adds at least one non-CLI adapter (Telegram, via python-telegram-bot). The adapter must be
added within `bridge` — no new top-level module is created for remote access. `bridge`
defines an `AdapterProtocol` that both the CLI and future adapters implement (see ADR-0002).
`flow` and `know` never import from `bridge`.

**NF-10 note:** Orientation synthesis (what to surface and in what order) may require a
`soul`-level analysis before v1.1. For v1-core, orientation is read-only from structured
state: SESSION-STATE.md, DECISIONS.md, and ROADMAP.md. Dedicated orientation atoms (if
needed) are a v1.1 decision.

---

## UC-to-Container Matrix

All 47 UCs are assigned to exactly one container. `core` owns no UCs; it is the shared
contract layer on which all other containers depend.

XP-02 is PENDING (uncertain horizon) but included in the matrix and assigned to `know`
for future planning coherence.

| UC-ID | Title | Stage | Container | Notes / Gaps |
|-------|--------------------------------------------------------|----------|-----------|--------------|
| NF-01 | Resume Work After Context Loss | v1-core | flow | State persistence is a workflow concern; SESSION-STATE.md is a flow artifact |
| NF-02 | Track and Enforce Architectural Decisions | v1-core | flow | DECISIONS.md and ADRs are flow artifacts; enforcement is a reviewer-step responsibility |
| NF-03 | Scope a Piece of Work Without Scope Creep | v1-core | flow | `in_scope_files` in task spec is the shaper step output |
| NF-04 | Self-Assess Quality Without Human Intervention | v1-core | flow | VBR gate requires subprocess test execution — flow manages the gate |
| NF-05 | Route Approvals Without Blocking Progress | v1-core | flow | Tier classification and queue management are core workflow responsibilities |
| NF-06 | Learn From Past Mistakes Across Sessions | v1-core | soul | Pattern detection reads flow's session/capture artifacts; writes lessons back to state/ |
| NF-07 | Bootstrap a New Project Using the Framework | v1-core | flow | Scaffolding, template instantiation, project isolation |
| NF-08 | Measure and Visualize Framework Health | v1.1 | soul | Health metrics computation reads both flow and know state; writes to state/health/ |
| NF-09 | Ensure Every Deliverable Traces Back to a UC | v1-core | flow | Traceability chain validation at S8 reviewer step |
| NF-10 | Maintain the Thread for the Multi-Project Human | v1-core | bridge | Orientation surface rendered to the human; data sourced from flow state and know atoms |
| NF-11 | Detect Vision Drift | v1.1 | soul | Periodic comparison of work artifacts vs. vision.md; triggered by curator step |
| NF-12 | Explore a Vague Idea Without Structure | v1-core | flow | Pre-workflow exploration mode; no artifact commitment; produces optional idea capture |
| NF-13 | Generate Multiple Options at Decision Point | v1-core | soul | Core reasoning capability at S3-S4 (options sheet generation) |
| NF-14 | Track Human-AI Work Ratio | v1.1 | soul | Gate-level instrumentation hooks in flow; measurement and trend analysis in soul |
| AP-01 | Track Regulatory Requirements as Living Knowledge | v1 | know | Domain data in generic knowledge model; confidence + expiry metadata |
| AP-02 | Manage Product Formulation as Versioned Knowledge | v1 | know | Versioned knowledge atoms; version history is a know-module capability |
| AP-03 | Model Supply Chain Relationships and Risks | v1.2 | know | Graph relationship modeling; network structure suits know's connection model |
| AP-04 | Capture Market Intelligence Over Time | v1.1 | know | Temporal knowledge with source confidence grading |
| AP-05 | Plan and Track Business Milestones | v1.2 | know | Dependency-aware milestone atoms; milestone dependencies are knowledge graph edges |
| AP-06 | Evaluate a Business Decision With Traceability | v1 | know | Decision atom — same generic model as NF-02 but domain-scoped data |
| AP-07 | Onboard a Collaborator Into the Project Context | v1.2 | know | Requires sensitivity filtering (PK-06 model) + scoped summary generation |
| RE-01 | Inventory Existing Processes Before Digitalization | v1 | know | Process knowledge atoms with step/participant/handoff structure |
| RE-02 | Track Property Data Across Lifecycle Stages | v1.2 | know | Entity lifecycle modeling; lifecycle stage is a know-atom attribute |
| RE-03 | Capture Stakeholder Relationships and Constraints | v1.2 | know | Graph relationships; stakeholder entity + relationship edge in know module |
| RE-04 | Prioritize Digitalization by Impact and Feasibility | v1.2 | know | Multi-criteria scoring on know data; scoring logic may need soul assistance |
| RE-05 | Detect Inconsistencies Across Property Records | v2 | know | Consistency checking within know; contradiction detection extends XP-04's model |
| RE-06 | Support Long-Term Investment Decision Tracking | v1 | know | Decision atoms with temporal outcome linking; pattern across properties is soul territory |
| RE-07 | Generate Reports for Different Audiences | v1.2 | know | Report generation from know data with audience-scoped sensitivity filtering |
| PK-01 | Capture a Thought Before It's Lost | v1-core | bridge | Input surface; bridge routes raw input to know for persistence |
| PK-02 | Surface Relevant Knowledge Without Being Asked | v1.1 | know | Proactive relevance detection; semantic similarity query within know module |
| PK-03 | Maintain a "Today" View Across All Projects | v1-core | bridge | Renders from flow state + know atoms; bridge assembles the unified daily view |
| PK-04 | Let Knowledge Decay and Clean Up Gracefully | v1.1 | know | TTL, staleness scoring, archival logic — know module internal |
| PK-05 | Build Understanding Incrementally Over a Topic | v1.1 | know | Incremental synthesis; resolves conflicts within a topic in know module |
| PK-06 | Protect Sensitive Personal Knowledge | v1.1 | know | Access control layer in know; sensitivity tags on atoms; foundation for AP-07, RE-07, XP-10 |
| PK-07 | Ingest and Integrate External Documents | v1.1 | know | Ingestion pipeline: extract → grade → link → flag contradictions |
| PK-08 | Interact with nowu from Any Interface | v1 | bridge | Non-CLI adapters extend bridge; NO new top-level module. See ADR-0002 and ADR-0005. |
| XP-01 | Discover Connections Across Projects Automatically | v1-core | know | Cross-project semantic search in know's federation layer |
| XP-02 | Maintain Consistent Terminology Across Projects (PEND) | PENDING | know | If activated: per-project namespace + disambiguation is consistent with know's model |
| XP-03 | Transfer Lessons Learned Between Projects | v1.1 | soul | Cross-project lesson evaluation; reads know federation + flow capture artifacts |
| XP-04 | Handle Conflicting High-Confidence Knowledge | v1.1 | soul | Conflict detection triggered by know; surfacing and escalation are soul reasoning tasks |
| XP-05 | Scale the Knowledge Base Without Degrading Performance | v2 | know | Indexing strategy, cold storage, query optimization — know module internal |
| XP-06 | Allow Multiple Agents to Work Without Conflicts | v2 | know | Concurrency control at know's persistence layer; write locking, deferred archival |
| XP-07 | Adapt the Framework to a New Domain Without Rewriting | v2 | know | Schema extensibility; custom knowledge types as tags/namespaces, not DB migrations |
| XP-08 | Export Full Project State in Portable Format | v1.1 | know | Primary data export from know (atoms, connections); flow artifacts included in snapshot |
| XP-09 | Onboard a New nowu User | v2 | flow | Guided workflow experience; integrates pre-workflow + initial project setup |
| XP-10 | Run a Small Company on nowu | v2 | know | Multi-user access control extends PK-06's sensitivity model in know module |
| XP-11 | Query Knowledge Graph in Role-Appropriate Format | v1.1 | know | Role-appropriate rendering layer within know; same atom data, different lenses |

**UC counts by container:**

| Container | Count | UC IDs |
|---|---|---|
| `flow` | 9 | NF-01, NF-02, NF-03, NF-04, NF-05, NF-07, NF-09, NF-12, XP-09 |
| `soul` | 7 | NF-06, NF-08, NF-11, NF-13, NF-14, XP-03, XP-04 |
| `know` | 27 | AP-01–AP-07, RE-01–RE-07, PK-02, PK-04, PK-05, PK-06, PK-07, XP-01, XP-02, XP-05, XP-06, XP-07, XP-08, XP-10, XP-11 |
| `bridge` | 4 | PK-01, PK-03, PK-08, NF-10 |
| `core` | 0 | (shared contract layer — not a UC owner) |
| **Total** | **47** | |

---

## Cross-Cutting Concerns

### `core/contracts.py` as the Only Cross-Module Border

All cross-module communication passes through `core/contracts.py`. This is not a
guideline — it is an enforced module boundary (ADR-0001, D-002, D-003). The legal import
graph is:

```
flow   → core
soul   → core
know   → core
bridge → core, flow, know
```

Direct imports between `flow`, `soul`, `know`, and `bridge` are forbidden. The only
exception: `soul` reads/writes file artifacts in paths that `flow` owns (`state/`) — this
is a filesystem-level coupling, not a Python import. `bridge` may call `flow` and `know`
through their contracted APIs only.

### Artifact-Based soul↔flow Coupling (D-012)

`soul` and `flow` are decoupled at the Python level. Communication happens exclusively at
the filesystem level via `state/` artifacts:

- `flow` produces workflow artifacts (session logs, capture records, decision files).
- `soul` reads these artifacts, runs analysis, and writes insight artifacts (options sheets,
  health metrics, drift reports) back to `state/health/` and `state/arch/`.
- `flow` reads soul's insight artifacts on the next cycle.
- At S9 close, `flow` invokes `nowu soul run` as an OS-level subprocess; soul failure is
  non-fatal (error logged, sentinel written, S9 continues).

This preserves soul's independent triggering capability and ensures all inter-module
data is inspectable on the filesystem.

### Per-Project SQLite Isolation (D-011)

`know` maintains one SQLite file per active project. There is no shared database between
projects. Cross-project queries (XP-01) are handled by a federation query layer inside
`know` that fans out across all project files. `core` is I/O-free — it defines
`KnowledgeStoreProvider` as a Protocol with no database imports. `know` provides the sole
concrete implementation and owns all SQLite connection lifecycle.

### LLM Client Ownership (D-012 corollary)

Both `flow` and `soul` call the LLM API directly with independent client instances. This is
not a defect — it is the necessary consequence of artifact-based coupling (ADR-0006). If
`flow` routed LLM calls through `soul` at runtime, it would create an implicit runtime
dependency that violates D-002 and the artifact-based coupling constraint. `core/contracts.py`
defines `LLMClientConfig` as the shared configuration type; credentials are provided once
and referenced by both clients without duplication.

---

## Dependencies Diagram

```
%%{init: {'theme': 'default'}}%%
C4Container
    title nowu — Container Diagram (C4 L2)

    Person(raphael, "Raphael", "Multi-project human")
    System_Ext(llm, "LLM API", "Claude / GPT")
    System_Ext(remote_iface, "Remote Interface", "Messaging platform — v1 (PK-08)")
    System_Ext(ext_docs, "External Documents", "PDFs, URLs — ingested by PK-07")

    System_Boundary(nowu, "nowu — local Python process") {

        Container(bridge, "bridge", "Python module + Typer CLI",
            "CLI + future adapters. Today view, fast capture, orientation, approvals. AdapterProtocol for PK-08 non-CLI adapters.")

        Container(flow, "flow", "Python module + state/ YAML/Markdown",
            "Pipeline orchestrator. Implements pre-workflow (P0-P4), implementation cycle (S1-S9), GAP (G0-G2), and health checks. Session state, approval routing, traceability. Calls LLM for pipeline agent steps.")

        Container(soul, "soul", "Python module + LLM calls",
            "Agent intelligence. Pattern detection, health metrics, drift detection, options generation, lesson transfer, conflict surfacing. Artifact-coupled to flow.")

        Container(know, "know", "Python module + SQLite (per project)",
            "Knowledge store. Atoms, confidence grades, sensitivity, connections, cross-project federation. Ingestion pipeline. Export. All domain data (AP, RE, PK, XP).")

        Container(core, "core", "Python module — no I/O",
            "Shared contracts, domain models, inter-module protocols. No UC ownership. Foundation layer.")
    }

    Rel(raphael, bridge, "Uses CLI / messaging adapter", "terminal / messaging platform")
    Rel(bridge, remote_iface, "Sends digest; receives captures and approvals (PK-08, v1)")
    Rel(remote_iface, raphael, "Delivers digest + prompts to any device")

    Rel(bridge, flow, "Reads project state for orientation + today view")
    Rel(bridge, know, "Reads atoms for today view; routes captures to know")

    Rel(flow, llm, "Sends agent prompts; receives completions (workflow steps)")
    Rel(flow, know, "Reads decision atoms; writes traceability records")

    Rel(soul, llm, "Sends analysis prompts; receives insights")
    Rel(soul, know, "Reads atoms for analysis; writes lessons as atoms")
    Rel(soul, flow, "Reads state/ artifacts (session logs, capture records) — file-level only")

    Rel(know, ext_docs, "Ingests knowledge from external documents (PK-07)")

    Rel(bridge, core, "Uses contracts")
    Rel(flow, core, "Uses contracts")
    Rel(soul, core, "Uses contracts")
    Rel(know, core, "Uses contracts")
```

---

## Pending Updates

> This section records C4 L2 deltas identified at S9 capture. Do not rewrite above sections
> directly — apply during next architecture review (gap-check or P3 pass).

### intake-001 (2026-05-13) — Session persistence surfaces now live

`flow` module now owns two concrete session persistence surfaces not previously documented:

- **`flow/session_store.py` (`FileSessionStore`)** — writes an atomic JSON checkpoint and a
  YAML bookmark. The YAML bookmark path is `state/SESSION_STATE.md` (the canonical
  human-readable artifact for session state on resume).
- **`core/contracts/session.py` (`SessionStore` protocol)** — the binding protocol for
  session persistence, now updated to `save(checkpoint: SessionCheckpoint)` and
  `load() -> SessionCheckpoint | None`. `@runtime_checkable` decorator added.
- **`core/contracts/types.py` (`SessionCheckpoint`)** — 10-field versioned dataclass
  (schema_version, last_step, next_action, active_task, completed_steps, active_intake,
  active_epic, project_root, git_branch, notes). Replaces 5-field `SessionSnapshot`.

These are C4 L3 surfaces within the existing `core` and `flow` containers. No new containers
or cross-module imports were introduced. Module boundary rules (D-002, D-003) were respected
throughout. Decision: D-024.
