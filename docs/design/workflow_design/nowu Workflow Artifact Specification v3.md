# nowu Workflow Artifact Specification v3
## Overview
This specification defines the **exact artifact** produced at each step of the nowu 9-step workflow, along with what context each step's producer needs, what the recipient may assume, and what must be excluded. The design is grounded in three empirical findings:

- Handoffs with **explicit state serialization succeed 94%** of the time, versus 66% with implicit context sharing — a study of 10,842 real agent handoffs.[^1]
- Adding a **handoff justification** ("why this is being passed to you") improved receiving agent task completion by 18%.[^1]
- **Context loss causes 62%** of all handoff failures; the fix is a fixed schema the receiver can parse without guessing.[^1]

The artifacts below are designed to be stored as structured YAML/Markdown files today, and as `know` atoms in the future. Every artifact includes a **handoff header** — a 3-line block that tells the next step: what it's receiving, why, and what to do next.

***
## The Handoff Header (Required on Every Artifact)
Every artifact begins with this block. It is the single most impactful element for reliable handoffs:[^2][^1]

```yaml
handoff:
  from_step: S1           # Which step produced this
  to_step: S2             # Which step should consume this
  justification: >        # WHY this is ready for the next step
    Problem is well-defined with clear use-case references.
    Ready for architectural constraint analysis.
  status: READY_FOR_ARCH  # Machine-readable status
```

The `status` field uses a fixed enum that mirrors the PubNub subagent queue pattern:[^3]

| Status | Meaning |
|--------|---------|
| `READY_FOR_ARCH` | S1 complete → S2 can start |
| `READY_FOR_OPTIONS` | S2 complete → S3 can start |
| `READY_FOR_DECISION` | S3 complete → S4 can start |
| `READY_FOR_SHAPING` | S4 complete → S5 can start |
| `READY_FOR_IMPL` | S5 complete → S6 can start |
| `READY_FOR_VBR` | S6 complete → S7 can start |
| `READY_FOR_REVIEW` | S7 complete → S8 can start |
| `READY_FOR_CAPTURE` | S8 complete → S9 can start |
| `DONE` | S9 complete → cycle finished |
| `BLOCKED` | Cannot proceed — needs human input |
| `CHANGES_REQUESTED` | Returned from review — go back to S6 |

***
## S1: Intake Brief
### Producer
Main session or human (intake is often the starting point of a conversation).
### Artifact Schema
```yaml
# File: state/intake/<id>.md
handoff:
  from_step: S1
  to_step: S2
  justification: >
    [Why this is ready for architecture analysis]
  status: READY_FOR_ARCH

intake:
  id: intake-YYYYMMDD-XX
  title: "Short descriptive name"
  origin: "V1_PLAN Step 02" | "bug report" | "feature idea" | "user request"
  
  problem_statement: >
    2-5 sentences. What is the problem? Who has it? Why does it matter now?
  
  use_case_ids:
    - "NF-01"
    - "NF-04"
  
  affected_modules:
    - "core"
    - "flow"
  
  suspected_scope:
    in_scope: >
      What this change likely touches.
    out_of_scope: >
      What this change should NOT touch.
  
  appetite: "small (≤2h)" | "medium (≤4h)" | "large (≤8h)" | "extra-large (needs shaping)"
  
  open_questions:
    - "Does this need a new contract or extend an existing one?"
```
### Context the Producer Needs
- `docs/V1_PLAN.md` — to identify which step/feature this relates to
- `docs/USE_CASES.md` — referenced by ID only, to tag the right use-case numbers
- `docs/PROGRESS.md` — to check what's already done
### Context to Exclude
Source code, test files, architecture details — those are for S2.
### What the Recipient (S2) May Assume
- There is exactly one intake brief to work from.
- `use_case_ids` are valid references (they exist in USE_CASES.md).
- `affected_modules` is a first guess, not a final answer — S2 will refine it.
- `appetite` is the human's time budget — the architect should respect it.
### Definition of Done
- [ ] Problem statement is specific enough that two people would solve roughly the same problem.
- [ ] At least one use-case ID is linked.
- [ ] Appetite is set (prevents unbounded scope).

