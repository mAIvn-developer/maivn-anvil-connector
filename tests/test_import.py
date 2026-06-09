from __future__ import annotations

import maivn_anvil_connector
from maivn_anvil_connector import version


def test_package_is_importable() -> None:
    assert maivn_anvil_connector is not None


def test_version() -> None:
    assert version.__version__ == "0.1.0"
