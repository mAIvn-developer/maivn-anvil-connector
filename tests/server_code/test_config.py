from __future__ import annotations

import anvil.secrets
import pytest
from maivn_anvil_connector import config


def test_resolve_api_key_from_secret() -> None:
    anvil.secrets._set("MAIVN_API_KEY", "sk-live")  # type: ignore[attr-defined]
    assert config.resolve_api_key() == "sk-live"


def test_resolve_api_key_explicit_override() -> None:
    assert config.resolve_api_key("sk-override") == "sk-override"


def test_missing_secret_raises_clear_error() -> None:
    with pytest.raises(config.MaivnConfigError):
        config.resolve_api_key()
