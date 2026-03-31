---
step: health.uc
artifact_id: health-uc-2026-03-31
artifact_path: state/health/health-use-cases-2026-03-31.md
run_date: 2026-03-31
agent: health-use-cases
outcome: GREEN
---

# Health Check Analysis — Use Case Catalog (2026-03-31)

## What Was Straightforward

**Catalog structure parsing** — USE_CASES.md follows a clear template with consistent frontmatter and section formatting. No ambiguity in structure, formatting, or metadata.

**Vision alignment mapping** — Vision document (2026-03-31, APPROVED) has explicit product principles and horizons. Mapping each UC to a principle (e.g., "Continuity," "Compound Progress," "Enforcement") was direct and unambiguous.

**Stage alignment verification** — V1_PLAN.md explicitly lists use case dependencies for each of the 7 steps. Plan-to-catalog mapping was a simple lookup.

**Artifact inventory** — No active work beyond intake-001 and Step 02 architecture files. Empty directories have clear reasons (pre-workflow not triggered for AP/RE yet).

---

## Friction Points

**1. Project portfolio boundary clarity**

*Tension:* The USE_CASES.md catalog mixes two roles:
- **In-scope for v1 rollout:** NF-01 through NF-09 (framework self-development)
- **Out-of-scope but documented:** AP, RE (business projects that are test beds, not commitments); PK, XP (cross-cutting concerns that serve all projects)

The distinction is mentioned in the preamble ("Project Key" section) but is not formalized in UC status fields. Each UC could be tagged with `stage_target: v1 | v1.1 | later` to reduce ambiguity for future readers.

*Recommendation:* Add a frontmatter field to each UC group:
```
stage_target: v1
product_commitment: required
```
This makes intake decisions faster later (is this AP UC in scope for P0.UC or should it be cut?).

---

**2. AP project scope assumptions**

*Tension:* AP-01 through AP-07 are thorough and detailed — they assume a mature, multi-phase product engagement:
- Regulatory tracking (AP-01)
- Formulation versioning (AP-02)
- Supply chain modeling (AP-03)
- Market intelligence (AP-04)
- Milestone dependency tracking (AP-05)
- Decision recording (AP-06)
- Onboarding (AP-07)

If AP is a test project to validate nowu's UX/workflow, should these UCs represent a full-bore product build or a slim v1 integration test? Current UCs suggest "full product." But v1 appetite may only allow for AP-01 (regulatory tracking) as a focused test of the "live knowledge" pattern.

*Recommendation:* When P0.UC runs for AP, be explicit about appetite vs. UC completeness. Either:
- Accept all 7 UCs and plan multi-step AP development (AP.step-N), OR
- Create `AP-LEAN` subset with 3 critical UCs for Stage 1 validation.

---

**3. PK feature distribution**

*Tension:* PK-01 through PK-06 are scattered across Steps 05-07 in the plan, but there's no single intake that says "Personal Knowledge Management Phase" or "Fast Capture Experience." Features (PK-01 fast capture, PK-02 proactive surface, PK-03 today-view) are woven across multiple step deliverables.

This is not wrong — it's a valid pattern (features decomposed into infrastructure prerequisites). But someone reading V1_PLAN will not immediately see "oh, there's a PK phase" — they see "Step 05 touches PK-03, Step 06 touches PK-04."

*Recommendation:* Add a "PK integration checkpoint" in V1_PLAN after Step 05, listing which PK UCs are available and which are still pending. Makes the plan more readable for future team members.

---

**4. XP (cross-project) feature maturity tiers**

*Tension:* XP-01 (discovery), XP-03 (lesson transfer), XP-04 (conflict resolution) are infrastructure-heavy. XP-02 (terminology) and XP-05 (scale) are even heavier. But the plan doesn't distinguish between:
- Essential for Stage 1 (XP-01 discovery: needed so AP/RE projects can find framework knowledge)
- Nice-to-have for Stage 1 (XP-03 lesson transfer: happens if you're lucky, not required)
- Post-MVP (XP-05 scale: not a blocker until 10K+ atoms)

*Recommendation:* Annotate each XP UC with `maturity_tier: essential | nice-to-have | future` in the catalog.

---

## Check Quality

**Completeness: HIGH**

- All required inputs present: vision.md (APPROVED), V1_PLAN.md (ACTIVE), USE_CASES.md (current)
- Optional inputs: No PROGRESS.md, but not critical (no stale signals to check against)
- No missing artifact types (no orphaned problems, stories, epics — as expected at this stage)

**Clarity of inputs: HIGH**

- Vision is explicit and well-articulated
- V1_PLAN has clear UC dependencies
- USE_CASES.md has consistent structure

**Depth of checks: HIGH**

- Performed catalog-existence, vision-alignment, stage-alignment, usage-coverage, and orphan-work checks as specified
- Spotted no RED signals
- Identified 1 GREEN/YELLOW transition point (project scope for AP at future P0.UC)

---

## Improvement Signals

### 1. For UC Catalog Structure

Add optional frontmatter fields to UC blocks to improve intake/prioritization decisions later:

```yaml
---
id: AP-01
stage_target: v1 | v1.1 | future
product_commitment: required | nice-to-have | research
priority_in_stage_target: high | medium | low
---
```

This removes ambiguity when pre-workflow (P0.UC) runs for AP/RE projects and needs to decide scope.

### 2. For Plan-to-UC Linking

In V1_PLAN.md, after each step's mini-plan, add a "verification gate":

```markdown
### Step 02 — Verify
[ ] All use cases NF-01, NF-02, PK-03, XP-01 exist in catalog — ✓ 2026-03-31
[ ] No new UCs were discovered that should have been in this step — ✓ (checked at S9)
```

This makes it easy to spot creep or gaps if the plan gets out of sync with the catalog.

### 3. For Health Check Frequency

Current cadence: health-use-cases runs once (this pass). Recommend:
- **Trigger:** After any P0.UC intake or major plan update (V1_PLAN v1.2+)
- **Frequency:** Monthly minimum (every 4 weeks of calendar time or 7 completed S1-S9 cycles, whichever is sooner)
- **Report location:** state/health/health-use-cases-YYYY-MM-DD.md (current pattern good)

### 4. For UC Template

Consider adding one more optional field:

```yaml
affected_modules: [core, know]  # if NF UC
traceability_required: true      # if implementation-bound (False for UX/discovery UCs)
```

This helps S6 implementers know whether they need to export validation_trace to core/contracts/ or just document in a test.

---

## Tags

- `step:health.uc`
- `status:GREEN`
- `friction:project-scope, pk-feature-dist, xp-maturity-tiers`
- `input_quality:HIGH`
- `check_depth:FULL`
- `recommendation_count:3`
- `blocking_issues:0`
- `advice:add_stage_target_field, add_plan_verification_gate, establish_health_cadence`
