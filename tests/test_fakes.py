from __future__ import annotations

import anvil.secrets
import anvil.server
import anvil.tables as tables


def test_fake_secret_roundtrip() -> None:
    anvil.secrets._set("MAIVN_API_KEY", "sk-test")  # type: ignore[attr-defined]
    assert anvil.secrets.get_secret("MAIVN_API_KEY") == "sk-test"


def test_fake_callable_registers() -> None:
    @anvil.server.callable
    def ping() -> str:
        return "pong"

    assert anvil.server._registry["ping"]() == "pong"  # type: ignore[attr-defined]


def test_fake_table_add_and_search() -> None:
    t = tables.app_tables.maivn_events
    t.add_row(session_id="s1", seq=1, kind="final", payload={}, created=None)
    rows = t.search(session_id="s1")
    assert len(list(rows)) == 1
