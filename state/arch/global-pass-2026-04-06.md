---
id: global-pass-2026-04-06
status: APPLIED
applied_at: 2026-04-06T00:00:00Z
agent_version: gap-analyst@1.0
generated_at: 2026-04-06T00:00:00Z
trigger: Clean-sheet GAP run. No prior context.md or containers.md exists. Derived solely from vision.md (v2.0) and USE_CASES.md (v2.2). All 47 UCs (46 ACTIVE + 1 PENDING) assigned to containers.
gap_scope: FULL_RESET
product_stage_at_time: Stage 1 — v1-core framework, Step 02 (Memory Integration Layer) in progress
inputs:
  - docs/vision.md (v2.0, approved 2026-03-31)
  - docs/USE_CASES.md (v2.2, accepted 2026-04-06)
uc_count: 47
uc_active: 46
uc_pending: 1 (XP-02)
---

# Global Architecture Pass — 2026-04-06

## Why This GAP Was Run

This is the first-ever architectural Global Architecture Pass for nowu. No `context.md` or
`containers.md` exists; no prior GAP summary exists against which to diff. The run was
triggered to establish a clean-sheet C4 L1 + L2 architecture derived entirely from the
47-UC catalog (USE_CASES.md v2.2) and the product vision (v2.0), without importing legacy
architectural assumptions from archived ADRs or templates. The scope is FULL_RESET: produce
complete context and container proposals from which `context.md` and `containers.md` can be
authored by the human.

Seven stage targets are in play across the 47 UCs (v1-core through v2 + PENDING). The
architecture must be capable of serving v1-core UCs today and remain coherent through v2 —
but must not over-engineer for v2 concerns that are 18-24 months away.

---

## UC-to-Container Matrix

All 47 UCs are assigned to exactly one container. `core` owns no UCs; it is the shared
contract layer on which all other containers depend.

XP-02 is PENDING (uncertain horizon) but included in the matrix and assigned to `know`
for future planning coherence.

