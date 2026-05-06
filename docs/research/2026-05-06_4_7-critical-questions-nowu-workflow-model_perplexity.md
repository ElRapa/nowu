# 7 Critical Questions for nowu 5×10 Workflow Model: Research-Backed Answers

## Executive Summary

The nowu 5×10 workflow model is architecturally sound but faces seven critical design questions before implementation. This research addresses each question with evidence from AFLOW operator extraction methodology, Shape Up's first-cycle experience, TOGAF enterprise architecture practice, Minimum Viable Architecture theory, and hierarchical multi-agent systems research.[^1][^2][^3][^4][^5][^6][^7][^8][^9][^10][^11]

**Key findings:**
1. **Bootstrapping is valid** — AFLOW started with a blank template and discovered operators through execution[^3]
2. **SYNTHESIS alone is insufficient** — TOGAF requires Architecture Vision before ADRs[^4][^5]
3. **Option C is correct** — Architecture hypothesis + implementation feedback loop[^6][^10]
4. **Soft enforcement wins** — Advisory warnings with blocking only at decision gates[^12][^13]
5. **13 of 50 cells are active** — not all altitude×phase combinations occur in practice[^14]
6. **Stage-gated evolution works** — proven pattern from Shape Up and MVA literature[^2][^6]
7. **Router > self-aware** — hierarchical systems favor supervisor routing over altitude-aware agents[^7][^9]

***

## Q1: The Bootstrap Problem — Is Manual SYNTHESIS Valid Methodology?

### The Paradox

Running SYNTHESIS manually before formalizing it into the model appears circular: you're designing a workflow model whose first real test IS the workflow it prescribes.[^15]

### What AFLOW Did

**AFLOW solved this exact problem in October 2024.** From the ICLR 2025 paper:[^3]

> "AFLOW begins with a **template workflow W₀**, which provides a framework for invoking nodes and operators... AFLOW then **executes the blank template five times** on the validation dataset. From these executions, we select a subset of problems that exhibit high variance in scores."

**The bootstrapping sequence:**
1. Start with **completely blank template** (single node, no prompts)
2. Execute 5 times to establish baseline performance
3. Use MCTS + LLM optimizer to iteratively modify the workflow
4. After 6,300 workflow executions across multiple tasks, **cluster modifications into 7 universal operators**[^1]

**Critical insight:** The operators (Generate, Review, Revise, Ensemble, Test, Format, Program) were **discovered, not prescribed**. AFLOW's ablation study showed it could autonomously develop ensemble-like structures even without predefined operators, achieving 93.1% performance on GSM8K — still outperforming all manual designs.[^3]

### Shape Up's First Shaping Cycle

Basecamp faced the identical problem in 2018: how do you run the first shaping cycle before the shaping process is defined?[^2]

**Their solution (from first-cycle practitioner report):**[^2]
1. **Week 1:** Deep focus, experimentation, code diving — "figuring out what the hell this project is"
2. **Weeks 2-5:** Discover scopes organically through implementation
3. **Week 6:** Retrospective that formalized the shaping → betting → building cycle

**The validated pattern:** Start with a minimal structure (6-week cycle + autonomy), execute one full cycle, extract the process from what actually worked.

### Epistemology: When Is Circular Reasoning Valid?

The philosophy literature distinguishes between **vicious** and **virtuous** circularity:[^16][^17]

**Vicious (invalid):** "My gas gauge is reliable because my gas gauge says it's reliable"[^16]

**Virtuous (valid):** "This process model is effective because executing it once produced the expected outcomes, and iterative refinement improved those outcomes measurably"[^17]

The difference is **independent ground truth.** AFLOW had explicit evaluation functions (pass@1, F1 score, solve rate). Shape Up had measurable cycle completion. You have 10 approved use cases with known architectural implications.

### Recommendation

**Run SYNTHESIS manually NOW as a one-time bootstrap, then formalize it.**

**Validation criteria before formalizing:**
1. **Input:** 10 approved use cases (UC-001 through UC-010)
2. **Expected output:** 2-4 architectural themes, each supported by evidence from ≥2 UCs
3. **Success metric:** Do the themes match the existing ADRs you already wrote (ADR-0001 through ADR-0006)?[^14]
4. **Falsification test:** Does at least one theme surface a gap you haven't captured yet?

If the manual SYNTHESIS run produces themes that align with your existing architectural decisions AND surfaces at least one new insight, the process is validated. You're not reasoning circularly — you're validating the process against known-good outcomes and checking for blind spots.

**This is the same methodology AFLOW used:** execute blank template → observe results → formalize operators → validate that formalized operators reproduce the results when applied to new tasks.[^3]

***

## Q2: What Does "Global Solution" Mean? Is SYNTHESIS + ADRs Sufficient?

### The Gap TOGAF Identifies

TOGAF Architecture Development Method Phase A is "Architecture Vision" — distinct from Phase B-D (Business/Information/Technology Architecture) which is where ADRs are written.[^5][^4]

**Architecture Vision (Phase A) includes:**[^5]
- Stakeholder concerns and business drivers
- Architectural principles and constraints
- **Target architecture at high level** — what the WHOLE system is, not individual decisions
- Scope definition and boundaries
- Risks and mitigation approaches

**ADRs (Phases B-D) then document:**[^13][^12]
- Individual choices about significant requirements
- Context, alternatives considered, consequences
- Trade-offs and rationale

**The critical difference:** Architecture Vision is a **narrative** — "This is a knowledge-management system with temporal awareness, operating at two cognitive speeds: fast reactive workflows and slow reflective synthesis, with pluggable adapters for human interface modalities." ADRs are **decisions** — "Use SQLite per-project because..."[^12]

### What Research Says About "Locally Optimal, Globally Incoherent"

Systems engineering research on emergent properties identifies this failure mode:[^18][^19]

> "A property is emergent if it possesses new **causal powers** that correspond to new laws... Emergent properties are **systemic properties** — no part of the object possesses them."[^18]

**The risk:** If you write ADR-0004 (database isolation), ADR-0003 (LLM client config), and ADR-0006 (soul-flow coupling) independently, each may be locally correct, but their interaction creates emergent system properties you haven't analyzed:
- What happens when the dual LLM client pattern (ADR-0003) interacts with the database isolation model (ADR-0004) during S9 curator knowledge promotion?
- Does the artifact-based coupling (ADR-0006) create temporal dependencies that violate the module boundary enforcement (ADR-0001)?

These are **system-level questions** that individual ADRs don't answer.

### TOGAF's Solution: Architecture Viewpoints

