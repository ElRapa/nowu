# Proposal: Roadmap + Session State / Session Log Update

```yaml
---
research_artifact:
  version: "1.0"
  date: "2026-05-10"
  topic: "Roadmap + session state/log alignment (PROPOSAL)"
  perplexity_session_id: "nowu-5x10-refactor-roadmap-session-log-proposal"

problem_statement:
  diagnosis: |
    ROADMAP-001.md was created during the 5×10 architecture session and currently
    acts as an implementation-focused W/K/A/F tracker. It does not explicitly
    reference upstream artifacts (vision, goals, use cases, SYNTHESIS,
    Architecture Vision, ADRs) and co-exists with stale state files from the
    old linear V1_PLAN (e.g., state/PROGRESS.md, March health reports). There
    is no canonical session log that records "what happened, when, and why".
  context: |
    The orchestrator layer (D-022) now treats ROADMAP-NNN.md as the single
    source of truth for sequencing. Without aligning ROADMAP-001.md with the
    actual artifact inventory and cleaning up stale state, both humans and
    agents (work-scheduler, roadmap-updater) face ambiguity. The lack of a
    session log also makes it hard to reconstruct intent and evaluate future
    changes.
  scope: |
    IN SCOPE: (1) Updating ROADMAP-001.md to reference upstream artifacts and
    clarify its scope, (2) marking stale/legacy state files and archiving or
    annotating them, (3) designing a simple session-log format and seeding it
    with a small number of key sessions. OUT OF SCOPE: Rewriting the roadmap
    structure wholesale, changing decisions (D-020/D-022), or performing a
    full historical reconstruction across all git history.

evaluation_criteria:
  - criterion: "Orientation & traceability"
    weight: "high"
    rationale: "Humans and agents should be able to answer 'where are we and why?' from a small set of docs."
  - criterion: "Consistency with decisions"
    weight: "high"
    rationale: "ROADMAP-001, state/, and decisions (D-020, D-022) must not contradict each other."
  - criterion: "Implementation effort"
    weight: "medium"
    rationale: "This should be achievable in a single focused architecture-altitude session."
  - criterion: "Future maintainability"
    weight: "medium"
    rationale: "The session log and state conventions should be easy to keep up-to-date."

alternatives:
  - id: "A"
    name: "One-pass alignment (roadmap + state + session-log)"
    summary: |
      In a single architecture-altitude session, update ROADMAP-001.md with
      explicit artifact references and scope, mark/annotate stale state files,
      and create a canonical session-log file seeded with key past sessions.
    changes:
      - file: "docs/ROADMAP-001.md"
        action: "edit"
        change: |
          Add a Sources/Inputs section referencing vision, goals, USE_CASES,
          SYNTHESIS-001, ARCHITECTURE-VISION, and key ADRs. Clarify that this is
          an implementation roadmap born from the 5×10 architecture work.
      - file: "state/PROGRESS.md"
        action: "edit"
        change: |
          Mark as STALE, add note that V1_PLAN has been superseded by
          ROADMAP-001 (per D-020), and point readers to the roadmap instead.
      - file: "state/health/*.md"
        action: "edit"
        change: |
          For March 2026 health reports, mark as STALE and capture a short note
          explaining that they predate the architecture rework.
      - file: "state/SESSION_STATE.md"
        action: "edit"
        change: |
          Either remove or annotate as TEMPLATE ONLY, with pointer to the new
          session-log file for real session records.
      - file: "state/session-log.md"
        action: "create"
        change: |
          Create a canonical session log with a simple structured format
          (date, altitude, primary phase, artifacts touched, decisions/links,
          next work item) and seed with a small number of key sessions.
    pros:
      - "Produces a coherent, up-to-date view of roadmap, state, and history in one pass."
      - "Minimizes time where roadmap and state are out of sync."
      - "Provides a clear anchor for future work (session-log)."
    cons:
      - "Requires careful, focused work to avoid accidental scope creep."
      - "Touches multiple files in one session, so changes must be well-reviewed."
    effort: "medium"
    risk: "medium"
    evaluation:
      orientation___traceability: "excellent"
      consistency_with_decisions: "good"
      implementation_effort: "good"
      future_maintainability: "good"

  - id: "B"
    name: "Roadmap-first, state & log later"
    summary: |
      Update ROADMAP-001.md to reference upstream artifacts and clarify scope,
      but leave stale state files and session logging for a later session.
    changes:
      - file: "docs/ROADMAP-001.md"
        action: "edit"
        change: |
          Add Sources/Inputs and Scope sections; explicitly note that some state
          files are stale and will be cleaned up later.
    pros:
      - "Simpler change set; easy to complete quickly."
      - "Improves roadmap orientation immediately."
    cons:
      - "Leaves stale state and missing session log unaddressed, causing ongoing ambiguity."
      - "Risk of forgetting to schedule the cleanup session."
    effort: "low"
    risk: "low"
    evaluation:
      orientation___traceability: "acceptable"
      consistency_with_decisions: "acceptable"
      implementation_effort: "excellent"
      future_maintainability: "poor"

  - id: "C"
    name: "Session-log-first, roadmap/state later"
    summary: |
      Design a session-log format and seed it from git history and 
      state/learnings, but defer roadmap and state-file alignment.
    changes:
      - file: "state/session-log.md"
        action: "create"
        change: |
          Create a canonical session log and backfill as much as is reasonable."
    pros:
      - "Starts capturing history immediately, which can help future analysis."
      - "Does not require touching existing roadmap right away."
    cons:
      - "Session-log entries may encode an outdated mental model from the old roadmap/state."
      - "Does not reduce current ambiguity around ROADMAP-001 and stale state."
    effort: "medium"
    risk: "medium"
    evaluation:
      orientation___traceability: "acceptable"
      consistency_with_decisions: "poor"
      implementation_effort: "good"
      future_maintainability: "acceptable"

recommendation:
  chosen: "A (PROPOSAL ONLY)"
  rationale: |
    A single, time-boxed architecture-altitude session that updates
    ROADMAP-001.md, marks stale state files, and introduces a canonical
    session-log provides the best balance of orientation, consistency, and
    manageable effort. However, this is explicitly a PROPOSAL for OmO to
    evaluate—not a directive. OmO should confirm the artifact inventory,
    adjust the exact set of files to touch, and may choose a hybrid of A and B
    based on what it sees in the repo at execution time.
  runner_up: |
    If the combined scope proves too large for one session, OmO may choose a
    phased approach: perform the ROADMAP-001 update plus minimal stale-file
    marking first (subset of A), and define the session-log format as a
    follow-up task.

implementation:
  prerequisites:
    - "docs/ROADMAP-001.md exists and is under version control."
    - "DECISIONS.md includes D-020 and D-022."
    - "state/ and docs/ directories are available for inspection (no major pending merges)."
  steps:
    - step: "Inventory key upstream artifacts (vision, goals, USE_CASES, SYNTHESIS-001, ARCHITECTURE-VISION, ADRs)."
      verify: "List of artifacts is captured in a temporary note and cross-checked with MODEL-REFERENCE."
    - step: "Edit docs/ROADMAP-001.md to add Sources/Inputs and Scope sections referencing the inventoried artifacts."
      verify: "ROADMAP-001.md clearly states its inputs and that it is an implementation-focused roadmap derived from those."
    - step: "Review state/PROGRESS.md, state/health/*, state/SESSION_STATE.md, and nearby files for staleness."
      verify: "Each stale or template file is either archived, marked STALE, or annotated with a clear comment."
    - step: "Create state/session-log.md with a simple structured format and seed it with 2–5 key sessions (architecture roadmap creation, orchestrator decision, etc.)."
      verify: "Session-log contains at least a header describing its purpose and a small number of accurate seed entries."
  validation:
    - test: "A new contributor can read ROADMAP-001.md + state/session-log.md and explain what has been done so far and what comes next."
      expected: "They can name at least the main W/K/A/F items, understand their inputs, and identify the next work item without reading V1_PLAN or stale state files."
    - test: "work-scheduler reads ROADMAP-001.md and state/ and returns a coherent 'next work item' decision without being confused by stale state."
      expected: "No references to V1_PLAN-era state; if stale files are present, they are clearly marked and ignored."

context_for_omo:
  files_to_review:
    - "docs/ROADMAP-001.md"
    - "docs/DECISIONS.md"
    - "docs/PRE-WORKFLOW.md"
    - "docs/model/MODEL-REFERENCE.md"
    - "state/PROGRESS.md"
    - "state/health/"
    - "state/learnings/INDEX.md"
  decisions_informed:
    - "D-020 — Areas × Stages replaces linear V1_PLAN"
    - "D-022 — Orchestrator layer external to 5×10"
  related_artifacts:
    - "docs/orchestrator-layer-design.md (if present)"
    - "docs/research/* (architecture/orchestrator sessions)"
  constraints:
    - "This artifact is a PROPOSAL for OmO to evaluate and adjust—not a mandatory plan."
    - "Changes must be backward compatible with current S1–S9 workflow and orchestrator agents."
    - "No deletion of historical artifacts; stale items should be archived or annotated, not removed."
---
```
