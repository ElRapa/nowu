---
id: disc-v1core
source: vision.md v2.0 + USE_CASES.md v2.2
created: 2026-04-07
status: ACCEPTED
---

# Discovery Research: nowu v1-core

---

## 1. Problem Space Summary

The gap between individual AI sessions and sustained productive output is not a capability problem — it is a continuity problem. Current AI tools are excellent within a session but leave nothing durable behind: no memory of what was decided, no understanding of why, no thread to pick up from. Each new session starts from approximation, relying on the human to reconstruct context they may have only partially retained. The bottleneck has shifted from "can AI do this?" to "can AI keep working toward what I actually want across many sessions, many projects, and many interruptions?"

For the multi-project human specifically, this problem compounds. Running several concurrent projects means context-switching is not occasional — it is the normal mode of operation. Returning to a project after days or weeks requires a re-orientation effort that is itself a significant tax on progress. The "low-grade guilt of stalled projects" described in the vision is not a productivity failure; it is a structural consequence of re-orientation cost being too high to pay repeatedly. Projects stall not because work isn't happening but because the cost of resuming productive work exceeds the available time and energy.

There is a second, less visible layer to the problem: decision memory. When significant decisions are made — architectural, strategic, business — the choice itself is sometimes recorded, but the reasoning, the alternatives considered, and the context at the time almost never are. Months later, the human revisits the decision without knowing why it was made, repeats the analysis, and either arrives at the same conclusion (wasted effort) or a different one (drift). The absence of traceable reasoning means that the value of past thinking is almost fully lost.

A third layer: knowledge that accumulates across domains and projects does not connect. The coconut plantation that feeds the aperitif supply chain and the real-estate project containing it live in separate mental compartments. The lesson learned debugging workflow scoping in a software project might apply directly to a business milestone planning exercise — but the connection is never made unless the human happens to remember it. Individual knowledge does not compound into shared understanding without a layer that actively maintains those relationships.

---

## 2. Primary Persona — Validated Pain Points

**Raphael — the multi-project human** runs several concurrent endeavours across different domains (framework development, food business, real-estate operation, creative work) and uses AI heavily for all of them. He is not always at his desk when relevant moments occur — ideas surface on commutes, observations arise at supplier meetings, decision triggers emerge mid-conversation. The system must meet him wherever he is.

**Validated pain points, grounded in the UC catalog:**

- **Re-orientation overhead dominates return visits.** Every time Raphael returns to a project after any gap, he spends significant time reconstructing context: what was he doing, what did he decide, what's next. This overhead is often enough to defer the session entirely. (NF-01, NF-10)

- **Decision rationale disappears within weeks.** Raphael can find that a decision was made but rarely why, what was rejected, or what the conditions were at the time. Six months later he either repeats the analysis or treats past decisions as arbitrary. (NF-02, NF-13, AP-06, RE-06)

- **Capture friction exceeds the value of many ideas.** When a thought arrives away from a structured environment, the effort of routing it into the right project, the right format, with the right context is enough to kill it. Valuable capture moments are systematically lost because the system requires more structure than the moment permits. (PK-01, PK-08)

- **Multi-project life means no unified view of what matters today.** Raphael checks multiple systems — project boards, notes, calendar, messages — to assemble a picture of priorities that he then holds only in his head. Important items from one project are eclipsed by urgent-but-low-importance items from another. (PK-03)

- **Knowledge does not connect across project walls.** Observations and facts captured in one project context are invisible when working in another. Cross-project connections exist but are never surfaced — the human must remember them or miss them. (XP-01, PK-02)

- **Running multiple domains means perpetual expertise gaps.** Raphael is capable in software; in food regulation, supply chain management, real-estate valuation, and creative production he operates with significantly less domain depth. Decisions in those domains require expert judgment he does not personally hold. Currently the workaround is ad-hoc research, relying on advisors, or avoidance — none of which integrate the knowledge into a durable, reusable form that compounds across sessions. AI research and synthesis is the viable bridge, but only if what is learned is retained and connected rather than discarded when the session ends. (PK-05, PK-09)

- **Scope discipline collapses without active enforcement.** When working with AI agents, tasks that should be bounded frequently expand. Without a mechanism to actively hold the boundary, what was scoped as a focused change becomes an unplanned refactor. (NF-03)

- **The same framework does not naturally extend to non-software work.** Process documentation, regulatory tracking, business decision analysis, and supply chain reasoning all need structured memory but have no equivalent of an existing software workflow. The human manages these domains in ad-hoc notes, spreadsheets, and memory — outside any system. (NF-07, AP-01, AP-02, RE-01)

