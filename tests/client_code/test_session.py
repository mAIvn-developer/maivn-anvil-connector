from __future__ import annotations

from typing import Any

from maivn_anvil_connector.session import MaivnSession


class _FakeServer:
    def __init__(self, batches: list[list[dict[str, Any]]]) -> None:
        self._batches = batches
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def call(self, fn: str, **kwargs: Any) -> Any:
        self.calls.append((fn, kwargs))
        if fn == "maivn_start_session":
            return {"session_id": "sid-1", "session_secret": "secret-1"}
        if fn == "maivn_drain_events":
            return self._batches.pop(0) if self._batches else []
        return None


def test_session_dispatches_events_and_finishes() -> None:
    server = _FakeServer(
        [
            [{"seq": 1, "kind": "assistant_chunk", "payload": {"data": {"text": "Hi"}}}],
            [{"seq": 2, "kind": "final", "payload": {"data": {"response": "Hi there"}}}],
        ]
    )
    seen: list[str] = []
    s = MaivnSession(agent_key="demo", call=server.call)
    s.on("assistant_chunk", lambda e: seen.append(e.text))
    s.on("final", lambda e: seen.append(f"FINAL:{e.text}"))
    s.start(messages=[{"role": "user", "content": "hi"}])

    s.pump_once()
    s.pump_once()

    assert seen == ["Hi", "FINAL:Hi there"]
    assert s.is_done is True


def test_session_tracks_cursor_high_water_mark() -> None:
    server = _FakeServer(
        [[{"seq": 5, "kind": "status_message", "payload": {"data": {"text": "x"}}}]]
    )
    s = MaivnSession(agent_key="demo", call=server.call)
    s.start(messages=[])
    s.pump_once()
    assert s.cursor == 5
    s.pump_once()
    assert (
        "maivn_drain_events",
        {"session_id": "sid-1", "session_secret": "secret-1", "after_seq": 5},
    ) in server.calls
