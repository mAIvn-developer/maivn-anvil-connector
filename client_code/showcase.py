# pyright: basic
"""Shared layout for the showcase example forms (DRY chrome around a panel).

Skulpt-safe (no annotations/typing).
"""

from anvil import Button, HtmlTemplate, Label, open_form

from .components.MaivnChatPanel import MaivnChatPanel

_LIMITS_NOTE = (
    "Demo limited: capped messages/day and short responses. Install the SDK with "
    "your own MAIVN_API_KEY to run without limits."
)


def build_example(form, agent_key, example, title, description, source):
    """Populate a ColumnPanel form with a titled, runnable example + source."""
    form.role = "maivn-chat"
    form.add_component(Label(text=title, role="maivn-interrupt-prompt"))
    form.add_component(Label(text=description))
    form.add_component(MaivnChatPanel(agent_key=agent_key, example=example))
    form.add_component(HtmlTemplate(html=f'<p class="maivn-powered">{_LIMITS_NOTE}</p>'))
    form.add_component(
        HtmlTemplate(
            html=f'<details><summary>View source</summary><pre class="maivn-code">'
            f"<code>{_escape(source)}</code></pre></details>"
        )
    )
    form.add_component(Button(text="<- Back", click=lambda **e: open_form("Home")))


def _escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
