---
id: global-pass-2026-04-06
status: PROPOSED
agent_version: gap-analyst@1.0
generated_at: 2026-04-06T00:00:00Z
trigger: "UC catalog grew from 36 to 47 active UCs. Vision v2.0 added 'atomic knowledge layer' (XP-11) and 'ubiquitous access' (PK-08). ARCHITECTURE.md v1.3 references stale UC count. containers.md has no owner for PK-08, XP-11, NF-10, NF-12, NF-13."
gap_scope: DOMAIN_EXPANSION + DRIFT_CORRECTION
prior_gap: global-pass-2026-03-29 (APPLIED)
product_stage_at_time: Stage 1 — v1 core (Step 02 of 7 in progress)
---

# Global Architecture Pass — 2026-04-06 (DELTA)

## Why This GAP Was Run

The prior GAP (2026-03-29) established the full C4 L1 / L2 baseline via FULL_RESET. Since
then, the UC catalog has grown from 36 to 47 active UCs across two passes (USE_CASES.md
v2.0 and v2.1, both anchored to vision v2.0 approved 2026-03-31). Vision v2.0 introduced
two architectural concepts that have no container owner in the existing baseline:

1. **Atomic knowledge layer** (XP-11): "same data, different lenses" — role-appropriate
   rendering of the knowledge graph for human vs. AI agent.
2. **Ubiquitous access** (PK-08): "nowu must meet him wherever he is" — the primary
   persona explicitly operates from mobile, remote, and non-IDE contexts.

Additionally, eleven UCs added since the baseline carry no explicit container assignment
in `containers.md`. This pass assigns all eleven, resolves gap_scope DOMAIN_EXPANSION for
PK-08 and XP-11, and corrects the documentation drift (DRIFT_CORRECTION).

**Scope:** This is a DELTA pass. The 36 UC assignments from `global-pass-2026-03-29`
are confirmed unchanged and are not re-litigated here. Only the 11 new UCs are analysed,
plus the cross-cutting impact on context.md, containers.md, and the ADR set.

---

## UC-to-Container Matrix — New UCs Only (delta from 2026-03-29 baseline)

All 11 UCs added since the 2026-03-29 GAP. The 36 prior UC assignments remain valid —
see `global-pass-2026-03-29.md` UC-to-Container Matrix for those entries.

