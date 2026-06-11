# pyright: strict
"""Smoke tests: every form constructs under the real Anvil template contract.

``init_components`` only exists on the designer-generated ``_anvil_designer``
templates (faked faithfully in conftest), so a form that subclasses a raw
container fails here exactly as it does in the browser — the regression these
tests pin down.
"""

from __future__ import annotations

import importlib
from typing import Any

import anvil
import pytest

_FORMS = [
    "Startup",
    "Home",
    "Docs",
    "Example_BasicChat",
    "Example_InterruptApproval",
    "Example_SwarmResearch",
    "components.InterruptPrompt",
    "components.Composer",
    "components.MaivnChatPanel",
    "components.ActivityFeed",
    "components.MessageList",
    "components.PoweredByBadge",
]


def _form_class(dotted: str) -> type[Any]:
    module = importlib.import_module(f"maivn_anvil_connector.{dotted}")
    name = dotted.rsplit(".", 1)[-1]
    form_cls: type[Any] = getattr(module, name)
    return form_cls


@pytest.mark.parametrize("dotted", _FORMS)
def test_form_instantiates(dotted: str) -> None:
    form = _form_class(dotted)()
    assert isinstance(form, anvil.Component)


def test_template_applies_yaml_container_properties() -> None:
    home = _form_class("Home")()
    assert home.role == "maivn-chat"
