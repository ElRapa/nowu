# /evaluate-research Skill Definition

**Purpose:** Evaluate a research artifact (from Perplexity or manual) and generate implementation alternatives with recommendation.

---

## Input Formats

### Format 1: Structured YAML (Preferred)
```yaml
research_artifact:
  version: "1.0"
  problem_statement: { ... }
  alternatives: [ ... ]
  # Full schema in research-artifact-schema.yaml
```

### Format 2: Prose Report (Fallback)
Plain markdown research report. Skill will extract:
- Problem statement
- Proposed solutions
- Evaluation criteria (inferred if not explicit)
- Pros/cons
- Recommendation

---

## Process

### Step 1: Parse Input
- If structured YAML → load directly
- If prose → extract problem, solutions, criteria using LLM
- Validate: does input have enough information to evaluate?

### Step 2: Generate Alternatives (if needed)
- If input has 0-1 alternatives → generate 2-3 alternatives
- If input has 2+ alternatives → proceed to evaluation
- Each alternative must have:
  - Name and summary
  - Concrete file changes
  - Pros/cons
  - Effort and risk estimate

### Step 3: Evaluate Against Criteria
- Extract or infer evaluation criteria from problem context
- Score each alternative against each criterion
- Calculate weighted score if criteria have weights

### Step 4: Generate Recommendation
- Rank alternatives by weighted score
- Select top alternative as recommendation
- Provide rationale (why this one beats the others)
- Note runner-up (for sensitivity: "if X changes, consider Y")

### Step 5: Create Implementation Plan
- Extract concrete changes from chosen alternative
- Order changes by dependency (prerequisites first)
- Add verification steps for each change
- Add validation tests for overall success

### Step 6: Output Decision Document
- Format: structured YAML + prose summary
- Save to: `state/decisions/YYYY-MM-DD-topic-decision.md`
- Present to user with:
  - Problem recap
  - 3 alternatives with scores
  - Recommendation with rationale
  - Implementation checklist

---

## Output Template

```markdown
# Decision: [Topic]

**Date:** YYYY-MM-DD  
**Source:** [Perplexity session ID or manual]  
**Status:** Awaiting approval

---

## Problem
[Brief diagnosis]

---

## Alternatives Evaluated

### Option A: [Name]
**Summary:** [1-2 sentences]  
**Changes:** [list of files]  
**Pros:** [list]  
**Cons:** [list]  
**Score:** [X/10]

### Option B: [Name]
[same structure]

### Option C: [Name]
[same structure]

---

## Recommendation: Option [X]

**Rationale:** [why this one]

**Runner-up:** [if constraint Y changes, consider alternative Z]

---

## Implementation Plan

**Prerequisites:**
- [ ] [item 1]
- [ ] [item 2]

**Steps:**
1. [Change file X] → Verify: [how]
2. [Change file Y] → Verify: [how]
3. [Test Z] → Expected: [what]

**Validation:**
- [ ] [End-to-end test 1]
- [ ] [End-to-end test 2]

---

## Next Steps

1. User reviews alternatives and approves chosen option
2. Invoke `/implement-choice state/decisions/YYYY-MM-DD-topic-decision.md [A|B|C]`
3. After implementation, invoke `/session-learning` to save insights
4. Invoke `/ship` to commit changes
```

---

## Usage

```
/evaluate-research [artifact_path or paste artifact]
```

**Examples:**

```bash
# From file
/evaluate-research docs/research/sessions/2026-05-09_bootstrap/report.md

# From pasted content
/evaluate-research
[user pastes YAML or prose report]
```

**Options:**
- `--criteria="criterion1, criterion2"` — Override evaluation criteria
- `--alternatives=N` — Generate N alternatives (default: 3)
- `--output=path` — Custom output path for decision doc

---

## Error Handling

**If input is incomplete:**
- Prompt user for missing pieces (problem statement, context, constraints)
- Or: generate missing pieces with explicit "INFERRED - verify" markers

**If alternatives are too similar:**
- Flag: "Options A and B are nearly identical. Merge or differentiate?"

**If no clear winner:**
- Present tie: "Options A and B score equally. Decision depends on [trade-off X]."

---

## Integration with Other Skills

This skill produces input for:
- `/implement-choice` — takes decision doc + chosen alternative
- `/session-learning` — can save the decision rationale
- `/ship` — commits the implemented changes

Can be chained via `/research-to-ship` pipeline (future).

---

## Implementation Notes for OmO

1. **Schema location:** `research-artifact-schema.yaml` defines the structured input format
2. **Example artifact:** `research-artifact-example.md` shows a complete filled example
3. **Fallback parsing:** If input is prose, use LLM to extract structure. Validate with user before proceeding.
4. **Scoring rubric:** For each criterion, use 4-point scale: excellent (4) > good (3) > acceptable (2) > poor (1). Weighted average = final score.
5. **File safety:** Decision docs go in `state/decisions/` (not `docs/`) because they're session-specific, not permanent docs.