| UC-ID | Title | Stage | Natural Container | Gap / Risk |
|---|---|---|---|---|
| NF-10 | Maintain the Thread for the Multi-Project Human | v1-core | `flow` (orientation assembly, extending session open/resume) + `bridge` (human-facing "catch me up" entry point) | No new container needed. `flow` opens sessions; orientation is a specialised session mode. `bridge` surfaces the result. Responsibility wording in both containers must be updated explicitly. |
| NF-11 | Detect Vision Drift | v1.1 | `flow` (S9 curator drift-detection pass) + `core` (drift-signal Protocol, for machine-verifiable enforcement) | Drift detection involves comparing current work artifacts against vision.md — this is a `flow` orchestration concern. The signal schema belongs in `core` to satisfy NF-09 traceability. No new container. |
| NF-12 | Explore a Vague Idea Without Structure | v1-core | `flow` (pre-S1 framing mode; "Framer Agent" is a new agent type in the workflow pipeline) | The distinction between `/capture` (soul-level identity action) and "structured exploration" (a new lightweight workflow mode) must be named. This is a `flow` extension, not a new module. |
| NF-13 | Generate Multiple Options at Decision Point | v1-core | `flow` (S3 nowu-options agent — this UC formalizes an already-operational `flow` step) | No container gap. S3 (nowu-options) already handles this. NF-13 is the UC-level formalization of the S3 guarantee. `flow`'s responsibility description should list NF-13 explicitly alongside NF-03. |
| NF-14 | Track Human-AI Work Ratio | v1.1 | `flow` (S9 curator telemetry hook) + `know` (ratio metric atoms, queried by `bridge health`) | Measurement of human vs. AI input is a session-end hook in `flow`; storage in `know`; display via `bridge`. Overlaps ADR-006 scope — both NF-08 and NF-14 are health-metric UCs that should be co-designed. |
| PK-07 | Ingest and Integrate External Documents | v1.1 | `bridge` (ingestion CLI command) + `know` (atom storage for ingested content, with provenance metadata) | Ingestion pipeline (parse → chunk → deduplicate → store) has no architectural design yet. Requires a new ADR (ADR-010). External document sources should be reflected in `context.md` as a new external system. |
| PK-08 | Interact with nowu from Any Interface | v1-core | `bridge` (multi-interface abstraction — extends current CLI to include non-IDE UX channels) | **Most significant gap.** `bridge` is the natural owner (it is the interface layer), but its current definition assumes CLI + VS Code only. "Any interface" implies mobile, web, or lightweight API access. Requires a new ADR (ADR-009) to define permitted interface protocols. Has security implications for ADR-005 (unauthenticated or weakly-authenticated remote access). No new container needed, but `bridge` technology description must be updated. |
| XP-08 | Export Full Project State in Portable Format | v1.1 | `bridge` (export CLI command) + `soul` (state serialisation format definition) | `soul` owns the WAL schema and identity artifacts; `bridge` assembles and serialises. No gap in container ownership — this is a new `bridge` command using existing `soul` conventions. |
| XP-09 | Onboard a New nowu User | v2 | `bridge` (onboarding wizard command) + `flow` (project bootstrap, extends NF-07) | Stage v2; not blocking v1. Container fit is clear: `bridge` entry point + `flow` bootstrap logic. No action needed before v1 completes. |
| XP-10 | Run a Small Company on nowu | v2 | `bridge` + `flow` (company-scale multi-project orchestration) | Stage v2; architectural implications to be analysed at the v2 GAP. Not blocking v1. No action needed. |
| XP-11 | Query Knowledge Graph in Role-Appropriate Format | v1.1 | `core` (role-aware query protocol / MemoryService extension — the "scoping by role" logic) + `bridge` (human-readable CLI rendering at v1.1) + `dash` (visual human rendering at Stage 2+, per ADR-008 activation gate) | **Split ownership across two stages.** At v1.1, `core` owns the role-scoping logic and `bridge` owns the formatted output. `dash` takes over the visual human rendering at Stage 2+ once ADR-008 is ACCEPTED. Requires a new ADR (ADR-011) to formalise this split and prevent premature `dash` scaffolding under the guise of XP-11. |

---

## Answers to the Seven Specific Questions

### Q1: Which container owns PK-08 (ubiquitous access, any interface)?

**Owner: `bridge` — no new container.**

`bridge` is the DDD interface layer: "all user-facing interaction." PK-08 extends that
boundary from CLI + VS Code to any interface the primary persona uses. The question is one
of implementation protocol within `bridge`, not of container ownership.

What needs to change:
- `bridge`'s technology description should change from "Python module / CLI" to
  "Python module / CLI + multi-interface abstraction layer."
- `bridge`'s responsibility must explicitly list PK-08 (multi-interface UX channels).
- A new ADR (ADR-009) must define which interface protocols are permitted, how
  authentication is handled outside a VS Code session, and the activation sequencing
  (CLI remains primary for v1-core; other interfaces are gated behind ADR-009 ACCEPTED).
- ADR-005 must be amended: it currently models a single-user, IDE-bound context. Remote
  access from an unauthenticated device changes the threat model.

There is no architectural justification for a new container (e.g., an "api" or "mobile"
module) before ADR-009 resolves the interface protocol question.

---

### Q2: Which container owns XP-11 (knowledge graph rendering — human vs. agent view)?

**Split ownership: `core` (query logic) + `bridge` (human rendering, v1.1) + `dash` (visual rendering, Stage 2+).**

The vision language is explicit: "same data, different lenses." The data lives in `know`.
The lens logic — deciding what scope and shape to return based on who is asking — is a
`core` concern (MemoryService extension: a role-aware query method). The rendering of that
result is an interface concern:

- **Agent view** (structured, scoped): already handled by `core` MemoryService + `know`
  queries. No gap. Agents query `know` via `core` protocols and receive structured atoms.
- **Human view at v1.1 (CLI)**: `bridge` renders the result as a formatted, condensed
  CLI output. This must be implemented in `bridge` without reaching into `dash`.
- **Human view at Stage 2+ (visual)**: `dash` takes over once ADR-008 is ACCEPTED and
  Stage 2 begins. `dash` reads from `core` contracts only (per ADR-008, Option A).

A new ADR (ADR-011) is required to codify this split and explicitly rule out premature
`dash` scaffolding as an implementation path for XP-11 at v1.1.

---

### Q3: Do NF-10, NF-12, NF-13 belong in `flow` or require container changes?

