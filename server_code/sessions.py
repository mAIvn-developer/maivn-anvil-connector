"""Session lifecycle callables. Anvil-runtime-safe (no annotations)."""

import secrets

import anvil.server

from . import limits, tables

# Namespaced to avoid colliding with host-app @anvil.server.callable names.
RPC_START = "maivn_start_session"
RPC_CANCEL = "maivn_cancel_session"


def is_authorized(session_id, session_secret):
    if not session_secret:
        return False
    bound = owner_of(session_id)
    return bound is not None and bound == session_secret


def owner_of(session_id):
    return tables.read_session_owner(session_id)


def bind_owner(session_id, session_secret):
    """Bind a session id to a client-held secret (tests and advanced wiring).

    ``start_session`` generates the secret and stores it as a sentinel row in
    ``maivn_events`` (seq 0, kind ``_session_owner``) so ``drain_events`` can
    authorize callers on any server instance without relying on Anvil session ids.
    """
    tables.bind_session_owner(session_id, session_secret)


@anvil.server.callable(RPC_START)
def start_session(*, agent_key, messages, example=None):
    limits.enforce_start(example=example, messages=messages)
    session_id = secrets.token_urlsafe(24)
    session_secret = secrets.token_urlsafe(24)
    bind_owner(session_id, session_secret)
    anvil.server.launch_background_task(
        "run_agent_session", session_id=session_id, agent_key=agent_key, messages=messages
    )
    return {"session_id": session_id, "session_secret": session_secret}


@anvil.server.callable("start_session")
def start_session_legacy(**kwargs):
    return start_session(**kwargs)


@anvil.server.callable(RPC_CANCEL)
def cancel_session(*, session_id, session_secret):
    _require_owner(session_id, session_secret)
    tables.append_event(
        session_id,
        seq=2_000_000_001,
        kind="error",
        payload={"data": {"message": "Session cancelled."}},
    )


@anvil.server.callable("cancel_session")
def cancel_session_legacy(**kwargs):
    return cancel_session(**kwargs)


def _require_owner(session_id, session_secret):
    from .drain import NotAuthorizedError

    if not is_authorized(session_id, session_secret):
        raise NotAuthorizedError("Not authorized for this session.")


def reset():
    tables.reset_session_owners()