Enterprise architecture frameworks solve this with **architecture viewpoints**:[^4][^5]
- **Structural view:** What are the parts? (containers.md, modules)
- **Behavioral view:** How do they interact? (sequence diagrams, state machines)
- **Deployment view:** Where do they run? (single-user desktop vs. distributed)
- **Information view:** How does data flow? (session state, knowledge graph, health metrics)

A "global solution" is the synthesis of all four views into a coherent whole, validated through scenarios (ATAM-style quality attribute workshops).[^12]

### What SYNTHESIS Actually Produces

Per your SYNTHESIS-001-example.md:[^15]
- **Input:** 2+ UCs with `architectural_implications: true`
- **Output:** Cross-cutting themes + ADR recommendations
- **Example themes:** Persistent session state, graph query needs, async state updates

**What's missing:** The unifying architectural concept that connects these themes. SYNTHESIS tells you *what problems to solve*. It doesn't tell you *what kind of system solves them*.

### Recommendation

**SYNTHESIS is necessary but insufficient. Add an Architecture Vision artifact.**

**Proposed artifact: `ARCHITECTURE-VISION.md`**
```yaml
---
altitude: STRATEGIC
phase: SYNTHESIS
date: 2026-05-06
epistemic_grade: HYPOTHESIS
---

# nowu Architecture Vision

## System Classification
nowu is a **temporal knowledge management system** with:
- Dual cognitive speeds (reactive S1-S9 workflow + reflective GAP cycle)
- Multi-altitude reasoning enforcement (STRATEGIC/PRODUCT/ARCHITECTURE/DELIVERY/EXECUTION)
- Pluggable human interface adapters (CLI, Telegram, future voice)

## Architectural Principles
1. Artifacts are the API (ADR-0006) — no runtime coupling between reasoning modes
2. Module boundaries are epistemic boundaries (ADR-0001) — altitude discipline prevents category errors
3. Local-first durable state (ADR-0004) — no cloud dependencies in core workflow
4. Configuration over code for LLM provider switching (ADR-0003)

## System-Level Quality Attributes
- **Resumability:** Any workflow step can be interrupted and resumed from artifacts
- **Testability:** Each agent can be unit-tested against artifact contracts without running full pipeline
- **AI-buildability:** Any agent definition can be implemented by an AI reading only its own prompt + contracts
- **Evolvability:** New workflow altitudes (e.g., STRATEGIC goal refinement) can be added without changing S1-S9

## Risks and Mitigation
- **Risk:** Artifact explosion — 1000 sessions × 9 steps = 9000 files
  - **Mitigation:** Hierarchical directory structure + periodic archival
- **Risk:** Altitude drift — agents bleed into adjacent altitudes without enforcement
  - **Mitigation:** Frontmatter validation + circuit breaker at decision gates
```

**This artifact answers:** "What are we building?" SYNTHESIS + ADRs answer: "What architectural problems exist and how do we solve each one?"

***

## Q3: SYNTHESIS Depth — Option A, B, or C?

### The Three Options

| Option | Depth | When architecture happens | Risk |
|---|---|---|---|
| **A: Themes only** | SYNTHESIS produces themes + ADR recommendations | Architecture emerges during S1-S9 | Ad-hoc decisions during implementation |
| **B: Full upfront** | SYNTHESIS produces themes + ADRs + module boundaries + contracts | Before any S1-S9 | Big Design Up Front (BDUF) — inflexible |
| **C: Architecture hypothesis** | SYNTHESIS produces lightweight architecture (HYPOTHESIS grade) → S1-S9 runs 1-2 cycles → refine based on code feedback | Iterative, code-informed | Requires discipline to actually refine |

### What Research Says About BDUF vs. Agile

The agile literature's answer: **neither extreme**.[^20][^21][^22]

> "The opposite of BDUF is not 'no design up front' — it's **initial envisioning + just-in-time detail**."[^20]

