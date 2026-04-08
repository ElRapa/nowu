---
id: epic-v1core-001
source_problem: problem-001, problem-006
created: 2026-04-08
status: APPROVED
agent_version: story-mapper@2.3 (enriched)
parent_goal: goal-001  # Continuity — thread survives interruptions (TBD: idea-006)
generated_at: 2026-04-08T00:00:00Z
---

# Epic: epic-v1core-001 — Continuity & Capture

## Epic Summary

This epic delivers the foundation that every other epic depends on: the ability to return to any project and immediately know where things stand, resume an active work cycle without loss, and capture observations in the moment they occur. Without reliable persisted context (problem-001) and frictionless entry of new signals (problem-006), every other workflow capability is undermined by re-orientation overhead and knowledge lost at the moment of capture.

This epic is the concrete v1-core probe of Vision Theme “the workflow is yours” and Discovery Theme 1 (Continuity Gap) and Theme 3 (Frictionless Capture) — it is how we make re-orientation cost approach zero and test whether the user will trust what nowu knows about each project more than their own fuzzy recall. It also anchors the “multi-project human” persona in practice: at least one software and one non-software project must be resumable through the same continuity layer, even though non-software domains will be further tested in AP/RE epics.

## Vision & Discovery Alignment

- Vision (6 months): “The AI carries the full cycle… and a human can start from a vague idea and get meaningful output without the process feeling like overhead… you trust what nowu knows about each project because you’ve seen it hold the thread through real interruptions.” This epic implements the “hold the thread” and “resume after interruption” pieces for v1-core, without yet tackling ubiquity of interfaces.  
- Vision (12 months): “At least six projects are active across different domains… they do not interfere with each other… someone else could pick up any project from the artifacts alone.” This epic lays the orientation and capture artifacts that later epics will reuse for collaboration and cross-project knowledge.  
- Discovery Theme 1 (Continuity Gap): Directly addressed by NF-01 + NF-10 slices in this epic.  
- Discovery Theme 3 (Frictionless Capture Across All Contexts): Addressed partially via PK-01 in a single-interface CLI form; multi-interface and async enrichment are explicitly deferred.  
- Discovery Theme 5 (Unified Daily Orientation): Addressed through a minimal PK-03 “Today view” scoped to v1-core.

## Use Case Mapping

| UC-ID | Description | Covered by |
|---|---|---|
| NF-01 | Resume Work After Context Loss | story-v1core-001-s001, story-v1core-001-s002 |
| NF-10 | Maintain the Thread for the Multi-Project Human | story-v1core-001-s001 |
| PK-01 | Capture a Thought Before It's Lost | story-v1core-001-s003 |
| PK-03 | Maintain a “Today” View Across All Projects | story-v1core-001-s004 |
| NF-16 | Detect and Surface Strategic Drift | story-v1core-001-s005 *(v1, deferred)* |

### v1-core Slice Only

For this epic, each UC is deliberately scoped to its v1-core slice:

- NF-01 / NF-10: Single-user, single-machine, CLI-only orientation and resumption, with state in versioned artifacts (e.g., SESSION-STATE, DECISIONS, PROGRESS). No proactive push of orientation; the human must request it.  
- PK-01: Low-friction capture inside the CLI environment only, with minimal required structure at capture time and manual enrichment as an acceptable interim.  
- PK-03: A “Today view” built from existing project artifacts, for a single human user, across multiple projects inside the same installation.
- NF-16: **Deferred to v1.** Strategic drift detection requires goal layer artifacts (idea-006) that do not exist in v1-core. Story-v1core-001-s005 is the founding story and stays DRAFT until goal-NNN.md files exist.

Multi-interface capture, mobile/voice entry, proactive resurfacing of knowledge, and historical analytics are intentionally excluded from v1-core and appear only in higher-stage UCs (PK-02, PK-08, NF-08).

## Story Index

| Story ID | Title | Appetite | Priority |
|---|---|---|---|
| story-v1core-001-s001 | Human Project Orientation on Return | Medium | Must |
| story-v1core-001-s002 | Agent Checkpoint Resumption | Small | Must |
| story-v1core-001-s003 | Frictionless Structured Capture | Small | Must |
| story-v1core-001-s004 | Cross-Project Today View | Small | Must |
| story-v1core-001-s005 | Vision-Aligned Session Orientation | Small | v1 (deferred) |

