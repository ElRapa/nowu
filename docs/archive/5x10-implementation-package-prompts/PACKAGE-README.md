# nowu 5x10 Implementation Package v1.1

**Version:** 1.1  
**Date:** 2026-05-05  
**Status:** READY FOR IMPLEMENTATION

Complete implementation guide for the 5-altitude x 10-phase workflow model.

---

## Package Structure

```
nowu-5x10-implementation-package/
├── docs/
│   ├── MODEL-REFERENCE.md          ← THE model spec (altitudes, phases, mappings, agents)
│   ├── IMPLEMENTATION-GUIDE.md     ← What to build, in what order
│   └── VERIFICATION-GUIDE.md       ← How to verify correctness (4 levels)
├── prompts/
│   ├── 00-OMO-MASTER-PROMPT-v1.1.md   ← Package 1: metadata foundation
│   ├── 01-package-2-agent-definitions.md  ← Package 2: phase agents
│   └── 02-package-3-runtime.md     ← Package 3: circuit breaker
├── templates/
│   ├── ARTIFACT-TEMPLATE.md        ← Knowledge + workflow phase frontmatter
│   ├── GOAL-template.md            ← Strategic goal template
│   └── agent-definition-template.md ← Phase operator agent template
├── examples/
│   ├── GOAL-001-example.md         ← Worked strategic goal
│   ├── SYNTHESIS-001-example.md    ← Worked cross-cutting analysis
│   └── OPTIONS-architecture-example.md ← Worked OPTIONS at ARCHITECTURE
├── standards/
│   └── WORKFLOW-STANDARDS-v1.1.md  ← Binding rules (ratified)
└── verification/
    └── verify-artifact.py          ← Level 0 automated syntax checker
```

---

## Quick Start

1. **Understand the model**: Read `docs/MODEL-REFERENCE.md`
2. **Plan implementation**: Read `docs/IMPLEMENTATION-GUIDE.md`
3. **Run Package 1**: Use `prompts/00-OMO-MASTER-PROMPT-v1.1.md` with your AI agent
4. **Verify**: Use `docs/VERIFICATION-GUIDE.md` + `verification/verify-artifact.py`
5. **Human review**: Check 5-10 artifacts, approve SYNTHESIS-001.md

---

## The 3 Reference Docs

| Document | Purpose | Read When |
|---|---|---|
| `MODEL-REFERENCE.md` | Complete 5x10 model: altitudes, phases, grades, S1-S9 zigzag, P0-P4, GAP, agent contracts, promotion rules | Understanding the model |
| `IMPLEMENTATION-GUIDE.md` | 3 packages, artifact storage, metadata schema, inference rules, success criteria | Building it |
| `VERIFICATION-GUIDE.md` | 4 verification levels, altitude/phase checklists, security integration, automated script | Checking correctness |

---

## Key Model Facts

- **5 altitudes**: STRATEGIC > PRODUCT > ARCHITECTURE > DELIVERY > EXECUTION
- **10 phases**: IDEA > PROBLEM > ANALYSIS > SYNTHESIS > OPTIONS > DECISION > EVALUATION > IMPLEMENTATION > VERIFICATION > LEARN
- **S1-S9 zigzags across altitudes**: S1=DELIVERY, S2-S4=ARCHITECTURE, S5=DELIVERY, S6-S8=EXECUTION, S9=EXECUTION->ALL
- **Phases are cognitive modes**: IMPLEMENTATION works at ARCHITECTURE, DELIVERY, and EXECUTION (not locked to one altitude)
- **SYNTHESIS** is the only altitude-locked phase (ARCHITECTURE only, triggered when >=2 approved UCs exist)
- **Epistemic grades are tiered**: HYPOTHESIS minimum at STRATEGIC creation, EVIDENCE_BASED aspirational at decision

---

## Concept Foundation

This package implements the design from `.sisyphus/drafts/idea-004-2d-altitude-phase-model.md`, validated by Guo et al. 2025, Rombaut 2026, AFLOW (ICLR 2025), Shape Up, and Anthony 1965.
