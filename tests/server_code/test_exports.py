from __future__ import annotations


def test_public_server_surface_is_submodule_style() -> None:
    from maivn_anvil_connector import attachments, interrupts, registry

    assert hasattr(registry, "register_agent")
    assert hasattr(interrupts, "make_anvil_interrupt_handler")
    assert hasattr(attachments, "media_to_attachment")


def test_deep_imports_resolve() -> None:
    from maivn_anvil_connector.config import resolve_api_key
    from maivn_anvil_connector.registry import register_agent

    assert callable(register_agent)
    assert callable(resolve_api_key)


def test_server_callables_are_defined() -> None:
    # Each @anvil.server.callable / @background_task entry point must exist as a
    # module attribute; Anvil imports every server module once at startup, which
    # is what performs the actual registration. (We avoid asserting on the live
    # registry here because the autouse reset + import caching make its contents
    # order-dependent, and reloading modules would mutate shared class identity.)
    from maivn_anvil_connector import drain, interrupts, runner, sessions

    assert callable(sessions.start_session)
    assert callable(sessions.cancel_session)
    assert callable(drain.drain_events)
    assert callable(interrupts.submit_interrupt)
    assert callable(runner.run_agent_session)