---

## 3. Opportunity Themes

### Theme 1 — The Continuity Gap

**What the user is missing:** A reliable mechanism to return to any project — after any duration of absence — and know immediately where things stand, what was decided, and what comes next. Not a transcript, not a commit log, but an active orientation that feels like picking up where you left off.

**What failure looks like:** Every project return demands a 15–30 minute archaeological dig. The guilt of starting that dig accumulates into avoidance. Projects that are genuinely important stall not from lack of intent but from the compounding cost of re-entry.

**What would change if solved:** The re-orientation cost approaches zero. The human spends the recovered time doing the work rather than reconstructing the context for the work. Projects do not stall between sessions; they resume. The experience of "progress compounds" becomes observable, not aspirational.

---

### Theme 2 — Decision Memory and Traceable Reasoning

**What the user is missing:** A durable record of not just what was decided, but why — what alternatives were rejected, what was known at the time, what assumptions were made, and what would need to change to revisit the decision. This applies equally to architectural choices in software, strategic choices in a food business, and investment decisions in real estate.

**What failure looks like:** Past reasoning is invisible. The human either repeats the same analysis from scratch (wasted) or makes a new decision that contradicts an old one without realising it (drift). Decisions made confidently today become arbitrary-seeming obstacles six months later.

**What would change if solved:** Every significant decision carries its reasoning forward in time. Future sessions — human or AI-assisted — can evaluate a decision in its original context. Contradictions surface before they become embedded. The compounding of good judgment becomes possible because past judgment is not lost.

---

### Theme 3 — Frictionless Capture Across All Contexts

**What the user is missing:** A way to record a thought, observation, or decision trigger in the moment it occurs — regardless of device, location, or available structure — at a friction cost low enough that the capture actually happens. Enrichment, categorisation, and linking can happen later; the moment of capture must be near-instant.

**What failure looks like:** Capture requires the right device, the right app, and the right level of categorisation before the moment passes. Thoughts that would have been valuable are systematically lost. Or they are captured in a medium (paper, voice message, text thread) that exists outside every system, orphaned.

**What would change if solved:** The capture moment decouples from the organisation moment. Valuable observations enter the system regardless of context. The human trusts that what they capture will be found and connected — so they capture more freely, and the knowledge base grows from real experience rather than only from deliberate documentation.

---

### Theme 4 — Knowledge That Compounds Across Projects

**What the user is missing:** A layer that actively connects what is known across projects. The human's coconut plantation, their aperitif business, and their knowledge of the Bicol supply chain should be able to inform each other. A lesson learned in one domain should surface as a recommendation in another. A fact captured in one context should be discoverable when it becomes relevant elsewhere.

**What failure looks like:** Projects exist in separate silos. The human is the only connection layer — relying on their own memory to transfer knowledge between domains. Obvious connections are missed. The same mistakes are made independently in each project. The knowledge base grows but does not deepen.

**What would change if solved:** Cross-project knowledge becomes an active resource rather than a passive archive. The benefit of running multiple projects increases because each one enriches the others. The "12-month shared, queryable knowledge base" horizon becomes a real experience rather than a technical feature.

---

### Theme 5 — A Unified Daily Orientation

**What the user is missing:** A single view — across all projects and domains — that gives the human a clear signal of what actually matters today, calibrated by importance and urgency rather than by recency or source. Not a list of everything; a curated surface of what to focus on.

**What failure looks like:** The human assembles their daily orientation manually from multiple disconnected systems. Low-importance urgent items crowd out high-importance tasks. The "right" thing to work on is rarely what gets worked on because the selection mechanism is random (whatever was opened last) rather than intentional.

**What would change if solved:** The start of each day requires one view, not four. The human's attention is directed to what actually moves their most important projects forward. The experience of "steady, meaningful progress without keeping everything in your head" becomes achievable.

---

### Theme 6 — A Framework That Works for Non-Software Work

**What the user is missing:** The same continuity, decision memory, and knowledge compounding that nowu provides for software development applied equally to business operation, real-estate management, and any other domain. These domains have structured knowledge needs — regulatory requirements, product formulation, supply chain relationships, investment theses — but no existing workflow that treats them with the same rigor.

