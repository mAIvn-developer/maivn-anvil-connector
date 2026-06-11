"""Agent registry. Anvil-runtime-safe (no annotations)."""

_agents = {}


class UnknownAgentError(KeyError):
    """Raised when a session references an unregistered agent key."""


def register_agent(key, agent):
    """Expose a maivn Agent/Swarm under a string key the client can request."""
    _agents[key] = agent


def resolve_agent(key):
    try:
        return _agents[key]
    except KeyError as exc:
        raise UnknownAgentError(
            f"No agent registered for key {key!r}. Call register_agent({key!r}, agent) at import."
        ) from exc


def reset():
    _agents.clear()
