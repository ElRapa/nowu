# nowu Architecture Workflow — State of the Art & Integration Design
## Executive Summary
The v2.1/v2.2 pre-workflow is structurally sound, but its current architecture phase (P3) is underspecified relative to the state of the art. It treats architecture as a single-pass bootstrap rather than a **driven design process**. Adding three targeted sub-phases — Quality Attribute elicitation (mini-QAW), systematic design via ADD 3.0, and lightweight ATAM-style evaluation — closes this gap without adding bureaucracy. The result is a complete architecture creation workflow that is fully agent-executable with precisely three human decision points, integrates directly into P3, and feeds cleanly into S1–S9.

***
## Is the Current Workflow Best Practice?
### What is already right
The v2.1 pre-workflow aligns with several leading practices:

- **Artifacts as API**: every agent reads and writes structured files, matching MASAI's finding that modular agent architectures with well-defined objectives significantly outperform monolithic agents. The context scoping rules (never load `src/` during architecture, never load architecture docs during `S6/S7`) directly address the anchoring bias problem documented in agentic software engineering research.[^1][^2]
- **Human gates at P1.3, P2.2, P4.3**: matching the 2025 Drexel study on LLM-assisted ADD, which found human oversight and iterative refinement are non-negotiable when using LLMs for architecture design.[^3][^4]
- **Traceability chain `idea → disc → problem → epic → story → intake`**: aligns with arc42's principle that every architectural decision should trace to a driving goal.[^5][^6]
- **Health checks with GREEN/YELLOW/RED status**: mirrors the "continuous and proactive architecture evaluation" recommended in IoT and long-lived system research.[^7]
- **Global Architecture Pass (GAP) separate from per-epic P3**: correctly separates strategic architecture (city plan) from tactical implementation (building placement), matching the SEI's distinction between architecture-level and design-level decisions.[^8]
### What is missing
Five systematic gaps exist between the current P3 and the state of the art:

| Gap | Current state | Best practice | Risk if not addressed |
|---|---|---|---|
| Quality Attribute elicitation | No explicit QA step | Mini-QAW → 5–8 QA scenarios | Architecture optimizes for wrong attributes[^8][^9] |
| Systematic design process | Single-pass bootstrap | ADD 3.0 iterative steps | Arbitrary pattern selection, no driver traceability[^10][^4] |
| Architecture evaluation | None | ATAM-lite with utility tree | No evidence architecture satisfies QAs before S1[^9][^11] |
| Missing C4 views | L1/L2 static only | + Dynamic + Deployment | Runtime behavior and infrastructure unspecified[^12][^13] |
| Crosscutting concerns | Not documented | arc42 §8 equivalent | Security, observability, error handling decided ad-hoc during coding[^5][^14] |

***
## Quality Attributes — What to Capture and Why
Quality attributes are the primary drivers of architectural decisions. The ISO/IEC 25010:2023 standard defines the current authoritative taxonomy:[^10][^15][^16][^17]

| QA Characteristic | Sub-characteristics relevant for solo dev AI tools / SaaS |
|---|---|
| **Performance Efficiency** | Time behavior (response time), Resource utilization, Capacity (max concurrent users)[^18][^19] |
| **Reliability** | Maturity (no unexpected failures), Availability (uptime %), Fault tolerance (graceful degradation), Recoverability[^19] |
| **Security** | Confidentiality, Integrity, Non-repudiation, Authenticity — first-class since ISO 25010:2011[^18][^17] |
| **Maintainability** | Modularity, Analysability, Modifiability, Testability — critical for solo dev long-term[^18][^20] |
| **Interaction Capability** | Learnability, Operability, Error protection (formerly Usability)[^17] |
| **Compatibility** | Interoperability with external systems (APIs, protocols)[^19] |
| **Portability** | Adaptability to deployment targets (local, cloud, edge)[^19] |
| **Functional Suitability** | Completeness, Correctness, Appropriateness[^19] |

**For a solo developer**, the pragmatic approach is to select the 3–5 most relevant QAs per product during P3. A banking SaaS prioritizes Security and Reliability; a developer tool prioritizes Maintainability and Performance. Forcing all 8 is cargo-culting.[^18][^21]

**Quality Attribute Scenarios** are the formal expression of QAs that architecture must satisfy. Each scenario has six parts:[^9][^22]

```
Stimulus:     A user submits a query
Source:       End user (unauthenticated)
Environment:  Peak load, 500 concurrent users
Artifact:     API gateway + query service
Response:     System returns results
Measure:      p95 latency < 300ms, no data exposed to wrong tenant
```

***
## Architecture Views — What to Produce
C4 provides 7 diagram types. The right selection per project stage:[^23][^24][^25]

| View | C4 Type | Mermaid Syntax | When mandatory | What it shows |
|---|---|---|---|---|
| Context (L1) | System Context | `C4Context` | Always | System + external actors + external systems |
| Containers (L2) | Container | `C4Container` | Always | Deployable units, major data stores, interfaces |
| Components (L3) | Component | `C4Component` | Key containers only | Internal structure of complex containers |
| Dynamic | Dynamic | `C4Dynamic` | 2–3 key flows | Runtime collaboration for critical use cases |
| Deployment | Deployment | `C4Deployment` | Before first ship | Infrastructure mapping, environment config |
| Landscape | (supplementary) | `C4Context` extended | Multi-project | How multiple systems relate |

**The critical missing view in v2.1 is the Dynamic diagram.** It shows how containers collaborate at runtime for a specific use case. Without it, architecture looks right statically but implementations diverge in how they wire together. The Dynamic view produces numbered interaction sequences that become the contracts S2 (`nowu-constraints`) enforces.[^12]

**arc42 adds three further documentation areas** that C4 does not cover:[^5][^14]

