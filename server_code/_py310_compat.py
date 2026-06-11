"""Anvil server-runtime bootstrap.

Anvil auto-imports every server module at startup and prepends a line to each
one, so ``from __future__ import annotations`` is forbidden in ``server_code/``.
Every annotation is therefore evaluated at import time on the downlink worker,
which does not support PEP 585/604 syntax (``list[str]``, ``dict[str, Any]``,
``str | None``, subscripted ``collections.abc`` types, etc.).

Server modules in this package are therefore written **annotation-free**, like
``client_code/`` (Skulpt). Static typing for local dev/CI lives in tests and
pyright config, not in runtime annotations.

This module also backports ``datetime.UTC`` (3.11+) before any ``maivn`` import.
It is named with a leading underscore so Anvil auto-imports it before other
server modules during dependency startup.
"""

import datetime


def apply():
    if not hasattr(datetime, "UTC"):
        datetime.UTC = datetime.timezone.utc  # type: ignore[attr-defined]


apply()
