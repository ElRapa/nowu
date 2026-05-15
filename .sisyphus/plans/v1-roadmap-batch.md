# v1 Roadmap Batch: Domain Validation + Know Integration + ADR Promotion

## TL;DR

> **Quick Summary**: Execute 5 v1 roadmap tasks (W28→W19→W20→K3→W9) to validate nowu across a second domain, formalize domain extension and traceability patterns as ADRs, connect the `know` module for runtime knowledge persistence, and promote hypothesis ADRs to evidence-based. Includes double-agent experiments on W28 and K3 comparing workflow-driven vs freeform approaches.
> 
> **Deliverables**:
> - W28: RE domain bootstrap (intake-008 + gap comparison vs W27)
> - W19: ADR-0011 domain extension model
> - W20: ADR-0012 traceability metadata standard
> - K3: MemoryService integration (first runtime know↔nowu bridge)
> - W9: Hypothesis ADR promotion (ADR-0007..0010 → evidence-based)
> - Double-agent comparison learnings for W28 and K3
> - Session-learning docs after each task
> 
> **Estimated Effort**: Large (5 roadmap items across architecture + implementation)
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: W28 → W19 → K3 → commit

---

## Context

### Original Request
Execute 3-6 roadmap tasks from ROADMAP-004 to advance v1. Dogfood the nowu S1-S9 workflow using repo-defined agents/skills. Run double-agent experiments comparing workflow agents vs freeform approach. Create commits and session-learning docs. Track models and agents fired per task.

### Interview Summary
**Key Discussions**:
- User confirmed all 5 tasks (W28, W19, W20, K3, W9)
- Double-agent experiments on BOTH W28 and K3
- Double-agent comparison = repo-workflow agents vs "just do it" freeform
- Session persistence tasks (task-001..005) deferred to next batch
- User updated session-log from old session before this planning session
- W27 already established dual-agent evaluation pattern (see session-2026-05-15-dual-agent-evaluation.md)

**Research Findings**:
- know module (v0.4.0) provides full KnowledgeAtom CRUD, connections, search, curator, embeddings
- MemoryService Protocol currently has 4 methods using generic types (str, dict, list[Any])
- .claude/skills/ has full-cycle, implement-loop, single-step skills with orchestration instructions
- .claude/agents/ has 35 agent specs with altitude/phase frontmatter
- 2 completed intakes (001, 007), 7 completed tasks, 5 intakes in arch queue
- GAP-001 (MemoryService too narrow) + GAP-002 (no atom CRUD) are K3's evidence base

### Metis Review
**Identified Gaps** (addressed):
- **K1 dependency**: K1 is ACTIVE (ongoing baseline), not one-shot. W20/K3 not blocked.
- **core→know imports**: MemoryService uses generic types (Any, str, dict). K3 adapter in bridge/ casts to know types. No boundary violation.
- **W28 output format**: Follows W27 pattern → produces intake-008 through S1-S9. Third completed intake.
- **"Systemic" criteria**: Gap is systemic if it manifests in ≥2 domains with equivalent structural impact.
- **W9 intake count**: "2+ intakes" from roadmap is met now (001, 007). After W28 → 3 intakes. W9 can proceed.
- **K3 method list**: Expand MemoryService with atom CRUD + query + connections (7 methods max). Keep generic types.
- **Decay mismatch (GAP-007)**: ADR-0010 says 90d, know says 180d. W20 notes this for resolution. K3 does NOT resolve it.
- **Skill files**: .claude/skills/ exists with full-cycle, implement-loop, session-learning, etc. Agent specs in .claude/agents/.
- **E1 (gaps not systemic)**: Batch proceeds regardless. W19/W20 note asymmetric findings if applicable.
- **E2 (core→know types)**: TYPE_CHECKING not needed — Protocol already uses Any. Adapter in bridge/ handles casting.

### ROADMAP-004 v5 Update (Know Internal Items)
ROADMAP-004 was updated to v5 in parallel, adding KI-1..KI-5 (Know Internal work items for `../know` sibling repo). Impact on this plan:
- **KI-3 (depends K3)**: Downstream consumer — expands KnowAdapter on know-side AFTER K3 creates the nowu-side Protocol + adapter. K3 should design the adapter interface to be KI-3-extensible (clean method signatures, not monolithic).
- **KI-4 (depends W19)**: Downstream consumer — implements domain atom type registry in know based on W19's extension model. W19 should specify type extensibility requirements that KI-4 can implement.
- **KI-1/KI-2**: No deps on our tasks, know-side only, no plan impact.
- **KI-5**: v1.1, out of scope.
- **No structural changes to this plan.** Our tasks are upstream producers; KI items are downstream consumers.

---

## Work Objectives

### Core Objective
Advance v1 critical path by validating nowu's domain generality, formalizing architecture patterns, and connecting the knowledge layer.

### Concrete Deliverables
- `state/intake/intake-008.md` — RE domain intake (W28)
- Full S1-S9 artifact chain for intake-008 in `state/arch/`, `state/tasks/`, `state/reviews/`, `state/capture/`
- `state/arch/w28-gap-comparison.md` — systemic vs AP-specific gap classification
- `docs/architecture/adr/ADR-0011-domain-extension-model.md` (W19)
- `docs/architecture/adr/ADR-0012-traceability-metadata-standard.md` (W20)
- Expanded `src/nowu/core/contracts/memory.py` — MemoryService with atom CRUD (K3)
- `src/nowu/bridge/know_adapter.py` — KnowAdapter implementing MemoryService (K3)
- `tests/` — TDD tests for K3 adapter
- Updated `docs/architecture/adr/ADR-0007..0010` — promoted status/grade metadata (W9)
- `state/learnings/session-*-dual-agent-*.md` — comparison learnings for W28 + K3
- Session-learning docs after each of the 5 tasks

### Definition of Done
- [ ] All 5 roadmap items marked ✅ DONE in ROADMAP-004
- [ ] `uv run pytest && uv run mypy src/ --strict && uv run ruff check .` passes
- [ ] 3+ completed intakes exist (after W28)
- [ ] MemoryService Protocol expanded and adapter passes tests (K3)
- [ ] ≥1 hypothesis ADR promoted to higher grade (W9)
- [ ] All feature branches merged or ready for merge

### Must Have
- W28 must produce comparative analysis against W27 gap register
- K3 MemoryService expansion uses ONLY generic types in Protocol (no know imports in core)
- K3 adapter lives in `src/nowu/bridge/` (import boundary compliance)
- Double-agent experiments on W28 and K3 with pre-defined comparison dimensions
- Session-learning after each task using repo's session-learning skill format
- Each task on a feature branch per D-025

