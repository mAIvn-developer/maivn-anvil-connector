import asyncio
from typing import Any, Iterable, Protocol

from . import _py310_compat  # noqa: F401
from maivn.events import (
    EventBridge,
    NormalizedStreamState,
    forward_normalized_event,
    normalize_stream_event,
)


class _Writer(Protocol):
    def write(self, kind: str, payload: dict[str, Any]) -> None: ...
    def flush(self) -> None: ...


def run_stream_to_writer(
    *,
    session_id: str,
    raw_stream: Iterable[Any],
    writer: _Writer,
    default_agent_name: str | None = None,
) -> None:
    """Forward a raw SDK stream through a frontend_safe bridge into the writer.

    Security boundary: every event is sanitized by the EventBridge
    (audience='frontend_safe') before it is drained to the writer, so injected
    private data and PII never reach the persisted rows.
    """
    loop = asyncio.new_event_loop()
    try:
        bridge = EventBridge(session_id, audience="frontend_safe")
        norm_state = NormalizedStreamState()
        fwd_state = None
        for raw in raw_stream:
            for app_event in normalize_stream_event(
                raw, state=norm_state, default_agent_name=default_agent_name
            ):
                fwd_state = loop.run_until_complete(
                    forward_normalized_event(app_event, bridge=bridge, state=fwd_state)
                )
                _drain(bridge, writer)
        _drain(bridge, writer)
        writer.flush()
    finally:
        loop.close()


def _drain(bridge: EventBridge, writer: _Writer) -> None:
    while not bridge.stream_queue_empty():
        ui_event = bridge.stream_queue_get_nowait()
        row = ui_event.to_dict()
        writer.write(str(row["type"]), {"data": row["data"], "id": row["id"]})
