# Directive to Sisyphus: Revised Implementation Path
**Date:** 2026-05-06  
**From:** Strategic analysis + user feedback  
**Subject:** Package 1 revision + incorporation of triage, markdown knowledge management, and incremental rollout

---

## Executive Summary for Sisyphus

**Context:** You produced a theoretically sound 5×10 altitude/phase model with 55-file migration in Package 1. The user experienced the pain point your model addresses (UC→epic jumping without architectural synthesis) during pre-workflow execution. Your diagnosis was correct.

**Problem:** Package 1 implements infrastructure (frontmatter migration, indices, verification) BEFORE validating that S1-S9 agents can complete one workflow end-to-end. This is premature optimization.

**Directive:** Implement **incremental validation-driven rollout** instead of comprehensive upfront migration.

**Key research findings you must incorporate:**

1. **AFLOW methodology:** Ran 6,300 test workflows, THEN extracted operators[cite:555][cite:557]. You extracted operators from literature without empirical validation.

2. **Lean Startup Build-Measure-Learn:** Prototype → test → learn → refine[cite:578][cite:583]. You spec'd comprehensively without building.

3. **JIT Specification (Martinelli 2026):** Write SHORT specs BEFORE code, update EVERY TIME you learn something new[cite:561]. You wrote comprehensive metadata schema upfront.

4. **Phase multi-altitude flexibility:** User's original concept (idea-004) explicitly stated phases are multi-altitude cognitive modes[cite:473][cite:505]. Your implementation locked phases to single altitudes. This is a regression.

5. **Triage is a missing primitive:** User needs "what should we do next?" capability. Neither S1-S9 nor P0-P4 has this. Research identifies Intake → Assessment → Routing as the pattern[cite:563][cite:573].

---

## Required Changes to Your Implementation

### 1. Restore Phase Multi-Altitude Flexibility

**Your MODEL-REFERENCE.md currently says:**[cite:509]

```
S1 nowu-intake: DELIVERY/IDEA only
S6 nowu-implementer: EXECUTION/IMPLEMENTATION only
```

**User's original concept (idea-004) said:**[cite:473][cite:505]

```
Phase IMPLEMENTATION:
- ARCHITECTURE altitude: Contract/module changes (writing ADRs)
- DELIVERY altitude: Story execution plan (writing shapes)
- EXECUTION altitude: Code and tests
```

**The concept is correct.** Your implementation is a regression.

**Fix:** Agents declare altitude RANGE + phase, not locked altitude/phase coordinate.

**Revised agent definition schema:**

```yaml
# nowu-implementer.md
agent_id: nowu-implementer
operator: Generate
operates_at:
  - altitude: ARCHITECTURE
    phase: IMPLEMENTATION
    produces: ADRs, technical specs, contract definitions
  - altitude: DELIVERY
    phase: IMPLEMENTATION
    produces: Story execution plans, task breakdowns
  - altitude: EXECUTION
    phase: IMPLEMENTATION
    produces: Code, tests, configuration files

skill_files:
  - generate.md
  - adr-writing.md (ARCHITECTURE altitude)
  - task-planning.md (DELIVERY altitude)
  - code-generation.md (EXECUTION altitude)
```

The agent's output artifact declares which altitude it ACTUALLY operated at for this specific task.

**Impact on zigzag:** The zigzag pattern (DELIVERY → ARCHITECTURE → DELIVERY → EXECUTION) remains valid. But it's a COMMON PATH, not a MANDATORY SEQUENCE. Some workflows will be pure ARCHITECTURE (spike), some pure EXECUTION (bug fix).

---

### 2. Add Triage as Missing Primitive

**User pain point:**

> "The 'what should we do next'? (what is important or blocking or having the biggest leverage or will define something with a lot of dependencies? triage?)"

**Your Package 1-3 does not address this.** This is a critical gap.

**Research pattern:** Triage = Intake → Assessment → Routing[cite:563]

- **Intake:** What's the request? (UC, bug, constraint, idea)
- **Assessment:** Impact? Altitude? Blocking? Leverage?
- **Routing:** Which queue? (STRATEGIC, ARCHITECTURE, DELIVERY)