***
## S2: Constraints Sheet
### Producer
`nowu-architect` subagent.
### Artifact Schema
```yaml
# File: state/arch/<intake-id>-constraints.md
handoff:
  from_step: S2
  to_step: S3
  justification: >
    [Why constraints are complete and options can be explored]
  status: READY_FOR_OPTIONS

constraints:
  intake_id: intake-YYYYMMDD-XX
  
  module_boundaries:
    affected:
      - module: "flow"
        role: "Primary — new logic lives here"
      - module: "core"
        role: "Read-only — uses existing contracts"
    not_affected:
      - "bridge"
      - "soul"
  
  architectural_constraints:
    - constraint: "Domain layer must not import infrastructure"
      source: "D-007"
    - constraint: "All persistence goes through MemoryService"
      source: "D-001"
  
  risks:
    - risk: "Session WAL complexity may exceed appetite"
      severity: "medium"
      mitigation: "Prototype WAL in isolation first"
  
  assumptions:
    - assumption: "know v0.2.0 API is stable"
      validated: false
  
  open_questions:
    - "Should session state be mirrored to know on every step or only on close?"
```
### Context the Producer Needs
- The S1 Intake Brief (the direct input).
- `docs/ARCHITECTURE.md` — module map, layer rules (Section 4.1).
- `docs/DECISIONS.md` — existing decisions that constrain the design.
- `core/contracts/*.py` — the public API surface (read-only, not implementations).
### Context to Exclude
Source code internals, test files, implementation details, V1_PLAN.md (already consumed in S1), USE_CASES.md (already tagged in S1).
### What the Recipient (S3) May Assume
- All known architectural constraints are listed — nothing is hidden.
- Module boundaries are refined from S1's initial guess.
- Risks have severity ratings, so the Options step can factor them in.
- Unvalidated assumptions are flagged — options should address them.
### Definition of Done
- [ ] Every existing decision (D-NNN) that constrains this work is referenced.
- [ ] Module boundaries are explicit (affected vs. not affected).
- [ ] At least one risk is identified (if zero risks, state why).

***
## S3: Options Sheet
### Producer
`nowu-architect` subagent (same agent, second pass — or a continuation).
### Artifact Schema
```yaml
# File: state/arch/<intake-id>-options.md
handoff:
  from_step: S3
  to_step: S4
  justification: >
    [Why options are complete and a decision can be made]
  status: READY_FOR_DECISION

options:
  intake_id: intake-YYYYMMDD-XX
  constraints_id: "<intake-id>-constraints"
  
  options:
    - id: A
      title: "Wrap know in MemoryService"
      summary: >
        1-3 sentences describing the approach.
      design_sketch: >
        Key classes/contracts involved. Module interactions.
        NOT implementation details — C4 Level 2 only.
      pros:
        - "Centralized retry and caching policy"
        - "Single surface for testing"
      cons:
        - "Extra indirection layer"
        - "Risk of leaky abstraction"
      addresses_risks:
        - "Session WAL complexity → contained in one service"
      estimated_effort: "medium (≤4h)"
      migration_path: >
        How we get from current state to this option.
    
    - id: B
      title: "Call know directly everywhere"
      # ... same structure
  
  evaluation:
    criteria:
      - name: "Simplicity"
        weight: 0.3
        description: "How simple is the implementation?"
      - name: "Reliability"
        weight: 0.3
        description: "How robust under failure conditions?"
      - name: "Fits appetite"
        weight: 0.2
        description: "Can it be done within the time budget?"
      - name: "Future-proofness"
        weight: 0.2
        description: "How well does it support v2+ goals?"
    scores:
      A: { simplicity: 4, reliability: 5, fits_appetite: 4, future_proofness: 5 }
      B: { simplicity: 5, reliability: 3, fits_appetite: 5, future_proofness: 2 }
    
    recommendation: "A"
    recommendation_rationale: >
      Option A scores highest weighted. It addresses the WAL risk
      and creates a stable contract for future know upgrades.
```
### Context the Producer Needs
- S2 Constraints Sheet (the direct input).
- S1 Intake Brief (for appetite and scope).
- `core/contracts/*.py` — to understand existing interfaces.
- Module `__init__.py` files — to understand public API surface.
### Context to Exclude
Full source code, test files, ARCHITECTURE.md (already consumed in S2), DECISIONS.md (already consumed in S2). The architect should not be anchored by implementation details when exploring options.[^4]
### What the Recipient (S4) May Assume
- Options are mutually exclusive and collectively exhaustive for the problem space.
- Each option has been evaluated against the same criteria with the same weights.
- A recommendation exists with explicit rationale.
- Effort estimates respect the appetite from S1.
### Definition of Done
- [ ] At least 2 options are presented (unless justified why only 1 exists).
- [ ] Every option addresses at least one risk from S2.
- [ ] Weighted scores are computed and a recommendation is stated.
- [ ] No option requires effort exceeding the appetite.