**What failure looks like:** The aperitif business is managed in notes, spreadsheets, and memory. Regulatoryrequirements are scattered across bookmarks. Formulation history is lost when a phone breaks. Business decisions are made in conversations and forgotten by the next meeting. The value of the nowu framework is available only in the one domain (software) where the human already has the most tooling.

**What would change if solved:** A regulatory requirement carries the same traceability as an architectural decision. A supply chain relationship has the same durability as a software decision record. The framework serves every domain equally — so the human's full range of work benefits, not just the most technical part.

---

### Theme 7 — AI as Expertise Bridge

**What the user is missing:** Access to trustworthy domain expertise across the breadth of domains they are running. The multi-project human is, by definition, not deeply expert in most of their domains. They need specialist-level judgment — regulatory, technical, operational, commercial — in order to make sound decisions in each project. Currently that judgment arrives ad-hoc through research, advisors, or trial and error, and none of it is retained in a form that compounds. When a similar question recurs three months later, the research starts again.

**What failure looks like:** Regulatory requirements are looked up fresh every time a question arises. Technical specifications from a supplier are evaluated without context from industry norms. Business decisions are made under-informed — not from irresponsibility but from the structural impossibility of being deeply expert in six domains simultaneously. Expert knowledge acquired in preparation for one decision disappears immediately after it, unavailable to any future decision that touches the same domain.

**What would change if solved:** Expert-level guidance becomes available on demand, contextualised to the specific project and decision. Research conducted for one decision is retained as a knowledge atom and becomes available for future related decisions — with graded confidence and timestamped source provenance. The human's effective competence depth in each domain grows over time, not because they personally study more, but because the system accumulates what has already been learned and keeps it current. Domain expertise stops being a one-time cost and starts compounding like every other form of project knowledge.

---

## 4. Key Tensions in the Problem Space

### Tension A — Breadth of Capture vs. Depth of Utility

The problem demands frictionless capture (Theme 3) — but low-friction capture tends to produce raw, unstructured input that requires significant enrichment to be useful. The more structure is required at capture time, the less frequently capture happens; the less structure is captured, the more ambiguous the enrichment task becomes later. There is no frictionless capture that is also immediately connected and well-attributed. The system must assume capture and enrichment are separate moments, while ensuring that the gap between them does not create a backlog that itself becomes a burden.

### Tension B — Automation vs. Human Direction

The user explicitly does not want to manage a system — they want a system that manages itself well enough that they can just show up and move forward. But the same user needs the AI to remain aligned with what they actually want, not what it infers they want from prior sessions. Too much automation risks AI confident divergence (drift that goes unnoticed); too little automation reintroduces the exact overhead the framework is meant to eliminate. The boundary for human intervention must be placed precisely: high-stakes decisions require human direction; execution-level work should not.

### Tension C — Premature Structure vs. No Structure

The vision explicitly protects the early fuzzy phase: "a vague start is expected and fine." But the same framework eventually needs structured artifacts to support continuity, traceability, and compounding. The tension is not between structure and no structure — it is about when structure is introduced and at what cost. Forcing an idea into a use case at the moment of its capture kills ideas; never structuring it means the idea never becomes actionable. The framework must allow ideas to live at low structure until they are ready, without abandoning them.

### Tension D — Personal System vs. Collaborative Surface

The problem is deeply personal: Raphael's multi-project life, his reasoning trails, his captured thoughts, his business decisions. But the 12–24 month vision horizons explicitly describe collaboration — a colleague picking up a project, a business partner reading a briefing, a collaborator joining the aperitif project. What is optimised for personal, trusted, fast access may be poorly suited to selective sharing with appropriate visibility controls. A system built for one introspective user is not automatically a collaboration layer; the transition requires resolving who sees what without losing the personal experience that makes the system valuable in the first place.

---

## 5. Success Horizons

*Close paraphrase from vision.md v2.0*

**6 Months — The workflow is yours**
nowu runs its own development using itself. The AI carries the full cycle — discovery, architecture, implementation, and capture — with 90–99% of the work handled by AI, and a human can start from a vague idea and get meaningful output without the process feeling like overhead. The experience is genuinely enjoyable — low friction, clear feedback, visible progress. At least two real projects outside software are active and growing, and the human trusts what nowu knows about each project because they have seen it hold the thread through real interruptions.

**12 Months — Knowledge compounds across projects**
At least six projects are active across different domains, including both software and non-software work. They do not interfere with each other; knowledge accumulates within each project and starts to connect usefully across them through a shared, queryable knowledge base. Someone else could pick up any project from the artifacts alone, because the workflow, decisions, and reasoning are durable enough to survive the original builder stepping away. The workflow itself improves with each cycle — the path from vision to shipped becomes faster, more direct, and clearer.

