# nowu 5×10 Verification Guide

**Version:** 1.1  
**Date:** 2026-05-05  
**Status:** CANONICAL

See MODEL-REFERENCE.md for altitude/phase definitions.

---

## Purpose

This guide is the single actionable reference for verification in the nowu 5×10 system.
It consolidates:

- The 4-level verification framework
- Altitude-specific checks
- Phase-specific checks
- Security integration (OWASP)
- Automated syntax verification script
- Human review checklist template

Use this document to run consistent verification from artifact creation through workflow completion.

---

## 1) Verification Levels Overview

The verification stack has four levels.

| Level | Name | Owner | Timing | Purpose |
|---|---|---|---|---|
| 0 | Syntax | Machine | On write / pre-commit | Validate structure and machine-checkable constraints |
| 1 | Semantic | Human or AI reviewer | Before phase transition | Validate meaning, fit, and epistemic integrity |
| 2 | Flow | Human + automation | On workflow completion | Validate traversal and dependency correctness |
| 3 | Circuit Breaker | Runtime guardrail (future) | At runtime | Prevent forbidden cross-altitude behavior |

Level progression is cumulative:

1. Level 0 rejects malformed artifacts early.
2. Level 1 ensures content quality and assignment correctness.
3. Level 2 validates the workflow graph and gate logic.
4. Level 3 blocks unsafe runtime interactions.

---

## 2) Level 0: Syntax (Machine-Checkable)

Level 0 verifies only objective, deterministic constraints.

### Required checks

- YAML frontmatter valid
- All required fields present for artifact class
- Field values match allowed enums
- `id` matches filename (knowledge artifacts)
- `artifact_class` is `knowledge` or `workflow_phase`
- File in correct `state/artifacts/{altitude}/{type}/` directory
- Referenced `related_artifacts` exist in index

### Notes

- This level should run automatically in local checks and CI.
- Violations are blocking for progression.
- Keep this level strict and deterministic; avoid subjective interpretation.

### Tool

- `verify-artifact.py`

---

## 3) Level 1: Semantic (Human or AI Review)

Level 1 verifies that the artifact says the right thing at the right altitude and phase.

### Required checks

- Altitude assignment correct (content discusses altitude-appropriate concerns)
- Phase assignment correct
- Epistemic grade matches evidence level
- `grade_justification` actually explains grade
- `consumer_altitudes` reasonable
- `related_artifacts` meaningful

### Review output

Reviewer should produce one of:

- `APPROVED`
- `NEEDS_REVISION` (with concrete issues)
- `BLOCKED` (critical violation)

---

## 4) Level 2: Flow (Workflow Traversal)

Level 2 verifies graph consistency and allowed phase transitions.

### Required checks

- DECISION has upstream ANALYSIS or OPTIONS
- IMPLEMENTATION has upstream DECISION or EVALUATION
- LEARN has upstream VERIFICATION
- SYNTHESIS has ≥2 approved USE-CASE inputs
- No EXECUTION artifact references STRATEGIC directly

### Outcome

- Flow-valid artifacts can be finalized.
- Flow-invalid artifacts must re-enter revision with explicit corrections.

---

## 5) Level 3: Circuit Breaker (Future)

Level 3 is a runtime enforcement layer to prevent structural violations during agent execution.

### Required checks

- STRATEGIC agent doesn't read EXECUTION artifacts
- EXECUTION agent doesn't write STRATEGIC artifacts
- LEARN promoted insights are abstracted
- SYNTHESIS only when ≥2 approved UCs
- Human gates enforced

### Implementation intent

- Guardrails should be runtime-blocking, not advisory.
- Violations should fail closed.
- Exceptions require explicit human override records.

---

## 6) Altitude-Specific Verification

Use the relevant checklist for the artifact altitude.

### STRATEGIC verification

What to verify:

- No file paths, module names, code-level details
- Time horizon ≥6 months
- Success criteria measurable at outcome level
- Language describes durable direction, not implementation

Example violation:

❌ `title: "Refactor soul module to use LLM client"`

Corrected:

✅ `title: "Enable continuous learning from multi-session usage patterns"`

---

### PRODUCT verification

What to verify:

- Describes user problem or job-to-be-done
- No architectural patterns or technical details
- Success criteria user-observable
- Focus on value and behavior from user perspective

Example violation:

❌ `title: "Store atoms in PostgreSQL with JSONB"`

Corrected:

✅ `title: "Cross-project knowledge retrieval in <200ms"`

---

### ARCHITECTURE verification

What to verify:

- Describes modules, contracts, protocols, quality attributes
- No file paths, function names, code snippets
- ADR format followed
- Alternatives documented
- Constraints and tradeoffs explicit

Example violation:

❌ `decision: "Add altitude field to line 47 of artifact.py"`

Corrected:

✅ `decision: "All workflow artifacts carry altitude metadata in frontmatter"`

---

### DELIVERY verification

What to verify:

- Defines scope boundary
- Acceptance criteria observable and testable
- Time-boxed (appetite stated)
- No implementation approach specified
- Scope is independently verifiable

