# Package 3: Runtime Verification & Circuit Breaker

**Purpose:** Build the automated verification layer that catches model violations at artifact creation time, plus the circuit breaker that halts workflows when invariants are broken.

**Prerequisite:** Package 1 (metadata) and Package 2 (agents) must be complete and verified.

---

## What to Build

### Component 1: Artifact Validator (extend verify-artifact.py)

The Level 0 validator already exists at `verification/verify-artifact.py`. Extend it to support all 4 verification levels:

| Level | What It Checks | When It Runs |
|---|---|---|
| Level 0 | YAML syntax, required fields present, enum values valid | Every artifact save |
| Level 1 | Epistemic grade ≥ minimum for altitude, phase permitted at altitude | Every artifact save |
| Level 2 | Cross-artifact consistency (lineage valid, no orphans, no cycles) | Before DECISION gates |
| Level 3 | Decision-gate readiness (aspirational grade met, all inputs present) | At human gates only |

#### Level 1 Implementation

```python
ALTITUDE_PHASE_MATRIX = {
    "STRATEGIC": ["IDEA", "PROBLEM", "ANALYSIS", "OPTIONS", "DECISION",
                   "EVALUATION", "VERIFICATION", "LEARN"],
    "PRODUCT": ["IDEA", "PROBLEM", "ANALYSIS", "OPTIONS", "DECISION",
                 "EVALUATION", "VERIFICATION", "LEARN"],
    "ARCHITECTURE": ["IDEA", "PROBLEM", "ANALYSIS", "SYNTHESIS", "OPTIONS",
                      "DECISION", "EVALUATION", "IMPLEMENTATION", "VERIFICATION", "LEARN"],
    "DELIVERY": ["IDEA", "PROBLEM", "ANALYSIS", "OPTIONS", "DECISION",
                  "EVALUATION", "IMPLEMENTATION", "VERIFICATION", "LEARN"],
    "EXECUTION": ["IDEA", "PROBLEM", "ANALYSIS", "OPTIONS", "DECISION",
                   "EVALUATION", "IMPLEMENTATION", "VERIFICATION", "LEARN"],
}

EPISTEMIC_MINIMUMS = {
    "STRATEGIC": "HYPOTHESIS",
    "ARCHITECTURE": "HYPOTHESIS",
    "PRODUCT": "SPECULATION",
    "DELIVERY": "SPECULATION",
    "EXECUTION": "SPECULATION",
}

EPISTEMIC_ORDER = ["SPECULATION", "HYPOTHESIS", "INFORMED_ESTIMATE",
                    "EVIDENCE_BASED", "VERIFIED_FACT"]
```

Check: `phase in ALTITUDE_PHASE_MATRIX[altitude]` and `grade_index >= minimum_index`.

#### Level 2 Implementation

- Parse `promoted_from` / `promotes_to` fields
- Verify referenced artifacts exist
- Detect cycles in promotion chain (A→B→A)
- Warn on orphans (artifacts with no upstream reference and not at STRATEGIC)

#### Level 3 Implementation

- At DECISION gates, check aspirational thresholds:

```python
ASPIRATIONAL_THRESHOLDS = {
    "STRATEGIC": "EVIDENCE_BASED",
    "ARCHITECTURE": "EVIDENCE_BASED",
    "PRODUCT": "INFORMED_ESTIMATE",
    "DELIVERY": "HYPOTHESIS",
    "EXECUTION": "HYPOTHESIS",
}
```

- Verify all required input artifacts are present and at correct grade
- Check human gate artifacts have `approved_by` field

### Component 2: Circuit Breaker

A workflow-level guard that halts execution when critical invariants are violated.

#### Triggers (HALT workflow)

1. **Altitude violation**: Artifact created at wrong altitude for its phase (e.g., SYNTHESIS at DELIVERY)
2. **Grade violation at gate**: Epistemic grade below aspirational at a DECISION phase
3. **Missing human approval**: Proceeding past a DECISION gate without `approved_by`
4. **Lineage break**: `promoted_from` references non-existent artifact

#### Triggers (WARN, don't halt)

1. Grade below advisory but above minimum
2. Orphan artifact (no upstream reference)
3. Stale artifact (last_edited_at > 30 days, status still ACTIVE)

#### Circuit Breaker Interface

```python
from typing import Protocol
from enum import Enum

class Severity(Enum):
    HALT = "halt"
    WARN = "warn"
    INFO = "info"

class Violation:
    severity: Severity
    rule: str       # e.g., "altitude_phase_matrix"
    message: str    # human-readable explanation
    artifact_id: str
    suggested_fix: str

class CircuitBreaker(Protocol):
    def check(self, artifact_path: str) -> list[Violation]:
        """Run all checks on a single artifact."""
        ...

    def check_gate(self, phase: str, altitude: str,
                   artifact_paths: list[str]) -> list[Violation]:
        """Run gate-level checks before DECISION."""
        ...

    def should_halt(self, violations: list[Violation]) -> bool:
        """Return True if any violation has HALT severity."""
        ...
```

### Component 3: Integration Hook

Wire the circuit breaker into the workflow:

1. **Pre-save hook**: Run Level 0 + Level 1 on every artifact write
2. **Pre-gate hook**: Run Level 2 + Level 3 before DECISION phases
3. **Report format**: Structured output matching `Violation` schema above

---

## Implementation Order

1. Extend `verify-artifact.py` with Level 1 checks (altitude-phase matrix + epistemic minimums)
2. Add Level 2 checks (cross-artifact consistency)
3. Add Level 3 checks (gate readiness)
4. Build `CircuitBreaker` class implementing the Protocol above
5. Wire hooks into workflow execution path
6. Test with examples from `examples/` directory

---

## Success Criteria

- [ ] Level 0-3 checks all implemented and tested
- [ ] Circuit breaker halts on altitude violations, grade violations at gates, missing approvals
- [ ] Circuit breaker warns (doesn't halt) on advisory-level grade issues
- [ ] All example artifacts in `examples/` pass Level 0-1 validation
- [ ] SYNTHESIS-001 correctly validates as ARCHITECTURE-only
- [ ] At least one negative test per level (intentionally invalid artifact → correct error)
