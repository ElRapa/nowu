---
id: epic-v1core-002
source_problem: problem-002, problem-003, problem-004
created: 2026-04-08
status: APPROVED
agent_version: story-mapper@2.3 (enriched)
parent_goal: goal-002
generated_at: 2026-04-08T00:00:00Z
---

# Epic: epic-v1core-002 — Building Trust: Decision Memory & Pipeline Quality

## Epic Summary

This epic delivers the mechanisms that make the workflow trustworthy: every significant decision is generated with visible alternatives and preserved with full traceable reasoning; every task is explicitly bounded before execution begins; every piece of finished work is independently verified before reaching the human; and recurring failure patterns are detected and fed back so the framework improves cycle over cycle. Taken together, these capabilities make a 90–99% AI-handled workflow safe to trust rather than dangerous to delegate to.

This epic is the v1-core probe of Discovery Theme 2 (Decision Memory & Traceable Reasoning) and Theme 4 (Knowledge That Compounds Across Projects) and directly supports the 6‑month vision claim that “the AI carries the full cycle… with 90–99% of the work handled by AI” without becoming a black box. It is how you go from “AI can do the work” to “I still trust my own past reasoning six months later and can safely delegate execution.”

## Vision & Discovery Alignment

- Vision (6 months): “The AI carries the full cycle… with 90–99% of the work handled by AI… the experience is genuinely enjoyable, low friction, clear feedback, visible progress.” This epic provides the decision and pipeline checks that make that level of delegation feel safe, not reckless.  
- Vision (Guiding Principles): “Decisions are provisional and traceable”; “Multiple options before a decision”; “The system learns by running.” NF‑02, NF‑13, NF‑06, and NF‑09 slices in this epic are the concrete expressions of those principles in v1-core.  
- Discovery Theme 2 (Decision Memory and Traceable Reasoning): Addressed by NF‑02 and NF‑13 plus the decision recording and enforcement stories.  
- Discovery Theme 4 (Knowledge That Compounds Across Projects): Addressed indirectly by NF‑06 and NF‑09: lessons and traces from one project can be reused in another once they are atoms in the knowledge layer.  
- Discovery Theme 5 (Unified Daily Orientation): Supported by ensuring that what shows up in orientation / today views is backed by decisions and traceable work, not opaque agent behavior.

## Use Case Mapping

| UC-ID | Description | Covered by |
|---|---|---|
| NF-02 | Track and Enforce Architectural Decisions | story-v1core-002-s001, story-v1core-002-s002 |
| NF-13 | Generate Multiple Options at Decision Point | story-v1core-002-s001 |
| NF-03 | Scope a Piece of Work Without Scope Creep | story-v1core-002-s003 |
| NF-04 | Self-Assess Quality Without Human Intervention | story-v1core-002-s004 |
| NF-05 | Route Approvals Without Blocking Progress | story-v1core-002-s005 |
| NF-09 | Ensure Every Deliverable Traces Back to a Use Case | story-v1core-002-s006 |
| NF-06 | Learn From Past Mistakes Across Sessions | story-v1core-002-s006 |
| NF-15 | Assign and Surface Epistemic Grades on Workflow Outputs | story-v1core-002-s007 |

### v1-core Slice Only

For this epic, each UC is scoped to a conservative v1-core slice:

- NF-02 / NF-13: Decisions are captured as structured ADR-like artifacts with at least two options and explicit tradeoffs, but the generation and enforcement logic is deterministic and rule-based, not learned from past approvals.  
- NF-03: Scoping is performed by a single scoping agent using file-level boundaries; no cross-agent negotiation or dynamic re-scoping based on run-time behavior.  
- NF-04: Verification is limited to running tests and checks defined in the task spec in a single-agent, single-repo context; no flaky-test heuristics or complex non-code verification yet.  
- NF-05: Tiered approvals use explicit human-authored rules (what is Tier 1/2/3) with simple queues; no ML-based tier learning, escalation heuristics, or SLA-driven routing.  
- NF-09: Traceability is enforced through explicit links from tasks and tests back to UC IDs; no automatic discovery of orphan code beyond what the review pipeline checks.  
- NF-06: “Learn from past mistakes” is implemented as explicit, human-reviewed lessons that modify prompts/constraints; no unsupervised behavioral shifts.
- NF-15: Epistemic grades are added as required metadata fields (`epistemic_grade` + `grade_justification`) on decision records and options sheets; grade-presence is a blocking S8 reviewer check. The full confidence sub-loop (trigger research when grade is below threshold, re-grade after evidence gathering) and retroactive grading of existing artifacts are deferred to idea-005/v1.1.

Health metrics dashboards, learned tier classification, and concurrent multi-agent behaviors are intentionally deferred to later stages (NF‑08 v1.1, XP‑06 v2).

## Story Index