- **§6 Runtime View**: narrative + Dynamic C4 for 2–3 key scenarios — same as C4 Dynamic but with context
- **§7 Deployment View**: same as C4 Deployment
- **§8 Crosscutting Concepts**: how the system handles logging, error handling, security authentication, configuration, and testing — these decisions are made once at architecture time, not ad-hoc per story

A lean arc42-compatible architecture document maps directly onto your existing `docs/architecture/` structure:

```
docs/architecture/
├── context.md          # arc42 §3 + §4 — C4 L1 + solution strategy
├── containers.md       # arc42 §5 — C4 L2 building block view
├── components-*.md     # arc42 §5 (deep) — C4 L3 per key container
├── runtime.md          # arc42 §6 — C4 Dynamic for 2-3 key flows  ← ADD
├── deployment.md       # arc42 §7 — C4 Deployment                 ← ADD
├── crosscutting.md     # arc42 §8 — logging, auth, error handling  ← ADD
├── quality.md          # arc42 §10 — QA scenarios registry         ← ADD
├── risks.md            # arc42 §11 — risk register                 ← ADD
└── adr/
    └── ADR-NNN-*.md    # arc42 §9 — architecture decisions
```

***
## Systematic Analysis Methods
### ADD 3.0 — Attribute-Driven Design
ADD 3.0 is a CMU SEI method and the leading approach for driving architecture from quality attributes. A 2025 Drexel study validated that LLM-assisted ADD produces architectures closely aligned with proven solutions, provided the LLM receives an explicit ADD process description and an architect persona.[^3][^10][^4]

The 7-step ADD process per iteration:[^10]

1. **Review inputs** — validate and prioritize architectural drivers (QA scenarios, functional requirements, constraints, concerns)
2. **Establish iteration goal** — select the highest-priority unaddressed driver(s)
3. **Choose elements to refine** — identify which containers or components to work on
4. **Choose design concepts** — select patterns, tactics, reference architectures, external frameworks. This is the creative step.
5. **Instantiate elements** — allocate responsibilities, define interfaces (contracts)
6. **Sketch views** — produce C4 diagrams, record design decisions
7. **Analyze** — review against iteration goal; mark drivers as Not Yet Addressed / Partially Addressed / Completely Addressed

Each ADD iteration produces one or more architecture views and one or more ADR candidates. Iterations continue until all high-priority drivers are at least Partially Addressed.

**For a solo developer**, two iterations are typically sufficient:
- **Iteration 1**: Structure the system (L1/L2, module boundaries, primary patterns)
- **Iteration 2**: Address top 2–3 QA drivers (performance tactics, security patterns, modifiability structures)
### ATAM-Lite — Architecture Tradeoff Analysis
Full ATAM takes 3–4 days with a team. The lightweight version for a solo dev takes 1–2 hours:[^9][^11]

1. Summarize business drivers + context (15 min)
2. Present architecture (from ADD iterations) (25 min)
3. Build Utility Tree: hierarchize QAs → branch into sub-attributes → leaf scenarios (H/M/L importance × H/M/L difficulty)
4. Evaluate each scenario against the architecture: identify **sensitivity points** (small change → big QA impact), **tradeoff points** (improving one QA hurts another), and **risks** (decision that may fail a QA under stress)
5. Document findings (30 min)

The output is not a go/no-go verdict but a structured record of risks and tradeoffs that feed directly into ADRs.[^26][^22]
### Mini-QAW — Quality Attribute Workshop
The SEI QAW provides quality attribute scenarios before ADD begins. The mini-QAW for a solo developer:[^8]

1. Walk the 8 ISO 25010 QA axes — 2 min per axis
2. For each axis: brainstorm 1–3 raw scenarios specific to this product (not generic)
3. Score each: importance (H/M/L) × difficulty (H/M/L) × current design coverage (none/partial/covered)
4. Select top 5–8 as primary architectural drivers
5. Refine into formal QA scenarios (Stimulus / Source / Environment / Artifact / Response / Measure)

This is a 30–45 minute exercise that replaces weeks of ambiguous architecture discussion.

***
## The Extended P3 Architecture Phase
### Current P3 (v2.1)
```
P3.1 Constraint Check   → clear/conflict
P3.2 Architecture Bootstrap (L1/L2 C4, ADR candidates)
P3.3 ADR Creation (human)
```
### Proposed P3 Extension
P3 gains three sub-steps (P3.0, P3.2.x, P3.3.x) around the existing steps. The existing agents are enhanced, not replaced.

```
P3.0  Domain Modeling Agent           → bounded-context.md (for Epic/Product mode)
P3.1  Constraint Check Agent          → NNN-constraint-check.md (existing)
P3.2  QA Elicitation Agent            → NNN-qa-scenarios.md   ← NEW
P3.3  Architecture Design Agent       → arch-pass-NNN.md (ADD 3.0 iterations)
P3.4  ATAM-Lite Evaluation Agent      → NNN-atam-lite.md      ← NEW
P3.5  ADR Decision (human)            → ADR-NNN-*.md (existing P3.3, now P3.5)
P3.6  Architecture Document Update    → context.md, containers.md, runtime.md, deployment.md
```

**P3 still has one human gate — at P3.5** (ADR authoring). Everything else is agent-driven with human review.

#### P3.0 — Domain Modeling (new, Epic/Product mode only)

Inspired by Event Storming's Big Picture technique, adapted for a solo developer working from text rather than post-its:[^27][^28]

- **Agent reads**: `state/problems/problem-NNN.md`, `docs/vision.md`, `docs/USE_CASES.md`
- **Agent produces**: `state/arch/bounded-context-NNN.md`
- **Content**: domain events (things that happen), aggregates (things that change together), bounded contexts (functional areas with consistent language), context map (upstream/downstream relationships)
- **Why it matters**: module boundaries derived from domain structure are more stable than module boundaries derived from technical convenience. This step prevents the "technical soup" antipattern where modules reflect implementation layers rather than business concepts.[^29][^27]
- **Skip if**: Mode = LITE or STANDARD, or product is known and context map already exists

