"""Showcase usage limits. Anvil-runtime-safe (no annotations)."""

import anvil.server

EXAMPLE_DAILY_CAP = 20
EXAMPLE_MAX_CHARS = 4000

_counts = {}
_owner_provider = None


class UsageLimitError(anvil.server.AnvilWrappedError):
    """Raised when a showcase example exceeds its usage cap."""


def set_owner_provider(provider):
    global _owner_provider
    _owner_provider = provider


def _owner():
    if _owner_provider is not None:
        return _owner_provider()
    return "anonymous"


def enforce_start(*, example, messages):
    if example is None:
        return
    for m in messages:
        if len(str(m.get("content", ""))) > EXAMPLE_MAX_CHARS:
            raise UsageLimitError("Message too long for the demo. Try a shorter prompt.")
    key = f"{_owner()}::{example}"
    used = _counts.get(key, 0)
    if used >= EXAMPLE_DAILY_CAP:
        raise UsageLimitError("Daily demo limit reached. Add your own API key to run unlimited.")
    _counts[key] = used + 1


def reset():
    _counts.clear()
