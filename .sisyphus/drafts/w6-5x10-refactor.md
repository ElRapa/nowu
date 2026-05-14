# Draft: W6 — 5×10 Model Refactor + Agent-Grid Mapping

## Requirements (confirmed from roadmap)
- W6: "5×10 model refactor with full agent-grid mapping"
- Stage: v1-core
- Depends on: W4 (complete)
- UC links: NF-02 (Track and Enforce Architectural Decisions), NF-03 (Scope a Piece of Work)
- Status in roadmap: READY

## Perplexity Proposal Evaluation

### What Perplexity Got RIGHT:
1. S7/S8 fix — confirmed by W5 §5.2
2. Section 13 coverage gaps — confirmed by W5 §5.5, §5.6
3. Consumption-position convention — confirmed by W5 D-SESS-01
4. artifact_type vocabulary formalization at model level (not artifact level)
5. Agent grid creation in docs
6. Agent frontmatter altitude/phase additions
7. S9 checklist update for metadata verification
8. S4 decision file enforcement
9. Summary artifact (state/arch/w6-5x10-refactor-summary.md)
10. Non-goals: no new altitudes/phases, no artifact renames, no retroactive S4 backfill

### Concerns / Issues with Perplexity's proposal:
1. **SCOPE SIZE** — Touches 6+ docs + potentially 35+ agent files. Risk of token exhaustion for any single agent.
2. **WORKFLOW-DETAILED.md update** — Need to verify what this file contains for S7/S8 before committing to "align"
3. **PRE-WORKFLOW.md altitude mapping** — Need to check if P0-P4 already have explicit altitudes or not
4. **Agent frontmatter** — Need to check if agents have YAML frontmatter at all (they might be pure markdown)
5. **"Formalize artifact_type in MODEL-REFERENCE"** — W5 explicitly said "deferred to K1/W20". Is model-level formalization different from enforcement? Possibly YES — define vocab in model, enforce in K1/W20.
6. **Perplexity references "5×10 v2" from the research proposal** — but W6 should be corrections/alignment, NOT a version bump of the model. The model is correct; the docs are inconsistent.

### My assessment: Perplexity's scope is ~80% correct but slightly over-scoped
- The agent frontmatter updates (35 files) could be a mechanical edit wave
- The core model corrections (MODEL-REFERENCE, WORKFLOW, WORKFLOW-DETAILED) are the real intellectual work
- PRE-WORKFLOW alignment is small (P0-P4 altitude labels)
- The "5×10 v2" framing from the research proposal is WRONG for W6 — W6 is corrections+alignment, not a model version bump

## W5 Recommendations for W6 (binding input)
1. Fix S7/S8 agent mapping in MODEL-REFERENCE §7
2. Add missing artifact types to Section 13: state/changes/, state/analysis/
3. Document Section 13 convention: consumption position, not creation
4. Add S4 decision file check to S5 pre-shaping checklist
5. Standardize artifact_type vocabulary (at model level; enforcement deferred to K1/W20)
6. Resolve state/sessions/ references in bootstrap files

## Open Questions (RESOLVED by exploration)
- ✅ 35 agent files; only 4/35 have altitude/phase (roadmap-creator, roadmap-updater, synthesis-agent, architecture-vision-agent)
- ✅ Agent frontmatter schema: name, description, tools, model, memory (simple, consistent)
- ✅ WORKFLOW-DETAILED.md correctly maps S7=VBR, S8=Review (no conflict with WORKFLOW.md)
- ✅ PRE-WORKFLOW.md uses procedural language, NOT explicit altitude labels. MODEL-REFERENCE has a P0-P4 mapping table.
- ✅ AGENTS.md is at REPO ROOT (not docs/). It's a project overview, NOT an agent grid.

## CRITICAL DISCOVERY: Bug is in TWO places, not one
W5 identified the S7/S8 bug in MODEL-REFERENCE.md Section 7. But it ALSO exists in:
- **WORKFLOW-STANDARDS.md Rule 1.1** — maps S8 to VERIFICATION (should be EVALUATION)
- Perplexity's proposal MISSED this second location.

