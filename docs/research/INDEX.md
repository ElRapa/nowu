---
artifact_type: RESEARCH_INDEX
created_at: 2026-05-05
purpose: "Master catalog of research sessions, traceability to decisions"
---

# nowu Research Index

**Purpose:** Catalog of research sessions — what research exists, when it was done, and what decisions it informed.

---

## Research Sessions

| Date | Session | Key Question | Informed Decisions | Processed |
|---|---|---|---|---|
| 2026-05-10 | `2026-06-10_3_perplexity_roadmap-session-log-proposal` | How should ROADMAP-001, stale state files, and session-log be aligned? | ROADMAP-001 v2 update; session-log creation; stale file marking | Yes |
| 2026-05-10 | `2026-06-10_2_perplexity_refactor-5x10-workflow-proposal` | How should the 5×10 model be refactored to map all agents into the grid? | W6 (5×10 refactoring) added to ROADMAP-001 | No |
| 2026-05-10 | `2026-05-10_1_perplexity_workflow_triage_update` | How should ROADMAP items be triaged so work-scheduler can prioritize READY items? | ROADMAP triage; work-scheduler integration | No |
| 2026-05-09 | `2026-05-09_1_perplexity_Research-to-Ship Skillset` | What is the structured research artifact schema & how should OmO evaluate/convert research into decisions or implementation? | Research artifact schema; /evaluate-research skill | No |
| 2026-05-08 | `2026-05-08_3_perplexity_Document Maintenance Strategy` | Where should research outputs live? Who maintains docs? | (this INDEX + template changes) | No |
| 2026-05-08 | `2026-05-08_2_perplexity_Context Loading Strategy` | How should bootstrap context loading work? | Bootstrap architecture (BOOTSTRAP-*.md files) | No |
| 2026-05-08 | `2026-05-08_1_perplexity_orchestrator implementation` | How should the orchestrator layer work? | (pending — D-022, orchestrator agents) | Yes |
| 2026-05-06 | `2026-05-06_5_practical-implementation-grid-adr-contracts_perplexity.md` | Practical implementation grid for ADRs and contracts | ROADMAP-001 structure | Yes |
| 2026-05-06 | `2026-05-06_4_7-critical-questions-nowu-workflow-model_perplexity.md` | 7 critical questions about workflow model | D-013..D-015 (model refinements) | Yes |
| 2026-05-06 | `2026-05-06_3_strategic-analysis-for-you_perplexity.md` | Strategic analysis of nowu approach | Vision validation | Yes |
| 2026-05-06 | `2026-05-06_3_directive-to-sisyphus_perplexity.md` | Directive for AI agent calibration | Agent prompt patterns | Yes |
| 2026-05-06 | `2026-05-06_2_critical-decisions-analysis_perplexity.md` | Critical decisions analysis | D-001..D-012 validation | Yes |
| 2026-05-06 | `2026-05-06_1_sisyphus-5x10-critical-analysis_by-perplexity.md` | Is nowu's 5x10 model architecturally sound? | D-002, D-003, model structure | Yes |
| 2026-05-06 | `2026-05-06_5x10-session-insights.md` | 5x10 session insights synthesis | Model refinements | Yes |
| 2026-05-05 | `2026-05-05-workflow_traversal_analysis-perplexity.md` | Workflow traversal patterns | S1-S9 pipeline design | Yes |

---

## How to Add New Research

1. Create session output in `docs/research/sessions/` using convention: `YYYY-MM-DD_N_source_topic/` (folder) or `YYYY-MM-DD_topic_source.md` (single file)
2. Update this INDEX.md with a new row
3. If research informs a decision, cite the session path in the D-NNN or ADR entry's `Intake` field

---

## Notes

- Sessions are time-bound (answered a question at a specific moment)
- Naming convention: `YYYY-MM-DD_N_source_topic` encodes date, sequence number, source tool, and topic
- When comparative or literature content accumulates, create `comparative/` and `literature/` subdirs per research doc recommendations