| UC-ID | Title                                                  | Stage    | Container | Notes / Gaps |
|-------|--------------------------------------------------------|----------|-----------|--------------|
| NF-01 | Resume Work After Context Loss                         | v1-core  | flow      | State persistence is a workflow concern; SESSION-STATE.md is a flow artifact |
| NF-02 | Track and Enforce Architectural Decisions              | v1-core  | flow      | DECISIONS.md and ADRs are flow artifacts; enforcement is a reviewer-step responsibility |
| NF-03 | Scope a Piece of Work Without Scope Creep              | v1-core  | flow      | `in_scope_files` in task spec is the shaper step output |
| NF-04 | Self-Assess Quality Without Human Intervention         | v1-core  | flow      | VBR gate requires subprocess test execution — flow manages the gate |
| NF-05 | Route Approvals Without Blocking Progress              | v1-core  | flow      | Tier classification and queue management are core workflow responsibilities |
| NF-06 | Learn From Past Mistakes Across Sessions               | v1-core  | soul      | Pattern detection reads flow's session/capture artifacts; writes lessons back to state/ |
| NF-07 | Bootstrap a New Project Using the Framework            | v1-core  | flow      | Scaffolding, template instantiation, project isolation |
| NF-08 | Measure and Visualize Framework Health                 | v1.1     | soul      | Health metrics computation reads both flow and know state; writes to state/health/ |
| NF-09 | Ensure Every Deliverable Traces Back to a UC           | v1-core  | flow      | Traceability chain validation at S8 reviewer step |
| NF-10 | Maintain the Thread for the Multi-Project Human        | v1-core  | bridge    | Orientation surface rendered to the human; data sourced from flow state and know atoms |
| NF-11 | Detect Vision Drift                                    | v1.1     | soul      | Periodic comparison of work artifacts vs. vision.md; triggered by curator step |
| NF-12 | Explore a Vague Idea Without Structure                 | v1-core  | flow      | Pre-workflow exploration mode; no artifact commitment; produces optional idea capture |
| NF-13 | Generate Multiple Options at Decision Point            | v1-core  | soul      | Core reasoning capability at S3-S4 (options sheet generation) |
| NF-14 | Track Human-AI Work Ratio                              | v1.1     | soul      | Gate-level instrumentation hooks in flow; measurement and trend analysis in soul |
| AP-01 | Track Regulatory Requirements as Living Knowledge      | v1       | know      | Domain data in generic knowledge model; confidence + expiry metadata |
| AP-02 | Manage Product Formulation as Versioned Knowledge      | v1       | know      | Versioned knowledge atoms; version history is a know-module capability |
| AP-03 | Model Supply Chain Relationships and Risks             | v1.2     | know      | Graph relationship modeling; network structure suits know's connection model |
| AP-04 | Capture Market Intelligence Over Time                  | v1.1     | know      | Temporal knowledge with source confidence grading |
| AP-05 | Plan and Track Business Milestones                     | v1.2     | know      | Dependency-aware milestone atoms; milestone dependencies are knowledge graph edges |
| AP-06 | Evaluate a Business Decision With Traceability         | v1       | know      | Decision atom — same generic model as NF-02 but domain-scoped data |
| AP-07 | Onboard a Collaborator Into the Project Context        | v1.2     | know      | Requires sensitivity filtering (PK-06 model) + scoped summary generation |
| RE-01 | Inventory Existing Processes Before Digitalization     | v1       | know      | Process knowledge atoms with step/participant/handoff structure |
| RE-02 | Track Property Data Across Lifecycle Stages            | v1.2     | know      | Entity lifecycle modeling; lifecycle stage is a know-atom attribute |
| RE-03 | Capture Stakeholder Relationships and Constraints      | v1.2     | know      | Graph relationships; stakeholder entity + relationship edge in know module |
| RE-04 | Prioritize Digitalization by Impact and Feasibility    | v1.2     | know      | Multi-criteria scoring on know data; scoring logic may need soul assistance |
| RE-05 | Detect Inconsistencies Across Property Records         | v2       | know      | Consistency checking within know; contradiction detection extends XP-04's model |
| RE-06 | Support Long-Term Investment Decision Tracking         | v1       | know      | Decision atoms with temporal outcome linking; pattern across properties is soul territory |
| RE-07 | Generate Reports for Different Audiences               | v1.2     | know      | Report generation from know data with audience-scoped sensitivity filtering |
| PK-01 | Capture a Thought Before It's Lost                     | v1-core  | bridge    | Input surface; bridge routes raw input to know for persistence |
| PK-02 | Surface Relevant Knowledge Without Being Asked         | v1.1     | know      | Proactive relevance detection; semantic similarity query within know module |
| PK-03 | Maintain a "Today" View Across All Projects            | v1-core  | bridge    | Renders from flow state + know atoms; bridge assembles the unified daily view |
| PK-04 | Let Knowledge Decay and Clean Up Gracefully            | v1.1     | know      | TTL, staleness scoring, archival logic — know module internal |
| PK-05 | Build Understanding Incrementally Over a Topic         | v1.1     | know      | Incremental synthesis; resolves conflicts within a topic in know module |
| PK-06 | Protect Sensitive Personal Knowledge                   | v1.1     | know      | Access control layer in know; sensitivity tags on atoms; foundation for AP-07, RE-07, XP-10 |
| PK-07 | Ingest and Integrate External Documents                | v1.1     | know      | Ingestion pipeline: extract → grade → link → flag contradictions |
| PK-08 | Interact with nowu from Any Interface                  | v1       | bridge    | Non-CLI adapters extend bridge; NO new top-level module. See ADR-E and note below. |
| XP-01 | Discover Connections Across Projects Automatically     | v1-core  | know      | Cross-project semantic search in know's federation layer |
| XP-02 | Maintain Consistent Terminology Across Projects (PEND) | PENDING  | know      | If activated: per-project namespace + disambiguation is consistent with know's model |
| XP-03 | Transfer Lessons Learned Between Projects              | v1.1     | soul      | Cross-project lesson evaluation; reads know federation + flow capture artifacts |
| XP-04 | Handle Conflicting High-Confidence Knowledge           | v1.1     | soul      | Conflict detection triggered by know; surfacing and escalation are soul reasoning tasks |
| XP-05 | Scale the Knowledge Base Without Degrading Performance | v2       | know      | Indexing strategy, cold storage, query optimization — know module internal |
| XP-06 | Allow Multiple Agents to Work Without Conflicts        | v2       | know      | Concurrency control at know's persistence layer; write locking, deferred archival |
| XP-07 | Adapt the Framework to a New Domain Without Rewriting  | v2       | know      | Schema extensibility; custom knowledge types as tags/namespaces, not DB migrations |
| XP-08 | Export Full Project State in Portable Format           | v1.1     | know      | Primary data export from know (atoms, connections); flow artifacts included in snapshot |
| XP-09 | Onboard a New nowu User                                | v2       | flow      | Guided workflow experience; integrates pre-workflow + initial project setup |
| XP-10 | Run a Small Company on nowu                            | v2       | know      | Multi-user access control extends PK-06's sensitivity model in know module |
| XP-11 | Query Knowledge Graph in Role-Appropriate Format       | v1.1     | know      | Role-appropriate rendering layer within know; same atom data, different lenses |

