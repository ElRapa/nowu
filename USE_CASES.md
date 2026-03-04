# nowu Framework — Use Cases & Requirements

**Date**: 2026-03-04  
**Purpose**: Define what nowu must be able to support — across all projects and project types — so that AI agents and humans can develop against a shared target.  
**Principle**: Use cases describe *what needs to happen*, not *how*. Implementation details are deliberately omitted unless they constrain the problem space.

---

## How to Read This Document

Each use case follows this structure:

| Field | Meaning |
|---|---|
| **ID** | Stable identifier (e.g., `NF-03`) for referencing in tasks, ADRs, tests |
| **Title** | One-line name |
| **Actor** | Who or what triggers/participates (Human, Agent, Curator, System) |
| **Situation** | The context in which this need arises — the "when" |
| **Need** | What the actor needs to accomplish — the "what" |
| **Success looks like** | Observable outcomes that confirm the need was met |
| **Failure looks like** | What happens if nowu can't handle this — why it matters |
| **Open questions** | Unresolved design tensions. These are intentionally left open. |

### Project Key

| Code | Project |
|---|---|
| **NF** | nowu Framework (self-development, meta) |
| **AP** | Filipino Aperitif & Pili-Nut Business |
| **RE** | Real-Estate Business Digitalization |
| **PK** | Personal Knowledge Management |
| **XP** | Cross-Project & Framework-Level |

---

## A. nowu Framework — Self-Development & Meta

These use cases describe what nowu needs to support *its own development*. Since nowu eats its own dog food, these are the first use cases it must satisfy.

---

### NF-01: Resume Work After Context Loss

| Field | Detail |
|---|---|
| **Actor** | Agent (any of the four: Framer, Shaper, Implementer, Reviewer) |
| **Situation** | A new session starts. The previous session ended mid-task â€” possibly abruptly (token limit, crash, human walked away). The agent has no memory of what happened. |
| **Need** | Reconstruct enough context to continue productive work without re-doing completed steps or asking the human to repeat themselves. |
| **Success looks like** | Agent reads persisted state, identifies the last verified checkpoint, and proposes the correct next action within the first response â€” without hallucinating progress that didn't happen. |
| **Failure looks like** | Agent starts over from scratch, contradicts previous decisions, or claims work is done that was never completed. Human loses trust and begins micromanaging. |
| **Open questions** | How much context is "enough"? Should recovery be automatic or should the agent present a recovery plan for human approval? What's the minimum viable state that must survive a crash? |

---

### NF-02: Track and Enforce Architectural Decisions

| Field | Detail |
|---|---|
| **Actor** | Reviewer Agent; also Implementer Agent (as constrained party) |
| **Situation** | The team (human + agents) has made design decisions over time (e.g., "use SQLite not Postgres", "JSON as source of truth", "no circular imports"). These decisions accumulate. New code is being written. |
| **Need** | Decisions must be recorded with rationale, discoverable by any agent working on related code, and enforceable â€” violations should be caught before merge. |
| **Success looks like** | When an Implementer generates code that violates an ADR, the Reviewer flags the specific violation and references the original decision. The Implementer either fixes the code or proposes an ADR amendment. |
| **Failure looks like** | Architectural drift accumulates silently. Six weeks later, the codebase is internally contradictory and nobody remembers why anything was chosen. |
| **Open questions** | Should ADRs be machine-parseable (structured) or natural language? Can agents propose ADR amendments autonomously, or must a human approve all changes to architectural decisions? |

---

### NF-03: Scope a Piece of Work Without Scope Creep

| Field | Detail |
|---|---|
| **Actor** | Shaper Agent; Human (as approver) |
| **Situation** | A raw idea exists ("add semantic search to the CLI"). It needs to become a bounded set of tasks that an Implementer can complete without spiraling into adjacent concerns. |
| **Need** | Transform the idea into 3â€“7 tasks with explicit boundaries: what's in scope, what's explicitly out, what the acceptance criteria are, and what other work this depends on or blocks. |
| **Success looks like** | Each task can be completed in < 4 hours of agent work. Scope boundaries prevent touching unrelated modules. The Implementer never needs to ask "should I also do X?" because the boundary already says no. |
| **Failure looks like** | A task balloons from "add a CLI flag" into "refactor the entire search module." Or: tasks are so vague that two agents produce conflicting implementations. |
| **Open questions** | How granular should boundaries be â€” file-level? Module-level? Function-level? Should the Shaper have access to the codebase structure to inform scoping, or should it work purely from the problem description? |

---

### NF-04: Self-Assess Quality Without Human Intervention

| Field | Detail |
|---|---|
| **Actor** | Implementer Agent; Reviewer Agent |
| **Situation** | The Implementer has written code and claims it's done. Before requesting human review, the system needs to verify the claim. |
| **Need** | Automatically verify that: tests pass, coverage meets threshold, the code compiles/runs, and the output matches the acceptance criteria from the task spec â€” without relying on the agent's self-report. |
| **Success looks like** | The Verify Before Reporting (VBR) protocol runs actual tests in a sandbox. Only verified-passing work reaches the human review queue. False "done" claims are caught and recycled back to the Implementer. |
| **Failure looks like** | Agents claim tasks are complete based on their own assessment. Human discovers broken code during batch review. Trust erodes. Review becomes a bottleneck instead of a gate. |
| **Open questions** | What verification is feasible for non-code tasks (documentation, architecture diagrams, research)? How do we handle flaky tests vs. genuine failures? |

---

### NF-05: Route Approvals Without Blocking Progress

