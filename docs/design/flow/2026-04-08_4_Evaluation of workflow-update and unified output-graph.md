<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# What do you think? Should we adapt the workflow now? Maybe as we migrate to opencode (with the execution altitude) or go ahead with the further implementation of nowu framework?

Also maybe we should think of architecture in different levels/altitudes? Like global vs module vs features? Or even completely ignore the C4 levels and think of all our outputs of all the steps on the different altitudes, as part of a huge (knowledge-) graph like CPG.

Good — I have enough. The LORE paper  is particularly interesting: it describes atomically binding knowledge (commit messages, decisions, rationale) permanently to exact code changes — which directly connects to the CPG-as-universal-graph idea. Now I can answer both questions substantively.[^1]

***

These are two good, separable questions. Here's a direct take on both — no report needed for this one.

## Q1: Should you adapt the workflow now, or continue with nowu implementation?

**Continue with nowu implementation.** Don't adapt the workflow mid-stride for the OpenCode migration.

The reasoning is straightforward and ties back to the previous report's most important principle: **formalise only what you have validated.** Your current v1-core, Step 02 work is building the very artifact schemas that any migration depends on. Pausing to redesign the workflow model now, before those schemas are stable, means you'd be restructuring the scaffolding while the foundation is still wet.

The specific migration question — "should we adapt the workflow as we migrate to OpenCode?" — has a clean answer: **no, but align them.** The GLOBAL-MODEL v2.0 EXECUTION altitude already maps to today's S0–S9 workflow. When you do the OpenCode migration (which is a build-tool swap, not a workflow change), you carry the existing SKILL.md files and agent prompts across largely unchanged. The `--altitude EXECUTION` routing the CLI will eventually need is additive, not disruptive to the current workflow.

**What would actually be worth doing right now** is the one concrete thing the GLOBAL-MODEL revealed that isn't yet in your artifacts: adding `altitude` and `phase` as explicit header fields to every artifact type. That's a small, additive change — a YAML front-matter addition to the artifact schemas — that costs almost nothing now but avoids a painful backfill later. Something like:

```yaml
altitude: EXECUTION
phase: DECISION
step: S4
```

This can be done incrementally alongside Step 02 work, not instead of it.

***

## Q2: Should the ARCHITECTURE altitude be split into global vs. module vs. feature levels? And should we consider everything as one huge heterogeneous knowledge graph, abandoning C4?

These are actually two proposals with different merits. Let me take them separately.

### On splitting the ARCHITECTURE altitude

The instinct is right but the framing of "global vs. module vs. feature" maps too closely to C4's container/component hierarchy, which you're questioning. The more useful split, which the GLOBAL-MODEL already implies, is **structural granularity within the ARCHITECTURE altitude's own phases**, not separate altitudes:

- `ARCHITECTURE/ANALYSIS` at **system scope** = constraint identification, QA elicitation across the whole system
- `ARCHITECTURE/OPTIONS` at **epic scope** = Global Architecture Pass (GAP), per-epic arch passes (P3 bootstrap)
- `ARCHITECTURE/DECISION` at **module scope** = individual ADRs, specific structural contracts

The scope of the artifact varies, but all three belong at ARCHITECTURE altitude — they differ in the breadth of what they reason about, not in the abstraction level. Introducing a new altitude for this would proliferate the matrix without adding clarity. The existing artifact naming already handles this: `arch-pass-001.md` (system-scope) vs. `adr-0004.md` (module-scope) are both ARCHITECTURE/DECISION, just at different radii.

**However**, if the ARCHITECTURE altitude currently feels like it's doing too much work, that's probably because the DELIVERY altitude's `OPTIONS` and `DECISION` phases (epic shaping, intake approval, sequencing) aren't yet distinct enough from architecture decisions. Sharpening the DELIVERY altitude — making "what to build" clearly separate from "how to build it" — would relieve that pressure more than splitting ARCHITECTURE into sub-levels.

### On treating everything as a unified heterogeneous knowledge graph

This is the more interesting and genuinely ambitious idea. The short version: **directionally correct for the long term, premature as a v1 design constraint, but should absolutely shape the `know` schema design starting now.**

Here's what makes it compelling. A recent arXiv paper on using Git commit messages as structured knowledge records ("Lore") describes the same instinct you're pointing at: knowledge permanently fused to the exact artifact it describes, queryable as a graph, not stored in parallel documentation. The vision is that an ADR isn't a separate file that refers to code — it's a node in the same graph as the code module it governs, connected by a `CONSTRAINS` edge. A task-spec isn't a document that describes a story — it's a node connected to the story by `IMPLEMENTS`, to the acceptance criteria by `SATISFIES`, to the use case by `TRACES_TO`.[^1]

The GLOBAL-MODEL's Section 10 already points exactly here: the CPG "merges AST, CFG, and PDG into one queryable graph", and you're proposing extending that same graph model upward through all altitudes. Instead of:[^2][^3]