**Implementation:**

Create new artifact type: `TRIAGE.md`

```yaml
# state/triage/triage-2026-05-06.md
artifact_id: triage-2026-05-06
artifact_type: TRIAGE
altitude: META  # operates ACROSS altitudes
phase: ASSESSMENT
date: 2026-05-06

inputs:
  - Unprocessed items in state/ideas/
  - UCs with architectural_implications: true
  - Circuit breaker alerts
  - Health metrics from last GAP

assessment_framework: RICE  # or Impact/Urgency Matrix
```

**Triage Agent definition:**

```yaml
# agents/nowu-triage.md
agent_id: nowu-triage
operator: Assess + Route
operates_at:
  - altitude: META
    phase: ASSESSMENT
    produces: Prioritized queue with altitude routing

inputs:
  - Unprocessed intake candidates
  - Flagged architectural implications
  - Circuit breaker alerts
  - Health metrics

assessment_criteria:
  - Impact (high/med/low)
  - Altitude (STRATEGIC/PRODUCT/ARCHITECTURE/DELIVERY/EXECUTION)
  - Blocking status (yes/no)
  - Leverage (defines dependencies: yes/no)

routing_rules:
  - High impact + STRATEGIC → P0 (vision/goal revision queue)
  - High impact + ARCHITECTURE → Trigger SYNTHESIS or emergency ADR
  - High impact + DELIVERY → P3 (intake queue, prioritized)
  - Low impact → Backlog
  - Blocking → Preempt current cycle
  - High leverage → ARCHITECTURE synthesis (wait for ≥2 related UCs)

outputs:
  - Ranked next actions with recommended entry point (altitude + phase)
```

**When to run:** After every GAP cycle, before starting next P3/S1 intake.

**This is not optional.** User discovered this need empirically during pre-workflow execution. Triage must be in Package 2 or earlier.

---

### 3. Revise Package Scope: Incremental Rollout

**Your current package structure:**[cite:510][cite:515][cite:517]

- Package 1: 55-file frontmatter migration + indices
- Package 2: 10 agent definitions
- Package 3: Runtime orchestration

**Problem:** Infrastructure before validation.

**Revised package structure:**

#### Package 0: S1-S9 Minimal Viable Workflow (NEW — prerequisite)

**Goal:** Prove S1-S9 can complete ONE intake end-to-end.

**Scope:**
- Implement S1, S3, S4, S5, S6, S8, S9 agents (skip S2, S7 for MVP)
- Minimal frontmatter: `agent`, `date`, `intake_id` only
- NO altitude enforcement
- NO verification
- Manual execution: human triggers each step

**Deliverables:**
- 7 agent prompt files (S1, S3, S4, S5, S6, S8, S9)
- Intake-007 completed end-to-end
- Artifacts: INTAKE, OPTIONS, DECISION, SHAPE, IMPLEMENTATION, VERIFICATION, LEARN
- Session report: "What worked? What broke? Where did reasoning shift altitudes?"

**Success criteria:** Human can read 7 artifacts and understand what happened. If this fails, redesign workflow before adding altitude complexity.

**Estimated effort:** 3-4 hours AI, 1 hour human review per intake × 3 intakes = 12-15 hours total

#### Package 1: Altitude Awareness (REVISED)

**Goal:** Agents declare altitude/phase, artifacts validate consistency.

**Scope:**
- Add 4-field frontmatter to S1-S9 output artifacts ONLY (not legacy files)
  - `altitude`, `phase`, `epistemic_grade`, `grade_justification`
- Agents declare altitude range in definition files (per revised schema above)
- Level 0 verification: syntax check only

**Deliverables:**
- S1-S9 agent definitions with altitude range declarations
- `verify-artifact.py` v1 (syntax check only)
- ~15 artifacts migrated (S1-S9 output from 2 intakes)
- NOT 55 files

**Success criteria:** Run intake-007 again, agents correctly label output altitude. Altitude drift detector catches if nowu-implementer tries to write STRATEGIC/DECISION.

