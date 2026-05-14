---
artifact_type: SESSION_LEARNINGS
session: "W8+W29: Epistemic enforcement tests + roadmap hygiene"
created_at: 2026-05-14
session_type: "S1-S9"
source_artifacts:
  - tests/architecture/test_epistemic_enforcement.py
  - state/tasks/task-008-w29-level0-enforcement.md
  - state/tasks/task-009-w8-level1-enforcement.md
  - docs/ROADMAP-003.md
  - state/session-log.md
  - 25+ state/ files (artifact_type backfill)
purpose: "Implement D-015 enforcement levels 0+1 as fitness tests; assess roadmap quality"
---

# Session Learnings: W8+W29 Epistemic Enforcement + Roadmap Hygiene

## What Was Done

- Implemented 4 enforcement tests in `test_epistemic_enforcement.py`: 2 Level 0 (field existence) + 2 Level 1 (grade minimum + capture inheritance)
- Backfilled `artifact_type` on 25+ state/ files that predated the §13.1 vocabulary (W6)
- Fixed capture-intake-001 grade inheritance (INFORMED_ESTIMATE → EVIDENCE_BASED per W32 §3.3)
- Discovered and fixed 6 ROADMAP-003 inconsistencies: stale Section 7, work-grid vs dep-graph mismatches, F3/W29 overlap, wrong F5/F6/F7 dependencies
- Updated session-log dashboard and blocked items

## Decisions Made

### D-SESS-01: F3 subsumed by W29

**Decision:** Marked F3 ("Level 0 artifact verification script") as ✅ DONE (via W29) since `test_epistemic_enforcement.py` implements exactly what F3 described.
**Context:** F3 and W29 were independently defined work items with overlapping scope. Neither referenced the other.
**Why it matters:** Duplicate work items in the roadmap hide true progress and can lead to double-implementing the same capability. The roadmap needs a deduplication pass whenever new items are added.

---

## Process Insights

### Insight 1: ROADMAP-003 has two sources of truth that drift apart

**Observation:** The work grid (Section 2) and the dependency graph (Section 4) independently track status and dependencies. In this session: F1/F2 were ✅ DONE in the work grid but PLANNED/READY in the dep graph. F5/F6/F7 had different dependency lists in each section. This was not caught by any automated check.
**Type:** workflow-process
**Implication:** Either (a) enforce a rule that work grid and dep graph are always updated atomically, or (b) make one section the canonical source and derive the other. The dep graph YAML is more precise (has evidence links) — consider making it canonical and rendering the work grid from it.

### Insight 2: Section 7 (Current Work Item) goes stale on every completion

**Observation:** After completing W8+W29, Section 7 still pointed to W8 as the next work item. The session-log dashboard had the same issue — W8/W29 listed as "READY" in blocked items when they were done. This is the third session in a row where Section 7 was stale at the start.
**Type:** workflow-process
**Implication:** S9 curator checklist should explicitly include "update ROADMAP Section 7 next_work_item" and "update session-log dashboard". Consider: the `nowu-curator` agent should have this as a mandatory step, not optional.

### Insight 3: Vocabulary formalization should precede artifact creation

**Observation:** W4/W5 created 22+ artifacts. W6 formalized the §13.1 `artifact_type` vocabulary. W8/W29 enforcement tests then needed a backfill of `artifact_type` on all those artifacts. If §13.1 had existed before W4, the backfill wouldn't have been needed.
**Type:** workflow-process
**Implication:** When introducing a new metadata standard (like artifact_type vocabulary), formalize the vocabulary BEFORE creating artifacts that should carry it. This is a sequencing lesson for future metadata extensions.

### Insight 4: Roadmap is clear on WHAT but weak on WHERE and HOW

**Observation:** Each work item has a clear description, stage, UC mapping, and dependencies. But the roadmap doesn't specify: (a) which files/artifacts the work item will produce, (b) which existing files it needs to read, (c) what "done" looks like in concrete terms. Section 7 has `input_artifacts` for the current work item, but only for one item at a time. This means an agent picking up any non-current work item has to rediscover context from scratch.
**Type:** workflow-process
**Implication:** Consider adding an `input_artifacts` and `output_artifacts` field to each work item in the dep graph YAML. This would make the roadmap self-documenting for agent consumption. Alternatively, this is what task specs (S5 output) provide — but task specs only exist after S5, not at planning time.

