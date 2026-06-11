from __future__ import annotations

from typing import Any

import pytest
from maivn_anvil_connector import drain, limits, registry, sessions, tables


class _StubAgent:
    name = "demo"

    def stream(self, messages: Any, **kwargs: Any) -> list[Any]:
        return []


def _setup() -> None:
    registry.reset()
    sessions.reset()
    limits.reset()
    registry.register_agent("demo", _StubAgent())


def test_start_session_returns_ids_and_binds_secret() -> None:
    _setup()
    result = sessions.start_session(agent_key="demo", messages=[])
    assert isinstance(result, dict)
    sid = result["session_id"]
    secret = result["session_secret"]
    assert len(sid) >= 16
    assert len(secret) >= 16
    assert sessions.owner_of(sid) == secret


def test_drain_rejects_wrong_secret() -> None:
    _setup()
    result = sessions.start_session(agent_key="demo", messages=[])
    sid = result["session_id"]
    tables.append_event(sid, seq=1, kind="status_message", payload={"data": {"text": "x"}})

    with pytest.raises(drain.NotAuthorizedError):
        drain.drain_events(session_id=sid, session_secret="wrong-secret", after_seq=0)


def test_drain_returns_events_for_holder() -> None:
    _setup()
    result = sessions.start_session(agent_key="demo", messages=[])
    sid = result["session_id"]
    secret = result["session_secret"]
    tables.append_event(sid, seq=1, kind="final", payload={"data": {"response": "done"}})
    rows = drain.drain_events(session_id=sid, session_secret=secret, after_seq=0)
    assert rows[0]["kind"] == "final"


def test_drain_authorizes_from_data_table_without_memory_binding() -> None:
    """Simulate drain on a fresh server instance that only sees Data Tables."""
    _setup()
    sid = "table-bound-session"
    secret = "table-bound-secret"
    tables.bind_session_owner(sid, secret)
    tables.append_event(sid, seq=1, kind="final", payload={"data": {"response": "done"}})
    rows = drain.drain_events(session_id=sid, session_secret=secret, after_seq=0)
    assert rows[0]["kind"] == "final"
