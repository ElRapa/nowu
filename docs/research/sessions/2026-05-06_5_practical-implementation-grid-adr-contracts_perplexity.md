# Practical Implementation: 5×10 Grid, HYPOTHESIS-Grade ADRs, and Contract Evolution

## Part 1: Should We Define the 5×10 Grid As Navigation?

**Short answer: Yes — as a navigation grid, not an enforcement matrix.**

### The Grid as Cognitive GPS

The 5×10 matrix should function like a GPS system for agents: it tells them *where they are* and *where valid moves are*, but doesn't prescribe a single path.[^1]

**Implement it as:**

```python
# core/workflow_model.py

from enum import Enum
from typing import Set, Optional
from dataclasses import dataclass

class Altitude(Enum):
    STRATEGIC = "STRATEGIC"
    PRODUCT = "PRODUCT"
    ARCHITECTURE = "ARCHITECTURE"
    DELIVERY = "DELIVERY"
    EXECUTION = "EXECUTION"

class Phase(Enum):
    IDEA = "IDEA"
    PROBLEM = "PROBLEM"
    ANALYSIS = "ANALYSIS"
    SYNTHESIS = "SYNTHESIS"
    OPTIONS = "OPTIONS"
    DECISION = "DECISION"
    EVALUATION = "EVALUATION"
    IMPLEMENTATION = "IMPLEMENTATION"
    VERIFICATION = "VERIFICATION"
    LEARN = "LEARN"

@dataclass
class WorkflowCell:
    """A valid altitude×phase combination."""
    altitude: Altitude
    phase: Phase
    frequency: str  # 'PRIMARY' | 'SECONDARY' | 'RARE'
    examples: list[str]
    typical_agents: list[str]
    output_artifact_types: list[str]

# The 5×10 Grid Registry
WORKFLOW_GRID: dict[tuple[Altitude, Phase], WorkflowCell] = {
    # PRIMARY PATH (S1-S9) — traversed in every workflow
    (Altitude.DELIVERY, Phase.IDEA): WorkflowCell(
        altitude=Altitude.DELIVERY,
        phase=Phase.IDEA,
        frequency='PRIMARY',
        examples=['S1 nowu-intake', 'intake-NNN.md'],
        typical_agents=['nowu-intake'],
        output_artifact_types=['INTAKE']
    ),
    (Altitude.ARCHITECTURE, Phase.ANALYSIS): WorkflowCell(
        altitude=Altitude.ARCHITECTURE,
        phase=Phase.ANALYSIS,
        frequency='PRIMARY',
        examples=['S2 nowu-constraints', 'GAP G1 gap-analyst'],
        typical_agents=['nowu-constraints', 'gap-analyst'],
        output_artifact_types=['CONSTRAINTS', 'GAP_ANALYSIS']
    ),
    (Altitude.ARCHITECTURE, Phase.OPTIONS): WorkflowCell(
        altitude=Altitude.ARCHITECTURE,
        phase=Phase.OPTIONS,
        frequency='PRIMARY',
        examples=['S3 nowu-options', 'P2 architecture bootstrap'],
        typical_agents=['nowu-options'],
        output_artifact_types=['OPTIONS']
    ),
    (Altitude.ARCHITECTURE, Phase.DECISION): WorkflowCell(
        altitude=Altitude.ARCHITECTURE,
        phase=Phase.DECISION,
        frequency='PRIMARY',
        examples=['S4 nowu-decider', 'ADR-NNNN.md'],
        typical_agents=['nowu-decider'],
        output_artifact_types=['DECISION', 'ADR']
    ),
    (Altitude.DELIVERY, Phase.EVALUATION): WorkflowCell(
        altitude=Altitude.DELIVERY,
        phase=Phase.EVALUATION,
        frequency='PRIMARY',
        examples=['S5 nowu-shaper', 'SHAPE.md'],
        typical_agents=['nowu-shaper'],
        output_artifact_types=['SHAPE']
    ),
    (Altitude.EXECUTION, Phase.IMPLEMENTATION): WorkflowCell(
        altitude=Altitude.EXECUTION,
        phase=Phase.IMPLEMENTATION,
        frequency='PRIMARY',
        examples=['S6 nowu-implementer', 'code/tests'],
        typical_agents=['nowu-implementer'],
        output_artifact_types=['CODE', 'TEST']
    ),
    (Altitude.EXECUTION, Phase.VERIFICATION): WorkflowCell(
        altitude=Altitude.EXECUTION,
        phase=Phase.VERIFICATION,
        frequency='PRIMARY',
        examples=['S7 nowu-reviewer', 'S8 VBR'],
        typical_agents=['nowu-reviewer', 'vbr'],
        output_artifact_types=['REVIEW', 'VERIFICATION']
    ),
    (Altitude.EXECUTION, Phase.LEARN): WorkflowCell(
        altitude=Altitude.EXECUTION,
        phase=Phase.LEARN,
        frequency='PRIMARY',
        examples=['S9 nowu-curator'],
        typical_agents=['nowu-curator'],
        output_artifact_types=['LESSON', 'KNOWLEDGE_ATOM']
    ),
    
    # SECONDARY PATH (P0-P4, GAP) — pre-workflow and reflective cycles
    (Altitude.STRATEGIC, Phase.DECISION): WorkflowCell(
        altitude=Altitude.STRATEGIC,
        phase=Phase.DECISION,
        frequency='SECONDARY',
        examples=['P0.V Vision bootstrap'],
        typical_agents=['vision-bootstrap'],
        output_artifact_types=['VISION']
    ),
    (Altitude.PRODUCT, Phase.PROBLEM): WorkflowCell(
        altitude=Altitude.PRODUCT,
        phase=Phase.PROBLEM,
        frequency='SECONDARY',
        examples=['P0.UC Use-case agent', 'P1 Discovery'],
        typical_agents=['use-case-agent', 'discovery-agent'],
        output_artifact_types=['USE_CASE', 'PROBLEM_STATEMENT']
    ),
    (Altitude.ARCHITECTURE, Phase.SYNTHESIS): WorkflowCell(
        altitude=Altitude.ARCHITECTURE,
        phase=Phase.SYNTHESIS,
        frequency='SECONDARY',
        examples=['SYNTHESIS on 2+ UCs → themes'],
        typical_agents=['synthesis-agent'],
        output_artifact_types=['SYNTHESIS']
    ),
    (Altitude.ARCHITECTURE, Phase.IDEA): WorkflowCell(
        altitude=Altitude.ARCHITECTURE,
        phase=Phase.IDEA,
        frequency='SECONDARY',
        examples=['GAP G0 gap-detector'],
        typical_agents=['gap-detector'],
        output_artifact_types=['GAP_SIGNAL']
    ),
    
    # RARE — valid but infrequent
    (Altitude.STRATEGIC, Phase.VERIFICATION): WorkflowCell(
        altitude=Altitude.STRATEGIC,
        phase=Phase.VERIFICATION,
        frequency='RARE',
        examples=['Goal review after 5+ intakes'],
        typical_agents=['goal-reviewer'],
        output_artifact_types=['GOAL_REVIEW']
    ),
    
    # NON-EXISTENT cells are simply not in the registry
}

def get_valid_next_moves(current: tuple[Altitude, Phase]) -> list[WorkflowCell]:
    """
    Given current position, return valid next cells.
    This is the navigation logic.
    """
    altitude, phase = current
    
    # S1-S9 primary path
    if current == (Altitude.DELIVERY, Phase.IDEA):
        return [WORKFLOW_GRID[(Altitude.ARCHITECTURE, Phase.ANALYSIS)]]
    elif current == (Altitude.ARCHITECTURE, Phase.ANALYSIS):
        return [WORKFLOW_GRID[(Altitude.ARCHITECTURE, Phase.OPTIONS)]]
    elif current == (Altitude.ARCHITECTURE, Phase.OPTIONS):
        return [WORKFLOW_GRID[(Altitude.ARCHITECTURE, Phase.DECISION)]]
    elif current == (Altitude.ARCHITECTURE, Phase.DECISION):
        return [WORKFLOW_GRID[(Altitude.DELIVERY, Phase.EVALUATION)]]
    elif current == (Altitude.DELIVERY, Phase.EVALUATION):
        return [WORKFLOW_GRID[(Altitude.EXECUTION, Phase.IMPLEMENTATION)]]
    elif current == (Altitude.EXECUTION, Phase.IMPLEMENTATION):
        return [WORKFLOW_GRID[(Altitude.EXECUTION, Phase.VERIFICATION)]]
    elif current == (Altitude.EXECUTION, Phase.VERIFICATION):
        # VBR can loop back to S6 or proceed to S9
        return [
            WORKFLOW_GRID[(Altitude.EXECUTION, Phase.IMPLEMENTATION)],  # retry
            WORKFLOW_GRID[(Altitude.EXECUTION, Phase.LEARN)]  # proceed
        ]
    elif current == (Altitude.EXECUTION, Phase.LEARN):
        # S9 curator can promote to any altitude
        return [cell for cell in WORKFLOW_GRID.values() if cell.phase == Phase.LEARN]
    
    # For other paths, allow exploration
    return []

def is_valid_cell(altitude: Altitude, phase: Phase) -> bool:
    """Check if an altitude×phase combination is valid."""
    return (altitude, phase) in WORKFLOW_GRID

def get_cell_info(altitude: Altitude, phase: Phase) -> Optional[WorkflowCell]:
    """Get metadata about a cell."""
    return WORKFLOW_GRID.get((altitude, phase))
```