**UC counts by container:**
- `flow`: 9 UCs (NF-01, NF-02, NF-03, NF-04, NF-05, NF-07, NF-09, NF-12, XP-09)
- `soul`: 7 UCs (NF-06, NF-08, NF-11, NF-13, NF-14, XP-03, XP-04)
- `know`: 27 UCs (AP-01–07, RE-01–07, PK-02, PK-04, PK-05, PK-06, PK-07, XP-01, XP-02, XP-05, XP-06, XP-07, XP-08, XP-10, XP-11)
- `bridge`: 4 UCs (PK-01, PK-03, PK-08, NF-10)
- `core`: 0 UCs (shared contract layer; not a UC owner)
- **Total: 47** ✓

**Note on PK-08:** PK-08 is staged at `v1` (after v1-core CLI is stable). It must live in
`bridge` as an additional adapter — not a new top-level module. The bridge must be designed
with an AdapterProtocol (see ADR-B) so that a messaging bot adapter can be added without
modifying `flow`, `soul`, or `know`.

---

## C4 L1 — System Context

*Input for `docs/architecture/context.md`. No prior context.md exists.*

### Primary Actor

**Raphael — the Multi-Project Human.**
Initiates captures, reads daily orientation, approves decisions, resumes any of several
concurrent projects (software, food business, real estate). Not always at a desk — needs
the system to meet him via mobile, voice, or remote interface. Does not want to manage the
system; wants it to surface what matters and hold the thread between sessions.

### System Boundary Statement

nowu is a **local Python CLI tool** running on a single machine, for a single human user.
It is not cloud-hosted, not SaaS, and not multi-tenant through v1.2. It calls external
LLM APIs over the network (outbound only) and — at v1 — pushes/receives to a messaging
platform for remote access. All project data is stored locally. There is no server,
no authentication, no JWT, no Kubernetes.

### External Systems

| External System | Why it exists | UC anchor |
|---|---|---|
| **LLM API** (Claude / GPT) | Provides reasoning, completion, and synthesis for all agent steps in `flow` and analytical tasks in `soul`. The only non-local compute dependency. | NF-01 through NF-14 (all agent-driven workflow UCs); soul UCs |
| **External Documents** | PDFs, Markdown files, URLs — regulatory documents, market reports, product specs — ingested by PK-07 and processed into knowledge atoms. | PK-07 |
| **Remote Interface** (messaging platform, v1) | Enables PK-08's three interaction modes (capture, review, light action) from mobile/remote without a CLI session. Adapter in `bridge`. | PK-08 |

### C4 L1 — System Context Diagram (Mermaid)

```
%%{init: {'theme': 'default'}}%%
C4Context
    title nowu — System Context

    Person(raphael, "Raphael", "Multi-project human. Captures ideas, reads today view, approves decisions, resumes projects across domains.")

    System(nowu, "nowu", "Local Python CLI. Continuity layer between having a goal and making it real. Holds project intent, decisions, and knowledge across sessions.")

    System_Ext(llm, "LLM API", "Claude / GPT. Provides reasoning and completion for all agent steps. Called by flow (workflow agents) and soul (analytical tasks).")
    System_Ext(ext_docs, "External Documents", "PDFs, Markdown, URLs. Regulatory documents, market reports, specs. Ingested by PK-07.")
    System_Ext(remote_iface, "Remote Interface", "Messaging platform (e.g. Telegram). Capture/review/light-action from mobile. v1 stage, after v1-core CLI is stable.")

    Rel(raphael, nowu, "Captures ideas, reads orientation, approves decisions, reviews state")
    Rel(nowu, llm, "Sends agent prompts, receives reasoning and completions")
    Rel(nowu, ext_docs, "Ingests knowledge atoms from external sources (PK-07)")
    Rel(nowu, remote_iface, "Sends digest + action prompts; receives captures and approvals (PK-08)")
    Rel(remote_iface, raphael, "Delivers digest, receives input from any device")
```

