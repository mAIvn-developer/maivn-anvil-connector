# This repository is an Anvil dependency app. Learn more at https://anvil.works/
# To run server-side code locally with the Anvil App Server, see README.md.

from __future__ import annotations

import datetime
import os
import typing

if not hasattr(datetime, "UTC"):
    datetime.UTC = datetime.timezone.utc  # type: ignore[attr-defined]

if not hasattr(typing, "Self"):
    try:
        from typing_extensions import Self
    except ImportError:
        Self = typing.TypeVar("Self")
    typing.Self = Self  # type: ignore[attr-defined]

__path__ = [
    os.path.join(os.path.dirname(__file__), "server_code"),
    os.path.join(os.path.dirname(__file__), "client_code"),
]