***
## S4: Decision Record (D-NNN)
### Producer
`nowu-architect` + human approval (Tier 2).
### Artifact Schema
The decision record is appended to `docs/DECISIONS.md` using the existing format, but with explicit links back to the upstream artifacts:[^5][^6]

```markdown
## D-NNN: [Title]

**Date**: YYYY-MM-DD  
**Status**: accepted  
**Intake**: intake-YYYYMMDD-XX  
**Options evaluated**: A (chosen), B (rejected)

### Context
Why this decision was needed (1-3 sentences from intake + constraints).

### Decision
We chose Option [X] because [rationale from Options Sheet evaluation].

### Consequences
- [Positive consequence]
- [Negative consequence / accepted tradeoff]
- [What this enables for future work]

### Constraints Created
- [New constraint that downstream steps must respect]
```

Plus the handoff artifact:

```yaml
# File: state/arch/<intake-id>-decision.md
handoff:
  from_step: S4
  to_step: S5
  justification: >
    Decision D-NNN approved. Ready for task shaping.
  status: READY_FOR_SHAPING

decision:
  intake_id: intake-YYYYMMDD-XX
  decision_id: D-NNN
  chosen_option: A
  title: "Wrap know in MemoryService"
  new_constraints:
    - "All know access must go through MemoryService"
  approved_by: "human"
  approved_date: "YYYY-MM-DD"
```
### Context the Producer Needs
- S3 Options Sheet (the direct input).
- `docs/DECISIONS.md` — to avoid contradictions and assign next D-NNN number.
### Context to Exclude
Source code, tests, contracts (decision is at system level, not code level).
### What the Recipient (S5) May Assume
- There is exactly one approved decision with one chosen option.
- New constraints are explicit — the shaper must respect them.
- The decision is final — S5 should not re-evaluate alternatives.
### STOP Point
**S4 always requires human approval before proceeding.** The architect presents the options + recommendation. The human approves, modifies, or rejects. Only after approval does the status flip to `READY_FOR_SHAPING`.[^3]

***
## S5: Task Spec(s)
### Producer
`nowu-shaper` subagent.
### Artifact Schema
One file per task. For multi-task breakdowns, a manifest links them:

