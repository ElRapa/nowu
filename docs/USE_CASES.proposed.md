---
version: 2.0
generated_by: use-case-agent@2.2
generated_at: 2026-03-31
based_on_vision: v2.0 (approved 2026-03-31)
status: PROPOSED
---

# nowu Framework — Use Cases & Requirements

## Change Summary (v1.1 → v2.0)

**Vision anchor:** First UC catalog refresh against vision v2.0 (approved 2026-03-31).
Key new language from the vision: *compound progress*, *continuity layer*, *multi-project human*,
"six months in, you still trust your own past reasoning."

**Added:**
- NF-10: Maintain the Thread (v1-core) — new UC for the human's multi-project orientation and
  compound progress experience. Not covered by NF-01 (which is agent resumption).

**Promoted (stage advanced):**
- PK-01: Fast Capture → `v1-core` (was unlabeled; now essential for the 6-month vision
  "at least two real projects outside software are active and growing")
- PK-03: Today View → `v1-core` (confirms V1_PLAN Step 05 requirement; referenced in intake-001)
- XP-01: Cross-Project Discovery → `v1-core` (was v1 nice-to-have; the 12-month vision
  explicitly requires "shared, queryable knowledge base" across projects)

**Language updated (vision v2.0 alignment):**
- NF-01: Reframed around "continuity layer" — applies to both AI agents and the human
- NF-02: Updated to emphasise human recall of reasoning ("six months in, you still trust
  your own past reasoning") alongside agent enforcement
- NF-06: Explicitly tied to v2.0 principle "The system learns by running"
- NF-07: Reframed for multi-domain project bootstrapping (not just software)

**Stage targets added (new field for all UCs):**
Every UC now carries an explicit `stage_target` (v1-core | v1.1 | v1 | v2 | post-v1).
This resolves the ambiguity flagged in the 2026-03-31 health check analysis.

**Moved to Pending (scope reduction for v1):**
- AP-03, AP-04, AP-05, AP-07 → `v2` (deep AP features beyond v1 dogfooding scope)
- RE-02, RE-03, RE-04, RE-05, RE-07 → `v2` (deep RE features; RE-01 + RE-06 are enough for v1)
- XP-02 (terminology management), XP-05 (scale), XP-06 (concurrency) → `post-v1` CANDIDATE

**Stage reassigned but kept ACTIVE:**
- NF-08 → `v1.1` (health metrics are not a Stage 1 blocker)
- XP-07 → `v2` (domain extensibility becomes relevant at Stage 3 Framework Product)

**Active intake mapping confirmed:**
- intake-001 (Step 02 Memory Integration Layer) → NF-01, NF-02, NF-09, PK-03, XP-01
  All 5 UCs are confirmed ACTIVE with `stage_target: v1-core`. ✓

**No retirements:** No UCs have been deprecated in this pass. All demoted UCs move to Pending.

---

## How to Read This Document

Each use case follows this structure:

| Field | Meaning |
|---|---|
| **ID** | Stable identifier (e.g., `NF-03`) for referencing in tasks, ADRs, tests |
| **Title** | One-line name |
| **stage_target** | When this UC is scheduled: v1-core · v1 · v1.1 · v2 · post-v1 |
| **Actor** | Who or what triggers/participates (Human, Agent, Curator, System) |
| **Situation** | The context in which this need arises — the "when" |
| **Need** | What the actor needs to accomplish — the "what" |
| **Success looks like** | Observable outcomes that confirm the need was met |
| **Failure looks like** | What happens if nowu can't handle this — why it matters |
| **Open questions** | Unresolved design tensions. Intentionally left open. |

### Project Key

| Code | Project |
|---|---|
| **NF** | nowu Framework (self-development, meta) |
| **AP** | Filipino Aperitif & Pili-Nut Business |
| **RE** | Real-Estate Business Digitalization |
| **PK** | Personal Knowledge Management |
| **XP** | Cross-Project & Framework-Level |

---

## 1. Catalog Overview

- **Product:** nowu
- **Vision anchor:** nowu is the continuity layer between having a goal and making it real. It holds
  the project's intent, decisions, and the reasoning behind them — so nothing disappears between
  sessions and the AI always knows what it's building toward. The more you use it, the more it
  knows — the vision sharpens, the decisions compound, and the knowledge becomes part of the
  product itself. For the multi-project human who loses context easily: nowu is the difference
  between a project that compounds and one that resets.
- **Current stage:** Stage 1 — v1-core framework. Step 02 (Memory Integration Layer) in progress.
- **Scope of this catalog:**
  - NF group: v1-core framework self-development (all 10 UCs, Stage 1 required)
  - AP, RE groups: v1 dogfooding (minimal 2-3 UCs per project, test nowu on real non-software work)
  - PK group: v1-core (fast capture + today view) and v1.1 (rest)
  - XP group: v1-core (cross-project discovery) and v1.1/v2 (advanced cross-project features)

---

## 2. Use Case Table (active)

| UC-ID  | Title                                          | stage_target | Primary Persona       | Status    |
|--------|------------------------------------------------|--------------|-----------------------|-----------|
| NF-01  | Resume Work After Context Loss                 | v1-core      | Agent / Human         | ACTIVE    |
| NF-02  | Track and Enforce Architectural Decisions      | v1-core      | Agent / Human         | ACTIVE    |
| NF-03  | Scope a Piece of Work Without Scope Creep      | v1-core      | Agent (Shaper)        | ACTIVE    |
| NF-04  | Self-Assess Quality Without Human Intervention | v1-core      | Agent (Reviewer)      | ACTIVE    |
| NF-05  | Route Approvals Without Blocking Progress      | v1-core      | System / Human        | ACTIVE    |
| NF-06  | Learn From Past Mistakes Across Sessions       | v1-core      | Curator / System      | ACTIVE    |
| NF-07  | Bootstrap a New Project Using the Framework    | v1-core      | Human / Orchestrator  | ACTIVE    |
| NF-08  | Measure and Visualize Framework Health         | v1.1         | Curator / Human       | ACTIVE    |
| NF-09  | Ensure Every Deliverable Traces Back to a UC   | v1-core      | Reviewer / Shaper     | ACTIVE    |
| NF-10  | Maintain the Thread for the Multi-Project Human| v1-core      | Multi-Project Human   | ACTIVE    |
| AP-01  | Track Regulatory Requirements as Living Knowledge | v1        | Human / Agent         | ACTIVE    |
| AP-02  | Manage Product Formulation as Versioned Knowledge | v1        | Human / Agent         | ACTIVE    |
| AP-06  | Evaluate a Business Decision With Traceability | v1           | Human / Agent         | ACTIVE    |
| RE-01  | Inventory Existing Processes Before Digitalization | v1        | Human / Agent         | ACTIVE    |
| RE-06  | Support Long-Term Investment Decision Tracking | v1           | Human / Agent         | ACTIVE    |
| PK-01  | Capture a Thought Before It's Lost             | v1-core      | Human                 | ACTIVE    |
| PK-02  | Surface Relevant Knowledge Without Being Asked | v1.1         | System (proactive)    | ACTIVE    |
| PK-03  | Maintain a "Today" View Across All Projects    | v1-core      | Human                 | ACTIVE    |
| PK-04  | Let Knowledge Decay and Clean Up Gracefully    | v1.1         | Curator / Human       | ACTIVE    |
| PK-05  | Build Understanding Incrementally Over a Topic | v1.1         | Human / Agent         | ACTIVE    |
| PK-06  | Protect Sensitive Personal Knowledge           | v1.1         | Human / System        | ACTIVE    |
| XP-01  | Discover Connections Across Projects Automatically | v1-core  | System / Human        | ACTIVE    |
| XP-03  | Transfer Lessons Learned Between Projects      | v1.1         | Agent / Human         | ACTIVE    |
| XP-04  | Handle Conflicting High-Confidence Knowledge   | v1.1         | Curator / Human       | ACTIVE    |
| XP-07  | Adapt the Framework to a New Domain Without Rewriting | v2  | Human / System        | ACTIVE    |

---

## 3. Use Cases (detailed)

---

## A. nowu Framework — Self-Development & Meta

These use cases describe what nowu needs to support *its own development*. Since nowu eats its own
dog food, these are the first use cases it must satisfy.

---

### NF-01: Resume Work After Context Loss

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Any step agent (nowu-intake, nowu-constraints, nowu-options, nowu-decider, nowu-shaper, nowu-implementer, nowu-reviewer, nowu-curator); also the Multi-Project Human resuming a project |
| **Situation** | A new session starts. The previous session ended mid-task — possibly abruptly (token limit, crash, human walked away). Neither the agent nor the human has the working memory of what happened. nowu must be the continuity layer that bridges the gap. |
| **Need** | Reconstruct enough context to continue productive work without re-doing completed steps or asking the human to repeat themselves. For agents: read persisted state and identify the last verified checkpoint. For the human: receive a clear signal of where things stand so they can confidently resume direction. |
| **Success looks like** | Agent reads persisted state, identifies the last verified checkpoint, and proposes the correct next action within the first response — without hallucinating progress that didn't happen. The human's first interaction with a resuming project feels like picking up where they left off, not restarting. |
| **Failure looks like** | Agent starts over from scratch, contradicts previous decisions, or claims work is done that was never completed. Human loses trust and begins micromanaging. Projects drift because the continuity overhead is too high. |
| **Open questions** | What's the minimum viable state that must survive a crash? *(Recovery approach resolved: agent reads `state/SESSION-STATE.md` bookmark and proposes next action — human confirms at S1 gate. See WORKFLOW.md §S0.)* How should the human-facing orientation differ from the agent-facing resumption protocol? |

---

### NF-02: Track and Enforce Architectural Decisions

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Reviewer Agent (enforcer); Implementer Agent (constrained party); Multi-Project Human (recall reader) |
| **Situation** | The team (human + agents) has made design decisions over time. New code is being written. Separately, months later, the human is evaluating a new approach and needs to trust that the decision they made six months ago was sound — and understand why. |
| **Need** | Decisions must be recorded with rationale, discoverable by any agent working on related code, and enforceable — violations caught before merge. Equally, the human must be able to retrieve the *why* behind any significant decision, understand what was known at the time, and evaluate whether it still holds. "Six months in, you still trust your own past reasoning." |
| **Success looks like** | When an Implementer generates code that violates an ADR, the Reviewer flags the specific violation and references the original decision. Six months later, the human retrieves a design decision, reads its rationale and the alternatives considered, and can confidently affirm or challenge it with full context. |
| **Failure looks like** | Architectural drift accumulates silently. OR: the human revisits a past decision and has no idea why it was made, treats it as arbitrary, and repeats the same analysis from scratch — abandoning what was already hard-won. |
| **Open questions** | Should ADRs be machine-parseable (structured) or natural language? Can agents propose ADR amendments autonomously, or must a human approve all changes to architectural decisions? |

---

### NF-03: Scope a Piece of Work Without Scope Creep

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Shaper Agent; Human (as approver) |
| **Situation** | A raw idea exists ("add semantic search to the CLI"). It needs to become a bounded set of tasks that an Implementer can complete without spiraling into adjacent concerns. |
| **Need** | Transform the idea into 3—7 tasks with explicit boundaries: what's in scope, what's explicitly out, what the acceptance criteria are, and what other work this depends on or blocks. |
| **Success looks like** | Each task can be completed in < 4 hours of agent work. Scope boundaries prevent touching unrelated modules. The Implementer never needs to ask "should I also do X?" because the boundary already says no. |
| **Failure looks like** | A task balloons from "add a CLI flag" into "refactor the entire search module." Or: tasks are so vague that two agents produce conflicting implementations. |
| **Open questions** | *(Both resolved: boundaries are file-level via `in_scope_files` in Task Spec (S5 output). nowu-shaper loads the file tree. See WORKFLOW.md context scoping rules.)* |

---

### NF-04: Self-Assess Quality Without Human Intervention

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Implementer Agent; Reviewer Agent |
| **Situation** | The Implementer has written code and claims it's done. Before requesting human review, the system needs to verify the claim independently. |
| **Need** | Automatically verify that: tests pass, coverage meets threshold, the code compiles/runs, and the output matches the acceptance criteria from the task spec — without relying on the agent's self-report. |
| **Success looks like** | The Verify Before Reporting (VBR) protocol runs actual tests in a sandbox. Only verified-passing work reaches the human review queue. False "done" claims are caught and recycled back to the Implementer. |
| **Failure looks like** | Agents claim tasks are complete based on their own assessment. Human discovers broken code during batch review. Trust erodes. Review becomes a bottleneck instead of a gate. |
| **Open questions** | What verification is feasible for non-code tasks (documentation, architecture diagrams, research)? How do we handle flaky tests vs. genuine failures? |

---

### NF-05: Route Approvals Without Blocking Progress

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | System (approval routing); Human (as approver) |
| **Situation** | The framework operates on a tiered approval model. Some actions need immediate human approval (Tier 3: merge to main), some can be batched (Tier 2: code review), and some can auto-proceed with audit trail (Tier 1: test generation). |
| **Need** | Classify each action into the correct tier, queue it appropriately, and allow low-risk work to continue flowing while high-risk work waits. The human should be able to review batched approvals efficiently. |
| **Success looks like** | At mid-afternoon, the human opens a queue of 5 items, reviews and approves them in 10 minutes, and agents immediately resume. Tier 1 items were never blocked. Tier 3 items halted exactly where they should have. |
| **Failure looks like** | Everything blocks on human approval (progress stalls) OR nothing blocks (dangerous changes go through unchecked) OR the tier classification is wrong (a breaking change is auto-approved). |
| **Open questions** | Can tier classification be learned from past decisions? Should there be an escalation path if the human doesn't respond within X hours? What metadata does a queued item need for fast human review? |

---

### NF-06: Learn From Past Mistakes Across Sessions

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | nowu-curator (S9); pattern detection triggered by nowu-implementer and nowu-reviewer outputs |
| **Situation** | A pattern emerges across sessions: the same type of bug keeps being introduced, or the same scoping mistake keeps being made. Capture records accumulate. The system has everything it needs to improve — but only if it runs the analysis and feeds results back into future behaviour. This is what "The system learns by running" means in practice. |
| **Need** | Detect recurring patterns in session logs, code review feedback, and task outcomes. Surface them as "lessons learned" that actively influence future agent behaviour — not just passive documentation. Each cycle makes the system more aligned with what works. |
| **Success looks like** | After the third time a date-parsing bug appears, the Implementer proactively adds timezone-aware handling before being told. After two failed scoping attempts on UI tasks, the Shaper adjusts its task size heuristic. Capture records reference prior lessons by ID, and the loop visibly closes. |
| **Failure looks like** | The same mistakes repeat indefinitely. Session logs grow but are never analysed. The framework gets "more documented" but not "smarter." Using nowu longer does not make it better at its job. |
| **Open questions** | How do we distinguish a genuine pattern from coincidence (minimum occurrences)? Should lessons feed into prompts, into constraints, or into both? How do we prevent "over-learning" from a small sample? |

---

### NF-07: Bootstrap a New Project Using the Framework

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Human (initiating); Orchestrator Agent (executing) |
| **Situation** | The human wants to start a new project — a food business, a real-estate operation, a creative project, or a software tool. The nowu framework is already operational. Now it needs to be applied to a completely different domain, without contaminating the framework's own development state. The vision requires "at least two real projects outside software" to be active by the 6-month horizon. |
| **Need** | Create the project scaffolding (directory structure, initial artifacts, project identity) and configure the agents to operate within that project's context. This must work equally well for software and non-software projects. |
| **Success looks like** | After a single command or conversation, the new project has its own memory space, its own decision journal, and agents can begin framing the first idea — all while the framework's own development continues independently. Bootstrapping a non-software project (e.g., a food business) feels as natural as bootstrapping a code project. |
| **Failure looks like** | Framework state and project state bleed into each other. OR: bootstrapping a new project requires hours of manual setup. OR: the framework only works for software, forcing the human to manage non-software projects outside of nowu entirely. |
| **Open questions** | Should each project be a separate repository, a separate branch, or a separate directory? How much agent configuration should be inherited vs. customised per project? How does the framework know a project is "software" vs. "non-software" in terms of what defaults to apply? |

---

### NF-08: Measure and Visualize Framework Health

| Field | Detail |
|---|---|
| **stage_target** | v1.1 |
| **Actor** | nowu-curator (S9, periodic health pass); Human (reviewing) |
| **Situation** | The framework has been running for several weeks across multiple projects. The human wants to know: Is it actually working? Is quality improving? Are agents productive? |
| **Need** | Collect and surface health metrics: task completion velocity, test coverage trend, decision documentation coverage, approval latency, memory integrity, agent loop frequency, recurring failure patterns. |
| **Success looks like** | A weekly health report shows trends over time. The human can spot problems (declining velocity, rising loop frequency) before they become crises. The report is generated by agents, not manually compiled. |
| **Failure looks like** | The framework "feels" productive but nobody knows if quality is actually improving. Problems are discovered retroactively when something breaks in production. |
| **Open questions** | What's the minimum set of health metrics that's actually actionable (avoid dashboard overload)? Should health reports trigger automatic interventions (e.g., pause work if coverage drops below threshold)? |

---

### NF-09: Ensure Every Deliverable Traces Back to a Use Case

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | nowu-reviewer (S8); nowu-shaper (S5, as producer) |
| **Situation** | The team (human + agents) has been building features and fixing bugs across multiple steps. Over time it becomes unclear whether some pieces of work were actually needed — or whether they drifted from the original intent. |
| **Need** | Every implemented feature must carry an unbroken chain from code → test → acceptance criterion → use case ID → intake brief → project objective. This chain must be machine-checkable at review time, not reconstructed from memory. |
| **Success looks like** | When nowu-reviewer runs S8 on a change set, it reads the `validation_trace` in the task spec and can follow every criterion back to a use case ID in this document. Any criterion without a traceable use case is flagged as a scope violation — not a suggestion, a blocker. |
| **Failure looks like** | Code exists with no traceable use case. Reviewers ask "why was this built?" and nobody can answer without reading git history. Over time the codebase contains features that serve no documented need. |
| **Open questions** | Should orphaned code (code with no use case link) be automatically flagged by a linter, or only checked during review? How should use case IDs be embedded in tests — as comments, as test name prefixes, or as structured metadata? |

---

### NF-10: Maintain the Thread for the Multi-Project Human

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Multi-Project Human (primary); nowu system (orientation provider) |
| **Situation** | Raphael is running several concurrent projects across different domains. When he returns to any given project — after a day, a week, or longer — he arrives without the working memory he had last time. He knows things were moving forward but cannot easily answer: what was I doing, what did I decide, what should I do next? The "low-grade guilt of stalled projects" comes from the re-orientation cost, not from lack of effort. |
| **Need** | Give the human a fast, trustworthy orientation into any project at any time — pulling together the current state, the last active thread, the most recent decisions, and the next logical action — without requiring them to read through a transcript or commit history. The experience must make progress feel compounding, not resetting. |
| **Success looks like** | The human opens a project they haven't touched in 10 days. Within one interaction, they know: what was completed, what's in progress, the last key decision and why it was made, and the recommended next step. The "thread" has been held. They can make a meaningful contribution in minutes rather than re-investing an hour to re-load context. |
| **Failure looks like** | Every return to a project requires a 20-minute archaeological dig through files, notes, and commit logs. The human carries the context burden in their own head. Projects stall not because of insufficient work, but because the re-orientation cost is too high to pay repeatedly. Progress resets instead of compounds. |
| **Open questions** | What is the minimum viable orientation artifact — can it be synthesised from existing structured state (`SESSION-STATE.md`, `DECISIONS.md`, `PROGRESS.md`) or does it need dedicated session-summary atoms in `know`? Should orientation be triggered explicitly by the human ("catch me up") or offered automatically when a project is opened after an absence? How does orientation for a first-time human visitor differ from the owner resuming? |

---

## B. Filipino Aperitif & Pili-Nut Business

These use cases describe what nowu must support for managing a real food & beverage product
business, from concept to market. For v1, three UCs are ACTIVE as dogfooding targets.
The remaining four are deferred to v2 (see Section 5).

---

### AP-01: Track Regulatory Requirements as Living Knowledge

| Field | Detail |
|---|---|
| **stage_target** | v1 |
| **Actor** | Human (researcher); Agent (tracker) |
| **Situation** | Launching a food/beverage product in the Philippines requires navigating multiple regulatory bodies: FDA (License to Operate, Certificate of Product Registration), DTI/SEC registration, BIR tax compliance, local government permits (barangay clearance, mayor's permit, sanitary permit), plus excise tax requirements for alcoholic beverages. Requirements change, have dependencies, and have deadlines. |
| **Need** | Capture each regulatory requirement as a piece of knowledge with its source, confidence level, dependencies on other requirements, and status. Surface what's blocking what. Alert when something may have changed or expired. |
| **Success looks like** | At any point, the human can ask "what do I still need to do to legally sell this product?" and get an accurate, dependency-ordered answer that reflects the current state — including which permits depend on which other permits being obtained first. |
| **Failure looks like** | Requirements are scattered across notes, bookmarks, and memory. A critical dependency is missed (e.g., you need the FDA LTO before you can get the CPR). The product launch is delayed by months because of a forgotten permit. |
| **Open questions** | How should nowu handle regulatory requirements that are "probably still current" but haven't been verified recently? Should there be automatic reminders for permit renewals? How to handle conflicting information from different government sources? |

---

### AP-02: Manage Product Formulation as Versioned Knowledge

| Field | Detail |
|---|---|
| **stage_target** | v1 |
| **Actor** | Human (formulator); Agent (recorder, searcher) |
| **Situation** | The aperitif recipe evolves through experimentation. Each version has specific ingredient ratios, process steps, taste notes, shelf-life observations, and cost implications. Some versions are abandoned, some are promising, and one becomes the production recipe. |
| **Need** | Record each formulation version with its parameters, link it to taste test results and cost analysis, track why versions were abandoned or selected, and make it easy to compare versions or revisit abandoned approaches when new information arrives. |
| **Success looks like** | When the human asks "why did we abandon version 3?" the system returns the decision with rationale. When ingredient costs change, the system can show which formulations are affected. |
| **Failure looks like** | Recipes exist as notes in a phone, a notebook, and a spreadsheet. Version history is lost. The human re-tests a formulation that was already proven to fail. Or: the winning recipe's rationale is forgotten, making it impossible to adapt when ingredients change. |
| **Open questions** | Should formulation data be structured (key-value) or narrative? How detailed should process steps be (reproducibility vs. documentation burden)? Should the system support multimedia (photos of results, taste test recordings)? |

---

### AP-06: Evaluate a Business Decision With Traceability

| Field | Detail |
|---|---|
| **stage_target** | v1 |
| **Actor** | Human (decision-maker); Agent (analyst, recorder) |
| **Situation** | The human faces a business decision: Should we use glass bottles or pouches for the first production run? There are cost, branding, regulatory, and supply chain implications. The human wants to think through the decision systematically and revisit the reasoning later. This is the non-software equivalent of NF-02 — traceable decisions apply to any domain. |
| **Need** | Structure the decision: what are the options, what criteria matter, what evidence supports each option, what's the recommendation, what's the chosen path and why. Store the decision with links to the evidence and rationale so it can be revisited when conditions change. |
| **Success looks like** | Six months later, when considering a packaging change, the human retrieves the original decision, sees that "glass was chosen because of premium positioning and FDA label requirements" and evaluates whether those reasons still hold given new conditions. |
| **Failure looks like** | The decision is made in a conversation and forgotten. When the packaging question comes up again, the entire analysis is repeated from scratch. Or worse: the same decision is revisited repeatedly without remembering the previous conclusions. |
| **Open questions** | Should decision templates be prescriptive (force a structure) or flexible (allow freeform with optional structure)? How do we handle decisions made quickly and informally — is there a "lightweight decision" format? |

---

## C. Real-Estate Business Digitalization

These use cases describe what nowu must support for migrating a traditional, paper-heavy
real estate operation into digital workflows. For v1, two UCs are ACTIVE as dogfooding
targets. The remaining five are deferred to v2 (see Section 5).

---

### RE-01: Inventory Existing Processes Before Digitalization

| Field | Detail |
|---|---|
| **stage_target** | v1 |
| **Actor** | Human (business analyst); Agent (documenter) |
| **Situation** | The real estate business runs on paper, phone calls, and human memory. Before digitalising anything, the current processes need to be understood: how are properties listed, how are tenants onboarded, how are contracts managed, how is maintenance tracked? Nobody has documented these processes — they exist as institutional knowledge in people's heads. |
| **Need** | Capture each process as a sequence of steps, participants, inputs/outputs, and pain points. Link processes to each other where they share data or handoffs. Identify which processes are highest-value to digitalise first. |
| **Success looks like** | After interviews and observation, the system contains a map of ~10-20 core processes. Each has clear steps, identified bottlenecks, and an estimated digitalisation value. The human can prioritise digitalisation by actual impact rather than gut feel. |
| **Failure looks like** | Digitalisation starts with whatever seems obvious ("let's build a website!") rather than where the actual pain is. Processes are digitalised in isolation, creating new data silos that are worse than the paper originals. |
| **Open questions** | How should informal/ad-hoc processes be captured vs. formal ones? Should the system enforce a process notation (BPMN) or accept natural language? How do we handle processes that vary by property or person? |

---

### RE-06: Support Long-Term Investment Decision Tracking

| Field | Detail |
|---|---|
| **stage_target** | v1 |
| **Actor** | Human (investor/owner); Agent (analyst) |
| **Situation** | Real estate investment decisions play out over years. A decision to acquire a property was based on assumptions about rental yield, appreciation, and renovation costs. Years later, the human wants to evaluate: were those assumptions correct? What can we learn for the next acquisition? |
| **Need** | Record investment theses (assumptions, projections, confidence levels) at decision time, link them to actual outcomes as they materialise, and support retrospective analysis. Enable pattern recognition across multiple properties over time. |
| **Success looks like** | Three years after acquiring Property A, the system shows: "Projected yield: 8%. Actual yield: 6.5%. Primary variance: renovation costs were 40% over estimate (see decision RE-DEC-003). This matches the pattern in Property B and C." |
| **Failure looks like** | Investment decisions are made in conversations and forgotten. Performance is tracked in spreadsheets disconnected from the original reasoning. The same estimation mistakes are repeated across properties because nobody connects the pattern. |
| **Open questions** | How to model financial projections as knowledge (structured vs. narrative)? Should the system track actual financial performance, or is that a separate financial tool? How to handle the sensitivity of investment data? |

---

## D. Personal Knowledge Management

These use cases describe what nowu must support for the human's personal knowledge — the
foundation layer beneath all projects.

---

### PK-01: Capture a Thought Before It's Lost

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Human |
| **Situation** | Raphael is juggling multiple concurrent projects. A thought arrives at any moment — at 11 PM, during a commute, mid-conversation. It might be a business idea, a cross-project connection, a fragment worth keeping. The capture moment is brief. If the cost of capturing it is too high, the thought disappears — and with it a potential compound move for one of his projects. |
| **Need** | Record the thought with minimal friction (a few words, a voice note, a quick type). The system handles categorisation, linking, and enrichment later — not at capture time. The thought must not be lost even if it is not yet organised. |
| **Success looks like** | The next morning, the human's captured thoughts are organised by likely project, tagged with suggested connections to existing knowledge, and surfaced in the relevant context. Capturing takes 5-10 seconds. Reviewing and routing takes 5 minutes. The system handles the work of connecting inputs to existing knowledge. |
| **Failure looks like** | Capturing a thought requires choosing a project, a type, tags, and a confidence level. The friction is so high that the human reverts to a paper napkin. The system has perfect metadata but nobody uses it. |
| **Open questions** | What's the minimum viable capture format? Should auto-categorisation happen immediately or in batch? How do we handle truly miscellaneous thoughts that don't belong to any project? |

---

### PK-02: Surface Relevant Knowledge Without Being Asked

| Field | Detail |
|---|---|
| **stage_target** | v1.1 |
| **Actor** | System (proactive); Human (recipient) |
| **Situation** | The human is working on the aperitif project — specifically on packaging. They don't realize that three weeks ago, during real-estate research, they captured a note about a packaging supplier they encountered. |
| **Need** | When the human is working in a specific context, proactively surface knowledge from other projects or past captures that is semantically relevant — without overwhelming them with noise. |
| **Success looks like** | While working on AP packaging decisions, the system gently surfaces: "You noted a packaging contact during RE research on Feb 12 — possibly relevant?" The human either links it (valuable discovery) or dismisses it (low cost). |
| **Failure looks like** | Either: nothing is ever surfaced (missed connections accumulate) OR everything even vaguely related is surfaced (the system becomes annoying and is ignored). |
| **Open questions** | What threshold of relevance justifies interrupting the human's focus? Should surfacing be pull (human asks "what else do I know about this?") or push (system proactively suggests)? How do we measure if cross-pollination is actually valuable? |

---

### PK-03: Maintain a "Today" View Across All Projects

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | Human |
| **Situation** | Raphael wears multiple hats across concurrent projects. Each morning, he needs to know: what's due today? What's overdue? What's the most important thing to focus on? This requires pulling from multiple projects and personal reminders — without him assembling it manually from four different systems. V1_PLAN Step 05 delivers the CLI surface that makes this possible. Referenced in intake-001. |
| **Need** | A unified daily view that aggregates tasks, reminders, and upcoming deadlines across all projects and personal knowledge. Sorted by actual urgency and importance, not just by project. Able to distinguish "buy groceries" (low importance, time-sensitive) from "FDA application deadline" (high importance, time-sensitive). |
| **Success looks like** | The human starts the day with a single view showing 3-5 focus items and 10-15 background items. The focus items are genuinely the most important things to do today. The view adapts as items are completed and new work is added. No external system needs to be consulted. |
| **Failure looks like** | The human checks 4 different systems (project boards, to-do lists, calendar, notes) to assemble their own daily plan. Important items from one project are eclipsed by urgent-but-unimportant items from another. |
| **Open questions** | How should importance be calculated across different projects (is an aperitif FDA deadline more important than a framework milestone)? Should the daily view be generated by an agent or computed from structured data? How to handle items without explicit due dates? |

---

### PK-04: Let Knowledge Decay and Clean Up Gracefully

| Field | Detail |
|---|---|
| **stage_target** | v1.1 |
| **Actor** | Curator (automated); Human (reviewer) |
| **Situation** | Over months, the knowledge base accumulates: old grocery lists, superseded decisions, market intelligence about a product that was abandoned, regulatory information that may have changed, and notes that seemed important at the time but never connected to anything. |
| **Need** | Periodically review knowledge for staleness, obsolescence, and irrelevance. Identify candidates for archival or deletion. Flag high-importance knowledge that hasn't been verified in a long time. Handle the distinction between "this is old and probably still true" vs. "this is old and probably wrong now." |
| **Success looks like** | Monthly, the Curator surfaces: 15 items recommended for archival (no connections, no access, low importance), 3 items flagged for re-verification (high importance but stale), 1 contradiction detected between two high-confidence items. The human reviews in 10 minutes. |
| **Failure looks like** | The knowledge base grows indefinitely. Search results are polluted with stale information. The human stops trusting the system because outdated information is surfaced alongside current information. Or: aggressive cleanup deletes something that turns out to be needed. |
| **Open questions** | Should archived knowledge be searchable or hidden? How do we distinguish "timeless" knowledge from "time-sensitive" knowledge without requiring the human to classify everything? What's the cost of a false deletion vs. the cost of eternal accumulation? |

---

### PK-05: Build Understanding Incrementally Over a Topic

| Field | Detail |
|---|---|
| **stage_target** | v1.1 |
| **Actor** | Human (learner); Agent (synthesiser) |
| **Situation** | The human is learning about something over time: Philippine excise tax law, pili-nut processing techniques, property valuation methods, or a new programming framework. Knowledge arrives in fragments across days or weeks — an article here, a conversation there, a practical experiment. |
| **Need** | Assemble fragments into an evolving understanding. Track what's well-understood vs. what has gaps. When new information arrives, integrate it with existing understanding — especially when it contradicts or refines what was previously known. |
| **Success looks like** | After reading 5 articles about excise tax over 3 weeks, the human asks "summarize what I know about excise tax for coconut-based spirits" and gets a coherent synthesis that includes confidence levels ("the base rate is P8/proof liter — well established" vs. "annual escalation schedule — needs verification, sources disagree"). |
| **Failure looks like** | Each article is stored as a separate note with no synthesis. The human has 5 notes about excise tax but can't answer a basic question without re-reading all of them. New information doesn't update old understanding — both coexist without resolution. |
| **Open questions** | Should synthesis be automatic or human-triggered? How to handle contradictions between sources of similar authority? Should the system track the human's confidence separately from the source's reliability? |

---

### PK-06: Protect Sensitive Personal Knowledge

| Field | Detail |
|---|---|
| **stage_target** | v1.1 |
| **Actor** | Human (owner); System (access control) |
| **Situation** | The knowledge base contains information of varying sensitivity: public (product specs), internal (business strategy), personal (financial information, health notes, relationship observations), and confidential (legal documents, investment details). |
| **Need** | Control what knowledge is accessible in which context. Prevent sensitive personal knowledge from leaking into generated reports, shared briefings, or agent-generated outputs. Allow the human to classify sensitivity without requiring it for every item. |
| **Success looks like** | When generating a briefing for a business partner (AP-07), the system automatically excludes personal financial notes, internal competitive analysis, and real-estate investment details — even though they're in the same knowledge base. |
| **Failure looks like** | A generated report includes a personal note about a business partner. Or: the sensitivity system is so restrictive that agents can't access the knowledge they need to be useful. |
| **Open questions** | Should sensitivity be per-atom, per-project, or per-tag? What are the default sensitivity levels? How should agents handle knowledge they can "see" exists but can't "read" due to sensitivity? |

---

## E. Cross-Project & Framework-Level

These use cases describe capabilities that span multiple projects or operate at the
framework level.

---

### XP-01: Discover Connections Across Projects Automatically

| Field | Detail |
|---|---|
| **stage_target** | v1-core |
| **Actor** | System (semantic search); Human (evaluator) |
| **Situation** | The 12-month vision horizon requires "knowledge accumulates within each project and starts to connect usefully across them through a shared, queryable knowledge base." The human's coconut plantation (real-estate project) is also a potential supply source for the aperitif business. A technical pattern learned while building the framework might solve a problem in the real-estate project. These connections aren't explicitly created — they emerge from overlapping knowledge. |
| **Need** | When working in one project's context, discover and surface relevant knowledge from other projects based on semantic similarity, shared entities, or shared concepts — without requiring the human to manually link everything. This is essential for the multi-project human to benefit from the full scope of what they know. |
| **Success looks like** | While planning the aperitif supply chain, the system surfaces the coconut plantation property from the real-estate project as a potential supplier. The human doesn't need to remember it exists or maintain the link manually. Referenced in V1_PLAN Step 02 and intake-001. |
| **Failure looks like** | Projects exist in complete isolation. The human manually cross-references by memory. Obvious connections are missed, and the "shared, queryable knowledge base" remains aspirational because it only works within project walls. |
| **Open questions** | How should cross-project discovery be balanced against project focus (too much cross-pollination is distracting)? Should cross-project connections be explicit (create a link) or implicit (just surface in search)? How to handle conflicting knowledge across projects? |

---

### XP-03: Transfer Lessons Learned Between Projects

| Field | Detail |
|---|---|
| **stage_target** | v1.1 |
| **Actor** | Learner Agent; Human (evaluator) |
| **Situation** | A process improvement discovered while building the framework (e.g., "tasks scoped to < 4 hours are 3x more likely to succeed") might apply to digitalisation task planning. A vendor evaluation technique used for the aperitif business might work for selecting real-estate technology partners. |
| **Need** | When a lesson is learned in one project, evaluate whether it generalises to other projects. If it does, surface it as a recommendation — not an automatic change — in the relevant project context. |
| **Success looks like** | After discovering that "tasks > 4 hours fail 60% of the time" in the framework project, the system flags 3 tasks in the real-estate project that exceed 4 hours and suggests decomposition. |
| **Failure looks like** | Each project learns its own lessons in isolation. The same mistake is made independently in each project. Or: a lesson from one domain is applied blindly to another where it doesn't fit. |
| **Open questions** | What makes a lesson "transferable" vs. "domain-specific"? Should transferred lessons carry lower confidence than native ones? How to prevent a lesson from one small project from inappropriately influencing a larger one? |

---

### XP-04: Handle Conflicting High-Confidence Knowledge

| Field | Detail |
|---|---|
| **stage_target** | v1.1 |
| **Actor** | Curator (detector); Human (resolver) |
| **Situation** | Two pieces of knowledge exist with high confidence but contradict each other. Perhaps an older verified fact conflicts with newer information from a different source. Or two sources with similar authority disagree about a parameter. |
| **Need** | Detect the contradiction, present both pieces of knowledge with their provenance and timestamps, and escalate to the human for resolution — especially when the contradicting items are both high-confidence or when downstream decisions depend on the resolution. |
| **Success looks like** | The system flags: "CONFLICT: Atom #A says excise tax is P8/proof liter (grade 5, verified 2025-01). Atom #B says it's P12/proof liter (grade 4, captured 2025-11). Atom #A is linked to 3 cost calculations. Resolution needed." The human resolves, the old fact is marked as superseded. |
| **Failure looks like** | Both facts coexist. An agent uses the stale one for a cost calculation. Nobody notices until the first tax filing. "The system knows two things that contradict each other and has no way to tell you." |
| **Open questions** | Should conflict detection run continuously or periodically? How to handle "soft" contradictions (values that are close but not identical) vs. "hard" contradictions (mutually exclusive claims)? What happens when neither the human nor the agent can determine which is correct? |

---

### XP-07: Adapt the Framework to a New Domain Without Rewriting

| Field | Detail |
|---|---|
| **stage_target** | v2 |
| **Actor** | Human (new domain); System (framework) |
| **Situation** | After succeeding with the initial projects, the human wants to apply nowu to a completely new domain: maybe learning a language, planning a community event, or helping a friend organise their business. The new domain has different knowledge types, different rhythms, and different importance criteria. |
| **Need** | The framework should accommodate new domains without requiring changes to core code. Knowledge types, connection types, approval tiers, and agent behaviours should be configurable or extensible per project. The core remains stable while the periphery adapts. |
| **Success looks like** | Adding a "language learning" project requires: creating the project, optionally defining a few custom knowledge types, and starting to capture knowledge. No code changes. No migration. The existing projects are unaffected. |
| **Failure looks like** | Every new domain requires modifying the schema, adding database columns, or changing agent behaviour. The framework becomes rigid — optimised for its original projects but hostile to new ones. |
| **Open questions** | How much domain-specific configuration should be allowed vs. how much should be handled by the generic knowledge model? Should custom knowledge types be true schema extensions or just tags/conventions? Where's the line between "flexible enough" and "so flexible it's meaningless"? |

---

## 4. Stage Mapping

**v1-core — Must be satisfied for Stage 1 exit (all 7 V1_PLAN steps):**
- NF-01, NF-02, NF-03, NF-04, NF-05, NF-06, NF-07, NF-09, NF-10
- PK-01, PK-03
- XP-01

V1_PLAN step-to-UC traceability:
- Step 01 (Done): NF-01, NF-02, NF-03
- Step 02 (In Progress): NF-01, NF-02, NF-09, PK-03, XP-01 ← intake-001
- Step 03: NF-01, NF-04
- Step 04: NF-02, NF-03, NF-04
- Step 05: NF-05, NF-07, PK-01, PK-03
- Step 06: NF-06, PK-04, XP-04
- Step 07: NF-07, XP-01, XP-03

**v1 (Stage 1, dogfooding) — Must be tested before Stage 1 exit via real non-software projects:**
- AP-01, AP-02, AP-06 (aperitif project as test bed)
- RE-01, RE-06 (real estate as test bed)

**v1.1 — Stage 2, reliability and wider dogfooding:**
- NF-08
- PK-02, PK-04, PK-05, PK-06
- XP-03, XP-04

**v2 — Stage 3, Framework Product (installable, first external users):**
- XP-07
- AP-03, AP-04, AP-05, AP-07 (full AP product suite)
- RE-02, RE-03, RE-04, RE-05, RE-07 (full RE product suite)

**post-v1 CANDIDATE (uncertain; not yet committed):**
- XP-02 (terminology management)
- XP-05 (scale)
- XP-06 (concurrency)

---

## 5. Pending and Deprecated

### Pending — Active CANDIDATE (deferred, not yet sequenced)

These UCs are well-understood and will eventually be needed, but are out of scope for v1
and have not been sequenced into a delivery plan yet.

**AP-03: Model Supply Chain Relationships and Risks** (v2)
Map supplier network with attributes — capacity, reliability, risk, seasonal constraints.
Deferred: complex modeling; v1 dogfooding is satisfied by AP-01/AP-02/AP-06.

**AP-04: Capture Market Intelligence Over Time** (v2)
Store episodic market observations with temporal context, source attribution,
and trend synthesis. Deferred: depends on AP project having active market activity.

**AP-05: Plan and Track Business Milestones** (v2)
Model milestones with dependency awareness, re-calculate critical paths when
dependencies shift. Deferred: requires mature AP project with multi-month timelines.

**AP-07: Onboard a Collaborator Into the Project Context** (v2)
Generate role-appropriate briefing documents for new collaborators. Deferred: becomes
relevant once AP/RE projects involve more than one person actively.

**RE-02: Track Property Data Across Lifecycle Stages** (v2)
Organise property data by lifecycle stage while maintaining history. Deferred:
requires RE project baseline (RE-01) to complete first.

**RE-03: Capture Stakeholder Relationships and Constraints** (v2)
Map stakeholders with roles, histories, and constraints across properties. Deferred.

**RE-04: Prioritize Digitalization by Impact and Feasibility** (v2)
Evaluate and rank processes for digitalisation priority. Deferred: follows RE-01.

**RE-05: Detect Inconsistencies Across Property Records** (v2)
Automatically detect contradictions, implausible values, and missing links. Deferred.

**RE-07: Generate Reports for Different Audiences** (v2)
Generate audience-appropriate reports from the knowledge base. Deferred.

**XP-02: Maintain Consistent Terminology Across Projects** (post-v1, CANDIDATE)
Detect and resolve terminology collisions across project namespaces.
Status: CANDIDATE — uncertain whether to model as a framework concern vs. a knowledge
organisation convention. Not committed to any stage.

**XP-05: Scale the Knowledge Base Without Degrading Performance** (post-v1, CANDIDATE)
Maintain interactive response times as the knowledge base grows to thousands of atoms.
Status: CANDIDATE — not a v1 blocker; revisit when scale numbers become observable.

**XP-06: Allow Multiple Agents to Work Without Conflicts** (post-v1, CANDIDATE)
Concurrent agent access to the knowledge base without data corruption.
Status: CANDIDATE — v1 is single-agent sequential; true concurrency is post-v1.

### Deprecated

None in this pass. No UCs have been removed; unneeded ones have been deferred to Pending.

---

## Summary Statistics

| Category | Total | ACTIVE (this catalog) | Pending / CANDIDATE |
|---|---|---|---|
| nowu Framework (NF) | 10 | 10 (v1-core: 9, v1.1: 1) | 0 |
| Aperitif Business (AP) | 7 | 3 (v1: 3) | 4 (v2) |
| Real Estate (RE) | 7 | 2 (v1: 2) | 5 (v2) |
| Personal Knowledge (PK) | 6 | 6 (v1-core: 2, v1.1: 4) | 0 |
| Cross-Project (XP) | 7 | 4 (v1-core: 1, v1.1: 2, v2: 1) | 3 (CANDIDATE) |
| **Total** | **37** | **25 ACTIVE** | **12 Pending** |

---

## How to Use This Document

**For the human (you):**
- Review each use case for accuracy and completeness
- Mark which use cases are highest priority for initial development
- Add use cases that are missing — especially edge cases from your real experience
- Challenge the "open questions" — your answers will become ADRs

**For AI agents (nowu-intake, nowu-constraints, nowu-options, nowu-decider, nowu-shaper, nowu-implementer, nowu-reviewer, nowu-curator):**
- Use these use cases as the acceptance criteria source for all framework work
- Every feature, task spec (S5), and decision record (S4) must reference the use case IDs it satisfies
- When scoping work (S5 Shaping), populate the `validation_trace` field with use case IDs
- When reviewing (S8), verify the chain: code → test → AC → use_case — no link may be broken
- When in doubt about scope, the use case boundaries define what's in and what's out

**For the nowu framework itself:**
- This document is a living artifact — updated whenever the vision or plan changes
- UC IDs (NF-01, AP-03, etc.) are referenced in decision records, task definitions, and test names
- `stage_target` is the single authoritative field for sequencing scope questions at P4/S1
- The "open questions" are a backlog of design decisions that need ADRs

---

*37 use cases across 5 categories. 25 ACTIVE, 12 Pending. Solution-agnostic where possible.
Anchored to vision v2.0, compound progress, continuity layer, and the multi-project human.*

***
Human next steps:

1. Review `docs/USE_CASES.proposed.md` against `docs/USE_CASES.md`.
2. Pay particular attention to:
   - NF-10 (new) — does it describe the right job-to-be-done for the multi-project human?
   - UC demotion choices (AP-03/04/05/07, RE-02–05/07) — does the v1 dogfooding scope feel right?
   - Stage targets on PK-01 and XP-01 (both promoted to v1-core) — agree?
3. If changes look correct, replace the canonical file:
   - Overwrite `docs/USE_CASES.md` with this content.
   - Remove `docs/USE_CASES.proposed.md`.
4. Commit with a message like:
   `chore: refresh use cases catalog v2.0 (NF-10 added, stage_target for all UCs)`
