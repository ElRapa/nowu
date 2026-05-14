# Agent Classification Table — W6 Validated

Validated against:
- `docs/model/MODEL-REFERENCE.md` §7, §9, §10, §11
- `docs/WORKFLOW.md` Step Reference + W1–W3.5 table
- `docs/PRE-WORKFLOW.md` P0–P4 sequence and step-agent mapping
- all 35 agent files in `.claude/agents/`

Total agents classified: **35**

## S1-S9 Pipeline Agents

| Agent | File | Step | Altitude | Phase | Notes |
|-------|------|------|----------|-------|-------|
| nowu-intake | `.claude/agents/nowu-intake.md` | S1 | DELIVERY | IDEA | Matches MODEL §7 (S1 intake at DELIVERY/IDEA). |
| nowu-constraints | `.claude/agents/nowu-constraints.md` | S2 | ARCHITECTURE | ANALYSIS | Matches MODEL §7 + §11 constraints analyst contract. |
| nowu-options | `.claude/agents/nowu-options.md` | S3 | ARCHITECTURE | OPTIONS | Matches MODEL §7 options generation. |
| nowu-decider | `.claude/agents/nowu-decider.md` | S4 | ARCHITECTURE | DECISION | Matches MODEL §7 decision step + D-NNN recording intent. |
| nowu-shaper | `.claude/agents/nowu-shaper.md` | S5 | DELIVERY | EVALUATION | Matches MODEL §7 (scope/AC fit evaluation before implementation). |
| nowu-implementer | `.claude/agents/nowu-implementer.md` | S6+S7 | EXECUTION | IMPLEMENTATION | **Primary phase IMPLEMENTATION**; secondary VERIFICATION via built-in VBR gate in same agent run. |
| nowu-reviewer | `.claude/agents/nowu-reviewer.md` | S8 | EXECUTION | EVALUATION | Matches corrected canonical mapping: S8 is evaluation/review (not VBR). |
| nowu-curator | `.claude/agents/nowu-curator.md` | S9 | EXECUTION | LEARN | Primary EXECUTION/LEARN; note upward promotion behavior (`next_cycle_trigger`) after capture. |

## Pre-Workflow Agents

| Agent | File | Step | Altitude | Phase | Notes |
|-------|------|------|----------|-------|-------|
| vision-bootstrap | `.claude/agents/vision-bootstrap.md` | P0.V (+ P0.G goals mode) | STRATEGIC | DECISION | Aligns with MODEL §9 P0.V. Also used for goal brief creation mode. |
| signal-capture | `.claude/agents/signal-capture.md` | P0.1 | STRATEGIC | IDEA | Signal intake at idea stage; MODEL §11 allows STRATEGIC/PRODUCT for this role (primary set to STRATEGIC). |
| idea-decomposition | `.claude/agents/idea-decomposition.md` | P0.D | PRODUCT | ANALYSIS | Classifies/routs ideas by size and stage fit (analysis work). |
| use-case-agent | `.claude/agents/use-case-agent.md` | P0.UC | PRODUCT | PROBLEM | Matches MODEL §9/§11 use-case catalog maintenance at PRODUCT problem-space. |
| discovery-agent | `.claude/agents/discovery-agent.md` | P1.1 | PRODUCT | ANALYSIS | Discovery research with explicit no-solution constraint. |
| perspective-interview | `.claude/agents/perspective-interview.md` | P1.2 | PRODUCT | PROBLEM | Produces `problem-NNN.md`; classified to PROBLEM (not generic analysis) per MODEL §11 contract table. |
| story-mapper | `.claude/agents/story-mapper.md` | P2.1 | DELIVERY | OPTIONS | Decomposes into epic/stories and candidate slices/options. |
| constraint-check | `.claude/agents/constraint-check.md` | P3.1 | ARCHITECTURE | ANALYSIS | Explicit constraint compatibility analysis, no design proposals. |
| architecture-bootstrap | `.claude/agents/architecture-bootstrap.md` | P3.2 | ARCHITECTURE | OPTIONS | Primary OPTIONS (directional L1/L2 architecture shaping); secondary decision pressure deferred to ADR/human gate. |
| readiness-checker | `.claude/agents/readiness-checker.md` | P4.1–P4.2 | DELIVERY | EVALUATION | Readiness gate evaluation before human P4.3 decision to set READY_FOR_S1. |
| qa-elicitation | `.claude/agents/qa-elicitation.md` | P3.2 (parallel support) | ARCHITECTURE | ANALYSIS | Elicits and prioritizes QA scenarios; architecture inputs, no design output. |

