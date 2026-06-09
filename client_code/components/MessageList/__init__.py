# pyright: basic
"""Scrolling transcript of user / assistant / tool / error bubbles.

Skulpt-safe (no annotations/typing). Theme-agnostic: bubbles use ``maivn-*`` CSS
classes that resolve against the host app's CSS variables (falling back to
neutral defaults). Markdown rendering lives in the pure, unit-tested
``maivn_anvil_connector.markdown`` module.
"""

from anvil import HtmlTemplate

from ...markdown import escape_html, render_markdown

_CONTAINER = '<div class="maivn-transcript-inner">{rows}</div>'


class MessageList(HtmlTemplate):
    def __init__(self, **properties):
        self._rows = []
        self._streaming_index = None
        self.init_components(**properties)
        self._render()

    # MARK: public API

    def add_user(self, text):
        self._rows.append(self._bubble("user", render_markdown(text)))
        self._streaming_index = None
        self._render()

    def update_streaming(self, text):
        bubble = self._bubble("assistant", render_markdown(text), streaming=True)
        if self._streaming_index is None:
            self._streaming_index = len(self._rows)
            self._rows.append(bubble)
        else:
            self._rows[self._streaming_index] = bubble
        self._render()

    def finalize_assistant(self, text, result=None):
        body = render_markdown(text)
        if result is not None:
            body += f'<pre class="maivn-result"><code>{escape_html(str(result))}</code></pre>'
        bubble = self._bubble("assistant", body)
        if self._streaming_index is not None:
            self._rows[self._streaming_index] = bubble
        else:
            self._rows.append(bubble)
        self._streaming_index = None
        self._render()

    def add_error(self, text):
        self._rows.append(self._bubble("error", escape_html(text)))
        self._streaming_index = None
        self._render()

    # MARK: internals

    @staticmethod
    def _bubble(role, body_html, streaming=False):
        cls = f"maivn-msg maivn-msg-{role}" + (" maivn-msg-streaming" if streaming else "")
        return f'<div class="{cls}"><div class="maivn-msg-body">{body_html}</div></div>'

    def _render(self):
        self.html = _CONTAINER.format(rows="".join(self._rows))
