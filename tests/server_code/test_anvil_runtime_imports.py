from __future__ import annotations

import importlib
from pathlib import Path


def test_all_server_modules_import_in_anvil_load_order() -> None:
    """Every server module must import on Anvil's Python 3.10 runtime.

    Anvil auto-imports dependency server modules at startup (alphabetically) and
    forbids ``from __future__ import annotations`` in server modules, so any
    runtime-evaluated annotation mistake surfaces here.
    """
    server_dir = Path(__file__).resolve().parents[2] / "server_code"
    module_names = sorted(
        path.stem for path in server_dir.glob("*.py") if path.name not in {"__init__.py"}
    )
    assert module_names[0] == "_py310_compat"

    for name in module_names:
        importlib.import_module(f"maivn_anvil_connector.{name}")