## Current S7/S8 state across docs:
| Source | S7 | S8 |
|--------|----|----|
| MODEL-REFERENCE §7 | nowu-reviewer / VERIFICATION (WRONG) | VBR / VERIFICATION (WRONG) |
| WORKFLOW-STANDARDS §1.1 | EXECUTION / VERIFICATION (correct) | EXECUTION / VERIFICATION (WRONG - should be EVALUATION) |
| WORKFLOW.md | nowu-implementer(VBR) / L4 (correct) | nowu-reviewer / L3-L4 (correct) |
| WORKFLOW-DETAILED.md | VBR gate (correct) | nowu-reviewer Review (correct) |
| Actual W4 practice | VBR / VERIFICATION (correct) | nowu-reviewer / EVALUATION (correct) |

## Section 13 current entries (verbatim from MODEL-REFERENCE):
- docs/vision.md → STRATEGIC / PROBLEM/DECISION
- docs/goals/goal-NNN.md → STRATEGIC / DECISION
- docs/USE_CASES.md → PRODUCT / PROBLEM
- state/ideas/idea-NNN.md → STRATEGIC or PRODUCT / IDEA
- state/discovery/disc-NNN.md → PRODUCT / ANALYSIS
- state/problems/problem-NNN.md → PRODUCT / PROBLEM
- state/epics/epic-NNN.md → DELIVERY / OPTIONS
- state/stories/story-NNN-*.md → DELIVERY / DECISION
- state/intake/intake-NNN.md → DELIVERY / DECISION→IMPLEMENTATION
- state/arch/arch-pass-NNN.md → ARCHITECTURE / OPTIONS
- state/arch/NNN-constraint-check.md → ARCHITECTURE / ANALYSIS
- state/arch/NNN-atam-lite.md → ARCHITECTURE / EVALUATION
- docs/architecture/adr/*.md → ARCHITECTURE / DECISION
- docs/DECISIONS.md → ARCHITECTURE / DECISION
- state/tasks/task-NNN.md → EXECUTION / IMPLEMENTATION
- state/vbr/vbr-task-NNN.md → EXECUTION / VERIFICATION
- state/capture/capture-task-NNN.md → EXECUTION→DELIVERY / LEARN
- state/health/arch-*.md → ARCHITECTURE / VERIFICATION
- state/analysis/session-review-*.md → DELIVERY / LEARN
- docs/ROADMAP-001.md → STRATEGIC / IMPLEMENTATION

MISSING from Section 13:
- state/changes/task-NNN.md → EXECUTION / IMPLEMENTATION (5 files produced in W4)
- state/analysis/S*-*.md (step analyses) — exists as "session-review" but pattern doesn't match
- state/learnings/*.md → (altitude varies) / LEARN
- state/reviews/review-*.md → EXECUTION / EVALUATION (currently NOT in the table!)
- state/arch/*-options.md → ARCHITECTURE / OPTIONS (not explicitly listed)
- state/arch/*-constraints.md → ARCHITECTURE / ANALYSIS (exists as "NNN-constraint-check" but naming differs)

## Decisions still needed from user
ALL RESOLVED:
1. artifact_type vocabulary → **Formalize in MODEL-REFERENCE** (define canonical 15-term vocabulary; K1/W20 handles enforcement)
2. Agent grid location → **Add section to root AGENTS.md** (all agents already load it)
3. Agent frontmatter scope → **All 31 agents in W6** (complete the grid in one pass)
4. Verification approach → **Both grep checks + Oracle review** (belt and suspenders)

## Scope Boundaries (preliminary)
- INCLUDE: MODEL-REFERENCE corrections (§7 S7/S8, §13 expansion, consumption convention), WORKFLOW-STANDARDS §1.1 fix, agent grid creation, agent frontmatter additions, process wiring (S9 checklist, S4 file check), summary artifact
- EXCLUDE: artifact_type enforcement on existing state/ files (K1/W20), new 5×10 model version, code changes, template updates (minor, can ride along or defer)
- UNCERTAIN: PRE-WORKFLOW.md altitude labels (MODEL-REFERENCE already has the table — adding to PRE-WORKFLOW may be redundant)
