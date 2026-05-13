"""Session pipeline entry points for session start and step-boundary checkpointing."""

from nowu.core.contracts import SessionCheckpoint, SessionStore


def start_session(store: SessionStore) -> SessionCheckpoint | None:
    """Load the latest checkpoint from *store* and return it.

    Args:
        store: A SessionStore implementation that provides load/save.

    Returns:
        The existing SessionCheckpoint if one is persisted, or ``None`` when
        no prior session exists for the configured session_id.
    """
    return store.load()


def checkpoint_at_step_boundary(
    store: SessionStore,
    checkpoint: SessionCheckpoint,
) -> None:
    """Persist *checkpoint* at a step boundary via *store*.

    Args:
        store: A SessionStore implementation that provides load/save.
        checkpoint: The checkpoint to persist at this step boundary.
    """
    store.save(checkpoint)