**How agents use it:**

```python
# In your orchestrator or agent runtime

current_artifact = load_artifact("state/session-007/S3-options.md")
current_position = (current_artifact.altitude, current_artifact.phase)

# Navigation query
next_moves = get_valid_next_moves(current_position)
print(f"From {current_position}, valid next steps:")
for move in next_moves:
    print(f"  → {move.altitude.value}/{move.phase.value} via {move.typical_agents}")

# Validation query
if not is_valid_cell(Altitude.STRATEGIC, Phase.EVALUATION):
    raise ValueError("STRATEGIC/EVALUATION is not a valid workflow cell")
```

**The grid answers four questions for any agent:**
1. **Where am I?** → `get_cell_info(artifact.altitude, artifact.phase)`
2. **Is this a valid position?** → `is_valid_cell(altitude, phase)`
3. **Where can I go next?** → `get_valid_next_moves((altitude, phase))`
4. **How common is this path?** → `cell.frequency` ('PRIMARY' | 'SECONDARY' | 'RARE')

**You fill agents as you go** — each cell lists `typical_agents` but you start with empty lists and populate as agents are implemented. The grid structure is stable from day one; the agent assignments evolve.

***

## Part 2: Sisyphus's Three Questions

### Q1: Minimum ADR Content for AI Agents

**Research basis: GitHub Spec Kit's four-phase gated workflow**[^2][^3][^4][^5]

GitHub Spec Kit defines what AI agents need to implement against constraints. The pattern:[^3]

1. **Constitution** (`speckit.constitution`) — non-negotiable rules and constraints
2. **Spec** — the "what" and "why"
3. **Plan** — technical implementation approach with constraints from Constitution
4. **Tasks** — small, well-defined chunks

**For nowu ADRs, this maps to:**

