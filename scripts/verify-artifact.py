#!/usr/bin/env python3
"""verify-artifact.py — Level 0 syntax verification for nowu 5x10 artifacts."""

import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS_KNOWLEDGE = [
    "artifact_class",
    "artifact_type",
    "id",
    "title",
    "origin_altitude",
    "origin_phase",
    "consumer_altitudes",
    "epistemic_grade",
    "grade_justification",
    "status",
    "created_at",
    "last_edited_at",
]

REQUIRED_FIELDS_WORKFLOW = [
    "artifact_class",
    "altitude",
    "phase",
    "session_id",
    "epistemic_grade",
    "grade_justification",
]

VALID_ALTITUDES = ["STRATEGIC", "PRODUCT", "ARCHITECTURE", "DELIVERY", "EXECUTION"]
VALID_PHASES = [
    "IDEA",
    "PROBLEM",
    "ANALYSIS",
    "SYNTHESIS",
    "OPTIONS",
    "DECISION",
    "EVALUATION",
    "IMPLEMENTATION",
    "VERIFICATION",
    "LEARN",
]
VALID_GRADES = [
    "SPECULATION",
    "HYPOTHESIS",
    "INFORMED_ESTIMATE",
    "EVIDENCE_BASED",
    "VERIFIED_FACT",
]
VALID_STATUS = ["ACTIVE", "SUPERSEDED", "DEPRECATED"]


def verify_artifact(filepath: Path) -> list[str]:
    """Returns list of violations, empty if valid."""
    violations = []

    with open(filepath) as f:
        content = f.read()

    # Check YAML frontmatter exists
    if not content.startswith("---\n"):
        return ["No YAML frontmatter found"]

    # Parse frontmatter
    try:
        _, fm, body = content.split("---\n", 2)
        metadata = yaml.safe_load(fm)
    except Exception as e:
        return [f"YAML parse error: {e}"]

    if not isinstance(metadata, dict):
        return ["Frontmatter is not a YAML mapping"]

    # Check artifact class
    artifact_class = metadata.get("artifact_class")
    if artifact_class not in ["knowledge", "workflow_phase"]:
        violations.append(f"Invalid artifact_class: {artifact_class}")
        return violations

    # Check required fields
    required = (
        REQUIRED_FIELDS_KNOWLEDGE
        if artifact_class == "knowledge"
        else REQUIRED_FIELDS_WORKFLOW
    )
    for field in required:
        if field not in metadata:
            violations.append(f"Missing required field: {field}")

    # Check enums
    if "altitude" in metadata and metadata["altitude"] not in VALID_ALTITUDES:
        violations.append(f"Invalid altitude: {metadata['altitude']}")
    if (
        "origin_altitude" in metadata
        and metadata["origin_altitude"] not in VALID_ALTITUDES
    ):
        violations.append(f"Invalid origin_altitude: {metadata['origin_altitude']}")
    if "phase" in metadata and metadata["phase"] not in VALID_PHASES:
        violations.append(f"Invalid phase: {metadata['phase']}")
    if "origin_phase" in metadata and metadata["origin_phase"] not in VALID_PHASES:
        violations.append(f"Invalid origin_phase: {metadata['origin_phase']}")
    if metadata.get("epistemic_grade") not in VALID_GRADES:
        violations.append(f"Invalid epistemic_grade: {metadata.get('epistemic_grade')}")
    if artifact_class == "knowledge" and metadata.get("status") not in VALID_STATUS:
        violations.append(f"Invalid status: {metadata.get('status')}")

    # Check file path matches altitude
    alt_key = (
        "altitude"
        if "altitude" in metadata
        else "origin_altitude"
        if "origin_altitude" in metadata
        else None
    )
    if alt_key:
        expected_dir = f"state/artifacts/{metadata[alt_key].lower()}"
        if expected_dir not in str(filepath):
            violations.append(
                f"File in wrong directory (expected path containing {expected_dir})"
            )

    # Check ID matches filename (for knowledge artifacts)
    if artifact_class == "knowledge" and "id" in metadata:
        expected_filename = f"{metadata['id']}.md"
        if filepath.name != expected_filename:
            violations.append(f"Filename mismatch (expected {expected_filename})")

    return violations


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify-artifact.py <filepath>")
        sys.exit(2)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"File not found: {target}")
        sys.exit(2)

    violations = verify_artifact(target)
    if violations:
        print("Violations found:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("Artifact valid")