---

## C4 L2 — Container Map

*Input for `docs/architecture/containers.md`. No prior containers.md exists.*

### Proposed Containers

---

#### `core` — Shared Contracts and Domain Models

| Field | Value |
|---|---|
| **Purpose** | Shared Python types, domain models, and inter-module contracts. Every module depends on `core`. `core` depends on nothing else. |
| **Technology** | Python module (no database, no I/O) |
| **UC ownership** | None — this is enabling infrastructure, not a behavior owner |
| **Dependencies** | None (foundational) |

`core` defines the interfaces through which `flow`, `soul`, `know`, and `bridge` communicate.
No module may call another module's internals directly — all cross-module communication goes
through types and protocols defined in `core/contracts.py`.

---

#### `flow` — Pipeline Orchestrator

| Field | Value |
|---|---|
| **Purpose** | Implements and orchestrates all named execution pipelines: pre-workflow (P0–P4), implementation cycle (S1–S9), Global Architecture Pass (G0–G2), and periodic health checks. Manages session state, approval routing, project bootstrapping, task scoping, traceability enforcement, and the VBR gate. |
| **Technology** | Python module; persists state as Markdown/YAML files in `state/` |
| **UC ownership** | NF-01, NF-02, NF-03, NF-04, NF-05, NF-07, NF-09, NF-12, XP-09 |
| **Dependencies** | `core` (contracts), `know` (reads decision atoms and project knowledge), `soul` (reads insight artifacts produced by soul), LLM API (for workflow agent steps) |

`flow` is the pipeline orchestrator for all named execution chains. Each chain
(pre-workflow P0–P4, implementation S1–S9, GAP G0–G2, health checks) is a concrete
pipeline implementation inside `flow` — not a configurable plugin. `flow` owns all
workflow artifacts (`state/tasks/`, `state/intake/`, `state/arch/`, `state/sessions/`,
`state/health/`). It calls the LLM directly for pipeline agent steps and does not call
`soul` at runtime — instead it reads insight artifacts that `soul` has produced into
`state/health/` and `state/arch/` (artifact-based coupling — see ADR-F).

**NF-04 implementation note:** VBR gate requires subprocess execution of `pytest`. `flow`
manages the gate; actual test invocation is a subprocess call, not an internal function.

---

#### `soul` — Agent Intelligence

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

**NF-14 note:** Work ratio instrumentation requires `flow` to emit gate-event records
(timestamps, actor type) that `soul` reads for measurement. Format of gate-event records
must be agreed before NF-14 is implemented.

---

#### `know` — Knowledge Store

| Field | Value |
|---|---|
| **Purpose** | Atomic knowledge storage: atoms, confidence grades, temporal metadata, sensitivity tags, relationship graph, cross-project federation, ingestion pipeline, and export. |
| **Technology** | Python module + SQLite database (local, per-project file) |
| **UC ownership** | AP-01, AP-02, AP-03, AP-04, AP-05, AP-06, AP-07, RE-01, RE-02, RE-03, RE-04, RE-05, RE-06, RE-07, PK-02, PK-04, PK-05, PK-06, PK-07, XP-01, XP-02 (PENDING), XP-05, XP-06, XP-07, XP-08, XP-10, XP-11 |
| **Dependencies** | `core` (contracts); no dependency on `flow`, `soul`, or `bridge` — all calls go inward |

`know` is the most loaded container (27 UCs). This is by design: all domain knowledge — for
the AP business, the RE operation, personal knowledge, and cross-project connections — is
data within a generic model, not code in separate modules. Domain projects (AP, RE) are
namespaced data in `know`, not separate containers.

**Persistence model (see ADR-A):** Per-project SQLite database file, with a cross-project
federation query layer for XP-01 and XP-03. The federation layer is `know`'s cross-project
search API — not a separate container.

**Sensitivity model (see ADR-C):** PK-06 implements per-atom sensitivity classification.
This model is the foundation for AP-07 (collaborator briefing), RE-07 (audience reports),
and XP-10 (multi-user access control at v2). Sensitivity must be implemented before any of
these downstream UCs is scoped.

**Export (XP-08):** Know owns the atom/connection export. `flow` workflow artifacts
(state/ directories) are included in a full project snapshot. Coordination between `know`
and `flow` for XP-08 must be defined in the export API contract in `core`.

---

#### `bridge` — Interface Layer