| Field | Detail |
|---|---|
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
| **Actor** | Learner Agent (or Orchestrator with learning capability) |
| **Situation** | A pattern emerges: the same type of bug keeps being introduced, or the same scoping mistake keeps being made, or a particular approach to a problem class keeps failing on first attempt. |
| **Need** | Detect recurring patterns in session logs, code review feedback, and task outcomes. Surface them as "lessons learned" that actively influence future agent behavior â€” not just passive documentation. |
| **Success looks like** | After the third time a date-parsing bug appears, the Implementer proactively adds timezone-aware handling before being told. After two failed scoping attempts on UI tasks, the Shaper adjusts its task size heuristic. |
| **Failure looks like** | The same mistakes repeat indefinitely. Session logs grow but are never analyzed. The framework gets "more documented" but not "smarter." |
| **Open questions** | How do we distinguish a genuine pattern from coincidence (minimum occurrences)? Should lessons feed into prompts, into constraints, or into both? How do we prevent "over-learning" from a small sample? |

---

### NF-07: Bootstrap a New Project Using the Framework

| Field | Detail |
|---|---|
| **Actor** | Human (initiating); Orchestrator Agent (executing) |
| **Situation** | The human wants to start a new project (e.g., the aperitif business). The nowu framework is already operational for its own development. Now it needs to be applied to a completely different domain. |
| **Need** | Create the project scaffolding (directory structure, initial artifacts, project identity) and configure the agents to operate within that project's context â€” without contaminating the framework's own development state. |
| **Success looks like** | After a single command or conversation, the new project has its own memory space, its own decision journal, and agents can begin framing the first idea â€” all while the framework's own development continues independently in its own context. |
| **Failure looks like** | Framework state and project state bleed into each other. An agent working on the aperitif project accidentally modifies framework code. Or: bootstrapping a new project requires manual setup that takes hours. |
| **Open questions** | Should each project be a separate repository, a separate branch, or a separate directory within the same repo? How much of the framework's own configuration (agent definitions, approval tiers) should be inherited vs. customized per project? |

---

### NF-08: Measure and Visualize Framework Health

| Field | Detail |
|---|---|
| **Actor** | Orchestrator Agent (automated); Human (reviewing) |
| **Situation** | The framework has been running for several weeks across multiple projects. The human wants to know: Is it actually working? Is quality improving? Are agents productive? |
| **Need** | Collect and surface health metrics: task completion velocity, test coverage trend, decision documentation coverage, approval latency, memory integrity, agent loop frequency, recurring failure patterns. |
| **Success looks like** | A weekly health report shows trends over time. The human can spot problems (declining velocity, rising loop frequency) before they become crises. The report is generated by agents, not manually compiled. |
| **Failure looks like** | The framework "feels" productive but nobody knows if quality is actually improving. Problems are discovered retroactively when something breaks in production. |
| **Open questions** | What's the minimum set of health metrics that's actually actionable (avoid dashboard overload)? Should health reports trigger automatic interventions (e.g., pause work if coverage drops below threshold)? |

---

## B. Filipino Aperitif & Pili-Nut Business

These use cases describe what nowu must support for managing a real-world food & beverage product business, from concept to market.

---

### AP-01: Track Regulatory Requirements as Living Knowledge

