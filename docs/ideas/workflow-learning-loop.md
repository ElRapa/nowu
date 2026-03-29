# Idea: Workflow Learning Loop

> Status: CONCEPT — ready for pre-workflow (STANDARD mode) when implementation is prioritised
> Origin: Conversation 2026-03-29 — synthesised from independent analysis + Perplexity + Guo et al. 2025

---

## The Core Insight

Every workflow step run already produces the raw material for learning:
structured artifacts, outcome signals, friction patterns. The problem is purely
a missing pipeline: these signals are written but never systematically mined or
fed forward. The fix is not architectural — it is additive. A lightweight
"learning layer" sits alongside the existing P0–P4 / S1–S9 flow without
modifying any artifact that workflow steps read.

**Key design constraint:** learning artifacts must NOT appear in any agent's
`## Inputs` section. Workflow steps must remain oblivious to the learning layer.
This prevents learning-layer noise from polluting the implementation pipeline.

---

## System Architecture

Three tiers, each building on the previous:

```
Tier 1 — Signal Capture (per step run)
  Every agent: upon completing its primary artifact, also writes a
  step-run analysis file to state/analysis/

Tier 2 — Pattern Mining (periodic, on demand)
  learning-sweep skill: reads recent analysis files + captures + VBRs +
  health reports → writes learning-sweep-YYYY-MM-DD.md + appends to
  docs/LEARNING.md "Raw Summaries"

Tier 3 — Reinjection (human-gated, periodic)
  prompt-refiner agent: reads docs/LEARNING.md (Stable + Heuristics +
  Anti-Patterns) → proposes targeted diffs to .claude/rules/ and agent defs
  → writes state/meta/prompt-proposals-YYYY-MM-DD.md → HUMAN APPROVES
  → applies
```

The human gate before Tier 3 is non-negotiable. Blind automated prompt
rewriting drifts and overfits (Guo et al. 2025). The value is in the
proposal + human judgement, not in automatic application.

---

## Tier 1: Step-Run Analysis Files

### Why per-step, not per-cycle

Perplexity's proposal extends `capture-record.md` with learning snippets.
That's useful but too late — S9 is the only data point and it retrospectively
reconstructs friction from memory. Capturing analysis at key steps gives:
- Signal where friction actually originated (S4 decision? S5 shaping?)
- Earlier visibility into process quality
- Richer data for the learning-sweep to detect per-step patterns

### Scope in Phase 0

In Phase 0, only the following steps emit analysis files:

- **S4** (decision) — option/decision friction
- **S5** (shaping) — task decomposition problems
- **S8** (review) — code/arch/AC coverage failures
- **S9** (capture) — overall outcome and cycle quality
- **health-sweep** — health check friction and false-positive risk
- **GAP chain** (G0/G1/G2) — when run

Other steps (S1, S2, S3, S6, pre-workflow P1/P2) MAY add analysis
later once Phase 0 proves the schema captures useful signal. Starting
norrow reduces overhead and makes patterns easier to detect with fewer files.

### File schema

```
state/analysis/{step}-{artifact-id}-analysis.md
```

Examples:
- `state/analysis/S1-intake-001-analysis.md`
- `state/analysis/S5-task-001-analysis.md`
- `state/analysis/health-sweep-2026-03-28-analysis.md`
- `state/analysis/P3-constraint-check-002-analysis.md`

Schema:

```markdown
---
analysis_id: {step}-{artifact-id}-analysis
step: S4 | S5 | S8 | S9 | health | gap   # Phase 0 scope
artifact_id: {the primary artifact produced this run}
artifact_path: state/.../{filename}
run_date: YYYY-MM-DD
agent: {agent name}
outcome: COMPLETED | BLOCKED | CHANGES_REQUESTED | SKIPPED
# COMPLETED: step finished; primary artifact reached expected status
# BLOCKED: halted due to missing input, constraint, or human gate
# CHANGES_REQUESTED: output produced but review/human requested changes
# SKIPPED: step intentionally not run for this cycle/mode
---

# Step-Run Analysis: {step} — {artifact-id}

## What Went Well
- [What was straightforward, clear, well-designed in this step]

## Friction Points
- [What slowed down or was unclear — be specific: which input file,
  which constraint, which ambiguity]

## Step Quality Assessment
- Input quality: HIGH | MEDIUM | LOW — [1 sentence why]
- Output quality: HIGH | MEDIUM | LOW — [1 sentence why]
- Confidence: HIGH | MEDIUM | LOW — [was the agent sure of its output?]

## Failure Classification
(Fill only if outcome is not COMPLETED)
failure_type (provisional — will be refined after first sweep): one of
  test-first-violation | scope-creep | import-boundary |
  type-error | missing-ac | api-mismatch | coverage-gap |
  stale-input | ambiguous-constraint | vision-misalignment |
  appetite-exceeded | process-mismatch | other
# process-mismatch: workflow itself was too heavy / wrong shape for this case

failure_detail: [1-2 sentences describing the specific failure]

## Improvement Signals
- [1-3 concrete suggestions for the framework: agent definition, rule,
  template, or checklist changes that would have prevented friction]
  e.g. "S2 agent should explicitly check for know API version in constraints"
  e.g. "intake template missing field for prior arch artifacts"

## Tags
tags: [step:S2, module:core, outcome:completed, friction:stale-input, ...]
```