| Field | Value |
|---|---|
| **Purpose** | Primary user-facing surface. CLI commands, today view, fast capture input, orientation rendering. Extensible adapter layer for PK-08's non-CLI interfaces. |
| **Technology** | Python module + Typer CLI; v1 adds a messaging-platform adapter implementing AdapterProtocol (see ADR-B) |
| **UC ownership** | PK-01, PK-03, PK-08, NF-10 |
| **Dependencies** | `core` (contracts), `flow` (reads project state for orientation and today view), `know` (reads atoms for today view; routes captures) |

`bridge` is the human's entry point. At v1-core, it is only a Typer CLI. At v1, PK-08
adds at least one non-CLI adapter (a messaging bot). The adapter must be added within
`bridge` — no new top-level module is created for remote access. Bridge defines an
`AdapterProtocol` that both the CLI and future adapters implement. `flow` and `know` never
import from `bridge`.

**NF-10 note:** Orientation synthesis (what to surface and in what order) may require a
`soul`-level analysis before v1.1. For v1-core, orientation is read-only from structured
state: SESSION-STATE.md, DECISIONS.md, and PROGRESS.md. dedicated orientation
atoms (if needed) are a v1.1 decision.

---

### C4 L2 — Container Diagram (Mermaid)

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

## ADR Candidates

All six are CANDIDATE status — no decision is made here. Human must review and author ADRs
using `templates/adr.md` before the relevant containers are implemented.

---

### ADR-A: Knowledge Atom Storage Engine

| Field | Value |
|---|---|
| **Decision needed** | Which persistence technology and schema strategy for `know`'s atom store |
| **Context** | `know` must persist thousands of atoms with confidence grades, temporal metadata, sensitivity tags, and graph edges — queryable by content, project, confidence, and relationship. This choice constrains XP-05 (scale), XP-06 (concurrency), XP-07 (extensibility), and XP-08 (export). Chosen before v1-core `know` implementation. |
| **Options** | (A) SQLite primary — atoms as rows, connections as edge table, confidence/sensitivity as columns. (B) Markdown files as primary source + SQLite index for search — maximum portability, slower writes. (C) SQLite + JSON blob per atom — flexible schema, harder to query. (D) Embedded graph DB (or NetworkX + JSON persistence) — natural for connections, less standard. |
| **Why it matters** | Locks in query model for all 27 `know` UCs. Wrong choice requires a migration at scale. Must support XP-08 open-format export without data lock-in. |
| **Status** | CANDIDATE |

---

### ADR-B: CLI Framework and Interface Adapter Protocol

| Field | Value |
|---|---|
| **Decision needed** | CLI library choice for `bridge` and the AdapterProtocol design for PK-08 |
| **Context** | PK-08 (v1) requires adding a non-CLI adapter to `bridge` without touching `flow` or `know`. The CLI library choice must support extensibility without forcing a monolithic command surface. |
| **Options** | (A) Typer — type-safe, modern Python, extensible via callback injection. (B) Click — more established, plugin architecture via click groups. (C) Command Bus pattern — bridge defines a command bus; CLI and messaging bot are both command sources. |
| **Why it matters** | The adapter protocol determines whether adding PK-08's messaging adapter is a 2-hour task or a 2-week refactor. This decision should precede any bridge implementation work. |
| **Status** | CANDIDATE |

---

### ADR-C: Sensitivity and Access Control Model

| Field | Value |
|---|---|
| **Decision needed** | Granularity and classification model for PK-06 sensitivity tags in `know` |
| **Context** | PK-06 (v1.1) requires sensitivity control. AP-07 (collaborator briefing) and RE-07 (audience reports) require sensitivity filtering in generated outputs. XP-10 (v2 multi-user) requires the sensitivity model to extend to role-based access. The model chosen at v1.1 must not require a breaking migration at v2. |
| **Options** | (A) Per-atom 4-level tags: public / internal / personal / confidential. (B) Per-project default sensitivity with per-atom override. (C) Per-rendering-context access policy — what's visible depends on the output context, not a fixed tag on the atom. |
| **Why it matters** | PK-06 is the foundation for AP-07, RE-07, XP-10. Getting the model wrong at v1.1 forces a migration just as domain projects deepen at v1.2. |
| **Status** | CANDIDATE |

---

### ADR-D: Cross-Project Knowledge Architecture