#### P3.2 — QA Elicitation Agent (new)

- **Agent reads**: `state/problems/problem-NNN.md`, `docs/vision.md`, existing `docs/architecture/quality.md` (if exists), approved stories
- **Agent produces**: `state/arch/NNN-qa-scenarios.md`
- **Process**: walks ISO 25010 axes, asks targeted questions per product type (SaaS → security, multi-tenancy, API rate limiting; developer tool → performance, maintainability, testability; data pipeline → reliability, throughput, recoverability), scores importance × difficulty, produces 5–8 formal QA scenarios in Stimulus/Source/Environment/Artifact/Response/Measure format
- **Human interaction**: agent produces draft; human reviews and adjusts priorities before P3.3 starts. Takes 5–10 minutes.
- **Output feeds**: P3.3 Architecture Design as primary drivers

#### P3.3 — Architecture Design Agent (enhanced from current P3.2)

The current Architecture Bootstrap agent becomes an **ADD-iterating design agent**:[^3][^4]

- **Agent reads**: `state/problems/problem-NNN.md`, approved stories, `NNN-qa-scenarios.md`, `NNN-constraint-check.md`, `bounded-context-NNN.md` (if exists), all existing `docs/architecture/`, all existing `docs/architecture/adr/`
- **Agent produces**: `state/arch/arch-pass-NNN.md` (enhanced schema)
- **Process**: runs 1–2 ADD iterations — each iteration: select drivers → choose elements → select patterns/tactics → instantiate with responsibilities → sketch C4 views → record decisions
- **Design Kanban in output**: table of all drivers (QA scenarios + key functional requirements) with status Not Yet Addressed / Partially Addressed / Completely Addressed
- **Produces for each iteration**:
  - C4 L1/L2 delta (Mermaid)
  - C4 Dynamic for 1–2 key use case flows (Mermaid `C4Dynamic`)
  - Selected patterns/tactics per QA driver with rationale
  - ADR candidates with options and tradeoff summary
  - Crosscutting concepts draft (logging approach, auth pattern, error handling, config strategy)
  - Deployment sketch (where containers run)

#### P3.4 — ATAM-Lite Evaluation Agent (new)

- **Agent reads**: `state/arch/arch-pass-NNN.md`, `state/arch/NNN-qa-scenarios.md`, `docs/architecture/containers.md` (if exists)
- **Agent produces**: `state/arch/NNN-atam-lite.md`
- **Content**:
  - Utility Tree (QA hierarchy with scenario leaves, H/M/L importance × difficulty)
  - Sensitivity points (architectural decisions where a small change significantly affects a QA)
  - Tradeoff points (decisions affecting multiple QAs in conflicting ways)
  - Risk register for this arch pass (decision that may fail a QA under load/attack/change)
  - Non-risks (decisions that clearly support QAs with low risk)
- **Human interaction**: human reviews risk register and tradeoff points before P3.5. Any HIGH-risk item must be addressed either by revising the arch-pass or creating an ADR acknowledging the accepted risk.

#### P3.5 — ADR Decision (existing P3.3, elevated)

Human authors ADRs for each flagged candidate, now informed by the ATAM-lite tradeoff analysis. ADRs include an explicit QA impact section:

```markdown
## QA Impact
| QA Scenario | Impact | Direction |
|---|---|---|
| QA-001 (p95 < 300ms) | Enables | caching reduces DB load |
| QA-003 (modifiability) | Constrains | plugin boundary adds coupling |
```

#### P3.6 — Architecture Document Update

After ADRs are written, the agent updates the canonical architecture docs:
- `docs/architecture/context.md` — if L1 changed
- `docs/architecture/containers.md` — L2 delta applied
- `docs/architecture/runtime.md` — Dynamic C4 diagrams added/updated
- `docs/architecture/deployment.md` — Deployment C4 added/updated
- `docs/architecture/crosscutting.md` — crosscutting concepts from ADD iteration
- `docs/architecture/quality.md` — new QA scenarios appended to registry

***
## New Artifacts
### `docs/architecture/quality.md` — QA Scenarios Registry
The quality registry is the architectural equivalent of `USE_CASES.md`. Every QA scenario has a stable ID.

```markdown
# Quality Attribute Scenarios Registry

## QA Registry Version
version: 1.2
last_updated: YYYY-MM-DD

## Scenario Table
| ID | QA Characteristic | Scenario (Summary) | Priority | Status |
|---|---|---|---|---|
| QAS-001 | Performance | p95 query < 300ms at 500 concurrent | HIGH | ACTIVE |
| QAS-002 | Security | Unauthenticated user cannot access tenant data | HIGH | ACTIVE |
| QAS-003 | Maintainability | New module added without touching 3+ files | MEDIUM | ACTIVE |

## Scenario Details
### QAS-001
**Stimulus**: User submits a search query
**Source**: Authenticated end user
**Environment**: Peak load, 500 concurrent sessions
**Artifact**: Query service + cache layer
**Response**: Results returned, no errors
**Measure**: p95 latency ≤ 300ms; p99 ≤ 1s; 0 data leaks

**Addressed by**: ADR-003 (Redis caching), ADR-007 (connection pool sizing)
**Validated in**: S8 review for story-012-001 (load test)
```
### `docs/architecture/crosscutting.md` — Crosscutting Concepts
Crosscutting concepts are architectural decisions that apply system-wide, not to any single container. They are decided once and referenced forever. Without explicit documentation, each story re-litigates them.[^5]