### Agent change required (minimal)

Agents in Phase 0 scope gain a single new output section:

```markdown
## Secondary Output (Analysis)

After writing your primary artifact, write a step-run analysis to:
`state/analysis/{step}-{artifact-id}-analysis.md`

The same agent that writes the primary artifact is responsible for
writing the analysis file immediately afterwards, in the same
invocation. No second agent or context reload is needed.

Use the schema from docs/ideas/workflow-learning-loop.md.
This file is NEVER read by any subsequent workflow step.
It is input only for the learning-sweep skill.
```

Only S4, S5, S8, S9, health agents, and GAP agents implement this in Phase 0.
No primary artifact format changes. No workflow logic changes.

---

## Tier 2: Learning Sweep

New skill: `learning-sweep` (analogous to `health-sweep`)

Runs: on demand, recommended after every 3–5 completed S9 captures.

Inputs:
- `state/analysis/` — all step-run analysis files since last sweep
- `state/capture/` — last 10 capture records
- `state/vbr/` — last 10 VBR reports
- `state/health/` — last health sweep
- `docs/LEARNING.md` — existing knowledge base (context only)

Output:
1. `state/learning/learning-sweep-YYYY-MM-DD.md` — structured pattern report
2. Appends a "Raw Summary" block to `docs/LEARNING.md`

Pattern detection clusters:
- Gate friction (which steps bounce most often, by failure_type)
- Input quality patterns (which upstream artifacts were consistently LOW quality)
- Appetite accuracy (estimated vs actual, tracked via VBR loop counts)
  Note: when S6 is added in Phase 3, its analysis includes `vbr_loops: N` —
  the number of VBR cycles before PASS. This is the primary appetite signal.
- Vision/goal drift signals (health YELLOW/RED patterns over time)
- Cross-level signals (micro-failures at S7–S9 that trace to vision or UC gaps)
- Rule/prompt effectiveness:
  - Which workflow or architecture rules are most often referenced in `failure_detail`?
  - Which steps repeatedly ignore an existing rule? (indicates wording or placement problem)
  This directly feeds Tier 3 — rules are the solution strategy, failures are the benchmark.

For each detected pattern (≥2 occurrences):
- Propose one heuristic or anti-pattern candidate for LEARNING.md
- Propose one checklist addition to the relevant step
- Do NOT auto-apply anything — proposals only

---

## Tier 3: Prompt Refiner

New agent: `prompt-refiner` (monthly cadence or on demand after learning-sweep)

Inputs:
- `docs/LEARNING.md` — Stable Principles + Heuristics + Anti-Patterns sections
- `.claude/rules/workflow.md` — current rules
- `state/learning/` — latest learning sweep

Output:
- `state/meta/prompt-proposals-YYYY-MM-DD.md` — structured diff proposals

Proposal format (per proposal):
```markdown
## Proposal {N}: {one-line description}
target_file: .claude/agents/nowu-shaper.md
target_section: ## Checks
change_type: ADD_CHECKLIST_ITEM | MODIFY_RULE | ADD_CONSTRAINT | REMOVE_ITEM
rationale: [which LEARNING.md entry supports this, with link]
proposed_diff:
  + [text to add]
  - [text to remove]
risk: LOW | MEDIUM | HIGH
```

Human reviews, approves or rejects each proposal individually. Approved
proposals are applied by an agent (gap-writer pattern) by the human's direction.

**Proposal limit per run:** prompt-refiner MUST propose at most:
- 3 prompt/rule changes total per run
- No more than 1 change per agent/rules file

Prioritise in this order:
1. Changes addressing high-frequency `failure_type` clusters
2. Changes to early steps (S4, S5) over late steps (S8, S9)
3. Rule wording fixes over new rule additions

**Hard constraint**: prompt-refiner never touches S6/S7 implementer scope
or test definitions. Rule and checklist changes only. Never rewrites agent
reasoning or decision logic wholesale.

---

## docs/LEARNING.md Structure

The long-term accumulation KB. Sections:

```markdown
# nowu Product Learning Log

## Meta
product: nowu | created_at: | last_updated:

## Stable Principles
[Items promoted from Heuristics after ≥3 independent confirmations.
Once here, they are candidates for .claude/rules/ or agent defs.]

## Heuristics
[Soft rules — observed patterns that usually hold but aren't universal.
Proposed by learning-sweep, promoted by human.]

## Anti-Patterns
[Things that consistently caused problems. Concrete, specific.]

## Open Questions
[Things the system cannot answer well yet — gaps in current design.]

## Raw Summaries (auto-appended by learning-sweep)
### YYYY-MM-DD
- N cycles analysed: [list]
- [5-7 bullet summary of patterns]
- [Link to state/learning/learning-sweep-YYYY-MM-DD.md]
```

