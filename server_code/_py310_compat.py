"""Backport ``datetime.UTC`` for Anvil's Python 3.10 server runtime.

``maivn`` / ``maivn_shared`` use ``from datetime import UTC``, which was added
in Python 3.11. Anvil server code still runs on 3.10, so we patch the stdlib
module before any SDK import.

This module is named with a leading underscore so Anvil auto-imports it before
other server modules (for example ``demo_agents``) during dependency startup.
"""

import datetime


def apply() -> None:
    if not hasattr(datetime, "UTC"):
        datetime.UTC = datetime.timezone.utc  # type: ignore[attr-defined]


apply()
