# W6 Cross-Reference Consistency Report

Generated: 2026-05-14  
Commit: e238ceb

## AC-1: S7/S8 Consistency — PASS

Commands run:

```bash
grep -n "S7\|S8" docs/model/MODEL-REFERENCE.md | grep -i "agent\|phase\|verif\|eval\|review\|VBR\|implement"
grep -n "S7\|S8" docs/model/WORKFLOW-STANDARDS.md | grep -i "VERIF\|EVAL"
grep -n "S7\|S8" docs/WORKFLOW.md | grep -i "nowu\|VBR"
grep -n "S7\|S8" docs/WORKFLOW-DETAILED.md | grep -i "nowu\|VBR"
grep -n "S8" docs/WORKFLOW-DETAILED.md | grep -i "review\|evalu\|nowu"
```

Output highlights:

- `MODEL-REFERENCE.md`:
  - `193: | S7 | VBR | EXECUTION | VERIFICATION | ... |`
  - `194: | S8 | nowu-reviewer | EXECUTION | EVALUATION | ... |`
  - `314: | VBR (S7) | EXECUTION | VERIFICATION | ... |`
  - `315: | nowu-reviewer (S8) | EXECUTION | EVALUATION | ... |`
  - `522: state/vbr/vbr-task-NNN.md ... (S7)`
  - `523: state/reviews/review-task-NNN.md ... (S8)`
- `WORKFLOW-STANDARDS.md`:
  - `33: | S7 | EXECUTION | VERIFICATION |`
  - `34: | S8 | EXECUTION | EVALUATION |`
- `WORKFLOW.md`:
  - `65: | S6+S7 | Implement + VBR | nowu-implementer | ... |`
  - `66: | S8 | Review | nowu-reviewer | ... |`
- `WORKFLOW-DETAILED.md`:
  - `205: ## S7 — VBR (Verify Before Responding)`
  - `208: Actor: nowu-implementer + automation`
  - `231: ## S8 — Review`
  - `234: Actor: nowu-reviewer agent`

Finding: Core S7/S8 role mapping is consistent across all 4 docs (S7=VBR/VERIFICATION via nowu-implementer, S8=review/EVALUATION via nowu-reviewer).

## AC-2: All 35 Agents Have altitude/phase — PASS

Commands run:

```bash
grep -c "^altitude:" .claude/agents/*.md | grep -v ":1$"
grep -c "^phase:" .claude/agents/*.md | grep -v ":1$"
grep "^altitude:" .claude/agents/*.md | wc -l
grep "^phase:" .claude/agents/*.md | wc -l
```

Outputs:

- `grep -v ":1$"` on altitude: *(no output)*
- `grep -v ":1$"` on phase: *(no output)*
- Total altitude lines: `35`
- Total phase lines: `35`

## AC-3: All altitude values valid enums — PASS

Command:

```bash
grep "^altitude:" .claude/agents/*.md | awk -F': ' '{print $2}' | sort -u
```

Output:

```text
ARCHITECTURE
DELIVERY
EXECUTION
PRODUCT
STRATEGIC
```

All values are within allowed set `{STRATEGIC, PRODUCT, ARCHITECTURE, DELIVERY, EXECUTION}`.

## AC-4: All phase values valid enums — PASS

Command:

```bash
grep "^phase:" .claude/agents/*.md | awk -F': ' '{print $2}' | sort -u
```

Output:

```text
ANALYSIS
DECISION
EVALUATION
IDEA
IMPLEMENTATION
LEARN
OPTIONS
PROBLEM
SYNTHESIS
VERIFICATION
```

All values are within allowed set `{IDEA, PROBLEM, ANALYSIS, SYNTHESIS, OPTIONS, DECISION, EVALUATION, IMPLEMENTATION, VERIFICATION, LEARN}`.

## AC-5: No forbidden file changes — FAIL

Commands run:

```bash
git diff HEAD~4 -- docs/WORKFLOW.md docs/WORKFLOW-DETAILED.md | wc -l
git diff HEAD~4 -- docs/PRE-WORKFLOW.md CLAUDE.md | wc -l
git diff HEAD~4 -- src/ tests/ scripts/ templates/ | wc -l
git diff --name-only HEAD~4 -- src/ tests/ scripts/ templates/
git diff HEAD~4 -- src/nowu.egg-info/SOURCES.txt
```

Outputs:

- Workflow docs diff lines: `0`
- PRE-WORKFLOW/CLAUDE diff lines: `0`
- `src/tests/scripts/templates` diff lines: `12`
- Changed file:
  - `src/nowu.egg-info/SOURCES.txt`
- Diff excerpt:
  - Added line entry: `src/nowu/flow/pipeline.py`

Finding: Forbidden-path diff is not zero due to generated metadata file under `src/`.

## AC-6: AGENTS.md grid matches frontmatter (5-agent spot-check) — PASS

Commands run:

```bash
grep "nowu-implementer" AGENTS.md
grep "^altitude:\|^phase:" .claude/agents/nowu-implementer.md

grep "vision-bootstrap" AGENTS.md
grep "^altitude:\|^phase:" .claude/agents/vision-bootstrap.md

grep "health-architecture" AGENTS.md
grep "^altitude:\|^phase:" .claude/agents/health-architecture.md

grep "gap-analyst" AGENTS.md
grep "^altitude:\|^phase:" .claude/agents/gap-analyst.md

grep "work-scheduler" AGENTS.md
grep "^altitude:\|^phase:" .claude/agents/work-scheduler.md
```

Result matrix:

- `nowu-implementer`: AGENTS `EXECUTION | IMPLEMENTATION`; frontmatter `altitude: EXECUTION`, `phase: IMPLEMENTATION` ✅
- `vision-bootstrap`: AGENTS `STRATEGIC | DECISION`; frontmatter `altitude: STRATEGIC`, `phase: DECISION` ✅
- `health-architecture`: AGENTS `ARCHITECTURE | VERIFICATION`; frontmatter `altitude: ARCHITECTURE`, `phase: VERIFICATION` ✅
- `gap-analyst`: AGENTS `ARCHITECTURE | ANALYSIS`; frontmatter `altitude: ARCHITECTURE`, `phase: ANALYSIS` ✅
- `work-scheduler`: AGENTS `STRATEGIC | EVALUATION`; frontmatter `altitude: STRATEGIC`, `phase: EVALUATION` ✅

## AC-7: Section 13 consumption note + planned entries — PASS

Commands run:

```bash
grep -c "consumption" docs/model/MODEL-REFERENCE.md
grep "state/changes" docs/model/MODEL-REFERENCE.md
grep "state/reviews" docs/model/MODEL-REFERENCE.md
grep "state/learnings" docs/model/MODEL-REFERENCE.md
```

Outputs:

- `consumption` count: `1`
- `state/changes` matched
- `state/reviews` matched
- `state/learnings` matched

## AC-8: artifact_type vocabulary covers all existing values — FAIL

Commands run:

```bash
grep -rh "^artifact_type:" docs/ templates/ state/ | sort -u > /tmp/existing_types.txt
wc -l /tmp/existing_types.txt
python - <<'PY'
import pathlib
root=pathlib.Path('.')
vals=set()
for base in ['docs','templates','state']:
    for p in (root/base).rglob('*'):
        if p.is_file():
            try:
                text=p.read_text(encoding='utf-8')
            except Exception:
                continue
            for line in text.splitlines():
                if line.startswith('artifact_type:'):
                    vals.add(line.split(': ',1)[1].strip())
model=(root/'docs/model/MODEL-REFERENCE.md').read_text(encoding='utf-8')
missing=[v for v in sorted(vals) if v not in model]
print('TOTAL_VALUES',len(vals))
print('MISSING_COUNT',len(missing))
for v in missing:
    print('MISSING',v)
PY
grep -n "^artifact_type:\s*GOAL \| USE_CASE \| ADR \| SYNTHESIS \| LESSON" templates/artifact-5x10.md docs/model/IMPLEMENTATION-GUIDE.md
```

Outputs:

- Existing artifact_type lines: `21`
- Coverage check:
  - `TOTAL_VALUES 21`
  - `MISSING_COUNT 1`
  - `MISSING GOAL | USE_CASE | ADR | SYNTHESIS | LESSON`
- Missing value appears in:
  - `templates/artifact-5x10.md:8`
  - `docs/model/IMPLEMENTATION-GUIDE.md:167`

Finding: One literal artifact_type value used in repo is not listed in MODEL-REFERENCE §13.1 canonical vocabulary table.

## Additional Check: Verification status labels present — PASS

All AC sections are explicitly labeled with one of: PASS, FAIL, WARNING, BLOCKER.

## Summary

- PASS: 7
- FAIL: 2
- WARNING: 0
- BLOCKER: 0

No BLOCKER entries detected.
