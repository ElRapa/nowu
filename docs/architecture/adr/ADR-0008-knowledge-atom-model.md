---
id: ADR-0008
title: Knowledge Atom Model & Lifecycle
date: 2026-05-07
status: PROPOSED
epistemic_grade: HYPOTHESIS
superseded_by: ~
source_synthesis: SYNTHESIS-001
source_themes: [T2, T1, T4, T5, T8, T9]
source_ucs: [PK-01, PK-02, PK-04, PK-05, PK-06, PK-07, PK-09, XP-01, XP-03, XP-04, XP-05, XP-11, AP-01, AP-02, AP-04, RE-02, RE-05]
---

# ADR-0008: Knowledge Atom Model & Lifecycle

## Status

PROPOSED (HYPOTHESIS grade) — Derived from SYNTHESIS-001 Theme T2 (Knowledge Persistence
& Lifecycle). Will be validated through first S1-S9 intake (W4). Promoted to
INFORMED_ESTIMATE after 2+ intakes confirm or refine.

## Context

SYNTHESIS-001 identifies T2 (Knowledge Persistence & Lifecycle) as a critical theme
spanning 17+ use cases. Five other themes (T1: Continuity, T4: Epistemic Awareness,
T5: Domain Agnosticism, T8: Progressive Disclosure, T9: Audience-Aware Rendering) depend
on the knowledge model being defined. Without a canonical atom schema, those themes cannot
be resolved.

The `know` module (external sibling at `../know`) already implements a `KnowledgeAtom`
dataclass with type, grade, lifecycle, and relationship support. nowu accesses `know`
only through the `MemoryService` Protocol (ADR-0001). The architectural question is not
"what should the atom look like?" but "how does nowu adopt and extend the existing model
for its workflow needs?"

Simultaneously, D-001 (File-Based Memory) established file-based artifacts (Markdown +
YAML frontmatter) as the persistence layer for workflow state. The relationship between
file-based artifacts and knowledge atoms must be clarified.

## Decision

**The `know` module's `KnowledgeAtom` is the canonical knowledge unit for the entire
nowu ecosystem.** All structured knowledge — captured thoughts, decisions, facts, lessons,
domain data — is stored as atoms in the `know` module's per-project SQLite store.

Workflow artifacts (Markdown files in `state/`) remain the primary interface for agent
handoffs (per D-001 and ADR-0006). They are NOT atoms. Artifacts may reference atoms,
and significant artifact content may be promoted to atoms, but they serve different purposes:

| Concern | Workflow Artifacts (`state/`) | Knowledge Atoms (`know`) |
|---------|------------------------------|--------------------------|
| Purpose | Agent handoff, human review, audit trail | Durable knowledge, semantic recall, cross-project linking |
| Format | Markdown + YAML frontmatter | Structured dataclass (JSON + SQLite) |
| Lifecycle | DRAFT → APPROVED → consumed | active → verified → stale → archived/deleted |
| Scope | Single intake/task cycle | Persists across cycles and projects |
| Access | File read/write | `MemoryService` Protocol via `KnowAdapter` |

### Atom Schema (Adopted from `know`)

The canonical `KnowledgeAtom` fields (from `know/src/know/schema.py`):

**Identity & Type:**
- `id`: Unique identifier (UUID)
- `type`: `KnowledgeType` — one of: `decision`, `fact`, `concept`, `task`, `action`,
  `preference`, `lesson`, `reference`, `ephemeral`
- `title`: Human-readable title (required, non-empty)
- `content`: Full content body

**Epistemic Metadata (see ADR-0010):**
- `epistemic_grade`: `EpistemicGrade` enum — 5-level scale from `SPECULATION` (1) to
  `VERIFIED_FACT` (5). Default: `SPECULATION`.
- `epistemic_justification`: Required when grade >= `EVIDENCE_BASED` (4).
- `confidence`: Float 0.0–1.0, subjective certainty within grade band.

**Lifecycle:**
- `status`: `AtomStatus` — `active` | `archived` | `deleted`
- `decay_rate`: `DecayRate` — `fast` | `medium` | `slow`
- `created_at`, `updated_at`, `last_verified`, `last_accessed`: ISO timestamps
- `version`: Integer, incremented on update

**Scoping & Organization:**
- `project_scope`: List of project identifiers this atom belongs to
- `tags`: Free-form tags for categorization

**Relationships (via `Connection` dataclass):**
- `depends_on`, `supports`, `contradicts`, `refines`, `supersedes` (and others)
- Connections are first-class: typed, weighted, with metadata

### Lifecycle State Machine

```
                    ┌──────────────────────┐
                    │                      │
   create_atom()   ▼                      │
  ──────────────► ACTIVE ──── verify ────►│
                    │                      │
                    ├── decay threshold ──► STALE (status remains active,
                    │                      │       grade auto-downgrades)
                    │                      │
                    ├── archive ──────────► ARCHIVED
                    │                      │
                    └── delete ───────────► DELETED (soft; hard_delete for purge)
                                           │
                    ARCHIVED ── restore ──► ACTIVE
```

**Transitions:**
- **Create → Active**: Any module can create atoms via `MemoryService`. Default grade
  is `SPECULATION`. Async enrichment may run after creation (PK-01: capture without
  blocking).
- **Active → Stale**: Curator checks `last_verified` against `decay_rate` half-life.
  Stale atoms get grade auto-downgraded (e.g., `EVIDENCE_BASED` → `INFORMED_ESTIMATE`).
  See `know/src/know/curator.py`.
- **Stale → Active**: Re-verification by human or agent resets `last_verified` and
  may restore grade.
