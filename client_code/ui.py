# pyright: basic
"""Tiny Skulpt-safe UI helpers shared by the showcase forms and components."""

from anvil import Button


def button(text, on_click, role=None):
    """Build a Button wired to a click handler.

    Anvil component constructors accept only properties; event handlers must be
    attached via ``set_event_handler``.
    """
    btn = Button(text=text, role=role)
    btn.set_event_handler("click", on_click)
    return btn
