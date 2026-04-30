# The nowu Octahedron — Global Product Model

> This model is motivational and navigational. It answers: "Where are we?
> What are we looking at? What have we already built?"

## Concept

The Octahedron combines two complementary models:

**Upper Diamond (WHY)** — the problem space
Borrowed from the Double Diamond design process (Design Council, 2005).
Starts at the vision (single point), diverges through use cases and ideas,
then converges through requirements and decisions.

**Lower Pyramid (WHAT)** — the solution space
Borrowed from the C4 Model (Simon Brown). Starts at the decision equator
and materialises through system, modules, components, down to code.

**Equator (DECISIONS)** — the translation layer
Every architectural decision sits on the equator. It connects WHY (what use
case drove this) to WHAT (which C4 layer it affects). The `level` field on
every D-NNN entry places it precisely: product | system | module | component | code

## The Shape

```
        ▲  Vision (single point — the "why" apex)
       ╱│╲
      ╱ │ ╲  Discover: user research, pain points, opportunities
     ╱  │  ╲
    ──────────  Define: use cases, personas, problem statements
     ╲  │  ╱
      ╲ │ ╱  Develop: feature ideas, capability options
       ╲│╱
    ════════  DECISION EQUATOR (D-NNN entries with level field)
       ╱│╲
      ╱ │ ╲  C4 L1: System Context (actors, boundaries)
     ╱  │  ╲
    ──────────  C4 L2: Container / Module Map
     ╲  │  ╱
      ╲ │ ╱  C4 L3: Component (contracts, file structure)
       ╲│╱
        ▼  C4 L4: Code (the lower apex — most materialised)
```

## How It Fills In Over Time

The lower pyramid materialises with every completed task. After each S9 Capture:
- A new module boundary is confirmed (L2 fills in)
- New contracts are written (L3 fills in)
- New tests and code exist (L4 fills in)

This is the "house builder" effect: you can see what you've built.
The lower pyramid grows denser and more defined sprint by sprint.

## Decision Level Mapping

| Decision Level | Octahedron Position | Example |
|---------------|---------------------|---------|
| product | Upper diamond (wide) | "We build for solo developers first" |
| system | Upper→Equator | "We use file-based memory, not a database" |
| module | Equator | "know depends only on core" |
| component | Equator→Lower | "SessionOrchestrator implements FlowProtocol" |
| code | Lower pyramid | "Use dataclasses not Pydantic for domain models" |

## Workflow Mapping

| Workflow Steps | Octahedron Zone | Mode |
|---------------|-----------------|------|
| S1 Intake | Upper diamond (discover/define) | Divergent |
| S2-S3 Constraints+Options | Approaching equator | Convergent |
| S4 Decision | The equator itself | Decision point |
| S5 Shaping | Top of lower pyramid (L3) | Materialising |
| S6-S7 Implement+VBR | Lower pyramid (L4) | Building |
| S8-S9 Review+Capture | Whole pyramid check + equator update | Validating |

## C4 vs CPG: Which to Use

| Need | Use | Why |
|------|-----|-----|
| Explain architecture to humans | C4 (L1-L4 diagrams) | Human-readable, 4 zoom levels |
| Enforce import boundaries | AST-based arch test | Practical, runs in pytest today |
| Query code structure at scale | CPG (future, via `know`) | Machine-queryable supergraph |
| Motivational progress model | C4 pyramid filling in | Visible materialisation over time |

C4 is the primary model for nowu today. CPG is the future state of `know`.
They do not contradict — C4 is for communication, CPG is for analysis.