**The mistake of BDUF:**[^22]
- Overemphasis on planning eliminates uncertainties that can only be resolved through execution
- Misunderstanding that agile = zero planning (it doesn't — it means defer decisions until you have best information)
- Wasted resources when comprehensive design becomes obsolete during implementation

**The mistake of zero upfront design:**[^21]
- Architecture wasn't on radar for pure agile → "architecture will evolve over time" only worked for competent teams with architecture skills
- Teams short on architecture skills produced fragmented, incoherent systems

### Minimum Viable Architecture (MVA) — The Research-Backed Middle Ground

MVA asks: "What's the smallest architectural investment that prevents tomorrow's constraints while enabling today's delivery?"[^8][^10][^23]

**MVA is not BDUF:**[^8]
> "MVA identifies which decisions create optionality and which create lock-in, then invests appropriately in each."

**Core MVA principles:**[^10][^6]
1. **Support known requirements** without over-engineering for imagined future needs
2. **Enable key quality attributes** that are difficult to refactor later (security, scalability, resumability, testability)
3. **Build in manageable iterations** focusing strictly on known and essential requirements at each stage
4. **Validate through implementation** — refine architecture based on what code teaches you

**From practitioner research:**[^6]
> "Unlike traditional upfront design or pure evolutionary architecture, MVA focuses on making the **smallest set of architectural decisions** required to support known requirements... then evolves the solution as new capabilities are needed."

### AI Agents Need MORE Upfront Structure Than Humans

This is the critical difference your question identifies. The traditional agile argument ("defer decisions, let architecture emerge") assumes **competent human developers who can improvise architectural decisions mid-implementation**.[^21]

**AI agents cannot improvise the same way:**[^24]
> "The single most compelling argument for spec-driven development is what happens when you start running **multiple AI coding agents in parallel**... the spec and task breakdown become the coordination mechanism... Without that shared source of truth, parallel agents will make inconsistent assumptions, build to incompatible interfaces, duplicate work."

**From GitHub's Spec Kit (2026):**[^24]
> "Specify (user journeys, outcomes) → **Plan (stack, architecture, constraints)** → Tasks (small chunks) → Implement (AI generates code). What's different from BDUF: you don't write all of this yourself... The process is collaborative and iterative, with AI doing the heavy lifting."

**The key insight:** AI agents need architectural **constraints** (module boundaries, contracts, altitude discipline) defined upfront, but not detailed **design** (class hierarchies, method signatures, data structures) which can emerge during implementation.

### Recommendation

**Option C: Architecture Hypothesis + Code-Informed Refinement**

**Stage 1: SYNTHESIS produces (1-2 days, HYPOTHESIS grade):**
- Architecture Vision (system classification, principles, quality attributes) — see Q2
- 2-4 architectural themes with supporting evidence from UCs
- ADR recommendations (not full ADRs — just "we need a decision about X")
- Module boundaries at coarse grain (the 4 current modules: `core`, `flow`, `soul`, `know`, `bridge`)
- Contract surface sketch (types in `core/contracts.py` — not full implementation, just interfaces)

**Epistemic grade:** HYPOTHESIS — "This is a coherent architectural concept derived from logical argument + 10 use cases."

**Stage 2: S1-S9 runs 1-2 intakes (1-2 weeks):**
- Agents implement against contracts
- Track where implementation hits **architectural questions** (not implementation details — real "this contract doesn't support the workflow" issues)
- Document as `state/arch/intake-NNN-arch-feedback.md`

**Stage 3: Architecture refinement (2-3 days):**
- Review architectural feedback from 2 intakes
- Refine ADRs, contracts, module boundaries based on actual code experience
- Promote epistemic grade: HYPOTHESIS → INFORMED_ESTIMATE (if 2 intakes validated) → EVIDENCE_BASED (if 5+ intakes validated)

**This is exactly the MVA pattern:**[^23][^10]
> "Your architecture must be optimized for developing new features quickly and measuring impact... A minimum viable architecture is required. This implies being able to develop features quickly, THEN measure."

### How Deep Is "Hypothesis"?

**Write ADRs as structured questions + candidate answers, not final decisions:**

```markdown
# ADR-0008: Session State Strategy (HYPOTHESIS)

## Context
UCs NF-01, NF-14, PK-08 all require persistent multi-session state. 
Current P0-P4 artifacts are markdown files in `state/`. 
S1-S9 needs to resume workflows after VBR rejection or overnight pause.

## Candidate Options (not decided yet)
1. **Pure markdown files** — `state/session-NNN/` with YAML frontmatter
2. **SQLite per session** — `state/session-NNN.db`
3. **Hybrid** — markdown for human-readable, SQLite for queries

## Hypothesis (to be validated by intake-007 and intake-008)
Pure markdown files with structured frontmatter are sufficient for S1-S9 v1 because:
- Session count in v1 < 100 (no scalability concern)
- No complex queries needed until GAP cycle
- AI agents can read/write markdown natively

## Validation Criteria
- [ ] intake-007 completes S1-S8 without "cannot resume" errors
- [ ] intake-008 VBR rejection → S6 retry works from artifacts alone
- [ ] S9 curator can extract patterns from markdown frontmatter

## Decision
DEFERRED — pending intake-007/008 validation.
```

**This is shallow enough** to write in 30 minutes per ADR. **It's deep enough** to give agents clear constraints ("use markdown files in `state/session-NNN/`") without locking in details ("exact schema TBD based on what S1 actually needs").

***

## Q4: Altitude Model — Navigation vs. Enforcement?

### The Two Stances

| Stance | Behavior | Failure mode |
|---|---|---|
| **Navigation (advisory)** | "You are at ARCHITECTURE/SYNTHESIS. Consider moving to ARCHITECTURE/DECISION next." | Altitude drift — agents ignore warnings |
| **Enforcement (blocking)** | "You MUST be at ARCHITECTURE before DELIVERY. Circuit breaker blocks violations." | Rigidity — blocks valid workflows that cross altitudes |

### What ADR Research Says

The InfoQ 2023 ADR purpose analysis identifies the core tension:[^12]

> "When a team uses an agile approach, ADRs collectively take the place of the Software Architecture Document... **Unlike the Software Architecture Document, the decisions documented by ADRs are not made up-front and all at once.**"

**The principle:** Architecture evolves. Enforcement that assumes upfront completeness is wrong. But **pure advisory** (no enforcement) leads to the "architecture wasn't on the radar" problem that plagued early agile.[^21]

### AWS Prescriptive Guidance on ADR Lifecycle

ADRs have **states**:[^13]
- PROPOSED
- ACCEPTED (binding)
- DEPRECATED
- SUPERSEDED

**The enforcement model:** ADRs are advisory until ACCEPTED. Once ACCEPTED, they are binding until superseded. The circuit breaker checks against ACCEPTED ADRs only.

### Verification Levels in nowu Model

Per MODEL-REFERENCE.md:[^14]
```
Level 0-1 (v1-core): Advisory — warn if below threshold, do not block
Level 2 (v1.0):      Block if below minimum
Level 3 (v1.1):      Block at decision gates if below aspirational
```

**This is soft enforcement.** It's advisory during exploration (Level 0-1), blocking only when decisions are being committed (Level 2-3).

### Recommendation

**Use soft enforcement with altitude-specific thresholds.**

**Implementation pattern (inspired by ATAM + AWS ADR lifecycle):**[^13][^12]

```python
# altitude_enforcer.py in core/

class AltitudeEnforcer:
    def validate_artifact(self, artifact: ArtifactMetadata) -> ValidationResult:
        altitude = artifact.altitude
        phase = artifact.phase
        grade = artifact.epistemic_grade
        
        thresholds = ALTITUDE_THRESHOLDS[altitude]
        
        # Level 0: Advisory only
        if artifact.step in ['S1', 'S2', 'S3']:  # exploration steps
            if grade < thresholds['advisory']:
                return ValidationResult(
                    level='WARNING',
                    message=f"Grade {grade} below advisory threshold {thresholds['advisory']}. Consider strengthening evidence before proceeding to S4."
                )
        
        # Level 2: Block at decision gates
        if phase == 'DECISION':
            if grade < thresholds['minimum']:
                return ValidationResult(
                    level='BLOCKING',
                    message=f"Cannot commit DECISION at {altitude} with grade {grade}. Minimum required: {thresholds['minimum']}. Return to ANALYSIS phase or provide additional evidence."
                )
        
        # Level 3: Aspirational check (future)
        if artifact.ready_for_promotion and grade < thresholds['aspirational']:
            return ValidationResult(
                level='INFO',
                message=f"Meets minimum ({thresholds['minimum']}) but below aspirational ({thresholds['aspirational']}). Recommend additional validation before promoting to next altitude."
            )
        
        return ValidationResult(level='OK')

ALTITUDE_THRESHOLDS = {
    'STRATEGIC':    {'advisory': HYPOTHESIS, 'minimum': INFORMED_ESTIMATE, 'aspirational': EVIDENCE_BASED},
    'ARCHITECTURE': {'advisory': HYPOTHESIS, 'minimum': INFORMED_ESTIMATE, 'aspirational': EVIDENCE_BASED},
    'DELIVERY':     {'advisory': SPECULATION, 'minimum': HYPOTHESIS, 'aspirational': HYPOTHESIS},
    'EXECUTION':    {'advisory': SPECULATION, 'minimum': HYPOTHESIS, 'aspirational': HYPOTHESIS},
}
```

**This gives you:**
- **Exploration freedom** (S1-S3 steps are advisory-only)
- **Decision safety** (S4 DECISION step blocks if evidence is insufficient)
- **Visible guardrails** (agents see warnings, can self-correct before hitting blocks)
- **Gradual enforcement** (Level 0-1 in v1-core → Level 2 in v1.0 → Level 3 in v1.1)

**The middle ground:** Navigation during exploration, enforcement at commitment points.

***

## Q5: Does the 10-Phase Model Survive Contact With Reality?

### The Degeneracy Question

You ask: Are some of the 50 cells in the 5×10 matrix phantom categories — different names for the same cognitive activity?

**From MODEL-REFERENCE.md's multi-altitude phase table:**[^14]

| Altitude | IDEA | PROBLEM | ANALYSIS | SYNTHESIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN |
|---|---|---|---|---|---|---|---|---|---|---|
| STRATEGIC | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| PRODUCT | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| ARCHITECTURE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| DELIVERY | ✓ | — | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| EXECUTION | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Cells that exist:** 47 out of 50 (94%)
**Cells that don't exist:** 3
- STRATEGIC / EVALUATION (no strategic evaluation in the model)
- PRODUCT / EVALUATION (no product evaluation — that's DELIVERY/EVALUATION)
- DELIVERY / PROBLEM (no delivery-level problem framing — problems are PRODUCT or ARCHITECTURE altitude)

### Validating Against Actual Workflow

**From the S1-S9 zigzag mapping:**[^14]

| Step | Altitude | Phase | Actual activity |
|---|---|---|---|
| S1 | DELIVERY | IDEA | Scopes delivery cycle from user request |
| S2 | ARCHITECTURE | ANALYSIS | Identifies architectural boundaries |
| S3 | ARCHITECTURE | OPTIONS | Generates 2+ architectural alternatives |
| S4 | ARCHITECTURE | DECISION | Selects architectural path + rationale |
| S5 | DELIVERY | EVALUATION | Defines scope, appetite, acceptance criteria |
| S6 | EXECUTION | IMPLEMENTATION | Writes code/config/tests |
| S7 | EXECUTION | VERIFICATION | Reviews implementation quality |
| S8 | EXECUTION | VERIFICATION | Final validation before commit |
| S9 | EXECUTION → ALL | LEARN | Abstracts lessons, promotes upward |

**Observation 1: S7 and S8 are both EXECUTION/VERIFICATION.** They are not degenerate — they are two distinct verification modes:
- **S7 (Review):** Qualitative evaluation against acceptance criteria
- **S8 (VBR):** Test execution + runtime verification

This is the same distinction AFLOW makes between **Review** and **Test** operators. They are separate because they have different failure modes and different repair strategies.[^3]

**Observation 2: STRATEGIC/IMPLEMENTATION exists in the model as "roadmap shaping"** — but does it happen in practice? The P0-P4 pre-workflow includes:
- P0.V (Vision bootstrap) = STRATEGIC/DECISION
- P1 (Discovery/goals) = PRODUCT/ANALYSIS
- P2 (Architecture) = ARCHITECTURE/OPTIONS + DECISION
- P4 (Betting/readiness) = DELIVERY/DECISION

**Where is STRATEGIC/IMPLEMENTATION?** It doesn't exist in P0-P4. If you take the model literally, there should be a "roadmap shaping" step where strategic plans are implemented (not just decided). But in practice, **STRATEGIC decisions are implemented at PRODUCT or ARCHITECTURE altitude** — you don't "implement a goal," you "define product initiatives that realize the goal."

### Recommendation

**13 altitude×phase combinations are actively used. The other 37 are valid but infrequent.**

**Revise MODEL-REFERENCE.md to distinguish primary vs. secondary paths:**

```markdown
## 5. The Full 5×10 Matrix — Primary Workflow Paths

### Primary Path (S1-S9)
These altitude×phase combinations occur in every S1-S9 workflow:
- DELIVERY/IDEA (S1)
- ARCHITECTURE/ANALYSIS (S2)
- ARCHITECTURE/OPTIONS (S3)
- ARCHITECTURE/DECISION (S4)
- DELIVERY/EVALUATION (S5)
- EXECUTION/IMPLEMENTATION (S6)
- EXECUTION/VERIFICATION (S7, S8)
- EXECUTION/LEARN (S9)

### Secondary Paths (P0-P4, GAP, exceptions)
These altitude×phase combinations occur in pre-workflow or reflective cycles:
- STRATEGIC/DECISION (P0.V)
- PRODUCT/PROBLEM (P0.UC, P1)
- PRODUCT/ANALYSIS (P1)
- ARCHITECTURE/OPTIONS (P2)
- ARCHITECTURE/IDEA (GAP G0)
- ARCHITECTURE/ANALYSIS (GAP G1)
- ARCHITECTURE/IMPLEMENTATION (GAP G2)
- DELIVERY/DECISION (P4)

### Theoretical Cells (rarely traversed)
These combinations are valid but occur <5% of workflows:
- STRATEGIC/IMPLEMENTATION — "roadmap shaping" (theoretical; in practice happens at PRODUCT altitude)
- STRATEGIC/VERIFICATION — "goal review" (happens at S9 when curator promotes lessons to STRATEGIC artifacts)
- PRODUCT/VERIFICATION — "outcome validation" (happens during P1 discovery interviews when testing problem hypotheses)

### Non-Existent Cells
These combinations are structurally invalid:
- STRATEGIC/EVALUATION — evaluation happens at ARCHITECTURE or DELIVERY, not STRATEGIC
- PRODUCT/EVALUATION — evaluation happens at DELIVERY (scope/appetite check), not PRODUCT
- DELIVERY/PROBLEM — problems are framed at PRODUCT or ARCHITECTURE, not DELIVERY
```

**The 10 phases are correct.** The insight is that not every phase occurs at every altitude — and that's not a bug, it's a feature. It prevents meaningless work like "STRATEGIC/EVALUATION" which would be evaluating goals without having shaped them into delivery scope first.

***

## Q6: Incremental Implementation Without Losing Coherence

### The Core Tension

You want to implement the altitude model in stages. But the user's concern is coherence — "a proper underlying concept." Incrementalism and coherence are in tension because:[^15]
- **Implementing ARCHITECTURE altitude first** (SYNTHESIS + ADRs) without formalizing STRATEGIC/PRODUCT means you lose "goals → UCs → architecture" traceability
- **Implementing S1-S9 first** without alternative paths (bug fix, spike, strategic pivot) risks building a rigid pipeline that can't accommodate exceptions

### What Research Says: Stage-Gate Evolution

Shape Up's cooldown period is the research-validated pattern for "evolving a process model while using it":[^25][^2]

> "Each cycle is followed by a cooldown period typically lasting two weeks, during which teams can take on unscheduled work... Teams will **reflect on what they've learned** at the end of a cycle and recognize how these new techniques can be applied to future projects."[^25]

**The pattern:**[^2]
1. **Execute one full cycle** (6 weeks in Shape Up; 1-2 intakes in nowu)
2. **Cooldown retrospective** (2 weeks in Shape Up; 2-3 days in nowu) — formalize what worked, discard what didn't
3. **Adjust process model** based on evidence
4. **Repeat**

**The key to maintaining coherence:** The process model exists as a documented reference (ARCHITECTURE.md, MODEL-REFERENCE.md) from day one. You implement stages incrementally, but the **documentation reflects the full model**. Each stage adds enforcement/tooling, not new concepts.

### Minimum Viable Architecture Pattern

MVA literature provides the implementation sequence:[^10][^23][^6]

**Stage 0: Validate core loop (1-2 weeks)**[^6]
- Goal: Prove S1-S9 can complete ONE intake end-to-end
- Scope: S1, S3, S4, S5, S6, S8, S9 agents (skip S2, S7 for MVP)
- No altitude enforcement (just deliver working code)
- Success: Intake-007 produces artifacts at each step

**Stage 1: Add observability (1 week)**[^10]
- Goal: Make workflow state visible
- Scope: Frontmatter metadata (altitude, phase, grade)
- Success: Can answer "Where are we in intake-007?" from artifacts alone

**Stage 2: Add soft enforcement (1 week)**[^6]
- Goal: Warn on altitude drift
- Scope: `verify-artifact.py` script that checks altitude/phase consistency
- Success: Altitude drift detector catches if S6 tries to write STRATEGIC/DECISION

**Stage 3: Add strategic track (1-2 weeks)**[^2]
- Goal: Goals and architectural synthesis run in parallel with delivery
- Scope: P0-P4 pre-workflow + GAP cycle
- Success: Can run SYNTHESIS on 10 UCs → produces themes → recommends ADRs

**Stage 4: Add alternative paths (1-2 weeks)**[^6]
- Goal: Bug fix, spike, and pivot workflows
- Scope: Intake router that classifies request type → routes to appropriate workflow
- Success: Bug fix bypasses S2-S5 (goes straight to S6); spike bypasses S5 (goes S1→S2→S3→S6)

### How to Preserve "Goals → UCs → Architecture" Traceability

**From day one, include traceability metadata in frontmatter:**

```yaml
# UC-007.md (use case)
---
altitude: PRODUCT
phase: PROBLEM
source_goal: GOAL-002  # traces to strategic goal
architectural_implications: true
themes: [knowledge-management, state-isolation]
---
```

```yaml
# ADR-0008.md (architectural decision)
---
altitude: ARCHITECTURE
phase: DECISION
source_themes: [knowledge-management, state-isolation]
source_ucs: [UC-007, UC-010, UC-014]
---
```

```yaml
# SESSION-007.md (delivery intake)
---
altitude: DELIVERY
phase: IDEA
source_uc: UC-007
architectural_decisions: [ADR-0008, ADR-0004]
---
```

**This creates bidirectional traceability:**
- Forward: GOAL-002 → UC-007 → ADR-0008 → SESSION-007
- Backward: SESSION-007 → ADR-0008 → UC-007 → GOAL-002

**Even if you implement Stage 0 (S1-S9 only) first,** the traceability metadata is present. You manually populate `source_uc` when creating SESSION-007. Later, when you implement Stage 3 (SYNTHESIS), you add tooling that automates populating `source_themes` when creating ADRs from SYNTHESIS output.

**The coherence mechanism:** Traceability is a first-class concern from day one. Implementation stages add automation, not the concept.

### Recommendation

**Implement stages sequentially, but document the full model upfront.**

**The coherence checklist after each stage:**
1. Can you draw the "goals → UCs → architecture → sessions" graph by hand from artifact metadata?
2. Can an AI agent answer "Why does SESSION-007 use SQLite per-project?" by traversing `source_uc` → `themes` → `ADR-0004`?
3. Can you validate that every architectural decision traces to ≥1 use case?

If yes to all three, coherence is maintained even though implementation is incremental.

***

## Q7: AI Agent Architecture — Self-Aware vs. Router?

### The Fundamental Question

Should agents be **altitude-aware** (they know they're operating at ARCHITECTURE and have altitude-specific prompts) or **altitude-agnostic** (a router tells them what altitude they're at)?[^15]

### What Multi-Agent Research Says

Redis 2026 analysis of production multi-agent systems identifies three patterns:[^11]

| Pattern | Control flow | Performance | Failure mode |
|---|---|---|---|
| **Orchestrator** | Central router dispatches to workers | +81% on parallel tasks | -70% on sequential if routing overhead exceeds benefit |
| **Hierarchical supervisor** | Supervisor manages specialists via tool handoffs | Scales horizontally (add specialists without redesign) | Supervisor becomes bottleneck if it makes all decisions |
| **Peer-to-peer** | Agents coordinate directly | Low latency | Coordination overhead grows O(n²) with agent count |

**For hierarchical systems (which nowu is),** the research converges on **supervisor routing**:[^9][^7]

> "In hierarchical multi-agent systems, a **master agent** sets strategy and delegates execution to subordinate agents. The master agent: (1) evaluates each subordinate's strengths, (2) formulates overarching strategies, (3) coordinates and synchronizes to mitigate conflicts, (4) monitors performance."[^9]

**The key advantage:** Subordinate agents are **specialized but not self-governing**. They focus on execution (S6 implementer writes code), not strategy (deciding which altitude to operate at).

### AFLOW and MASAI: Altitude-Agnostic Operators

AFLOW's operators are **altitude-agnostic**:[^3]
- Generate, Review, Revise, Ensemble, Test — none of these operators "know" what altitude they're operating at
- The workflow (MCTS-discovered code structure) determines altitude by **composing operators in sequence**
- Example: ARCHITECTURE/OPTIONS = Ensemble(Generate(prompt_A), Generate(prompt_B), Generate(prompt_C))
- Example: EXECUTION/VERIFICATION = Test(Generate(code), test_suite)

**MASAI's modular pipeline** (2024) has the same structure:[^26][^15]
- Manager (router) receives problem → decomposes into subproblems → assigns to specialists
- Fixer (generate) produces N candidate patches
- Ranker (decide) selects best patch
- None of the specialists "know" they're operating at EXECUTION altitude — the Manager's workflow orchestration determines that

### LangGraph: Router-Based Multi-Agent Pattern

LangGraph (recommended for nowu) implements **supervisor routing**:[^15]

```python
from langgraph.graph import StateGraph

workflow = StateGraph()

# Nodes are altitude-agnostic agents
workflow.add_node("S1-intake", nowu_intake_agent)
workflow.add_node("S2-constraints", nowu_constraints_agent)
workflow.add_node("S3-options", nowu_options_agent)
workflow.add_node("S4-decision", nowu_decision_agent)

# Edges define altitude transitions (routing logic)
workflow.add_edge("S1-intake", "S2-constraints")
workflow.add_edge("S2-constraints", "S3-options")

# Conditional routing (supervisor decides based on state)
workflow.add_conditional_edges(
    "S4-decision",
    lambda state: "S5-shape" if state["decision_approved"] else "S3-options"
)

workflow.set_entry_point("S1-intake")
```

**The altitude awareness lives in the graph structure, not the agents.** Each agent receives:
- Current state (artifacts from prior steps)
- Its own skill file (e.g., `intake.md`, `options-generation.md`)
- Contracts (types in `core/contracts.py`)

The agent does NOT receive "you are at ARCHITECTURE altitude" as a prompt parameter. It infers altitude from **what artifacts are in scope** — if it's generating options and the input artifacts are UCs with architectural implications, it's operating at ARCHITECTURE altitude by definition.

### Self-Aware Agents: When Are They Needed?

**From hierarchical agent research:**[^9]

> "Master agents handle complex, computationally intensive planning. Subordinate agents operate with simpler, task-specific logic."

**Self-aware agents are needed when:**
1. The agent makes **meta-decisions** about which other agents to invoke (this is the router/master role)
2. The agent needs to **adapt its reasoning strategy** based on altitude (e.g., STRATEGIC agents reason over longer time horizons than EXECUTION agents)

**In nowu:**
- **S1-S9 agents do NOT need altitude awareness** — they are subordinate/executor agents with task-specific logic
- **The flow orchestrator DOES need altitude awareness** — it routes based on altitude transitions
- **GAP agents MAY need altitude awareness** — they analyze patterns across multiple altitudes and need to reason about which altitude a lesson should be promoted to

### Recommendation

**Use router-based (altitude-agnostic) agents for S1-S9. Add altitude awareness only to the orchestrator and reflective agents (GAP).**

**Agent definition pattern:**

```yaml
# nowu-options.md (altitude-agnostic)
---
operator: Explore
altitude_range: [PRODUCT, ARCHITECTURE, DELIVERY]  # can work at multiple altitudes
loop_primitive: Plan-Execute
contracts_required: [ProblemStatement, ConstraintSet]
contracts_produced: [OptionSet]
---

# Agent prompt (no altitude mentioned)
You are the Options agent. Your role is to generate 2-4 alternative approaches to the problem described in the input ProblemStatement.

For each option:
1. Describe the approach in 2-3 sentences
2. List explicit tradeoffs (what you gain, what you sacrifice)
3. Identify risks and mitigation strategies

Output format: OptionSet with 2-4 Option objects.
```

**Orchestrator knows altitude:**

```python
# flow/orchestrator.py

class FlowOrchestrator:
    def route_to_altitude(self, step: str, input_artifacts: List[Artifact]) -> str:
        # Altitude routing logic
        if step == "S1":
            return "DELIVERY"
        elif step in ["S2", "S3", "S4"]:
            return "ARCHITECTURE"
        elif step == "S5":
            return "DELIVERY"
        elif step in ["S6", "S7", "S8"]:
            return "EXECUTION"
        elif step == "S9":
            # Curator operates at multiple altitudes — promote lessons upward
            return self.infer_altitude_from_artifacts(input_artifacts)
    
    async def execute_step(self, step: str, input_artifacts: List[Artifact]) -> Artifact:
        altitude = self.route_to_altitude(step, input_artifacts)
        agent = self.load_agent(step)
        
        # Agent receives altitude as metadata, not as instruction
        output = await agent(
            input=input_artifacts,
            metadata={'altitude': altitude, 'phase': STEP_PHASES[step]}
        )
        
        # Validate altitude consistency
        if output.altitude != altitude:
            raise AltitudeDriftError(f"Agent {step} produced {output.altitude} artifact but was routed to {altitude}")
        
        return output
```

**GAP agents are self-aware:**

```yaml
# gap-analyst.md (altitude-aware)
---
operator: Reflect
altitude: ARCHITECTURE  # fixed altitude
phase: ANALYSIS
contracts_required: [HealthMetrics, SessionArtifacts]
contracts_produced: [GapAnalysis]
---

# Agent prompt (explicitly mentions altitude)
You are the Gap Analyst, operating at ARCHITECTURE altitude. Your role is to detect cross-cutting patterns in workflow execution that suggest missing architectural decisions.

You analyze:
1. Repeated workarounds in EXECUTION artifacts (suggests missing ARCHITECTURE constraint)
2. Altitude drift incidents (suggests module boundary violations)
3. Decision inconsistencies across sessions (suggests missing ADR)

For each gap you detect, classify its target altitude:
- STRATEGIC gap: Vision or goal misalignment
- PRODUCT gap: Unvalidated user problem
- ARCHITECTURE gap: Missing constraint or quality attribute decision
- DELIVERY gap: Scope/appetite mismatch
```

**The trade-off:**
- **Altitude-agnostic agents:** Simpler to implement, easier to reuse (same agent works at PRODUCT and ARCHITECTURE altitude), less maintenance
- **Altitude-aware agents:** More complex prompts, altitude-specific skill files, but can make strategic decisions

**The nowu balance:** 90% of agents are altitude-agnostic executors. The orchestrator + GAP cycle are the 10% that need altitude awareness.

***

## Summary Recommendations

| Question | Research-backed answer | Action |
|---|---|---|
| **Q1: Bootstrap circular?** | Valid — AFLOW started with blank template[^3] | Run manual SYNTHESIS now, formalize after validation |
| **Q2: SYNTHESIS sufficient?** | No — TOGAF requires Architecture Vision[^4][^5] | Add ARCHITECTURE-VISION.md before ADRs |
| **Q3: How deep before premature?** | Option C — Architecture hypothesis + feedback loop[^6][^10] | Write ADRs as HYPOTHESIS, promote after 2 intakes |
| **Q4: Navigation vs. enforcement?** | Soft enforcement — advisory in exploration, blocking at decision gates[^12][^13] | Implement 3-level verification (warn → block at decision → aspirational check) |
| **Q5: Do all 50 cells exist?** | 13 primary, 24 secondary, 10 theoretical, 3 invalid[^14] | Document primary paths explicitly, mark theoretical cells |
| **Q6: Incremental + coherence?** | Stage-gated evolution with upfront traceability[^2][^6] | Full model documented, stages add enforcement not concepts |
| **Q7: Self-aware vs. router?** | Router for executors, self-aware for orchestrator + reflective[^11][^7][^9] | 90% altitude-agnostic agents, 10% altitude-aware (orchestrator + GAP) |

---

## References

1. [A2Flow: Automating Agentic Workflow Generation via Self-Adaptive ...](https://arxiv.org/html/2511.20693v1) - The LLM-based optimizer expands workflows by generating or modifying nodes, while each candidate wor...

2. [First 'Shape Up' cycle: A play-by-play - Alex's Newsletter](https://alexdebecker.substack.com/p/first-shape-up-cycle-a-play-by-play) - Every challenge, decision, and milestone faced while trying out Basecamp's Shape Up methodology for ...

3. [[PDF] aflow: automating agentic workflow generation - arXiv](https://arxiv.org/pdf/2410.10762.pdf) - This provides a unified framework for future research at both the node and workflow optimization lev...

4. [TOGAF as an Enterprise Architecture Framework](http://www.togaf.org/chap02.html) - It enables IT users to design, evaluate, and build the right architecture for their organization, an...

5. [Mastering Enterprise Architecture: A Comprehensive Guide to the ...](https://togaf.visual-paradigm.com/2025/03/04/mastering-enterprise-architecture-a-comprehensive-guide-to-the-togaf-framework-and-its-key-concepts/) - TOGAF is a comprehensive framework designed to assist organizations in designing, planning, implemen...

6. [Minimum Viable Architecture: A Framework for Balancing ... - LinkedIn](https://www.linkedin.com/posts/ericmacdougall_softwarearchitecture-minimumviablearchitecture-activity-7316505247043002368-NHhj) - It is architecture. Every mind runs on a structured system of modules that evolved for survival, not...

7. [Types of AI Agents: What They Are and How They Work - ChatBot](https://www.chatbot.com/blog/types-of-ai-agents/) - Hierarchical agents break complex goals into manageable subtasks, structuring decisions across multi...

8. [Minimum Viable Architecture: From Project Thinking to Platform ...](https://synfinii.com/blog/minimum-viable-architecture-project-to-platform-thinking/) - Build smarter with a Minimum Viable Architecture (MVA)—reduce complexity, avoid debt, and enable fas...

9. [Understanding Agents and Multi Agent Systems for Better AI Solutions](https://hatchworks.com/blog/ai-agents/multi-agent-systems/) - Understanding Agents and Multi Agent Systems: Boost AI with specialized agents working together for ...

10. [The essential guide to building a minimum viable architecture](https://www.multiplayer.app/blog/future-proof-your-mvp-the-essential-guide-to-minimum-viable-architecture/) - Enter the concept of minimum viable architecture (MVA), which dictates the initial design decisions ...

11. [AI Agent Architecture Patterns: Single & Multi-Agent Systems - Redis](https://redis.io/blog/ai-agent-architecture-patterns/) - Single-agent patterns keep things simple with fewer LLM calls per task, but multi-agent systems can ...

12. [Has Your Architectural Decision Record Lost Its Purpose? - InfoQ](https://www.infoq.com/articles/architectural-decision-record-purpose/) - Architectural Decision Records (ADRs) are important vehicles for communicating the architectural dec...

13. [ADR process - AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) - An architectural decision record (ADR) is a document that describes a choice the team makes about a ...

14. [MODEL-REFERENCE.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/a8f96545-8701-4263-8be2-24e02a56f12f/MODEL-REFERENCE.md?AWSAccessKeyId=ASIA2F3EMEYE65CNXQ6V&Signature=9hokW0VZzXhwO8p2%2BPKO3nMFXtk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEM3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCKfLWOndWlnCq8ohEvsQNz3WUz9%2BTBrXZHysHM8h1rrAIhANYv32VDtgi%2BLHU6iMGua4Sjlar57L2SzJpq709zWfY%2BKvwECJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1IgwTN3yhC73oarzf9Z4q0ATmYQoKR6merEMl1BStFZMQLwsqUQ7S9PmyIkI5Tqhtrp6Ftl%2BpeWOapEAC8TUmmdxoUmBzUYzkzYOoUOWC5MpAQDuASRh980QGSsv9a7gX%2BLEIfOKZqdTbjsf3FcrOBPqvgKKLy9x9I5yNC4%2F%2BEKpSrYyzeO2EtJiqD%2FUnTuxJLx8gpiPQUpNMkZ0uChBcy4tN5j%2BVib%2FkCadfJyFkvSS1Gx8b%2BihNevIUpSxBAOYCq4rzlXe1TdZthW4TgOaiVlM5tZY37nDmKa5wbwLLrL%2FS1wo4ODiR5cqPeA78M056j7fT28HXyzj2l7eCAHf0NpDst5rolb2%2B3UHj3fj2txf43DXHy6jK%2BauCBNw9u11Jqq66e%2F%2FaRqIeUPVXBdoGl7TR0%2FE8UaWntOC9u%2Fe7kGU%2FQHGSBGpw956lC%2BLhGYcjh1AqcYeg1DeRiYarJNK9lALJ2YysH4mLbSBYBeWDHVnyu4Lm%2FshDwtUMvmHXsoKi3qss0Y5dYDE3ZjZbl5JHKsg3ijLBGD4gVPlo6tFBps0SB2JoH8ukuJrrLyTGatJKMfA9QQKYV3XFZ32cQEX24SMG8WTo8dbVO23cv3jrDf3CLBIF7xDRtq6oCOnTdKmrVYWdVGmQ5jyR6qLo0cFGS2Mg6rIkmT0UWQXgE8hZgbJh8DrG8uv70HDMiGmHn91abw%2BgpDQZVgscr0DwIq8Pvw4qcgHMMizykGkZRAvbepYnvEY0SVi8wdJKqLxRJwiuPOa8uLfA4RfVg2s%2FSeyMG1qMh0iwLC7nnFNZ0ThaLVwuMPmC688GOpcBH%2FX4VJJ%2Fccf54rVk2A1QcI4Z6X9pGKHt6g2Qt42%2BcUHK4AUv9h5syTUhjki2iElbG1i3kgR4fFMnNgzL2Ug1w4Eeg%2FGNZyVdA5k1Act3ZbScyyrL56vZg%2F58mOoGHYINJbPC7cfKIhezvhlsxXCCvBwpWKa6MZcCUvCiiQo6ng0TLxDeM5EBQCCYCndg5nwIqIfqijkJHA%3D%3D&Expires=1778044748) - Version 1.1 Date 2026-05-05 Status CANONICAL This document is the single authoritative reference for...

15. [e9f6c64a-7d94-44d3-8f77-fc9e58bc9ad6.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_3afb3469-1ef5-402e-97a3-f551f4b0fb0b/2b2466db-1895-42ed-93af-124e966e1413/e9f6c64a-7d94-44d3-8f77-fc9e58bc9ad6.md?AWSAccessKeyId=ASIA2F3EMEYE65CNXQ6V&Signature=FW6UTrdL8JgQ%2FmlNpi9xhCO1M5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEM3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCKfLWOndWlnCq8ohEvsQNz3WUz9%2BTBrXZHysHM8h1rrAIhANYv32VDtgi%2BLHU6iMGua4Sjlar57L2SzJpq709zWfY%2BKvwECJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1IgwTN3yhC73oarzf9Z4q0ATmYQoKR6merEMl1BStFZMQLwsqUQ7S9PmyIkI5Tqhtrp6Ftl%2BpeWOapEAC8TUmmdxoUmBzUYzkzYOoUOWC5MpAQDuASRh980QGSsv9a7gX%2BLEIfOKZqdTbjsf3FcrOBPqvgKKLy9x9I5yNC4%2F%2BEKpSrYyzeO2EtJiqD%2FUnTuxJLx8gpiPQUpNMkZ0uChBcy4tN5j%2BVib%2FkCadfJyFkvSS1Gx8b%2BihNevIUpSxBAOYCq4rzlXe1TdZthW4TgOaiVlM5tZY37nDmKa5wbwLLrL%2FS1wo4ODiR5cqPeA78M056j7fT28HXyzj2l7eCAHf0NpDst5rolb2%2B3UHj3fj2txf43DXHy6jK%2BauCBNw9u11Jqq66e%2F%2FaRqIeUPVXBdoGl7TR0%2FE8UaWntOC9u%2Fe7kGU%2FQHGSBGpw956lC%2BLhGYcjh1AqcYeg1DeRiYarJNK9lALJ2YysH4mLbSBYBeWDHVnyu4Lm%2FshDwtUMvmHXsoKi3qss0Y5dYDE3ZjZbl5JHKsg3ijLBGD4gVPlo6tFBps0SB2JoH8ukuJrrLyTGatJKMfA9QQKYV3XFZ32cQEX24SMG8WTo8dbVO23cv3jrDf3CLBIF7xDRtq6oCOnTdKmrVYWdVGmQ5jyR6qLo0cFGS2Mg6rIkmT0UWQXgE8hZgbJh8DrG8uv70HDMiGmHn91abw%2BgpDQZVgscr0DwIq8Pvw4qcgHMMizykGkZRAvbepYnvEY0SVi8wdJKqLxRJwiuPOa8uLfA4RfVg2s%2FSeyMG1qMh0iwLC7nnFNZ0ThaLVwuMPmC688GOpcBH%2FX4VJJ%2Fccf54rVk2A1QcI4Z6X9pGKHt6g2Qt42%2BcUHK4AUv9h5syTUhjki2iElbG1i3kgR4fFMnNgzL2Ug1w4Eeg%2FGNZyVdA5k1Act3ZbScyyrL56vZg%2F58mOoGHYINJbPC7cfKIhezvhlsxXCCvBwpWKa6MZcCUvCiiQo6ng0TLxDeM5EBQCCYCndg5nwIqIfqijkJHA%3D%3D&Expires=1778044748) - - Models workflows as explicit state machines with typed state - Conditional branching, checkpointin...

16. [[PDF] The Bootstrapping Problem - Jonathan Weisberg](https://jonathanweisberg.org/pdf/Phil%20Compass.pdf) - Abstract. Bootstrapping is a suspicious form of reasoning that verifies a source's reliability by ch...

17. [[PDF] Reliabilism, Bootstrapping, and Epistemic Circularity - PhilArchive](https://philarchive.org/archive/BRIRBA-2) - The problem with bootstrapping can be located in a specific form of epistemic circularity: The justi...

18. [4 Emergent Properties | The Material Mind](https://ucp.manifoldapp.org/read/the-material-mind/section/2118adbe-ee3f-4d38-ada1-b2768519fc68) - The aim of this chapter is to justify the causal efficacy of mental properties by presenting the hyp...

19. [Emergent Properties - Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/archives/win2021/entries/properties-emergent/) - Accounts of strong emergence specify it as (merely) nomological necessity (conditional on the holdin...

20. [Big Modeling Up Front (BMUF) Anti-Pattern](https://agilemodeling.com/essays/bmuf.htm) - Big modeling up front (BMUF) is the desire to create comprehensive models of the requirements, archi...

21. [Agile Needs More Architecture 'Stuff'](https://www.architectureandgovernance.com/agile/agile-needs-more-architecture-stuff/) - In this article I discuss how a lack of “architecture stuff” in mainstream agile contributed to the ...

22. [Big Design Up Front (BDUF): A Software Development Antipattern](https://deviq.com/antipatterns/big-design-up-front/) - BDUF is a software development antipattern that involves creating a comprehensive and detailed desig...

23. [Minimum Viable Architecture (MVA) - Caroli.org](https://caroli.org/en/minimum-viable-architecture-mva/) - A minimum viable architecture (MVA) is required. This implies being able to develop new features qui...

24. [With Spec-Driven Development we've come full circle to Big Design ...](https://www.multiplayer.app/blog/with-spec-driven-development-weve-come-full-circle-to-big-design-up-front/) - Without some upfront design, you end up with: Teams working from different mental models of the same...

25. [Definition of the Shape Up Method - Airfocus](https://airfocus.com/glossary/what-is-the-shape-up-method/) - The Shape Up Method is a process for developing products across six-week cycles, with “cooldown” per...

26. [MASAI: Modular Architecture for Software-engineering AI Agents](https://arxiv.org/html/2406.11638v1) - Our method, MASAI, achieves the highest resolution rate of 28.33% on the dataset, thereby establishi...

