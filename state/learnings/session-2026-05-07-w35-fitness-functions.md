---
artifact_type: SESSION_LEARNINGS
session: "W3.5 — Fitness Functions + ADR Refinements from Reviews #2 and #3"
created_at: 2026-05-07
session_type: "architecture"
source_artifacts:
  - tests/architecture/test_adr_fitness.py
  - tests/conftest.py
  - .claude/agents/hypothesis-adr-writer.md
  - .claude/agents/fitness-function-writer.md
  - docs/architecture/adr/ADR-0007-session-continuity-protocol.md (Known Limitations added)
  - docs/architecture/adr/ADR-0008-knowledge-atom-model.md (Artifact-to-Atom Extraction added)
  - state/learnings/session-2026-05-07-w3-hypothesis-adrs.md (addenda #2 and #3 added)
  - state/arch/2026-05-07_2_perplexity_review_W3.md
  - state/arch/2026-05-07_3_perplexity+human_review_ADRs.md
purpose: "Fitness function execution, ADR refinements from two Perplexity reviews, agent creation for W3 and W3.5"
---

# Session Learnings: W3.5 — Fitness Functions + ADR Refinements

## What Was Done

- Evaluated two Perplexity reviews (review #2: W3 output evaluation; review #3: architectural questions)
- Applied review #3 refinements: ADR-0007 "Known Limitations" section (multi-session gap), ADR-0008 "Artifact-to-Atom Extraction" section
- Review #2 gaps all turned out to be false positives — ADRs already had the referenced elements
- Created two agent definitions: `hypothesis-adr-writer.md` (W3) and `fitness-function-writer.md` (W3.5)
- Wrote W3.5 fitness tests: `tests/architecture/test_adr_fitness.py` (10 tests across ADR-0007, 0008, 0010)
- Fixed `tests/conftest.py` to resolve know package path issue (iCloud path-with-spaces bug)
- Quality suite: 12 tests pass, mypy --strict clean, ruff clean

## Decisions Made

### D-SESS-04: Fitness functions skip rather than fail when know is unavailable

**Decision:** Tests that require `know.schema` use `self.skipTest()` when the import
fails, rather than raising an ImportError that fails the test run.

**Context:** The `know` package is an editable sibling dependency. In clean environments
where `uv sync` hasn't been run, the import fails. A skip is more informative than a
failure — it signals "this test needs setup" rather than "the architecture is violated."

**Why it matters:** Keeps the test suite runnable in environments without know installed,
while preserving the intent (when know IS available, the structural properties are verified).

---

### D-SESS-05: conftest.py is the right place for editable dependency path workarounds

**Decision:** Added `tests/conftest.py` to add the know/src path to sys.path, working
around the iCloud path-with-spaces bug where .pth files aren't processed.

**Context:** The `know` package is installed as an editable dependency via a .pth file.
Paths containing spaces (iCloud's "Mobile Documents" directory) cause the .pth file to
be silently skipped by Python's site module, making `import know` fail even though
`uv pip list` shows it as installed.

**Why it matters:** Without the conftest fix, 4 of 10 architecture tests would be
skipped even in a properly configured environment. The fix is self-documenting (docstring
explains the root cause) and isolated to the test infrastructure.

---

## Process Insights

### Insight 1: Perplexity "gap" findings based on truncated context are unreliable for detail checks

**Observation:** Review #2 identified 4 "minor gaps" in the ADRs — all were false positives.
The reviewer was searching file snippets rather than reading full files. Every gap it
identified (missing frontmatter keys, missing cross-refs, truncated file, missing backlinks)
already existed in the full files.

**Type:** workflow-process

**Implication:** Perplexity reviews are reliable for structural assessment (overall
architecture validity, dependency ordering) but unreliable for detail verification (specific
fields present, exact cross-references). Always verify detail claims against full file
content before acting on them.

---

### Insight 2: Architecture tests as documentation of ADR requirements

**Observation:** Writing the fitness tests forced explicit enumeration of which ADR fields
are "required" vs. "optional." For ADR-0008, this meant choosing 9 key fields from 23
total KnowledgeAtom fields. That selection IS the fitness function specification — it
captures what the ADR says is non-negotiable.

**Type:** workflow-process

**Implication:** Fitness functions are not just tests — they're machine-readable
documentation of ADR requirements. When refining ADR-0008 from HYPOTHESIS to
INFORMED_ESTIMATE, check whether the 9 required fields still match the refined spec.

---

### Insight 3: iCloud path-with-spaces breaks Python .pth editable installs silently

**Observation:** The `know` package was correctly installed as an editable dependency
(`uv pip list` confirmed it, `.pth` file existed), but `import know` failed. Root cause:
Python's `site` module doesn't process `.pth` entries containing spaces correctly on some
configurations. This affected only the test runner — direct `uv run python` with path
injection worked fine.

**Type:** tooling

**Implication:** For any project living in iCloud Drive (or any path with spaces), editable
sibling packages may silently fail to be importable. Add a `conftest.py` path injection
as a standard workaround. Document it clearly — future developers will be confused by
"it's installed but can't import."

---

### Insight 4: "Known Limitations" sections in hypothesis ADRs are better than silence

**Observation:** ADR-0007 assumed single-session usage without stating it. When the human
asked about multi-session support, the gap was obvious in hindsight. Adding an explicit
"Known Limitations" section listing v1-core simplifications turns implicit constraints
into visible refinement candidates.

**Type:** workflow-process

**Implication:** Every hypothesis ADR should end with a "Known Limitations" section.
Each limitation is a named item in the v1 refinement backlog. This prevents future readers
from assuming HYPOTHESIS coverage is complete, and gives the next reviewer a checklist
of things to validate or extend.

---

## Anti-Patterns Observed

### Anti-Pattern 1: Acting on Perplexity gap findings without verification

**Temptation:** "The reviewer said ADR-0009 is missing the ADR-0006 cross-reference —
let me add it right away."

**Reality:** All 4 identified gaps were false positives. Acting without verification would
have added duplicate content to files that already had the referenced elements. Always
verify by reading the full file, not just the snippet the reviewer cited.

### Anti-Pattern 2: Test failures vs. test skips for optional dependencies

**Temptation:** "If know isn't importable, the test should FAIL — that's a real problem."

**Reality:** A missing optional dependency is a setup issue, not an architectural violation.
Architecture fitness tests should fail only when the architecture is actually violated.
A clean environment without `uv sync` run shouldn't produce false failures — it should
clearly signal "run uv sync first" via the skip message.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| Fitness tests (10 tests) | `tests/architecture/test_adr_fitness.py` | PASSING | ADR-0008, 0010, 0007 structural validation |
| conftest.py | `tests/conftest.py` | PASSING | know path workaround for iCloud environments |
| W3 agent | `.claude/agents/hypothesis-adr-writer.md` | READY | ADR writing agent for future W3-equivalent work |
| W3.5 agent | `.claude/agents/fitness-function-writer.md` | READY | Fitness function agent for future W3.5-equivalent work |
| ADR-0007 refinement | Known Limitations section added | PROPOSED | Multi-session gap made explicit |
| ADR-0008 refinement | Artifact-to-Atom Extraction section added | PROPOSED | Extraction pattern formalized |
| Session learnings addenda | `state/learnings/session-2026-05-07-w3-hypothesis-adrs.md` | DONE | Reviews #2 and #3 insights captured |

## What Should Happen Next

1. **Execute W4**: Select first S1-S9 intake (recommend NF-01 or NF-07). Run full
   cycle using hypothesis ADRs as architectural context.
2. **Validate fitness functions during W4**: Do the 10 structural checks still pass
   after any code changes in W4? If not, ADR has diverged from implementation.
3. **Promote ADRs after 2+ intakes**: ADR-0007..0010 are HYPOTHESIS grade. After
   W4 and W5 validate them, promote to INFORMED_ESTIMATE.
4. **Multi-session support (v1)**: ADR-0007 Known Limitations section names the gap.
   When implementing the orchestrator, design session_type taxonomy + storage hierarchy.
5. **Artifact-to-Atom extraction (S9)**: ADR-0008 now specifies the extraction table.
   When implementing nowu-curator, use it as the implementation spec.