| Field | Value |
|---|---|
| **Decision needed** | How project isolation and cross-project discovery are reconciled in `know` |
| **Context** | XP-01 (v1-core) requires cross-project semantic search. The vision's 12-month horizon requires a "shared, queryable knowledge base." But the focus principle requires projects not to contaminate each other's context. XP-10 (v2) adds multi-user concerns. |
| **Options** | (A) Single shared SQLite DB with `project_id` column — simpler queries, harder to export per-project (XP-08 conflict). (B) Per-project SQLite files + federation query layer for cross-project search — stronger isolation, portable per-project exports, adds federation complexity. (C) Per-project Markdown dirs + spanning semantic vector index — maximum portability, non-relational, performance unknown at scale. |
| **Why it matters** | XP-01 is v1-core — this decision is needed before Step 02 is complete. Option A and B have meaningfully different isolation and portability tradeoffs. Wrong choice is painful to migrate given known connection between XP-01 and XP-08. |
| **Status** | CANDIDATE — URGENT (XP-01 is v1-core; intake-001 references it) |

---

### ADR-E: Multi-Interface Strategy for PK-08

| Field | Value |
|---|---|
| **Decision needed** | Which non-CLI interface to implement first as the PK-08 adapter in `bridge` |
| **Context** | PK-08 (v1 — after v1-core CLI stable) must support capture, review, and light-action from mobile/remote. Three interaction modes must be served by the same adapter. The messaging platform choice determines external dependency. |
| **Options** | (A) Async messaging bot (Telegram) — covers all three modes (capture message, read digest, reply to approve); single API, works on any smartphone. (B) HTTP webhook — lightweight, no external platform dependency, requires the human to use a browser or curl. (C) Cloud sync file watcher (Dropbox/iCloud drop dir for capture + daily digest as a synced file) — no new API, lowest technical complexity, but limited for light actions. |
| **Why it matters** | The platform choice is a v1 external dependency. If Option A (Telegram), nowu takes a runtime dependency on the Telegram Bot API. If Option C, no new runtime dependency but light-action (PK-08 mode 3) is nearly impossible to implement cleanly. |
| **Status** | CANDIDATE |

---

### ADR-F: Agent-Workflow Integration Pattern

| Field | Value |
|---|---|
| **Decision needed** | How `soul` and `flow` are coupled at runtime |
| **Context** | `soul` produces insights that `flow` uses (e.g., health metrics before S8 review, drift report, options sheet). The coupling mechanism determines testability, deployment simplicity, and import discipline. |
| **Options** | (A) Artifact-based (no runtime coupling) — `soul` reads `state/` artifacts and writes insight artifacts; `flow` reads them on the next cycle. No function calls between modules. (B) Direct function call — `flow` calls `soul.generate_options()` at S3; tight coupling, simpler code path. (C) Event bus — `flow` emits events; `soul` subscribes; requires an in-process event bus. |
| **Why it matters** | Determines whether `soul` can be triggered independently (e.g., as a scheduled curator job), whether its output is inspectable, and whether the "artifacts are the API" principle is upheld. NF-13 (options generation) is v1-core — this decision must precede the S3 implementer step. |
| **Status** | CANDIDATE — URGENT (NF-13 is v1-core) |

---

## Constraints for P3

These apply to all P3 Architecture Bootstrap runs after this GAP is accepted. They are
binding on all future epics and stories.

1. **Five-module ceiling.** The five containers (`core`, `flow`, `soul`, `know`, `bridge`)
   are the complete set through v2. No new top-level Python module may be created without a
   superseding ADR. Proposals that require a sixth module must stop at P3 and create an ADR.

2. **Domain projects are data, not code.** AP and RE project UCs are knowledge atoms in
   `know`, not separate modules. No `ap/` or `re/` Python package may be created. All
   domain logic is configuration or data in the generic knowledge model.

3. **PK-08 adapters live in `bridge`.** Any non-CLI interface adapter is an implementation
   of `bridge`'s AdapterProtocol. No new top-level module for remote access.

4. **All cross-module calls go through `core/contracts.py`.** Direct imports between
   `flow`, `soul`, `know`, and `bridge` are forbidden. The only legal import graph is:
   all modules → `core`; `soul` reads/writes file artifacts owned by `flow` (no function
   call); `bridge` calls `flow` and `know` through their contracted APIs.

5. **All persistence is local.** No cloud database, no SaaS backend, no hosted API (other
   than LLM calls) through v1.2. This is a single-user local Python CLI. Proposals that
   introduce remote state storage require a Tier 3 approval.