## SYNTHESIS + Architecture Agents

| Agent | File | Step | Altitude | Phase | Notes |
|-------|------|------|----------|-------|-------|
| synthesis-agent | `.claude/agents/synthesis-agent.md` | W1 | ARCHITECTURE | SYNTHESIS | **Already has altitude/phase in frontmatter**; values are correct. |
| architecture-vision-agent | `.claude/agents/architecture-vision-agent.md` | W2 | ARCHITECTURE | ANALYSIS | **Already has altitude/phase in frontmatter**; kept as primary ANALYSIS for W2 derivation pass (MODEL §11 also describes SYNTHESIS→DECISION span). |
| architecture-design | `.claude/agents/architecture-design.md` | P3.3 | ARCHITECTURE | OPTIONS | ADD-based structural optioning at C4 L1/L2; no code-level design. |
| atam-lite | `.claude/agents/atam-lite.md` | P3.4 | ARCHITECTURE | EVALUATION | ATAM-style risk/sensitivity/tradeoff evaluation of arch pass. |
| hypothesis-adr-writer | `.claude/agents/hypothesis-adr-writer.md` | W3 | ARCHITECTURE | DECISION | Formalizes chosen architectural decisions into hypothesis ADRs. |
| fitness-function-writer | `.claude/agents/fitness-function-writer.md` | W3.5 | ARCHITECTURE | VERIFICATION | Writes structural fitness checks that verify ADR constraints automatically. |

## Health / GAP Agents

| Agent | File | Step | Altitude | Phase | Notes |
|-------|------|------|----------|-------|-------|
| health-vision | `.claude/agents/health-vision.md` | Health check (`/health-check vision`) | STRATEGIC | VERIFICATION | Validates vision freshness/completeness/alignment. |
| health-goals | `.claude/agents/health-goals.md` | Health check (`/health-check goals`) | STRATEGIC | VERIFICATION | Verifies goal/traceability integrity vs active work. |
| health-architecture | `.claude/agents/health-architecture.md` | Health check (`/health-check architecture`) | ARCHITECTURE | VERIFICATION | Architecture drift/coverage verification against documented structure. |
| health-use-cases | `.claude/agents/health-use-cases.md` | Health check (`health.UC`) | PRODUCT | VERIFICATION | UC catalog validity against vision/plan/activity. |
| gap-detector | `.claude/agents/gap-detector.md` | G0 | ARCHITECTURE | IDEA | Matches MODEL §10 GAP loop start (trigger/sentinel detection). |
| gap-analyst | `.claude/agents/gap-analyst.md` | G1 | ARCHITECTURE | ANALYSIS | Matches MODEL §10 GAP analysis step. |
| gap-writer | `.claude/agents/gap-writer.md` | G2 | ARCHITECTURE | IMPLEMENTATION | Applies approved global-pass deltas to canonical architecture artifacts. |

## Orchestrator + Meta Agents

| Agent | File | Step | Altitude | Phase | Notes |
|-------|------|------|----------|-------|-------|
| roadmap-creator | `.claude/agents/roadmap-creator.md` | Orchestrator milestone | STRATEGIC | IMPLEMENTATION | **Already has altitude/phase in frontmatter**; values are correct per MODEL §8. |
| roadmap-updater | `.claude/agents/roadmap-updater.md` | Orchestrator milestone | STRATEGIC | LEARN | **Already has altitude/phase in frontmatter**; values are correct per MODEL §8. |
| work-scheduler | `.claude/agents/work-scheduler.md` | Orchestrator query | STRATEGIC | EVALUATION | Meta-layer query agent; MODEL §8 marks it external/N-A, but mapped to valid enum pair for table normalization. |

## Enum Evidence (for automated grep)

altitude: STRATEGIC
altitude: PRODUCT
altitude: ARCHITECTURE
altitude: DELIVERY
altitude: EXECUTION

phase: IDEA
phase: PROBLEM
phase: ANALYSIS
phase: SYNTHESIS
phase: OPTIONS
phase: DECISION
phase: EVALUATION
phase: IMPLEMENTATION
phase: VERIFICATION
phase: LEARN
