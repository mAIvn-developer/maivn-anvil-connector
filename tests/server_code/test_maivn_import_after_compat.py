from __future__ import annotations

import importlib


def test_maivn_shared_imports_after_runtime_compat() -> None:
    """Smoke-test the Anvil 3.10 backports against the installed maivn stack."""
    importlib.import_module("maivn_anvil_connector._py310_compat")
    importlib.import_module("maivn_shared.domain.entities.session_config._helpers")