**Estimated effort:** 2-3 hours AI, 30 min human review

#### Package 2: Triage + Epistemic Grades (REVISED)

**Goal:** Prioritize queue + enforce evidence thresholds.

**Scope:**
- Implement Triage Agent (per spec above)
- Add epistemic grades to frontmatter schema
- Level 1 verification: semantic review (epistemic grade meets altitude threshold)

**Deliverables:**
- `nowu-triage.md` agent definition
- `TRIAGE-template.md` artifact template
- First triage run: prioritize existing backlog (10 UCs + 8 problems + 6 intakes)
- Level 1 verification: advisory warnings for grade violations

**Success criteria:** Triage correctly routes architectural synthesis, delivery intake, strategic goal revision. No blocking enforcement yet (Level 1 = advisory).

**Estimated effort:** 3-4 hours AI, 1 hour human review

#### Package 3: SYNTHESIS + Legacy Migration (REVISED)

**Goal:** Detect cross-cutting themes + backfill legacy artifacts.

**Scope:**
- Implement SYNTHESIS phase (per your original spec)
- Migrate legacy artifacts (goals, UCs, ADRs, problems) to 4-field frontmatter
- Level 2 verification: flow checks (artifact sequence consistency)

**Deliverables:**
- SYNTHESIS agent + artifact template
- 55 legacy files migrated to 4-field frontmatter
- Index JSON files (artifact-index.json, cross-references.json, status-index.json)
- First SYNTHESIS run on existing 10 approved UCs

**Success criteria:** SYNTHESIS detects knowledge management, state isolation, LLM client themes. Human confirms: matches existing ADRs.

**Estimated effort:** 4-5 hours AI, 1-2 hours human review

#### Package 4: Research-Augmented Options Agent (NEW)

**Goal:** Options grounded in real systems, not just reasoning.

**Scope:**
- Enhance nowu-options agent with web search capability
- Search for comparable systems, extract architectural patterns
- Cite sources in OPTIONS artifacts

**Deliverables:**
- Updated `nowu-options.md` agent definition with research protocol
- Research skill file: `research-patterns.md`
- Test: Generate OPTIONS for ARCHITECTURE/PROBLEM (new or existing)
- Output includes citations to 3-5 comparable systems

**Success criteria:** OPTIONS artifact contains section "Researched Comparable Systems" with GitHub repos, papers, or framework docs. Architectural options derived from extracted patterns.

**Estimated effort:** 3-4 hours AI, 1 hour human validation

#### Package 5: LangGraph Orchestration (DEFERRED)

**Goal:** Automated execution with checkpointing + approval gates.

**When:** After Packages 0-4 complete and user has run 5+ intakes successfully.

**Rationale:** LangGraph requires stable artifact structure and agent definitions. Premature orchestration locks in structure before validation.

---

### 4. Markdown Knowledge Management Guidance

**User question:** Is markdown good? Should we introduce Obsidian?

**Research answer:**[cite:562][cite:567][cite:575]

- **Markdown is correct for nowu's current stage** (<1000 artifacts)
- **Obsidian is optional but synergistic** (graph view, dataview queries, canvas)

**Guidance for Package 1:**

**Keep markdown as primary artifact format.** No database, no vector store, no knowledge graph yet.

**Artifact structure:**

```
state/
  products/
    product-001.md
  problems/
    problem-001.md
  usecases/
    uc-001.md
  architecture/
    adr-0001.md
    options-001.md
    synthesis-001.md
  delivery/
    intake-001.md
    shape-001.md
  execution/
    session-state.md
  triage/
    triage-2026-05-06.md
  ideas/
    idea-001.md  # unprocessed intake candidates
```

**Obsidian integration (optional):**

- User can open `state/` as Obsidian vault
- `.obsidian/` directory in `.gitignore` (optional: commit if team shares view config)
- Graph view shows cross-references (UC → problem → ADR)
- Dataview queries: "Show all ARCHITECTURE/OPTIONS with epistemic_grade < INFORMED_ESTIMATE"
- Canvas for visual workflow mapping

