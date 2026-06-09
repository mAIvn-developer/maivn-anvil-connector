# pyright: basic
"""Message composer: text box + send button + attachment loader.

Skulpt-safe (no annotations/typing). Exposes ``text`` and ``attachments`` (a
list of Anvil Media) and raises 'x-send' when the user submits. The host clears
it via ``reset()`` after send.
"""

from anvil import Button, FileLoader, FlowPanel, TextArea


class Composer(FlowPanel):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._text = TextArea(placeholder="Send a message...", role="maivn-composer-input")
        self._loader = FileLoader(multiple=True, role="maivn-composer-files")
        self._send = Button(text="Send", role="maivn-composer-send", click=self._on_send)
        self.add_component(self._text)
        self.add_component(self._loader)
        self.add_component(self._send)

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