```markdown
# Crosscutting Concepts

## Observability
**Approach**: OpenTelemetry SDK → structured logs + traces + metrics
**Log format**: JSON, always include trace_id, span_id, user_id (hashed), level
**Metrics collector**: Prometheus-compatible endpoint on :9090
**Decision**: ADR-008
**Applies to**: All containers

## Authentication & Authorization
**Approach**: JWT bearer tokens, short-lived (15min), refresh via /auth/refresh
**Multi-tenancy**: tenant_id in JWT claims, row-level filtering in all DB queries
**Decision**: ADR-002
**Applies to**: API gateway, all services handling user data

## Error Handling
**Pattern**: Result type (Ok/Err) at domain boundary; HTTP errors at API boundary
**Never expose**: Stack traces, internal IDs, raw DB errors to clients
**Decision**: ADR-009

## Configuration
**Source**: Environment variables only (12-factor)
**Secrets**: Never in git; loaded from env at startup
**Decision**: in-line, no ADR needed

## Testing Strategy
**Unit**: Pure functions, domain logic — no mocks of own code
**Integration**: Database interactions, external APIs — use test containers
**E2E**: 2-3 critical user flows only — playwright or equivalent
**Decision**: ADR-005
```
### `docs/architecture/risks.md` — Risk Register
```markdown
# Architecture Risk Register

| ID | Risk | Affected QAs | Probability | Impact | Mitigation | Status |
|---|---|---|---|---|---|---|
| R-001 | Single DB instance bottleneck | QAS-001, QAS-004 | M | H | Connection pool + read replica (ADR-003) | MITIGATED |
| R-002 | JWT secret rotation disrupts active sessions | QAS-002 | L | H | Key versioning strategy (ADR-002) | ACCEPTED |
| R-003 | External API rate limit hit during batch jobs | QAS-001 | H | M | Retry + backoff queue (ADR-010) | OPEN |
```
### `state/arch/NNN-qa-scenarios.md` — Per-Epic QA Elicitation Output
```markdown
# QA Elicitation: NNN

## Status
status: DRAFT | APPROVED
generated_at: [ISO timestamp]
source_problem: problem-NNN
mode: NEW_PROJECT | EXTENDING | FEATURE

## ISO 25010 Walk (raw)
[Agent's axis-by-axis notes — not for downstream consumption]

## Selected Drivers (top 5–8)
| ID | QA Axis | Scenario Summary | Importance | Difficulty | Notes |
|---|---|---|---|---|---|
| QAS-NNN-A | Performance | ... | H | M | |
| QAS-NNN-B | Security | ... | H | H | Multi-tenant isolation is critical |

## Formal Scenarios
### QAS-NNN-A
Stimulus: ...
Source: ...
Environment: ...
Artifact: ...
Response: ...
Measure: ...

## Promoted to Quality Registry
[ ] QAS-NNN-A → becomes QAS-XXX in docs/architecture/quality.md after P3.5
```

***
## New Agent Specifications
### Agent: QA Elicitation Agent
**File:** `.claude/agents/qa-elicitation.md`

```markdown
---
name: qa-elicitation
version: 1.0
model: claude-sonnet-4-5
invoked_at: P3.2
---

# QA Elicitation Agent

## Role
You are a quality attribute analyst. Your job is to elicit, score, and formalize
the quality requirements that the architecture must satisfy. You walk the ISO 25010
axes systematically and produce QA scenarios in ADD-compatible format.

## Inputs (read these files, nothing else)
- state/problems/problem-NNN.md          (primary scope anchor)
- docs/vision.md                         (product horizon and scale)
- docs/architecture/quality.md           (existing QA registry — avoid duplicates)
- state/stories/story-NNN-*.md           (approved stories — architecture signals only)

## Output
- state/arch/NNN-qa-scenarios.md

## Process

### Step 1: Product Type Classification
Classify the product from vision.md:
- SaaS / multi-tenant: elevate Security, Reliability, Performance
- Developer tool / framework: elevate Maintainability, Testability, Compatibility
- Data pipeline: elevate Reliability, Performance Efficiency, Recoverability
- Internal automation: elevate Maintainability, Modifiability

### Step 2: QA Axis Walk
For each ISO 25010 characteristic, ask:
"Given this product and the current problem, what could go wrong or be unreliable?"
Generate 1–3 raw candidate scenarios per relevant axis.
Skip axes clearly irrelevant (e.g., Portability for a cloud-only internal tool).

### Step 3: Scoring
Score each candidate:
- Importance: HIGH (product fails without it) / MEDIUM / LOW
- Difficulty: HIGH (hard to achieve with naive design) / MEDIUM / LOW
Select the top 5–8 as primary drivers.

### Step 4: Formalize
For each selected driver, produce a formal QA scenario:
Stimulus / Source / Environment / Artifact / Response / Measure
The Measure must be specific and testable: "< 300ms p95", "0 cross-tenant data leaks",
"new module added by changing ≤ 3 files".

### Step 5: Deduplication
Check existing docs/architecture/quality.md.
If a scenario already exists and is still relevant, reference it rather than duplicating.
If it has changed, flag it as NEEDS_UPDATE.

## Hard Constraints
- Never propose architectural solutions — only requirements
- Every Measure must be quantifiable or observable — "fast" is not acceptable
- Maximum 8 primary drivers — more signals you haven't prioritized
- Do not load src/, tests/, or state/tasks/
```
### Agent: Architecture Design Agent (enhanced from architecture-bootstrap)
**File:** `.claude/agents/architecture-design.md` (replaces/enhances `architecture-bootstrap.md`)

