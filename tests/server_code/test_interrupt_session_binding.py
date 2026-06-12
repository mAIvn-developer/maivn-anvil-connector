from __future__ import annotations

import threading

import pytest
from maivn_anvil_connector import interrupts, tables


def test_handler_resolves_active_session_when_unset() -> None:
    token = interrupts.set_active_session("s-active")
    try:
        tables.put_interrupt(
            "s-active", interrupt_id="i1", prompt="?", input_type="text", choices=None
        )
        handler = interrupts.make_anvil_interrupt_handler(interrupt_id="i1", poll_seconds=0)
        tables.write_interrupt_response("s-active", "i1", "answer")
        assert handler("?") == "answer"
    finally:
        interrupts.reset_active_session(token)


def test_handler_falls_back_to_thread_local_session() -> None:
    """Active session binding works on a worker thread (Anvil background-task path)."""
    results: list[str] = []
    ready = threading.Event()
    release = threading.Event()

    def worker() -> None:
        token = interrupts.set_active_session("s-thread")
        try:
            tables.put_interrupt(
                "s-thread", interrupt_id="i3", prompt="?", input_type="text", choices=None
            )
            handler = interrupts.make_anvil_interrupt_handler(interrupt_id="i3", poll_seconds=0)
            ready.set()
            release.wait(timeout=2.0)
            results.append(handler("?"))
        finally:
            interrupts.reset_active_session(token)

    thread = threading.Thread(target=worker)
    thread.start()
    assert ready.wait(timeout=2.0)
    tables.write_interrupt_response("s-thread", "i3", "thread-answer")
    release.set()
    thread.join(timeout=2.0)
    assert results == ["thread-answer"]


def test_handler_without_session_raises() -> None:
    handler = interrupts.make_anvil_interrupt_handler(interrupt_id="i2", poll_seconds=0)
    with pytest.raises(RuntimeError):
        handler("?")
