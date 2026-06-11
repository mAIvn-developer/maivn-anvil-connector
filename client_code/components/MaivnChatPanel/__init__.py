# pyright: basic, reportMissingModuleSource=false
"""The one-line drop-in: a complete streaming agent chat surface.

Skulpt-safe (no annotations/typing).

Usage in a consuming Anvil app (after adding this app as a dependency)::

    from maivn_anvil_connector.components.MaivnChatPanel import MaivnChatPanel
    self.add_component(MaivnChatPanel(agent_key="support"))

Wires a MessageList transcript, an ActivityFeed, a Composer, and interrupt
prompts to a MaivnSession, polled by an Anvil Timer with adaptive cadence. The
component is theme-agnostic (inherits the host app's theme); the optional
"Powered by mAIvn" badge can be turned off with ``show_badge=False``.
"""

import anvil.server
from anvil import Timer

from ...session import MaivnSession
from ..ActivityFeed import ActivityFeed
from ..Composer import Composer
from ..InterruptPrompt import InterruptPrompt
from ..MessageList import MessageList
from ..PoweredByBadge import PoweredByBadge
from ._anvil_designer import MaivnChatPanelTemplate


class MaivnChatPanel(MaivnChatPanelTemplate):
    def __init__(self, agent_key="", example=None, show_badge=True, **properties):
        self.agent_key = agent_key
        self.example = example
        self.init_components(**properties)

        self._messages = []
        self._session = None
        self._current_text = ""

        self._transcript = MessageList()
        self._feed = ActivityFeed()
        self._composer = Composer()
        self._composer.set_event_handler("x-send", self._on_send)
        self._timer = Timer(interval=0)
        self._timer.set_event_handler("tick", self._on_tick)

        self.add_component(self._transcript)
        self.add_component(self._feed)
        self.add_component(self._composer)
        self.add_component(self._timer)
        if show_badge:
            self.add_component(PoweredByBadge())

    # MARK: send + poll loop

    def _on_send(self, **event_args):
        text = self._composer.text
        attachments = self._composer.attachments
        if not text.strip() and not attachments:
            return

        turn = {"role": "user", "content": text}
        if attachments:
            turn = {**turn, "attachments": attachments}
        self._messages.append(turn)
        self._transcript.add_user(text)
        self._composer.reset()
        self._current_text = ""

        self._session = MaivnSession(
            agent_key=self.agent_key, call=anvil.server.call, example=self.example
        )
        self._session.on("assistant_chunk", self._on_chunk)
        self._session.on("final", self._on_final)
        self._session.on("error", self._on_error)
        self._session.on("interrupt_required", self._on_interrupt)
        self._session.on("tool_event", self._feed.add_event)
        self._session.on("system_tool_start", self._feed.add_event)
        self._session.on("system_tool_complete", self._feed.add_event)
        self._session.on("agent_assignment", self._feed.add_event)
        self._session.on("status_message", self._feed.add_event)
        self._session.start(messages=self._messages)
        self._timer.interval = self._session.next_interval

    def _on_tick(self, **event_args):
        if self._session is None:
            return
        interval = self._session.pump_once()
        self._timer.interval = 0 if self._session.is_done else interval

    # MARK: event handlers

    def _on_chunk(self, event):
        self._current_text += event.text
        self._transcript.update_streaming(self._current_text)

    def _on_final(self, event):
        self._transcript.finalize_assistant(event.text, event.result)
        self._messages.append({"role": "assistant", "content": event.text})

    def _on_error(self, event):
        self._transcript.add_error(event.text or "Something went wrong.")

    def _on_interrupt(self, event):
        data = event.payload.get("data", {}) if isinstance(event.payload, dict) else {}
        prompt = InterruptPrompt(spec=data)
        prompt.set_event_handler("x-answer", self._make_answer(str(data.get("interrupt_id"))))
        self.add_component(prompt)

    def _make_answer(self, interrupt_id):
        def answer(value="", **event_args):
            if self._session is not None:
                self._session.submit_interrupt(interrupt_id=interrupt_id, response=value)

        return answer