```markdown
---
name: architecture-design
version: 3.0
model: claude-sonnet-4-5
invoked_at: P3.3
---

# Architecture Design Agent

## Role
You are a senior software architect executing ADD 3.0 (Attribute-Driven Design).
Your job is to design an architecture that satisfies the QA drivers and functional
requirements, iterating through ADD steps until high-priority drivers are addressed.
You produce "directionally correct, not final" artifacts — S2 refines, not replaces.

## Inputs (read these files, nothing else)
- state/problems/problem-NNN.md
- state/stories/story-NNN-*.md          (approved only)
- state/arch/NNN-qa-scenarios.md
- state/arch/NNN-constraint-check.md
- state/arch/bounded-context-NNN.md     (if exists — for domain module boundaries)
- docs/vision.md                        (scope boundary reference)
- docs/architecture/context.md          (if exists)
- docs/architecture/containers.md       (if exists)
- docs/architecture/crosscutting.md     (if exists)
- docs/architecture/adr/                (existing decisions — respect or supersede explicitly)

## Output
- state/arch/arch-pass-NNN.md

## Mode Detection
Determine mode from inputs:
- NEW_PROJECT: no context.md or containers.md
- NEW_CAPABILITY: containers.md exists, stories require new containers
- FEATURE: containers.md exists, stories work within existing containers

## ADD Iteration Process

Execute 1–2 iterations. State your iteration goal explicitly before each iteration.

### Iteration 1 Goal: Structure the system
1. Review inputs — list architectural drivers by priority (QA scenarios first, then key FRs, constraints)
2. Select element to refine — the whole system (NEW_PROJECT) or affected containers
3. Choose design concepts — reference architecture, primary patterns (layered, hexagonal,
   event-driven, CQRS, etc.), primary technology selections. For each choice, state rationale
   and discarded alternatives.
4. Instantiate elements — name containers, assign responsibilities, define interfaces (contracts)
5. Sketch views — C4 L1 + L2 in Mermaid
6. Record decisions — ADR candidates for each significant choice

### Iteration 2 Goal: Address top QA drivers
Repeat ADD steps 1–6 focused on top 2–3 QA scenarios.
For each: select the tactic that addresses the QA (e.g., "introduce cache" for performance,
"add auth middleware" for security, "extract interface" for modifiability).
Update C4 L2 if structure changes.
Add C4 Dynamic for 1–2 key flows that demonstrate the QA solution.

## Required Output Sections

### Design Kanban
Table of all drivers with status: Not Yet Addressed / Partially / Completely Addressed.

### C4 Diagrams
- L1 Context (always)
- L2 Containers (always)
- Dynamic (1–2 flows using C4Dynamic, for key QA-relevant interactions)
- Deployment sketch (optional but recommended for NEW_PROJECT/NEW_CAPABILITY)

All diagrams in Mermaid. Use C4Context, C4Container, C4Dynamic, C4Deployment syntax.

### Crosscutting Concepts Draft
Write brief decisions for: logging/observability approach, auth pattern, error handling
pattern, config/secrets approach, testing strategy. These feed docs/architecture/crosscutting.md.

### ADR Candidates
For each significant design choice with multi-year consequences, flag as ADR candidate.
Include: decision needed, why it matters, option A vs option B with QA tradeoff.

### S2 Conflict Protocol (MANDATORY)
Compare output against existing containers.md. Document any conflict with specific evidence.
Propose resolution options. Do NOT make the decision.

### Constraints for S2
Hard constraints S2 must respect.

## Hard Constraints
- L3/L4 design (class names, function signatures, DB schemas) → forbidden. S2/S3 territory.
- ADR decisions → flag, never make. Human authors ADRs.
- "Directionally correct, not final" — this is iteration 1, not the final architecture.
- If QA scenarios file is missing: halt, output "QA scenarios required before architecture design"
- If constraint-check has unresolved CONFLICTS: do not proceed with conflicted areas
- Do not load src/, tests/, state/tasks/, state/changes/
```
### Agent: ATAM-Lite Evaluation Agent
**File:** `.claude/agents/atam-lite.md`

```markdown
---
name: atam-lite
version: 1.0
model: claude-sonnet-4-5
invoked_at: P3.4
---

# ATAM-Lite Evaluation Agent

## Role
You are an architecture evaluator applying a lightweight ATAM-style analysis.
Your job is to evaluate the designed architecture against QA scenarios, identifying
risks, tradeoff points, and sensitivity points. You produce findings, not verdicts.

## Inputs (read these files, nothing else)
- state/arch/arch-pass-NNN.md
- state/arch/NNN-qa-scenarios.md
- docs/architecture/containers.md      (if exists — for comparison baseline)
- docs/architecture/risks.md           (if exists — check against existing risks)

## Output
- state/arch/NNN-atam-lite.md

## Process

### Step 1: Build Utility Tree
Create a two-level hierarchy:
- Level 1: QA characteristics (from QA scenarios)
- Level 2: Scenarios (leaves)
For each leaf: (Importance to system success, Difficulty to achieve) rated H/M/L.

### Step 2: Evaluate each scenario against the architecture
For each QA scenario from NNN-qa-scenarios.md:
- Quote the relevant architectural decision(s) that address it
- Assess: SATISFIED / PARTIALLY / NOT_ADDRESSED
- Identify whether this is a Sensitivity Point (small change → big QA impact)
  or a Tradeoff Point (this decision improves one QA but hurts another)

### Step 3: Risk identification
For each design decision that is either:
- NOT_ADDRESSED for a HIGH-importance scenario
- A Tradeoff Point where a HIGH-importance QA is the loser
Flag as RISK with probability (H/M/L) and impact (H/M/L).

### Step 4: Produce findings
List all risks with remediation options (do not make decisions).
List all tradeoff points with QA consequences documented.
List non-risks (decisions that clearly satisfy QAs with no identified risk).

## Hard Constraints
- Never propose architectural solutions — only evaluate the existing architecture
- Every risk must reference a specific QA scenario and a specific arch-pass decision
- Do not create ADRs or modify any architecture documents
- Do not load src/, tests/, state/tasks/
- If arch-pass-NNN.md does not exist or has status DRAFT: halt with "Architecture pass required"
```

