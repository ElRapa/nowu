---
id: problem-005
source_idea: idea-v1core
source_discovery: disc-v1core
created: 2026-04-07
status: APPROVED
authored_by: perspective-interview@P1.2
reviewed_at:
---

# Problem Statement: problem-005

## Core Problem

The framework has no lifecycle model for ideas. A vague thought that arrives before it is ready to be a project has nowhere to go: it is either forced into a full intake (which kills it under premature structure) or written in an external note (where it escapes the system entirely). There is no scaffold for the arc from *seed* to *explored* to *grown* to *project*. Separately, even when an idea is ready to become a project, initialising that project requires a multi-hour manual setup ceremony. The result: ideas die early and projects start slowly, both for the same reason — the framework only serves work that is already fully formed.

## Validated Personas

**Primary:** Raphael (the multi-project human) — wants to start a non-software project (food business, real-estate operation) using the same framework as his software work, without a multi-hour setup ceremony or contamination of existing project state.
**Secondary:** Raphael as idea-holder — has a half-formed thought worth exploring but not yet ready to commit; needs a lightweight holding space that does not force premature decisions.

## Confirmed Outcome Goals

1. A vague idea can enter the system with zero structure — the framework meets it where it is: asking clarifying questions, doing light research, and letting the human explore or "play" with the idea without any binding artifact being created.
2. An idea that gains traction grows naturally into a fuller record over multiple sessions, accumulating context, research, and decisions incrementally — promoted by the human when it earns it, not forced by the system.
3. When an idea is ready to become a project (its own context, memory, and decision journal), that promotion happens in a single session — software or non-software domain, no manual directory construction or configuration editing.

## Flagged Assumptions (resolved)

| Assumption | Resolution | Impact |
|---|---|---|
| The same framework scaffolding works for software and non-software projects | Partially accepted — the same directory and artifact structure is domain-agnostic; domain-specific defaults may need a thin configuration layer. This is tested in problem-008 (AP and RE dogfooding). | Scoping note: this problem delivers the bootstrap mechanism; problem-008 validates it in real non-software domains |
| Premature structure kills ideas more often than it helps them | Accepted as a design constraint — the exploration mode (NF-12) must produce zero binding artifacts unless the human explicitly promotes. | Affects NF-12 design: no mandatory fields, no required outputs |
| An idea must have its own project context from the start | Rejected — an idea can be explored within the current project's context (or a neutral sandbox), and a dedicated project is only created if and when the idea earns it. The lifecycle arc (seed → explored → grown → project) is the unit of design, not the project bootstrap alone. | Affects NF-12 design: exploration-mode records are lightweight, promotable artifacts, not project scaffolds |

## Appetite

- [ ] Tiny (< 2 h)
- [x] Small (< 1 day)
- [ ] Medium (2-3 days)
- [ ] Large (up to 1 week)

**Rationale:** Both gaps are narrow and well-understood from the user's pain. Project initialisation must impose no manual setup burden on the human; idea exploration must produce zero binding structure unless the human promotes the record. Together these are a Small scope — two distinct but lightweight gaps with no cross-project infrastructure required.

## Out of Scope (explicit)

1. Applying the bootstrap to the AP and RE projects specifically — that is problem-008 (non-software dogfooding) which validates the mechanism in context.
2. Domain-specific knowledge type definitions (e.g., custom fields for regulatory tracking, supply chain mapping) — those are problem-008 scope.
3. Collaborator onboarding for new projects (AP-07 — v1.2 scope).
4. Automated idea decay or expiration of un-promoted captures — exploration records persist indefinitely in v1-core.

## Success Criteria

1. A half-formed idea can be entered into the system in under 2 minutes with no required fields; the framework responds with clarifying questions and optional light research — no intake artifact is created unless the human asks for one.
2. An idea that has been explored over one or more sessions can be promoted by the human into a fuller record (discovery artifact, problem statement, or project context) with a single instruction — existing exploration notes carry forward.
3. A new project of any domain type (software or non-software) can be initialised from an idea record — own memory space, own decision journal, agent-ready — in a single session without manual directory construction or configuration editing.
4. Two non-software projects (AP and RE) are bootstrapped using this mechanism and operate without any bleeding of state into the framework's own development context.

## Dependencies

None. This problem is independently solvable. problem-008 (non-software dogfooding) depends on this bootstrap mechanism existing, but this problem has no dependency on any other problem in this set.

## UC Coverage

- NF-07: Bootstrap a New Project Using the Framework
- NF-12: Explore a Vague Idea Without Structure
