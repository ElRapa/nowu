# Implementation Guide: /evaluate-research Skill

This guide shows OmO how to implement the `/evaluate-research` skill in the nowu framework.

---

## What You're Building

A skill that takes research artifacts from Perplexity (or manually written) and produces:
1. **2-3 evaluated alternatives** with pros/cons and scoring
2. **A recommendation** with rationale
3. **An implementation plan** with concrete file changes and verification steps

---

## File Structure

```
nowu/
├── .claude/
│   └── skills/
│       └── evaluate-research.md          ← Skill definition (create this)
└── state/
    └── decisions/                         ← Decision docs output here
        └── YYYY-MM-DD-topic-decision.md
```

---

## Step-by-Step Implementation

### Step 1: Create the Skill File

**Location:** `.claude/skills/evaluate-research.md`

**Content:** Copy from `evaluate-research-skill.md` (provided in this package).

**Frontmatter:**
```yaml
---
skill: evaluate-research
version: 1.0
altitude: META
purpose: Evaluate research artifacts and generate implementation alternatives
input: Research artifact (YAML or prose)
output: Decision document with alternatives, scores, recommendation, implementation plan
---
```

### Step 2: Test with Example Artifact

1. Copy `research-artifact-example.md` content
2. Invoke the skill: `/evaluate-research [paste artifact]`
3. Verify output:
   - Decision doc created in `state/decisions/`
   - 3 alternatives with scores
   - Recommendation with rationale
   - Implementation plan with verification steps

### Step 3: Integrate with Perplexity Handoff

**Workflow:**
1. Perplexity generates research report with structured YAML section
2. User copies YAML section to OmO
3. OmO invokes `/evaluate-research` with pasted YAML
4. Skill generates decision doc
5. OmO presents alternatives to user
6. User approves chosen alternative
7. OmO invokes `/implement-choice` (separate skill, to be built)

---

## Schema Reference

The structured input format is defined in `research-artifact-schema.yaml`.

**Required fields:**
- `problem_statement.diagnosis`
- `problem_statement.context`
- `evaluation_criteria` (at least 1 criterion)

**Optional fields:**
- `alternatives` (skill generates if missing)
- `recommendation` (skill generates)
- `implementation` (skill generates)

**If user provides prose instead of YAML:**
- Skill extracts structure using LLM
- Presents extracted structure to user for validation
- Proceeds only after user confirms accuracy

---

## Evaluation Rubric

For each criterion, score each alternative:
- **Excellent (4):** Fully satisfies criterion, no trade-offs
- **Good (3):** Satisfies criterion with minor trade-offs
- **Acceptable (2):** Partially satisfies, notable trade-offs
- **Poor (1):** Does not satisfy criterion

**Final score calculation:**
```
Score = Σ(criterion_weight × criterion_score) / Σ(criterion_weight)

Where weights:
- high = 3
- medium = 2  
- low = 1
```

**Example:**
```
Alternative A:
- Token efficiency (high, weight=3): excellent (4) → 3×4 = 12
- Maintainability (high, weight=3): good (3) → 3×3 = 9
- AI orientation (medium, weight=2): poor (1) → 2×1 = 2
- Implementation cost (medium, weight=2): excellent (4) → 2×4 = 8

Total: (12 + 9 + 2 + 8) / (3+3+2+2) = 31/10 = 3.1/4.0 = 7.75/10
```

---

## Decision Document Lifecycle

1. **Created** by `/evaluate-research` → saved to `state/decisions/YYYY-MM-DD-topic-decision.md`
2. **Reviewed** by user → user picks alternative A, B, or C
3. **Implemented** by `/implement-choice` → changes executed
4. **Learned** by `/session-learning` → rationale saved to learning log
5. **Shipped** by `/ship` → committed to repo
6. **Archived** after implementation → decision doc remains in `state/decisions/` as historical record

**Decision docs are immutable after creation.** If implementation reveals new info, create a new decision doc (e.g., `YYYY-MM-DD-topic-decision-v2.md`) rather than editing the original.

---

## Common Edge Cases

### Case 1: Input has only 1 alternative
**Action:** Generate 2 more alternatives as contrasts. Present all 3 for evaluation.

### Case 2: No clear winner (tie score)
**Action:** Present both tied alternatives with: "Decision depends on [trade-off X]. If X matters more, choose A. If Y matters more, choose B."

### Case 3: User provides vague problem statement
**Action:** Prompt for clarification: "To generate alternatives, I need: (1) current state, (2) desired state, (3) constraints. Can you provide these?"

### Case 4: Chosen alternative has high risk
**Action:** Add risk mitigation steps to implementation plan. Flag to user: "Note: this option is high-risk. Recommend [mitigation X] before proceeding."

### Case 5: Implementation plan dependencies are circular
**Action:** Flag as blocker: "Cannot implement — circular dependency detected: [A depends on B, B depends on A]. Resolve by [suggestion]."

---

## Next Steps After Implementation

Once `/evaluate-research` is working:

1. **Build `/implement-choice`** — takes decision doc, executes chosen alternative
2. **Validate the pattern** — run 2-3 full cycles (evaluate → approve → implement)
3. **Build `/research-to-ship` pipeline** — chains evaluate → approve → implement → learn → ship

**Don't build the pipeline until you've validated the atomic skills work well.**

---

## Questions?

If anything is unclear during implementation:
1. Check the example artifact (`research-artifact-example.md`)
2. Check the schema (`research-artifact-schema.yaml`)
3. Ask Perplexity to clarify the skill definition

The skill is designed to be modular — it doesn't depend on other skills, so it can be tested standalone.
