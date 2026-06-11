import contextvars
import time
import uuid
from typing import Callable

import anvil.server

from . import sessions, tables

# Set by the runner around a streamed turn so a session-less interrupt handler
# (constructed at agent-definition time) can resolve the live session at call
# time. Same-thread synchronous propagation makes this visible to tool
# execution during stream iteration.
_active_session: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "maivn_active_session", default=None
)


def set_active_session(session_id: str) -> contextvars.Token[str | None]:
    return _active_session.set(session_id)


def reset_active_session(token: contextvars.Token[str | None]) -> None:
    _active_session.reset(token)


def active_session() -> str | None:
    return _active_session.get()


def make_anvil_interrupt_handler(
    session_id: str | None = None,
    *,
    interrupt_id: str | None = None,
    prompt: str = "",
    input_type: str = "text",
    choices: list[str] | None = None,
    is_private: bool = False,
    poll_seconds: float = 0.5,
    timeout_seconds: float = 600.0,
) -> Callable[[str], str]:
    """Return a blocking input_handler for ``@depends_on_interrupt``.

    Writes an interrupt request, emits an interrupt_required event, then
    block-polls maivn_io for the client's response. Responses are deleted
    immediately after consumption (data minimization for private values).

    ``session_id`` may be omitted when the handler is attached at
    agent-definition time; it is then resolved from the active session the
    runner binds around the turn.
    """
    iid = interrupt_id or str(uuid.uuid4())

    def handler(handler_prompt: str) -> str:
        sid = session_id or active_session()
        if sid is None:
            raise RuntimeError(
                "No active mAIvn session for interrupt; the connector runner binds one "
                "around each turn. Pass session_id explicitly when calling outside a run."
            )
        if not tables.interrupt_exists(sid, iid):
            tables.put_interrupt(
                sid,
                interrupt_id=iid,
                prompt=handler_prompt or prompt,
                input_type=input_type,
                choices=choices,
                is_private=is_private,
            )
            tables.append_event(
                sid,
                seq=1_500_000_000,
                kind="interrupt_required",
                payload={
                    "data": {
                        "interrupt_id": iid,
                        "prompt": handler_prompt or prompt,
                        "input_type": input_type,
                        "choices": choices,
                    }
                },
            )
        deadline = time.monotonic() + timeout_seconds
        while True:
            response = tables.read_interrupt_response(sid, iid)
            if response is not None:
                tables.clear_interrupt(sid, iid)
                return response
            if time.monotonic() >= deadline:
                tables.clear_interrupt(sid, iid)
                raise TimeoutError(f"Interrupt {iid} timed out")
            time.sleep(poll_seconds)

    return handler


@anvil.server.callable
def submit_interrupt(*, session_id: str, interrupt_id: str, response: str) -> None:
    if sessions.owner_of(session_id) != sessions.current_owner():
        from .drain import NotAuthorizedError

        raise NotAuthorizedError("Not authorized for this session.")
    tables.write_interrupt_response(session_id, interrupt_id, response)
