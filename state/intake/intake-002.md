---
id: intake-002
created: 2026-04-06
status: READY_FOR_ARCH
appetite: spike
affected_modules:
  - core
  - know
use_case_ids:
  - PK-06
  - XP-11
workflow_mode: D
source_idea: idea-001
s1_note: >
  Mode D (Architecture Only) spike. No implementation expected. Output is a
  binding ADR that locks scoping and data-governance principles before Stage 2
  implementation begins. S2–S4 will proceed; S5–S7 are intentionally skipped.
---

# Intake Brief: Scoping and Data-Governance Principles (Architecture Spike)

## Problem Statement

The knowledge base will eventually hold information of varying sensitivity — public
product notes, internal business strategy, personal financial details, and relationship
observations — across multiple projects and consumers (human, AI agent). No architectural
principle currently governs what a consumer is allowed to see, how that scope is enforced
at the storage/index layer, or how agents should behave when they can detect that knowledge
exists but are not permitted to read it. Stage 1 (Step 02) is building `MemoryService`
right now — the surface where scoping enforcement will need to hook in. If the principles
are deferred, Step 02 will produce a concrete implementation that contradicts or ignores the
governance model and must be partially rewritten in Stage 2–3.

## Context

**Source:** idea-001 — "Scoping is a first-class feature … the index must also follow
these scoping/data-governance principles."

**Why now (not Stage 2):** Stage 1 Step 02 is actively shaping `core/memory_service.py`.
That surface is the natural hook point for future scoping enforcement. Decisions made in
Step 02 (protocol shape, atom retrieval API, index write path) will either accommodate
governance or close the door on it. An ADR produced by this spike becomes a pre-constraint
for Step 02's S2 constraints analysis, preventing retrofitting costs later.

**Relevant use cases:**
- **PK-06** (v1.1): The knowledge base must control what knowledge is accessible in which
  context, prevent sensitive atoms from leaking into generated reports or agent outputs, and
  allow classification without requiring it for every item. Open question from PK-06: how
  should agents handle knowledge they can "see" exists but cannot "read"?
- **XP-11** (v1.1): The same knowledge subgraph must be renderable in role-appropriate
  formats — a human-readable narrative versus a structured, confidence-graded context block
  for an AI agent — without maintaining separate knowledge copies. Scoping must operate
  below this rendering layer, not be a property of the rendered format.

**Stage target:** Both PK-06 and XP-11 are v1.1. The architectural principles decided in
this spike bind every implementation that touches them.

**What this spike does NOT do:** Produce task specs, shape implementation stories, write
code, or specify class names. The output is a single ADR in `docs/architecture/adr/` that
records the accepted scoping and governance model, binding all downstream implementation.

## Appetite

Spike. Timeboxed to analysis and decision. No implementation scope. If the decision space
is larger than one session, produce a decision with `status: PROPOSED` and escalate to
human (Tier 3 — new ADR creation requires human approval before ACCEPTED).

## Open Questions

The following must be answered by S2 (constraints) and resolved in S3–S4 (options and
decision) to produce the ADR:

1. **Granularity of sensitivity classification** — Is sensitivity a property of a knowledge
   atom, a project, a tag, or a combination? Each granularity has different enforcement costs
   and different failure modes. What is the minimum model that satisfies PK-06 without
   making routine capture burdensome?

2. **Default sensitivity level** — Should unclassified atoms be treated as unrestricted
   (opt-in restriction) or as restricted (opt-in access)? The choice determines the failure
   mode: leaking private knowledge vs. blocking useful context from agents.

3. **Agent visibility model** — When an agent executes a query, should it: (a) receive only
   atoms it is permitted to read, with no indication others exist; (b) receive permitted
   atoms plus tombstones indicating redacted atoms; or (c) something else? The PK-06 open
   question ("can see exists but can't read") is the crux here.

4. **Index-layer enforcement** — If the vector/search index is built over all atoms
   regardless of sensitivity, a scoped query can still leak the existence (and embedding
   neighbourhood) of restricted atoms through similarity scores. Must the index itself be
   partitioned by sensitivity, or is post-retrieval filtering sufficient? This is the
   hardest architectural constraint because it affects the `know` module's indexing surface
   directly.

5. **Scope context carrier** — What carries the "who is asking and in what context" signal
   into the `MemoryService` call? Options include: a caller identity token, an explicit
   scope parameter, a session-level context object. The answer must be consistent with the
   `MemoryService` protocol being shaped in Step 02.

6. **XP-11 interaction** — Scoping must operate before role-appropriate rendering, not
   inside it. The ADR must state clearly where in the retrieval pipeline enforcement occurs
   so XP-11 (dual rendering) does not become the de facto enforcement point.

---

```yaml
from_step: S1
to_step: S2
agent: nowu-constraints
status: READY_FOR_ARCH
```