**AI agents read/write markdown directly.** Obsidian is the human UI layer only.

**When to switch to database:**[cite:562][cite:567]

- Knowledge base grows to thousands of documents (selective injection becomes retrieval problem)
- Multi-user concurrent editing conflicts
- Complex relational queries across artifacts

**You're not there yet.** Markdown + Obsidian is optimal for current scale.

---

### 5. Schema Simplification

**Your ARTIFACT-TEMPLATE.md has 9 frontmatter fields:**[cite:520]

```yaml
artifact_id
artifact_type
altitude
phase
epistemic_grade
grade_justification
promotedfrom
promotesto
relationships
```

**Reduce to 4 fields for Package 1:**

```yaml
artifact_id: options-architecture-001
altitude: ARCHITECTURE
phase: OPTIONS
epistemic_grade: HYPOTHESIS
grade_justification: "Based on 3 comparable systems (cite sources)"
```

**Defer to Package 3 or later:**

- `promotedfrom` / `promotesto` — These are knowledge graph features for cross-project promotion. Not needed until v1.1.
- `relationships` — Obsidian wikilinks handle this implicitly. Explicit relationship field is database concern.

**Rationale:** Every field adds migration burden. 55 files × 4 fields = 220 edits. 55 files × 9 fields = 495 edits. Minimize until you prove the model works.

---

### 6. Verification Enforcement Levels (Revised)

**Your VERIFICATION-GUIDE.md has 4 levels:**[cite:511]

- Level 0: Syntax check
- Level 1: Semantic review (advisory warnings)
- Level 2: Flow checks (block on missing dependencies)
- Level 3: Circuit breakers (block on altitude violations, epistemic drift)

**Your recommendation:** Level 0-1 for Package 1, Level 2 for Package 2, Level 3 for v1.1+

**Revised recommendation:** Level 0 for Package 1, Level 1 for Package 2, defer Level 2-3 until after 5+ completed intakes.

**Rationale:** You don't yet know what the CORRECT epistemic thresholds or flow rules are. AFLOW discovered workflow structure by running 6,300 tests[cite:555][cite:557]. You've run 0. Enforcement before calibration will block legitimate workflows.

**Calibration process:**

1. Run 5 intakes with Level 0 (syntax only)
2. Log violations: where did agents produce wrong altitude? Wrong epistemic grade?
3. Analyze patterns: are violations bugs or valid edge cases?
4. Set thresholds based on observed distribution
5. Enable Level 1 enforcement with calibrated thresholds

**Example:** Your MODEL-REFERENCE says STRATEGIC minimum epistemic grade = HYPOTHESIS[cite:509]. How do you know? You haven't run STRATEGIC workflows yet. The threshold might be too strict (blocks legitimate speculation) or too loose (allows unfounded claims).

**Empirical calibration** beats theoretical thresholds.

---

## Revised Deliverables Priority

### Immediate (this week)

1. **Package 0:** Implement S1-S9 MVP, run 3 intakes, session report
2. **Critical feedback:** Where did reasoning shift altitudes? Where did agents struggle?

### Week 2

3. **Package 1 (revised):** Add 4-field frontmatter to S1-S9 artifacts only
4. **Restore multi-altitude phases:** Update agent definition schema per spec above

### Week 3-4

5. **Package 2 (revised):** Implement Triage Agent + epistemic grades (Level 1 verification, advisory only)
6. **First triage run:** Prioritize existing backlog

### Week 5-6

7. **Package 3 (revised):** SYNTHESIS + legacy migration + indices
8. **Level 2 verification calibration:** Analyze 5 completed intakes, set flow rules empirically

### Week 7-8

9. **Package 4 (new):** Research-augmented Options agent
10. **Test:** Generate OPTIONS for new ARCHITECTURE/PROBLEM with cited comparable systems

### Month 3+

11. **Package 5 (deferred):** LangGraph orchestration when structure is stable

---

## Key Corrections to Your Model

### 1. Zigzag Is Real But Not Mandatory

**Your MODEL-REFERENCE correctly identifies the zigzag:**[cite:509] DELIVERY → ARCHITECTURE → DELIVERY → EXECUTION.