***
## How the Extended P3 Fits the Full Workflow
### Updated P3 sequence in the pre-workflow
```
P3.0  Domain Modeling     [agent, SKIP if mode=LITE/STANDARD]
      ↓
P3.1  Constraint Check    [agent → CLEAR or CONFLICTS_FOUND]
      ↓ (human resolves conflicts if any)
P3.2  QA Elicitation      [agent → 5-8 QA scenarios]
      ↓ (human reviews: 5-10 min, adjusts priorities)
P3.3  Architecture Design [agent, ADD 3.0, 1-2 iterations]
      ↓
P3.4  ATAM-Lite Eval      [agent → risks, tradeoffs, sensitivity points]
      ↓ (human reviews risk register: 10-15 min)
P3.5  ADR Authoring       [HUMAN GATE 🛑 — authors ADRs for flagged decisions]
      ↓
P3.6  Arch Doc Update     [agent → updates context.md, containers.md, runtime.md,
                            deployment.md, crosscutting.md, quality.md]
```

**Total P3 time estimate**:
- Mode FULL (new product/epic): 60–90 min agent time, 30–45 min human time
- Mode BOOTSTRAP (new product, no prior architecture): 90–120 min agent time, 60–75 min human time
- Mode LITE/STANDARD: P3 skipped (Constraint Check only, P3.1)
### What S2 (nowu-constraints) receives now
S2 previously received `arch-pass-NNN.md` as an optional enrichment. With the extended P3, it receives a **much richer starting point**:

| Input | Before v3 P3 | After v3 P3 |
|---|---|---|
| Module boundaries | Rough C4 L2 sketch | C4 L2 + responsibility table + domain-derived boundaries |
| Quality constraints | None | 5–8 formal QA scenarios with measures |
| Pattern decisions | ADR candidates | ADRs already authored, binding |
| Runtime contracts | None | C4 Dynamic for key flows → explicit interface expectations |
| Crosscutting decisions | None | `crosscutting.md` — logging, auth, error handling decided |
| Risk register | None | `NNN-atam-lite.md` — risks S2 must watch for |

S2's job shifts from "discover constraints" to "verify and refine the pre-designed constraints." This is the correct division: pre-workflow does strategic architecture, S2–S4 do tactical design.
### Where the architecture is consumed by S1–S9
| S step | What it reads from architecture | Purpose |
|---|---|---|
| S1 (Intake) | `docs/vision.md`, `docs/V1_PLAN.md` | Confirm problem alignment, not architecture |
| S2 (Constraints) | `docs/architecture/containers.md`, `docs/DECISIONS.md`, `arch-pass-NNN.md`, `crosscutting.md` | Identify affected modules, enforce QA constraints |
| S3 (Options) | `docs/architecture/containers.md`, `NNN-constraints.md` | Generate options within architectural invariants |
| S4 (Decision) | `docs/DECISIONS.md` | Record decisions linked to ADRs and QA scenarios |
| S5 (Shaping) | `decision-handoff.md`, file tree, contracts | Break into tasks; `crosscutting.md` constrains every task's scope |
| S6/S7 (Implement) | Task spec + `inscopefiles` ONLY | `crosscutting.md` approach applied but docs not loaded |
| S8 (Review) | `.claude/rules/architecture.md`, story files | Verify QA constraints not violated |
| S9 (Capture) | `docs/DECISIONS.md`, `docs/PROGRESS.md` | Update risk register if new risks discovered |

***
## Health Checks — What Else to Check
The current three health checks (vision, architecture, goals) cover the high-level alignment. Adding two more completes the picture:

| Check | Existing | Agent | What it examines |
|---|---|---|---|
| `health-check vision` | ✓ | `health-vision` | Freshness, persona match, stage alignment |
| `health-check architecture` | ✓ | `health-architecture` | C4 accuracy vs `src/`, ADR coverage, no implementation drift |
| `health-check goals` | ✓ | `health-goals` | Story-backlog alignment with vision |
| `health-check use-cases` | ✓ (v2.2) | `health-use-cases` | UC-NNN alignment with vision + plan |
| `health-check quality` | **NEW** | `health-quality` | QA scenarios still relevant, not covered by implementation |
| `health-check risks` | **NEW** | `health-risks` | Risk register current, no new risks from recent captures |
| `health-check crosscutting` | **NEW** | `health-crosscutting` | Crosscutting decisions still consistent with recent ADRs |
### `health-check quality` — QA Scenarios Health
Checks:
- All HIGH-priority QA scenarios have at least one ADR addressing them
- No QA scenario is older than 180 days without review (growing products change their QA priorities)
- Recent stories (last 3 captures) have not introduced behaviors that violate existing QA measures
- `quality.md` version matches the `containers.md` last-updated date (prevents stale QA docs)

Status: GREEN (all aligned), YELLOW (some scenarios unaddressed or aging), RED (HIGH-priority scenario with no architectural coverage)
### `health-check risks` — Risk Register Health
Checks:
- OPEN risks in `risks.md` with HIGH probability + HIGH impact: flag as blocking
- Risks marked MITIGATED: verify the mitigating ADR/decision still exists
- Recent captures in `state/capture/`: scan for "unexpected" or "surprised by" language that may signal a new risk not yet recorded
- Count of OPEN risks per product stage: more than 5 OPEN HIGH+HIGH risks at Stage 1 = RED
### `health-check crosscutting` — Crosscutting Concepts Health
Checks:
- Every section in `crosscutting.md` references a valid ADR or an explicit "no ADR needed" marker
- No ADR in `docs/architecture/adr/` contradicts a decision in `crosscutting.md`
- Recent stories do not have architecture signals that imply a different crosscutting approach (e.g., new story uses a different auth pattern without an ADR)
### Expanded `health-check architecture`
The existing check should add:
- `runtime.md` exists if product is at Stage 2+ (Core Loop requires documented runtime behavior)
- `deployment.md` exists if product is at Stage 4+ (Ship requires documented deployment)
- Dynamic diagrams in `runtime.md` correspond to UC-NNN entries in USE_CASES.md

