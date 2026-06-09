from __future__ import annotations

from typing import Any

import pytest
from maivn._internal.core.entities.sse_event import SSEEvent
from maivn.events import FINAL_EVENT_NAME, BridgeAudience
from maivn_anvil_connector import pump


class _RecordingWriter:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []
        self.flushed = False

    def write(self, kind: str, payload: dict[str, Any]) -> None:
        self.events.append((kind, payload))

    def flush(self) -> None:
        self.flushed = True


def _final_stream() -> list[SSEEvent]:
    return [SSEEvent(name=FINAL_EVENT_NAME, payload={"response": "Hello"})]


def test_final_event_is_written_and_flushed() -> None:
    writer = _RecordingWriter()
    pump.run_stream_to_writer(
        session_id="s1", raw_stream=_final_stream(), writer=writer, default_agent_name="demo"
    )
    assert "final" in [k for k, _ in writer.events]
    assert writer.flushed is True


def test_pump_only_drains_a_frontend_safe_bridge(monkeypatch: pytest.MonkeyPatch) -> None:
    """Security contract: the bridge the pump emits through must be frontend_safe."""
    captured: list[str] = []
    real_bridge = pump.EventBridge

    def _spy_bridge(session_id: str, *, audience: BridgeAudience = "internal") -> Any:
        captured.append(audience)
        return real_bridge(session_id, audience=audience)

    monkeypatch.setattr(pump, "EventBridge", _spy_bridge)
    writer = _RecordingWriter()
    pump.run_stream_to_writer(session_id="s1", raw_stream=_final_stream(), writer=writer)

    assert captured == ["frontend_safe"]
