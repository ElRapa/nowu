---
id: epic-v1core-003
source_problem: problem-005
created: 2026-04-08
status: APPROVED
agent_version: story-mapper@2.3 (enriched)
parent_goal: goal-001
generated_at: 2026-04-08T00:00:00Z
---

# Epic: epic-v1core-003 — Project Bootstrap & Idea Lifecycle

## Epic Summary

This epic delivers the on-ramp that the rest of the system needs to serve non-software work: a lightweight space for half-formed ideas to exist and develop without premature structure, and a fast path from an explored idea to a fully operational project context with its own memory, decision journal, and agent-ready state. Without this foundation, the framework remains useful only for work that is already fully formed — denying it access to the earliest and most fragile creative moments, and making every new non-software project a manual setup burden.

This epic is the concrete v1-core probe of Discovery Theme 6 (Project Bootstrap) and directly tests whether the nowu framework can serve work that has not yet crystallised into a formal project. It also provides the prerequisite infrastructure that epic 004 depends on: AP and RE projects cannot be bootstrapped without the mechanism this epic delivers.

## Vision & Discovery Alignment

- **Vision (6 months):** "You can start from a vague idea and get meaningful output without the process feeling like overhead." This epic delivers the "start from a vague idea" part — zero-friction entry, agent-assisted exploration, and promotion to a real project when the idea earns it.
- **Vision (12 months):** "At least six projects are active across different domains… they do not interfere with each other." The bootstrap mechanism this epic delivers is the prerequisite for any new project to exist within the framework. All six projects require it.
- **Discovery Theme 6 (Project Bootstrap Gap):** Directly addressed by NF-07. Without a fast bootstrap path, every new project is a manual burden that discourages the multi-project operating model the vision requires.
- **Discovery Theme 3 (Frictionless Capture Across All Contexts):** Partially addressed by NF-12 — idea exploration is a form of capture for work that is not yet a project.
- **Discovery Assumption 5 (Premature structure kills ideas):** This epic is the direct test of that assumption. NF-12 is designed around it.

## Use Case Mapping

| UC-ID | Description | Covered by |
|---|---|---|
| NF-12 | Explore a Vague Idea Without Structure | story-v1core-003-s001 |
| NF-07 | Bootstrap a New Project Using the Framework | story-v1core-003-s002 |

### v1-core Slice Only

For this epic, each UC is scoped to its v1-core slice:

- **NF-12:** Exploration is CLI-only, single-human, zero mandatory fields. The system asks clarifying questions and optionally does light research. The only binding output is a promotable idea record — and only when the human explicitly requests promotion. No automated maturity detection, no decay timers, no forced structure.
- **NF-07:** Bootstrap is a single-session operation that creates a project with its own isolated state directory, decision journal, and agent-ready configuration. Domain-agnostic: the same mechanism serves software and non-software projects. No domain-specific templates, no collaborator setup, no remote access.

## Story Index

| Story ID | Title | Appetite | Priority |
|---|---|---|
| story-v1core-003-s001 | Lightweight Idea Exploration | Small | Must |
| story-v1core-003-s002 | Single-Session Project Bootstrap | Small | Must |

### Story Success Bounds (v1-core)

- **story-v1core-003-s001 (Idea Exploration):** Delivers a zero-friction entry point for half-formed ideas: capture, clarifying questions, optional light research, and a promotable record. It does not include automated research synthesis, multi-session idea threads, or any form of binding commitment without explicit human action.
- **story-v1core-003-s002 (Project Bootstrap):** Delivers a single-session setup command that creates an isolated project context (own state, own journal, own agent defaults) for any domain. It does not include domain-specific templates, collaborator onboarding, or automatic import of existing notes.

## Out-of-Scope for v1-core (for this Epic)

- No automated idea maturity scoring or system-initiated promotion.
- No idea decay, expiration, or archival of un-promoted captures.
- No domain-specific project templates (AP, RE) — domain-agnostic bootstrap only; domain validation is epic-004's job.
- No collaborator onboarding or multi-user project contexts (AP-07: v1.2).
- No remote or mobile access to exploration flows (PK-08: v1).

## Scope Hammer Log

| Dropped Story | Reason |
|---|---|
| Automated idea decay and expiration of un-promoted captures | problem-005 explicitly defers this. Exploration records persist indefinitely in v1-core. Introducing a decay mechanism now adds policy complexity before we know what exploration patterns the human actually develops. |
| Collaborator onboarding for new projects | AP-07 is v1.2 scope. Bootstrapping for a solo operator is the correct first target; multi-user access surfaces real sharing requirements that do not exist yet. |
| Domain-specific template layers for AP and RE | problem-005 explicitly defers this to problem-008. The bootstrap mechanism must prove it works domain-agnostically before domain-specific variants are worth designing. |
| Automatic project promotion based on idea maturity signals | Adds system-initiated binding commitment, which contradicts the core design constraint: exploration records produce zero binding artifacts unless the human explicitly promotes. |

## Assumption Probes & Tensions

This epic is explicitly testing:

- **Assumption 5 (Premature structure kills ideas):** The no-mandatory-fields design of NF-12 is the direct test. Evidence: does the human actually use the exploration mode, or do they skip it and go straight to intake? If skip rate is high, the assumption holds but the UX may be wrong; if exploration is used but few ideas are promoted, the promotion path may be too heavy.
- **Assumption 6 (Domain-agnostic bootstrap is sufficient):** The AP and RE bootstrap tests in problem-005 SC-3 will answer whether one mechanism genuinely serves all domains or whether the first non-software project surfaces requirement gaps. Findings must be captured at S9 and fed into epic-004.

Key tensions monitored:

- **Tension D (Zero structure vs. findable later):** NF-12 deliberately produces minimal structure. The risk is that un-enriched idea records accumulate and become unsearchable noise. We watch for: backlog of unexplored ideas, human frustration with finding old captures. If this emerges, the enrichment step needs to be triggered earlier in the lifecycle.
- **Tension E (Flexibility vs. consistency across domains):** Domain-agnostic bootstrap is the right v1-core target, but it may produce projects that feel structurally different from each other in practice. We watch for: human confusion about which project holds what, or state contamination between projects.

## Epic Appetite

Total: 2 Small — fits within 1 implementation cycle
