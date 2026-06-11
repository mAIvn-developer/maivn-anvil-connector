"""Event drain callable. Anvil-runtime-safe (no annotations)."""

import anvil.server

from . import sessions, tables


class NotAuthorizedError(anvil.server.AnvilWrappedError):
    """Raised when a caller drains a session it does not own."""


@anvil.server.callable
def drain_events(*, session_id, after_seq, limit=500):
    if not sessions.is_authorized(session_id):
        raise NotAuthorizedError("Not authorized for this session.")
    return tables.read_events(session_id, after_seq=after_seq, limit=limit)
