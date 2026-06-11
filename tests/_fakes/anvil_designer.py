"""Fake for Anvil's virtual ``_anvil_designer`` modules.

At Anvil runtime, every form package gets a synthesized ``_anvil_designer``
module whose ``<FormName>Template`` class subclasses the container declared in
the form's ``form_template.yaml`` and provides ``init_components``. This
meta-path finder mirrors that behaviour for tests so form modules import and
instantiate under the same contract they face in production: a form that
subclasses a raw container (instead of its template) has no ``init_components``
and fails here exactly as it would in the browser.
"""

from __future__ import annotations

import importlib.abc
import importlib.util
import re
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any

import anvil

_SUFFIX = "._anvil_designer"


def _container_spec(form_dir: Path) -> tuple[type[Any], dict[str, Any]]:
    """Read the container type and its default properties from form_template.yaml."""
    template_path = form_dir / "form_template.yaml"
    text = template_path.read_text(encoding="utf-8")
    type_match = re.search(r"^container:\n\s+type:\s*(\w+)", text, re.MULTILINE)
    if type_match is None:
        msg = f"No container type declared in {template_path}"
        raise ImportError(msg)
    container: type[Any] = getattr(anvil, type_match.group(1))
    role_match = re.search(r"^\s+role:\s*([\w-]+)\s*$", text, re.MULTILINE)
    defaults: dict[str, Any] = {"role": role_match.group(1)} if role_match else {}
    return container, defaults


def _make_template(name: str, container: type[Any], defaults: dict[str, Any]) -> type[Any]:
    def init_components(self: Any, **properties: Any) -> None:
        merged = {**defaults, **properties}
        container.__init__(self, **merged)

    return type(name, (container,), {"init_components": init_components})


class AnvilDesignerFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Synthesizes ``<form_package>._anvil_designer`` like the Anvil runtime."""

    def find_spec(
        self,
        fullname: str,
        path: object = None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        if not fullname.endswith(_SUFFIX):
            return None
        parent = sys.modules.get(fullname.removesuffix(_SUFFIX))
        if parent is None or getattr(parent, "__path__", None) is None:
            return None
        return importlib.util.spec_from_loader(fullname, self)

    def create_module(self, spec: ModuleSpec) -> ModuleType | None:
        return None

    def exec_module(self, module: ModuleType) -> None:
        parent_name = module.__name__.removesuffix(_SUFFIX)
        parent = sys.modules[parent_name]
        form_dir = Path(next(iter(parent.__path__)))
        form_name = parent_name.rsplit(".", 1)[-1]
        container, defaults = _container_spec(form_dir)
        setattr(module, f"{form_name}Template", _make_template(form_name, container, defaults))


def install() -> None:
    """Register the finder once on sys.meta_path."""
    if not any(isinstance(finder, AnvilDesignerFinder) for finder in sys.meta_path):
        sys.meta_path.append(AnvilDesignerFinder())