- **Active → Archived**: Manual or automated. Archived atoms are queryable but excluded
  from proactive surfacing.
- **Active → Deleted**: Soft delete by default. Hard delete available for purge.

### Cross-Project Scoping

- Each atom has a `project_scope` list identifying which projects can see it.
- Cross-project queries (XP-01: discovery across boundaries) are federated inside
  `know` — nowu modules never access another project's data directly.
- Project isolation is enforced per D-011 (per-project SQLite, from D-001 evolution).
  Cross-project recall uses `KnowAdapter.recall(cross_project=True)`.

### Domain Extensibility (T5)

The `KnowledgeType` enum is the extension point for domain-specific atoms. The current
set (`decision`, `fact`, `concept`, etc.) is framework-generic. Domain projects (AP, RE)
may need additional types (e.g., `regulation`, `property`, `formulation`).

**Hypothesis:** Domain-specific types are added via project configuration, not framework
code changes. The `know` module's `ontology.json` is the registry. This will be validated
during AP/RE domain dogfooding and formalized in ADR-0011 (Domain Extension Model).

## Rationale

1. **Reuse over reinvention** (D-006): `know` already implements the atom model with
   type, grade, lifecycle, relationships, and per-project SQLite. Building a separate
   model in nowu would violate D-006 and create two sources of truth.

2. **Separation of concerns**: Workflow artifacts serve agent handoffs (transient,
   step-scoped). Knowledge atoms serve durable memory (persistent, cross-cycle). Conflating
   them forces atoms to carry workflow metadata or artifacts to carry knowledge semantics.

3. **Foundation for 5 themes**: T1 needs atoms for session state. T4 needs atoms to carry
   grades. T5 needs atoms to be domain-extensible. T8 needs atoms to have maturity stages.
   T9 needs atoms as the storage layer separated from rendering.

## Consequences

**Positive:**
- Single canonical data type for all knowledge across all projects
- Existing `know` implementation provides immediate functionality (create, query, link,
  search, curator, decay) without new code
- Cross-project knowledge sharing has a defined mechanism (`project_scope` + federated queries)
- Epistemic grades are built into the atom, not bolted on

**Negative:**
- Workflow artifacts and atoms are separate concepts — agents must know when to create
  atoms from artifact content (promotion) and when to reference atoms in artifacts
- `know` module becomes a critical dependency — any schema change in `know` affects nowu
- Domain-specific types need a registration mechanism (deferred to ADR-0011)

**Neutral:**
- JSON is source of truth for atom persistence (DB is an index) — aligns with D-001's
  file-first philosophy
- The `MemoryService` Protocol in `core/contracts/memory.py` will need to be updated to
  expose the full `KnowledgeAtom` field set (currently a minimal surface)

## Artifact-to-Atom Extraction

Large structured artifacts (ADRs, SYNTHESIS, Architecture Vision) are NOT stored as atoms
directly. They remain as files — the source of truth. At acceptance or S9 capture, key
facts are extracted as individual atoms:

| Artifact Type | Extracts To | KnowledgeType | Example |
|---|---|---|---|
| ADR (accepted) | 2-5 atoms | `constraint`, `principle`, `rule` | "Session continuity requires two-layer checkpoints" |
| SYNTHESIS | 5-10 atoms | `concept`, `constraint` | "T2: knowledge lifecycle spans 17+ UCs" |
| Architecture Vision | 3-5 atoms | `principle`, `concept` | "Principle P2: artifacts are the interface" |
| S4 Decision | 1 atom | `decision` | "Chose Typer for CLI (rejected Click)" |
| S9 Capture | 1-3 atoms | `lesson`, `decision` | "VBR caught 3 type errors in module X" |

The S9 curator (`nowu-curator`) is the extraction point — it reads session artifacts,
identifies durable knowledge, and creates atoms via `MemoryService`. The full artifact
remains as a file; the atoms make its essence queryable and cross-referenceable across
projects.

**Key distinction:** Documents don't *become* atoms — they **produce** atoms. The document
is the narrative source of truth; the atoms are the queryable index into that narrative.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Adopt `know` KnowledgeAtom as canonical (recommended) | Existing implementation, tested, single source of truth | Dependency on external sibling module | **Selected** — D-006 already decided this |
| Build separate atom model in `core/contracts/` | Full control, no external dependency | Duplicates `know`, two atom schemas to maintain, violates D-006 | Contradicts D-006; maintenance burden |
| Merge artifacts and atoms into one concept | Simpler mental model, fewer concepts | Artifacts need workflow metadata (status, gates) that pollute knowledge semantics; atoms need lifecycle (decay, grades) that pollute workflow | Conflation creates a "god object" that does neither well |
| No formal atom model; ad-hoc knowledge storage | Fastest to start, no schema decisions | T2 theme (17+ UCs) becomes impossible; no confidence tracking, no decay, no cross-project linking | Fails the fundamental architectural requirement |

## Related

- synthesis: SYNTHESIS-001 (Theme T2)
- arch_vision: docs/architecture/ARCHITECTURE-VISION.md (Principle P1)
- decisions: D-001 (file-based memory), D-006 (know as external memory), D-011 (per-project SQLite)
- adrs: ADR-0001 (module boundaries — know access via Protocol only)
- depends_on: none (foundational)
- depended_on_by: ADR-0010 (grades live on atoms), ADR-0007 (session state uses atoms),
  ADR-0011 (domain types extend atoms), ADR-0014 (maturity stages on atoms),
  ADR-0015 (rendering reads atoms)