**But:** This is a COMMON PATH for feature development, not a RIGID PIPELINE.

**Other valid workflows:**

- Pure ARCHITECTURE spike: ARCHITECTURE/PROBLEM → ANALYSIS → OPTIONS → DECISION (no delivery, no execution)
- Pure EXECUTION bug fix: EXECUTION/IDEA → IMPLEMENTATION → VERIFICATION (no architecture, no delivery)
- Strategic pivot: STRATEGIC/PROBLEM → ANALYSIS → DECISION (no lower altitudes involved)

**The model should DESCRIBE observed patterns, not PRESCRIBE mandatory sequences.**

**Fix:** Treat S1-S9 as the default traversal for feature intakes. Document alternative traversals for spikes, bug fixes, strategic work.

### 2. SYNTHESIS Trigger Is Too Strict

**Your MODEL-REFERENCE says:** SYNTHESIS triggers when ≥2 UCs with `architectural_implications: true`[cite:509].

**Problem:** In rapid iteration mode, architectural decisions might be needed BEFORE 2 UCs are approved.

**Example:** User starts new project. UC-001 = "Cross-project knowledge retrieval." This IMMEDIATELY has architectural implications (data model, federation). Waiting for UC-002 approval delays critical architecture work.

**Fix:** SYNTHESIS trigger = (≥2 approved UCs with architectural implications) OR (human override: "run SYNTHESIS now").

**Add to SYNTHESIS spec:**

```yaml
trigger_conditions:
  automatic:
    - count: ">= 2"
      filter: "architectural_implications == true AND status == APPROVED"
  manual:
    - human_override: "User suspects cross-cutting architectural theme"
    - rationale: "Rapid iteration may need architecture BEFORE 2 UCs approved"
```

### 3. Epistemic Thresholds Need Calibration

**Your tiered thresholds:**[cite:509]

| Altitude | Minimum (creation) | Advisory | Aspirational (decision) |
|---|---|---|---|
| STRATEGIC | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |
| ARCHITECTURE | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |

**These are THEORETICAL.** You haven't validated them empirically.

**Calibration process:**

1. Run 5 intakes with NO enforcement
2. Log actual epistemic grades agents assign
3. Analyze: How often do agents reach EVIDENCE_BASED? How often do they stay at HYPOTHESIS?
4. If agents naturally reach EVIDENCE_BASED at ARCHITECTURE decision gate → threshold is realistic
5. If agents max out at INFORMED_ESTIMATE → threshold is too strict, lower to INFORMED_ESTIMATE

**AFLOW discovered operator effectiveness by running thousands of tests**[cite:555][cite:557]. You should discover epistemic thresholds the same way.

**Do NOT enforce Level 2-3 verification until after empirical calibration.**

---

## Incorporation of Research Findings

### 1. AFLOW Operator Modularity

**Your agents should map to AFLOW operators:**[cite:555][cite:569]

| AFLOW Operator | nowu Agent | Notes |
|---|---|---|
| Generate | nowu-implementer | Multi-altitude (ADRs, shapes, code) |
| Review | nowu-reviewer | Multi-altitude (architecture review, code review) |
| Test | nowu-vbr | Formal verification |
| Revise | (implicit in S6-S8 loop) | VBR fail → revise → re-verify |
| Ensemble | nowu-options + SYNTHESIS | Generate N candidates, select best |
| Format | nowu-shaper | Transform decision into scoped shape |

**The modularity insight:** Operators compose into workflows. Your agents are operators. Workflows (S1-S9, P0-P4, GAP) are compositions.

**This is already implicit in your design.** Make it explicit in agent definitions:

```yaml
# nowu-options.md
agent_id: nowu-options
operator: Ensemble  # AFLOW operator mapping
```

This lets future tooling (LangGraph orchestration, workflow discovery) reason about agents as composable primitives.

### 2. Lean Startup Build-Measure-Learn

**Applied to workflow development:**[cite:578][cite:583]