### Must NOT Have (Guardrails)
- **NO full know API exposure in K3** — limit to 7 methods max (atom CRUD + query + connections)
- **NO code changes in W28, W19, W20, W9** — these produce documentation/ADR artifacts only
- **NO architecture bleed in W28 S1** — keep intake at problem level per W27 insight
- **NO content rewriting in W9** — promotion is metadata change + evidence linkage only
- **NO shared context in double-agent experiments** — workflow agent gets zero hints from freeform agent and vice versa
- **NO decay semantics resolution in this batch** — GAP-007 noted in W20 but deferred to K12
- **NO session persistence implementation** — deferred to next batch (task-001..005)
- **NO know type imports in core/** — Protocol uses generic types, adapter in bridge/ casts

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.
> Acceptance criteria requiring "user manually tests/confirms" are FORBIDDEN.

### Test Decision
- **Infrastructure exists**: YES (pytest + mypy + ruff via uv)
- **Automated tests**: TDD for K3 (mandatory per D-004). Architecture tasks (W28/W19/W20/W9) verified by artifact existence + fitness tests.
- **Framework**: pytest (unittest.TestCase style), mypy --strict, ruff check

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Architecture tasks (W28/W19/W20/W9)**: Use Bash — validate artifact existence, frontmatter correctness, cross-references
- **Code task (K3)**: Use Bash — run pytest, mypy, ruff, import boundary test, adapter smoke test
- **Session-learnings**: Use Bash — validate file exists, INDEX.md updated, required sections present

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — W28 full S1-S9 cycle):
├── Task 1: W28-workflow — RE domain bootstrap via S1-S9 workflow agents [deep]
├── Task 2: W28-freeform — Same goal via freeform approach (double-agent) [deep]
└── Task 3: W28-compare — Compare outputs, record learnings [quick]
   (Tasks 1+2 run in parallel, Task 3 after both complete)

Wave 2 (After W28 — architecture ADRs, MAX PARALLEL):
├── Task 4: W19 — ADR-0011 domain extension model [deep]
├── Task 5: W20 — ADR-0012 traceability metadata standard [deep]
└── Task 6: W9 — Hypothesis ADR promotion [unspecified-high]
   (All three can run in parallel — independent work)

Wave 3 (After W19 — K3 implementation):
├── Task 7: K3-workflow — MemoryService integration via workflow agents [deep]
├── Task 8: K3-freeform — Same goal via freeform approach (double-agent) [deep]
└── Task 9: K3-compare — Compare outputs, record learnings [quick]
   (Tasks 7+8 run in parallel, Task 9 after both complete)

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| T1 (W28-workflow) | — | T3, T4, T5, T6 | 1 |
| T2 (W28-freeform) | — | T3 | 1 |
| T3 (W28-compare) | T1, T2 | — | 1 |
| T4 (W19) | T1 (needs W28 evidence) | T7 | 2 |
| T5 (W20) | T1 (needs W28 evidence) | — | 2 |
| T6 (W9) | T1 (needs intake-008) | — | 2 |
| T7 (K3-workflow) | T4 (W19 shapes contract) | T9, F1-F4 | 3 |
| T8 (K3-freeform) | T4 (W19 shapes contract) | T9 | 3 |
| T9 (K3-compare) | T7, T8 | — | 3 |
| F1-F4 | T1-T9 | — | FINAL |

### Agent Dispatch Summary

- **Wave 1**: 3 tasks — T1 → `deep`, T2 → `deep`, T3 → `quick`
- **Wave 2**: 3 tasks — T4 → `deep`, T5 → `deep`, T6 → `unspecified-high`
- **Wave 3**: 3 tasks — T7 → `deep`, T8 → `deep`, T9 → `quick`
- **FINAL**: 4 tasks — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

### Double-Agent Experiment Protocol

For W28 and K3, two agents run in parallel with IDENTICAL acceptance criteria but DIFFERENT approaches:

**Agent A (Workflow)**: Receives ONLY the repo's .claude/skills/full-cycle/SKILL.md instructions + the intake brief. Follows S1-S9 step by step using .claude/agents/ specs. Gets ZERO additional context from the orchestrator beyond what the workflow defines. Models and agents fired are tracked.

**Agent B (Freeform)**: Receives the same goal/acceptance criteria but NO workflow structure. Works as a normal subagent would — reads what it needs, produces deliverables however it sees fit. Models and agents fired are tracked.

**Comparison Dimensions** (measured for both):
1. **Time**: Wall-clock duration per task
2. **Artifact quality**: Completeness, accuracy, specificity (scored 1-5)
3. **Blindspot detection**: Issues found by post-review that the agent missed
4. **Process overhead**: Number of tool calls, files read, intermediate artifacts
5. **Evidence depth**: Concreteness of examples, data references, cross-links

### Session-Learning Protocol

After EACH of the 5 roadmap tasks (not each sub-task), produce:
- `state/learnings/session-YYYY-MM-DD-{task-slug}.md` following `.claude/skills/session-learning/SKILL.md` format
- Update `state/learnings/INDEX.md`
- Include: models used, agents fired, friction points, decisions made, comparison insights (for double-agent tasks)

### Commit Strategy

Per D-025 (branch strategy):
- Each roadmap item gets branch: `feat/W28`, `feat/W19`, `feat/W20`, `feat/K3`, `feat/W9`
- Double-agent experiments: use the BETTER output as the committed result (document why in session-learning)
- Merge order follows dependency: W28 first → W19/W20/W9 → K3
- Merges to main are Tier 3 (human-gated) — present batch for merge review at end

---

## TODOs

- [x] 1. W28-workflow — RE Domain Bootstrap via S1-S9 Workflow Agents

  **What to do**:
  - Follow `.claude/skills/full-cycle/SKILL.md` orchestration steps with the overrides listed below
  - Load ONLY what each step specifies (context scoping rules)
  - S1: Create intake-008 from RE-01 (Inventory Existing Processes) and RE-06 (Support Long-Term Investment Decision Tracking) use cases
  - S2-S4: Architecture analysis, options, decision — compare constraints against W27 pattern
  - S5: Shape 1-3 tasks for RE domain evidence artifacts
  - S6-S7: Implement evidence artifacts (validation docs, NOT code) following TDD where applicable
  - S8: Review with Oracle pre-review (per D-SESS-01 from W27 learnings)
  - S9: Capture, update roadmap, session-log
  - Key output: `state/arch/w28-gap-comparison.md` classifying each of GAP-001..007 as systemic or AP-specific
  - Classification criterion: gap is "systemic" if it manifests in ≥2 domains with equivalent structural impact
  - Apply W27 D-SESS-01 guardrails: S1 architecture-bleed prevention, S2 blindspot reporting, Oracle pre-review before S8

  **Workflow Overrides (MANDATORY — full-cycle SKILL.md has stale references)**:
  - Replace `docs/STAGED-PLAN.md` → `docs/ROADMAP-004.md` (STAGED-PLAN.md does not exist)
  - Replace `docs/ARCHITECTURE.md` → `docs/architecture/ARCHITECTURE-VISION.md` (ARCHITECTURE.md does not exist)
  - Replace ALL `docs/ROADMAP-003.md` → `docs/ROADMAP-004.md` (ROADMAP-003 superseded by ROADMAP-004 v5)
  - **S4 human gate → self-approve**: Agent evaluates decision quality and auto-proceeds if sound. User instruction: "Try to do everything by yourself."
  - **S5 human gate → self-approve**: Agent evaluates shaped tasks and auto-proceeds. Same user instruction applies.
  - These overrides exist because the skill file has not been updated to match current repo state. The S1-S9 workflow PATTERN is still followed faithfully.

  **Must NOT do**:
  - Write ANY Python code (this is a documentation/evidence task)
  - Load src/ during S1-S4 (context scoping rule)
  - Mix problem framing with architecture in S1 (W27 Insight 1)
  - Share ANY context with the freeform agent (T2)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Full S1-S9 cycle requires thorough research and multi-step orchestration
  - **Skills**: []
    - Agent receives ONLY the full-cycle skill text and agent specs from .claude/ as its instructions
  - **Skills Evaluated but Omitted**:
    - All opencode skills omitted — this agent must follow ONLY the repo's workflow definitions

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 2)
  - **Parallel Group**: Wave 1
  - **Blocks**: T3 (comparison), T4 (W19), T5 (W20), T6 (W9)
  - **Blocked By**: None (can start immediately)

  **References**:

  **Pattern References**:
  - `.claude/skills/full-cycle/SKILL.md` — The exact orchestration steps this agent must follow
  - `.claude/agents/nowu-intake.md` — S1 agent spec (intake creation)
  - `.claude/agents/nowu-constraints.md` — S2 agent spec
  - `.claude/agents/nowu-options.md` — S3 agent spec
  - `.claude/agents/nowu-decider.md` — S4 agent spec
  - `.claude/agents/nowu-shaper.md` — S5 agent spec
  - `.claude/agents/nowu-reviewer.md` — S8 agent spec
  - `.claude/agents/nowu-curator.md` — S9 agent spec
  - `state/intake/intake-007.md` — W27 intake pattern to follow for structure
  - `state/arch/intake-007-gap-register.md` — The gap register W28 must compare against

  **API/Type References**:
  - `docs/USE_CASES.md` — RE-01 and RE-06 use case definitions (search for "RE-01" and "RE-06")
  - `docs/architecture/adr/ADR-0008-knowledge-atom-model.md` — Knowledge model constraints
  - `docs/architecture/adr/ADR-0009-orchestration-protocol.md` — Orchestration constraints

  **External References**:
  - `state/learnings/session-2026-05-15-dual-agent-evaluation.md` — W27 dual-agent learnings (Insights 1-9 and D-SESS-01/02)
  - `state/capture/capture-intake-007.md` — W27 capture with next_cycle_trigger → W28
  - `docs/ROADMAP-004.md` Section 7 — W28 framing and validation_goal

  **WHY Each Reference Matters**:
  - full-cycle SKILL.md is the EXACT workflow this agent follows — no deviation allowed
  - intake-007 artifacts are the structural pattern W28 must mirror for RE domain
  - gap-register is what W28 must compare against — the whole point is systemic vs AP-specific
  - W27 dual-agent learnings contain guardrails that must be applied (D-SESS-01, D-SESS-02)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Intake-008 created with correct structure
    Tool: Bash
    Preconditions: Agent has completed S1
    Steps:
      1. Check file exists: `ls state/intake/intake-008.md`
      2. Validate frontmatter: `head -20 state/intake/intake-008.md` — must contain artifact_type: INTAKE_BRIEF, status field, uc_ids containing RE-01 and RE-06
      3. Verify no architecture bleed: grep for "ADR", "schema", "module" in first 30 lines — should be 0 or minimal
    Expected Result: File exists with correct frontmatter, problem-level framing, RE-01 and RE-06 referenced
    Evidence: .sisyphus/evidence/task-1-intake-008-structure.txt

  Scenario: Gap comparison document classifies all 7 gaps
    Tool: Bash
    Preconditions: Agent has completed S6
    Steps:
      1. Check file exists: `ls state/arch/w28-gap-comparison.md` (or similar path)
      2. Verify all 7 gaps addressed: grep for "GAP-001", "GAP-002", ... "GAP-007"
      3. Verify classification: grep for "systemic" or "domain-specific" — each gap must have one
      4. Verify RE-01 and RE-06 evidence cited
    Expected Result: All 7 gaps classified with RE domain evidence
    Evidence: .sisyphus/evidence/task-1-gap-comparison.txt

  Scenario: Full S1-S9 artifact chain exists
    Tool: Bash
    Preconditions: Agent has completed S9
    Steps:
      1. Check: `ls state/arch/intake-008-constraints.md state/arch/intake-008-options.md state/arch/intake-008-decision.md`
      2. Check: `ls state/reviews/` for intake-008 review
      3. Check: `ls state/capture/capture-intake-008.md`
      4. Verify roadmap updated: grep "W28" docs/ROADMAP-004.md | grep -i "done"
    Expected Result: Complete artifact chain from intake to capture
    Evidence: .sisyphus/evidence/task-1-artifact-chain.txt
  ```

  **Commit**: YES
  - Message: `feat(workflow): W28 RE domain bootstrap — second-domain validation`
  - Branch: `feat/W28`
  - Files: `state/intake/intake-008.md`, `state/arch/intake-008-*.md`, `state/tasks/task-014+.md`, `state/reviews/`, `state/capture/capture-intake-008.md`
  - Pre-commit: `uv run pytest --tb=short -q`

- [x] 2. W28-freeform — RE Domain Bootstrap via Freeform Approach

  **What to do**:
  - Achieve the IDENTICAL goal as Task 1 but WITHOUT following S1-S9 workflow structure
  - Read RE-01 and RE-06 use cases, existing ADRs, and W27 gap register
  - Produce the same deliverables (intake brief, gap comparison, evidence artifacts) however you see fit
  - No prescribed step order, no agent specs, no context scoping rules
  - Track: time spent, files read, approach taken, artifacts produced
  - Save outputs to `.sisyphus/evidence/w28-freeform/` (NOT to state/ — only workflow version goes to state/)

  **Must NOT do**:
  - Read ANY .claude/skills/ or .claude/agents/ files (no workflow contamination)
  - Share ANY context with the workflow agent (T1)
  - Write to state/ directories (only the workflow version's outputs get committed)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Needs thorough analysis to match workflow agent's depth without structure
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1)
  - **Parallel Group**: Wave 1
  - **Blocks**: T3 (comparison)
  - **Blocked By**: None

  **References**:
  - `docs/USE_CASES.md` — RE-01 and RE-06 definitions
  - `docs/architecture/adr/ADR-0008-knowledge-atom-model.md`
  - `docs/architecture/adr/ADR-0009-orchestration-protocol.md`
  - `state/arch/intake-007-gap-register.md` — Gaps to classify
  - `docs/ROADMAP-004.md` — W28 validation goal

  **Acceptance Criteria**:

  ```
  Scenario: Freeform produces equivalent deliverables
    Tool: Bash
    Steps:
      1. Check: `ls .sisyphus/evidence/w28-freeform/` — should contain intake brief, gap comparison, evidence docs
      2. Verify gap comparison covers all 7 gaps
      3. Verify RE-01 and RE-06 use cases are addressed
    Expected Result: Equivalent set of deliverables in evidence directory
    Evidence: .sisyphus/evidence/task-2-freeform-deliverables.txt
  ```

  **Commit**: NO (outputs saved to .sisyphus/evidence/ only — workflow version is the committed output)

- [x] 3. W28-compare — Double-Agent Comparison & Session-Learning

  **What to do**:
  - Compare T1 (workflow) and T2 (freeform) outputs along 5 dimensions:
    1. Time (wall-clock duration)
    2. Artifact quality (completeness, accuracy, specificity — scored 1-5)
    3. Blindspot detection (issues found by post-review that agent missed)
    4. Process overhead (tool calls, files read, intermediate artifacts)
    5. Evidence depth (concreteness of examples, data references, cross-links)
  - Produce comparison document
  - Run session-learning per `.claude/skills/session-learning/SKILL.md` format
  - Record models used and agents fired for both approaches
  - If freeform produces BETTER gap comparison, incorporate improvements into committed workflow output

  **Must NOT do**:
  - Skip any comparison dimension
  - Produce subjective "workflow is better" without evidence

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Analysis of two existing outputs, no new artifacts
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (after T1+T2)
  - **Blocks**: None
  - **Blocked By**: T1, T2

  **References**:
  - `.sisyphus/evidence/w28-freeform/` — Freeform outputs to compare
  - `state/` — Workflow outputs to compare
  - `state/learnings/session-2026-05-15-dual-agent-evaluation.md` — Previous comparison format
  - `.claude/skills/session-learning/SKILL.md` — Learning capture format

  **Acceptance Criteria**:

  ```
  Scenario: Comparison document complete
    Tool: Bash
    Steps:
      1. Check: `ls state/learnings/session-*-w28-dual-agent.md`
      2. Verify all 5 dimensions scored/assessed
      3. Verify models and agents listed
    Expected Result: Complete comparison with quantified scores
    Evidence: .sisyphus/evidence/task-3-comparison.txt

  Scenario: Session-learning for W28 created
    Tool: Bash
    Steps:
      1. Check: `ls state/learnings/session-*-w28*.md`
      2. Check INDEX updated: `grep "w28" state/learnings/INDEX.md`
    Expected Result: Learning file exists, INDEX updated
    Evidence: .sisyphus/evidence/task-3-session-learning.txt
  ```

  **Commit**: YES (amend onto feat/W28 branch)
  - Message: `docs(learnings): W28 dual-agent comparison + session-learning`
  - Files: `state/learnings/session-*-w28*.md`, `state/learnings/INDEX.md`

- [x] 4. W19 — ADR-0011 Domain Extension Model

  **What to do**:
  - Use S2-S4 workflow pattern (constraints → options → decision) to produce ADR-0011
  - Input: W28's gap comparison (systemic vs AP-specific findings) + W27 gap register (GAP-003, GAP-005)
  - Analyze: How should nowu handle adding a NEW domain beyond AP/RE?
  - Define: Extension points in contracts, artifact templates, agent configurations
  - Must show applicability to BOTH AP and RE with concrete examples
  - Must NOT require changes to core/ — extension happens via bridge/ and configuration
  - ADR status: HYPOTHESIS (per existing ADR pattern)
  - Also produce session-learning after completion

  **Must NOT do**:
  - Write Python code (ADR only)
  - Propose changes to core/contracts/ that break import boundaries
  - Over-engineer — this is a HYPOTHESIS ADR, not a full spec

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Architecture-level analysis requiring synthesis of W27+W28 evidence across domain patterns
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - architecture-only skill: Would be ideal but is a repo-specific Claude Code skill. Agent should read `.claude/skills/architecture-only/SKILL.md` for guidance.

  **Parallelization**:
  - **Can Run In Parallel**: YES (with T5 and T6)
  - **Parallel Group**: Wave 2
  - **Blocks**: T7 (K3 — W19 shapes what MemoryService must support)
  - **Blocked By**: T1 (W28 evidence needed)

  **References**:
  - `state/arch/w28-gap-comparison.md` — Systemic vs AP-specific classification (from T1)
  - `state/arch/intake-007-gap-register.md` — GAP-003 (evidence model thin) + GAP-005 (no domain extension mechanism)
  - `docs/architecture/adr/ADR-0008-knowledge-atom-model.md` — Current knowledge model W19 must extend
  - `docs/architecture/adr/ADR-0009-orchestration-protocol.md` — Orchestration constraints
  - `src/nowu/core/contracts/memory.py` — Current MemoryService Protocol (4 methods) that K3 will expand
  - `src/nowu/core/boundaries.py` — Import boundary rules W19 must respect
  - `docs/architecture/adr/ADR-0001-*.md` through `ADR-0006-*.md` — Existing accepted ADRs for pattern reference

  **WHY Each Reference Matters**:
  - W28 gap comparison determines WHETHER gaps are systemic (shaping the extension model's scope)
  - GAP-003/005 are the specific evidence that W19 must resolve
  - ADR-0008 is what W19 EXTENDS — must be compatible
  - boundaries.py ensures extension doesn't violate import rules

  **Downstream Consumer**: KI-4 (in `../know`) will implement a domain atom type registry based on W19's extension model. W19 should specify type extensibility requirements clearly enough for KI-4 to implement without ambiguity.

  **Acceptance Criteria**:

  ```
  Scenario: ADR-0011 created with correct structure
    Tool: Bash
    Steps:
      1. Check: `ls docs/architecture/adr/ADR-0011-domain-extension-model.md`
      2. Validate frontmatter: must have status: PROPOSED, epistemic_grade: HYPOTHESIS
      3. Verify GAP-003 and GAP-005 referenced: `grep -c "GAP-003\|GAP-005" docs/architecture/adr/ADR-0011*.md` — expect ≥2
      4. Verify AP and RE examples present: `grep -c "AP\|RE" docs/architecture/adr/ADR-0011*.md` — expect ≥4
      5. Verify no core/ changes proposed: grep for "core/contracts" should appear only in "does not change" or "compatible with" context
    Expected Result: ADR-0011 exists, HYPOTHESIS grade, addresses both gaps, shows AP+RE examples
    Evidence: .sisyphus/evidence/task-4-adr-0011.txt

  Scenario: Session-learning for W19 created
    Tool: Bash
    Steps:
      1. Check: `ls state/learnings/session-*-w19*.md`
      2. Check INDEX: `grep -i "w19\|domain.extension" state/learnings/INDEX.md`
    Expected Result: Learning file exists, INDEX updated
    Evidence: .sisyphus/evidence/task-4-session-learning.txt
  ```

  **Commit**: YES
  - Message: `docs(architecture): ADR-0011 domain extension model (W19, GAP-003/005)`
  - Branch: `feat/W19`
  - Files: `docs/architecture/adr/ADR-0011-domain-extension-model.md`, `state/learnings/session-*-w19*.md`
  - Pre-commit: `uv run pytest --tb=short -q`

- [x] 5. W20 — ADR-0012 Traceability Metadata Standard

  **What to do**:
  - Use S2-S4 workflow pattern to produce ADR-0012
  - Input: W28 evidence chain + W27 gap register (GAP-003, GAP-007) + K2 trace validation findings
  - Define: Standard metadata fields that every artifact must carry for traceability
  - Map to NF-09: "every deliverable traces back to a UC"
  - Address GAP-007: NOTE the decay semantics mismatch (ADR-0010: 90d vs know: 180d) but DO NOT resolve it — defer to K12
  - Address GAP-003: Define how evidence chains link decision records to domain atoms
  - ADR status: HYPOTHESIS
  - Also produce session-learning

  **Must NOT do**:
  - Resolve the decay semantics mismatch (GAP-007 resolution deferred to K12)
  - Write Python code
  - Contradict existing ADR-0010 epistemic grade assignments

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Must synthesize trace evidence from 2 completed intakes + ADR constraints
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with T4 and T6)
  - **Parallel Group**: Wave 2
  - **Blocks**: None directly (K3 benefits from but doesn't block on W20)
  - **Blocked By**: T1 (W28 evidence needed)

  **References**:
  - `state/arch/intake-007-gap-register.md` — GAP-003 (evidence model thin) + GAP-007 (decay mismatch)
  - `state/arch/k2-trace-validation.md` — K2 findings on current trace gaps
  - `docs/architecture/adr/ADR-0009-orchestration-protocol.md` — Orchestration metadata constraints
  - `docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md` — Grade model (do not contradict)
  - `state/arch/w5-5x10-validation.md` — W5 artifact_type vocabulary proposal
  - `docs/USE_CASES.md` — NF-09 definition (traceability requirement)
  - `state/arch/w28-gap-comparison.md` — W28 evidence chain for RE domain (from T1)

  **WHY Each Reference Matters**:
  - GAP-003/007 are the specific evidence W20 resolves/notes
  - K2 found 3 non-blocking trace observations — W20 should formalize solutions
  - ADR-0010 must not be contradicted (existing binding decision)
  - W5's artifact_type vocabulary is a precursor to the metadata standard

  **Acceptance Criteria**:

  ```
  Scenario: ADR-0012 created with correct structure
    Tool: Bash
    Steps:
      1. Check: `ls docs/architecture/adr/ADR-0012-traceability-metadata-standard.md`
      2. Validate frontmatter: status: PROPOSED, epistemic_grade: HYPOTHESIS
      3. Verify GAP-003 referenced: `grep -c "GAP-003" docs/architecture/adr/ADR-0012*.md` — expect ≥1
      4. Verify GAP-007 noted but deferred: `grep -i "GAP-007\|decay\|defer" docs/architecture/adr/ADR-0012*.md` — expect ≥2
      5. Verify NF-09 mapped: `grep "NF-09" docs/architecture/adr/ADR-0012*.md` — expect ≥1
    Expected Result: ADR-0012 exists, addresses GAP-003, notes GAP-007 deferral, maps to NF-09
    Evidence: .sisyphus/evidence/task-5-adr-0012.txt

  Scenario: Session-learning for W20 created
    Tool: Bash
    Steps:
      1. Check: `ls state/learnings/session-*-w20*.md`
      2. Check INDEX: `grep -i "w20\|traceability" state/learnings/INDEX.md`
    Expected Result: Learning file exists, INDEX updated
    Evidence: .sisyphus/evidence/task-5-session-learning.txt
  ```

  **Commit**: YES
  - Message: `docs(architecture): ADR-0012 traceability metadata standard (W20, GAP-003/007)`
  - Branch: `feat/W20`
  - Files: `docs/architecture/adr/ADR-0012-traceability-metadata-standard.md`, `state/learnings/session-*-w20*.md`
  - Pre-commit: `uv run pytest --tb=short -q`

- [x] 6. W9 — Promote Hypothesis ADRs via Intake Evidence

  **What to do**:
  - Evaluate each hypothesis ADR (0007-0010) against cumulative intake evidence (001, 007, 008)
  - For each ADR: map which intake provided supporting evidence, which gaps/risks remain
  - Promote qualifying ADRs from HYPOTHESIS → INFORMED_ESTIMATE (or EVIDENCE_BASED if strongly supported)
  - Promotion = metadata change (status, epistemic_grade, evidence links) + brief evidence summary section
  - Do NOT rewrite ADR decision text — only add evidence linkage and update grade
  - Minimum: promote ≥1 ADR. If only 1 qualifies, mark W9 as partial-complete with justification.
  - Also produce session-learning

  **Must NOT do**:
  - Rewrite ADR decision content (grade/metadata changes only)
  - Promote without specific intake evidence (must cite intake-NNN + specific finding)
  - Promote to EVIDENCE_BASED without ≥2 intakes confirming the pattern
  - Demote any ADR (only promote or leave unchanged)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Evidence evaluation task requiring careful analysis but no code
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with T4 and T5)
  - **Parallel Group**: Wave 2
  - **Blocks**: None (W12/W14 are v1.1)
  - **Blocked By**: T1 (W28 produces intake-008 evidence)

  **References**:
  - `docs/architecture/adr/ADR-0007-session-continuity-protocol.md` — Evaluate against intake-001 session findings
  - `docs/architecture/adr/ADR-0008-knowledge-atom-model.md` — Evaluate against intake-007 + intake-008 knowledge findings
  - `docs/architecture/adr/ADR-0009-orchestration-protocol.md` — Evaluate against all 3 intakes' workflow evidence
  - `docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md` — Evaluate against W29/W32 enforcement evidence
  - `state/intake/intake-001.md` — First intake evidence
  - `state/intake/intake-007.md` — AP domain intake evidence
  - `state/intake/intake-008.md` — RE domain intake evidence (from T1)
  - `state/capture/capture-intake-001.md` — Capture with lessons learned
  - `state/capture/capture-intake-007.md` — W27 capture
  - `state/arch/intake-007-gap-register.md` — Gaps that inform promotion confidence
  - `docs/model/MODEL-REFERENCE.md` §6 — Per-artifact-type thresholds (W32 output)

  **WHY Each Reference Matters**:
  - Each ADR must be evaluated against concrete intake evidence, not abstract reasoning
  - Captures contain explicit lessons learned that inform promotion confidence
  - Gap register shows where ADRs still have weaknesses (limits promotion grade)
  - MODEL-REFERENCE §6 defines what each grade means

  **Acceptance Criteria**:

  ```
  Scenario: At least 1 ADR promoted
    Tool: Bash
    Steps:
      1. For each ADR-0007..0010, check grade: `grep "epistemic_grade" docs/architecture/adr/ADR-000{7,8,9}*.md docs/architecture/adr/ADR-0010*.md`
      2. At least 1 must show grade > HYPOTHESIS (i.e., INFORMED_ESTIMATE or EVIDENCE_BASED)
      3. Each promoted ADR must have evidence section: `grep -l "intake-00[178]" docs/architecture/adr/ADR-00*.md`
    Expected Result: ≥1 ADR promoted with intake evidence linkage
    Evidence: .sisyphus/evidence/task-6-adr-promotion.txt

  Scenario: No content rewriting detected
    Tool: Bash
    Steps:
      1. Check git diff on ADR files: changes should be metadata (frontmatter) + evidence section additions only
      2. Core decision text sections should be unchanged
    Expected Result: Only metadata and evidence sections changed
    Evidence: .sisyphus/evidence/task-6-no-rewrite.txt

  Scenario: Session-learning for W9 created
    Tool: Bash
    Steps:
      1. Check: `ls state/learnings/session-*-w9*.md`
      2. Check INDEX: `grep -i "w9\|adr.promot" state/learnings/INDEX.md`
    Expected Result: Learning file exists, INDEX updated
    Evidence: .sisyphus/evidence/task-6-session-learning.txt
  ```

  **Commit**: YES
  - Message: `docs(architecture): promote hypothesis ADRs with intake evidence (W9)`
  - Branch: `feat/W9`
  - Files: `docs/architecture/adr/ADR-0007*.md`, `ADR-0008*.md`, `ADR-0009*.md`, `ADR-0010*.md`, `state/learnings/session-*-w9*.md`
  - Pre-commit: `uv run pytest --tb=short -q`

- [x] 7. K3-workflow — MemoryService Integration via Workflow Agents

  **What to do**:
  - Follow repo workflow for implementation: use S1-S5 to create intake + shape tasks, then S6-S7 for TDD implementation
  - Goal: Expand MemoryService Protocol with atom CRUD + query + connections (max 7 new methods)
  - Implement KnowAdapter in `src/nowu/bridge/know_adapter.py` that delegates to know.KnowledgeBase
  - MemoryService Protocol stays in `src/nowu/core/contracts/memory.py` using ONLY generic types (str, dict[str, Any], list[Any])
  - KnowAdapter in bridge/ handles casting between generic types and know's KnowledgeAtom
  - TDD mandatory (D-004): write failing tests FIRST, then implement
  - Run quality gates: pytest + mypy --strict + ruff check
  - Apply W27 D-SESS-01 guardrails for S8 review
  - The agent receives ONLY the repo's workflow instructions — no additional context from orchestrator
  - **CRITICAL**: Update `tests/architecture/test_adr_fitness.py` to exempt `bridge/` from the no-direct-know-import rule. Bridge IS the infrastructure adapter layer — it's architecturally CORRECT for it to import know (ADR-0001, ADR-0008). The test at line 83-119 (`test_no_direct_know_import_in_nowu_modules`) currently rejects ALL know imports under `src/nowu/`. Add an exemption for files in `src/nowu/bridge/` (the adapter boundary layer). Without this fix, K3 cannot create a working adapter AND pass the fitness test.

  **Workflow Overrides (MANDATORY — full-cycle SKILL.md has stale references)**:
  - Replace `docs/STAGED-PLAN.md` → `docs/ROADMAP-004.md` (STAGED-PLAN.md does not exist)
  - Replace `docs/ARCHITECTURE.md` → `docs/architecture/ARCHITECTURE-VISION.md` (ARCHITECTURE.md does not exist)
  - Replace ALL `docs/ROADMAP-003.md` → `docs/ROADMAP-004.md` (ROADMAP-003 superseded by ROADMAP-004 v5)
  - **S4 human gate → self-approve**: Agent evaluates decision quality and auto-proceeds if sound.
  - **S5 human gate → self-approve**: Agent evaluates shaped tasks and auto-proceeds.
  - These overrides exist because the skill file has not been updated to match current repo state.

  **New MemoryService methods (exactly these 7, keeping existing 4)**:
  1. `create_atom(self, atom_type: str, title: str, content: str, project_scope: list[str], tags: list[str] | None = None, epistemic_grade: str | None = None) -> str` — Create knowledge atom, return id
  2. `get_atom(self, atom_id: str) -> dict[str, Any] | None` — Retrieve atom by id
  3. `update_atom(self, atom_id: str, updates: dict[str, Any]) -> bool` — Update atom fields
  4. `delete_atom(self, atom_id: str) -> bool` — Delete atom
  5. `query_atoms(self, filters: dict[str, Any], limit: int = 50) -> list[dict[str, Any]]` — Query atoms with filters
  6. `add_connection(self, source_id: str, target_id: str, relation_type: str) -> str` — Add connection between atoms
  7. `get_connections(self, atom_id: str) -> list[dict[str, Any]]` — Get connections for an atom

  **Must NOT do**:
  - Import know types in core/ (use generic types only — str, dict, Any)
  - Add more than 7 new methods to MemoryService
  - Expose know's search, curator_run, versioning, subgraph, cross-project federation
  - Change existing 4 MemoryService methods (backward compatible)
  - Put adapter in core/ or flow/ (must be in bridge/)
  - Share ANY context with freeform agent (T8)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Full intake → implementation cycle with TDD, import boundary constraints, cross-workspace dependency
  - **Skills**: []
    - Agent receives ONLY full-cycle + implement-loop skill text as instructions

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 8)
  - **Parallel Group**: Wave 3
  - **Blocks**: T9 (comparison), F1-F4 (final verification)
  - **Blocked By**: T4 (W19 shapes what contract must support)

  **References**:

  **Pattern References**:
  - `.claude/skills/full-cycle/SKILL.md` — Workflow orchestration
  - `.claude/skills/implement-loop/SKILL.md` — Implementation loop specifics
  - `.claude/agents/nowu-implementer.md` — S6-S7 agent spec
  - `src/nowu/core/contracts/memory.py` — CURRENT MemoryService (4 methods) to expand
  - `src/nowu/core/contracts/types.py` — DecisionRecord and other types used by MemoryService

  **API/Type References**:
  - `src/nowu/core/boundaries.py` — Import rules: bridge→{core, flow}, core→nothing
  - `tests/architecture/test_import_boundaries.py` — Boundary enforcement test (must still pass)
  - `tests/architecture/test_adr_fitness.py` — ADR fitness test including no-direct-know-imports check
  - `../know/src/know/schema.py` — KnowledgeAtom dataclass, KnowledgeType enum, EpistemicGrade enum
  - `../know/src/know/api.py` — KnowledgeBase class methods to delegate to

  **Test References**:
  - `tests/core/` — Existing contract importability smoke tests (pattern to follow)
  - `tests/architecture/` — Architecture enforcement tests (must still pass after changes)

  **External References**:
  - `docs/architecture/adr/ADR-0008-knowledge-atom-model.md` — Knowledge model that K3 implements against
  - `docs/architecture/adr/ADR-0011-domain-extension-model.md` — From T4, shapes extension points
  - `state/arch/intake-007-gap-register.md` — GAP-001 (Protocol too narrow) + GAP-002 (no atom CRUD)

  **WHY Each Reference Matters**:
  - memory.py is what we're EXPANDING — must understand current 4 methods
  - boundaries.py + test_import_boundaries.py ENFORCE where adapter can live
  - test_adr_fitness.py checks no direct know imports — must still pass
  - know/schema.py is what the adapter wraps — need to know the types
  - know/api.py is what the adapter delegates to — need to know method signatures
  - GAP-001/002 are the evidence justifying WHY K3 exists

  **Downstream Consumer**: KI-3 (in `../know`) will expand the KnowAdapter to map the full MemoryService v2 Protocol to know's KnowledgeBase API. Design adapter method signatures to be clean and KI-3-extensible (avoid monolithic methods; prefer one-to-one mapping to Protocol methods).

  **Acceptance Criteria**:

  **TDD (tests enabled):**
  - [ ] Test file created: `tests/bridge/test_know_adapter.py` (or equivalent)
  - [ ] `uv run pytest tests/bridge/ -v` → PASS (≥7 tests for 7 new methods + 4 existing)
  - [ ] `uv run pytest tests/architecture/ -v` → PASS (boundary + fitness tests)
  - [ ] `uv run mypy src/ --strict` → 0 errors
  - [ ] `uv run ruff check .` → 0 issues

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: MemoryService Protocol has 11 methods (4 existing + 7 new)
    Tool: Bash
    Preconditions: K3 implementation complete
    Steps:
      1. Count Protocol methods: `grep "def " src/nowu/core/contracts/memory.py | wc -l` — expect 11
      2. Verify no know imports in core: `grep -r "from know\|import know" src/nowu/core/` — expect 0
      3. Verify only generic types: `grep "KnowledgeAtom\|KnowledgeType\|EpistemicGrade" src/nowu/core/` — expect 0
    Expected Result: 11 methods, zero know type imports in core
    Evidence: .sisyphus/evidence/task-7-protocol-expansion.txt

  Scenario: KnowAdapter exists in bridge and passes tests
    Tool: Bash
    Steps:
      1. Check: `ls src/nowu/bridge/know_adapter.py`
      2. Verify it imports from know: `grep "from know" src/nowu/bridge/know_adapter.py` — expect ≥1
      3. Verify it imports MemoryService: `grep "MemoryService" src/nowu/bridge/know_adapter.py` — expect ≥1
      4. Run tests: `uv run pytest tests/bridge/test_know_adapter.py -v` — expect all PASS
    Expected Result: Adapter exists in bridge/, imports know, implements MemoryService, tests pass
    Evidence: .sisyphus/evidence/task-7-adapter-tests.txt

  Scenario: All architecture tests still pass (including updated fitness test)
    Tool: Bash
    Steps:
      1. Run: `uv run pytest tests/architecture/ -v`
      2. Verify import boundary test passes (no bridge→soul, no core→know)
      3. Verify ADR fitness test passes — it must have been updated to exempt bridge/ from the no-direct-know-imports check
      4. Verify exemption: `grep -c "bridge" tests/architecture/test_adr_fitness.py` — expect ≥1 (bridge exemption present)
      5. Verify non-bridge modules still checked: the test must still reject know imports from core/, flow/, soul/
    Expected Result: All architecture tests PASS, bridge/ exempted from know-import check
    Evidence: .sisyphus/evidence/task-7-architecture-tests.txt

  Scenario: Full quality gate passes
    Tool: Bash
    Steps:
      1. `uv run pytest --tb=short -q` — expect all pass
      2. `uv run mypy src/ --strict` — expect 0 errors
      3. `uv run ruff check .` — expect 0 issues
    Expected Result: All three quality gates pass
    Evidence: .sisyphus/evidence/task-7-quality-gates.txt
  ```

  **Commit**: YES
  - Message: `feat(bridge): K3 MemoryService integration — atom CRUD + connections via know adapter`
  - Branch: `feat/K3`
  - Files: `src/nowu/core/contracts/memory.py`, `src/nowu/bridge/know_adapter.py`, `src/nowu/bridge/__init__.py`, `tests/bridge/test_know_adapter.py`
  - Pre-commit: `uv run pytest --tb=short -q && uv run mypy src/ --strict && uv run ruff check .`

- [x] 8. K3-freeform — MemoryService Integration via Freeform Approach

  **What to do**:
  - Achieve the IDENTICAL goal as Task 7 but WITHOUT following S1-S9 workflow
  - Same acceptance criteria: expand MemoryService (7 new methods), implement KnowAdapter in bridge/, TDD, quality gates
  - Work however you see fit — read code, write tests, implement, iterate
  - Track: time spent, approach taken, files read, test strategy
  - Save outputs to `.sisyphus/evidence/k3-freeform/` (NOT to src/ — only workflow version gets committed)
  - Since this produces CODE, run the quality gates on the freeform output too (pytest, mypy, ruff)
  - **CRITICAL**: Must also produce an updated `test_adr_fitness.py` that exempts bridge/ from the no-direct-know-import rule (same requirement as T7 — without this exemption, the adapter cannot pass architecture tests)

  **Must NOT do**:
  - Read ANY .claude/skills/ or .claude/agents/ files
  - Share context with workflow agent (T7)
  - Write to src/ or tests/ (save to .sisyphus/evidence/k3-freeform/ instead)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Same implementation complexity as T7 but without workflow structure
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 7)
  - **Parallel Group**: Wave 3
  - **Blocks**: T9 (comparison)
  - **Blocked By**: T4 (W19 shapes contract)

  **References**:
  - Same API/Type references as T7 (memory.py, boundaries.py, know/schema.py, know/api.py)
  - `state/arch/intake-007-gap-register.md` — GAP-001/002 evidence
  - `docs/architecture/adr/ADR-0008-knowledge-atom-model.md`

  **Acceptance Criteria**:

  ```
  Scenario: Freeform produces equivalent implementation
    Tool: Bash
    Steps:
      1. Check: `ls .sisyphus/evidence/k3-freeform/` — should contain memory.py, know_adapter.py, test_know_adapter.py
      2. Run quality gates on freeform output (copy to temp location, run pytest/mypy/ruff)
    Expected Result: Equivalent implementation that passes quality gates
    Evidence: .sisyphus/evidence/task-8-freeform-quality.txt
  ```

  **Commit**: NO (freeform outputs in .sisyphus/evidence/ only)

- [x] 9. K3-compare — Double-Agent Comparison & Session-Learning

  **What to do**:
  - Compare T7 (workflow) and T8 (freeform) outputs along same 5 dimensions as T3
  - Additional code-specific comparisons:
    - Test coverage: which agent wrote more/better tests?
    - Type safety: which used stricter types?
    - API design: which produced a cleaner MemoryService expansion?
  - If freeform produces BETTER code, consider incorporating improvements into committed version
  - Run session-learning per `.claude/skills/session-learning/SKILL.md`
  - Record models used and agents fired

  **Must NOT do**:
  - Skip code quality comparison
  - Produce subjective assessment without evidence

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Comparative analysis of existing outputs
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (after T7+T8)
  - **Blocks**: None
  - **Blocked By**: T7, T8

  **References**:
  - `.sisyphus/evidence/k3-freeform/` — Freeform outputs
  - `src/nowu/bridge/know_adapter.py` — Workflow outputs
  - `tests/bridge/test_know_adapter.py` — Workflow tests
  - `state/learnings/session-*-w28-dual-agent*.md` — W28 comparison for cross-reference

  **Acceptance Criteria**:

  ```
  Scenario: K3 comparison document complete
    Tool: Bash
    Steps:
      1. Check: `ls state/learnings/session-*-k3-dual-agent.md`
      2. Verify code comparison included (test count, type strictness, API design)
      3. Verify models and agents listed
    Expected Result: Complete comparison with code-specific metrics
    Evidence: .sisyphus/evidence/task-9-comparison.txt

  Scenario: Session-learning for K3 created
    Tool: Bash
    Steps:
      1. Check: `ls state/learnings/session-*-k3*.md`
      2. Check INDEX: `grep -i "k3\|memory" state/learnings/INDEX.md`
    Expected Result: Learning file exists, INDEX updated
    Evidence: .sisyphus/evidence/task-9-session-learning.txt
  ```

  **Commit**: YES (amend onto feat/K3 branch)
  - Message: `docs(learnings): K3 dual-agent comparison + session-learning`
  - Files: `state/learnings/session-*-k3*.md`, `state/learnings/INDEX.md`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
>
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists. For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Run `uv run pytest && uv run mypy src/ --strict && uv run ruff check .`. Review all changed files for: `as any`/`@ts-ignore` equivalents, empty catches, debug prints in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names.
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high`
  Start from clean state. Execute EVERY QA scenario from EVERY task. Test cross-task integration (W19 referenced by K3, W28 evidence feeds W9). Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance. Detect cross-task contamination.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Success Criteria

### Verification Commands
```bash
uv run pytest --tb=short -q         # Expected: all tests pass
uv run mypy src/ --strict            # Expected: 0 errors
uv run ruff check .                  # Expected: 0 issues
ls state/intake/intake-008.md        # Expected: exists (W28)
ls docs/architecture/adr/ADR-0011*   # Expected: exists (W19)
ls docs/architecture/adr/ADR-0012*   # Expected: exists (W20)
ls src/nowu/bridge/know_adapter.py   # Expected: exists (K3)
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All tests pass (including architecture fitness tests)
- [ ] 5 session-learning files created
- [ ] 2 double-agent comparison learnings recorded
- [ ] All feature branches ready for merge review
- [ ] ROADMAP-004 updated with W28/W19/W20/K3/W9 → ✅ DONE
- [ ] Session-log updated with entries for all 5 tasks
