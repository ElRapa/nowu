# Triage Update Package

This package extends the nowu orchestrator layer with a concrete triage system for roadmap work items.

## Files

- `triage-metadata-spec.md` — Defines triage fields, scales, scoring formulas, and patterns for high-impact/low-confidence work.
- `roadmap-triage-update.md` — Step-by-step guide to adding triage metadata to `docs/ROADMAP-001.md` and future roadmap versions.
- `work-scheduler-triage-update.md` — How `work-scheduler` should use triage metadata when choosing the next work item.

## How to Use

1. **Read `triage-metadata-spec.md`** to understand the fields and scoring.
2. **Apply `roadmap-triage-update.md`** to add `triage:` blocks to existing v1-core items in `docs/ROADMAP-001.md`.
3. **Update `work-scheduler`** per `work-scheduler-triage-update.md` so it uses `priority_bucket` and `wsjf_score` when multiple work items are READY.

Once integrated, the orchestrator will:
- Continue to enforce dependencies and stage gates.
- Prefer high-value, high-risk-reduction, right-sized items.
- Surface small, high-learning tasks when confidence is low.