***
## Does the Current Workflow Support Full Product Creation?
### The question: from raw idea `"nowu is an AI-first framework..."` → production product
**Short answer**: yes, the complete P0–P4 + S1–S9 + extended P3 cycle supports this, but with two important caveats:

1. **The Global Architecture Pass (GAP) is the critical first act.** For a product like nowu, the first run must be Bootstrap mode → P0.V (Vision Bootstrap) + P0.D (Idea Decomposition → Stage Map) + full P1–P4 with the extended P3 (domain modeling + QA elicitation + ADD 3.0 + ATAM-lite). This first pass produces the global architecture that all subsequent per-epic P3 passes respect.

2. **Stage progression triggers re-architecture.** The Stage 0→1→2→3→4→5 model already in v2.1 handles this correctly: GAP runs again when stage transitions occur. A feature that was out-of-scope at Stage 1 (e.g., multi-tenancy) becomes an architectural constraint at Stage 3. The health checks surface when re-architecture is needed.
### Product evolution mapping for nowu
| Stage | What changes in the workflow | Key architectural events |
|---|---|---|
| Stage 0 (Concept) | Bootstrap mode: P0.V + P0.D → Stage Map | First GAP: C4 L1/L2, QA registry, domain model, crosscutting.md |
| Stage 1 (Foundation) | First 2–4 epics via Full mode P0–P4 | P3 adds Dynamic views for core flows, ADRs for persistence + API patterns |
| Stage 2 (Core Loop) | Standard mode for known epics; Full for new capabilities | GAP Stage 1→2: re-examine module boundaries, add runtime.md |
| Stage 3 (Hardening) | S1–S9 only (architecture stable); health checks drive | QA scenarios get acceptance tests; risks.md closes open items |
| Stage 4 (Ship) | ADRs for deployment, observability, SLOs | deployment.md finalized; crosscutting.md locked |
| Stage 5 (Growth) | New discovery runs; PRODUCT_PIVOT triggers GAP | QA scenarios re-evaluated against user feedback |

***
## Changes to S1–S9 Recommended by This Analysis
### S2 (nowu-constraints) — load two new files
Add to `S2 Load`:
- `docs/architecture/crosscutting.md` — constraints on every task's implementation approach
- `state/arch/NNN-atam-lite.md` — risks to watch during constraint analysis

Add to `S2 Produces`:
- Explicit "QA Scenario Coverage" section in `constraints-sheet.md`: for each QA scenario from `NNN-qa-scenarios.md`, note whether this story's implementation will affect it and how
### S4 (nowu-decider) — link decisions to QA scenarios
Add to `decision.md` template:
```markdown
## QA Scenario Impact
| QA-ID | Scenario | Impact of this decision | Direction |
|---|---|---|---|
```
### S8 (nowu-reviewer) — check crosscutting compliance
Add to S8 verification checklist:
- Does the implementation follow the logging approach in `crosscutting.md`?
- Does the implementation follow the auth pattern in `crosscutting.md`?
- Does the implementation follow the error handling pattern in `crosscutting.md`?

If `crosscutting.md` does not exist for the project: flag as YELLOW, create ticket to produce it.
### S9 (nowu-curator) — update risk register
Add to S9 actions:
- Scan the review report for language indicating architectural surprise
- If found: append to `docs/architecture/risks.md` as a new OPEN risk with evidence
- If a known risk was triggered and mitigated: update status to MITIGATED

***
## Summary: State-of-the-Art Assessment
The nowu pre-workflow + S1–S9 pipeline, with the extended P3 described in this report, represents a **production-grade, research-validated architecture workflow** for a solo developer. The key claim:

> LLM-assisted ADD 3.0 with a structured architect persona produces architectures "closely aligned with proven solutions and partially satisfying architectural drivers" — and this validation was done specifically for the LLM-guided, human-in-the-loop, structured-process approach.[^3][^4]

The addition of:
- **Mini-QAW** (P3.2) as the driver-gathering step[^8]
- **ADD 3.0** (P3.3) as the design method[^10][^4]
- **ATAM-lite** (P3.4) as the evaluation step[^9][^26]
- **arc42 §6/§7/§8/§10/§11** as the documentation structure[^5][^14]
- **ISO 25010** as the QA taxonomy[^16][^18][^17]

...elevates the architecture phase from "useful sketch" to "systematically designed and evaluated architecture that satisfies stated quality requirements." That is state of the art for a solo developer context.

---

## References

