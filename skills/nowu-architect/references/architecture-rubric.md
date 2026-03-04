# nowu Architecture Rubric

Use this rubric to evaluate architecture options consistently.

## Scoring model

Score each criterion from 1 (poor) to 5 (excellent), then apply weights.

| Criterion | Weight | What high score means |
|---|---:|---|
| Delivery speed | 25 | Can be shipped quickly by solo + AI workflow |
| Reliability | 20 | Deterministic behavior, easy recovery, low hidden coupling |
| Modularity | 20 | Clear boundaries, isolated changes, easy extension |
| Operational simplicity | 15 | Low infra overhead, low run cost, easy local debugging |
| Governance/traceability | 20 | Decisions/audit paths are explicit and enforceable |

## Required checks

1. Does the option preserve `know` as the system-of-record memory layer?
2. Are module ownership boundaries explicit?
3. Can failures be detected and recovered without manual archaeology?
4. Can the option be executed in <=2 incremental slices?
5. Does it improve or preserve VBR and approval routing?

## Decision quality gate

Do not finalize an option unless:

- weighted score is documented
- at least one key risk is listed with mitigation
- migration impact on existing docs/contracts is listed