```yaml
# File: state/tasks/<task-id>.md
handoff:
  from_step: S5
  to_step: S6
  justification: >
    [Why this task is ready for implementation]
  status: READY_FOR_IMPL

task:
  id: task-YYYYMMDD-XX
  title: "Implement MemoryService with know integration"
  intake_id: intake-YYYYMMDD-XX
  decision_id: D-NNN
  use_case_ids: ["NF-01", "NF-04"]
  
  scope:
    in_scope_files:
      - "src/nowu/core/services/memory_service.py"
      - "src/nowu/core/contracts/memory.py"
      - "tests/unit/core/test_memory_service.py"
    out_of_scope:
      - "Do NOT modify flow/ or bridge/ modules"
      - "Do NOT change existing contracts"
    primary_module: "core"
  
  acceptance_criteria:
    - id: AC-1
      criterion: "MemoryService.store() persists a know atom and returns its ID"
      test: "test_store_returns_atom_id"
    - id: AC-2
      criterion: "MemoryService.recall() retrieves atoms by type and relation"
      test: "test_recall_filters_by_type"
    - id: AC-3
      criterion: "All know access is through MemoryService (no direct imports elsewhere)"
      test: "test_architecture_no_direct_know_imports"
  
  test_strategy:
    write_first:
      - "tests/unit/core/test_memory_service.py::test_store_returns_atom_id"
      - "tests/unit/core/test_memory_service.py::test_recall_filters_by_type"
    mock_boundary: "know SDK — mock at MemoryService boundary"
  
  dependencies:
    - task_id: "task-YYYYMMDD-01"
      type: "must-complete-first"
      reason: "Contract must exist before service"
  
  estimated_hours: 3
  
  context_for_implementer: >
    You are implementing a wrapper service. Read the chosen option
    from D-NNN. The contract in core/contracts/memory.py defines
    the interface. Write tests against the contract first.
```
### Context the Producer Needs
- S4 Decision handoff (decision + chosen option + new constraints).
- File tree of affected modules (`find src/nowu/<module> -name '*.py'`).
- `core/contracts/*.py` — existing interface contracts.
- `tests/` directory structure — to know where tests should go.
- `docs/PROGRESS.md` — to check task numbering and dependencies.
### Context to Exclude
Architecture docs (decision is settled), vision docs, unrelated modules' source code, USE_CASES.md (already tagged in S1).
### What the Recipient (S6) May Assume
- `in_scope_files` is exhaustive — if a file isn't listed, the implementer should NOT touch it.
- Acceptance criteria have pre-named test functions — write exactly those tests first.
- `test_strategy.write_first` gives the exact test order for TDD.
- `context_for_implementer` is a compressed, right-level briefing (avoids loading upstream docs).
### STOP Point
**S5 always requires human approval of scope before implementation proceeds.** This prevents the #1 failure mode: scope creep from unbounded implementation.[^3]
### Definition of Done
- [ ] Every acceptance criterion has a corresponding named test.
- [ ] `in_scope_files` is explicit (no wildcards, no "and related files").
- [ ] Estimated hours ≤ 4h per task (break down further if exceeded).
- [ ] Dependencies between tasks are explicit.

***
## S6: Change Set
### Producer
Main Claude Code session (implementation).
### Artifact Schema
This is the lightest artifact — it's ephemeral working state, not a durable document. But it still needs a handoff header for S7:

```yaml
# File: state/changes/<task-id>.md
handoff:
  from_step: S6
  to_step: S7
  justification: >
    Implementation complete. All acceptance criteria addressed.
    Ready for VBR verification.
  status: READY_FOR_VBR

changeset:
  task_id: task-YYYYMMDD-XX
  
  files_changed:
    - path: "src/nowu/core/services/memory_service.py"
      change_type: "created"
      summary: "MemoryService class with store() and recall() methods"
    - path: "tests/unit/core/test_memory_service.py"
      change_type: "created"
      summary: "3 tests covering AC-1, AC-2, AC-3"
  
  acceptance_criteria_addressed:
    - id: AC-1
      addressed: true
      test: "test_store_returns_atom_id"
    - id: AC-2
      addressed: true
      test: "test_recall_filters_by_type"
    - id: AC-3
      addressed: true
      test: "test_architecture_no_direct_know_imports"
  
  notes: >
    Any implementation decisions made during coding.
    "Chose to use Protocol class instead of ABC for MemoryService."
```
### Context the Producer Needs
- S5 Task Spec (the direct input — specifically `in_scope_files`, acceptance criteria, test strategy).
- The actual in-scope files listed in the task spec.
- `pyproject.toml` — for tooling config (ruff, mypy, pytest settings).
- Related test files.
### Context to Exclude
**Everything else.** Architecture docs, decisions, vision, plan, other modules' code, USE_CASES.md. The implementer works at C4 Level 4 (code) and should not be distracted by system-level context. This is the most aggressively scoped step — and the one where context pollution causes the most damage, since loading architecture docs during coding causes agents to re-litigate settled decisions.[^4][^1]
### What the Recipient (S7) May Assume
- `acceptance_criteria_addressed` maps 1:1 to the task spec's criteria.
- `files_changed` is complete — no hidden modifications.
- The implementer believes all tests pass (S7 will verify).
### Definition of Done
- [ ] Every acceptance criterion from S5 is addressed (true/false per criterion).
- [ ] Files changed are listed explicitly.
- [ ] No files outside `in_scope_files` were modified.