```markdown
# ADR-0008: Session State Strategy (HYPOTHESIS)

## Status
HYPOTHESIS — to be validated by intake-007 and intake-008

## Context (the "why")
**Problem:** UCs NF-01, NF-14, PK-08 require persistent multi-session state.
Current P0-P4 uses markdown files in `state/`. S1-S9 must resume workflows 
after VBR rejection (S8→S6 retry) or overnight pause.

**Quality attributes affected:**
- Resumability (primary) — must resume from any step
- Testability (secondary) — agents must unit-test against artifacts without running full pipeline
- AI-buildability (secondary) — agents read/write artifacts without database expertise

**Evidence:** 
- 3 UCs with multi-session requirement [UC-NF-01, UC-NF-14, UC-PK-08]
- 2 intake retries in manual testing (intake-004, intake-005) both required manual state reconstruction

## Constraints (the "what you must respect")
**From ADR-0001 (Module boundary enforcement):**
- Session state must be readable by `flow`, `soul`, and `know` without runtime coupling
- State format must be version-controllable (git-trackable)

**From ADR-0006 (Soul-flow integration):**
- Artifacts are the API — no runtime state sharing

**From Architecture Vision:**
- Local-first — no cloud dependencies in core workflow

**Implementation constraints for AI agents:**
1. State MUST be in `state/session-{id}/` directory structure
2. Each step MUST produce one artifact file with frontmatter metadata
3. Frontmatter MUST include: `altitude`, `phase`, `step`, `date`, `epistemic_grade`
4. Artifact filenames MUST follow pattern: `{step}-{agent-name}.md`
5. Resume logic MUST work by reading artifacts only — no in-memory state

## Options Considered

### Option A: Pure Markdown Files (RECOMMENDED for HYPOTHESIS validation)
**Approach:** Each S1-S9 step writes `state/session-NNN/S{N}-{agent}.md` with YAML frontmatter.

**Pros:**
- Zero dependencies — no database
- Git-native versioning
- AI agents read/write markdown natively (no schema translation)
- Human-inspectable for debugging

**Cons:**
- No indexed queries (must scan files to find "all sessions with VBR failure")
- Large file count at scale (1000 sessions × 9 steps = 9000 files)

**AI implementation guidance:**
```python
# flow/session.py

from pathlib import Path
from dataclasses import dataclass, asdict
import yaml

@dataclass
class SessionArtifact:
    session_id: str
    step: str
    altitude: str
    phase: str
    agent: str
    date: str
    epistemic_grade: str
    content: str
    
def write_artifact(artifact: SessionArtifact):
    """AI agents call this to persist step output."""
    session_dir = Path(f"state/session-{artifact.session_id}")
    session_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = session_dir / f"{artifact.step}-{artifact.agent}.md"
    
    frontmatter = {k: v for k, v in asdict(artifact).items() if k != 'content'}
    
    with open(file_path, 'w') as f:
        f.write("---\\n")
        yaml.dump(frontmatter, f)
        f.write("---\\n\\n")
        f.write(artifact.content)

def resume_from_step(session_id: str, step: str) -> SessionArtifact:
    """AI agents call this to resume a workflow."""
    file_path = Path(f"state/session-{session_id}") / f"{step}-*.md"
    matches = list(Path(f"state/session-{session_id}").glob(f"{step}-*.md"))
    
    if not matches:
        raise FileNotFoundError(f"No artifact found for session {session_id} step {step}")
    
    with open(matches) as f:
        content = f.read()
        parts = content.split('---', 2)
        metadata = yaml.safe_load(parts)[^6]
        body = parts.strip()[^7]
    
    return SessionArtifact(**metadata, content=body)
```

**Validation criteria (what makes this HYPOTHESIS → INFORMED_ESTIMATE):**
- [ ] intake-007 completes S1→S8 without "cannot resume" errors
- [ ] intake-008 VBR rejection → S6 retry works from artifacts alone (no manual intervention)
- [ ] S9 curator extracts lessons from markdown frontmatter without parsing failures
- [ ] File count at 20 sessions < 200 files (9 steps × 20 + 20% overhead)

**If validation fails:** Escalate to Option B (hybrid markdown + SQLite index).

### Option B: Hybrid Markdown + SQLite Index (deferred until 50+ sessions)
**Approach:** Same markdown files, but `state/sessions.db` indexes metadata for queries.

**When to escalate:** If GAP G1 (gap analyst) cannot efficiently answer "find all sessions with altitude drift" by scanning 500+ markdown files.

### Option C: SQLite Per-Session (rejected for v1)
**Rejected because:** Violates "AI-buildability" — agents need SQL expertise, schema migrations, and ORM knowledge. Markdown is the lowest-friction format for AI agents.

## Decision

**For v1-core and v1.0:** Use **Option A (pure markdown)** at HYPOTHESIS grade.

**Rationale:**
1. Satisfies all hard constraints (ADR-0001, ADR-0006, Architecture Vision)
2. Lowest implementation friction for AI agents (no database layer)
3. Validation criteria are measurable and achievable in 1-2 intakes
4. Failure mode is recoverable — can add SQLite index later without rewriting artifacts

**Recorded alternatives:** Option B deferred, Option C rejected.

## Consequences

**Positive:**
- AI agents implement against markdown I/O contract (simplest possible)
- Human-inspectable state for debugging
- Git-native versioning enables time-travel debugging

**Negative:**
- No efficient cross-session queries until Option B
- File count grows linearly with sessions (mitigation: archival after 6 months)

**Risks:**
- At 1000 sessions, directory scan becomes slow (mitigation: add SQLite index at 50 sessions)
- Concurrent writes to same session could corrupt YAML (mitigation: file locking in v1.1)

## Validation Triggers

**Promote to INFORMED_ESTIMATE if:**
- 2 intakes complete validation criteria above
- No "cannot resume" errors in 10 consecutive workflows

**Supersede if:**
- File count exceeds 500 and GAP queries take >5 seconds
- 3+ incidents of YAML parse errors from concurrent writes

## Implementation Checklist for AI Agents

```python
# Example agent using this ADR

from flow.session import write_artifact, resume_from_step, SessionArtifact

class NowuShaper:
    def execute(self, session_id: str):
        # Step 1: Resume from prior step
        decision = resume_from_step(session_id, "S4")
        
        # Step 2: Process (actual shaping logic)
        shaped_scope = self.shape(decision.content)
        
        # Step 3: Write artifact (contract from ADR-0008)
        artifact = SessionArtifact(
            session_id=session_id,
            step="S5",
            altitude="DELIVERY",
            phase="EVALUATION",
            agent="nowu-shaper",
            date=datetime.now().isoformat(),
            epistemic_grade="HYPOTHESIS",
            content=shaped_scope
        )
        write_artifact(artifact)
