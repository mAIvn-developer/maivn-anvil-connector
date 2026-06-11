"""Test/type double for the Anvil client API.

This package is the project's `anvil` resolution source for both pytest (runtime
behaviour) and basedpyright (types). It mirrors the *real* Anvil API surface the
connector uses so the type checker validates component usage; at Anvil runtime
the genuine `anvil` package is provided by the platform and this double is never
loaded. The classes here have trivial runtime bodies — tests do not instantiate
UI components, but the package must import cleanly and the signatures must match
Anvil so type checking is meaningful.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

# MARK: Component model


class Component:
    """Base Anvil component: a property bag with the shared component methods."""

    role: str | None
    visible: bool
    enabled: bool
    tag: Any

    def __init__(self, **properties: Any) -> None:
        self.role = properties.get("role")

    # NOTE: deliberately no ``init_components`` here. In real Anvil it exists only
    # on the designer-generated ``_anvil_designer`` templates (faked by the
    # ``anvil_designer`` meta-path finder), not on raw components — defining it on
    # Component would mask forms that subclass a raw container by mistake.

    def add_component(
        self,
        component: Component,
        *,
        slot: str | None = None,
        index: int | None = None,
        **layout: Any,
    ) -> None: ...

    def set_event_handler(self, event_name: str, handler: Callable[..., Any]) -> None: ...

    def raise_event(self, event_name: str, **event_args: Any) -> None: ...

    def clear(self) -> None: ...

    def remove_from_parent(self) -> None: ...


class Container(Component):
    """Layout container base."""


class ColumnPanel(Container): ...


class FlowPanel(Container): ...


class Label(Component):
    text: str

    def __init__(self, *, text: str = "", role: str | None = None, **properties: Any) -> None:
        super().__init__(role=role, **properties)
        self.text = text


class Button(Component):
    text: str

    def __init__(
        self,
        *,
        text: str = "",
        role: str | None = None,
        click: Callable[..., Any] | None = None,
        **properties: Any,
    ) -> None:
        super().__init__(role=role, **properties)
        self.text = text


class TextBox(Component):
    text: str

    def __init__(
        self, *, placeholder: str = "", text: str = "", role: str | None = None, **properties: Any
    ) -> None:
        super().__init__(role=role, **properties)
        self.text = text


class TextArea(Component):
    text: str

    def __init__(
        self, *, placeholder: str = "", text: str = "", role: str | None = None, **properties: Any
    ) -> None:
        super().__init__(role=role, **properties)
        self.text = text


class FileLoader(Component):
    files: list[Any]

    def __init__(
        self, *, multiple: bool = False, role: str | None = None, **properties: Any
    ) -> None:
        super().__init__(role=role, **properties)
        self.files = []

    def clear(self) -> None: ...


class Timer(Component):
    interval: float

    def __init__(self, *, interval: float = 0, **properties: Any) -> None:
        super().__init__(**properties)
        self.interval = interval


class DropDown(Component):
    items: list[Any]
    selected_value: Any

    def __init__(self, *, items: list[Any] | None = None, **properties: Any) -> None:
        super().__init__(**properties)
        self.items = items or []
        self.selected_value = None


class HtmlTemplate(Component):
    html: str

    def __init__(self, *, html: str = "", **properties: Any) -> None:
        super().__init__(**properties)
        self.html = html


def open_form(form: str | Component, *args: Any, **kwargs: Any) -> Component: ...
