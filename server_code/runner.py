from typing import Any

import anvil.server

from . import interrupts, registry, tables
from .events_writer import EventsWriter
from .messages import to_sdk_messages
from .pump import run_stream_to_writer

_ERROR_SENTINEL_SEQ = 2_000_000_000


@anvil.server.background_task
def run_agent_session(*, session_id: str, agent_key: str, messages: list[dict[str, Any]]) -> None:
    """Background task: stream the registered agent and persist sanitized events."""
    writer = EventsWriter(
        session_id,
        append=lambda *, seq, kind, payload: tables.append_event(
            session_id, seq=seq, kind=kind, payload=payload
        ),
    )
    token = interrupts.set_active_session(session_id)
    try:
        agent = registry.resolve_agent(agent_key)
        run_stream_to_writer(
            session_id=session_id,
            raw_stream=agent.stream(to_sdk_messages(messages), status_messages=True),
            writer=writer,
            default_agent_name=getattr(agent, "name", None),
        )
    except Exception as exc:  # noqa: BLE001 - surface any failure to the client as an error event
        writer.flush()
        tables.append_event(
            session_id,
            seq=_ERROR_SENTINEL_SEQ,
            kind="error",
            payload={"data": {"message": "The agent run failed. Please try again."}},
        )
        _log_internal(session_id, exc)
    finally:
        interrupts.reset_active_session(token)


def _log_internal(session_id: str, exc: Exception) -> None:
    print(f"[maivn-connector] session {session_id} failed: {type(exc).__name__}")
