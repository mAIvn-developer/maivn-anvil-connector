# pyright: basic
"""Client-side session controller. Skulpt-safe (no annotations/typing).

Starts an agent run and drains its event stream behind a transport-agnostic
event API. ``call`` is injected (``anvil.server.call`` in production) so this
module has no direct server dependency.
"""

from .events import is_terminal, parse_row
from .poller import CadenceController


class MaivnSession:
    """Starts a run and drains its event stream via an injected `call`."""

    def __init__(self, agent_key, call, cadence=None, example=None):
        self._agent_key = agent_key
        self._call = call
        self._cadence = cadence or CadenceController()
        self._example = example
        self._handlers = {}
        self.session_id = None
        self.cursor = 0
        self.is_done = False
        self.next_interval = self._cadence.active

    def on(self, kind, handler):
        self._handlers.setdefault(kind, []).append(handler)

    def start(self, messages):
        self.session_id = self._call(
            "start_session",
            agent_key=self._agent_key,
            messages=messages,
            example=self._example,
        )

    def submit_interrupt(self, interrupt_id, response):
        self._call(
            "submit_interrupt",
            session_id=self.session_id,
            interrupt_id=interrupt_id,
            response=response,
        )

    def cancel(self):
        if self.session_id is not None:
            self._call("cancel_session", session_id=self.session_id)
        self.is_done = True

    def pump_once(self):
        if self.is_done or self.session_id is None:
            return self.next_interval
        rows = self._call("drain_events", session_id=self.session_id, after_seq=self.cursor) or []
        for row in rows:
            event = parse_row(row)
            self.cursor = max(self.cursor, event.seq)
            self._dispatch(event)
            if is_terminal(event.kind):
                self.is_done = True
        self.next_interval = self._cadence.next_interval(got_events=bool(rows))
        return self.next_interval

    def _dispatch(self, event):
        for handler in self._handlers.get(event.kind, []):
            handler(event)
