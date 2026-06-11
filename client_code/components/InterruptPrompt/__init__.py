# pyright: basic, reportMissingModuleSource=false
"""Renders the right input control for an interrupt and raises 'x-answer'.

Skulpt-safe (no annotations/typing). Supports input_type in
{'text', 'boolean', 'choice'}. The host (MaivnChatPanel) binds 'x-answer' and
forwards the value to MaivnSession.submit_interrupt.
"""

from anvil import Button, DropDown, Label, TextBox

from ...interrupt_controls import control_kind
from ._anvil_designer import InterruptPromptTemplate


class InterruptPrompt(InterruptPromptTemplate):
    def __init__(self, spec=None, **properties):
        self._spec = spec or {}
        self.init_components(**properties)

        prompt = str(self._spec.get("prompt") or "Input required")
        self.add_component(Label(text=prompt, role="maivn-interrupt-prompt"))

        self._kind = control_kind(self._spec.get("input_type"), self._spec.get("choices"))
        self._input = None
        if self._kind == "choice":
            self._input = DropDown(items=list(self._spec.get("choices") or []))
            self.add_component(self._input)
            self.add_component(
                Button(text="Submit", role="maivn-interrupt-submit", click=self._answer)
            )
        elif self._kind == "boolean":
            self.add_component(Button(text="Yes", click=lambda **e: self._send("yes")))
            self.add_component(Button(text="No", click=lambda **e: self._send("no")))
        else:
            self._input = TextBox(placeholder="Type your answer...")
            self.add_component(self._input)
            self.add_component(
                Button(text="Submit", role="maivn-interrupt-submit", click=self._answer)
            )

    def _answer(self, **event_args):
        attr = "selected_value" if self._kind == "choice" else "text"
        self._send(str(getattr(self._input, attr)))

    def _send(self, value):
        self.raise_event("x-answer", value=value)
