# Code Review Prompt

Use when reviewing a PR from the Copilot coding agent (paste into PR comment mentioning @copilot).

---

@copilot Please review this PR against the following checklist:

**Architecture compliance:**
- [ ] Does this PR only touch the intended module? No cross-module boundary violations?
- [ ] Are all calls to the database routed through `know`'s Storage class?
- [ ] Does any new code violate a decision in DECISIONS.md?

**Code quality:**
- [ ] Are all functions type-hinted?
- [ ] Are all public functions documented with docstrings?
- [ ] Are there no magic strings (AtomType and ConnectionType enums used)?
- [ ] Is test coverage ≥ 90% for new code?

**Completeness:**
- [ ] Are all acceptance criteria in the task file checked?
- [ ] Does the PR update DECISIONS.md if a new decision was made?
- [ ] Is SESSION-STATE.md updated with what was implemented?

If any item is not met, explain what needs to change and make the corrections.
