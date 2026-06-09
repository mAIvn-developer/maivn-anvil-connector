from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_PKG_NAME = "maivn_anvil_connector"
_REPO_ROOT = Path(__file__).resolve().parents[1]
_FAKES_ROOT = Path(__file__).resolve().parent / "_fakes"


def _register_fake_anvil() -> None:
    """Put the fake ``anvil`` package on sys.path so server_code imports resolve."""
    fake_path = str(_FAKES_ROOT)
    if fake_path not in sys.path:
        sys.path.insert(0, fake_path)


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


_register_fake_anvil()
_register_anvil_package()


@pytest.fixture(autouse=True)
def _reset_anvil_state() -> None:
    import anvil.secrets
    import anvil.server
    import anvil.tables

    anvil.server.reset()
    anvil.secrets.reset()
    anvil.tables.reset()
