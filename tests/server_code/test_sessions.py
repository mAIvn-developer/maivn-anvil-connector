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


def test_start_session_returns_unguessable_id_and_binds_owner() -> None:
    _setup()
    sessions.set_owner_provider(lambda: "owner-A")
    sid = sessions.start_session(agent_key="demo", messages=[])
    assert len(sid) >= 16
    assert sessions.owner_of(sid) == "owner-A"


def test_drain_rejects_foreign_owner() -> None:
    _setup()
    sessions.set_owner_provider(lambda: "owner-A")
    sid = sessions.start_session(agent_key="demo", messages=[])
    tables.append_event(sid, seq=1, kind="status_message", payload={"data": {"text": "x"}})

    sessions.set_owner_provider(lambda: "attacker-B")
    with pytest.raises(drain.NotAuthorizedError):
        drain.drain_events(session_id=sid, after_seq=0)


def test_drain_returns_events_for_owner() -> None:
    _setup()
    sessions.set_owner_provider(lambda: "owner-A")
    sid = sessions.start_session(agent_key="demo", messages=[])
    tables.append_event(sid, seq=1, kind="final", payload={"data": {"response": "done"}})
    rows = drain.drain_events(session_id=sid, after_seq=0)
    assert rows[0]["kind"] == "final"


def test_drain_authorizes_from_data_table_without_memory_binding() -> None:
    """Simulate drain on a fresh server instance that only sees Data Tables."""
    _setup()
    sessions.set_owner_provider(lambda: "owner-A")
    sid = "table-bound-session"
    tables.bind_session_owner(sid, "owner-A")
    tables.append_event(sid, seq=1, kind="final", payload={"data": {"response": "done"}})
    rows = drain.drain_events(session_id=sid, after_seq=0)
    assert rows[0]["kind"] == "final"
