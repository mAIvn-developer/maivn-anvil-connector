"""Session lifecycle callables. Anvil-runtime-safe (no annotations)."""

import secrets

import anvil.server

from . import limits, tables

_owner_provider = None


def set_owner_provider(provider):
    """Test/seam hook; in real Anvil this defaults to the Anvil session id."""
    global _owner_provider
    _owner_provider = provider


def current_owner():
    if _owner_provider is not None:
        return _owner_provider()
    get_session_id = getattr(anvil.server, "get_session_id", None)
    if callable(get_session_id):
        return str(get_session_id())
    session = anvil.server.session
    session_id = getattr(session, "session_id", None)
    if session_id is not None:
        return str(session_id)
    if hasattr(session, "get"):
        stored = session.get("session_id")
        if stored is not None:
            return str(stored)
    return "anonymous"


def is_authorized(session_id):
    bound_owner = owner_of(session_id)
    if bound_owner is None:
        return False
    return bound_owner == current_owner()


def owner_of(session_id):
    return tables.read_session_owner(session_id)


def bind_owner(session_id, owner=None):
    """Bind a session id to an owner (defaults to the current owner).

    ``start_session`` calls this; it is also the supported seam for advanced
    wiring or tests that need an owned session without launching a task.

    Ownership is stored as a sentinel row in ``maivn_events`` (seq 0,
    kind ``_session_owner``) so ``drain_events`` can authorize the caller even
    when Anvil routes callables to a different server instance than
    ``start_session``, without requiring a schema change.
    """
    tables.bind_session_owner(
        session_id,
        owner if owner is not None else current_owner(),
    )


@anvil.server.callable
def start_session(*, agent_key, messages, example=None):
    limits.enforce_start(example=example, messages=messages)
    session_id = secrets.token_urlsafe(24)
    bind_owner(session_id)
    anvil.server.launch_background_task(
        "run_agent_session", session_id=session_id, agent_key=agent_key, messages=messages
    )
    return session_id


@anvil.server.callable
def cancel_session(*, session_id):
    _require_owner(session_id)
    tables.append_event(
        session_id,
        seq=2_000_000_001,
        kind="error",
        payload={"data": {"message": "Session cancelled."}},
    )


def _require_owner(session_id):
    from .drain import NotAuthorizedError

    if not is_authorized(session_id):
        raise NotAuthorizedError("Not authorized for this session.")


def reset():
    tables.reset_session_owners()