***
## S7: VBR Report
### Producer
Automated (Claude Code hooks or manual commands).
### Artifact Schema
```yaml
# File: state/vbr/<task-id>.md
handoff:
  from_step: S7
  to_step: S8
  justification: >
    All quality checks pass. Ready for architectural review.
  status: READY_FOR_REVIEW  # or CHANGES_REQUESTED if failed

vbr:
  task_id: task-YYYYMMDD-XX
  timestamp: "YYYY-MM-DDTHH:MM:SS"
  
  checks:
    - name: "pytest"
      command: "uv run pytest --tb=short -q"
      result: "pass"  # pass | fail
      output: |
        12 passed in 0.34s
    - name: "mypy"
      command: "uv run mypy src/ --strict"
      result: "pass"
      output: |
        Success: no issues found in 8 source files
    - name: "ruff"
      command: "uv run ruff check ."
      result: "pass"
      output: |
        All checks passed!
  
  overall: "pass"  # pass only if ALL checks pass
  
  scope_check:
    files_in_diff: ["src/nowu/core/services/memory_service.py", "tests/unit/core/test_memory_service.py"]
    files_allowed: ["src/nowu/core/services/memory_service.py", "src/nowu/core/contracts/memory.py", "tests/unit/core/test_memory_service.py"]
    scope_violation: false
  
  notes: >
    Any warnings or non-blocking observations.
```
### Context the Producer Needs
- S6 Change Set (to know what was changed).
- S5 Task Spec (to verify scope — `in_scope_files` vs actual diff).
- `pyproject.toml` (to run the correct commands).
### Context to Exclude
Everything else. VBR is mechanical — it runs commands and reports results.
### What the Recipient (S8) May Assume
- If `overall: pass`, all three checks (pytest, mypy, ruff) passed.
- `scope_check` confirms whether only allowed files were modified.
- The raw output is included — the reviewer can inspect it without re-running.
### Definition of Done
- [ ] All three checks have been run (not skipped).
- [ ] Scope check compares actual diff against task spec's `in_scope_files`.
- [ ] Overall is `pass` only if every individual check passes.

***
## S8: Review Report
### Producer
`nowu-reviewer` subagent (fresh context window — no implementation context pollution).[^3]
### Artifact Schema
```yaml
# File: state/reviews/<task-id>.md
handoff:
  from_step: S8
  to_step: S9  # or back to S6 if changes requested
  justification: >
    [Why approved, or what needs to change]
  status: READY_FOR_CAPTURE  # or CHANGES_REQUESTED

review:
  task_id: task-YYYYMMDD-XX
  reviewer: "nowu-reviewer"
  timestamp: "YYYY-MM-DDTHH:MM:SS"
  
  outcome: "approved" | "changes_requested"
  
  checklist:
    - check: "Architecture boundaries respected"
      pass: true
      evidence: "No imports cross layer boundaries"
    - check: "Only in-scope files modified"
      pass: true
      evidence: "Diff matches task spec in_scope_files"
    - check: "Tests written before implementation (TDD)"
      pass: true
      evidence: "Git log shows test commit before impl commit"
    - check: "Acceptance criteria covered"
      pass: true
      evidence: "3/3 criteria have corresponding passing tests"
    - check: "Types clean (mypy --strict)"
      pass: true
      evidence: "VBR report shows mypy pass"
    - check: "Style clean (ruff)"
      pass: true
      evidence: "VBR report shows ruff pass"
    - check: "Follows existing decisions"
      pass: true
      evidence: "D-NNN constraints respected"
  
  critical_issues: []
    # - issue: "MemoryService imports know directly in domain layer"
    #   fix_required: "Move import to infrastructure adapter"
  
  warnings:
    - "Test names could be more descriptive (minor)"
  
  suggestions:
    - "Consider adding a docstring to MemoryService.recall()"
  
  lessons_observed:
    - "The Protocol approach worked better than ABC for this contract"
```
### Context the Producer Needs
- S7 VBR Report (test results, scope check).
- S6 Change Set (file list, acceptance criteria mapping).
- S5 Task Spec (acceptance criteria, scope boundaries — the "contract" to review against).
- Git diff of the actual changes.
- `.claude/rules/architecture.md` — the rules to check against.
### Context to Exclude
Full architecture docs (the rules summary is sufficient), vision/plan docs, upstream intake/constraints/options (the reviewer checks code against the task spec, not against the original problem). This is critical: the reviewer should have **fresh eyes**, not accumulated context from the entire cycle.[^1][^7]
### What the Recipient (S9) May Assume
- If `outcome: approved`, the code meets all quality standards.
- `lessons_observed` contains insights worth capturing in long-term memory.
- If `outcome: changes_requested`, `critical_issues` lists exactly what must be fixed.
### Definition of Done
- [ ] Every checklist item has a pass/fail verdict with evidence.
- [ ] If any critical issues exist, outcome is `changes_requested` (never approved with critical issues).
- [ ] Lessons observed are noted (even if empty — "no new lessons" is valid).

