
# Create comprehensive guidance document on docs placement and maintenance

guidance = """# Perplexity Research Outputs: Placement & Maintenance Strategy

**Date:** 2026-05-08  
**Context:** Where should Perplexity research reports live in nowu, and who maintains docs?

---

## Part 1: Where Perplexity Research Outputs Belong

### Current FILE-STRUCTURE.md Analysis

Your current structure has:
```
docs/
├── design/
│   ├── concepts/      ← Future concept docs — ideas ready for pre-workflow
│   └── research/      ← Research artifacts and analysis
```

**The `docs/research/` directory is the natural home** for Perplexity outputs. But it needs better internal structure.

### Recommended Structure: `docs/research/`

```
docs/research/
├── INDEX.md                           ← Master index: what research exists, when, why
├── sessions/                          ← Perplexity research session outputs
│   ├── 2026-05-06-architecture-analysis/
│   │   ├── report.md                  ← Main research report
│   │   ├── orchestrator-design.md     ← Deliverable designs/recommendations
│   │   ├── context-loading-strategy.md
│   │   └── META.md                    ← Session metadata (who requested, what prompted, what decisions traced from it)
│   ├── 2026-05-07-workflow-model-evaluation/
│   │   ├── report.md
│   │   ├── altitude-wording-analysis.md
│   │   └── META.md
│   └── 2026-05-08-docs-maintenance-strategy/
│       ├── report.md
│       └── META.md
├── comparative/                       ← Cross-tool/framework comparisons
│   ├── nowu-vs-palantir.md
│   ├── nowu-vs-guo-et-al.md
│   └── orchestrator-frameworks-comparison.md
├── literature/                        ← Academic papers, industry frameworks (curated subset)
│   ├── guo-et-al-2025-llm-agent-survey.pdf
│   ├── rombaut-2026-coding-agent-taxonomy.pdf
│   └── aflow-iclr-2025.pdf
└── validation/                        ← Post-implementation validation studies
    └── (empty until v1 dogfooding)
```

### Why This Structure

**`sessions/` by date:**
- Perplexity research is **time-bound** (asks a question, gets an answer, produces artifacts)
- Date-based folders prevent naming conflicts and provide natural chronology
- Each session folder is self-contained: report + deliverables + metadata
- Easy to grep: "What research informed ADR-0009?" → check `META.md` files for ADR references

**`comparative/`:**
- Cross-framework analyses that **aren't time-bound** (evergreen references)
- Updated when new information invalidates prior comparison
- Versioned if comparison changes significantly

**`literature/`:**
- **Curated subset only** — not a paper dump
- Papers that are **actively referenced** in nowu design decisions
- Must be cited in at least one ADR or DECISION to stay here

**`validation/`:**
- Post-implementation studies (e.g., "Did the orchestrator reduce context-loading errors?")
- Empty until v1 dogfooding starts

### The INDEX.md File

```markdown
# nowu Research Index

**Purpose:** Master catalog of research sessions, what they informed, and traceability to decisions.

---

## Active Research Sessions

| Date | Session | Key Question | Deliverables | Informed Decisions |
|---|---|---|---|
| 2026-05-06 | architecture-analysis | Is nowu's global architecture correct? | 3 architecture options, ATAM eval, recommendation | D-002, D-003, D-013..D-015 |
| 2026-05-07 | workflow-model-evaluation | How do nowu's workflows compare to SOTA? | 5-altitude model, 10 operators, wording analysis | (pending — roadmap formalization) |
| 2026-05-08 | docs-maintenance-strategy | Who maintains docs and how? | Maintenance responsibility matrix, update protocols | (pending — D-023) |

## Comparative Studies

| Study | Last Updated | Status | ADRs Informed |
|---|---|---|---|
| nowu-vs-palantir.md | 2026-05-06 | CURRENT | ADR-0008 (atom model) |
| nowu-vs-guo-et-al.md | 2026-05-06 | CURRENT | ADR-0006 (soul-flow coupling) |
| orchestrator-frameworks-comparison.md | 2026-05-07 | CURRENT | D-022 (orchestrator layer) |

## Literature (Actively Referenced)

| Paper | Year | Cited In |
|---|---|---|
| Guo et al. 2025 LLM Agent Survey | 2025 | ADR-0006, D-012, orchestrator design |
| Rombaut 2026 Coding Agent Taxonomy | 2026 | Workflow model evaluation |
| AFLOW (ICLR 2025) | 2025 | Orchestrator design, operator vocabulary |

## Validation Studies

(None yet — will populate after v1 dogfooding)

---

## How to Add New Research

1. Create session folder: `docs/research/sessions/YYYY-MM-DD-brief-topic/`
2. Add `report.md` (main Perplexity output)
3. Add deliverables (designs, strategies, recommendations)
4. Create `META.md` with:
   ```yaml
   ---
   date: YYYY-MM-DD
   session_id: YYYY-MM-DD-brief-topic
   requested_by: [human name or "orchestrator"]
   prompted_by: [what triggered the research need]
   key_question: [one sentence]
   deliverables: [list of .md files in this folder]
   status: ACTIVE | SUPERSEDED | ARCHIVED
   superseded_by: [if SUPERSEDED, link to newer session]
   informed_decisions: [list of D-NNN or ADR-NNN]
   ---
   ```
5. Update `docs/research/INDEX.md` with new row
6. If research informs a decision, **cite the session folder** in the ADR or DECISION entry:
   ```markdown
   ## D-023 — Documentation Maintenance Protocol
   
   **Date**: 2026-05-08 | **Status**: ACCEPTED | **Level**: system  
   **Intake**: docs/research/sessions/2026-05-08-docs-maintenance-strategy/
   ```

---

## When to Move Research to `comparative/` or `literature/`

**Move to `comparative/` when:**
- Research compares nowu to external frameworks/tools
- Comparison is **evergreen** (not tied to a specific decision moment)
- You expect to update it as nowu or the external tool evolves

**Move to `literature/` when:**
- A paper is cited in 2+ ADRs or decisions
- Paper is foundational to nowu's design (e.g., Guo et al. agent survey)

**Keep in `sessions/` when:**
- Research was time-bound (answered a specific question at a specific moment)
- Deliverables are implementation-ready (e.g., orchestrator agent definitions)
- Research is **not** a comparison (it's analysis of nowu itself)

---

## Archival Rules

**SUPERSEDED research:**
- Mark `status: SUPERSEDED` in `META.md`
- Add `superseded_by: sessions/YYYY-MM-DD-newer-session/` pointer
- Keep in `sessions/` folder (don't delete — it's part of decision lineage)
- Remove from "Active Research Sessions" table in INDEX.md

**ARCHIVED research:**
- Research that was exploratory but didn't inform any decisions
- Move to `docs/research/archive/` after 6 months
- Keep `META.md` so it's still searchable

**NEVER delete research** — decisions must be traceable to their evidence base.
```

---

## Part 2: Documentation Maintenance — Who, When, How

### The Problem (Research-Validated)

**Documentation decay** is the #1 cause of technical debt in agile systems[cite:841][cite:848]. The literature identifies three failure modes:

1. **Documentation as homework** — separated from workflow, updated "later" (never)[cite:841]
2. **No clear ownership** — "everyone's responsible" = nobody's responsible[cite:837][cite:842]
3. **Stale without detection** — no automated validation that docs match reality[cite:843][cite:848]

### Five Maintenance Strategies (SOTA Synthesis)

#### Strategy 1: Living Documentation (Agile/DevOps Standard)[cite:841][cite:846][cite:848]

**Principle:** Documentation is a living artifact that evolves alongside the project, not a one-time upfront effort.

**How it works:**
- **Co-location:** Docs live in the same repo as code, updated in the same commits[cite:843]
- **Automation:** API docs, schema docs, and config references are auto-generated from code/infra[cite:843][cite:846]
- **Validation:** CI/CD fails if docs are incomplete or incorrect[cite:843][cite:848]
- **Continuous verification:** Docs are checked against code state on every commit[cite:848]

**Example from research:**[cite:843]
```yaml
# Pull Request Checklist
- [ ] Code changes tested
- [ ] Documentation updated to reflect changes
- [ ] OpenAPI spec regenerated if endpoints changed
```

**nowu translation:**
- `docs/architecture/containers.md` updated when `src/` module boundaries change
- `docs/WORKFLOW-DETAILED.md` updated when S1-S9 agent prompts change
- `docs/DECISIONS.md` updated when S4 (decider) or G2 (gap-writer) record new decisions

#### Strategy 2: Documentation Champions (Rotating Ownership)[cite:841]

**Principle:** "Everyone's responsible" fails. Assign explicit, rotating ownership.

**How it works:**
- **Rotating champions:** Each sprint/cycle, one person is the "documentation champion"[cite:841]
- **Not a writer** — a curator who reviews, prunes, and flags stale docs[cite:841][cite:845]
- **Rotation prevents burnout** and spreads knowledge[cite:841]

**nowu translation:**
- In a human+AI workflow, **the human is the documentation champion** for each cycle
- AI agents **propose** updates; human **curates** and **approves**
- In a future fully-AI workflow, the orchestrator assigns a meta-agent as champion per roadmap stage

#### Strategy 3: Documentation in Definition of Done[cite:837][cite:850]

**Principle:** No work is complete until documentation is updated.

**How it works:**
- Every task, story, or ADR has "update docs" as a **mandatory** completion criterion[cite:837][cite:850]
- The reviewer (S8 in nowu) checks doc updates before approving work[cite:837]

**nowu translation:**
- **S5 (shaper):** Every task spec must declare which docs it will update (if any)
- **S8 (reviewer):** VBR checklist includes "docs updated as declared in task spec"[cite:837]
- **S9 (curator):** Writes session learnings + updates `docs/PROGRESS.md` (already in your model)

#### Strategy 4: Scheduled Audits (Quarterly/Bi-annual)[cite:837][cite:841][cite:842]

**Principle:** Even with living docs, entropy accumulates. Schedule deep reviews.

**How it works:**
- **Quarterly audits:** Prune duplicate pages, merge outdated decisions, archive dead context[cite:841]
- **Track usage metrics:** Which pages get referenced? Where do readers drop off?[cite:841]
- **Subject-matter expert reviews:** Domain experts validate technical accuracy[cite:837][cite:842]

**nowu translation:**
- **G0 (pattern detection):** Should flag documentation drift as a health metric[cite:841]
- **Quarterly roadmap review:** When `roadmap-updater` runs after stage gates, audit docs for staleness
- **Explicit audit task:** Add to ROADMAP-003.md: "Q4: Documentation audit + pruning"

#### Strategy 5: Automated Staleness Detection[cite:841][cite:843]

**Principle:** Humans forget to update docs. Bots never forget to nag.

**How it works:**
- **Automated reminders:** Scripts ping doc owners when sections go untouched for X days[cite:841]
- **CI/CD validation:** Build fails if docs reference non-existent files or outdated config[cite:843]
- **Git hooks:** Pre-commit checks verify doc changes accompany code changes in certain paths[cite:843]

**nowu translation:**
- **G1 (drift analysis):** Should detect when `docs/` artifacts are stale relative to `state/` or `src/`[cite:841]
- **S8 (reviewer):** Can run a lint check: "Does this task change module boundaries? If yes, is containers.md updated?"[cite:843]
- **Future v1.1:** `work-scheduler` queries "last updated" timestamps and flags stale docs before starting work

---

## Part 3: nowu-Specific Maintenance Responsibility Matrix

### Artifact-Level Ownership

| Artifact | Owner Agent | Update Trigger | Validation | Grade Progression |
|---|---|---|---|---|
| **`vision.md`** | Human (agent-assisted) | P0.V, annual review | health-vision | INFORMED_ESTIMATE (stable) |
| **`USE_CASES.md`** | Human + use-case-agent | P0.UC, new UC discovery | health-use-cases | EVIDENCE_BASED (validated) |
| **`DECISIONS.md`** | S4 (decider), G2 (gap-writer) | Every S4 decision, every G2 lesson | S2, S5, S8 reference checks | EVIDENCE_BASED (binding) |
| **`ROADMAP-NNN.md`** | roadmap-creator, roadmap-updater | SYNTHESIS, Arch Vision, stage gates | work-scheduler (queries for consistency) | HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED |
| **`containers.md`** | P3.2 (arch-bootstrap), S2 (constraints) | Module boundary changes, new modules | health-architecture | EVIDENCE_BASED (binding) |
| **`ADR-NNN.md`** | hypothesis-adr-writer, P3.3 | Architecture decisions | fitness-function tests | HYPOTHESIS → INFORMED_ESTIMATE → ACCEPTED |
| **`WORKFLOW-DETAILED.md`** | Human (infrequent), session-learning | Agent prompt changes, step clarifications | health-sweep (manual) | EVIDENCE_BASED (stable) |
| **`MODEL-REFERENCE.md`** | Human (infrequent), orchestrator (when model evolves) | Major workflow model changes | No automated check (foundational doc) | EVIDENCE_BASED (stable) |
| **`PROGRESS.md`** | S9 (curator) | Every S9 cycle closure | None (audit trail) | EVIDENCE_BASED (log) |
| **`research/INDEX.md`** | Human (manual), future: documentation-champion-agent | After each research session | None (catalog) | N/A (always current by definition) |

### Update Frequency by Altitude

| Altitude | Docs in Scope | Update Frequency | Responsible Agent/Role |
|---|---|---|---|
| **STRATEGIC** | vision.md, goals/, ROADMAP-NNN.md | Quarterly (or after major milestone) | roadmap-updater, human |
| **PRODUCT** | USE_CASES.md | Per-UC (P0.UC), batch updates monthly | use-case-agent, human |
| **ARCHITECTURE** | containers.md, ADRs, SYNTHESIS, Arch Vision | Per-decision (S4), per-arch-pass (P3.2) | S4, P3.2, hypothesis-adr-writer |
| **DELIVERY** | WORKFLOW-DETAILED.md, task specs | Rare (only when step logic changes) | session-learning (proposes), human (approves) |
| **EXECUTION** | src/ code, tests/ | Every S6 implementation | S6 (implementer) |
| **RETROSPECTIVE** | PROGRESS.md, health/, learnings/ | Every S9, every GAP cycle | S9 (curator), G0/G1/G2 |

---

## Part 4: Concrete Maintenance Protocols for nowu

### Protocol 1: The LEARN Phase Update Rule

**Rule:** Every altitude's LEARN phase is responsible for updating docs at that altitude.

| Altitude | LEARN Phase | Updates | Output Location |
|---|---|---|---|
| STRATEGIC | roadmap-updater (after milestones) | ROADMAP-NNN.md, vision.md (if drift detected) | `docs/` |
| PRODUCT | P0.UC (use-case-agent) | USE_CASES.md | `docs/` |
| ARCHITECTURE | S4 (decider) | DECISIONS.md, ADRs (if S4 makes an arch decision) | `docs/`, `docs/architecture/adr/` |
| DELIVERY | S9 (curator) | PROGRESS.md, session learnings | `docs/`, `state/learnings/` |
| RETROSPECTIVE | G2 (gap-writer) | Health reports, GAP outputs, DECISIONS.md (lessons) | `state/health/`, `docs/DECISIONS.md` |

**Implementation:**
- Each altitude's LEARN phase agent has **explicit instructions** to update canonical docs
- S9 (curator) updates both `PROGRESS.md` and `state/learnings/INDEX.md`[cite:837]
- G2 (gap-writer) writes to `DECISIONS.md` when lessons are architectural/binding[cite:841]

### Protocol 2: The S8 Documentation Validation Gate

**Rule:** S8 (reviewer) validates that docs were updated as declared in S5 (task spec).

**S5 (shaper) template addition:**
```yaml
---
task_id: task-NNN
title: [...]
docs_to_update:
  - docs/DECISIONS.md (if this task makes a binding decision)
  - docs/architecture/containers.md (if this task changes module boundaries)
  - None (if this task is purely implementation with no doc impact)
---
```

**S8 (reviewer) checklist addition:**[cite:837]
```markdown
## Documentation Validation
- [ ] All docs declared in `docs_to_update` are modified in this changeset
- [ ] If `docs_to_update: None`, confirm no binding decisions or module changes were made
- [ ] If new ADR was created, it is referenced in DECISIONS.md
```

### Protocol 3: The G0 Documentation Drift Metric

**Rule:** G0 (pattern detection) flags stale docs as a health risk.

**G0 enhancement:**
- Check `git log` for docs/ files: which haven't been updated in 90+ days?[cite:841]
- Cross-reference against `state/` activity: if `state/arch/` has new content but `docs/architecture/containers.md` is stale, flag drift
- Output: "Documentation drift detected: `containers.md` last updated 120 days ago but 8 new ADRs created since then"[cite:841]

**G1 (drift analysis) enhancement:**
- Deep-read stale docs and compare to recent `state/` artifacts
- Output: "Drift analysis: `containers.md` still shows 4 modules but ADR-0002 added `soul` as 5th module"[cite:841]

**G2 (gap-writer) enhancement:**
- Propose doc updates to close drift gaps
- Write to `state/health/doc-drift-YYYY-MM-DD.md` with recommended updates

### Protocol 4: The Quarterly Documentation Audit (Roadmap Stage Gates)

**Rule:** When `roadmap-updater` runs after a stage gate (v1-core → v1, v1 → v1.1), trigger a doc audit.

**Audit checklist:**[cite:837][cite:841]
1. **Prune duplicates:** Are there multiple docs saying the same thing? Merge or delete.
2. **Archive dead context:** Are there docs referencing v0 concepts that no longer exist? Move to `archive/`.
3. **Update grade progression:** Docs that started as HYPOTHESIS but are now validated → promote to EVIDENCE_BASED.
4. **Check landmark freshness:** Are the 5 landmark files (vision, UCs, containers, DECISIONS, intake) current?[cite:837]

**Implementation:**
- Add to `roadmap-updater` agent prompt:
  ```markdown
  ## Step 4 (Stage Gate Passage): Documentation Audit
  
  When updating the roadmap after a stage gate, perform a documentation audit:
  1. List all docs in `docs/` modified in the last 90 days
  2. Flag docs NOT modified in 90+ days for human review
  3. Check landmark files (vision, USE_CASES, containers, DECISIONS) — when were they last updated?
  4. Output audit summary in ROADMAP-NNN+1.md Section 8 "Documentation Health"
  ```

### Protocol 5: The Research Session Integration Rule

**Rule:** When Perplexity research informs a decision, the decision MUST cite the research session.

**Example:**[cite:841]
```markdown
## D-023 — Documentation Maintenance Protocol

**Date**: 2026-05-08 | **Status**: ACCEPTED | **Level**: system  
**Intake**: docs/research/sessions/2026-05-08-docs-maintenance-strategy/

### Context

Documentation decay is the #1 cause of technical debt in agile systems (research 
synthesis from 10 industry sources). The nowu workflow model has LEARN phases at 
every altitude but lacks explicit doc maintenance protocols.

**Evidence base:** docs/research/sessions/2026-05-08-docs-maintenance-strategy/report.md

### Decision

Implement 5 maintenance protocols:
1. LEARN phase update rule (every altitude's LEARN phase updates docs at that altitude)
2. S8 documentation validation gate (docs_to_update in S5 task spec)
3. G0 documentation drift metric (stale doc detection)
4. Quarterly documentation audit (triggered by roadmap stage gates)
5. Research session integration rule (decisions cite research evidence)
```

---

## Part 5: Implementation Roadmap

### Immediate (W4 — First S1-S9 Intake)
- [ ] Create `docs/research/INDEX.md` with current sessions
- [ ] Move Perplexity outputs to `docs/research/sessions/YYYY-MM-DD-*/`
- [ ] Add `META.md` to each session folder
- [ ] Add `docs_to_update` field to S5 (shaper) template
- [ ] Add "Documentation Validation" section to S8 (reviewer) checklist

### v1 (After Telegram Adapter + 5 UCs Dogfooded)
- [ ] Enhance G0 (pattern detection) with stale doc detection
- [ ] Enhance G1 (drift analysis) with doc-vs-state comparison
- [ ] Add "Documentation Health" section to `roadmap-updater` output

### v1.1 (Cross-Project Federation)
- [ ] Automated staleness detection: `work-scheduler` checks doc timestamps before starting work
- [ ] CI/CD validation: Pre-commit hooks verify doc changes accompany relevant code changes
- [ ] Documentation champion rotation: If multi-user, rotate quarterly; if single-user+AI, orchestrator assigns meta-agent

### v2 (Platform for External Use)
- [ ] Auto-generated docs: API references from docstrings, schema docs from Pydantic models
- [ ] Usage metrics: Track which docs are accessed, flag never-accessed docs for archival
- [ ] Living documentation pipeline: Docs updated on every commit, validated in CI/CD

---

## Summary Answers to Your Questions

### "Where should Perplexity research outputs live?"

**`docs/research/sessions/YYYY-MM-DD-topic/`** with:
- `report.md` (main research output)
- Deliverable files (designs, strategies, recommendations)
- `META.md` (session metadata, traceability to decisions)
- `INDEX.md` at `docs/research/` level as master catalog

**Why:** Time-bound research is naturally organized by date. Sessions are self-contained, traceable, and searchable.

### "Should all agents be responsible for docs maintenance?"

**No.** "Everyone's responsible" = nobody's responsible.[cite:837][cite:842]

**Instead:** Explicit per-altitude ownership:
- **STRATEGIC:** `roadmap-updater` updates `ROADMAP-NNN.md` after milestones
- **PRODUCT:** `use-case-agent` updates `USE_CASES.md` per-UC
- **ARCHITECTURE:** S4 (decider) updates `DECISIONS.md`, P3.2 updates `containers.md`
- **DELIVERY:** S9 (curator) updates `PROGRESS.md` and session learnings
- **RETROSPECTIVE:** G2 (gap-writer) updates health reports and proposes doc drift fixes

**Plus:** S8 (reviewer) validates docs were updated as declared in S5 task spec.[cite:837][cite:850]

### "Should doc updates be part of the LEARN step on each altitude?"

**Yes.** This is the cleanest pattern.[cite:841][cite:846]

- STRATEGIC altitude LEARN = `roadmap-updater` → updates `ROADMAP-NNN.md`
- ARCHITECTURE altitude LEARN = S4 (decider) + S9 (curator) → updates `DECISIONS.md`
- RETROSPECTIVE altitude LEARN = G2 (gap-writer) → updates health reports + proposes doc drift fixes

**Plus quarterly audits** triggered by roadmap stage gates (v1-core → v1, etc.).[cite:837][cite:841]

### "What does research say?"

**Living documentation** (co-located, automated, validated in CI/CD) is the industry standard for preventing doc decay.[cite:841][cite:846][cite:848]

**Key practices:**[cite:837][cite:841][cite:843]
1. Update docs in the same commit as code/decisions (co-location)
2. Auto-generate where possible (API docs, schema docs, config references)
3. Validate in CI/CD (build fails if docs are incomplete)
4. Explicit ownership (rotating champions or per-step agents)
5. Scheduled audits (quarterly pruning + grade progression)
6. Continuous verification (docs checked against reality on every commit)

### "How do I best implement it?"

**Phase 1 (Immediate — W4):**
- Add `docs_to_update` to S5 template
- Add "Documentation Validation" to S8 checklist
- Create `docs/research/INDEX.md` and migrate Perplexity outputs

**Phase 2 (v1 — After Dogfooding):**
- Enhance G0/G1 with stale doc detection
- Add "Documentation Health" to `roadmap-updater` output

**Phase 3 (v1.1+):**
- Automated staleness detection in `work-scheduler`
- CI/CD hooks for doc validation
- Auto-generated docs from code

**This gives you:**
- ✅ Clear ownership (LEARN phases update docs at their altitude)
- ✅ Validation gates (S8 checks docs were updated)
- ✅ Drift detection (G0/G1 flag stale docs)
- ✅ Quarterly audits (triggered by roadmap stage gates)
- ✅ Traceability (research sessions cited in decisions)
"""

with open("docs-placement-and-maintenance-guide.md", "w") as f:
    f.write(guidance)

print("✅ Created comprehensive docs maintenance guide")
print("\n📋 Key Recommendations:")
print("   1. Location: docs/research/sessions/YYYY-MM-DD-topic/")
print("   2. Ownership: LEARN phases update docs at their altitude")
print("   3. Validation: S8 checks docs were updated (S5 declares intent)")
print("   4. Drift detection: G0/G1 flag stale docs, G2 proposes fixes")
print("   5. Quarterly audits: Triggered by roadmap stage gates")
