<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Here is a better overview of my desired workflow and the global-model. Does it change anything about the outcome of your previous report?

# GLOBAL-MODEL — Altitude × Phase Workflow Model

> Version: 2.0 | Updated: 2026-04-08
> Supersedes: C4-centric model (v1.x)

---

## 1. Core Model

nowu treats work as a **2D matrix**, not a pipeline. Every artifact sits at the
intersection of:

- an **altitude** — what level of abstraction it addresses, and
- a **phase** — what kind of work is being done at that level.

This matters for agents: an agent must know not only *what to do* but *at what altitude*.
Without explicit altitude, agents fall downhill — starting from a strategic pain and
immediately emitting features, commands, or implementation details.

---

## 2. Five Altitudes

| Altitude | What it addresses | Permitted language |
| :-- | :-- | :-- |
| **STRATEGIC** | Vision, portfolio direction, product thesis | Goals, personas, bets, horizons |
| **PRODUCT** | Validated user/domain problems, outcome shaping | Problems, pain, outcomes, appetite |
| **ARCHITECTURE** | Constraints, quality attributes, structural options, ADRs | Modules, contracts, tradeoffs, risks |
| **DELIVERY** | Epics, intakes, stories, sequencing, shippable slices | Scope, ACs, dependencies, priorities |
| **EXECUTION** | Code, tests, runtime behavior, verification, operational learning | Files, functions, test cases, errors |

**Altitude discipline:** no artifact at one altitude should contain language that belongs
one level lower. A problem statement must not name commands. A story must not name files
unless the schema is already decided. An idea note must not name modules.

---

## 3. Nine Phases

Each altitude runs its own loop through these phases:


| Phase | What happens |
| :-- | :-- |
| **IDEA** | Raw signal, seed, or emerging concern |
| **PROBLEM** | Validated pain, outcome goal, appetite |
| **ANALYSIS** | Research, synthesis, tradeoff exploration |
| **OPTIONS** | Alternative paths, candidate shapes |
| **DECISION** | Chosen path, rationale, rejected alternatives recorded |
| **EVALUATION** | Fitness check — did the decision hold? |
| **IMPLEMENTATION** | Execution of the chosen path |
| **VERIFICATION** | Evidence that the implementation satisfies the decision |
| **LEARN** | Captured lessons; may trigger upward promotion |


---

## 4. The Full Matrix

| Altitude | IDEA | PROBLEM | ANALYSIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **STRATEGIC** | Vision themes, opportunity seeds | Strategic tensions, portfolio pains | Discovery synthesis, trend synthesis | Product directions, horizon options | Vision changes, scope bets | Coherence, viability, strategic fit | Roadmap shaping | Goal review, progress against vision | Vision updates, strategic lessons |
| **PRODUCT** | Initiative seed | Problem statement | Discovery research, persona validation | Outcome shapes, candidate capabilities | Initiative selection, appetite | Problem-solution fit, desirability review | Epic shaping | Outcome validation | Product learning, new assumptions |
| **ARCHITECTURE** | Architectural concern | Constraint / problem statement | QA scenarios, tradeoff analysis | Structural options | ADR / architecture choice | ATAM / risk review | Contract / module changes | Fitness checks, integration tests | Architecture corrections |
| **DELIVERY** | Slice candidate | Delivery obstacle | Readiness, dependency analysis | Sequencing and shaping options | Intake approval, story approval | Scope / risk review | Story execution plan | AC review, completion check | Cycle retrospective |
| **EXECUTION** | Task / code change idea | Bug, defect, mismatch | Root cause analysis | Technical approach options | Local design / code decision | Review / test evaluation | Code and tests | CI, runtime, behavior checks | Capture, postmortem, refactor lesson |


---

## 5. Same Topic Across Altitudes

The same topic appears at multiple altitudes without confusion. Each is a legitimate
artifact at its level — they are not duplicates:

**Example: cross-project knowledge**