***
## S9: Capture Record
### Producer
`nowu-curator` subagent.
### Artifact Schema
```yaml
# File: state/capture/<date>-<scope>.md
handoff:
  from_step: S9
  to_step: "DONE" | "S5" | "S1"
  justification: >
    [What was captured and what happens next]
  status: DONE  # or READY_FOR_SHAPING (next task) or READY_FOR_ARCH (next feature)

capture:
  intake_id: intake-YYYYMMDD-XX
  decision_ids: ["D-NNN"]
  tasks_completed: ["task-YYYYMMDD-XX"]
  
  progress_update:
    step: "Step 02 — Memory Integration Layer"
    previous_status: "in-progress"
    new_status: "completed"  # or "in-progress" if more tasks remain
    summary: >
      MemoryService implemented with store/recall. All tests passing.
  
  decisions_captured:
    - id: D-NNN
      already_in_DECISIONS_md: true
    - id: D-NNN+1
      already_in_DECISIONS_md: false
      action: "Append to DECISIONS.md"
  
  lessons:
    - lesson: "Protocol classes work better than ABCs for cross-module contracts"
      category: "architecture"
      applicable_to: "future contract definitions"
    - lesson: "Shaping with explicit out_of_scope prevented implementer from touching bridge module"
      category: "process"
      applicable_to: "all future task shaping"
  
  follow_ups:
    - "Create task for know integration tests (currently mocked)"
    - "Update ARCHITECTURE.md Section 4.1 with MemoryService module"
  
  commit_message: >
    feat(core): add MemoryService with know integration [NF-01, NF-04]
  
  files_updated:
    - "docs/PROGRESS.md"
    - "docs/DECISIONS.md" (if new decisions)
```
### Context the Producer Needs
- S8 Review Report (lessons observed, outcome).
- `docs/DECISIONS.md` — to check what needs updating.
- `docs/PROGRESS.md` — to update the current step status.
- Git log of recent commits — to compose the commit message.
### Context to Exclude
Source code, test files (the curator writes about "what" and "why", never "how"). This prevents overly technical capture records that no one reads later.[^4]
### What the Next Cycle May Assume
- `PROGRESS.md` is current — the next S1 or S5 can trust it.
- All decisions are in `DECISIONS.md` — no undocumented decisions exist.
- `lessons` are categorized and actionable — future agents can search by category.
- `follow_ups` are concrete next steps, not vague wishes.
### Definition of Done
- [ ] `PROGRESS.md` is updated.
- [ ] Any new decisions are in `DECISIONS.md`.
- [ ] At least one lesson is captured (even "no new lessons from this cycle").
- [ ] Follow-ups are listed (even if empty).
- [ ] Commit message follows conventional format with use-case IDs.

***
## Traceability Chain
Every artifact links back to its origin. The full chain for any piece of code is:

```
Intake (S1)  ──intake_id──▶  Constraints (S2)
                                    │
                              ──intake_id──▶  Options (S3)
                                                   │
                                             ──intake_id──▶  Decision (S4)
                                                                  │
                                                         ──decision_id──▶  Task Spec (S5)
                                                                               │
                                                                      ──task_id──▶  Change Set (S6)
                                                                                        │
                                                                                ──task_id──▶  VBR (S7)
                                                                                                │
                                                                                        ──task_id──▶  Review (S8)
                                                                                                        │
                                                                                                ──intake_id──▶  Capture (S9)
```