```

## Links
- Source UCs: [UC-NF-01](../use-cases/UC-NF-01.md), [UC-NF-14](../use-cases/UC-NF-14.md)
- Depends on: [ADR-0001](./ADR-0001-module-boundary-enforcement.md), [ADR-0006](./ADR-0006-soul-flow-integration-pattern.md)
- Architecture Vision: [ARCHITECTURE-VISION.md](../arch/ARCHITECTURE-VISION.md)
```

**What makes this HYPOTHESIS-grade but AI-implementable?**

1. **Constraints are explicit** — 5 implementation rules AI agents must follow[^5][^2]
2. **Decision is clear** — "Use Option A" with rationale
3. **Validation criteria are measurable** — 4 checkboxes that can be automated
4. **Implementation example is provided** — AI agent sees exactly what code to write
5. **Failure mode is documented** — "If validation fails, escalate to Option B"

**Contrast with INFORMED_ESTIMATE-grade ADR:**

An INFORMED_ESTIMATE ADR (after 2 intakes validate) would add:
- Performance benchmarks (file scan time: 50 sessions → 0.3s, 200 sessions → 1.2s)
- Actual failure count (0 "cannot resume" errors in 15 workflows)
- Adjustment based on code feedback ("Added file locking after concurrent write corruption in intake-011")

***

### Q2: ADR Invalidation Feedback Mechanism

**Research basis: Fitness functions + evolutionary architecture**[^8][^9][^10]

The problem: S6 implementer discovers that `SessionArtifact` contract from ADR-0008 doesn't support storing approval state (needed for S8 VBR human approval). Do you:
- (A) Silently extend the contract and keep going? → Drift
- (B) Re-run full SYNTHESIS cycle? → Overhead
- (C) Lightweight contract amendment with traceability? → Correct

**The fitness function pattern:**[^9][^8]

> "Fitness functions are guardrails that enable continuous evolution of your system's architecture, within a range and direction that you desire and define."[^9]

**For nowu, implement as:**

```python
# core/fitness_functions.py

from dataclasses import dataclass
from typing import Callable
from enum import Enum

class FitnessScope(Enum):
    ATOMIC = "ATOMIC"      # Single module or contract
    HOLISTIC = "HOLISTIC"  # Cross-module interaction

@dataclass
class ArchitecturalFitness:
    """A fitness function validates an architectural characteristic."""
    name: str
    scope: FitnessScope
    quality_attribute: str  # Resumability, Testability, AI-buildability
    check: Callable[[], tuple[bool, str]]
    severity: str  # 'BLOCKING' | 'WARNING' | 'INFO'

# Example fitness functions for ADR-0008 (Session State)

def check_artifact_resumability() -> tuple[bool, str]:
    """
    Atomic fitness function: Can any S1-S9 agent resume from artifacts alone?
    """
    test_sessions = ['session-007', 'session-008', 'session-009']
    
    for session_id in test_sessions:
        for step in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']:
            try:
                artifact = resume_from_step(session_id, step)
                # Check required metadata exists
                if not all([artifact.altitude, artifact.phase, artifact.step]):
                    return False, f"Missing metadata in {session_id}/{step}"
            except FileNotFoundError:
                return False, f"Cannot resume {session_id} from {step}"
    
    return True, "All test sessions resumable"

def check_contract_completeness() -> tuple[bool, str]:
    """
    Atomic fitness function: Does SessionArtifact contract support all S1-S9 needs?
    """
    required_fields = [
        'session_id', 'step', 'altitude', 'phase', 'agent',
        'date', 'epistemic_grade', 'content'
    ]
    
    from flow.session import SessionArtifact
    artifact_fields = SessionArtifact.__dataclass_fields__.keys()
    
    missing = set(required_fields) - set(artifact_fields)
    if missing:
        return False, f"SessionArtifact missing fields: {missing}"
    
    return True, "Contract complete"

def check_altitude_boundaries() -> tuple[bool, str]:
    """
    Holistic fitness function: Are module boundaries respected?
    (From ADR-0001)
    """
    violations = []
    
    # Check: flow does not import from soul
    try:
        import ast
        flow_files = Path('flow').glob('**/*.py')
        for file in flow_files:
            tree = ast.parse(file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith('soul'):
                        violations.append(f"{file}: imports {node.module}")
    except Exception as e:
        return False, f"Parse error: {e}"
    
    if violations:
        return False, f"Altitude boundary violations: {violations}"
    
    return True, "Module boundaries respected"

# Register fitness functions
FITNESS_SUITE = [
    ArchitecturalFitness(
        name="artifact_resumability",
        scope=FitnessScope.ATOMIC,
        quality_attribute="Resumability",
        check=check_artifact_resumability,
        severity='BLOCKING'
    ),
    ArchitecturalFitness(
        name="contract_completeness",
        scope=FitnessScope.ATOMIC,
        quality_attribute="AI-buildability",
        check=check_contract_completeness,
        severity='BLOCKING'
    ),
    ArchitecturalFitness(
        name="altitude_boundaries",
        scope=FitnessScope.HOLISTIC,
        quality_attribute="Testability",
        check=check_altitude_boundaries,
        severity='BLOCKING'
    ),
]

def run_fitness_checks() -> dict:
    """Run all fitness functions. Called in CI/CD."""
    results = {}
    for fitness in FITNESS_SUITE:
        passed, message = fitness.check()
        results[fitness.name] = {
            'passed': passed,
            'message': message,
            'severity': fitness.severity,
            'quality_attribute': fitness.quality_attribute
        }
        
        if not passed and fitness.severity == 'BLOCKING':
            print(f"❌ BLOCKING: {fitness.name} failed: {message}")
    
    return results
```

**The lightweight invalidation process:**

```markdown
# When S6 implementer discovers contract gap

## Step 1: Detect via fitness function failure

```bash
$ python -m core.fitness_functions
❌ BLOCKING: contract_completeness failed: SessionArtifact missing fields: {'approval_state', 'approver'}
```

## Step 2: Create amendment artifact (not full ADR revision)

```markdown
# ADR-0008-AMENDMENT-001: Add Approval State to SessionArtifact

## Date
2026-05-10

