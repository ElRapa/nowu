"""File-based implementation of the SessionStore Protocol.

Writes checkpoint JSON atomically and maintains a YAML human-readable
bookmark at a configurable path (state/SESSION_STATE.md by default).
"""

from __future__ import annotations

import json
import tempfile
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import yaml

from nowu.core.contracts import SessionCheckpoint


_OLD_SNAPSHOT_FIELDS = frozenset(
    {"session_id", "active_project", "active_role", "next_action", "blockers"}
)

_NEW_CHECKPOINT_FIELDS = frozenset(
    {
        "session_id",
        "active_project",
        "active_role",
        "next_action",
        "active_step",
        "last_artifact_path",
        "checkpoint_grade",
        "active_ids",
        "completed_steps",
        "schema_version",
    }
)

_BOOKMARK_REQUIRED_KEYS = [
    "session_id",
    "active_project",
    "active_role",
    "active_step",
    "next_action",
    "completed_steps",
    "last_artifact_path",
    "schema_version",
]


class FileSessionStore:
    """Persist SessionCheckpoint objects to the local filesystem.

    JSON checkpoints are stored at:
        ``{sessions_dir}/{session_id}/checkpoint-latest.json``

    A YAML human bookmark is maintained at ``bookmark_path``.

    The save operation is atomic: the JSON is written via a temp file and
    renamed into place; the bookmark is only written after the JSON rename
    succeeds.  If the rename fails, no partial JSON remains and the bookmark
    is not touched.
    """

    def __init__(
        self,
        sessions_dir: Path,
        bookmark_path: Path,
        session_id: str = "",
    ) -> None:
        """Initialise the store.

        Args:
            sessions_dir: Directory that holds per-session subdirectories.
            bookmark_path: Path to the human-readable YAML bookmark file.
            session_id: Session whose checkpoint ``load()`` reads.  When empty,
                ``load()`` returns ``None``.
        """
        self._sessions_dir = sessions_dir
        self._bookmark_path = bookmark_path
        self._session_id = session_id

    # ------------------------------------------------------------------
    # Protocol methods
    # ------------------------------------------------------------------

    def load(self) -> SessionCheckpoint | None:
        """Load the latest checkpoint for the configured session_id.

        Returns:
            A ``SessionCheckpoint`` (possibly migrated from old format) or
            ``None`` when no checkpoint file exists.
        """
        if not self._session_id:
            return None

        checkpoint_path = (
            self._sessions_dir / self._session_id / "checkpoint-latest.json"
        )
        if not checkpoint_path.exists():
            return None

        try:
            raw: dict[str, Any] = json.loads(
                checkpoint_path.read_text(encoding="utf-8")
            )
        except JSONDecodeError as exc:
            raise ValueError(
                f"Checkpoint file contains invalid JSON: {checkpoint_path}"
            ) from exc

        if "schema_version" not in raw:
            return _migrate_snapshot_to_checkpoint(raw)

        return SessionCheckpoint(
            session_id=raw["session_id"],
            active_project=raw["active_project"],
            active_role=raw["active_role"],
            next_action=raw["next_action"],
            active_step=raw.get("active_step", ""),
            last_artifact_path=raw.get("last_artifact_path", ""),
            checkpoint_grade=raw.get("checkpoint_grade", "unknown"),
            active_ids=raw.get("active_ids", {}),
            completed_steps=raw.get("completed_steps", []),
            schema_version=raw.get("schema_version", "v1"),
        )

    def save(self, checkpoint: SessionCheckpoint) -> None:
        """Atomically persist *checkpoint* and refresh the YAML bookmark.

        The JSON is written first via a temp-file-and-rename sequence so
        that no partial file is ever visible.  The YAML bookmark is only
        written after the JSON rename succeeds.

        Args:
            checkpoint: The checkpoint to persist.

        Raises:
            OSError: Propagated from the filesystem if the atomic rename fails.
        """
        session_dir = self._sessions_dir / checkpoint.session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        json_path = session_dir / "checkpoint-latest.json"
        self._atomic_write_json(json_path, checkpoint)
        self._write_yaml_bookmark(checkpoint)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _atomic_write_json(self, target: Path, checkpoint: SessionCheckpoint) -> None:
        """Write JSON to *target* atomically using a sibling temp file."""
        payload = {
            "session_id": checkpoint.session_id,
            "active_project": checkpoint.active_project,
            "active_role": checkpoint.active_role,
            "next_action": checkpoint.next_action,
            "active_step": checkpoint.active_step,
            "last_artifact_path": checkpoint.last_artifact_path,
            "checkpoint_grade": checkpoint.checkpoint_grade,
            "active_ids": checkpoint.active_ids,
            "completed_steps": checkpoint.completed_steps,
            "schema_version": checkpoint.schema_version,
        }

        # Write to a sibling temp file; rename is atomic on POSIX.
        fd, tmp_name = tempfile.mkstemp(
            dir=target.parent, prefix=".tmp-checkpoint-", suffix=".json"
        )
        tmp_path = Path(tmp_name)
        try:
            with open(fd, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=2)
            # Atomic rename — may raise OSError (tested by atomicity test)
            tmp_path.replace(target)
        except Exception:
            # Best-effort cleanup of temp file; ignore secondary errors.
            try:
                tmp_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise

    def _write_yaml_bookmark(self, checkpoint: SessionCheckpoint) -> None:
        """Write the human-readable YAML bookmark to ``bookmark_path``."""
        data = {
            "session_id": checkpoint.session_id,
            "active_project": checkpoint.active_project,
            "active_role": checkpoint.active_role,
            "active_step": checkpoint.active_step,
            "next_action": checkpoint.next_action,
            "completed_steps": list(checkpoint.completed_steps),
            "last_artifact_path": checkpoint.last_artifact_path,
            "schema_version": checkpoint.schema_version,
        }
        self._bookmark_path.parent.mkdir(parents=True, exist_ok=True)
        self._bookmark_path.write_text(
            yaml.dump(data, default_flow_style=False, allow_unicode=True),
            encoding="utf-8",
        )


def _migrate_snapshot_to_checkpoint(raw: dict[str, Any]) -> SessionCheckpoint:
    """Translate a legacy 5-field SessionSnapshot dict to SessionCheckpoint.

    Args:
        raw: Parsed JSON dict from an old-format checkpoint file.

    Returns:
        A ``SessionCheckpoint`` with migrated defaults for missing fields.
    """
    return SessionCheckpoint(
        session_id=raw["session_id"],
        active_project=raw["active_project"],
        active_role=raw["active_role"],
        next_action=raw["next_action"],
        active_step="",
        last_artifact_path="",
        checkpoint_grade="unknown",
        active_ids={},
        completed_steps=[],
        schema_version="v0-migrated",
    )
