from __future__ import annotations

from typing import Any

_agents: dict[str, Any] = {}


class UnknownAgentError(KeyError):
    """Raised when a session references an unregistered agent key."""


def register_agent(key: str, agent: Any) -> None:
    """Expose a maivn Agent/Swarm under a string key the client can request."""
    _agents[key] = agent


def resolve_agent(key: str) -> Any:
    try:
        return _agents[key]
    except KeyError as exc:
        raise UnknownAgentError(
            f"No agent registered for key {key!r}. Call register_agent({key!r}, agent) at import."
        ) from exc


def reset() -> None:
    _agents.clear()