- `STRATEGIC/PROBLEM` — vision-level continuity story (projects compound)
- `PRODUCT/PROBLEM` — problem-007 (knowledge invisible across projects)
- `ARCHITECTURE/DECISION` — intake-003, ADR-0004 (per-project SQLite + federation)
- `DELIVERY/IMPLEMENTATION` — future stories (know module integration)
- `EXECUTION/LEARN` — retrospective after first real cross-project use

---

## 6. Artifact → Altitude × Phase Mapping

| Artifact | Altitude | Phase |
| :-- | :-- | :-- |
| `docs/vision.md` | STRATEGIC | PROBLEM / DECISION |
| `docs/USE_CASES.md` | PRODUCT | PROBLEM |
| `state/ideas/idea-NNN.md` | STRATEGIC or PRODUCT | IDEA |
| `state/discovery/disc-NNN.md` | PRODUCT | ANALYSIS |
| `state/problems/problem-NNN.md` | PRODUCT | PROBLEM |
| `state/epics/epic-NNN.md` | DELIVERY | OPTIONS |
| `state/stories/story-NNN-*.md` | DELIVERY | DECISION |
| `state/intake/intake-NNN.md` | DELIVERY | DECISION → IMPLEMENTATION |
| `state/arch/arch-pass-NNN.md` | ARCHITECTURE | OPTIONS |
| `state/arch/NNN-constraint-check.md` | ARCHITECTURE | ANALYSIS |
| `state/arch/NNN-atam-lite.md` | ARCHITECTURE | EVALUATION |
| `docs/architecture/adr/*.md` | ARCHITECTURE | DECISION |
| `state/tasks/task-NNN.md` | EXECUTION | IMPLEMENTATION |
| `state/vbr/vbr-task-NNN.md` | EXECUTION | VERIFICATION |
| `state/capture/capture-task-NNN.md` | EXECUTION → DELIVERY | LEARN |
| `docs/DECISIONS.md` | ARCHITECTURE | DECISION |


---

## 7. Promotion and Upward Movement

Artifacts are promoted across altitudes through explicit gates, not automatic downhill flow.

- **Forward promotion** (normal): PRODUCT/PROBLEM → DELIVERY/OPTIONS → EXECUTION/IMPLEMENTATION
- **Upward promotion** (learning): EXECUTION/LEARN → DELIVERY/LEARN → ARCHITECTURE/LEARN → PRODUCT/LEARN

The `next_cycle_trigger` from S9 (CONTINUE / ARCH_PIVOT / PRODUCT_PIVOT / COMPLETE) is
the mechanism for upward promotion. ARCH_PIVOT forces re-entry at ARCHITECTURE/PROBLEM.
PRODUCT_PIVOT forces re-entry at PRODUCT/ANALYSIS.

---

## 8. Agent Altitude Contracts

Every agent operates at a declared altitude and phase. Agents must not emit language
belonging to a lower altitude.


| Agent role | Altitude | Phase |
| :-- | :-- | :-- |
| Discovery agent | PRODUCT | ANALYSIS |
| Perspective interview | PRODUCT | PROBLEM |
| Story mapper | DELIVERY | OPTIONS |
| Constraint check | ARCHITECTURE | ANALYSIS |
| QA elicitation | ARCHITECTURE | ANALYSIS |
| Architecture design | ARCHITECTURE | OPTIONS |
| ATAM-lite | ARCHITECTURE | EVALUATION |
| Readiness checker | DELIVERY | EVALUATION |
| Intake analyst (S1) | DELIVERY | PROBLEM |
| Constraints analyst (S2) | ARCHITECTURE | ANALYSIS |
| Options designer (S3) | ARCHITECTURE | OPTIONS |
| Decision maker (S4) | ARCHITECTURE | DECISION |
| Task shaper (S5) | DELIVERY | IMPLEMENTATION |
| Implementer (S6–S7) | EXECUTION | IMPLEMENTATION + VERIFICATION |
| Quality agent (S8) | EXECUTION | EVALUATION |
| Curator (S9) | EXECUTION → STRATEGIC | LEARN |


