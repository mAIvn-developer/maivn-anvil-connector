"""Event drain callable. Anvil-runtime-safe (no annotations)."""

import anvil.server

from . import sessions, tables

RPC_DRAIN = "maivn_drain_events"


class NotAuthorizedError(anvil.server.AnvilWrappedError):
    """Raised when a caller drains a session it does not own."""


@anvil.server.callable(RPC_DRAIN)
def drain_events(*, session_id, session_secret, after_seq, limit=500):
    if not sessions.is_authorized(session_id, session_secret):
        raise NotAuthorizedError("Not authorized for this session.")
    return tables.read_events(session_id, after_seq=after_seq, limit=limit)


@anvil.server.callable("drain_events")
def drain_events_legacy(**kwargs):
    return drain_events(**kwargs)
