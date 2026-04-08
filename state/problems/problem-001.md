---
id: problem-001
source_idea: idea-v1core
source_discovery: disc-v1core
created: 2026-04-07
status: APPROVED
authored_by: perspective-interview@P1.2
reviewed_at:
---

# Problem Statement: problem-001

## Core Problem

Every time a human or AI agent returns to a project after any gap, they arrive without working memory of what was happening, what was decided, and what comes next. The re-orientation cost is high enough — 15–30 minutes per return visit — that it systematically defers or prevents productive work. Projects do not stall from lack of effort; they stall because the cost of picking up the thread exceeds the available time and energy.

## Validated Personas

**Primary:** Raphael (the multi-project human) — runs several concurrent projects across domains; the re-orientation overhead compounds across every project he maintains.
**Secondary:** AI agents (nowu pipeline) — must reconstruct context to continue a work cycle without repeating completed steps or contradicting prior decisions.

## Confirmed Outcome Goals

1. The human opens any project after any duration of absence and knows — within one interaction — what was last completed, what key decision was made and why, and what the recommended next step is.
2. An AI agent resuming a work cycle identifies the last verified checkpoint and proposes the correct next action without hallucinating progress or re-doing completed work.
3. Re-orientation cost approaches zero, so projects resume instead of stall and the experience of "progress compounds" becomes observable.

## Flagged Assumptions (resolved)

| Assumption | Resolution | Impact |
|---|---|---|
| The human will trust AI-held memory over their own reconstruction | Accepted — trust must be earned through consistent accuracy; early errors will erode adoption. Addressed by making the orientation artifact readable and verifiable by the human, not opaque. | Affects success criterion 1 (trustworthy orientation, not advisory) |
| Persisted state is sufficient to reconstruct context without a live session | Accepted as design constraint — state artifacts must be self-contained and structured enough to serve as the sole input for resumption. | Affects scoping: no background processes, pure artifact reads |

## Appetite

- [ ] Tiny (< 2 h)
- [ ] Small (< 1 day)
- [x] Medium (2-3 days)
- [ ] Large (up to 1 week)

**Rationale:** Two distinct resumption paths (human-facing orientation and agent-facing checkpoint detection) must both work reliably, with defined state artifact schemas and a protocol for the human to confirm resumption intent. This is more than a day's work but does not require cross-project infrastructure.

## Out of Scope (explicit)

1. Cross-project orientation (surfacing what matters across all projects at once — that is problem-006).
2. Automatic session start without human confirmation — resumption always ends at a human gate.
3. Orientation for first-time visitors / collaborators who did not create the project (that is v1.2 scope: AP-07).
4. Historical analytics or trend data about past sessions.

## Success Criteria

1. An AI agent resuming any nowu workflow step reads persisted state, identifies the correct next action, and proposes it without repeating a completed step — verified across at least 3 distinct mid-cycle interruption scenarios.
2. The human, returning to a project after ≥ 7 days of absence, receives a usable orientation (what was done, last decision and rationale, recommended next step) within their first interaction — without reading commit history, session logs, or previous artifacts manually.
3. The orientation artifact (or equivalent structured state) is produced consistently at the close of every work cycle, with no manual step required from the human.

## Dependencies

None. This is foundational — most other problems depend on having reliable persisted state, but this problem can be solved independently using the existing file-based state in `state/`.

## UC Coverage

- NF-01: Resume Work After Context Loss
- NF-10: Maintain the Thread for the Multi-Project Human
