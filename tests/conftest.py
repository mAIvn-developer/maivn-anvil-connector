# pyright: strict
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_PKG_NAME = "maivn_anvil_connector"
_REPO_ROOT = Path(__file__).resolve().parents[1]


def _register_anvil_package() -> None:
    """Load the Anvil dependency app root as ``maivn_anvil_connector``."""
    if _PKG_NAME in sys.modules:
        return
    init_path = _REPO_ROOT / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        _PKG_NAME,
        init_path,
        submodule_search_locations=[
            str(_REPO_ROOT / "server_code"),
            str(_REPO_ROOT / "client_code"),
        ],
    )
    if spec is None or spec.loader is None:
        msg = f"Could not load {_PKG_NAME} from {init_path}"
        raise ImportError(msg)
    module = importlib.util.module_from_spec(spec)
    sys.modules[_PKG_NAME] = module
    spec.loader.exec_module(module)


_register_anvil_package()
