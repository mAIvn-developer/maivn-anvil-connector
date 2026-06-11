from typing import Any

import anvil.server

from . import sessions, tables


class NotAuthorizedError(anvil.server.AnvilWrappedError):
    """Raised when a caller drains a session it does not own."""


@anvil.server.callable
def drain_events(*, session_id: str, after_seq: int, limit: int = 500) -> list[dict[str, Any]]:
    if sessions.owner_of(session_id) != sessions.current_owner():
        raise NotAuthorizedError("Not authorized for this session.")
    return tables.read_events(session_id, after_seq=after_seq, limit=limit)
