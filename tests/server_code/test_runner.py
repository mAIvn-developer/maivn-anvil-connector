from __future__ import annotations

from typing import Any

from maivn._internal.core.entities.sse_event import SSEEvent
from maivn.events import FINAL_EVENT_NAME
from maivn_anvil_connector import registry, runner, tables


class _StubAgent:
    name = "demo"

    def __init__(self, events: list[Any]) -> None:
        self._events = events
        self.last_messages: Any = None

    def stream(self, messages: Any, **kwargs: Any) -> list[Any]:
        self.last_messages = messages
        return self._events


def test_runner_writes_final_event() -> None:
    registry.reset()
    registry.register_agent(
        "demo", _StubAgent([SSEEvent(name=FINAL_EVENT_NAME, payload={"response": "hi"})])
    )
    runner.run_agent_session(
        session_id="s1", agent_key="demo", messages=[{"role": "user", "content": "hi"}]
    )
    rows = tables.read_events("s1", after_seq=0)
    assert any(r["kind"] == "final" for r in rows)


def test_runner_writes_error_event_on_failure() -> None:
    registry.reset()

    class _Boom:
        name = "boom"

        def stream(self, messages: Any, **kwargs: Any) -> list[Any]:
            raise RuntimeError("upstream down")

    registry.register_agent("boom", _Boom())
    runner.run_agent_session(session_id="s2", agent_key="boom", messages=[])
    rows = tables.read_events("s2", after_seq=0)
    assert any(r["kind"] == "error" for r in rows)
    # The internal failure detail is never persisted.
    assert all("upstream down" not in str(r["payload"]) for r in rows)
