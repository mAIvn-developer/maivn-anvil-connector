from __future__ import annotations

import pytest
from maivn_anvil_connector import interrupts, tables


def test_handler_resolves_active_session_when_unset() -> None:
    token = interrupts.set_active_session("s-active")
    try:
        tables.put_interrupt(
            "s-active", interrupt_id="i1", prompt="?", input_type="text", choices=None
        )
        # No explicit session_id -> resolves from the active session.
        handler = interrupts.make_anvil_interrupt_handler(interrupt_id="i1", poll_seconds=0)
        tables.write_interrupt_response("s-active", "i1", "answer")
        assert handler("?") == "answer"
    finally:
        interrupts.reset_active_session(token)


def test_handler_without_session_raises() -> None:
    handler = interrupts.make_anvil_interrupt_handler(interrupt_id="i2", poll_seconds=0)
    with pytest.raises(RuntimeError):
        handler("?")