## Context
S8 VBR agent needs to record human approval decision (APPROVED | REJECTED | PENDING).
Current SessionArtifact contract from ADR-0008 does not support this.

## Impact Analysis
**Breaking change?** NO — adding optional fields preserves backward compatibility.
**Affected agents:** S8 VBR (writer), S6 implementer (reader after retry)
**Quality attributes:** Resumability (unchanged), Testability (improved — approval state now traceable)

## Amendment
Add to SessionArtifact contract in `core/contracts.py`:

```python
@dataclass
class SessionArtifact:
    # ... existing fields ...
    approval_state: Optional[str] = None  # 'APPROVED' | 'REJECTED' | 'PENDING'
    approver: Optional[str] = None        # human identifier
```

## Validation
- [ ] S8 VBR writes approval_state to artifact
- [ ] S6 reads approval_state after VBR retry (intake-012)
- [ ] Fitness function `contract_completeness` passes

## Supersedes
None — this amends ADR-0008 without invalidating it.

## Parent ADR
[ADR-0008](./ADR-0008-session-state-strategy.md)
```

## Step 3: Update parent ADR status (not rewrite)

In ADR-0008, add to frontmatter:

```yaml
status: INFORMED_ESTIMATE  # promoted after 2 intakes
amendments: 
  - ADR-0008-AMENDMENT-001  # approval state fields added 2026-05-10
```

## Step 4: Re-run fitness functions

```bash
$ python -m core.fitness_functions
✅ contract_completeness passed: All required fields present
✅ artifact_resumability passed: All test sessions resumable
✅ altitude_boundaries passed: Module boundaries respected
```
```

**This pattern is validated by:**

1. **API versioning research** — backward-compatible changes (adding optional fields) don't require new major versions[^11][^12]
2. **Fitness functions literature** — automated checks enable fast feedback during evolution[^10][^8][^9]
3. **ADR lifecycle research** — amendments preserve decision history without requiring full re-evaluation[^13][^14][^15]

**When does contract amendment escalate to full ADR supersession?**

| Change type | Mechanism | Example |
|---|---|---|
| **Add optional field** | Amendment | Adding `approval_state` to SessionArtifact |
| **Add new artifact type** | Amendment | Adding `REVIEW` artifact for S7 |
| **Change field semantics** | Amendment with migration note | `epistemic_grade` values change from 4 levels to 5 |
| **Remove required field** | Supersession (breaking) | Removing `altitude` from SessionArtifact |
| **Change storage format** | Supersession | Markdown → SQLite (ADR-0008 superseded by ADR-0015) |

***

### Q3: Lightweight Contract Update Process for nowu Specifically

**Given:**
- 5 modules: `core`, `flow`, `bridge`, `soul`, `know`
- Protocol-based contracts in `core/contracts.py`[^16][^17][^18]
- Architecture Vision: "artifacts are the API" and "module boundaries are epistemic boundaries"
- Problem: S1-S9 discovers `KnowledgeStoreProvider` protocol doesn't support temporal queries

**The lightweight 3-step process:**

#### Step 1: Detect Contract Gap (Agent or Human)

**Scenario:** S9 curator tries to promote lesson to `know` but needs "find all atoms created after 2026-05-01" query. Current `KnowledgeStoreProvider` protocol only supports `get_atom(id)` and `store_atom(atom)`.

**Detection mechanism:**

```python
# flow/agents/nowu_curator.py (S9 agent)

from core.contracts import KnowledgeStoreProvider

class NowuCurator:
    def __init__(self, knowledge_store: KnowledgeStoreProvider):
        self.knowledge = knowledge_store
    
    def promote_lesson(self, lesson: Lesson):
        # Need to check: Is there already a similar lesson?
        # This requires temporal query (not in contract)
        
        try:
            recent_atoms = self.knowledge.query_by_date_range(
                start_date="2026-05-01",
                end_date="2026-05-10"
            )
        except AttributeError:
            # Contract gap detected
            raise ContractGapError(
                contract="KnowledgeStoreProvider",
                missing_method="query_by_date_range",
                requester="nowu-curator (S9)",
                context="Lesson promotion needs temporal deduplication"
            )
```

**This raises a traceable exception that triggers the amendment process.**

#### Step 2: Propose Contract Amendment (In-Place, Non-Breaking)

**File:** `core/contracts.py` (the single source of truth)

**Before:**

```python
# core/contracts.py

from typing import Protocol, Optional
from datetime import datetime

class Atom:
    """A knowledge atom with temporal metadata."""
    id: str
    content: str
    confidence: float
    created_at: datetime
    # ... other fields

class KnowledgeStoreProvider(Protocol):
    """Contract for knowledge persistence."""
    
    def store_atom(self, atom: Atom) -> None:
        """Persist an atom."""
        ...
    
    def get_atom(self, id: str) -> Optional[Atom]:
        """Retrieve an atom by ID."""
        ...
```

**After amendment:**

```python
# core/contracts.py

from typing import Protocol, Optional, List
from datetime import datetime

class Atom:
    """A knowledge atom with temporal metadata."""
    id: str
    content: str
    confidence: float
    created_at: datetime
    # ... other fields

class KnowledgeStoreProvider(Protocol):
    """Contract for knowledge persistence.
    
    Amendment history:
    - 2026-05-10: Added query_by_date_range for S9 curator (ADR-0009-AMENDMENT-001)
    """
    
    def store_atom(self, atom: Atom) -> None:
        """Persist an atom."""
        ...
    
    def get_atom(self, id: str) -> Optional[Atom]:
        """Retrieve an atom by ID."""
        ...
    
    def query_by_date_range(
        self,
        start_date: str,  # ISO 8601
        end_date: str,
        limit: int = 100
    ) -> List[Atom]:
        """
        Retrieve atoms created within date range.
        
        Added: 2026-05-10 (ADR-0009-AMENDMENT-001)
        Requester: nowu-curator (S9)
        Rationale: Temporal deduplication for lesson promotion
        
        Args:
            start_date: ISO 8601 date string (inclusive)
            end_date: ISO 8601 date string (inclusive)
            limit: Max atoms to return (default 100)
        
        Returns:
            List of atoms sorted by created_at descending
        """
        ...
```

