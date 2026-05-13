---
name: tdd-commit-order
description: TDD RED→GREEN ordering cannot be verified when all implementation is in an uncommitted working tree
metadata:
  type: feedback
---

In intake-001, all 5 tasks' changes were in the working tree (uncommitted) when S8 review
ran. `git log` showed no implementation commits. This made it impossible to verify that
test files were created before implementation files.

**Why:** The workflow does not require per-task commits. S6-S7 can produce a fully working
implementation without ever committing, and S8 receives no git ordering evidence.

**How to apply:** When git log shows no implementation commits, rely on:
1. Task spec TDD test strategies (step-ordered: write test, confirm RED, implement, confirm GREEN)
2. VBR new-test counts per task (indirect evidence)
3. Note the gap explicitly in the review and in lessons for S9 to capture

Do not FAIL the TDD check solely on missing commits — but flag it as a friction point
in the analysis. Recommend S9 captures a lesson about per-task commit requirements.

Related: [[vbr-dependency-gap]]
