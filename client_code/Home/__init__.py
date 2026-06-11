# pyright: basic, reportMissingModuleSource=false
"""Branded showcase landing page. Skulpt-safe (no annotations/typing).

Hero + CTAs + example cards, rendered inside the standard-page shell. The SDK
reference is NOT duplicated here, per the docs policy; the shell header links
out to developer.maivn.io.
"""

from anvil import FlowPanel, HtmlTemplate, Label, open_form

from ..components.ExampleCards import ExampleCards
from ..shell import PageShell
from ..ui import button
from ._anvil_designer import HomeTemplate

_HERO = """
<div class="maivn-hero">
  <span class="maivn-hero-badge">Anvil + mAIvn</span>
  <h1 class="maivn-hero-title">Drop a streaming
    <span class="maivn-text-gradient">AI&nbsp;agent</span><br>into your Anvil app</h1>
  <p class="maivn-hero-sub">Install the mAIvn SDK in your server environment, add this app
  as a dependency, and wire your agent to a polished chat UI &mdash; live streaming,
  human-in-the-loop interrupts, and multi-agent swarms included.</p>
</div>
""".strip()


class Home(HomeTemplate, PageShell):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.add_component(HtmlTemplate(html=_HERO))

        ctas = FlowPanel(align="center")
        ctas.add_component(
            button(
                "Try the basic chat",
                lambda **e: open_form("Example_BasicChat"),
                role="maivn-btn-primary",
            )
        )
        ctas.add_component(
            button(
                "Read the integration guide",
                lambda **e: open_form("Docs"),
                role="maivn-btn-secondary",
            )
        )
        self.add_component(ctas)

        self.add_component(Label(text="Live examples", role="maivn-section-label"))
        self.add_component(ExampleCards())
