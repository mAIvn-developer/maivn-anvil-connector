# pyright: basic
"""Demo agents registered for the hosted showcase examples.

Constructed at import time (Anvil auto-imports server modules at startup) using
the App Secret API key. Each construction is guarded so a missing key or any
build error degrades gracefully (logs + skips) instead of crashing the server.

Usage caps for these examples live in ``limits.py`` and are enforced by
``start_session`` when an ``example`` key is supplied.
"""

from typing import Any

from maivn import Agent, Swarm, depends_on_interrupt

from . import (
    _py310_compat,  # noqa: F401
    registry,
)
from .config import MaivnConfigError, resolve_api_key
from .interrupts import make_anvil_interrupt_handler


def _api_key() -> str | None:
    try:
        return resolve_api_key()
    except MaivnConfigError:
        print("[maivn-connector] MAIVN_API_KEY not set; demo agents not registered.")
        return None


def _build_basic_chat(api_key: str) -> Agent:
    return Agent(
        name="basic_chat",
        description="A friendly general-purpose assistant.",
        system_prompt=(
            "You are a concise, friendly assistant in a mAIvn demo. Keep answers short."
        ),
        api_key=api_key,
    )


def _build_interrupt_approval(api_key: str) -> Agent:
    agent = Agent(
        name="interrupt_approval",
        description="Demonstrates a human-in-the-loop approval gate.",
        system_prompt=(
            "You help the user manage records. Before deleting anything, you MUST call "
            "delete_record, which requires explicit human approval."
        ),
        api_key=api_key,
    )

    @agent.toolify(description="Delete a record after explicit human approval")
    @depends_on_interrupt(
        arg_name="confirmation",
        input_handler=make_anvil_interrupt_handler(
            input_type="boolean", prompt="Approve deleting this record?"
        ),
        prompt="Approve deleting this record?",
    )
    def delete_record(confirmation: bool) -> dict[str, Any]:
        # Boolean interrupt: Anvil sends "yes"/"no"; the SDK coerces to bool.
        return {"deleted": confirmation}

    return agent


def _build_swarm_research(api_key: str) -> Swarm:
    researcher = Agent(
        name="researcher",
        description="Gathers and summarizes key points.",
        system_prompt="You research a topic and list the 3 most important points.",
        api_key=api_key,
    )
    writer = Agent(
        name="writer",
        description="Turns research points into a short paragraph.",
        system_prompt="You turn bullet points into one tight paragraph.",
        api_key=api_key,
    )
    return Swarm(name="swarm_research", agents=[researcher, writer])


_BUILDERS = {
    "basic_chat": _build_basic_chat,
    "interrupt_approval": _build_interrupt_approval,
    "swarm_research": _build_swarm_research,
}


def register_demo_agents() -> None:
    api_key = _api_key()
    if api_key is None:
        return
    for key, build in _BUILDERS.items():
        try:
            registry.register_agent(key, build(api_key))
        except Exception as exc:  # noqa: BLE001 - one bad demo must not break the others
            print(f"[maivn-connector] demo agent {key!r} failed to build: {type(exc).__name__}")


register_demo_agents()
