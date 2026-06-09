from __future__ import annotations

import pytest
from maivn_anvil_connector import registry


class _FakeAgent:
    name = "demo"


def test_register_and_resolve() -> None:
    registry.reset()
    agent = _FakeAgent()
    registry.register_agent("demo", agent)
    assert registry.resolve_agent("demo") is agent


def test_resolve_unknown_raises() -> None:
    registry.reset()
    with pytest.raises(registry.UnknownAgentError):
        registry.resolve_agent("missing")


def test_register_duplicate_replaces() -> None:
    registry.reset()
    registry.register_agent("demo", _FakeAgent())
    second = _FakeAgent()
    registry.register_agent("demo", second)
    assert registry.resolve_agent("demo") is second