### Story Success Bounds (v1-core)

- story-v1core-001-s001 (Orientation): Delivers an orientation artifact and flow that lets a returning human understand “what was done, what’s in progress, what’s next, and why” for a single project, on demand, via CLI. It does not include proactive orientation, analytics, or multi-user views.  
- story-v1core-001-s002 (Checkpoint Resumption): Delivers agent resumption from persisted state for a single project, with a clear “last verified checkpoint” and next-action proposal; no multi-agent orchestration or concurrency.  
- story-v1core-001-s003 (Capture): Delivers fast capture commands in the CLI that store thoughts as atomic knowledge items with minimal required metadata; enrichment later is manual, no async enrichment pipeline yet.  
- story-v1core-001-s004 (Today View): Delivers a simple, curated view of what matters today across projects for one human, using existing artifacts; no automated prioritization learning, calendar integration, or notification system.  
- story-v1core-001-s005 (Vision-Aligned Orientation): **v1, deferred.** Adds a drift-detection layer to orientation: open goals with no active epic, unaddressed ideas, uncovered UCs. Blocked by idea-006 (goal layer). Not in v1-core implementation scope.

## Scope Hammer Log

| Dropped Story | Reason |
|---|---|
| Vision-aligned drift detection and goal coverage query | Deferred to v1 as story-v1core-001-s005. Requires goal layer artifacts (idea-006) that do not exist in v1-core. Thread resumption (s001) is the correct v1-core foundation; drift detection extends it once goals are structured artifacts. |
| Multi-interface capture (voice, mobile, remote) | PK-08 (“Interact with nowu from Any Interface”) is explicitly v1 scope — the CLI foundation must exist and prove stable before remote access is meaningful. Attempting both in v1-core inflates the epic beyond appetite. |
| Async enrichment of captured signals | v1.1 scope per problem-006 and PK-01/PK-04 trajectory. Capture and enrichment must decouple; forcing async evaluation into v1-core introduces infrastructure risk with no immediate user-visible benefit given manual enrichment is an acceptable interim. |
| Proactive knowledge surfacing without prompting | PK-02 (“Surface Relevant Knowledge Without Being Asked”) is v1.1 scope. The human must request orientation in v1-core; the system pushes information in v1.1 once signal quality is calibrated. |
| Historical session analytics and trend data | problem-001 explicitly excludes this. Orientation is about the current thread, not retrospective analytics, which belong with NF-08 in v1.1. |

### Out-of-Scope for v1-core (for this Epic)

- No mobile, voice, or remote capture interfaces (PK-08: v1).  
- No proactive surfacing of orientation or recommendations (PK-02: v1.1).  
- No health dashboards or historical trend analytics (NF-08: v1.1).  
- No cross-user collaboration surfaces; all artifacts are optimized for a single human plus agents.  
- No automatic behavioral changes in agents based on trends; learning loops live in later epics.

## Assumption Probes & Tensions

This epic is explicitly testing:

- Assumption 1 (Capture habit): Does having low-friction CLI capture actually change behavior, or does the user still default to other tools? Evidence: volume and recency of PK-01 capture events per week vs. baseline habits.  
- Assumption 2 (Trust in AI-held memory): Does the human defer to orientation artifacts instead of reconstructing from memory? Evidence: how often the human accepts vs. overrides/respecifies the orientation in the first N resumptions.  
- Assumption 3 (Non-software fitness) indirectly, by requiring at least one non-software project to be oriented and resumed through the same mechanism.  

Key tensions monitored:

- Tension A (Breadth of Capture vs. Depth of Utility): We intentionally bias toward breadth of capture with minimal required metadata. We will watch for backlog of un-enriched captures becoming a burden; if it does, the epic has over-tilted toward breadth.  
- Tension B (Automation vs. Human Direction): Orientation and capture flows deliberately require explicit human actions (ask for orientation, invoke capture). If these feel like overhead instead of “just enough structure,” we are on the wrong side of the tension.

## Epic Appetite

Total: 1 Medium + 3 Small (v1-core) — fits within 2 implementation cycles (foundation cycle for resumption + capture cycle for orientation view). Story s005 is v1 scope and excluded from v1-core implementation.