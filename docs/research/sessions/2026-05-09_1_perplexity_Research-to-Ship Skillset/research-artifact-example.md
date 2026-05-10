# Example: Structured Research Artifact

```yaml
---
research_artifact:
  version: "1.0"
  date: "2026-05-09"
  topic: "Bootstrap context loading optimization"
  perplexity_session_id: "conversation_xyz"
  
problem_statement:
  diagnosis: |
    Current bootstrap files duplicate context loading logic between BOOTSTRAP.md and 
    individual skills. This creates token waste and maintenance burden. Altitude-awareness 
    is implicit, not explicit.
  context: |
    OmO identified this during context-loading-strategy.md review. The duplication makes 
    it unclear which files are authoritative and increases risk of desync.
  scope: |
    IN SCOPE: Altitude-stratified bootstrap files, context loading protocol
    OUT OF SCOPE: Skill-level context (that stays in skills), bootstrap for non-5×10 work

evaluation_criteria:
  - criterion: "Token efficiency"
    weight: "high"
    rationale: "AI agents have context limits; duplicate loading is expensive"
  - criterion: "Maintainability"
    weight: "high"
    rationale: "Single source of truth prevents desync"
  - criterion: "AI agent orientation"
    weight: "medium"
    rationale: "New agents need to know what to load without reading everything"
  - criterion: "Implementation cost"
    weight: "medium"
    rationale: "Migration cost vs. benefit"

alternatives:
  - id: "A"
    name: "Skill-only context loading"
    summary: |
      Push all context loading into skill files. BOOTSTRAP.md becomes a pure routing 
      index with zero file loads.
    changes:
      - file: "BOOTSTRAP.md"
        action: "edit"
        change: "Strip to routing logic only, no file loading"
      - file: ".claude/skills/*.md"
        action: "edit"
        change: "Add full context loading lists to each skill"
    pros:
      - "Eliminates duplication between bootstrap and skills"
      - "Single source of truth per workflow type"
    cons:
      - "Bootstrap loses orientation value for new agents"
      - "Chicken-and-egg: which skill to invoke?"
    effort: "low"
    risk: "low"
    evaluation:
      token_efficiency: "excellent"
      maintainability: "good"
      ai_agent_orientation: "poor"
      implementation_cost: "excellent"
  
  - id: "B"
    name: "Altitude-stratified bootstrap"
    summary: |
      Create 4 bootstrap files (STRATEGIC, ARCHITECTURE, DELIVERY, RETROSPECTIVE), 
      each loading altitude-common context. Skills add step-specific context on top.
    changes:
      - file: "BOOTSTRAP.md"
        action: "edit"
        change: "Become routing index to altitude-specific bootstraps"
      - file: "BOOTSTRAP-STRATEGIC.md"
        action: "create"
        change: "Load vision, goals, UCs, roadmap, model"
      - file: "BOOTSTRAP-ARCHITECTURE.md"
        action: "create"
        change: "Load decisions, ADRs, containers, synthesis, arch vision"
      - file: "BOOTSTRAP-DELIVERY.md"
        action: "create"
        change: "Load workflow model, standards, state artifacts"
      - file: "BOOTSTRAP-RETROSPECTIVE.md"
        action: "create"
        change: "Load health reports, GAP outputs, retrospective context"
    pros:
      - "Maps directly to 5×10 altitude model"
      - "Agents know which altitude → which bootstrap"
      - "Bootstrap retains orientation value"
      - "Context loading is scoped, not duplicated"
    cons:
      - "More bootstrap files to maintain (4 vs 1)"
      - "Requires discipline to keep altitude boundaries clean"
    effort: "medium"
    risk: "low"
    evaluation:
      token_efficiency: "good"
      maintainability: "good"
      ai_agent_orientation: "excellent"
      implementation_cost: "good"
  
  - id: "C"
    name: "Modular bootstrap with dynamic includes"
    summary: |
      Bootstrap becomes a module registry. Skills declare which modules they need 
      (e.g., `includes: [00-core-identity, 20-architecture-context]`). Advanced.
    changes:
      - file: "BOOTSTRAP.md"
        action: "edit"
        change: "Become module registry with include syntax"
      - file: ".claude/bootstrap-modules/"
        action: "create"
        change: "Create 00-core-identity.md, 01-workflow-model.md, 10-strategic.md, etc."
      - file: ".claude/skills/*.md"
        action: "edit"
        change: "Add `includes: [module1, module2]` frontmatter to each skill"
    pros:
      - "Maximum composability"
      - "No duplication at all"
      - "Easy to add new modules without touching existing files"
    cons:
      - "Most complex to implement"
      - "Requires tooling or discipline to enforce includes"
      - "Harder for humans to read (context scattered)"
    effort: "high"
    risk: "medium"
    evaluation:
      token_efficiency: "excellent"
      maintainability: "excellent"
      ai_agent_orientation: "good"
      implementation_cost: "poor"

recommendation:
  chosen: "B"
  rationale: |
    Altitude-stratified bootstrap strikes the best balance. It maps directly to the 
    5×10 model (agents already think in altitudes), retains bootstrap's orientation 
    value, and eliminates duplication without over-engineering. Option A loses too 
    much orientation value. Option C is premature for current scale (4 skills total).
  runner_up: |
    If the skill count grows to 20+, revisit Option C (modular includes) for 
    maximum composability.

implementation:
  prerequisites:
    - "MODEL-REFERENCE.md exists with 5 altitude definitions"
    - "Current BOOTSTRAP.md is backed up"
  steps:
    - step: "Create BOOTSTRAP-STRATEGIC.md with vision, goals, UCs, roadmap, model"
      verify: "File exists and loads 5 specific docs"
    - step: "Create BOOTSTRAP-ARCHITECTURE.md with decisions, ADRs, containers, synthesis"
      verify: "File exists and loads 6 specific docs"
    - step: "Create BOOTSTRAP-DELIVERY.md with workflow model, standards, state"
      verify: "File exists and loads 4 specific docs"
    - step: "Create BOOTSTRAP-RETROSPECTIVE.md with health, GAP outputs"
      verify: "File exists and loads 3 specific docs"
    - step: "Update BOOTSTRAP.md to routing index"
      verify: "File now points to 4 altitude bootstraps with usage table"
    - step: "Update .claude/skills/full-cycle.md to reference BOOTSTRAP-DELIVERY.md"
      verify: "Skill frontmatter or preamble links to correct bootstrap"
  validation:
    - test: "Run S1 intake with BOOTSTRAP-DELIVERY.md"
      expected: "Agent loads workflow model, standards, and session state correctly"
    - test: "Run SYNTHESIS work with BOOTSTRAP-STRATEGIC.md + BOOTSTRAP-ARCHITECTURE.md"
      expected: "Agent loads UCs, decisions, and prior synthesis without duplication"

context_for_omo:
  files_to_review:
    - "BOOTSTRAP.md (current)"
    - "docs/model/MODEL-REFERENCE.md (altitude definitions)"
    - ".claude/skills/full-cycle.md (example skill)"
  decisions_informed:
    - "None (this is implementation, not a decision)"
  related_artifacts:
    - "docs/research/sessions/2026-05-08_1_context-loading/report.md"
  constraints:
    - "Must not break existing skills during transition"
    - "No new tooling/dependencies"
    - "Backward compatible: BOOTSTRAP.md still works until skills updated"
---
```

## Prose Summary (Optional)

The research identified that the current bootstrap duplicates context loading with skills, 
causing token waste and maintenance burden. Three alternatives were evaluated:

- **Option A (Skill-only):** Eliminates duplication but loses orientation value
- **Option B (Altitude-stratified):** Maps to 5×10 model, retains orientation, eliminates duplication
- **Option C (Modular includes):** Maximum composability but over-engineered for current scale

**Recommendation: Option B.** Create 4 altitude-specific bootstrap files that load common 
context for each altitude. Skills reference the appropriate bootstrap and add step-specific 
context on top.

Implementation requires creating 4 new bootstrap files and updating BOOTSTRAP.md to a 
routing index. Validation: run S1 and SYNTHESIS work with new bootstraps.