6. **Sensitivity before briefing.** PK-06 (sensitivity classification in `know`) must be
   implemented before any story that touches AP-07 (collaborator briefing), RE-07 (audience
   reports), or XP-10 (multi-user). No workaround accepted.

7. **Cross-project federation before v1.1 knowledge UCs.** ADR-D's cross-project architecture
   must be implemented and tested before any of PK-02, PK-05, XP-03 is scoped. These UCs
   depend on a working federation layer.

8. **ADR-F resolved before NF-13 is shaped.** The agent-workflow integration pattern
   (how `soul` and `flow` couple) must be decided before the S3 options-generation step
   is implemented. NF-13 is v1-core and is in the immediate implementation horizon.

---

## What Stays the Same

Explicitly: these are NOT changed by this GAP.

1. **The vision (v2.0, approved 2026-03-31)** is the north star. This GAP derives
   architecture from it; it does not alter it.

2. **The UC catalog (USE_CASES.md v2.2)** is the inputs document. This GAP proposes
   containers to host UCs, not changes to the UCs themselves.

3. **The five-module structure** (`core`, `flow`, `bridge`, `soul`, `know`) is confirmed
   as the right ceiling — not a new invention. This GAP endorses it as the canonical L2.

4. **The artifact-based agent communication principle** ("artifacts are the API") is
   unchanged and drives ADR-F's recommendation.

5. **Python 3.11+** is the implementation language.

6. **The single-user, local-first model** holds through v1.2. Multi-user (XP-10) is a v2
   concern and does not affect v1-core or v1.1 architecture.

7. **The named pipeline structure** (pre-workflow P0–P4, implementation S1–S9, GAP G0–G2, health checks) is unchanged. This GAP assigns orchestration UCs to `flow` but does not alter the pipeline steps themselves.

---

## Open Questions for Human

These cannot be resolved without human judgment. containers.md should not be finalized
until questions 1 and 4 are answered (they affect v1-core).

1. **Database isolation model (ADR-D — URGENT).** Per-project SQLite file or single shared
   DB with namespaces? XP-01 is v1-core and intake-001 is in progress. This choice must be
   made before the `know` module's storage layer is implemented.

2. **Messaging platform for PK-08 (ADR-E).** Which platform (Telegram, Signal, or other)?
   This determines the external dependency chain and needs to be decided before v1 starts.
   Does not block v1-core.

3. **Agent-workflow coupling for NF-13 (ADR-F — URGENT).** Artifact-based (option A is
   recommended) vs. direct function call (option B)? NF-13 is v1-core; the S3 step cannot
   be implemented without knowing whether `flow` calls `soul` directly or reads an
   artifact. Needs decision before the next implementation sprint.

4. **LLM call ownership.** Should all LLM API calls go through `soul` (making `soul` the
   single LLM client), or does `flow` call the LLM directly for workflow agent steps? The
   proposed diagram shows both calling LLM. A single-client model (all LLM calls via
   `soul`) is cleaner but requires `flow` to depend on `soul` at runtime — which conflicts
   with the artifact-based coupling preference. Human must decide.

5. **`core` database access pattern.** Does `core` expose a shared DB connection/session
   factory, or does each module own its own DB file(s) entirely? The shared session model
   is simpler but couples module initialization. Per-module DB files are what ADR-D
   option B implies. Decide before first integration test is written.

6. **XP-02 (terminology management) staging.** Currently PENDING with uncertain horizon.
   Should this be promoted to ACTIVE with a v1.2 or v2 stage target? Terminology
   collisions are structurally guaranteed once cross-project search (XP-01) is live.
   Recommend: revisit after XP-01 is implemented and real collisions are observed.

---

## Resolved Questions

All six open questions have been resolved via Mode D architecture-only spikes (intake-003 and intake-004) and human approval of binding decisions D-011 and D-012.

