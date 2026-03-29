---
id: health-use-cases-2026-03-28
check_type: use_cases
status: YELLOW
generated_at: 2026-03-28T00:00:00Z
agent_version: health-use-cases@2.2
---

# Use Case Health — 2026-03-28

overall_status: YELLOW

## Checks

### 1. Catalog Existence

status: GREEN
finding: `docs/USE_CASES.md` exists. Contains 35 use cases across 5 categories: NF (9), AP (7), RE (7), PK (5), XP (7). Last updated 2026-03-22.

---

### 2. Vision Alignment

status: YELLOW
finding: NF use cases (NF-01 through NF-09) trace directly to vision problem, solution, and success horizons. AP/RE/PK/XP use cases have thin or indirect vision anchoring.
details:
- NF-01 through NF-09 map to the core vision problem ("solo developers lose continuity, accumulate architectural drift…") and success horizons ("v1 core operational", "3+ projects dogfooded"). Clear alignment. ✅
- PK-03 (Today view) is referenced in V1\_PLAN Step 02 and maps to the "resume work within minutes" success criterion. ✅
- XP-01 (cross-project discovery) maps to "cross-project recall" in V1\_PLAN Step 02. ✅
- AP (all 7 UCs), RE (all 7 UCs), PK-01, PK-02, PK-04, PK-05, XP-02 through XP-07 are covered by the 12-month horizon ("used for at least 3 distinct project domains") but not explicitly named or anchored. Per D-010 these are directional. The vision's 6-month outcome ("Aperitif or RE bootstrapped and active") provides lightweight anchoring for AP and RE but does not connect to specific UC IDs.
- Risk: if use-case-agent is run in future without vision update, AP/RE/PK/XP UCs may appear orphaned.

---

### 3. Stage Alignment (V1_PLAN)

status: GREEN
finding: V1 current stage = Stage 1, Step 02 in progress. Stage-relevant UCs are active.
details:
- Step 02 intake (`intake-001.md`) references NF-01, NF-02, NF-09, PK-03, XP-01. All exist in catalog with clear definitions. ✅
- Steps 03–07 UCs (NF-03, NF-04, NF-05, NF-06, NF-07) are in catalog and mapped to future V1 steps. Correctly "not yet active" at current step. ✅
- AP, RE, PK (beyond PK-03), XP (beyond XP-01) are documented for Stage 2+ dogfooding. Correctly deferred. ✅
- V1\_PLAN routing table exists and maps each step to use cases — stage alignment is intentional and clear.

---

### 4. Usage Coverage

status: YELLOW
finding: Active coverage exists for 5 of 35 UCs. 30 UCs have no current work item — this is by design for the current step but large.
details:
- UCs with active intake coverage: NF-01, NF-02, NF-09, PK-03, XP-01 (all through `intake-001.md`). ✅
- UCs with no work items but planned in V1\_PLAN (Steps 03–07): NF-03, NF-04, NF-05, NF-06, NF-07. Expected. ✅
- UCs with no work items and no V1\_PLAN step assignment: AP (all 7), RE (all 7), PK-01, PK-02, PK-04, PK-05, XP-02 through XP-07, NF-08. These are directional. ✅ by design.
- Note: NF-08 (health metrics / framework health) has no V1 step assigned but the health check system partially addresses it. Could be linked explicitly.

---

### 5. Orphan Work Items

status: GREEN
finding: No orphaned work items. All intakes reference existing UC IDs.
details:
- `intake-001.md` use\_case\_ids: [NF-01, NF-02, NF-09, PK-03, XP-01] — all present in `docs/USE_CASES.md`. ✅
- `state/stories/` is empty. No stories to check. ✅
- `state/epics/` is empty. No epics to check. ✅

---

## Summary

- `USE_CASES.md` is internally coherent and well-structured. NF + a handful of PK/XP UCs are well-anchored.
- 30 of 35 UCs are currently inactive — deliberate deferred scope, not drift.
- AP and RE UCs have thin vision anchoring; this is intentional per D-010 ("treat full set as direction") but will become a problem when AP/RE projects become active.
- NF-08 (health metrics) is present in the catalog but not assigned to any V1 step — the health check system partially satisfies it but without formal traceability.
- No orphaned work items. All UC references in active intake are valid.

## Recommended Actions

1. No immediate blocking action required for current work (Step 02).
2. When AP or RE work begins, run `use-case-agent` (`/health-check use-cases`) to formally anchor AP/RE UCs to updated vision success horizons. File: `docs/USE_CASES.md` and `docs/vision.md`.
3. Consider adding NF-08 to a V1 step or explicitly marking it as Stage 2. File: `docs/V1_PLAN.md`, section: `## 3. Steps`.