| Field | Detail |
|---|---|
| **Actor** | Human (researcher); Agent (tracker) |
| **Situation** | Launching a food/beverage product in the Philippines requires navigating multiple regulatory bodies: FDA (License to Operate, Certificate of Product Registration), DTI/SEC registration, BIR tax compliance, local government permits (barangay clearance, mayor's permit, sanitary permit), plus excise tax requirements for alcoholic beverages. Requirements change, have dependencies, and have deadlines. |
| **Need** | Capture each regulatory requirement as a piece of knowledge with its source, confidence level, dependencies on other requirements, and status. Surface what's blocking what. Alert when something may have changed or expired. |
| **Success looks like** | At any point, the human can ask "what do I still need to do to legally sell this product?" and get an accurate, dependency-ordered answer that reflects the current state â€” including which permits depend on which other permits being obtained first. |
| **Failure looks like** | Requirements are scattered across notes, bookmarks, and memory. A critical dependency is missed (e.g., you need the FDA LTO before you can get the CPR). The product launch is delayed by months because of a forgotten permit. |
| **Open questions** | How should nowu handle regulatory requirements that are "probably still current" but haven't been verified recently? Should there be automatic reminders for permit renewals? How to handle conflicting information from different government sources? |

---

### AP-02: Manage Product Formulation as Versioned Knowledge

| Field | Detail |
|---|---|
| **Actor** | Human (formulator); Agent (recorder, searcher) |
| **Situation** | The aperitif recipe evolves through experimentation. Each version has specific ingredient ratios, process steps, taste notes, shelf-life observations, and cost implications. Some versions are abandoned, some are promising, and one becomes the production recipe. The pili-nut component has its own versioning (roasting profiles, oil extraction methods). |
| **Need** | Record each formulation version with its parameters, link it to taste test results and cost analysis, track why versions were abandoned or selected, and make it easy to compare versions or revisit abandoned approaches when new information arrives. |
| **Success looks like** | When the human asks "why did we abandon version 3?" the system returns the decision with rationale. When ingredient costs change, the system can show which formulations are affected. When a new pili-nut processing technique emerges, it surfaces the abandoned versions that failed specifically due to the old technique. |
| **Failure looks like** | Recipes exist as notes in a phone, a notebook, and a spreadsheet. Version history is lost. The human re-tests a formulation that was already proven to fail. Or: the winning recipe's rationale is forgotten, making it impossible to adapt when ingredients change. |
| **Open questions** | Should formulation data be structured (key-value) or narrative? How detailed should process steps be (reproducibility vs. documentation burden)? Should the system support multimedia (photos of results, taste test recordings)? |

---

### AP-03: Model Supply Chain Relationships and Risks

| Field | Detail |
|---|---|
| **Actor** | Human (business planner); Agent (analyst) |
| **Situation** | The business depends on multiple supply relationships: coconut suppliers (potentially from the human's own plantation in Camarines Sur), pili-nut sources (Bicol region), packaging suppliers, distribution partners. Each has capacity, reliability, cost, and lead time characteristics. Some are seasonal. |
| **Need** | Map the supply chain as a network of relationships with attributes. Identify single points of failure. Track supplier performance over time. Surface risks (e.g., "if typhoon season disrupts Bicol transport, which ingredients are affected and what's the backup?"). |
| **Success looks like** | Before scaling production, the system can answer: "What's the maximum monthly output given current supplier capacity?" and "Which supplier relationship is the weakest link?" When the human evaluates a new supplier, the system shows where they fit in the existing network. |
| **Failure looks like** | A key supplier fails and there's no backup identified. Production scales but a bottleneck in one input (e.g., pili-nut kernel availability is seasonal) is discovered too late. Costs spiral because supplier alternatives weren't evaluated when negotiating position was strong. |
| **Open questions** | How much supply chain data should be modeled in nowu vs. in a dedicated supply chain tool? What level of supplier detail is worth maintaining for an early-stage business? |

---

### AP-04: Capture Market Intelligence Over Time

| Field | Detail |
|---|---|
| **Actor** | Human (researcher); Agent (collector, synthesizer) |
| **Situation** | The aperitif market in the Philippines is evolving. Competitor products appear and disappear. Consumer preferences shift. The human gathers intelligence from multiple sources: store visits, social media, industry reports, conversations, trade shows. This intelligence is episodic and arrives in fragments over months. |
| **Need** | Store market observations with temporal context (when was this observed?), source attribution (how reliable?), and connections to business decisions. Over time, synthesize fragments into trends. Distinguish between confirmed facts, anecdotes, and hypotheses. |
| **Success looks like** | After 6 months of fragments, the human asks "what do we know about our target customer?" and gets a synthesized view that distinguishes well-supported claims from thin evidence. When a competitor launches a new product, the system connects it to earlier observations about that competitor. |
| **Failure looks like** | Intelligence is captured in chat logs and forgotten. A critical market shift is noticed too late. Or: fragments are treated with equal weight â€” an offhand comment at a party carries the same authority as a published industry report. |
| **Open questions** | How should ephemeral observations (a conversation at a store) be distinguished from durable intelligence (an industry report)? Should the system suggest when intelligence is getting stale and needs refreshing? |

---

### AP-05: Plan and Track Business Milestones

| Field | Detail |
|---|---|
| **Actor** | Human (founder); Agent (planner, tracker) |
| **Situation** | The business has major milestones: formulation finalized, permits obtained, first production batch, first sale, break-even. These milestones have dependencies (can't do first production without permits and finalized recipe). The timeline is long (months to years) and frequently shifts. |
| **Need** | Represent milestones with their dependencies, track progress toward each, and re-calculate timelines when dependencies shift. Surface what's actually on the critical path vs. what feels urgent but isn't blocking. |
| **Success looks like** | When the FDA LTO application is delayed by 3 weeks, the system automatically shows the cascade effect on downstream milestones and identifies which parallel work can continue unaffected. |
| **Failure looks like** | The human works on whatever feels most urgent rather than what's actually blocking. Milestones are tracked in a list without dependency awareness. A 3-week delay in one permit turns into a 3-month delay because parallel work wasn't identified. |
| **Open questions** | Is this a Gantt-chart problem, a knowledge-graph problem, or both? How much schedule management should nowu own vs. defer to dedicated PM tools? Should milestones auto-decompose into tasks? |

---

### AP-06: Evaluate a Business Decision With Traceability

| Field | Detail |
|---|---|
| **Actor** | Human (decision-maker); Agent (analyst, recorder) |
| **Situation** | The human faces a business decision: Should we use glass bottles or pouches for the first production run? There are cost, branding, regulatory, and supply chain implications. The human wants to think through the decision systematically and be able to revisit the reasoning later. |
| **Need** | Structure the decision: what are the options, what criteria matter, what evidence supports each option, what's the recommendation, what's the chosen path and why. Store the decision with links to the evidence and rationale so it can be revisited when conditions change. |
| **Success looks like** | Six months later, when considering a packaging change, the human retrieves the original decision, sees that "glass was chosen because of premium positioning and FDA label requirements" and evaluates whether those reasons still hold given new conditions. |
| **Failure looks like** | The decision is made in a conversation and forgotten. When the packaging question comes up again, the entire analysis is repeated from scratch. Or worse: the same decision is revisited repeatedly without remembering the previous conclusions. |
| **Open questions** | Should decision templates be prescriptive (force a structure) or flexible (allow freeform with optional structure)? How do we handle decisions made quickly and informally â€” is there a "lightweight decision" format? |

---

### AP-07: Onboard a Collaborator Into the Project Context

| Field | Detail |
|---|---|
| **Actor** | Human (new collaborator â€” business partner, consultant, supplier); Agent (context builder) |
| **Situation** | A new person joins the aperitif project â€” maybe a food scientist, a regulatory consultant, or a distribution partner. They need to understand the project's current state, key decisions made, and open questions â€” without reading everything. |
| **Need** | Generate a context-appropriate summary of the project state that's tailored to the new collaborator's role. A food scientist needs formulation history and regulatory constraints. A distribution partner needs product specs and timeline. Neither needs the full decision log. |
| **Success looks like** | The system generates a role-specific briefing document in minutes that's accurate, current, and doesn't expose irrelevant internal deliberations. The new collaborator is productive in their domain immediately. |
| **Failure looks like** | Onboarding takes days of 1:1 meetings. Critical context is missed. The new collaborator makes recommendations that contradict decisions they weren't told about. |
| **Open questions** | How should "role" be defined â€” freeform, or from a predefined set? Should certain knowledge be marked as "internal only" vs. "shareable"? How do we handle confidential information in generated briefings? |

---

## C. Real-Estate Business Digitalization

These use cases describe what nowu must support for migrating a traditional, paper-heavy real estate operation into digital workflows.

---

### RE-01: Inventory Existing Processes Before Digitalization

| Field | Detail |
|---|---|
| **Actor** | Human (business analyst); Agent (documenter) |
| **Situation** | The real estate business runs on paper, phone calls, and human memory. Before digitalizing anything, the current processes need to be understood: how are properties listed, how are tenants onboarded, how are contracts managed, how is maintenance tracked? Nobody has documented these processes â€” they exist as institutional knowledge in people's heads. |
| **Need** | Capture each process as a sequence of steps, participants, inputs/outputs, and pain points. Link processes to each other where they share data or handoffs. Identify which processes are highest-value to digitalize first. |
| **Success looks like** | After interviews and observation, the system contains a map of ~10-20 core processes. Each has clear steps, identified bottlenecks, and an estimated digitalization value. The human can prioritize digitalization by actual impact rather than gut feel. |
| **Failure looks like** | Digitalization starts with whatever seems obvious ("let's build a website!") rather than where the actual pain is. Processes are digitalized in isolation, creating new data silos that are worse than the paper originals. |
| **Open questions** | How should informal/ad-hoc processes be captured vs. formal ones? Should the system enforce a process notation (BPMN) or accept natural language? How do we handle processes that vary by property or person? |

---

### RE-02: Track Property Data Across Lifecycle Stages

| Field | Detail |
|---|---|
| **Actor** | Human (property manager); Agent (data steward) |
| **Situation** | A property moves through lifecycle stages: acquisition, renovation, listing, tenant screening, lease execution, ongoing management, maintenance, lease renewal or turnover. At each stage, different data is relevant: title documents, inspection reports, tenant applications, lease terms, maintenance history, payment records. |
| **Need** | Organize property data by lifecycle stage while maintaining the full history. When looking at a property, surface the most relevant information for its current stage while making historical data accessible. Track which data is verified, which is self-reported, and which is estimated. |
| **Success looks like** | When a property enters the "listing" stage, the system surfaces the listing-relevant data (photos, specs, pricing analysis, comparable properties) while flagging gaps (missing inspection report, unverified utility costs). When a maintenance issue arises during tenancy, the full property history including renovation details is accessible. |
| **Failure looks like** | Property data is scattered across filing cabinets, email threads, and spreadsheets. During lease renewal, the original lease terms can't be found. A maintenance issue recurs because the previous repair wasn't documented. |
| **Open questions** | Should properties be first-class entities in nowu, or modeled as a collection of knowledge atoms with connections? How to handle photos, scanned documents, and other non-text data? What about properties that are prospects (not yet acquired)? |

---

### RE-03: Capture Stakeholder Relationships and Constraints

| Field | Detail |
|---|---|
| **Actor** | Human (business owner); Agent (relationship mapper) |
| **Situation** | Real estate involves many stakeholders: property owners, tenants, contractors, local government (permits), brokers, attorneys, banks. Each has their own constraints, preferences, and history. Some relationships span multiple properties. The Filipino real estate market adds specific dynamics: the Real Estate Service Act requires licensed brokers, barangay-level relationships matter for permits, and family/community relationships influence business. |
| **Need** | Map stakeholders with their roles, properties they're associated with, reliability history, and outstanding obligations. Surface relevant relationships when working on a specific property or decision. Track who needs to be consulted or notified for different types of actions. |
| **Success looks like** | When negotiating a lease renewal, the system surfaces: this tenant's payment history, their relationship with the building's maintenance contractor, and the fact that their lease in another property is also up for renewal â€” creating negotiation leverage. |
| **Failure looks like** | A key relationship is forgotten. A contractor who did poor work on one property is unknowingly hired for another. A permit application fails because the relevant barangay contact wasn't engaged. |
| **Open questions** | How to handle sensitive relationship information (personal notes about stakeholders)? Should the system track communication history or just relationships? Where's the line between CRM and knowledge management? |

---

### RE-04: Prioritize Digitalization by Impact and Feasibility

| Field | Detail |
|---|---|
| **Actor** | Human (business owner); Agent (analyst) |
| **Situation** | After inventorying processes (RE-01), the human needs to decide what to digitalize first. Not everything can be done at once. Some processes are high-pain but hard to digitalize (complex, many stakeholders, poor data). Others are low-pain but easy wins. Some have dependencies (can't digitalize rent collection without tenant data). |
| **Need** | Evaluate each process against multiple criteria (pain level, frequency, data readiness, stakeholder buy-in, dependency on other digitalization, estimated effort) and produce a prioritized roadmap. Support re-prioritization as conditions change. |
| **Success looks like** | The first digitalization sprint targets the highest-impact, lowest-risk process. Each subsequent sprint builds on data and infrastructure created by the previous one. Stakeholders see quick wins that build confidence for bigger changes. |
| **Failure looks like** | The most ambitious process is tackled first, takes 6 months, and delivers no visible value. Stakeholder buy-in evaporates. Or: easy wins are done first but they don't connect to each other, creating a patchwork of disconnected digital tools. |
| **Open questions** | Should nowu include a scoring/ranking mechanism, or is this a human judgment call with nowu providing the data? How to handle the political dimension (a powerful stakeholder wants their process digitalized first, even if it's not the highest impact)? |

---

### RE-05: Detect Inconsistencies Across Property Records

| Field | Detail |
|---|---|
| **Actor** | Agent (auditor); Human (reviewer) |
| **Situation** | As paper records are digitalized, inconsistencies emerge: a property's listed area in the title doesn't match the listing, the tenant's lease start date conflicts with the move-in record, or a maintenance report references a unit number that doesn't exist. These inconsistencies may reflect errors in digitalization, errors in the original records, or actual problems that need resolution. |
| **Need** | Automatically detect contradictions, implausible values, and missing links in the knowledge base. Classify each inconsistency by severity (data entry error vs. potential legal issue) and surface them for human resolution. |
| **Success looks like** | A weekly report flags: "Property X has conflicting area measurements: title says 120 sqm, listing says 130 sqm. Confidence: title is the authoritative source." The human reviews and resolves, improving data quality over time. |
| **Failure looks like** | Contradictory records coexist silently. A legal dispute arises and the business can't produce consistent documentation. Or: every inconsistency is flagged with equal urgency, creating alert fatigue. |
| **Open questions** | Which data source should be treated as authoritative when sources conflict (title > inspection > listing > self-reported)? How should resolved inconsistencies be recorded â€” correct the data, or keep both with a resolution note? |

---

### RE-06: Support Long-Term Investment Decision Tracking

| Field | Detail |
|---|---|
| **Actor** | Human (investor/owner); Agent (analyst) |
| **Situation** | Real estate investment decisions play out over years. A decision to acquire a property was based on assumptions about rental yield, appreciation, and renovation costs. Years later, the human wants to evaluate: were those assumptions correct? What can we learn for the next acquisition? |
| **Need** | Record investment theses (assumptions, projections, confidence levels) at decision time, link them to actual outcomes as they materialize, and support retrospective analysis. Enable pattern recognition across multiple properties over time. |
| **Success looks like** | Three years after acquiring Property A, the system shows: "Projected yield: 8%. Actual yield: 6.5%. Primary variance: renovation costs were 40% over estimate (see decision RE-DEC-003). This matches the pattern in Property B and C â€” renovation cost estimates have been systematically low." |
| **Failure looks like** | Investment decisions are made in conversations and forgotten. Performance is tracked in spreadsheets disconnected from the original reasoning. The same estimation mistakes are repeated across properties because nobody connects the pattern. |
| **Open questions** | How to model financial projections as knowledge (structured vs. narrative)? Should the system track actual financial performance, or is that a separate financial tool? How to handle the sensitivity of investment data? |

---

### RE-07: Generate Reports for Different Audiences

| Field | Detail |
|---|---|
| **Actor** | Human (requester); Agent (report generator) |
| **Situation** | Different stakeholders need different views of the same underlying data. A bank needs a property portfolio summary for a loan application. A tax accountant needs income and expense data organized by property and period. A potential buyer needs a property fact sheet. A tenant needs a lease summary. |
| **Need** | Generate audience-appropriate reports from the knowledge base without requiring the human to manually compile data from multiple sources. Reports should reflect the current state of knowledge and flag any data gaps or low-confidence items. |
| **Success looks like** | "Generate a portfolio summary for the bank" produces a document that includes property valuations (with confidence levels), occupancy rates, and income history â€” and flags "Property D valuation is based on 2024 assessment, recommend updating." |
| **Failure looks like** | Each report request triggers a multi-day manual compilation. Data is copied between formats with transcription errors. Stale data is presented as current. |
| **Open questions** | Should report templates be pre-defined or generated dynamically? How to handle data that's in the knowledge base but at low confidence â€” include it with a caveat, or omit it? What output formats matter (PDF, spreadsheet, narrative, structured data)? |

---

## D. Personal Knowledge Management

These use cases describe what nowu must support for the human's personal knowledge â€” the foundation layer beneath all projects.

---

### PK-01: Capture a Thought Before It's Lost

| Field | Detail |
|---|---|
| **Actor** | Human |
| **Situation** | The human has a thought â€” at 11 PM, during a commute, in the middle of a conversation. It might be an idea for the aperitif business, a reminder to buy something tomorrow, a fragment of a conversation worth remembering, or a connection between two previously unrelated things. The capture moment is brief. |
| **Need** | Record the thought with minimal friction (a few words, a voice note, a quick type). The system should handle the categorization, linking, and enrichment later â€” not at capture time. The thought should not be lost even if it's not yet organized. |
| **Success looks like** | The next morning, the human's captured thoughts are organized by likely project, tagged with suggested connections to existing knowledge, and surfaced in the relevant context (the grocery reminder shows up in "today", the business idea shows up in the aperitif project inbox). |
| **Failure looks like** | Capturing a thought requires choosing a project, a type, tags, and a confidence level. The friction is so high that the human reverts to a paper napkin. The system has perfect metadata but nobody uses it. |
| **Open questions** | What's the minimum viable capture format? Should auto-categorization happen immediately or in batch? How do we handle truly miscellaneous thoughts that don't belong to any project? |

---

### PK-02: Surface Relevant Knowledge Without Being Asked

| Field | Detail |
|---|---|
| **Actor** | System (proactive); Human (recipient) |
| **Situation** | The human is working on the aperitif project â€” specifically on packaging. They don't realize that three weeks ago, during real-estate research, they captured a note about a packaging supplier they encountered. Or: they're reading about coconut processing and don't connect it to the supply chain analysis they did for a different project. |
| **Need** | When the human is working in a specific context, proactively surface knowledge from other projects or past captures that is semantically relevant â€” without overwhelming them with noise. |
| **Success looks like** | While working on AP packaging decisions, the system gently surfaces: "You noted a packaging contact during RE research on Feb 12 â€” possibly relevant?" The human either links it (valuable discovery) or dismisses it (low cost). |
| **Failure looks like** | Either: nothing is ever surfaced (missed connections accumulate) OR everything even vaguely related is surfaced (the system becomes annoying and is ignored). |
| **Open questions** | What threshold of relevance justifies interrupting the human's focus? Should surfacing be pull (human asks "what else do I know about this?") or push (system proactively suggests)? How do we measure if cross-pollination is actually valuable? |

---

### PK-03: Maintain a "Today" View Across All Projects

| Field | Detail |
|---|---|
| **Actor** | Human |
| **Situation** | The human wears multiple hats: framework developer, business founder, property manager, person who needs groceries. Each morning, they need to know: what's due today? What's overdue? What's the most important thing to focus on? This requires pulling from multiple projects and personal reminders. |
| **Need** | A unified daily view that aggregates tasks, reminders, and upcoming deadlines across all projects and personal knowledge. Sorted by actual urgency and importance, not just by project. Able to distinguish "buy groceries" (low importance, time-sensitive) from "FDA application deadline" (high importance, time-sensitive). |
| **Success looks like** | The human starts the day with a single view showing 3-5 focus items and 10-15 background items. The focus items are genuinely the most important things to do today. The view adapts as items are completed. |
| **Failure looks like** | The human checks 4 different systems (project boards, to-do lists, calendar, notes) to assemble their own daily plan. Important items from one project are eclipsed by urgent-but-unimportant items from another. |
| **Open questions** | How should importance be calculated across different projects (is an aperitif FDA deadline more important than a framework milestone)? Should the daily view be generated by an agent or computed from structured data? How to handle items without explicit due dates? |

---

### PK-04: Let Knowledge Decay and Clean Up Gracefully

| Field | Detail |
|---|---|
| **Actor** | Curator (automated); Human (reviewer) |
| **Situation** | Over months, the knowledge base accumulates: old grocery lists, superseded decisions, market intelligence about a product that was abandoned, regulatory information that may have changed, and notes that seemed important at the time but never connected to anything. |
| **Need** | Periodically review knowledge for staleness, obsolescence, and irrelevance. Identify candidates for archival or deletion. Flag high-importance knowledge that hasn't been verified in a long time. Handle the distinction between "this is old and probably still true" (Bicol grows pili nuts) vs. "this is old and probably wrong now" (competitor X's pricing from 18 months ago). |
| **Success looks like** | Monthly, the Curator surfaces: 15 items recommended for archival (no connections, no access, low importance), 3 items flagged for re-verification (high importance but stale), 1 contradiction detected between two high-confidence items. The human reviews in 10 minutes. |
| **Failure looks like** | The knowledge base grows indefinitely. Search results are polluted with stale information. The human stops trusting the system because outdated information is surfaced alongside current information. Or: aggressive cleanup deletes something that turns out to be needed. |
| **Open questions** | Should archived knowledge be searchable or hidden? How do we distinguish "timeless" knowledge from "time-sensitive" knowledge without requiring the human to classify everything? What's the cost of a false deletion vs. the cost of eternal accumulation? |

---

### PK-05: Build Understanding Incrementally Over a Topic

| Field | Detail |
|---|---|
| **Actor** | Human (learner); Agent (synthesizer) |
| **Situation** | The human is learning about something over time: Philippine excise tax law, pili-nut processing techniques, property valuation methods, or a new programming framework. Knowledge arrives in fragments across days or weeks â€” an article here, a conversation there, a practical experiment. |
| **Need** | Assemble fragments into an evolving understanding. Track what's well-understood vs. what has gaps. When new information arrives, integrate it with existing understanding â€” especially when it contradicts or refines what was previously known. |
| **Success looks like** | After reading 5 articles about excise tax over 3 weeks, the human asks "summarize what I know about excise tax for coconut-based spirits" and gets a coherent synthesis that includes confidence levels ("the base rate is P8/proof liter â€” well established" vs. "annual escalation schedule â€” needs verification, sources disagree"). |
| **Failure looks like** | Each article is stored as a separate note with no synthesis. The human has 5 notes about excise tax but can't answer a basic question about it without re-reading all of them. New information doesn't update old understanding â€” both coexist without resolution. |
| **Open questions** | Should synthesis be automatic or human-triggered? How to handle contradictions between sources of similar authority? Should the system track the human's confidence separately from the source's reliability? |

---

### PK-06: Protect Sensitive Personal Knowledge

| Field | Detail |
|---|---|
| **Actor** | Human (owner); System (access control) |
| **Situation** | The knowledge base contains information of varying sensitivity: public (product specs), internal (business strategy), personal (financial information, health notes, relationship observations), and confidential (legal documents, investment details). Some of this knowledge may be shared with collaborators, agents, or used to generate reports. |
| **Need** | Control what knowledge is accessible in which context. Prevent sensitive personal knowledge from leaking into generated reports, shared briefings, or agent-generated outputs. Allow the human to classify sensitivity without requiring it for every item. |
| **Success looks like** | When generating a briefing for a business partner (AP-07), the system automatically excludes personal financial notes, internal competitive analysis, and real-estate investment details â€” even though they're in the same knowledge base. |
| **Failure looks like** | A generated report includes a personal note about a business partner. Or: the sensitivity system is so restrictive that agents can't access the knowledge they need to be useful. Or: everything defaults to "sensitive" and nothing is ever shared. |
| **Open questions** | Should sensitivity be per-atom, per-project, or per-tag? What are the default sensitivity levels? How should agents handle knowledge they can "see" exists but can't "read" due to sensitivity? |

---

## E. Cross-Project & Framework-Level

These use cases describe capabilities that span multiple projects or operate at the framework level.

---

### XP-01: Discover Connections Across Projects Automatically

| Field | Detail |
|---|---|
| **Actor** | System (semantic search); Human (evaluator) |
| **Situation** | The human's coconut plantation (real-estate project) is also a potential supply source for the aperitif business. A regulatory insight from the food business might apply to property documentation requirements. A technical pattern learned while building the framework might solve a problem in the real-estate digitalization project. These connections aren't explicitly created â€” they emerge from overlapping knowledge. |
| **Need** | When working in one project's context, discover and surface relevant knowledge from other projects based on semantic similarity, shared entities, or shared concepts â€” without requiring the human to manually link everything. |
| **Success looks like** | While planning the aperitif supply chain, the system surfaces the coconut plantation property from the real-estate project as a potential supplier â€” based on the semantic connection between "coconut supply" and "2-hectare coconut plantation in Camarines Sur." |
| **Failure looks like** | Projects exist in complete isolation. The human manually cross-references by memory. Obvious connections are missed. Or: every search returns results from every project, making project boundaries meaningless. |
| **Open questions** | How should cross-project discovery be balanced against project focus (too much cross-pollination is distracting)? Should cross-project connections be explicit (create a link) or implicit (just surface in search)? How to handle conflicting knowledge across projects? |

---

### XP-02: Maintain Consistent Terminology Across Projects

| Field | Detail |
|---|---|
| **Actor** | Agent (terminology tracker); Human (disambiguator) |
| **Situation** | The same concept may be called different things in different projects, or different concepts may share a name. "Property" means a real-estate asset in RE but a code attribute in NF. "LTO" could be FDA License to Operate or a long-term objective. "Batch" means a production run in AP but a review batch in NF. |
| **Need** | Detect terminology collisions and ambiguities. Maintain a per-project glossary or namespace. When searching across projects, disambiguate terms or present results with context. |
| **Success looks like** | Searching for "property" within the RE project returns real-estate assets. Searching across all projects flags the ambiguity and presents grouped results. When an agent generates a cross-project report, it uses unambiguous terminology. |
| **Failure looks like** | A cross-project search for "LTO" returns FDA licensing information when the human wanted framework objectives, or vice versa. An agent confuses code "properties" with real-estate "properties" and generates nonsensical output. |
| **Open questions** | Should disambiguation be automated or require human input? Is a global glossary practical, or should each project have its own namespace? How should agents handle ambiguity when the human hasn't clarified? |

---

### XP-03: Transfer Lessons Learned Between Projects

| Field | Detail |
|---|---|
| **Actor** | Learner Agent; Human (evaluator) |
| **Situation** | A process improvement discovered while building the framework (e.g., "tasks scoped to < 4 hours are 3x more likely to succeed") might apply to digitalization task planning. A vendor evaluation technique used for the aperitif business might work for selecting real-estate technology partners. |
| **Need** | When a lesson is learned in one project, evaluate whether it generalizes to other projects. If it does, surface it as a recommendation â€” not an automatic change â€” in the relevant project context. |
| **Success looks like** | After discovering that "tasks > 4 hours fail 60% of the time" in the framework project, the system flags 3 tasks in the real-estate project that exceed 4 hours and suggests decomposition. The human evaluates whether the pattern transfers to a different domain. |
| **Failure looks like** | Each project learns its own lessons in isolation. The same mistake is made independently in each project. Or: a lesson from one domain is applied blindly to another where it doesn't fit (e.g., "automated testing" lessons applied to paper-to-digital migration where testing means something different). |
| **Open questions** | What makes a lesson "transferable" vs. "domain-specific"? Should transferred lessons carry lower confidence than native ones? How to prevent a lesson from one small project from inappropriately influencing a larger one? |

---

### XP-04: Handle Conflicting High-Confidence Knowledge

| Field | Detail |
|---|---|
| **Actor** | Curator (detector); Human (resolver) |
| **Situation** | Two pieces of knowledge exist with high confidence but contradict each other. Perhaps: an older verified fact ("excise tax on coconut spirits is P8/proof liter") conflicts with newer information ("the 2025 tax reform changed the rate to P12/proof liter"). Or: two sources with similar authority disagree about a pili-nut processing parameter. |
| **Need** | Detect the contradiction, present both pieces of knowledge with their provenance and timestamps, and escalate to the human for resolution â€” especially when the contradicting items are both high-confidence or when downstream decisions depend on the resolution. |
| **Success looks like** | The system flags: "CONFLICT: Atom #A says excise tax is P8/proof liter (grade 5, verified 2025-01). Atom #B says it's P12/proof liter (grade 4, captured 2025-11). Atom #A is linked to 3 cost calculations. Resolution needed â€” which is current?" The human resolves, the old fact is marked as superseded, and the cost calculations are flagged for update. |
| **Failure looks like** | Both facts coexist. An agent uses the stale one for a cost calculation. The business plan is based on the wrong tax rate. Nobody notices until the first tax filing. |
| **Open questions** | Should conflict detection run continuously or periodically? How to handle "soft" contradictions (values that are close but not identical) vs. "hard" contradictions (mutually exclusive claims)? What happens when neither the human nor the agent can determine which is correct? |

---

### XP-05: Scale the Knowledge Base Without Degrading Performance

| Field | Detail |
|---|---|
| **Actor** | System (infrastructure); Human (user experiencing performance) |
| **Situation** | The knowledge base starts small (dozens of atoms). Over months it grows to thousands. Multiple projects contribute. Connections multiply. The search index, importance scoring, and cross-project discovery all need to keep working at interactive speed. |
| **Need** | Maintain sub-200ms response times for common operations (search, retrieve, connect) as the knowledge base scales. Degrade gracefully if performance thresholds are exceeded. Provide visibility into what's causing slowdowns. |
| **Success looks like** | At 10,000 atoms with 50,000 connections across 5 projects, search still returns in < 200ms. The human never waits. If semantic search is slow, exact and fuzzy search still respond instantly while semantic processes in background. |
| **Failure looks like** | After a few months, search becomes noticeably slow. The human starts using external tools to search their own knowledge base. Performance degrades silently until the system becomes unusable. |
| **Open questions** | What's the realistic scale target for a personal knowledge base (10K atoms? 100K?)? Should old/decayed atoms be moved to cold storage? Is the current SQLite + JSON architecture sufficient at scale, or is there a known ceiling? |

---

### XP-06: Allow Multiple Agents to Work Without Conflicts

| Field | Detail |
|---|---|
| **Actor** | Multiple agents operating concurrently; Orchestrator (coordinator) |
| **Situation** | The Implementer is working on framework code while the Framer is analyzing a new aperitif business idea and the Curator is running a weekly knowledge review. All three access the same knowledge base. The Implementer is creating new knowledge atoms. The Curator might archive or flag atoms the Framer is referencing. |
| **Need** | Concurrent access without data corruption or stale reads. Agents should not block each other unless they're modifying the same data. Conflicts should be detected and resolved, not silently dropped. |
| **Success looks like** | All three agents operate independently. The Curator flags an atom for archival that the Framer just referenced â€” the system detects the conflict and defers archival with a note: "Atom #X was referenced by Framer 2 minutes ago, deferring cleanup." |
| **Failure looks like** | Database locks cause agents to timeout. Or: the Curator archives an atom mid-reference, causing the Framer to error. Or: two agents create contradictory knowledge atoms because they don't see each other's in-progress work. |
| **Open questions** | Is true concurrency needed, or can agents take turns with short execution windows? How should write conflicts be resolved â€” last-write-wins, or merge? Should agents declare "intent" before modifying shared state? |

---

### XP-07: Adapt the Framework to a New Domain Without Rewriting

| Field | Detail |
|---|---|
| **Actor** | Human (new domain); System (framework) |
| **Situation** | After succeeding with the three initial projects, the human wants to apply nowu to a completely new domain: maybe learning a language, planning a community event, or helping a friend organize their business. The new domain has different knowledge types, different rhythms, and different importance criteria than the existing projects. |
| **Need** | The framework should accommodate new domains without requiring changes to core code. Knowledge types, connection types, approval tiers, and agent behaviors should be configurable or extensible per project. The core should remain stable while the periphery adapts. |
| **Success looks like** | Adding a "language learning" project requires: creating the project, optionally defining a few custom knowledge types ("vocabulary", "grammar rule", "practice observation"), and starting to capture knowledge. No code changes. No migration. The existing projects are unaffected. |
| **Failure looks like** | Every new domain requires modifying the schema, adding database columns, or changing agent behavior. The framework becomes rigid â€” optimized for its original three projects but hostile to new ones. |
| **Open questions** | How much domain-specific configuration should be allowed vs. how much should be handled by the generic knowledge model? Should custom knowledge types be true schema extensions or just tags/conventions? Where's the line between "flexible enough" and "so flexible it's meaningless"? |

---

## Summary Statistics

| Category | Count | Coverage Focus |
|---|---|---|
| nowu Framework (NF) | 8 | Self-development, quality, learning, bootstrapping, health |
| Aperitif Business (AP) | 7 | Regulatory, formulation, supply chain, market, decisions, collaboration |
| Real Estate (RE) | 7 | Process inventory, property lifecycle, stakeholders, digitalization planning, data quality |
| Personal Knowledge (PK) | 6 | Capture, surfacing, daily view, decay, incremental learning, privacy |
| Cross-Project (XP) | 7 | Discovery, terminology, lesson transfer, conflicts, scale, concurrency, extensibility |
| **Total** | **35** | |

---

## How to Use This Document

**For the human (you):**
- Review each use case for accuracy and completeness
- Mark which use cases are highest priority for initial development
- Add use cases that are missing â€” especially edge cases from your real experience
- Challenge the "open questions" â€” your answers will become ADRs

**For AI agents (Framer, Shaper, Implementer, Reviewer):**
- Use these use cases as the acceptance criteria source for all framework work
- Every feature should map to one or more use case IDs
- When scoping work, reference the relevant use case IDs in task definitions
- When reviewing code, check: "Does this actually serve a documented use case?"
- When in doubt about scope, the use case boundaries define what's in and what's out

**For the nowu framework itself:**
- This document is a living artifact â€” it should be updated as new use cases emerge from real usage
- Use case IDs (NF-01, AP-03, etc.) should be referenced in decision records, task definitions, and test names
- The "open questions" are a backlog of design decisions that need ADRs

---

*35 use cases across 5 categories. Solution-agnostic where possible. Broad enough to guide without constraining. Specific enough to test against.*