**This is non-breaking because:**
1. Existing methods unchanged
2. New method added (existing implementers can stub or implement)
3. Python Protocol checking is structural — implementers don't need to explicitly inherit

**TypedDict backward compatibility pattern:**[^17][^19]

If the contract were TypedDict instead of Protocol:

```python
# Non-breaking: Add optional field with default
class SessionArtifactV2(TypedDict, total=False):
    approval_state: str  # optional — total=False means not required
```

This is the same pattern used in PEP 728 for TypedDict evolution.[^19]

#### Step 3: Implement in Consumer, Stub in Provider (Stage 3)

**Implementer (consumer side — flow module):**

```python
# flow/agents/nowu_curator.py

class NowuCurator:
    def promote_lesson(self, lesson: Lesson):
        # Now contract supports temporal query
        recent_atoms = self.knowledge.query_by_date_range(
            start_date="2026-05-01",
            end_date="2026-05-10"
        )
        
        # Check for duplicates before promoting
        for atom in recent_atoms:
            if self.is_similar(lesson, atom):
                print(f"Lesson already exists as {atom.id}, skipping promotion")
                return
        
        # No duplicate found, promote
        new_atom = Atom(
            id=generate_id(),
            content=lesson.summary,
            confidence=0.8,
            created_at=datetime.now()
        )
        self.knowledge.store_atom(new_atom)
```

**Provider (know module) — Stage 1: Stub**

```python
# know/knowledge_store.py

class MarkdownKnowledgeStore:
    """Implementation of KnowledgeStoreProvider using markdown files."""
    
    def store_atom(self, atom: Atom) -> None:
        # ... existing implementation
        pass
    
    def get_atom(self, id: str) -> Optional[Atom]:
        # ... existing implementation
        pass
    
    def query_by_date_range(
        self,
        start_date: str,
        end_date: str,
        limit: int = 100
    ) -> List[Atom]:
        """
        Stub implementation: scan all atoms and filter by date.
        TODO: Add efficient index after 50+ atoms (ADR-0009-AMENDMENT-001)
        """
        all_atoms = self._load_all_atoms()
        
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        filtered = [
            atom for atom in all_atoms
            if start <= atom.created_at <= end
        ]
        
        return sorted(filtered, key=lambda a: a.created_at, reverse=True)[:limit]
```

**Stage 2: Optimize when needed**

After 50+ atoms, if scan performance degrades:

```python
def query_by_date_range(self, start_date: str, end_date: str, limit: int = 100) -> List[Atom]:
    """Optimized: use temporal index."""
    # Check if index exists
    index_path = Path('state/knowledge/temporal_index.json')
    if index_path.exists():
        return self._query_from_index(start_date, end_date, limit)
    else:
        # Fallback to scan
        return self._query_by_scan(start_date, end_date, limit)
```

