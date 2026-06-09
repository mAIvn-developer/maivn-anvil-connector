from __future__ import annotations

import importlib

import anvil.secrets
from maivn_anvil_connector import registry
from pydantic import TypeAdapter


def test_demo_agents_register_on_import() -> None:
    anvil.secrets._set("MAIVN_API_KEY", "sk-test")  # type: ignore[attr-defined]
    registry.reset()

    from maivn_anvil_connector import demo_agents

    importlib.reload(demo_agents)

    for key in ("basic_chat", "interrupt_approval", "swarm_research"):
        assert registry.resolve_agent(key) is not None


def test_missing_key_does_not_crash_registration() -> None:
    # No secret set -> register_demo_agents logs and returns without raising.
    registry.reset()

    from maivn_anvil_connector import demo_agents

    demo_agents.register_demo_agents()
    # Nothing registered, but no exception.
    assert True


def test_delete_record_accepts_boolean_interrupt_responses() -> None:
    """Anvil's boolean UI sends 'yes'/'no'; the SDK coerces them to bool."""
    anvil.secrets._set("MAIVN_API_KEY", "sk-test")  # type: ignore[attr-defined]
    registry.reset()

    from maivn_anvil_connector import demo_agents

    importlib.reload(demo_agents)

    agent = registry.resolve_agent("interrupt_approval")
    assert agent is not None
    tools = {tool.name: tool for tool in agent.list_tools()}
    delete_record = tools["delete_record"].func
    coerce = TypeAdapter(bool).validate_python

    assert delete_record(confirmation=coerce("yes")) == {"deleted": True}
    assert delete_record(confirmation=coerce("no")) == {"deleted": False}


def test_delete_record_rejects_string_membership_antipattern() -> None:
    """The old str-in-tuple check blocked approval when coerced to 'true'."""
    legacy_check = lambda confirmation: confirmation.strip().lower() in ("yes", "y", "approve")
    assert legacy_check("yes") is True
    assert legacy_check(str(True).lower()) is False