Example violation:

❌ `scope: "Use Pydantic for validation and FastAPI"`

Corrected:

✅ `scope: "API endpoint accepts JSON payloads and returns 400 for invalid schema"`

---

### EXECUTION verification

What to verify:

- Contains code, tests, configuration
- References upstream DELIVERY shape
- LEARN artifacts abstract before promoting
- Changes are concrete and verifiable
- Direct references stay within allowed adjacency

Example violation (promoted lesson):

❌ `"Fixed bug in line 142 of bridge.py"`

Corrected:

✅ `"CLI adapter protocol required explicit defaults; implicit defaults caused silent failures"`

---

## 7) Phase-Specific Verification

Apply checks based on artifact phase.

### PROBLEM

Checklist:

- States concrete problem (not solution)
- Problem statement is falsifiable
- References evidence
- Answers: "why is this a problem?"

Anti-pattern:

- `Problem: We need feature X`

---

### ANALYSIS

Checklist:

- Breaks down the problem into components
- Identifies constraints and assumptions
- Documents research conducted
- Epistemic grade justified with evidence quality
- Feeds into OPTIONS or DECISION

---

### SYNTHESIS (ARCHITECTURE only)

Checklist:

- Input ≥2 approved UCs
- Themes are structural, not feature-level
- Each theme maps to 1+ ADR
- Out-of-scope explicitly listed

Trigger rule:

```python
if len(approved_ucs) >= 2:
    trigger_synthesis()
```

---

### OPTIONS

Checklist:

- ≥2 distinct options (not straw men)
- Tradeoffs explicit
- Options are mutually exclusive
- Evaluation criteria defined
- "Do nothing" considered

Anti-pattern:

- Options differ only in library choice

---

### DECISION

Checklist:

- One option chosen
- Rationale explains WHY
- Rejected alternatives recorded
- Reversibility stated

---

### EVALUATION

Checklist:

- Quality attribute scenarios tested
- OWASP checklist if security-sensitive
- Tradeoffs documented
- Status is `APPROVED` or `BLOCKED`

---

### IMPLEMENTATION

Checklist:

- Actual code/config/tests exist
- Acceptance criteria met
- Changes scoped to task boundary
- Tests pass
- No altitude violations in code comments

---

### VERIFICATION

Checklist:

- Formal tests executed
- Results recorded
- Acceptance criteria checked
- Failed → revision loop triggered
- Human approval for high-risk artifacts

---

### LEARN

Checklist:

- Lesson abstracted (no code snippets)
- Lesson is actionable
- Tagged with target altitude
- Related artifacts updated if lesson invalidates prior decision
- Pattern detected and stated clearly

---

## 8) Security Integration (OWASP)

Run security-aware verification when this trigger condition is met.

### Trigger

Apply OWASP-integrated review if an ADR introduces:

- New data storage
- External API integration
- PII/PHI/financial data handling
- Authentication or authorization logic

### Required checklist (ARCHITECTURE/EVALUATION phase)

- A01: Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Authentication
- A08: Data Integrity
- A09: Logging/Monitoring
- A10: SSRF

### Security review output

Include:

- Threat notes per applicable OWASP category
- Residual risk summary
- Required mitigations before approval
- Explicit approval state (`APPROVED` or `BLOCKED`)

---

## 9) Automated Verification Script

Use the following script for Level 0 syntax verification.

