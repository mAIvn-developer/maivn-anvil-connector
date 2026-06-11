# pyright: basic, reportMissingModuleSource=false
"""Message composer: text box + send button + attachment loader.

Skulpt-safe (no annotations/typing). Exposes ``text`` and ``attachments`` (a
list of Anvil Media) and raises 'x-send' when the user submits. The host clears
it via ``reset()`` after send. Lays out via its own slotted HTML so the input
grows while the actions hug the right edge (Anvil's FlowPanel cannot flex).
"""

from anvil import FileLoader, TextArea

from ...ui import button
from ._anvil_designer import ComposerTemplate

_LAYOUT = (
    '<div class="maivn-composer">'
    '<div class="maivn-composer-grow" anvil-slot="input"></div>'
    '<div class="maivn-composer-actions" anvil-slot="actions"></div>'
    "</div>"
)


class Composer(ComposerTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.html = _LAYOUT
        self._text = TextArea(placeholder="Send a message...", role="maivn-composer-input")
        self._loader = FileLoader(multiple=True, role="maivn-composer-files")
        self._send = button("Send", self._on_send, role="maivn-composer-send")
        self.add_component(self._text, slot="input")
        self.add_component(self._loader, slot="actions")
        self.add_component(self._send, slot="actions")

    @property
    def text(self):
        return self._text.text or ""

    @property
    def attachments(self):
        files = self._loader.files
        return list(files) if files else []

    def reset(self):
        self._text.text = ""
        self._loader.clear()

    def _on_send(self, **event_args):
        if self.text.strip() or self.attachments:
            self.raise_event("x-send")