This means for any line of code, a human or agent can answer: **Why does this exist?** by tracing `task_id → decision_id → intake_id → use_case_ids`. This is the IEEE 12207 traceability principle adapted for an AI-native workflow.[^8][^6]

***
## Context Budget Per Step
This table summarizes what each step loads and excludes, with approximate token costs:[^4][^1]

| Step | C4 Level | Loads (≈tokens) | Excludes | Why Exclude |
|------|----------|------------------|----------|-------------|
| S1: Intake | L1 | V1_PLAN, USE_CASES (by ID), PROGRESS (~2k) | Source code, architecture, tests | Intake is about "what", not "how" |
| S2: Constraints | L1-2 | S1 artifact, ARCHITECTURE, DECISIONS, contracts (~4k) | Source internals, tests, V1_PLAN | Architecture analysis, not planning |
| S3: Options | L2 | S2 artifact, S1 artifact, contracts, `__init__.py` (~3k) | Source internals, tests, ARCHITECTURE (consumed in S2) | Design exploration, not constraint review |
| S4: Decision | L2 | S3 artifact, DECISIONS (~2k) | Source code, tests, contracts | Decision is about choosing, not designing |
| S5: Shaping | L3 | S4 handoff, file tree, contracts, test structure (~3k) | Architecture docs (settled), vision, unrelated modules | Scoping, not architecture |
| S6: Implementation | L4 | S5 task spec, in-scope files ONLY, pyproject.toml (~2-5k) | **Everything else** | Most aggressively scoped — prevents re-litigation |
| S7: VBR | L4 | S6 changeset, S5 task spec (scope), pyproject.toml (~1k) | Everything else | Mechanical verification only |
| S8: Review | L3-4 | S7 VBR, S6 changeset, S5 spec, git diff, rules (~4k) | Full arch docs, vision, plan, upstream artifacts | Fresh eyes, not accumulated context |
| S9: Capture | L1-2 | S8 review, DECISIONS, PROGRESS, git log (~2k) | Source code, tests | System-level capture, not code |

***
## Future: Artifacts as `know` Atoms
When the `know` module is built, each artifact naturally maps to atom types:

| Artifact | `know` Atom Type | Connections |
|----------|------------------|-------------|
| Intake Brief | `INTAKE` | → `USE_CASE`, → `MODULE` |
| Constraints Sheet | `CONSTRAINT` | → `INTAKE`, → `DECISION` |
| Options Sheet | `OPTION` | → `INTAKE`, → `CONSTRAINT` |
| Decision Record | `DECISION` | → `OPTION`, → `INTAKE` |
| Task Spec | `TASK` | → `DECISION`, → `USE_CASE` |
| Change Set | `CHANGE` | → `TASK` |
| VBR Report | `VERIFICATION` | → `TASK`, → `CHANGE` |
| Review Report | `REVIEW` | → `TASK`, → `CHANGE` |
| Capture Record | `CAPTURE` | → `DECISION`, → `TASK`, → `LESSON` |
| Lesson | `LESSON` | → `CAPTURE`, → `MODULE` |

This means `kb.subgraph(related_to="NF-01")` would return the entire chain: use case → intake → decision → tasks → reviews → lessons. The traceability is built into the data model.[^9]

---

## References

1. [Agent Handoff Patterns: A Case Study in Multi-Step Workflows](https://getathenic.com/blog/agent-handoff-patterns-case-study) - Real-world analysis of agent handoff patterns from Athenic's multi-agent system -when to handoff, ho...

2. [Handoff Orchestration (HO) - Agentic Design Patterns](https://agentic-design.ai/patterns/multi-agent/handoff-orchestration) - Dynamic delegation where agents intelligently transfer control based on context and specialized capa...

3. [Best practices for Claude Code subagents - PubNub](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/) - 1) Clear, visible handoffs · 2) Review the slug, not just prose · 3) Pause, resume, or branch intent...