```
vision.md → USE_CASES.md → epic.md → intake.md → adr.md → task.md → code
(separate files with loose textual references between them)
```

You'd have:

```
vision_node --[SHAPES]--> goal_node --[MOTIVATES]--> problem_node --[ADDRESSED_BY]--> decision_node --[CONSTRAINS]--> module_node --[IMPLEMENTED_BY]--> code_node
```

Every node has `(altitude, phase)` as properties. Every edge has a type. Queries become graph traversals: "what code exists because of this vision bet?" or "what strategic decisions are at risk if I change this module?" This is genuinely more powerful than any document-based system.

**The reason this should shape `know` schema design now** is that retrofitting it is expensive. If you design `KnowledgeAtom` with a `relationships: List[Relationship]` field from the start — where `Relationship` has `edge_type`, `target_id`, `target_altitude`, and `target_phase` — the graph is implicit in the data even before you have graph query infrastructure. You don't need a graph database on day one; you can build the atom store in SQLite/LlamaIndex and traverse relationships programmatically. The graph database (Neo4j, or FalkorDB which is Redis-compatible and faster for this kind of heterogeneous graph) can replace the query layer in v2 without changing the atom schema.

**What C4 becomes in this model:** C4 doesn't disappear — it becomes a **view** over the graph. The L1 context diagram is the subgraph of `ARCHITECTURE/ANALYSIS` nodes with their `COMMUNICATES_WITH` and `DEPENDS_ON` edges. The L2 container diagram is the same subgraph filtered to ARCHITECTURE/OPTIONS scope. C4 is not abandoned; it becomes a rendering lens over a richer underlying structure. This is exactly the "same data, different lenses" language from the vision: "condensed and visual for the human, structured and scoped for the AI agent."

**What's premature:** The graph traversal infrastructure, graph query language design, and graph database adoption are v2 work. Trying to build this in v1-core would consume the entire build budget on infrastructure that the current 5-altitude, 9-phase workflow can't yet feed with enough data to make the graph valuable. The `know` schema foundation is v1-core; the graph query layer is v1.1–v1.2; the CPG extension (code nodes into the same graph as decision nodes) is v2.

### Concrete recommendation

Three things to do now, one for each time horizon:

**Now (v1-core):** Add `altitude`, `phase`, and `relationships: []` to every artifact schema. Even if relationships stay empty for a while, the schema is there. This is the graph in latent form.

**v1.1:** Design the `KnowledgeAtom` node and `Relationship` edge types as the central schema. Choose an initial storage backend (SQLite + LlamaIndex for retrieval). Build the first cross-altitude edge type: `TRACES_TO` linking EXECUTION/task-spec nodes back to DELIVERY/intake nodes and PRODUCT/use-case nodes. This is NF-09 (every deliverable traces to a UC) expressed as graph edges rather than text references.

**v2:** Extend into the CPG direction. `EXECUTION/VERIFICATION` nodes carry `CALLS`, `IMPLEMENTS`, and `FLOWS_TO` edges from the actual code graph. ADR nodes gain `CONSTRAINS_MODULE` edges. The entire system becomes queryable as a heterogeneous graph  — and C4 diagrams are generated from it, not maintained separately.[^4]

The only risk worth flagging: graph schema design is one of the few decisions that is extremely hard to reverse once data accumulates. The node/edge type vocabulary, the `(altitude, phase)` property naming, and the relationship cardinality rules should be decided carefully in v1.1 — ideally with a short spike that actually runs a few dozen real atoms through the schema before committing. Don't over-engineer it upfront, but don't design it casually either. This is the highest-leverage design decision in the entire nowu knowledge layer.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://arxiv.org/pdf/2603.15566.pdf

[^2]: https://jun-zeng.github.io/file/tailor_paper.pdf

[^3]: https://www.usenix.org/system/files/usenixsecurity25-lekssays.pdf

[^4]: https://arxiv.org/html/2402.13746v1

[^5]: https://www.sciencedirect.com/science/article/abs/pii/S0950584920302147

[^6]: https://arxiv.org/abs/2406.02962

[^7]: https://www.icd.uni-stuttgart.de/research/doctoral-research/knowledge-graphs-for-multidisciplinary-co-design-of-buildings/

[^8]: https://aait.od.ua/index.php/journal/article/download/201/183/904

[^9]: https://pubs.acs.org/doi/10.1021/acs.jcim.4c01092

[^10]: https://dbs.uni-leipzig.de/files/research/publications/2024-8/pdf/information-15-00509-with-cover.pdf

[^11]: https://adr.github.io

[^12]: https://wnzhang.net/papers/2022-iconip-hgrkt.pdf

[^13]: https://github.com/joelparkerhenderson/architecture-decision-record

[^14]: https://www.nature.com/articles/s41598-023-33984-5

[^15]: https://www2.informatik.uni-hamburg.de/TGI/events/pnse/pnse17/pnse17_proceedings.pdf