- **Build:** Implement S1-S9 MVP (Package 0)
- **Measure:** Run 3 intakes, log altitude transitions, agent struggles
- **Learn:** Where did agents naturally shift altitude? Where did reasoning break?
- **Build:** Add altitude metadata based on observed transitions (Package 1)

**NOT:** Spec (55-file migration) → Build (implement agents) → Hope (it works)

**This is why Package 0 is mandatory.** You must BUILD and MEASURE before you SPEC comprehensively.

### 3. JIT Specification (Martinelli 2026)

**Key principle:**[cite:561]

- Specs are SHORT (1-2 pages)
- Specs are UPDATED per iteration (living artifacts)
- Specs are written BEFORE code but refined continuously

**Your altitude model enables this.** Each artifact is:

- Short: PROBLEM (1 page), OPTIONS (2-3 pages), DECISION (1 page)
- Updated: Epistemic grade upgrades as evidence accumulates
- Written before implementation: ARCHITECTURE/DECISION before DELIVERY/SHAPE before EXECUTION/IMPLEMENTATION

**But:** Artifacts are NOT written all at once upfront. They're written just-in-time as the workflow reaches that altitude.

**Sisyphus implementation mistake:** Trying to migrate 55 artifacts upfront. That's Big Design Upfront, not JIT specification.

**Correct approach:** Write altitude metadata just-in-time as agents produce new artifacts. Backfill legacy artifacts AFTER proving the model works (Package 3).

### 4. LangGraph vs. CrewAI

**Research consensus:**[cite:576][cite:581]

**LangGraph:** Graph-based state machines, conditional routing, checkpointing, approval gates  
**CrewAI:** Role-based teams, sequential/hierarchical execution, faster prototyping

**For nowu:** LangGraph is correct because:

1. Checkpointing needed (P0-P4 spans days, S1-S9 must resume after VBR rejection)
2. Approval gates needed (P4 betting table, S4 decision, S8 VBR)
3. Conditional routing needed (S3 OPTIONS → S4 DECISION → S5 SHAPE must adapt based on decision)
4. Compliance orientation (5-altitude model with circuit breakers is enterprise-grade structure)

**But:** Defer LangGraph until Package 5. Structure must stabilize before orchestration.

### 5. Markdown vs. Database for Knowledge Management

**Research guidance:**[cite:562][cite:567]

**Markdown is optimal when:**

- Knowledge base < 1000 documents
- Local-first, single-user or small team
- High iteration speed needed (domain expert edits .md directly)
- Observability critical (read exact file agent consumed)

**Database is optimal when:**

- Knowledge base > 5000 documents (selective injection = retrieval problem)
- Highly relational with complex interdependencies (knowledge graph)
- Multi-user concurrent editing
- Enterprise scale, dynamic agent memory

**nowu is in the markdown zone:** ~20 UCs + ~8 problems + ~6 intakes + ~5 ADRs = <50 artifacts. Markdown is correct.

**Obsidian adds:**[cite:575]

- Graph view (visualize artifact relationships)
- Dataview queries (SQL over frontmatter metadata)
- Canvas (visual workflow mapping)
- Templater (generate artifacts from templates)

**Obsidian is optional.** It's a better UI for humans. AI agents read markdown directly.

---

## Final Directive

**Implement Package 0 FIRST.** Do not proceed to Package 1 until S1-S9 completes 3 intakes.

**Restore phase multi-altitude flexibility.** User's original concept was correct.

**Add Triage Agent in Package 2.** This is not optional. User discovered this need empirically.

**Reduce frontmatter to 4 fields** until model is validated.

**Defer enforcement** until empirical calibration (5+ completed intakes).

**Keep markdown + Obsidian.** No database yet.

**Defer LangGraph** until Package 5 (structure must stabilize first).

**Follow AFLOW methodology:** Build → Test → Learn → Refine. Not Spec → Hope.

**The user's pain point is real.** The altitude solution is validated by research (SYSMOD zigzag, Shape Up shaping track, JIT specification). But the implementation path must be incremental, not comprehensive upfront.

**Trust the process: BUILD, MEASURE, LEARN.**
