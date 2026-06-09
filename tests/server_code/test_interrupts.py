from __future__ import annotations

import pytest
from maivn_anvil_connector import interrupts, sessions, tables
from maivn_anvil_connector.drain import NotAuthorizedError


def test_handler_returns_submitted_response() -> None:
    sessions.reset()
    sessions.set_owner_provider(lambda: "owner-A")
    sessions.bind_owner("s1", "owner-A")  # simulate a started session
    tables.put_interrupt("s1", interrupt_id="i1", prompt="Name?", input_type="text", choices=None)
    interrupts.submit_interrupt(session_id="s1", interrupt_id="i1", response="Ada")

    handler = interrupts.make_anvil_interrupt_handler("s1", interrupt_id="i1", poll_seconds=0)
    assert handler("Name?") == "Ada"


def test_private_response_is_deleted_after_consume() -> None:
    sessions.reset()
    sessions.set_owner_provider(lambda: "owner-A")
    sessions.bind_owner("s1", "owner-A")
    tables.put_interrupt(
        "s1", interrupt_id="i2", prompt="SSN?", input_type="text", choices=None, is_private=True
    )
    interrupts.submit_interrupt(session_id="s1", interrupt_id="i2", response="123-45-6789")

    handler = interrupts.make_anvil_interrupt_handler("s1", interrupt_id="i2", poll_seconds=0)
    assert handler("SSN?") == "123-45-6789"
    # Row is gone (data minimization) so the secret is not left at rest.
    assert tables.read_interrupt_response("s1", "i2") is None


def test_submit_rejects_foreign_owner() -> None:
    sessions.reset()
    sessions.set_owner_provider(lambda: "owner-A")
    sessions.bind_owner("s9", "owner-A")
    tables.put_interrupt("s9", interrupt_id="i9", prompt="?", input_type="text", choices=None)

    sessions.set_owner_provider(lambda: "attacker")
    with pytest.raises(NotAuthorizedError):
        interrupts.submit_interrupt(session_id="s9", interrupt_id="i9", response="x")
