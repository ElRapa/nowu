# Idea: Standardised Software Development via Fixed Steps with Variable Depth

> Status: INCORPORATED into docs/WORKFLOW.md (Execution Modes A-D)
> Origin: Conversation 2026-03-09 to 2026-03-15

## The Core Insight
Software development CAN be standardised, but not by prescribing the same
depth at every step. Instead: fixed step sequence, variable step depth.

## The Depth Matrix
Every project type runs the same 9 steps, but "thickness" varies:

| Step | Framework (nowu) | App (aperitif) | Script | Bug Fix |
|------|-----------------|----------------|--------|---------|
| S1-S4: Architecture | Thick | Medium | 1 sentence | Skip |
| S5: Shaping | Thick | Medium | 1 task | Thin |
| S6-S7: Implement+VBR | Thick (TDD) | Medium | Medium | Medium |
| S8-S9: Review+Capture | Thick | Medium | Self-review | Thin |

## Why This Works
The Guo et al. 2025 survey (150+ papers) found a convergent pattern across
all agentic approaches: requirements → design → implementation → verification
→ capture. The sequence is universal. The depth is context-dependent.

## Implications for Claude Code
"Skip" doesn't mean "omit the step entirely" — it means invoke the agent
with minimal context and accept a thin artifact. For a bug fix, the Intake
Brief is one sentence. The Constraints Sheet is "affects only X function".
The Task Spec has one AC. The full chain still exists for traceability.

## The "Step-and-Stop" Pattern (Mode E — not in v5 yet)
Sometimes you need just one step. "Use nowu-options to sketch 3 approaches
for this DB schema" — no intake, no shaping, just the options artifact.
This is valid for exploration and doesn't need a full cycle to justify it.
Add Mode E to WORKFLOW.md when needed.
