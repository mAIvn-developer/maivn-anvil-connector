# pyright: basic, reportMissingModuleSource=false
"""Collapsible live timeline of tool calls, system tools, and swarm assignments.

Skulpt-safe (no annotations/typing). Bind ``add_event`` to a MaivnSession's
tool/system/agent events. Starts collapsed; the header toggles visibility.
Theme-agnostic styling via ``maivn-feed-*`` classes.
"""

from ...markdown import escape_html
from ._anvil_designer import ActivityFeedTemplate

_LABELS = {
    "tool_event": "Tool",
    "system_tool_start": "System tool",
    "system_tool_complete": "System tool",
    "agent_assignment": "Agent",
    "status_message": "Status",
}


class ActivityFeed(ActivityFeedTemplate):
    def __init__(self, **properties):
        self._rows = []
        self._open = False
        self.init_components(**properties)
        self._render()

    def add_event(self, event):
        label = _LABELS.get(event.kind, event.kind)
        detail = event.text or self._summarize(event.payload)
        self._rows.append(
            f'<li class="maivn-feed-item">'
            f'<span class="maivn-feed-kind">{escape_html(label)}</span>'
            f'<span class="maivn-feed-detail">{escape_html(detail)}</span></li>'
        )
        self._render()

    def toggle(self, **event_args):
        self._open = not self._open
        self._render()

    @staticmethod
    def _summarize(payload):
        raw = payload.get("data")
        data = raw if isinstance(raw, dict) else {}
        for key in ("name", "tool", "agent_name", "title"):
            value = data.get(key)
            if value:
                return str(value)
        return ""

    def _render(self):
        count = len(self._rows)
        body = f'<ul class="maivn-feed-list">{"".join(self._rows)}</ul>' if self._open else ""
        caret = "v" if self._open else ">"
        self.html = (
            f'<div class="maivn-feed">'
            f'<button class="maivn-feed-header" onclick="anvil.call(this, \'toggle\')">'
            f"{caret} Activity ({count})</button>{body}</div>"
        )
