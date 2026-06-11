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
    "components.ExampleCards",
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


def test_shell_forms_provide_nav() -> None:
    """Pages render inside standard-page.html, whose header calls nav()."""
    for dotted in ["Home", "Docs", "Example_BasicChat"]:
        form = _form_class(dotted)()
        form.nav("Docs")
        form.nav("NotAForm")  # unknown targets are ignored, not opened


def test_template_applies_yaml_container_properties() -> None:
    prompt = _form_class("components.InterruptPrompt")()
    assert prompt.role == "maivn-interrupt"


@pytest.mark.parametrize("input_type", ["text", "boolean", "choice"])
def test_interrupt_prompt_variants(input_type: str) -> None:
    spec: dict[str, Any] = {"prompt": "Approve?", "input_type": input_type}
    if input_type == "choice":
        spec["choices"] = ["a", "b"]
    prompt = _form_class("components.InterruptPrompt")(spec=spec)
    assert isinstance(prompt, anvil.Component)