**All three belong in `flow`. No new container. `flow`'s responsibility description
must be updated to enumerate them.**

- **NF-10** (Maintain the Thread): The orientation assembly is a specialised session mode
  within `flow` — reading WAL checkpoints, recent decisions from `know`, and the current
  task spec, then producing a structured orientation artifact. This is an extension of
  session open/resume logic, which `flow` already owns (NF-01). `bridge` receives the
  human-facing "catch me up" command and hands it to `flow`. No new container.

- **NF-12** (Explore a Vague Idea): A new "Framer Agent" operating as a pre-S1 workflow
  mode. The pipeline already has S1–S9 plus pre-workflow P0–P4; NF-12 adds a lightweight
  "explore" mode that sits before S1 and does not produce binding artifacts. This is
  squarely in `flow`'s domain as the workflow pipeline owner. No new container.

- **NF-13** (Generate Multiple Options): S3 (nowu-options) in `flow` already implements
  this. NF-13 is the UC-level formalization of the S3 guarantee. `flow`'s responsibility
  already covers it operationally. The only change needed is adding NF-13 as an explicit
  UC citation alongside NF-03 in the `flow` responsibility description.

---

### Q4: Does the v1.2 delivery stage require any new ADRs?

**Yes — three new ADRs are required before v1.2 work begins. Two existing ADRs must
be ACCEPTED as prerequisites.**

v1.2 ("Domain projects fully operational", ~18 months) introduces:

| UC | Architectural requirement | ADR needed |
|---|---|---|
| PK-07 (v1.1) | Document ingestion pipeline: parse, chunk, deduplicate, provenance | **ADR-010** (new) |
| PK-08 (v1-core) | Multi-interface access beyond VS Code CLI | **ADR-009** (new) |
| XP-11 (v1.1) | Role-aware knowledge graph rendering contract | **ADR-011** (new) |
| AP-07 (v1.2) | Role-scoped briefing generation — requires sensitivity model | **ADR-005** must be ACCEPTED first |
| RE-07 (v1.2) | Audience-specific reports — same sensitivity + potential `dash` | **ADR-005** + **ADR-008** must be ACCEPTED first |

AP-03, AP-05, RE-02, RE-03, RE-04 (all v1.2) are accommodated in `know`'s existing
model (connection graphs, lifecycle-stage tagging, TASK atoms). No new ADRs required for
those — but ADR-004 (cross-project isolation) must be ACCEPTED before the first AP or RE
project is bootstrapped into `know` (unchanged from 2026-03-29 GAP guidance).

---

### Q5: Is context.md still accurate given persona v2.0 and new external concepts?

**Partially accurate. Two targeted updates are needed; the L1 boundary and actor list
remain structurally sound.**

Delta 1 — **Developer persona description (inaccurate):**
Current: "Triggers workflows via CLI + VS Code. Approves Tier 2 and Tier 3 decisions."
Required: "Triggers workflows via CLI + VS Code AND mobile/remote interfaces (not always
at his desk). Approves Tier 2 and Tier 3 decisions."

