# Proposal: Refactor 5×10 Workflow Model and Agents

```yaml
---
research_artifact:
  version: "1.0"
  date: "2026-05-10"
  topic: "5×10 workflow refactor (PROPOSAL)"
  perplexity_session_id: "nowu-5x10-refactor-workflow-proposal"

problem_statement:
  diagnosis: |
    The current 5×10 workflow model and agent set were designed bottom-up from
    implementation needs. Many agents primarily cover the implementation
    altitude, and the mapping from altitudes/phases to concrete artifacts is
    partially implicit across MODEL-REFERENCE.md, WORKFLOW.md, PRE-WORKFLOW.md,
    and AGENTS.md. This has led to drift between documentation, agent
    behavior, and the newly formalized orchestrator layer.
  context: |
    Recent work introduced an orchestrator layer (roadmap-creator,
    roadmap-updater, work-scheduler) and a ROADMAP-001 implementation plan,
    plus altitude-stratified bootstraps. To evolve nowu into a
    project-agnostic AI creation framework, the 5×10 model needs a cleaner,
    top-down definition that: (1) spans all altitudes (Governance →
    Retrospective), (2) maps clearly to artifact types and agents, and (3)
    coexists with the orchestrator layer without conflating planning and
    execution.
  scope: |
    IN SCOPE: Re-articulation of the 5×10 model in MODEL-REFERENCE.md,
    alignment of WORKFLOW.md / WORKFLOW-DETAILED.md / PRE-WORKFLOW.md with the
    new model, and a pass over AGENTS.md + key agent specs to ensure altitude
    and phase are explicit. OUT OF SCOPE: Implementation of new features in the
    framework itself, deep changes to orchestrator behavior, or hard
    commitments about how external products must adopt 5×10.

evaluation_criteria:
  - criterion: "Conceptual clarity across altitudes"
    weight: "high"
    rationale: "The 5×10 must give a crisp mental model for Governance, Strategic, Tactical, Delivery, and Retrospective work."
  - criterion: "Agent alignment"
    weight: "high"
    rationale: "Agents and skills should declare altitude/phase explicitly and match the model."
  - criterion: "Compatibility with orchestrator layer"
    weight: "high"
    rationale: "Planning and execution responsibilities should be separated but aligned."
  - criterion: "Backward compatibility"
    weight: "medium"
    rationale: "Existing S1–S9 workflows and agents should keep working with minimal changes."
  - criterion: "Implementation cost"
    weight: "medium"
    rationale: "Refactor should be achievable incrementally, not as a big-bang rewrite."

alternatives:
  - id: "A"
    name: "Incremental refactor inside current 5×10"
    summary: |
      Keep the current 5×10 axes and wording, but clean up documentation and
      agent specs incrementally. Clarify altitudes and phases mainly by adding
      examples and tables to MODEL-REFERENCE.md and WORKFLOW-DETAILED.md;
      adjust agents one-by-one as they are touched.
    changes:
      - file: "docs/model/MODEL-REFERENCE.md"
        action: "edit"
        change: "Add explicit altitude definitions and a clearer artifact mapping table."
      - file: "docs/WORKFLOW-DETAILED.md"
        action: "edit"
        change: "Clarify each phase with concrete examples and expected artifacts."
      - file: "docs/AGENTS.md"
        action: "edit"
        change: "Ensure each agent has altitude/phase columns filled and consistent."
    pros:
      - "Low-risk; minimal disruption to existing workflows."
      - "Can be done opportunistically during other work."
    cons:
      - "Does not fully address deeper conceptual debt or gaps across altitudes."
      - "Risk of continued drift if not done comprehensively."
    effort: "low"
    risk: "low"
    evaluation:
      conceptual_clarity_across_altitudes: "acceptable"
      agent_alignment: "acceptable"
      compatibility_with_orchestrator_layer: "acceptable"
      backward_compatibility: "excellent"
      implementation_cost: "excellent"

  - id: "B"
    name: "5×10 v2: top-down re-articulation"
    summary: |
      Define a 5×10 v2 model starting from altitudes and phase-types, then map
      artifacts and agents to it. Document this clearly in MODEL-REFERENCE.md,
      then update WORKFLOW.md / WORKFLOW-DETAILED.md / PRE-WORKFLOW.md and core
      agents so that altitude+phase are explicit and consistent.
    changes:
      - file: "docs/model/MODEL-REFERENCE.md"
        action: "edit"
        change: |
          Introduce a 5×10 v2 section that defines 5 altitudes and 10
          phase-types, with an explicit artifact mapping matrix. Clarify the
          orchestrator layer as "outside-the-field" and show how ROADMAP and
          session-log relate.
      - file: "docs/WORKFLOW.md"
        action: "edit"
        change: "Update overview narrative to describe the v2 model and its relationship to altitudes and orchestrator."
      - file: "docs/WORKFLOW-DETAILED.md"
        action: "edit"
        change: "Align detailed S1–S9 descriptions with v2 phases and altitudes."
      - file: "docs/PRE-WORKFLOW.md"
        action: "edit"
        change: "Ensure P0 phases reference altitudes and the v2 model explicitly."
      - file: "docs/AGENTS.md"
        action: "edit"
        change: |
          Review the table of skills/agents to ensure each has clear
          altitude/phase, and distinguish execution agents from orchestrator
         /meta-agents.
      - file: ".claude/agents/*"
        action: "edit"
        change: "Gradually update frontmatter to make altitude/phase explicit and consistent with v2."
    pros:
      - "Addresses conceptual debt; creates a clear, top-down model for all altitudes."
      - "Aligns documentation, agents, and orchestrator layer."
      - "Sets a solid foundation for project-agnostic framework ambitions."
    cons:
      - "Higher upfront effort; touches many core docs."
      - "Requires careful rollout to avoid confusing existing users."
    effort: "medium"
    risk: "medium"
    evaluation:
      conceptual_clarity_across_altitudes: "excellent"
      agent_alignment: "good"
      compatibility_with_orchestrator_layer: "excellent"
      backward_compatibility: "good"
      implementation_cost: "good"

  - id: "C"
    name: "Minimal "docs only" refresh"
    summary: |
      Restrict changes to prose in WORKFLOW.md and MODEL-REFERENCE.md without
      updating agents or PRE-WORKFLOW. Treat this as a documentation polish
      only.
    changes:
      - file: "docs/WORKFLOW.md"
        action: "edit"
        change: "Clarify existing wording and examples."
      - file: "docs/model/MODEL-REFERENCE.md"
        action: "edit"
        change: "Tighten up descriptions of existing phases and altitudes."
    pros:
      - "Very low effort and risk."
      - "Can be done quickly to improve readability."
    cons:
      - "Leaves structural issues unresolved."
      - "Widening gap between docs and actual agent/altitude behavior."
    effort: "low"
    risk: "low"
    evaluation:
      conceptual_clarity_across_altitudes: "acceptable"
      agent_alignment: "poor"
      compatibility_with_orchestrator_layer: "poor"
      backward_compatibility: "excellent"
      implementation_cost: "excellent"

recommendation:
  chosen: "B (PROPOSAL ONLY)"
  rationale: |
    A 5×10 v2 defined top-down provides the strongest foundation for aligning
    altitudes, phases, artifacts, agents, and the orchestrator layer. However,
    this artifact is explicitly a PROPOSAL for OmO to evaluate, not a
    step-by-step plan to follow blindly. OmO should:
    - Confirm the current 5×10 usage and pain points by reviewing MODEL-REFERENCE,
      WORKFLOW docs, PRE-WORKFLOW, AGENTS, and key agent specs.
    - Potentially adjust the set of altitudes or phase labels based on real
      usage.
    - Decide whether to commit to a v2 now or to start with a scoped pilot
      (e.g., refactor PRE-WORKFLOW and one or two key execution skills first).
  runner_up: |
    If the full v2 feels too heavy, consider a staged approach: begin with a
    more constrained refactor (hybrid of A and B) focusing on PRE-WORKFLOW and
    MODEL-REFERENCE, then expand to AGENTS and WORKFLOW-DETAILED once patterns
    stabilize.

implementation:
  prerequisites:
    - "Updated ROADMAP-001.md and session-log exist (or are in progress), so current work is visible."
    - "MODEL-REFERENCE.md, WORKFLOW.md, WORKFLOW-DETAILED.md, PRE-WORKFLOW.md, and AGENTS.md are available and reasonably up-to-date."
  steps:
    - step: "Synthesize current 5×10 usage across MODEL-REFERENCE, WORKFLOW docs, PRE-WORKFLOW, and AGENTS."
      verify: "OmO produces a short internal note capturing how 5×10 is actually used today."
    - step: "Draft 5×10 v2 section in MODEL-REFERENCE.md defining altitudes, phase-types, and artifact mapping."
      verify: "v2 section exists behind a clear heading and does not break existing references."
    - step: "Update WORKFLOW.md and WORKFLOW-DETAILED.md to reference v2 concepts while preserving current S1–S9 behavior."
      verify: "Docs for S1–S9 still describe the same steps but now link them to v2 altitudes/phases."
    - step: "Adjust PRE-WORKFLOW.md to align P0 phases with v2 altitudes (e.g., clearly STRATEGIC/PRODUCT)."
      verify: "P0 descriptions reference altitudes consistently."
    - step: "Review AGENTS.md and at least a small set of key agents to ensure their altitude/phase is explicit and matches v2."
      verify: "For reviewed agents, frontmatter and AGENTS.md table are consistent."
  validation:
    - test: "A new contributor reads MODEL-REFERENCE v2 section and can correctly map a given artifact (e.g., SYNTHESIS-001, intake-NNN, ADR-0008) into an altitude/phase cell."
      expected: "They choose the same cell OmO would, without reading agent prompts."
    - test: "An execution session (full S1–S9) can be run without changes to code, but with clearer altitude/phase framing in the docs."
      expected: "No regressions in behavior; improved orientation only."

context_for_omo:
  files_to_review:
    - "docs/model/MODEL-REFERENCE.md"
    - "docs/WORKFLOW.md"
    - "docs/WORKFLOW-DETAILED.md"
    - "docs/PRE-WORKFLOW.md"
    - "docs/AGENTS.md"
    - "orchestrator-layer-design.md (if present)"
  decisions_informed:
    - "D-019 — Router-based agent architecture"
    - "D-020 — Areas × Stages plan"
    - "D-022 — Orchestrator layer external to 5×10"
  related_artifacts:
    - "docs/research/* (workflow & orchestrator research sessions)"
  constraints:
    - "This artifact is a PROPOSAL for OmO to evaluate and adapt, not a fixed plan."
    - "Avoid breaking existing S1–S9 behavior; changes should be documentation-first and incremental."
    - "Do not rename or remove core artifacts (e.g., SYNTHESIS-001, ARCHITECTURE-VISION, ADRs) without explicit new decisions."
---
```
