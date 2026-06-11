from __future__ import annotations

import datetime
import importlib
import sys

import pytest


def test_py310_compat_backports_datetime_utc(monkeypatch: pytest.MonkeyPatch) -> None:
    if hasattr(datetime, "UTC"):
        monkeypatch.delattr(datetime, "UTC", raising=False)

    module_name = "maivn_anvil_connector._py310_compat"
    sys.modules.pop(module_name, None)
    importlib.import_module(module_name)

    assert datetime.UTC is datetime.timezone.utc


def test_package_import_applies_py310_compat() -> None:
    import maivn_anvil_connector  # noqa: F401

    assert datetime.UTC is datetime.timezone.utc
