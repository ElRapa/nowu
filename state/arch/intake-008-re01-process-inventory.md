---
artifact_type: RE_PROCESS_INVENTORY
id: intake-008-re01-process-inventory
intake_id: intake-008
decision_id: D-028
created_at: 2026-05-15
status: DRAFT
altitude: EXECUTION
phase: IMPLEMENTATION
epistemic_grade: HYPOTHESIS
---

# RE-01 Evidence Artifact — Process Inventory Before Digitalization

## Process Inventory (mini set)

| process_id | Process | Actors | Inputs | Outputs | Handoffs | Bottleneck | Digitalization Value |
|---|---|---|---|---|---|---|---|
| RE-P01 | Property Listing Initiation | Owner, Analyst | Property docs, photos, comparable rent notes | Listing draft | Analyst -> Approver | Missing standardized checklist causes omissions | HIGH |
| RE-P02 | Tenant Onboarding | Analyst, Tenant, Reviewer | Application packet, ID docs, lease template | Signed lease package | Analyst -> Reviewer -> Tenant | Manual back-and-forth causes delay and data loss | HIGH |
| RE-P03 | Maintenance Escalation | Tenant, Coordinator, Contractor | Issue report, prior maintenance notes | Work order + closure note | Tenant -> Coordinator -> Contractor | Prior repair context not consistently retrievable | MEDIUM |

## Cross-Process Handoffs

1. `RE-P01 -> RE-P02`: listing data quality directly affects tenant onboarding completeness.
2. `RE-P02 -> RE-P03`: signed lease terms and tenant contact records must be reused for maintenance context.

## Evidence of Representability

- Process steps, actors, handoffs, and bottlenecks are representable with current artifact structures.
- Value scoring can be represented as explicit metadata fields in markdown artifacts.

## Representational Limits

- No first-class graph traversal for process dependency/handoff queries (**maps to GAP-002**).
- No generic machine-query layer through nowu contracts for process nodes (**maps to GAP-001**).
- Process node types are convention-based, not formally typed extension entities (**maps to GAP-005**).

## Follow-on References

- K3 (contract/query surface)
- W19 (domain extension model)
