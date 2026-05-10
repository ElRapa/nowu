# Triage Metadata Specification for ROADMAP Work Items

## Purpose

Add a lightweight, research-backed triage layer on top of `ROADMAP-NNN.md` so the orchestrator (`work-scheduler`) can choose among READY work items based on value, urgency, risk reduction, effort, confidence, and learning value.

This spec is designed for W/K/A/F work items at the epic / multi-session level.

---

## Triage Fields

Attach a `triage:` block to each roadmap work item (W*, K*, A*, F*).

```yaml
triage:
  # Value & urgency
  reach: 1-5             # How many repos/teams/flows this benefits
  impact: 1-5            # Depth of benefit if successful (per-affected unit)
  time_criticality: 1-5  # Pain of delay; windows of opportunity
  risk_reduction: 1-5    # Structural/architectural risk reduced if done

  # Effort / cost
  job_size: 1-5          # Relative effort (sessions or S1–S9 cycles)

  # Uncertainty & learning
  confidence: 0.1-1.0    # Confidence in the above scores
  learning_value: 1-5    # How much this teaches us about the design space

  # Derived (computed by agent or script)
  wsjf_score: float      # ((impact + time_criticality + risk_reduction) / job_size) * confidence
  learning_score: float  # (learning_value / job_size)
  priority_bucket: HIGH | MEDIUM | LOW
```

### Scales

- `reach`: 1 = affects a single repo/user, 5 = affects most or all target repos/projects.
- `impact`: 1 = small quality-of-life improvement, 5 = step-change in capability.
- `time_criticality`: 1 = can safely slip, 5 = must be done soon or we lose options.
- `risk_reduction`: 1 = nice-to-have, 5 = removes major architectural or safety risk.
- `job_size`: 1 ≈ half-day / single S1–S9 traversal; 3 ≈ 1–3 days; 5 ≈ multi-week epic.
- `confidence`: 0.1 = pure speculation, 0.5 = rough guess, 0.8 = good evidence, 1.0 = high certainty.
- `learning_value`: 1 = little new information, 5 = significantly de-risks future design.

---

## Scoring Rules

### Main Priority Score (wsjf_score)

For each item:

\( wsjf\_score = ((impact + time\_criticality + risk\_reduction) / job\_size) * confidence \)

Interpretation:
- The numerator is a simple Cost-of-Delay proxy.
- Dividing by `job_size` biases toward smaller jobs with high value.
- Multiplying by `confidence` ensures speculative estimates do not dominate solely on claimed impact.

### Learning Score (learning_score)

\( learning\_score = learning\_value / job\_size \)

Use this to surface small, high-learning spikes and experiments, especially when big initiatives have very low confidence.

### Priority Buckets

Derive `priority_bucket` from `wsjf_score` (and optionally `learning_score`) using simple thresholds, for example:

- HIGH: top ~20% of `wsjf_score` among READY items, or items on the critical path with `wsjf_score` above a configurable threshold.
- MEDIUM: middle band.
- LOW: bottom band or explicitly deferred items.

The exact thresholds can be tuned; the key is to give `work-scheduler` a discrete `priority_bucket` to break ties once dependencies are satisfied.

---

## High-Impact, Low-Confidence Items

When an item has high `impact` but low `confidence`, do **not** execute it directly. Instead:

1. Keep the original high-impact item with low `confidence` (so its `wsjf_score` is moderated).
2. Create a separate, smaller work item whose explicit goal is to **raise confidence**:

```yaml
# Example: W_big — "Cross-repo auto-architecting"
triage:
  reach: 5
  impact: 5
  time_criticality: 3
  risk_reduction: 4
  job_size: 5
  confidence: 0.3
  learning_value: 4

# W_validate_big — "Validate feasibility of cross-repo auto-architecting"
triage:
  reach: 3
  impact: 4
  time_criticality: 4
  risk_reduction: 5
  job_size: 2
  confidence: 0.7
  learning_value: 5
```

3. Route `W_validate_big` through an ARCHITECTURE / STRATEGIC "confidence-clearing" pipeline:
   - SENSE: gather existing UCs, constraints, prior ADRs.
   - FRAME: identify key uncertainties and success criteria.
   - ACT/VERIFY: run a bounded experiment or spike.
   - LEARN: write a short SYNTHESIS or ADR updating `confidence` and possibly `impact` on the original item.

This pattern keeps the roadmap honest: big bets are visible but do not starve higher-confidence, high-leverage work.

---

## Where to Store Triage Metadata

- For now, store `triage:` blocks **inline in the ROADMAP** under each work item row.
- In future, you can extract triage fields into a separate `state/roadmap/triage-NNN.yaml` if you want tooling to manipulate triage without editing the roadmap prose.

---

## Responsibilities

- **Human + agents together** set `reach`, `impact`, `time_criticality`, `risk_reduction`, `job_size`, `confidence`, and `learning_value` when creating or updating a work item.
- An **automation script or agent** computes `wsjf_score`, `learning_score`, and `priority_bucket` whenever the roadmap is updated.
- `work-scheduler` uses these derived fields when choosing among READY items.
