# Idea: The nowu Octahedron — Global Product Model

> Status: FORMALISED in docs/GLOBAL-MODEL.md
> Origin: Conversation 2026-03-15

## Core Insight
Software is abstract and "flat" (literally 2-dimensional text files). This
makes it hard for builders to see progress or feel the weight of what they've
made — unlike a house, where the builder can stand back and say "I built that."

The Octahedron provides a 3D mental model that grows visibly as software
materialises. The lower pyramid fills in layer by layer with each completed
task, creating a tangible representation of progress.

## The Shape
Upper diamond (WHY) + Decision Equator + Lower pyramid (WHAT) = Octahedron.
In 3D: a true geometric octahedron where the equator is the widest cross-section.

## The WHY Problem
The CPG Pyramid only shows the implementation (WHAT). It has no "why".
The Double Diamond (Design Council, 2005) fills this gap: it models the
problem space as diverge→converge before the solution space begins.

Combined: Vision (upper apex) → use cases → requirements → decisions (equator)
→ system → modules → components → code (lower apex).

## Decision Level Filtering
Every decision has a `level` field: product | system | module | component | code.
This places it precisely on the equator and enables:
- Filtering: "show me all module-level decisions"
- Impact tracing: "this code decision connects to which system decision?"
- Gap detection: "there's a code implementation with no module-level decision upstream"

## Time as a Dimension
The pyramid fills in over time. Each S9 Capture updates the fill-in tracker.
Sprint 1: only L2 (module map). Sprint 5: L3 (contracts). Sprint 10: L4 (code).
Visualising the tracker gives the builder the "house under construction" feeling.

## Future: Interactive Octahedron
When `know` is operational, generate the octahedron as a queryable graph:
- Upper atoms: VISION, USE_CASE, REQUIREMENT, FEATURE_IDEA
- Equator atoms: DECISION (with level field)
- Lower atoms: SYSTEM, MODULE, COMPONENT, FUNCTION, TEST
- Edges: DRIVES (WHY→WHAT), IMPLEMENTS (WHAT→WHAT), TESTS (test→code)
Visualise with D3.js or similar — a live, interactive project map.


## linked files
- docs/archive/GLOBAL-MODEL.md