The vision v2.0 persona update ("He's not always at his desk when this happens — ideas
arrive or he wants to continue on a commute, at a supplier meeting, mid-dinner") is a
first-class architectural statement that changes what the system boundary must support.

Delta 2 — **New external system: External Document Sources (PK-07):**
PK-07 (Ingest and Integrate External Documents) implies a new external actor: documents
from the outside world (PDFs, URLs, structured data files). This is distinct from
"External Domain Data Sources [Stage 2+]" (which refers to government APIs like
Philippines FDA). PK-07's sources are generic document sources available at v1.1.
A new external system entry is needed in context.md's actor table and the Mermaid diagram.

Delta 3 — **Diagram subtitle (cosmetic but creates confusion):**
The title still reads "Stage 1 v1 · baseline 2026-03-29." The title should reference
the current baseline date when context.md is updated.

What remains accurate: the nowu system boundary, the `know` external system, Git,
File System, VS Code, and the staged future actors (Collaborators, AI Provider API).
The domain-specific external actor "External Domain Data Sources [Stage 2+]" remains
correctly staged.

---

### Q6: Do any of the 8 ADRs conflict with or need updating for the new UC requirements?

**No direct conflicts. Two ADRs need scope amendments before their decision is recorded.**

| ADR | Status | Assessment |
|---|---|---|
| ADR-001 (know API boundary) | PROPOSED | No conflict. XP-11 requires new query patterns from `know` (role-aware scoping), but the decision space (pin/shim/concert) fully covers this. The implementing decision should note XP-11 as a driver. |
| ADR-002 (WAL strategy) | PROPOSED | No conflict. NF-10 (orientation) may produce a new "orientation atom" type in `know` at session start — this fits within any of the three WAL options. |
| ADR-003 (approval queue) | PROPOSED | No conflict. No new UC introduces a new approval queue pattern. |
| ADR-004 (cross-project isolation) | PROPOSED | No conflict. PK-07 document ingestion is a tagged atom per project_scope — fits all three isolation options. |
| ADR-005 (security model) | PROPOSED | **Needs scope amendment.** The current context models a single-user, CLI/IDE-bound environment. PK-08 (ubiquitous access) introduces remote, potentially unauthenticated access from mobile devices. The options (A, B, C) were written without considering a multi-interface threat model. The "Consequences" section must be updated to require that whichever option is chosen, it must also address: (a) token-based auth for non-IDE access, (b) offline-first access pattern implications, (c) what happens if an API surface is exposed. |
| ADR-006 (health metrics) | PROPOSED | No conflict. **Scope note:** NF-11 (Vision Drift detection) and NF-14 (Human-AI Work Ratio) are health-adjacent UCs that should be co-designed with NF-08 in this ADR. The decision should explicitly cover all three. |
| ADR-007 (pattern detection) | PROPOSED | No conflict. |
| ADR-008 (dash activation) | PROPOSED | **Needs clarifying amendment.** XP-11's v1.1 human view (`bridge` CLI rendering) must be explicitly scoped OUT of `dash`. Without this clarification, XP-11 could be used to justify premature `dash` scaffolding ("we need a visual knowledge graph, that's `dash` territory"). The ADR options should add a note: "XP-11 at v1.1 is a `bridge`-rendered CLI concern, not a `dash` concern. `dash` takes over for XP-11's visual rendering at Stage 2+ only." |

---

### Q7: Does ARCHITECTURE.md need updates beyond the UC count correction?

**Yes — four categories of update are needed.**

1. **UC count**: 35 → 47 (plus update the stage map note to include v1.2).

2. **Primary persona update**: The "For Whom" or equivalent section should reflect that
   the primary persona is "not always at his desk" — this is a first-class architectural
   constraint, not a UX preference.

3. **Atomic knowledge layer**: Vision v2.0 added a distinct paragraph on the atomic
   knowledge model. ARCHITECTURE.md should reflect this as a first-class system property.

4. **Module responsibility updates**: The §4.1 module map descriptions should be updated
   to include the new UC ownership assignments:
   - `flow`: add NF-10 (orientation), NF-11 (drift detection trigger), NF-12 (framing
     mode), NF-13 (options guarantee — already operational at S3), NF-14 (telemetry hook)
   - `bridge`: add PK-07 (ingestion command), PK-08 (multi-interface abstraction), XP-08
     (export command), XP-11 (human-readable rendering at v1.1)
   - `core`: add XP-11 (role-aware query protocol in MemoryService), NF-11 (drift-signal
     Protocol)

The v1.2 stage ("Domain projects fully operational") should be added to the product stage
map in ARCHITECTURE.md — it was not present in v1.3 (which predates V1_PLAN.md v2.1's
addition of that stage).

---

## L1 Context — Changes Required (DELTA)

The L1 system boundary, external actor set, and relationships in `context.md` remain
structurally valid. Two targeted changes are required:

**Change 1 — Developer persona label:**
Old: `"Primary user. Triggers workflows via CLI + VS Code. Approves Tier 2 and Tier 3 decisions."`
New: `"Primary user. Triggers workflows via CLI + VS Code AND from mobile/remote contexts (not always at his desk). Approves Tier 2 and Tier 3 decisions."`

In the Mermaid diagram:
```
Person(developer, "Developer (Human)", "Primary user. Triggers workflows via CLI + VS Code and mobile/remote interfaces. Approves Tier 2 and Tier 3 decisions.")
```

**Change 2 — New external system: External Document Sources (PK-07):**
Add to the Mermaid diagram as a current (non-greyed) external system:
```
System_Ext(doc_sources, "External Document Sources", "PDFs, URLs, structured files ingested via PK-07. Accessed by bridge ingestion command; stored as know atoms with provenance.")
Rel(nowu, doc_sources, "Ingests documents", "HTTP / file I/O")
```

Add to the External Actor Reference table:
| External Document Sources | Generic external documents (PDFs, URLs, files) ingested and stored as knowledge atoms via PK-07 ingestion pipeline. | nowu → sources | v1.1 — active |

**Change 3 — Diagram subtitle:**
Update "Stage 1 v1 · baseline 2026-03-29" to "Stage 1 v1 · updated 2026-04-06" when
context.md is amended by gap-writer.

No other L1 context changes are needed. The earlier staged actors (Collaborators/External
Users [Stage 3], AI Provider API [future standalone]) remain correctly staged. The
domain-specific "External Domain Data Sources [Stage 2+]" label remains accurate for
the Philippines FDA / property registry integrations (AP-01, RE-01) — distinct from
PK-07's generic document ingestion.

---

## L2 Containers — Analysis (DELTA)

### Existing containers: assessment vs. new UCs

| Container | Still Valid? | Responsibility Update Needed? | Notes |
|---|---|---|---|
| `core` | Yes | **Yes** — add: XP-11 role-aware query protocol (MemoryService extension); NF-11 drift-signal Protocol | The query-scoping concern for XP-11 is a cross-module contract that belongs in `core`. NF-11 drift detection needs a machine-verifiable signal schema to satisfy NF-09. |
| `flow` | Yes | **Yes** — add: NF-10 (orientation mode), NF-11 (curator drift pass), NF-12 (framing mode / Framer Agent), NF-13 (S3 options guarantee, explicit UC citation), NF-14 (telemetry hook at S9) | `flow` gains 5 new explicit UC ownership entries. The core pipeline responsibility is unchanged. |
| `bridge` | Yes | **Yes** — add: PK-07 (ingestion command), PK-08 (multi-interface abstraction, pending ADR-009), XP-08 (export command), XP-11 (human-rendered CLI output at v1.1); update technology description | Technology description: "Python module / CLI" → "Python module / CLI + multi-interface abstraction layer (scope defined by ADR-009)." |
| `soul` | Yes | **Minor** — XP-08 (export) will read `soul` WAL artifacts; `soul`'s serialization format becomes the export schema source of truth | No new ownership. `soul` provides the format; `bridge` drives the export. |
| `know` (external) | Yes | N/A | Unchanged. Continues to store atoms for all new UCs (NF-10 orientation atoms, NF-14 ratio atoms, PK-07 ingested atoms, XP-11 knowledge graph atoms). Access exclusively via KnowledgeBase + KnowAdapter. |
| `dash` (FUTURE, BLOCKED) | N/A | No change | **Remains blocked.** XP-11's v1.1 human view is explicitly NOT a `dash` concern. `dash` takes XP-11's visual rendering at Stage 2+ only, after ADR-008 is ACCEPTED. |

---

### Proposed new containers

**None proposed.**

All 11 new UCs are accommodated within the existing 4 internal containers plus external
`know`. P3 constraint 1 remains fully intact:

> "No new top-level module without a superseding ADR to D-003."

A new "api" or "mobile" container for PK-08 would be premature before ADR-009 defines
which interface protocols are warranted. If ADR-009 determines that a standalone API
runtime is needed (e.g., a web server), that decision would generate a superseding ADR
to D-003 at that time. For now, `bridge` is the designated owner.

---

### Container responsibility deltas (concrete, for gap-writer)

**`core` — additions:**
```
- Role-aware query protocol (XP-11): MemoryService gains a role-scoped query method
  that returns human-formatted or agent-structured results from know. Contract defined
  in core/contracts/ before S6 implementation begins (P3 constraint 3).
- Drift-signal Protocol (NF-11): machine-verifiable drift signal schema for
  nowu-reviewer enforcement at S8. Prevents NF-11 from becoming a prompt-only concern.
```

**`flow` — additions:**
```
- Multi-project orientation mode (NF-10): extends session open/resume to produce
  an orientation artifact from WAL checkpoints, recent know atoms, and current task spec.
- Vision drift detection pass (NF-11): curator (S9) periodic pass comparing current
  work against vision.md; emits drift signals via core drift-signal Protocol.
- Pre-S1 framing mode (NF-12): lightweight exploration mode ("Framer Agent") that
  produces optional low-fidelity idea captures without triggering S1–S9 pipeline.
- Options guarantee (NF-13): S3 nowu-options agent is the implementation; the UC-level
  guarantee is that every decision point produces ≥2 distinct options with tradeoffs.
- Human-AI ratio telemetry hook (NF-14): S9 post-session hook that computes and writes
  ratio metric atoms to know (co-designed with NF-08 per ADR-006 scope note).
```

**`bridge` — additions and technology update:**
```
Technology: "Python module / CLI + multi-interface abstraction layer
             (scope defined by ADR-009)"

Responsibility additions:
- Document ingestion command (PK-07): CLI command that accepts a file path or URL,
  invokes the ingestion pipeline, and stores resulting atoms in know with provenance.
- Multi-interface UX channels (PK-08): interface abstraction beyond CLI — mobile,
  lightweight web, or other access protocols (architecture to be defined by ADR-009).
- Export command (XP-08): CLI command that serialises full project state from soul
  WAL, know atoms (project-scoped), and state/ artifacts into a portable format.
- Human-readable knowledge rendering (XP-11): formats role-scoped know query results
  into human-readable CLI output. Stage 2+ visual rendering deferred to dash.
```

**`soul` — no changes to responsibility.** XP-08 uses `soul`'s existing WAL format
as the export schema source; no new ownership is added to `soul`.

---

## ADR Candidates (new)

| # | Title | Context | Options to consider | Why it matters |
|---|---|---|---|---|
| ADR-009 | Multi-interface access protocol for `bridge` | PK-08 (v1-core) requires nowu to work beyond CLI + VS Code. "Any interface" is undefined. `bridge` is the owner, but no decision has been made on which protocols, authentication models, or activation sequencing apply. | (A) Lightweight HTTP API served by `bridge`, token-authenticated. (B) Telegram / messaging bot as the mobile interface. (C) Explicit CLI-first: all non-CLI interfaces are deferred until a standalone API ADR supersedes D-003. PK-08's v1-core stage means option C cannot simply defer forever — a minimum viable mobile path must be defined. | PK-08 is v1-core. Without an ADR, any implementation of PK-08 will make arbitrary protocol choices that affect ADR-005 security scope, `bridge` architecture, and potentially D-003 (if a new module is eventually warranted). ADR-009 must also be the security scope input for ADR-005's amendment. |
| ADR-010 | External document ingestion pipeline | PK-07 (v1.1) requires `bridge` to accept external documents (PDFs, URLs, structured files) and store them as know atoms with provenance. No ingestion pipeline exists. Key questions: how to chunk/parse, how to deduplicate against existing atoms, how to track provenance (source, date, confidence), and whether ingestion is synchronous or async. | (A) Synchronous ingestion in `bridge` command: parse → chunk → deduplicate → store atoms in a single CLI invocation. (B) Async ingestion: `bridge` queues an ingestion request; a `flow` hook processes it as a background task. (C) Delegate to an external ingestion service / `know` enhancement: `know` gains an `ingest_document()` API that handles all pipeline logic. | PK-07 is v1.1 and feeds AP-04 (market intelligence), AP-01 (regulatory requirements), and RE-01 (process inventory) — all of which depend on external document knowledge. Without a defined pipeline, document ingestion will be ad-hoc and provenance will be lost. Security implication: ingesting external content into `know` without sanitisation is an injection risk (OWASP A03). Deduplication strategy affects XP-01 (cross-project discovery) quality. |
| ADR-011 | Role-appropriate knowledge graph rendering | XP-11 (v1.1) requires the same knowledge graph to be rendered differently for human vs. agent consumers. No rendering contract exists. The split between `core` (query logic), `bridge` (v1.1 CLI rendering), and `dash` (Stage 2+ visual rendering) must be formalised before XP-11 implementation begins — to prevent either premature `dash` scaffolding or coupling `core` to presentation concerns. | (A) `core` owns a `query_for_role(role: Role)` method; `bridge` owns all rendering for v1.1; `dash` takes over visual rendering at Stage 2+. (B) `bridge` owns both the query parameterisation and the rendering at v1.1; `core` provides no role-specific API. (C) Role-rendering is a `know` capability: `know` API accepts a `render_mode` parameter and returns pre-formatted output. | Without this ADR, XP-11 implementation at v1.1 will likely reach into `dash` scope (violating P3 constraint 6), or place rendering logic in `core` (violating the domain/interface layer boundary from D-002). The decision also determines whether `dash` can cleanly inherit the human rendering at Stage 2+ without a rewrite. |

---

## Existing ADRs That Need Amendment

### ADR-005 — Security and sensitivity model for knowledge atoms

**Amendment required: expand scope to include multi-interface access control.**

Current context models a single-user, VS Code / CLI-bound environment. PK-08 changes the
threat model: if nowu is accessible from a mobile device or lightweight API, the following
attack surfaces appear that the current ADR options do not address:

1. **Unauthenticated access**: a shared device or network intercept could expose all
   knowledge atoms if the only authentication is the user's IDE session.
2. **API token leakage**: if `bridge` exposes an HTTP endpoint, token management (issuance,
   rotation, revocation) must be decided.
3. **Offline access**: "on a commute" implies possibly offline-capable UX — which raises
   questions about local caching of sensitive atoms.

The amendment must add to the Options Considered section (before the human records a
decision):

> **Multi-interface scope extension (applies to whichever option is chosen):** The
> accepted option must also specify: (a) how authentication works for non-IDE access
> (token-based, OAuth, passphrase?); (b) whether sensitive atoms (PK-06 class) are
> excluded from mobile/API rendering entirely; (c) what happens to locally-cached atoms
> on a lost device.

ADR-009 (multi-interface access protocol) defines which protocols are permitted.
ADR-005's decision must be compatible with ADR-009's choice.

---

### ADR-008 — dash scope, dependencies, and activation trigger

**Amendment required: explicit note that XP-11 at v1.1 is NOT a dash concern.**

Without this note, an implementer of XP-11 at v1.1 could reasonably interpret
"knowledge graph rendering for a human" as a `dash` requirement, triggering a P3
constraint 6 violation (scaffolding `dash` before ADR-008 is ACCEPTED and Stage 2).

Add to the ADR context and to each option's Consequences:

> **XP-11 scope clarification (v1.1):** XP-11's "human view" at v1.1 is a `bridge`
> CLI rendering concern — a formatted text output from a role-scoped `know` query.
> It is NOT a `dash` concern. `dash` takes over XP-11's visual and interactive
> human rendering at Stage 2+, after this ADR is ACCEPTED. Implementing XP-11 before
> ADR-008 is ACCEPTED does not require, justify, or permit scaffolding a `dash/`
> directory.

---

## Constraints for P3 (effective immediately, additions to 2026-03-29 baseline)

These constraints extend the six constraints established on 2026-03-29. All six prior
constraints remain in force unchanged.

7. **PK-08 implementation (`bridge` multi-interface) must not begin until ADR-009 is
   ACCEPTED.** The interface protocol and authentication model are undecided. Any
   `bridge` code that hardcodes a specific protocol (e.g., an HTTP server) before ADR-009
   is accepted is an architecture violation.

8. **PK-07 ingestion pipeline must not begin until ADR-010 is ACCEPTED.** Provenance
   tracking, deduplication strategy, and the async/sync question must be resolved before
   writing any ingestion code. Ingesting external content without input sanitisation is an
   injection risk (OWASP A03) — ADR-010 must address this explicitly.

9. **XP-11 implementation must not conflate `bridge` rendering (v1.1) with `dash` (Stage
   2+).** ADR-011 must be ACCEPTED before XP-11 implementation begins. Any rendering code
   for XP-11 at v1.1 must live in `bridge`, not in a `dash/` directory.

10. **NF-14 and NF-11 metric/signal schemas must be designed jointly with NF-08 under
    ADR-006.** Three health-adjacent UCs (NF-08, NF-11, NF-14) must share a common metric
    atom schema in `know`. Implementing any one of these before ADR-006 is ACCEPTED risks
    creating divergent metric formats that cannot be queried together.

---

## What Stays the Same (explicit baseline confirmation)

The following elements from the 2026-03-29 baseline are UNCHANGED by this pass:

1. **The 5-module structure** (`core`, `flow`, `bridge`, `soul`, external `know`) is
   confirmed valid for all 47 active UCs. No new top-level module is proposed. D-003
   is not superseded.

2. **All 36 UC assignments from the 2026-03-29 matrix** remain valid and are not
   modified by this pass.

3. **All binding decisions D-001 through D-010** remain ACCEPTED and unchanged.

4. **P3 constraints 1–6 from the 2026-03-29 baseline** remain in force; constraints
   7–10 above extend but do not replace them.

5. **ADR-001 through ADR-008 statuses** (all PROPOSED) are unchanged. ADR-005 and
   ADR-008 require scope amendments to their option text before the human records
   a decision, but their status and the core architectural question each ADR addresses
   are unchanged.

6. **`soul`'s responsibility** does not change. `soul` remains a storage and convention
   layer; it does not gain new business logic from any new UC.

7. **`know` remains external.** No new internal reimplementation is proposed. All new
   UCs that store atoms (NF-10, NF-14, PK-07, XP-11, XP-08) do so exclusively via
   `KnowledgeBase` + `KnowAdapter` (D-006).

8. **`dash` remains BLOCKED** until ADR-008 is ACCEPTED and the product is at Stage 2
   or later. XP-11 at v1.1 does not change this gate.

9. **The `know` version (v0.4.0) and access contract (D-006)** are unchanged. XP-11's
   role-scoped query may require new `know` API methods — if so, this requires either a
   `know` contribution (bump to v0.5.0) or a shim in `core`, per ADR-001's decision scope.

10. **ADR-004 (cross-project isolation) must still be ACCEPTED** before the first AP
    or RE project is bootstrapped into `know`. PK-07's document ingestion adds a new
    driver for this decision (ingested atoms must be project-scoped) but does not change
    the decision space.

---

## Open Questions for Human

1. **PK-08 minimum viable path**: "any interface" for v1-core — is there a concrete
   primary target (e.g., a Telegram bot, a lightweight web UI, an iOS shortcut)? This
   determines which ADR-009 option is viable and sets the security scope for ADR-005's
   amendment.

2. **ADR-005 + ADR-009 sequencing**: Should ADR-009 (interface protocol) be
   ACCEPTED before or concurrently with ADR-005 (security model)? Accepting ADR-005
   without knowing the interface protocol leaves the access control section under-specified.

3. **XP-11 `know` API**: Does `know` v0.4.0 support role-based query filtering natively,
   or will a new `know` API method be needed? If a `know` contribution is required, this
   creates a cross-repo coordination dependency that V1_PLAN.md Step 02 (Memory Integration
   Layer) should flag.

4. **NF-12 / idea explosion risk**: The "Framer Agent" is a new agent type. Should it be
   defined as a standalone `.agent.md` file under `.claude/skills/` (like existing agents),
   or as a mode of the `nowu-intake` agent? This requires a skill authoring decision that
   affects the `.claude/` agent configuration.

5. **v1.2 ADR sequencing**: ADR-009, ADR-010, and ADR-011 are all prerequisites for v1.1
   and v1.2 UCs. Should these three ADRs be authored in parallel (same planning session),
   or must ADR-009 be ACCEPTED before ADR-005's amendment is finalized?

---

## Recommended Next Steps

1. Human reviews this proposal and marks it APPROVED or requests changes (Tier 2 review).
2. Human amends ADR-005: add multi-interface access control scope to the options section.
3. Human amends ADR-008: add XP-11 v1.1 scope clarification note.
4. Human authors ADR-009, ADR-010, ADR-011 using `templates/adr.md`. Prioritize ADR-009
   (PK-08 is v1-core) and ADR-011 (XP-11 is v1.1, needed before XP-11 implementation).
5. Human (or gap-writer agent) updates `docs/architecture/context.md`:
   - Developer persona description (Delta 1 above)
   - External Document Sources system entry (Delta 2 above)
   - Diagram subtitle date (Delta 3 above)
6. Human (or gap-writer agent) updates `docs/architecture/containers.md`:
   - `core`: add XP-11 query protocol and NF-11 Protocol ownership
   - `flow`: add NF-10, NF-11, NF-12, NF-13, NF-14 responsibility entries
   - `bridge`: update technology description; add PK-07, PK-08, XP-08, XP-11 entries
   - P3 constraints: append constraints 7–10 from this pass
7. Human updates `docs/ARCHITECTURE.md`:
   - UC count: 35 → 47
   - UC count reference in stage map (if present)
   - Add v1.2 stage to stage overview
   - Module responsibility map: add new UC citations per step 6 above
   - Primary persona: add "not always at his desk" context
   - Atomic knowledge layer: add as a first-class system property per vision v2.0
8. Human sets `state/arch/gap-trigger.md` status to CLOSED.
9. Run `/health-check architecture` to verify containers.md and context.md are consistent.
