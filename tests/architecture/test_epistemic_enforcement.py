"""Architecture fitness tests for epistemic grade enforcement.

Implements two enforcement levels:
- Level 0 (W29): typed artifacts must carry a valid epistemic grade value
- Level 1 (W8): selected artifact types must meet minimum grade thresholds
"""

from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = PROJECT_ROOT / "state"
DOCS_DIR = PROJECT_ROOT / "docs"

GRADE_ORDER = [
    "SPECULATION",
    "HYPOTHESIS",
    "INFORMED_ESTIMATE",
    "EVIDENCE_BASED",
    "VERIFIED_FACT",
]

MINIMUM_GRADE_BY_TYPE: dict[str, str] = {
    "INTAKE_BRIEF": "HYPOTHESIS",
    "CONSTRAINTS_SHEET": "HYPOTHESIS",
    "OPTIONS_SHEET": "HYPOTHESIS",
    "DECISION_RECORD": "INFORMED_ESTIMATE",
    "TASK_SPEC": "HYPOTHESIS",
    "CHANGESET": "EVIDENCE_BASED",
    "VBR_REPORT": "EVIDENCE_BASED",
    "REVIEW_REPORT": "INFORMED_ESTIMATE",
    "CAPTURE_RECORD": "INFORMED_ESTIMATE",
    "SESSION_ANALYSIS": "INFORMED_ESTIMATE",
    "ADR": "HYPOTHESIS",
    "SYNTHESIS": "HYPOTHESIS",
    "VALIDATION_REPORT": "EVIDENCE_BASED",
    "ROADMAP": "INFORMED_ESTIMATE",
    "GOAL": "INFORMED_ESTIMATE",
    "SESSION_LEARNINGS": "INFORMED_ESTIMATE",
    "SESSION_LOG": "INFORMED_ESTIMATE",
}

VALID_GRADES = set(GRADE_ORDER)


def _parse_frontmatter(filepath: Path) -> dict[str, Any] | None:
    """Parse YAML frontmatter from a markdown file.

    Returns:
        Parsed frontmatter dictionary, or None if the file has no
        parseable YAML frontmatter.
    """
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return None

    end_index = content.find("\n---", 4)
    if end_index == -1:
        return None

    raw_frontmatter = content[4 : end_index + 1]
    try:
        parsed = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError:
        return None

    if not isinstance(parsed, dict):
        return None

    if "epistemic_grade" not in parsed and isinstance(parsed.get("grade"), str):
        normalized = dict(parsed)
        normalized["epistemic_grade"] = normalized["grade"]
        return normalized

    return parsed


def _is_typed_artifact(frontmatter: dict[str, Any]) -> bool:
    """Return whether frontmatter represents an enforceable typed artifact.

    Typed artifacts are those that declare an artifact_type and participate in
    the workflow metadata model via either altitude/phase or a grade field.
    """
    if "artifact_type" not in frontmatter:
        return False

    has_workflow_coordinates = "altitude" in frontmatter and "phase" in frontmatter
    has_grade_key = "epistemic_grade" in frontmatter or "grade" in frontmatter
    return has_workflow_coordinates or has_grade_key


def _grade_index(grade: str) -> int:
    """Return ordinal index for an epistemic grade value."""
    return GRADE_ORDER.index(grade)


class Level0EpistemicEnforcementTest(unittest.TestCase):
    """Level 0 (W29): enforce epistemic grade existence and value validity."""

    def test_all_typed_artifacts_have_epistemic_grade(self) -> None:
        """Ensure each typed artifact declares an epistemic grade.

        Scans markdown files in state/, parses YAML frontmatter, and checks that
        typed artifacts include epistemic_grade metadata.
        """
        violations: list[str] = []

        for filepath in STATE_DIR.rglob("*.md"):
            frontmatter = _parse_frontmatter(filepath)
            if frontmatter is None or not _is_typed_artifact(frontmatter):
                continue

            if "epistemic_grade" not in frontmatter:
                relative = filepath.relative_to(STATE_DIR)
                artifact_type = frontmatter.get("artifact_type", "<unknown>")
                violations.append(
                    f"{relative}: artifact_type={artifact_type} missing epistemic_grade"
                )

        self.assertFalse(
            violations,
            msg="Typed artifacts missing epistemic_grade:\n" + "\n".join(violations),
        )

    def test_epistemic_grades_are_valid_values(self) -> None:
        """Ensure declared epistemic grades use only canonical values.

        Any artifact frontmatter with epistemic_grade must use one of the 5
        canonical grades from ADR-0010.
        """
        violations: list[str] = []

        for filepath in STATE_DIR.rglob("*.md"):
            frontmatter = _parse_frontmatter(filepath)
            if frontmatter is None or "epistemic_grade" not in frontmatter:
                continue

            grade = frontmatter["epistemic_grade"]
            if grade not in VALID_GRADES:
                relative = filepath.relative_to(STATE_DIR)
                violations.append(f"{relative}: invalid epistemic_grade={grade!r}")

        self.assertFalse(
            violations,
            msg=(
                "Artifacts with invalid epistemic_grade values:\n"
                + "\n".join(violations)
            ),
        )


