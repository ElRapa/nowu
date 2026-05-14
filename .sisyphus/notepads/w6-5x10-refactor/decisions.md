# W6 5×10 Refactor — Decisions

## [2026-05-14] Architectural Choices
- T4 output (`.sisyphus/evidence/task-4-agent-classification.md`) is MANDATORY input for T7, T8, T9, T10
- AGENTS.md agent grid is the canonical source of truth for agent-to-5×10 mapping
- Multi-phase agents get PRIMARY phase (e.g., nowu-implementer = IMPLEMENTATION not VERIFICATION)
- New §13 subsection for vocabulary is §13.1 (NOT a new top-level section)
- S7=VBR/VERIFICATION, S8=nowu-reviewer/EVALUATION — this is the corrected canonical mapping

## [2026-05-14] Task 4 Classification Decisions
- For this evidence task, `work-scheduler` is normalized to valid enum values as STRATEGIC/EVALUATION with an explicit note that MODEL §8 treats it as meta-layer external (N/A in canonical table).
- `architecture-vision-agent` retained primary phase ANALYSIS (as currently declared), with note that model contract spans SYNTHESIS→DECISION.

## [2026-05-14] Verification Decision Log
- Classified AC-5 and AC-8 as FAIL (not BLOCKER) because task scope is report-only and no blocking execution constraint was violated.
- Preserved strict non-remediation posture: findings documented with evidence; no fixes applied.
