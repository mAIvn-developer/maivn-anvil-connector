# pyright: basic
"""Shared behaviour for forms rendered inside the standard-page shell.

Skulpt-safe (no annotations/typing). The shell's header buttons call
``anvil.call(this, 'nav', '<FormName>')``, which Anvil routes to the enclosing
form, so every top-level form mixes this in. Targets are validated against an
allowlist because the call originates from the DOM.
"""

from anvil import open_form

_NAV_TARGETS = {
    "Home",
    "Docs",
    "Example_BasicChat",
    "Example_InterruptApproval",
    "Example_SwarmResearch",
}


class PageShell:
    """Mixin for forms whose container is ``@theme:standard-page.html``."""

    def nav(self, target="Home", **event_args):
        if target in _NAV_TARGETS:
            open_form(target)