class Level1EpistemicEnforcementTest(unittest.TestCase):
    """Level 1 (W8): enforce minimum grade thresholds by artifact type."""

    def test_artifact_grades_meet_minimum_threshold(self) -> None:
        """Ensure artifact grades meet or exceed type-specific minimums.

        Enforces only known artifact types listed in MINIMUM_GRADE_BY_TYPE.
        Unknown artifact types are intentionally skipped.
        """
        violations: list[str] = []

        for filepath in STATE_DIR.rglob("*.md"):
            frontmatter = _parse_frontmatter(filepath)
            if frontmatter is None:
                continue

            artifact_type = frontmatter.get("artifact_type")
            if not isinstance(artifact_type, str):
                continue
            if artifact_type not in MINIMUM_GRADE_BY_TYPE:
                continue

            actual_grade = frontmatter.get("epistemic_grade")
            if actual_grade not in VALID_GRADES:
                continue

            minimum_grade = MINIMUM_GRADE_BY_TYPE[artifact_type]
            if _grade_index(actual_grade) < _grade_index(minimum_grade):
                relative = filepath.relative_to(STATE_DIR)
                violations.append(
                    f"{relative}: artifact_type={artifact_type} has {actual_grade}, "
                    f"minimum is {minimum_grade}"
                )

        self.assertFalse(
            violations,
            msg=(
                "Artifacts below minimum epistemic threshold:\n"
                + "\n".join(violations)
            ),
        )

    def test_capture_inherits_review_grade(self) -> None:
        """Ensure capture grade is not lower than the related review grade.

        Finds CAPTURE_RECORD artifacts in state/capture/, locates matching
        REVIEW_REPORT artifacts in state/reviews/ by intake_id in filename or
        frontmatter, and checks capture grade ordinal against review grade.
        """
        capture_dir = STATE_DIR / "capture"
        review_dir = STATE_DIR / "reviews"

        captures: list[tuple[Path, dict[str, Any]]] = []
        for filepath in capture_dir.rglob("*.md"):
            frontmatter = _parse_frontmatter(filepath)
            if frontmatter is None:
                continue
            if frontmatter.get("artifact_type") == "CAPTURE_RECORD":
                captures.append((filepath, frontmatter))

        if not captures:
            self.skipTest("No CAPTURE_RECORD artifacts found in state/capture/")

        review_items: list[tuple[Path, dict[str, Any]]] = []
        for filepath in review_dir.rglob("*.md"):
            frontmatter = _parse_frontmatter(filepath)
            if frontmatter is None:
                continue
            if frontmatter.get("artifact_type") == "REVIEW_REPORT":
                review_items.append((filepath, frontmatter))

        violations: list[str] = []
        compared = 0

        for capture_path, capture_frontmatter in captures:
            intake_id = capture_frontmatter.get("intake_id")
            capture_grade = capture_frontmatter.get("epistemic_grade")
            if not isinstance(intake_id, str):
                continue
            if capture_grade not in VALID_GRADES:
                continue

            matching_reviews: list[tuple[Path, dict[str, Any]]] = []
            for review_path, review_frontmatter in review_items:
                review_intake_id = review_frontmatter.get("intake_id")
                filename_match = intake_id in review_path.name
                frontmatter_match = review_intake_id == intake_id
                if filename_match or frontmatter_match:
                    matching_reviews.append((review_path, review_frontmatter))

            if not matching_reviews:
                continue

            review_path, review_frontmatter = matching_reviews[0]
            review_grade = review_frontmatter.get("epistemic_grade")
            if review_grade not in VALID_GRADES:
                continue

            compared += 1
            if _grade_index(capture_grade) < _grade_index(review_grade):
                violations.append(
                    f"{capture_path.relative_to(STATE_DIR)} ({capture_grade}) < "
                    f"{review_path.relative_to(STATE_DIR)} ({review_grade})"
                )

        if compared == 0:
            self.skipTest("No comparable CAPTURE_RECORD/REVIEW_REPORT pairs found")

        self.assertFalse(
            violations,
            msg="Capture grade lower than review grade:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