---

## What This Is NOT

- Not a RAG system over all workflow artifacts — too expensive per step
- Not automatic prompt rewriting — human gate is mandatory before Tier 3 applies
- Not a replacement for the human's editorial judgment — learning-sweep proposes,
  human promotes, prompt-refiner refines, human applies
- Not in-context lesson injection at S5/S6 — that is a separate, complementary
  mechanism (retrieve past captures by UC tags) and is a later optimization

---

## Relationship to Existing Patterns

| Existing mechanism | Learning layer role |
|---|---|
| `know` atoms (lessons, decisions) | Complementary. know stores long-term semantic memory; LEARNING.md stores workflow-specific process knowledge with different retrieval pattern (step-level, not topic-level) |
| GAP chain (G0→G1→G2) | Model for Tier 3 structure. Prompt-refiner follows the same propose→human-gate→apply pattern as gap-writer |
| health-sweep | Model for Tier 2 structure. learning-sweep is structurally identical but reads analysis files instead of docs |
| S9 capture record | Still produced; learning-sweep uses it as one of its inputs. Capture record focus = what was delivered. Analysis file focus = how the process went |
| NF-06 (learn from past mistakes) | This is the implementation plan for NF-06 |

---

## Alignment with Research (Guo et al. 2025 + Reflexion)

- **Reflexion (Shinn 2023)**: verbal self-reflection stored episodically, prepended
  to next attempt. This implements the storage half. Retrieval injection is deferred.
- **Self-refinement at prompt level**: Guo et al. confirm human-gated promotion
  outperforms blind auto-rewriting. Tier 3 gate is structurally aligned.
- **Task-type specific memory**: Guo recommends against undifferentiated blobs.
  `tags` field and per-step `failure_type` ensure memories are queryable by step,
  module, outcome, and failure category — not just by date.
- **Cross-level feedback**: Guo emphasises feedback should cross levels (micro S7
  failure → macro vision gap). The learning-sweep's cross-level signal cluster
  and the link from prompt-proposals back to health rules operationalise this.

---

## Implementation Phasing

### Phase 0 — NOW (Tier 1 only, narrow scope)
Scope: Add `## Secondary Output (Analysis)` section to **S4, S5, S8, S9** agent
definitions and the **4 health agents**. Create `state/analysis/` directory.
Include in git — analysis files are useful history. No new skills or agents
needed yet. Cost: ~20 lines across 8 agent files.

**This is the only thing that needs to happen now.** Every subsequent S4/S5/S8/S9
or health-sweep run starts generating data. The system cannot learn without data.
Do NOT add analysis to S1/S2/S3/S6 or pre-workflow agents yet — start lean.

### Phase 1 — After first 3 S9 cycles
Scope: Create `docs/LEARNING.md` skeleton. Write `learning-sweep` skill. Run
first sweep manually. Evaluate whether the analysis files produced in Phase 0
are actually useful (validate the schema is capturing the right signals).

If Phase 0 schema proves useful: expand to **P1 and P2 first** (before any
other steps). Problem framing quality (P1) and story AC quality (P2) are where
most downstream S8 failures originate — but that causal link is invisible in
S8/S9 data alone. P1/P2 data closes that gap.
Note: P1/P2 may need minor schema adaptation — their failure modes
(ambiguous problem space, thin ACs) differ structurally from S4/S5/S8/S9.

### Phase 2 — After first learning-sweep
Scope: Create `prompt-refiner` agent. Run first prompt-refiner pass. Apply first
set of approved proposals. Evaluate ROI.

### Phase 3 — Stabilise
Scope: Evaluate whether remaining steps (S1/S2/S3/S6) should be added based
on whether Phase 0–2 analysis revealed blind spots in those steps. P1/P2
will already have been added in Phase 1 if schema proved valuable.
Wire learning-sweep and prompt-refiner triggers into CLAUDE.md as commands.

---

## Open Questions (for pre-workflow)

1. Should analysis files be part of the commit (git-tracked) or ephemeral?
   Argument for: full history, gitblame shows learning evolution.
   Argument against: noise in git log, large volume over time.
   Tentative: include in git but in a separate branch or under `.gitignore`
   with an explicit `git add state/analysis/` when desired.

2. Should `failure_type` be an enum enforced structurally, or a freeform tag?
   **Resolved (Phase 0):** freeform with provisional list. Enumerate after
   first sweep reveals actual failure categories in practice.

3. Who writes the analysis file — the same agent that writes the primary
   artifact, or a separate post-processor?
   **Resolved (Phase 0):** same agent, same invocation. Simpler, no doubled
   context load. Revisit if agents show degraded primary output quality.

4. Does the learning layer eventually justify its own `know` atom type
   (`LESSON` or `PATTERN`)? Probably yes, after Phase 2, when patterns are
   stable enough to warrant semantic retrieval.