---

## 9. Relationship to C4

C4 (Simon Brown's Context / Container / Component / Code model) remains useful for
communicating software architecture. It maps to nowu altitudes as:


| C4 Level | nowu Altitude | Phase |
| :-- | :-- | :-- |
| Above C4 (vision, problems) | STRATEGIC + PRODUCT | IDEA through DECISION |
| L1 — System Context | ARCHITECTURE | ANALYSIS |
| L2 — Containers / Modules | ARCHITECTURE | OPTIONS + DECISION |
| L3 — Components | DELIVERY + EXECUTION | IMPLEMENTATION |
| L4 — Code | EXECUTION | IMPLEMENTATION + VERIFICATION |

C4 diagrams (`docs/architecture/context.md`, `docs/architecture/containers.md`) live at
ARCHITECTURE/DECISION altitude and are produced by the Global Architecture Pass (GAP)
and refined by P3 Architecture Bootstrap passes per epic.

---

## 10. Code Property Graph (future — via `know`)

A Code Property Graph (CPG) merges AST, CFG, and PDG into one queryable graph.
Operates at EXECUTION altitude; enables deep cross-codebase analysis.

**Today (v1):** AST-based tests enforce import and layering rules.
**Future (v2+):** Store code atoms and edges (`CALLS`, `FLOWS_TO`, `IMPLEMENTS`) in `know`.
Allow queries like `kb.subgraph(from="MODULE:flow", depth=3)` to reconstruct architecture
views without loading raw files.

Good. LangGraph's subgraph support is confirmed and well-documented. Now I have everything I need to give a precise delta analysis. This question is really a "does this change the recommendations?" question — the answer is yes in specific ways, and I should be precise rather than rewriting the whole report.[^1][^2][^3]

The GLOBAL-MODEL changes are significant but **directionally reinforce** most of the prior roadmap while adding three specific corrections. Let me answer directly and concisely — this is a clarification/delta question, not a request for a new full report.

***

Yes, the GLOBAL-MODEL v2.0 changes several things — some significantly. Here is a precise delta of what holds, what strengthens, and what needs to be revised.

## What is unchanged

The **phased strangler-fig strategy** (Option A → Option C → Option B) holds exactly. The GLOBAL-MODEL makes it *more* correct, not less — because the 2D matrix is even more reason not to formalise the orchestration prematurely. A graph that encodes a misunderstood topology is harder to undo than a script.

The **LangGraph for `flow`, LlamaIndex for `know`, PydanticAI for agents** stack is still right — but the *shape* of how LangGraph is used changes substantially (see below).

## What is materially revised

### 1. LangGraph is not a linear pipeline — it is a nested subgraph hierarchy

The previous report mapped S1–S9 as a single linear StateGraph. The GLOBAL-MODEL shows this was wrong. The real topology is:

```
ORCHESTRATOR (Parent Graph)
  ├── [STRATEGIC altitude] — subgraph running IDEAS → LEARN
  ├── [PRODUCT altitude] — subgraph running IDEAS → LEARN
  ├── [ARCHITECTURE altitude] — subgraph running ANALYSIS → EVALUATION
  ├── [DELIVERY altitude] — subgraph running OPTIONS → IMPLEMENTATION
  └── [EXECUTION altitude] — S0→S1→S2→S3→S4→S5→S6→S7→S8→S9 subgraph
         (what the previous report described, but only one of five)
```

LangGraph's subgraph model supports this exactly: each altitude is a compiled subgraph with its own state schema, and subgraphs at the same level share no state by default. The `next_cycle_trigger` values (CONTINUE / ARCH\_PIVOT / PRODUCT\_PIVOT / COMPLETE) from S9 become **cross-altitude routing edges** in the parent graph — the Curator node in EXECUTION emits a signal that the parent orchestrator uses to re-route into ARCHITECTURE/PROBLEM or PRODUCT/ANALYSIS.[^3][^4][^1]

**Implication for v1.1 build:** When migrating the nowu-cli to LangGraph, do not build one flat StateGraph. Build the EXECUTION altitude subgraph first (this is today's S0–S9), then add the DELIVERY altitude subgraph, then wire the parent orchestrator that routes across them. The `next_cycle_trigger` becomes the cross-subgraph routing condition in the parent.

### 2. The `altitude` field is a first-class state attribute on every artifact

The previous report treated altitude as a conceptual design principle. The GLOBAL-MODEL makes it an explicit, enforceable contract: every agent has a declared `(altitude, phase)` pair, and agents must not emit language belonging to a lower altitude. This constraint cannot be enforced by conversation — it must be enforced by the typed artifact schema.

**Implication for PydanticAI:** Every artifact Pydantic model needs an `altitude: Literal["STRATEGIC","PRODUCT","ARCHITECTURE","DELIVERY","EXECUTION"]` and `phase: Literal["IDEA","PROBLEM","ANALYSIS","OPTIONS","DECISION","EVALUATION","IMPLEMENTATION","VERIFICATION","LEARN"]` field. A validator rejects output that contains lower-altitude language. This is a mechanical enforcement of altitude discipline that PydanticAI is precisely suited for  — a validator function that checks, for example, that an `ArchitectureOptionsDoc` contains no file names (EXECUTION language). This is new work not described in the previous report.[^5]

### 3. The `know` module schema is more complex than anticipated

The GLOBAL-MODEL's Section 6 shows artifacts sitting at `(altitude, phase)` intersections. The `KnowledgeAtom` schema must therefore carry both `altitude` and `phase` as indexing dimensions, in addition to `source`, `confidence_grade`, and `relationships`. Cross-project discovery (XP-01) and cross-altitude promotion (upward learning) both require querying atoms by `(altitude, phase)` as filter dimensions, not just by semantic content.

This also means the Code Property Graph (CPG) described in Section 10 is a v2+ feature that lives at `EXECUTION/(VERIFICATION, LEARN)` altitude — it is a specialised knowledge atom type, not a separate system. LlamaIndex can store and query these atoms if the schema is defined correctly.

### 4. The 15 agent altitude-contracts are the right unit of migration

The previous report's strangler-fig migration table listed steps (S1, S2, ... S9) as the migration unit. The GLOBAL-MODEL shows the right unit is `(altitude, phase)` agent contracts — there are 15 of them in the matrix above Section 8. Migration should proceed:

1. First: all EXECUTION altitude agents (the current S0–S9) — these are what you have today
2. Second: DELIVERY altitude agents (intake analyst, task shaper, readiness checker, story mapper) — these are needed for v1 with AP/RE dogfooding
3. Third: ARCHITECTURE altitude agents (constraint check, QA elicitation, options designer, ADR decision maker, ATAM-lite) — needed for v1.1 when ADR enforcement (NF-02) becomes programmatic
4. Fourth: PRODUCT and STRATEGIC altitude agents — needed for v1.2+ when vision drift detection (NF-11) and cross-project learning are automated

### 5. CrewAI is even less appropriate than previously stated

The previous report said "CrewAI hits its ceiling at 6–12 months." The GLOBAL-MODEL makes it a non-starter from day one: CrewAI's crew model has no concept of altitude constraints, no cross-altitude routing, no mechanism for upward promotion via `next_cycle_trigger`, and no subgraph isolation per altitude. The 2D matrix architecture requires a graph runtime that supports hierarchical, nested, independently-stateful subgraphs — which is LangGraph's core design. Do not introduce CrewAI at any point.

## What is strengthened

- **"Artifacts with relevant information at some point"** (your Principle 0 clarification) now maps precisely to the 16 artifact types in Section 6, each sitting at a defined `(altitude, phase)` cell. Every step's conversation can be free-form, but the artifact that exits the step must satisfy the schema for its `(altitude, phase)` position. This is cleaner and more workable than the strict "docs-as-API" interpretation.

```
- **The thin Python CLI (Option C, v1 target)** needs one addition: an `altitude` parameter. `nowu run <project> --altitude EXECUTION --phase IMPLEMENTATION` triggers the S6 implementer. `nowu run <project> --altitude ARCHITECTURE --phase OPTIONS` triggers the architecture options designer. The CLI routing table maps `(altitude, phase)` → correct PydanticAI agent → correct artifact schema.
```

- **The `know` module priority** is confirmed and raised. The matrix's Section 5 example (same topic at 5 different altitudes without confusion) is only achievable if the knowledge atom schema correctly records `(altitude, phase)` at ingestion. This is the hardest design decision in the system and should be done before any LlamaIndex pipeline is built.


## Updated phase summary (delta only)

| Phase | Previous | Revised |
| :-- | :-- | :-- |
| **v1-core (Now)** | Stabilise S1–S9 artifact schemas | Stabilise EXECUTION altitude schemas + define `(altitude, phase)` fields on all artifact types |
| **v1 (Month 4–6)** | nowu-cli `run <project> <step>` | nowu-cli `run <project> --altitude X --phase Y` + DELIVERY altitude agents for AP/RE |
| **v1.1 (Month 7–12)** | LangGraph as flat S0–S9 StateGraph | LangGraph as **nested subgraph hierarchy**: EXECUTION subgraph first, parent orchestrator second, ARCHITECTURE subgraph third |
| **v1.2 (Month 13–18)** | Mature know layer | CPG atoms at EXECUTION/LEARN, PRODUCT/ANALYSIS discovery agents |
| **v2 (Month 19–24)** | Haystack wrapper | Unchanged — Haystack entry point still correct |

## One open question this raises

The GLOBAL-MODEL describes the Curator (S9) as operating at `EXECUTION → STRATEGIC` altitude during the LEARN phase. This upward reach — from code-level lessons to potentially triggering a vision-level reconsideration — is architecturally unusual and important. In LangGraph terms, the S9 node in the EXECUTION subgraph needs to be able to **post a message to the parent orchestrator** with a `next_cycle_trigger` signal, not just update local EXECUTION state. LangGraph supports this via the parent-child state communication model  — but the state key for `next_cycle_trigger` must live in the **parent graph's shared state schema**, not in the EXECUTION subgraph's private state. This is a non-obvious architecture detail worth locking down before the LangGraph migration begins.[^1][^3]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://docs.langchain.com/oss/python/langgraph/use-subgraphs

[^2]: https://pub.aimind.so/built-with-langgraph-23-subgraphs-8b7e08529bbf

[^3]: https://aipractitioner.substack.com/p/scaling-langgraph-agents-parallelization

[^4]: https://forum.langchain.com/t/how-does-state-work-in-langgraph-subgraphs/1755

[^5]: https://realpython.com/pydantic-ai/

[^6]: https://stackoverflow.com/questions/79888246/langgraph-studio-multi-agent-example-hierarchical-agents

[^7]: https://blog.langchain.com/langgraph-multi-agent-workflows/

[^8]: https://docs.langchain.com/oss/python/langgraph/graph-api

[^9]: https://towardsdatascience.com/langgraph-101-lets-build-a-deep-research-agent/

[^10]: https://www.science.org/doi/10.1126/sciadv.adx8006

[^11]: https://forum.langchain.com/t/state-loss-in-hierarchical-multi-agent-system-with-deep-agents-and-custom-agentstate/2592

[^12]: https://www.digitalapplied.com/blog/ai-agent-orchestration-workflows-guide

[^13]: https://www.youtube.com/watch?v=hvAPnpSfSGo

[^14]: https://www.tungstenautomation.de/learn/blog/the-agentic-ai-planning-pattern

[^15]: https://github.com/ombharatiya/ai-system-design-guide/blob/main/09-frameworks-and-tools/02-langgraph-orchestration.md

[^16]: https://arxiv.org/html/2507.14633v1

