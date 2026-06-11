# pyright: basic
"""Shared layout for the showcase example forms (DRY chrome around a panel).

Skulpt-safe (no annotations/typing). The forms render inside the
standard-page shell; this adds the page head, chat panel, and footer chrome.
"""

from anvil import HtmlTemplate, open_form

from .components.MaivnChatPanel import MaivnChatPanel
from .ui import button

_LIMITS_NOTE = (
    "Demo limited: capped messages/day and short responses. Install the SDK with "
    "your own MAIVN_API_KEY to run without limits."
)


def build_example(form, agent_key, example, title, description, source):
    """Populate a shell form with a titled, runnable example + source."""
    head = (
        f'<div class="maivn-page-head"><h2>{_escape(title)}</h2><p>{_escape(description)}</p></div>'
    )
    form.add_component(HtmlTemplate(html=head))
    form.add_component(MaivnChatPanel(agent_key=agent_key, example=example))
    form.add_component(HtmlTemplate(html=f'<p class="maivn-note">{_LIMITS_NOTE}</p>'))
    form.add_component(
        HtmlTemplate(
            html='<details class="maivn-source"><summary>View source</summary>'
            f'<pre class="maivn-code"><code>{_escape(source)}</code></pre></details>'
        )
    )
    form.add_component(
        button("<- All examples", lambda **e: open_form("Home"), role="maivn-btn-ghost")
    )


def _escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
