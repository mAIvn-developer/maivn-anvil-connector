from __future__ import annotations

import anvil.server
import pytest
from maivn_anvil_connector import sessions


@pytest.fixture(autouse=True)
def _clear_owner_provider() -> None:
    sessions.set_owner_provider(None)


def test_current_owner_uses_get_session_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(anvil.server, "get_session_id", lambda: "browser-session-42", raising=False)
    assert sessions.current_owner() == "browser-session-42"


def test_current_owner_falls_back_to_session_attribute(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delattr(anvil.server, "get_session_id", raising=False)

    class _Session:
        session_id = "attr-session-99"

    monkeypatch.setattr(anvil.server, "session", _Session(), raising=False)
    assert sessions.current_owner() == "attr-session-99"