**Q1 — Database isolation model (ADR-D):** ✅ **DECIDED**  
**Decision: [D-011](../../docs/DECISIONS.md#d-011—per-project-sqlite-isolation-model-for-know-and-db-session-pattern-adr-d)**  
Per-project SQLite files with `know`-internal federation query layer (ADR-D Option B).
- XP-04 cross-project search fans out across all project files.
- XP-08 export is a file copy — semantically complete by design.
- Federation performance bounded at ≤ 20 projects; materialized-index fallback above threshold.
- Q5 (core DB access pattern) resolved as corollary: each module owns its DB files entirely; `core` is I/O-free.

**Q2 — Messaging platform for PK-08 (ADR-E):** ✅ **DECIDED**  
**Platform: Telegram** (python-telegram-bot library, covers all 3 PK-08 modes, minimal integration overhead).  
Feeds directly into ADR-E stub; no spike required. ADR-E will be authored by gap-writer.

**Q3 — Agent-workflow coupling for NF-13 (ADR-F):** ✅ **DECIDED**  
**Decision: [D-012](../../docs/DECISIONS.md#d-012—artifact-based-socialsoul-flow-coupling-with-s9-triggered-soul-subprocess-adr-f)**  
Artifact-based coupling (ADR-F Option A) + S9 subprocess invocation (Trigger A1).
- `soul` and `flow` couple exclusively at the file-system level via `state/` artifacts.
- At S9 close, flow invokes `nowu soul run` as OS-level subprocess via bridge CLI.
- Soul failure is non-fatal (logs, writes sentinel, exits); S3 validates artifact presence on next cycle.
- NF-13 synchrony guaranteed without human discipline (PRIMARY SENSITIVITY for this decision).

**Q4 — LLM call ownership:** ✅ **RESOLVED (automatic corollary of Q3)**  
**Pattern: Dual independent clients + shared `LLMClientConfig` in core.**  
If artifact-based coupling is enforced (Q3 resolved), flow cannot route LLM calls through soul at runtime. Both `flow` and `soul` call LLM API directly with independent client instances. `core/contracts.py` defines shared `LLMClientConfig` type; no credential duplication, no hidden dependency.

**Q5 — `core` database access pattern:** ✅ **RESOLVED (automatic corollary of Q1)**  
**Pattern: Per-module DB files entirely.**  
Each module owns its DB file(s) with no shared session factory in core. `core` is I/O-free; it defines `KnowledgeStoreProvider` as a Protocol only. `know` provides the sole concrete implementation and owns all SQLite connections.

**Q6 — XP-02 (terminology management) staging:** ⏸ **DEFERRED**  
**Status**: PENDING → revisit after XP-01 is implemented and real collisions are observed.  
XP-02 terminology collisions are structurally guaranteed once cross-project search (XP-01) is live, but adoption urgency depends on empirical data.

---

## ADR Status Update

- **ADR-D** (Database isolation): CANDIDATE → **DECIDED** via D-011 (intake-003)
- **ADR-F** (Agent-workflow coupling): CANDIDATE → **DECIDED** via D-012 (intake-004)
- **ADR-A** (Module boundaries): CANDIDATE → ready for shaping (no blocking questions)
- **ADR-B** (Adapter protocol for PK-08): CANDIDATE → ready for shaping (messaging platform decided: Q2 → Telegram)
- **ADR-C** (Shared LLM client): CANDIDATE → ready for shaping (ownership model decided: Q4 → dual clients)
- **ADR-E** (Messaging bot adapter): CANDIDATE → ready for authoring (platform decided: Q2 → Telegram)

---

## Recommended Next Steps

1. **Human approves these resolutions** — verify "Resolved Questions" section matches your intent before gap-writer runs.

2. **Gap-writer updates** `docs/architecture/context.md`, `docs/architecture/containers.md`, and creates
   ADR stubs in `docs/architecture/adr/` based on this global-pass (gap-writer runs only when status: APPROVED).
   Sequence: ADR-D and ADR-F stubs first (already DECIDED via D-011, D-012), then ADR-A, ADR-B, ADR-C, ADR-E stubs (CANDIDATE).

3. **Human authors and approves ADRs** for each candidate using these stubs and `templates/adr.md`.
   Order: ADR-D (intake-003-decision.md ACCEPTED), ADR-F (intake-004-decision.md ACCEPTED), then
   ADR-A/-B/-C/-E in v1-core and v1 staging sequence.

4. **Human sets** `state/arch/gap-trigger.md` status to CLOSED once gap-writer completes and
   context.md + containers.md are accepted.

5. **Run** `/health-check architecture` to verify containers.md is internally consistent and trace
   connections to USE_CASES.md.

6. **Update** `docs/V1_PLAN.md` and `docs/PROGRESS.md` to reflect the resolved architecture and
   the next implementation phase (Stage 1 Step 02 continuation).