### Insight 5: Delegated artifact_type backfill needed two rounds

**Observation:** The `quick` category agent was given a comprehensive prompt with 14+ files to update but only completed 4 before stopping. Required a session continuation (`session_id`) to finish the remaining 20+. The agent treated "add artifact_type to all files" as "add to a few files and report."
**Type:** agent-behavior
**Implication:** For bulk mechanical edits, either (a) use `unspecified-high` category instead of `quick`, or (b) include explicit count verification in the prompt ("there are N files; confirm you've done all N"), or (c) split into parallel `quick` tasks of 3-5 files each. The `quick` category model (GPT-4o) optimizes for speed and tends to satisfice rather than complete exhaustively.

### Insight 6: The enforcement test architecture is clean and extensible

**Observation:** The 4-test structure (Level0: field_exists + artifact_type_exists; Level1: grade_minimum + capture_inherits) maps cleanly onto D-015's 3-level enforcement model. Adding Level 2 (blocking) in W11 will be a natural extension — same file, new test class. The `MINIMUM_GRADE_BY_TYPE` dict makes threshold updates trivial.
**Type:** domain-insight
**Implication:** This pattern (single test file per enforcement concern, one class per level, threshold dicts for calibration data) should be the template for future fitness function work (W12).

---

## Anti-Patterns Observed

### Anti-Pattern 1: Maintaining two status representations of the same data

**Temptation:** Having both a human-readable work grid table (Section 2) and a machine-readable dep graph YAML (Section 4) seems like it serves both audiences well.
**Reality:** They drift apart within one session. The work grid gets updated because it's visually prominent; the dep graph gets forgotten because it's deep in the file. Every session that completes a work item must now remember to update both. This is a maintenance multiplier, not a convenience.

### Anti-Pattern 2: Marking an item DONE in the roadmap without verifying downstream unblocks

**Temptation:** When W8 was completed, only W8's own status was updated. The downstream item W11 (which depends on W8) should have been updated from PLANNED to READY, but this was missed initially.
**Reality:** Stale dependency statuses hide available work. An agent consulting the roadmap for "what can I work on next?" would skip W11 because it still says PLANNED. Always cascade status updates to immediate dependents.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| Epistemic enforcement tests | `tests/architecture/test_epistemic_enforcement.py` | ACTIVE | 4 tests enforcing D-015 Level 0 + Level 1 |
| W29 task spec | `state/tasks/task-008-w29-level0-enforcement.md` | DONE | Level 0 enforcement task |
| W8 task spec | `state/tasks/task-009-w8-level1-enforcement.md` | DONE | Level 1 enforcement task |
| ROADMAP-003 (updated) | `docs/ROADMAP-003.md` | ACTIVE | Section 7 + dep graph fixes |
| Session log (updated) | `state/session-log.md` | ACTIVE | Dashboard + W8+W29 entry |
| 25+ state/ files | `state/` (various) | ACTIVE | artifact_type backfill |

## What Should Happen Next

1. **Roadmap structural fix**: Consider making the dependency graph YAML the single source of truth and generating the work grid table from it (or at minimum, add a fitness test that verifies Section 2 statuses match Section 4 statuses).
2. **S9 curator checklist update**: Add explicit steps for "update ROADMAP Section 7" and "cascade status to downstream dependents" and "update session-log dashboard blocked items."
3. **Deduplication pass**: Scan remaining roadmap items for overlaps similar to F3/W29. Candidates to check: F4 vs K4 (both mention session persistence), A1 vs baseline (is A1 even a discrete work item?).
4. **W11 scoping**: Level 2 blocking enforcement is now READY. Decide whether to tackle it in v1 (pulling it forward from v1.1) or defer as planned — the v1→v1.1 gate doesn't require it.
5. **Consider `input_artifacts` / `output_artifacts`**: Add to dep graph YAML entries to make the roadmap self-navigable for agents without requiring S5 task specs.