**No architectural re-evaluation needed** because:
1. Contract change is non-breaking (added method, didn't remove)
2. Consumer works immediately with stub implementation
3. Provider optimizes incrementally without changing contract

**Fitness function validates the amendment:**

```python
def check_contract_method_coverage() -> tuple[bool, str]:
    """
    Verify all KnowledgeStoreProvider implementations support required methods.
    """
    from know.knowledge_store import MarkdownKnowledgeStore
    
    required_methods = ['store_atom', 'get_atom', 'query_by_date_range']
    
    for method in required_methods:
        if not hasattr(MarkdownKnowledgeStore, method):
            return False, f"MarkdownKnowledgeStore missing {method}"
    
    return True, "All contract methods implemented"
```

***

## Summary: The Three-Layer Architectural Feedback System

| Layer | Mechanism | When to use | Output |
|---|---|---|---|
| **1. Navigation** | 5×10 grid registry | Agent asks "Where can I go from here?" | Valid next cells |
| **2. Validation** | Fitness functions | CI/CD checks after each commit | Pass/fail + blocking severity |
| **3. Amendment** | Contract evolution + ADR amendments | Contract gap detected during implementation | Updated Protocol + amendment ADR |

**The coherence mechanism:**

1. **Grid provides structure** — agents know valid altitude×phase combinations
2. **Fitness functions provide guardrails** — automated checks prevent drift
3. **Amendments provide evolution** — contracts adapt without breaking existing agents

**All three layers share one principle:** Traceability through explicit artifacts (grid registry, fitness test results, amendment ADRs) rather than implicit tribal knowledge.

This is the research-backed middle ground between BDUF (write perfect architecture upfront) and YAGNI (no architecture until you need it). GitHub Spec Kit calls it "spec-driven development". Evolutionary architecture calls it "fitness functions". nowu implements both through the 5×10 grid + fitness + amendment pattern.[^2][^3][^8][^9]

---

## References

1. [MODEL-REFERENCE.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/a8f96545-8701-4263-8be2-24e02a56f12f/MODEL-REFERENCE.md?AWSAccessKeyId=ASIA2F3EMEYE53TL3EMT&Signature=NVQ8jAoYigUx5ipwRgEiXZ858H0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEMz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJJNrdHEXYlbqokylFcPhmmcwgJscut37yRnPVht%2FPZgIhAKpIMc5X3mAVKLf5nwtIhiEQBRqQCM8zQpqZjJP7fTS9KvwECJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1IgygpsZzwMb6us6ti28q0ASD1lgMu8LdhPi2dtMJeEpvId7qcz274iJZAzRAgJm2RIWVK1iCYOdkm2weQl8OkPkg9fJZWS9rf7FPiRJJMXIHRMMgkap9WwYUTHwNmZiXjIa3hui964zORgU4s1kO%2FCFdQCwuU7Ts4CTlQTNWsKfpcPqsLMyfWWJjTdtlqeZTDftw40Gjk8cEnfCgpKBIAi1sP85t2d%2BjCOwPtxCVZdrZGnHheCQBsXfD1RrKBluw21PVNzf5mGIZkIWdqoSyG%2FgN%2B%2Br6zuQg%2B42LTLOnd0zToQOgLqnPK92KM0CJ%2FBnXA45VA5fk6HwtU1ygrto50s1VKx5ugHsPKPnzUMwsOk4ouvOVQNxmOwvZx6axtCqRMrcZ23WwWkbA1ObYJ0KKAxd7%2BS%2BBKmhqSDdq9QDdZyBF3HWUGpIe1FMFFykzZjmgDbGfkMV2NY6Svo6EDGls87BGZ0Mfsurz7yCvqbqEXomvYjyA0KKRWJuwwDzs%2BaBLPpwpOrNOYqbe2EMr3AmxxU2%2FvkEkeWRTBJxvFz1x1VwdEyEZUexdsva0EueXDUKA7f5OG8DzGV%2BYWB2uWoBezGEGIjGsEFdxZfr2FWZWYW%2FfMzwdQSEa9T5dZIFaFkkhs%2F5qOvsrDEK9PR7i%2B9a3chRTI2XZ17emCzsOUVhTEahlHPDbBCAKtkAywmPQ4ilEYHEH7jcTC9xV2cTE9xvwp1qEPeP9RGQbbk2i1kSG2O%2B%2F4VHpKrR7Jgk1U8Tz98Je3FPbfmhfyP8fS14luwWJCkBsZkgUZmQmaLjEUIKIZF4dMNj56s8GOpcBlBkL7sMDZc6BgVvM0OxOJnk4zCezG%2Bff7llqrxNvvd2JPrByK9A6zLQEeEiu%2BOUQOfd51qfKsbxxYjR2lxSHxxN1MckhVuI1ghYmIZPE7ZH8RTk9MMN%2FxW79GUMsCB2%2Foy9%2FSplDQiHflZ1UIJqIhplmxLDsBy02sD8FA3VnLPA65jU6gN2B3bF8deYLn8D4AAJXe%2BB9Ww%3D%3D&Expires=1778043563) - Version 1.1 Date 2026-05-05 Status CANONICAL This document is the single authoritative reference for...

2. [github/spec-kit: Toolkit to help you get started with Spec-Driven ...](https://github.com/github/spec-kit) - Supported AI Coding Agent Integrations. Spec Kit works with 30+ AI coding agents — both CLI tools an...

3. [Spec-driven development with AI: Get started with a new open ...](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) - Spec Kit works with coding agents like GitHub Copilot, Claude Code, and Gemini CLI. The key is to us...

4. [Diving Into Spec-Driven Development With GitHub Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit) - Ask the AI agent to create several implementations that rely on different Figma mocks exposed throug...

5. [How to write a good spec for AI agents - Addy Osmani](https://addyosmani.com/blog/good-spec/) - Boundaries: What the agent should never touch - secrets, vendor directories, production configs, spe...

6. [nowu_palantir_guo_et_al_comparison.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/6693d3f8-e4b4-4d6e-895e-c1ca51b8d317/nowu_palantir_guo_et_al_comparison.md?AWSAccessKeyId=ASIA2F3EMEYE53TL3EMT&Signature=6kZYPKQ3kos9rAhbARz6581QqVw%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEMz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJJNrdHEXYlbqokylFcPhmmcwgJscut37yRnPVht%2FPZgIhAKpIMc5X3mAVKLf5nwtIhiEQBRqQCM8zQpqZjJP7fTS9KvwECJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1IgygpsZzwMb6us6ti28q0ASD1lgMu8LdhPi2dtMJeEpvId7qcz274iJZAzRAgJm2RIWVK1iCYOdkm2weQl8OkPkg9fJZWS9rf7FPiRJJMXIHRMMgkap9WwYUTHwNmZiXjIa3hui964zORgU4s1kO%2FCFdQCwuU7Ts4CTlQTNWsKfpcPqsLMyfWWJjTdtlqeZTDftw40Gjk8cEnfCgpKBIAi1sP85t2d%2BjCOwPtxCVZdrZGnHheCQBsXfD1RrKBluw21PVNzf5mGIZkIWdqoSyG%2FgN%2B%2Br6zuQg%2B42LTLOnd0zToQOgLqnPK92KM0CJ%2FBnXA45VA5fk6HwtU1ygrto50s1VKx5ugHsPKPnzUMwsOk4ouvOVQNxmOwvZx6axtCqRMrcZ23WwWkbA1ObYJ0KKAxd7%2BS%2BBKmhqSDdq9QDdZyBF3HWUGpIe1FMFFykzZjmgDbGfkMV2NY6Svo6EDGls87BGZ0Mfsurz7yCvqbqEXomvYjyA0KKRWJuwwDzs%2BaBLPpwpOrNOYqbe2EMr3AmxxU2%2FvkEkeWRTBJxvFz1x1VwdEyEZUexdsva0EueXDUKA7f5OG8DzGV%2BYWB2uWoBezGEGIjGsEFdxZfr2FWZWYW%2FfMzwdQSEa9T5dZIFaFkkhs%2F5qOvsrDEK9PR7i%2B9a3chRTI2XZ17emCzsOUVhTEahlHPDbBCAKtkAywmPQ4ilEYHEH7jcTC9xV2cTE9xvwp1qEPeP9RGQbbk2i1kSG2O%2B%2F4VHpKrR7Jgk1U8Tz98Je3FPbfmhfyP8fS14luwWJCkBsZkgUZmQmaLjEUIKIZF4dMNj56s8GOpcBlBkL7sMDZc6BgVvM0OxOJnk4zCezG%2Bff7llqrxNvvd2JPrByK9A6zLQEeEiu%2BOUQOfd51qfKsbxxYjR2lxSHxxN1MckhVuI1ghYmIZPE7ZH8RTk9MMN%2FxW79GUMsCB2%2Foy9%2FSplDQiHflZ1UIJqIhplmxLDsBy02sD8FA3VnLPA65jU6gN2B3bF8deYLn8D4AAJXe%2BB9Ww%3D%3D&Expires=1778043563) - The nowu framework does not need a major overhaul. Both Palantirs Ontology architecture and the Guo ...

7. [USE_CASES.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/16494219-33d0-4eb0-a477-d4d9fc4d4968/USE_CASES.md?AWSAccessKeyId=ASIA2F3EMEYE53TL3EMT&Signature=dP1aS6DpElwzk%2F9bqm8fYlfu%2FWk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEMz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJJNrdHEXYlbqokylFcPhmmcwgJscut37yRnPVht%2FPZgIhAKpIMc5X3mAVKLf5nwtIhiEQBRqQCM8zQpqZjJP7fTS9KvwECJX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1IgygpsZzwMb6us6ti28q0ASD1lgMu8LdhPi2dtMJeEpvId7qcz274iJZAzRAgJm2RIWVK1iCYOdkm2weQl8OkPkg9fJZWS9rf7FPiRJJMXIHRMMgkap9WwYUTHwNmZiXjIa3hui964zORgU4s1kO%2FCFdQCwuU7Ts4CTlQTNWsKfpcPqsLMyfWWJjTdtlqeZTDftw40Gjk8cEnfCgpKBIAi1sP85t2d%2BjCOwPtxCVZdrZGnHheCQBsXfD1RrKBluw21PVNzf5mGIZkIWdqoSyG%2FgN%2B%2Br6zuQg%2B42LTLOnd0zToQOgLqnPK92KM0CJ%2FBnXA45VA5fk6HwtU1ygrto50s1VKx5ugHsPKPnzUMwsOk4ouvOVQNxmOwvZx6axtCqRMrcZ23WwWkbA1ObYJ0KKAxd7%2BS%2BBKmhqSDdq9QDdZyBF3HWUGpIe1FMFFykzZjmgDbGfkMV2NY6Svo6EDGls87BGZ0Mfsurz7yCvqbqEXomvYjyA0KKRWJuwwDzs%2BaBLPpwpOrNOYqbe2EMr3AmxxU2%2FvkEkeWRTBJxvFz1x1VwdEyEZUexdsva0EueXDUKA7f5OG8DzGV%2BYWB2uWoBezGEGIjGsEFdxZfr2FWZWYW%2FfMzwdQSEa9T5dZIFaFkkhs%2F5qOvsrDEK9PR7i%2B9a3chRTI2XZ17emCzsOUVhTEahlHPDbBCAKtkAywmPQ4ilEYHEH7jcTC9xV2cTE9xvwp1qEPeP9RGQbbk2i1kSG2O%2B%2F4VHpKrR7Jgk1U8Tz98Je3FPbfmhfyP8fS14luwWJCkBsZkgUZmQmaLjEUIKIZF4dMNj56s8GOpcBlBkL7sMDZc6BgVvM0OxOJnk4zCezG%2Bff7llqrxNvvd2JPrByK9A6zLQEeEiu%2BOUQOfd51qfKsbxxYjR2lxSHxxN1MckhVuI1ghYmIZPE7ZH8RTk9MMN%2FxW79GUMsCB2%2Foy9%2FSplDQiHflZ1UIJqIhplmxLDsBy02sD8FA3VnLPA65jU6gN2B3bF8deYLn8D4AAJXe%2BB9Ww%3D%3D&Expires=1778043563) - --- version 2.2 generatedby use-case-agent2.2 generatedat 2026-04-06 basedonvision v2.0 approved 202...

8. [Architectural Fitness Functions: Building Effective Feedback ...](https://www.shapingshifts.com/p/architectural-fitness-functions-building) - How software development teams can use fitness functions to establish feedback loops and evaluate qu...

9. [Fitness Functions for Your Architecture - InfoQ](https://www.infoq.com/articles/fitness-functions-architecture/) - Fitness functions are guardrails that enable continuous evolution of your system's architecture, wit...

10. [Fitness Functions: Unit Tests For Your Architecture](https://trailheadtechnology.com/fitness-functions-unit-tests-for-your-architecture/) - How Fitness Functions Work. Fitness functions create a continuous feedback loop, providing software ...

11. [API Contract Evolution: Safely Changing APIs Over Time - Digital API](https://www.digitalapi.ai/blogs/api-contract-evolution-safely-changing-apis-over-time) - Evolve API contracts safely, maintaining trust and stability. Learn best practices for versioning, d...

12. [Formal Model of Contract Evolution for APIs and Messages in Event ...](https://ijecs.in/index.php/ijecs/article/view/5486) - The research explores in detail the mechanisms that support backward and forward compatibility, as w...

13. [ADRs, Trade-offs, and an ATAM-Lite Checklist](https://techcommunity.microsoft.com/blog/azurearchitectureblog/how-great-engineers-make-architectural-decisions-%E2%80%94-adrs-trade-offs-and-an-atam-l/4463013) - Without a shared framework, context fades and teams' re-debate old choices. ADRs solve that by recor...

14. [Architecture Decision Records (ADR): Enhancing Software ... - Habr](https://habr.com/en/articles/781624/) - ADRs have evolved from being part of extensive technical specifications to a more structured and cen...

15. [Breaking the Architecture Bottleneck | gotopia.tech](https://gotopia.tech/articles/392/breaking-the-architecture-bottleneck) - So an ADR is an architectural decision record. So a single decision which ... feedback loop, which i...

16. [Python: Sharing type annotations between Protocol and TypedDict](https://stackoverflow.com/questions/60348451/python-sharing-type-annotations-between-protocol-and-typeddict) - I'd like to know if there is a way that I can centrally define the type annotations and tell mypy th...

17. [Typed dictionaries — typing documentation - Static Typing with Python](https://typing.python.org/en/latest/spec/typeddict.html) - A TypedDict definition may also contain the following keyword arguments in the class definition: ......

18. [Python's TypedDict: Structure, Compatibility, and Trade-offs - YouTube](https://www.youtube.com/watch?v=UTUXpZy_4jA) - The source provides an extensive guide to Python's typing.TypedDict, which is a type hint used for s...

19. [PEP 728 – TypedDict with Typed Extra Items | peps.python.org](https://peps.python.org/pep-0728/) - This PEP adds two class parameters, closed and extra_items to type the extra items on a TypedDict. T...

