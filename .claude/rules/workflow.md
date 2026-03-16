# Workflow Rules

## Delivery Loop (from WORKFLOW.md)
Every piece of work follows this sequence:
1. **Intake**: gather request, use-case IDs, affected modules
2. **Architecture analysis**: constraints, boundaries, failure modes
3. **Design options**: 2-3 approaches with tradeoffs
4. **Evaluation and decision**: score against criteria, record in DECISIONS.md
5. **Task shaping**: split into ≤4h tasks with acceptance criteria
6. **Implementation**: one shaped task at a time, TDD
7. **VBR**: run tests/lint/checks, compare to acceptance criteria
8. **Review**: architecture compliance, test quality, code standards
9. **Capture**: persist decisions/lessons/tasks to DECISIONS.md (later: `know`)

## Approval Tiers
- **Tier 1 (auto)**: docs edits, test additions, non-breaking internal refactors
- **Tier 2 (batch)**: feature additions in approved scope, dependency changes
- **Tier 3 (block)**: destructive migrations, architecture reversals, data integrity changes

## Task Sizing
- NEVER accept tasks > 8 hours — break them down
- Target ≤4 hours per implementation task
- Each task must have: scope, acceptance criteria, dependencies, test strategy

## Use-Case Traceability
- Every feature maps to one or more use-case IDs (NF-01, PK-03, etc.)
- Reference IDs in commit messages, task definitions, and test names