4. [Artifact-First Engineering: The Workflow That Replaced "Vibe Coding"](https://www.linkedin.com/pulse/artifact-first-engineering-workflow-replaced-vibe-coding-john-kehoe-ufgvc) - It also makes handoffs to other people (or other AI tools) possible for the first time. And it sets ...

5. [Design Phase in SDLC: Key Activities, Types & Examples](https://teachingagile.com/sdlc/design) - Complete guide to the design phase in software development. Learn key activities (HLD, LLD, UI desig...

6. [IEEE 12207 Software Life Cycle](https://cursa.ihmc.us/rid=1KBBSFCWH-1Q4C9MY-15QN/cs460%20ieee12207.pdf)

7. [How does Claude Code decide what context goes into subagents?](https://www.reddit.com/r/ClaudeAI/comments/1myki1h/how_does_claude_code_decide_what_context_goes/) - How does Claude Code decide what context goes into subagents?

8. [Requirement Analysis in SDLC: Steps & Techniques - Teaching Agile](https://teachingagile.com/sdlc/requirement-analysis) - Master requirement analysis in software development. Learn the 6-step process, gathering techniques ...

9. [Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LL.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/67744cb3-570d-4a0e-9547-4e0af858b4d2/Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LLM-Empowered-Agentic.pdf?AWSAccessKeyId=ASIA2F3EMEYE24XEHMNF&Signature=v1Mie37YvASo2s7Er4Jq0PrNQHs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH0aCXVzLWVhc3QtMSJGMEQCIDvNzksH79QGTMHf7Kpt6HW1TkJBwpOVpfF%2FBulLsnPjAiAPtq%2FnfPOv8NgORFt8jxcgrpjAOJde9ynBqMuMHcaCfirzBAhGEAEaDDY5OTc1MzMwOTcwNSIMCbYvHcA3MmYxesKUKtAEGfEsLpMdGjn7gK1VAH%2BVV%2B08O4QRuaIZIsOUr48eOgjeyBl6%2Fx2FnMV9Cdp2Fao4K%2B5BQj0XmN%2BwfVFys4V1KQ4vnNoLQGhWaAG71tlEb0OB%2FLoJM6wKkDXuYlxfS%2BGGlZ9u7TWzGKQp3j%2Fu8P%2B%2BOGM15sKoUPfgEnIvT57kfn6IhF32duTf%2F9n3S9qONPaFkPoj0OdbObT7%2FY5EnXTK5%2BjcflZ%2FxM3rCzg64G02qqhrkrB4x1GEJvwbSL0CytQzfy5KV92D5RuYqMOsHzbXKqfgbHeohxypOta790%2FtqWfCm26lq7UUC5cLiQU1c6j8Sf67gvzJRPhXoRxi%2BJIPnUTlfV%2BUxjqxKXOLTMTi1ey56UcJvQ2oU%2BtloA6HPEQFHoOqJSqi%2BNujxnIuYxGB0i72s%2BpzcpYkfVxfLpO4sLkaVu7wcaLh0dH84e1lTWi2DUyKc3WFIGmXHMgzKwz14xED0P9HMuvQMFKoHaamoEvn1AKHgldSGvYBkjc8IelPQ3GwFLccpMCrPef1FTgsRL0ddzz86QbVbhQj2LpKEg5IPTOaTcm%2FLvXrSruwQdf4dNd7XWBH3N6xAN3fixCcy%2FIczDv%2F5wH9JdPnlmRRsygIHI14assrWZ23k30%2B%2FMZcToEBrP98jkJkKs%2FKuRR4XjfcWz5XhuTvwzLDWEApBbRb%2FbUDwwTIob1Hbvjr%2BVgYy5xm%2BzEpQAquNVfkgLHaJ8zp4DdZHvMhg%2FSXjY7YQnU8LqlxMAj14v69R8dNf9c47xgdqxJx4VNkNC4FUuapKzCZpsDNBjqZARxaPFJe9oJe4fENqPI7TBX8b%2FUvBfn7K1yaiVA41RE7LJJkQjAotbnCaknnr9XkrmJKKgj7Ferg1LsSQkkYFwIl55B5rUFATXkjl7%2B023PunJBJuFjW1LQTdx3yVN3lttIwViutPA86DoPMb3Qp4exYp0WWQYssKaRq981YF2t3pr3psoV%2BUT%2BW4Wpf5OyEh0XOV6OoSyMBkA%3D%3D&Expires=1773152442) - A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic ...