| Story ID | Title | Appetite | Priority |
|---|---|---|---|
| story-v1core-002-s001 | Options Generation and Decision Recording | Small | Must |
| story-v1core-002-s002 | Decision Enforcement by Reviewer | Small | Must |
| story-v1core-002-s003 | Task Scoping and Scope Enforcement | Small | Must |
| story-v1core-002-s004 | Verified-Before-Reporting Quality Gate | Small | Must |
| story-v1core-002-s005 | Tiered Approval Routing | Small | Must |
| story-v1core-002-s006 | Traceability Enforcement and Cross-Session Learning | Small | Must |
| story-v1core-002-s007 | Decision Evidence and Epistemic Grade Recording | Small | Must |

### Story Success Bounds (v1-core)

- story-v1core-002-s001 (Options & Recording): Ensures that at identified decision points the system surfaces at least two distinct options with tradeoffs and records the chosen option plus rationale in a durable artifact; it does not attempt to optimize number or quality of options via learning.  
- story-v1core-002-s002 (Decision Enforcement): Ensures that when implementers produce work that violates recorded decisions, the reviewer can detect and flag that violation via static checks and prompts; no automatic refactoring or auto-repair.  
- story-v1core-002-s003 (Scoping & Enforcement): Produces task specs with explicit in-scope/out-of-scope boundaries and acceptance criteria, and ensures implementers stay within them; it does not yet support dynamic scope negotiation mid-task.  
- story-v1core-002-s004 (VBR Quality Gate): Implements a Verified-Before-Reporting gate that runs configured tests/checks before surfacing work as “done” to the human; it does not include flaky-test diagnosis, coverage analytics, or non-code verification heuristics.  
- story-v1core-002-s005 (Tiered Approvals): Implements a simple queue-based Tier 1/2/3 approval system with explicit routing rules; it does not include learned tiering, prioritization by risk, or time-based escalation.  
- story-v1core-002-s006 (Traceability & Learning): Enforces that all changes trace to UCs and captures recurring patterns as candidate lessons that must be human-reviewed before they affect agent behavior; no unsupervised lesson application.
- story-v1core-002-s007 (Epistemic Grades): Adds `epistemic_grade` + `grade_justification` as required fields on decision records and options sheets; adds grade-presence as a blocking S8 reviewer check; preserves grades in S9 capture records. Does not implement the full confidence sub-loop, retroactive grading, or grade-per-altitude rules.

## Scope Hammer Log

| Dropped Story | Reason |
|---|---|
| Automated lesson application without human review | problem-004 explicitly excludes this. Any lesson learned must be reviewed before changing agent behaviour — unsupervised behaviour change is a Tier 3 risk by framework rules. |
| Health metrics and framework performance dashboard | NF-08 is v1.1 scope. Qualitative observation at S9 is sufficient in v1-core; a formal metrics surface would inflate this epic significantly with low return at the current stage. |
| Automated tier-classification learning from past approval history | problem-003 explicitly excludes this. Manual tier rules are sufficient for v1-core and adding ML-based tier learning introduces an unvalidated dependency that would expand the implementation appetite beyond Medium. |
| Concurrent multi-agent conflict resolution | XP-06 is v2 scope. The framework operates sequentially in v1-core; this complexity is only warranted once the single-agent workflow is proven stable. |

### Out-of-Scope for v1-core (for this Epic)

- No health dashboards or time-series framework metrics (NF-08: v1.1).  
- No ML-based tier classification or auto-tuning of approval thresholds (post-v1).  
- No autonomous behavior changes by agents based on lessons (all lessons go through human review).  
- No concurrent multi-agent execution or conflict resolution (XP-06: v2).  
- No cross-repo or distributed pipeline orchestration; v1-core assumes a single logical codebase.

## Assumption Probes & Tensions

This epic is explicitly testing:

- Assumption 2 (The human will trust AI-held memory over their own): By providing recorded decisions with alternatives and rationale, we test whether the human uses them instead of re-litigating decisions from scratch. Evidence: rate of “reopen” vs. “reuse” of past decisions in similar contexts.  
- Assumption 4 (Decision capture overhead is tolerable): We test whether structured decision capture at key points is sustainable in day-to-day work. Evidence: how often decision recording is skipped or minimized, and whether humans complain about overhead.  
- Assumption 3 (Non-software domains benefit): Partly probed by how well NF‑02/NF‑06 style decision records apply to AP/RE decisions (regulatory, investment) without bespoke machinery.

Key tensions monitored:

- Tension B (Automation vs. Human Direction): We intentionally keep human approval and review in the loop for tier routing and lesson application. If humans feel burdened by approvals, or if they feel sidelined, the tension is mis-set.  
- Tension C (Premature Structure vs. No Structure): Decision capture is restricted to high-impact points where options are natural; if recording feels required for every micro-decision, we have over-structured and will see avoidance.  
- Tension A (Breadth vs. Depth in learning): NF‑06 is biased toward a small number of high-quality, human-reviewed lessons rather than broad unsupervised pattern mining; if we see repeated mistakes slipping through, that bias may need adjusting.

## Epic Appetite

Total: 7 Small — fits within 3 implementation cycles (decision-memory cycle, execution-pipeline cycle + epistemic grading, quality-loop + traceability cycle).