```python
#!/usr/bin/env python3
"""verify-artifact.py — Level 0 syntax verification for nowu 5×10 artifacts."""
import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS_KNOWLEDGE = [
    "artifact_class", "artifact_type", "id", "title",
    "origin_altitude", "origin_phase", "consumer_altitudes",
    "epistemic_grade", "grade_justification", "status",
    "created_at", "last_edited_at"
]

REQUIRED_FIELDS_WORKFLOW = [
    "artifact_class", "altitude", "phase",
    "session_id", "epistemic_grade", "grade_justification"
]

VALID_ALTITUDES = ["STRATEGIC", "PRODUCT", "ARCHITECTURE", "DELIVERY", "EXECUTION"]
VALID_PHASES = [
    "IDEA", "PROBLEM", "ANALYSIS", "SYNTHESIS", "OPTIONS",
    "DECISION", "EVALUATION", "IMPLEMENTATION", "VERIFICATION", "LEARN"
]
VALID_GRADES = [
    "SPECULATION", "HYPOTHESIS", "INFORMED_ESTIMATE",
    "EVIDENCE_BASED", "VERIFIED_FACT"
]
VALID_STATUS = ["ACTIVE", "SUPERSEDED", "DEPRECATED"]

def verify_artifact(filepath: Path) -> list[str]:
    violations = []
    with open(filepath) as f:
        content = f.read()
    if not content.startswith("---\n"):
        return ["No YAML frontmatter found"]
    try:
        _, fm, body = content.split("---\n", 2)
        metadata = yaml.safe_load(fm)
    except Exception as e:
        return [f"YAML parse error: {e}"]
    artifact_class = metadata.get("artifact_class")
    if artifact_class not in ["knowledge", "workflow_phase"]:
        violations.append(f"Invalid artifact_class: {artifact_class}")
        return violations
    required = REQUIRED_FIELDS_KNOWLEDGE if artifact_class == "knowledge" else REQUIRED_FIELDS_WORKFLOW
    for field in required:
        if field not in metadata:
            violations.append(f"Missing required field: {field}")
    if "altitude" in metadata and metadata["altitude"] not in VALID_ALTITUDES:
        violations.append(f"Invalid altitude: {metadata['altitude']}")
    if "origin_altitude" in metadata and metadata["origin_altitude"] not in VALID_ALTITUDES:
        violations.append(f"Invalid origin_altitude: {metadata['origin_altitude']}")
    if "phase" in metadata and metadata["phase"] not in VALID_PHASES:
        violations.append(f"Invalid phase: {metadata['phase']}")
    if "origin_phase" in metadata and metadata["origin_phase"] not in VALID_PHASES:
        violations.append(f"Invalid origin_phase: {metadata['origin_phase']}")
    if metadata.get("epistemic_grade") not in VALID_GRADES:
        violations.append(f"Invalid epistemic_grade: {metadata.get('epistemic_grade')}")
    if artifact_class == "knowledge" and metadata.get("status") not in VALID_STATUS:
        violations.append(f"Invalid status: {metadata.get('status')}")
    if "altitude" in metadata:
        expected_dir = f"state/artifacts/{metadata['altitude'].lower()}"
        if expected_dir not in str(filepath):
            violations.append(f"File in wrong directory (expected {expected_dir})")
    if artifact_class == "knowledge" and "id" in metadata:
        expected_filename = f"{metadata['id']}.md"
        if filepath.name != expected_filename:
            violations.append(f"Filename mismatch (expected {expected_filename})")
    return violations

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify-artifact.py <filepath>")
        sys.exit(2)
    violations = verify_artifact(Path(sys.argv[1]))
    if violations:
        print("Violations found:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("Artifact valid")
```

---

## 10) Human Review Checklist Template

Use this template for Level 1 and contextual sign-off.

```markdown
## Artifact Review: [ID]

**Reviewer:** [Name]
**Date:** YYYY-MM-DD
**Artifact:** [Path]

### Level 0: Syntax
- [ ] YAML frontmatter valid
- [ ] All required fields present
- [ ] Field values in allowed enums
- [ ] File path matches altitude

### Level 1: Semantic
- [ ] Altitude assignment is correct
- [ ] Phase assignment is correct
- [ ] Epistemic grade matches evidence in content
- [ ] Grade justification is meaningful
- [ ] Consumer altitudes are reasonable
- [ ] Related artifacts are relevant

### Altitude-Specific Checks
[Use appropriate section based on artifact's altitude]

### Phase-Specific Checks
[Use appropriate section based on artifact's phase]

### Decision
- [ ] APPROVED
- [ ] NEEDS_REVISION — issues below
- [ ] BLOCKED — critical violation

**Issues found:**
1. [Issue description]

**Recommendations:**
[What should change]
```

---

## 11) Verification Workflow

Run verification in this order:

1. On artifact creation: Run Level 0 automatically
2. Before phase transition: Run Level 1 review
3. On workflow completion: Run Level 2 flow checks
4. At runtime (future): Enable Level 3 circuit breaker

---

## Operational Usage Notes

### Recommended execution sequence per artifact

1. Execute `verify-artifact.py` on save or pre-commit.
2. Resolve all syntax violations before requesting semantic review.
3. Run semantic review against altitude and phase sections in this guide.
4. If artifact is terminal or transition-critical, run flow checks before closure.
5. For security-triggered ADRs, enforce OWASP-integrated evaluation before approval.

### Failure handling

- Any Level 0 violation: immediate fix required.
- Any Level 1 misassignment: reclassify altitude/phase or rewrite content.
- Any Level 2 flow break: add missing upstream artifacts or correct illegal references.
- Any Level 3 runtime violation (future): hard block and escalate for human decision.

### Evidence expectations by verification level

- Level 0 evidence: script output and pass/fail status.
- Level 1 evidence: completed checklist with reviewer notes.
- Level 2 evidence: traversal proof (upstream links, gate conditions, and approval states).
- Level 3 evidence (future): runtime guard logs and exception records.

### Traceability minimum

Each reviewed artifact should retain:

- reviewer identity
- review date
- verification decision
- unresolved issues (if any)
- link to superseding artifact if revised

### Escalation guidelines

Escalate to human review immediately when:

- security-trigger conditions apply
- epistemic grade appears overstated
- altitude assignment changes system intent
- flow dependency cannot be resolved without policy exception

### Definition of done for verification

Verification is complete only when:

- Level 0 passes
- Level 1 decision is APPROVED (or approved after revision)
- Level 2 checks pass for closure contexts
- Security checklist is completed when triggered
- Review record is stored and traceable