1. [Evaluation-Driven Development of LLM Agents: A Process Model and
  Reference Architecture](http://arxiv.org/pdf/2411.13768.pdf) - ...offline
(redevelopment) evaluations, enabling adaptive runtime adjustments and
systematic iterati...

2. [MASAI: Modular Architecture for Software-engineering AI Agents](http://arxiv.org/pdf/2406.11638v1.pdf) - ...problems. Inspired by this, we propose a
Modular Architecture for Software-engineering AI (MASAI)...

3. [An LLM-assisted approach to designing software architectures using ADD](https://arxiv.org/abs/2506.22688) - Designing effective software architectures is a complex, iterative process that traditionally relies...

4. [[PDF] An LLM-assisted approach to designing software architectures using ...](https://arxiv.org/pdf/2506.22688.pdf) - This paper proposes an approach for Large Language Model (LLM)-assisted software architecture design...

5. [arc42 Template Overview](https://arc42.org/overview) - arc42 is a template for architecture communication and documentation.

6. [1 - Introduction and Goals - arc42 Documentation](https://docs.arc42.org/section-1/) - Describes the relevant requirements and the driving forces that software architects and development ...

7. [Continuous and Proactive Software Architecture Evaluation: An IoT Case](http://pure-oai.bham.ac.uk/ws/files/151337313/sobhy2021contin.pdf) - Design-time evaluation is essential to build the initial software architecture to be deployed. Howev...

8. [Integrating the Quality Attribute Workshop (QAW) and the Attribute-Driven Design (ADD) Method](http://www.dtic.mil/docs/citations/ADA443486) - Abstract : The Software Architecture Technology Initiative at the Carnegie Mellon Software Engineeri...

9. [[PDF] Architecture Trade-off Analysis Method ATAM - CMS](https://cms.sic.saarland/atis_19/dl/14/Lecture_12.pdf) - How does ATAM work? 1. Bring stakeholders together. 2. Explain ATAM. 3. Summarize business driver/co...

10. [Attribute-Driven Design – Creating Architecture | Ch 20 - YouTube](https://www.youtube.com/watch?v=-wS5TU_Imbc) - the Attribute-Driven Design (ADD) method, which is discussed in detail ... Attribute-Driven Design –...

11. [[PDF] Architecture Tradeoff Analysis Method (ATAM)](https://www.sei.cmu.edu/library/file_redirect/2011_015_001_28266.pdf/) - The SEI Architecture Tradeoff Analysis. Method (ATAM) is the leading method in the area of software ...

12. [Dynamic diagram | C4 model](https://c4model.com/diagrams/dynamic) - A dynamic diagram can be useful when you want to show how elements in the static model collaborate a...

13. [Deployment diagram - C4 model](https://c4model.com/diagrams/deployment) - A deployment diagram allows you to illustrate how instances of software systems and/or containers in...

14. [5 - Building block view - arc42 Documentation](https://docs.arc42.org/section-5/) - The building block view shows the static decomposition of the system into building blocks (modules, ...

15. [Attribute Driven Design (ADD) Method | Software Architecture | Lec 44](https://www.youtube.com/watch?v=5w1UenRzM-w) - Attribute Driven Design (ADD) Method | Software Architecture | Lec 44 Join telegram https://t.me/jis...

16. [ISO/IEC 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) - The product quality model defined in ISO/IEC 25010 comprises the nine quality characteristics shown ...

17. [ISO/IEC 25010 - Systems and Software Quality](https://quality.arc42.org/standards/iso-25010) - ISO/IEC 25010: Systems and software Quality Requirements and Evaluation (SQuaRE). It defines a produ...

18. [Software Quality Attributes: ISO 25010 Quality Model | Lead With Skills](https://www.leadwithskills.com/blogs/software-quality-attributes-iso-25010-quality-model) - Software Quality Attributes: ISO 25010 Quality Model. Published on December 15, 2025 | 10-12 min rea...

19. [ISO 25010: Enhancing Our Software Quality Management Process](https://helpware.com/blog/tech/iso-25010-enhancing-our-software-quality-management-process) - ISO/IEC 25010 is a quality model determining which quality characteristics to consider when evaluati...

20. [Ultimate Guide to Non-Functional Requirements for Architects](https://www.workingsoftware.dev/the-ultimate-guide-to-write-non-functional-requirements/) - Here's a brief summary of the ISO/IEC 25010:2023 quality characteristics: Functional suitability: Me...

21. [Practical Steps, Templates, and Examples with ADRs, ATAM & ISO ...](https://www.linkedin.com/pulse/architecting-quality-software-systems-practical-steps-alejandro-jose-y9vbe) - Run a workshop with stakeholders to prioritize these attributes. Translate each priority into concre...

22. [[PDF] Architecture Tradeoff Analysis MethodSM (ATAMSM)](https://www.ifi.uzh.ch/dam/jcr:ffffffff-fd5f-cdf8-ffff-ffffde53807c/swa-04-ATAM.pdf) - The purpose of ATAM is: to assess the consequences of architectural decision alternatives in light o...

23. [C4 model: Home](https://c4model.com) - The C4 model is an easy to learn, developer friendly approach to software architecture diagramming: ...

24. [C4 Diagram | Mermaid Viewer Docs](https://docs.mermaidviewer.com/diagrams/c4) - C4 diagrams provide a way to visualize software architecture at different levels of abstraction. The...

25. [C4 Diagrams | Mermaid](https://mermaid.js.org/syntax/c4.html) - Proper documentation will be provided when the syntax is stable. Mermaid's C4 diagram syntax is comp...

26. [Architecture tradeoff analysis method - Wikipedia](https://en.wikipedia.org/wiki/Architecture_tradeoff_analysis_method) - Its purpose is to help choose a suitable architecture for a software system by discovering trade-off...

27. [How to use Event Storming to introduce Domain Driven Design](https://philippe.bourgau.net/how-to-use-event-storming-to-introduce-domain-driven-design/) - Event Storming is a collaborative design workshop. Using a big wall and post-its, a group of people ...

28. [EventStorming meets Domain-Driven Design with Alberto Brandolini](https://www.codecentric.de/en/knowledge-hub/blog/eventstorming-meets-domain-driven-design-with-alberto-brandolini) - The Big Picture EventStorming helps to identify Bounded Contexts together with the dev team: Units o...

29. [The Best way of implementing Domain-driven design, Clean ...](https://blog.devgenius.io/best-way-of-implementing-domain-driven-design-clean-architecture-and-cqrs-44d422b09882) - I am going to show you the best way learning Domain-Driven Design, Clean Architecture, CQRS, and Sof...

