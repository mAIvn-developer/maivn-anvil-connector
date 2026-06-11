"""Anvil server-runtime bootstrap (Python 3.10).

Anvil auto-imports every server module at startup and prepends a line to each
one, so ``from __future__ import annotations`` is forbidden in ``server_code/``.
Every annotation is therefore evaluated at import time.

Constraints on hosted Anvil (see README "Anvil server runtime"):

- ``datetime.UTC`` is 3.11+; patch it before importing ``maivn``.
- Do not subscript ``collections.abc`` generics (``Callable``, ``Iterable``,
  etc.) at module level or in annotations; use ``typing.Callable``,
  ``typing.Iterable``, and friends instead.
- ``list[str]``, ``dict[str, Any]``, and ``str | None`` are fine on 3.10.

This module is named with a leading underscore so Anvil auto-imports it before
other server modules during dependency startup.
"""

import datetime


def apply() -> None:
    if not hasattr(datetime, "UTC"):
        datetime.UTC = datetime.timezone.utc  # type: ignore[attr-defined]


apply()
