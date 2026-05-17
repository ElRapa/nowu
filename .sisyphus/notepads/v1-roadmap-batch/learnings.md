# v1-roadmap-batch Learnings

<!-- Append discoveries here. Never overwrite. Format: ## [TIMESTAMP] Task: {id} -->

## [2026-05-15T18:30:00Z] Task: W28-workflow

- Comparative domain validation is materially stronger when each gap row includes explicit AP evidence and RE evidence side-by-side before labeling.
- D-SESS-01 guardrails were effective in practice: S1 problem-only framing reduced rework; explicit S2 blindspot checks prevented overclaiming.
- W28 indicates 6/7 gaps are systemic (001/002/003/004/005/007), so K3/W19/W20/K9a should be treated as cross-domain priorities, not AP-only cleanup.

## [2026-05-15T19:20:00Z] Task: W20

- NF-09 traceability quality improves sharply when `trace_links` is mandatory rather than narrative; K2 observations map directly to explicit schema keys (`review_id`, `vbr_ids`, task closure links).
- W5 artifact_type proposal is mature enough to serve as ADR baseline vocabulary; reusing it avoids parallel naming drift.
- GAP-003 should be handled as a metadata contract problem (decision_context + domain_atom_refs) across AP and RE, not as one-off domain template edits.
- GAP-007 must be called out in traceability ADR text but resolution belongs to K12/ADR-0010 maintenance; explicit deferral language prevents scope bleed.

## [2026-05-15T19:10:00Z] Task: W19-domain-extension

- Keeping domain extension out of `core/contracts/` while using bridge mapping + know registry satisfies ADR-0001 boundaries and still addresses GAP-005.
- GAP-003 can be handled as typed decision-evidence link manifests, which preserves current DecisionRecord compatibility while enabling AP-06 and RE-06 richness.
- KI-facing ADRs are much more actionable when they include concrete type/method signatures plus behavioral requirements (unknown type rejection, required-field validation, chain query support).
