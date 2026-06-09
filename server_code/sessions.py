from __future__ import annotations

import secrets
from collections.abc import Callable
from typing import Any

import anvil.server

from . import limits

_owners: dict[str, str] = {}
_owner_provider: Callable[[], str] | None = None


def set_owner_provider(provider: Callable[[], str]) -> None:
    """Test/seam hook; in real Anvil this defaults to the Anvil session id."""
    global _owner_provider
    _owner_provider = provider


def current_owner() -> str:
    if _owner_provider is not None:
        return _owner_provider()
    return str(anvil.server.session.get("session_id", "anonymous"))


def owner_of(session_id: str) -> str | None:
    return _owners.get(session_id)


def bind_owner(session_id: str, owner: str | None = None) -> None:
    """Bind a session id to an owner (defaults to the current owner).

    ``start_session`` calls this; it is also the supported seam for advanced
    wiring or tests that need an owned session without launching a task.
    """
    _owners[session_id] = owner if owner is not None else current_owner()


@anvil.server.callable
def start_session(
    *, agent_key: str, messages: list[dict[str, Any]], example: str | None = None
) -> str:
    limits.enforce_start(example=example, messages=messages)
    session_id = secrets.token_urlsafe(24)
    bind_owner(session_id)
    anvil.server.launch_background_task(
        "run_agent_session", session_id=session_id, agent_key=agent_key, messages=messages
    )
    return session_id


@anvil.server.callable
def cancel_session(*, session_id: str) -> None:
    _require_owner(session_id)
    from . import tables

    tables.append_event(
        session_id,
        seq=2_000_000_001,
        kind="error",
        payload={"data": {"message": "Session cancelled."}},
    )


def _require_owner(session_id: str) -> None:
    from .drain import NotAuthorizedError

    if _owners.get(session_id) != current_owner():
        raise NotAuthorizedError("Not authorized for this session.")


def reset() -> None:
    _owners.clear()