**24 Months — It runs the operation**
nowu is infrastructure, not just a tool. Every project, decision, and capture flows through it — a company operating system by practice, not just by claim. It is stable enough to ship as a framework, installable product, or service that other people adopt, with collaboration and data governance built in as natural parts of how the system works. nowu is a full collaboration layer for humans and AI, and a knowledge layer accessible in the best ways for both.

---

## 6. Flagged Assumptions

**Assumption 1 — Low-friction capture will actually happen at the required frequency**
The vision and UC catalog assume that enabling capture from any interface (phone, voice, text) is sufficient to make capture habitual. But the existence of a low-friction path does not guarantee the habit forms. The user may still default to whatever they are already using (a notes app, a text message to themselves) unless the system provides a compelling reason to capture through nowu specifically. If capture does not happen habitually, the knowledge base grows only from structured sessions — missing exactly the ambient observations and passing thoughts that cross-project connection depends on.
*Why it matters: the entire compounding knowledge thesis depends on capture being reflexive, not deliberate.*

**Assumption 2 — The human will trust AI-held memory over their own**
The framework assumes that Raphael will defer to nowu's record of what was decided, what was captured, and what comes next — rather than reconstructing from his own memory or treating the system as advisory. This trust is not automatic; it must be earned through consistent accuracy over time. If the system produces even a few visible errors in memory retrieval (wrong decision retrieved, incorrect attribution, stale fact surfaced as current), the human will stop trusting it and revert to conventional methods — at which point the continuity benefit evaporates.
*Why it matters: the 6-month success criterion "you trust what nowu knows" is the central proposition, not a side effect.*

**Assumption 3 — Non-software domains will benefit as much as software from the same framework**
The UC catalog extends the nowu framework to food business (AP) and real estate (RE) with significant confidence. But these domains have fundamentally different rhythms, knowledge types, and update frequencies from software development. A regulatory permit has a different freshness model than a software ADR. A supplier relationship has different connection semantics than a module dependency. The assumption that the same framework — with minimal domain-specific configuration — is as useful for business process work as for software delivery has not been tested. The AP and RE dogfooding UCs are partly there to test this assumption, which means it should not be treated as confirmed.
*Why it matters: if non-software domains require substantial bespoke investment, the 12-month "six projects" vision horizon is at risk.*

**Assumption 4 — Decision capture will not create enough overhead to be abandoned**
The traceable reasoning theme (NF-02, NF-13, AP-06) requires that decisions be recorded with rationale and alternatives at the time they are made. For deliberate, high-stakes decisions this is natural. For the dozens of small decisions made in a typical working day, the overhead of structured capture may exceed the value perceived in the moment. The system may succeed at capturing the decisions that feel important and miss the ones that turn out to be important — which are often the same decisions made quickly without deliberation.
*Why it matters: if decision capture is selective based on perceived importance, the reasoning trail will have large gaps at the places where informal decisions later prove consequential.*

**Assumption 6 — AI-derived domain expertise will be accurate enough to be acted upon**
The expertise bridge theme assumes that AI research and synthesis will produce domain guidance of sufficient quality that the human can act on it without independent expert verification in most cases. For high-stakes domains — food safety regulation, tax compliance, structural engineering, legal commitments — the cost of an error may require professional verification regardless of AI confidence. If AI-derived expertise fails visibly in a high-stakes context and the human acts on it, both trust in the system and the real-world outcome suffer simultaneously.
*Why it matters: if the human learns they must independently verify AI expertise in each domain anyway, the expertise bridge reduces to a research assistant — useful but not the compounding knowledge asset the vision requires.*

**Assumption 5 — Cross-project connections will be valuable more often than they are distracting**
The vision and XP-01 present cross-project discovery as a clear benefit — the coconut plantation connection is the canonical example. But for every genuinely useful cross-project connection, there may be many surface-level associations that distract from the current focus. A knowledge system that proactively surfaces connections must be accurate enough in its relevance judgement that the signal-to-noise ratio remains high enough to act on. If the human learns to dismiss cross-project suggestions because too many are irrelevant, the mechanism stops being used — and the 12-month "shared, queryable knowledge base" becomes a dormant feature.
*Why it matters: cross-project discovery is one of the clearest differentiators from single-project tools; if it generates noise, it damages trust in the whole system.*
