# work-scheduler Triage Behavior Update

## Goal

Teach `work-scheduler` how to use triage metadata when choosing the next work item, while preserving its core responsibilities:

- Honor dependencies and stage gates.
- Never modify files (read-only).
- Provide clear, structured YAML output for the human or orchestrator.

---

## New Behavior Overview

When multiple work items are READY, `work-scheduler` will:

1. Filter to READY items (dependencies satisfied, stage gate passed if applicable).
2. Among READY items, prefer those with `priority_bucket: HIGH`.
3. Break ties using `wsjf_score` (higher first).
4. If no HIGH items exist, consider the item with highest `learning_score` as a candidate "confidence-clearing" spike.

This makes triage explicit while keeping decision logic simple and inspectable.

---

## Input Expectations

`work-scheduler` now expects that `docs/ROADMAP-NNN.md` includes, for each work item:

- A clear identifier (e.g., W4, K1, A3, F2).
- Dependency information (as today).
- A `triage:` block with at least:
  - `priority_bucket`
  - `wsjf_score`
  - `learning_score` (optional but recommended)

If triage metadata is missing for an item, `work-scheduler` should:

- Treat that item as `priority_bucket: MEDIUM` with `wsjf_score: 0` by default.
- Flag in its output that triage metadata is missing, and recommend running the triage update.

---

## Updated Decision Algorithm

Pseudo-logic for `work-scheduler`:

1. **Load roadmap:**
   - Read latest `docs/ROADMAP-NNN.md`.
   - Parse stages, work items, dependencies, and triage blocks.

2. **Determine candidate set:**
   - Identify current stage and "Current Work Item" section.
   - Gather all work items that:
     - Belong to the current stage, and
     - Are not marked COMPLETE/DONE, and
     - Have all dependencies satisfied (verified via `docs/` and `state/`).

3. **Apply triage:**
   - Partition candidates by `priority_bucket` (HIGH > MEDIUM > LOW).
   - Within the highest non-empty bucket:
     - Sort by `wsjf_score` descending.
     - If multiple items have similar `wsjf_score`, prefer the one with higher `learning_score`.

4. **Select next item:**
   - Choose the top item from the sorted list.

5. **Special case: no HIGH items ready:**
   - If only MEDIUM/LOW items exist and `learning_score` is available:
     - Consider recommending the highest-`learning_score` item explicitly as a "confidence-clearing" or "exploration" task.

6. **Output YAML:**

```yaml
status: READY
next_work_item: W4
priority_bucket: HIGH
wsjf_score: 3.0
learning_score: 1.67
description: First S1-S9 intake end-to-end
agent_to_invoke: nowu-intake
input_artifacts:
  - docs/USE_CASES.md (select 1 UC for intake)
  - docs/architecture/ARCHITECTURE-VISION.md
  - docs/architecture/adr/ADR-0007.md
  - docs/architecture/adr/ADR-0008.md
  - docs/architecture/adr/ADR-0009.md
  - docs/architecture/adr/ADR-0010.md
notes: |
  Triaged as HIGH priority due to high impact, high learning value, and
  position on the v1-core critical path.
```

If no candidates are READY:

```yaml
status: BLOCKED
next_work_item: W4
blocked_by:
  - K1: Missing triage metadata for key artifacts
  - F3: Verification script not integrated
recommended_action: |
  Implement or update the blocking items, then re-run work-scheduler.
```

---

## Non-Goals

- `work-scheduler` does **not** modify `ROADMAP-NNN.md` or triage values.
- It does **not** re-estimate `reach`, `impact`, etc.; that remains a human+agent responsibility.
- It does **not** attempt to micro-schedule S1–S9 phases inside a chosen work item; that remains the job of the execution skills.

---

## Implementation Notes for OmO

- Parsing can be approximate at first (regex/section-based) and refined later.
- For safety, log which roadmap version and which triage values were used for each recommendation.
- When triage metadata appears inconsistent (e.g., job_size == 0, confidence > 1.0), flag it in the `notes` field and suggest manual correction.
