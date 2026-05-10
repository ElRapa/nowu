# ROADMAP Triage Update Guide

## Goal

Augment `docs/ROADMAP-001.md` (and future `ROADMAP-NNN.md`) with triage metadata so the orchestrator can prioritize READY work items by value, risk reduction, urgency, effort, and learning potential.

---

## Step 1: Add Triage Blocks to v1-core Items

For each v1-core work item (W1–W5, K1–K2, A1–A2, F1–F3), add a `triage:` block.

Example for **W4 — First S1–S9 intake (end-to-end)**:

```markdown
| W4 | First S1-S9 intake (end-to-end) | Complete state/intake/ → state/tasks/ → implementation → capture cycle | W3.5 | ⬜ NEXT |

triage:
  reach: 3              # Affects nowu repo only, but critical for all future work
  impact: 5             # Enables real-world validation of the 5×10 workflow
  time_criticality: 4   # Needed before entering v1 stage work
  risk_reduction: 4     # Validates synthesis, ADRs, and contracts in practice
  job_size: 3           # 1–3 S1–S9 traversals
  confidence: 0.7       # Based on existing ADRs, some uncertainty remains
  learning_value: 5     # High: first full cycle will reveal many issues
```

Repeat this for W1–W3.5, W5, K1–K2, A1–A2, F1–F3 using rough but honest estimates.

---

## Step 2: Compute Scores (Manual or via Agent)

For each work item, compute:

- `wsjf_score = ((impact + time_criticality + risk_reduction) / job_size) * confidence`
- `learning_score = learning_value / job_size`

You can do this manually at first (inline comment or calculator), then later automate it with a small script or agent.

Example (continuing W4):

- Numerator: impact + time_criticality + risk_reduction = 5 + 4 + 4 = 13
- 13 / job_size (3) ≈ 4.33
- 4.33 * confidence (0.7) ≈ 3.03 → `wsjf_score: 3.0`
- `learning_score = 5 / 3 ≈ 1.67`

Add these to the triage block when computed:

```yaml
triage:
  ...
  wsjf_score: 3.0
  learning_score: 1.67
  priority_bucket: HIGH
```

---

## Step 3: Assign Priority Buckets

Once you have scores for v1-core items:

1. Look at all READY or NEXT items (currently W4 and K1 are likely candidates).
2. Rank them by `wsjf_score`.
3. Assign `priority_bucket`:
   - HIGH: top ~20% wsjf_score among v1-core items and/or items on the critical path.
   - MEDIUM: middle band.
   - LOW: items intentionally deferred.

For early use, you can simply:

- Mark W4 as `HIGH` (critical path, high impact and learning).
- Mark K1 as `MEDIUM` (important but not blocking W4).

Refine these as scores stabilize.

---

## Step 4: Extend the ROADMAP Template

Update your roadmap template (for v1, v1.1, v2) so that any new work item includes a triage block when it is first created.

At minimum, require:

- `reach`, `impact`, `time_criticality`, `risk_reduction`, `job_size`, `confidence`.
- `learning_value` for items that are exploratory, architectural, or experimental.

Derived fields can be added later by tools.

---

## Step 5: Keep Triage Updated via roadmap-updater

Whenever `roadmap-updater` creates `ROADMAP-NNN+1.md`:

- It should **copy over existing triage blocks** for unchanged items.
- It should **add new triage blocks** for any new items it introduces (using defaults if needed and marking `confidence` low).
- Optionally, it can recompute `wsjf_score` and `priority_bucket` if triage values changed.

This keeps triage metadata version-aligned with the roadmap itself.
