# pyright: basic
"""Branded showcase landing page. Skulpt-safe (no annotations/typing).

Shows the mAIvn wordmark, a short intro, navigation to the runnable examples,
and a link out to the SDK reference docs at developer.maivn.io/docs (the SDK
reference is NOT duplicated here, per the docs policy).
"""

from anvil import Button, ColumnPanel, HtmlTemplate, Label, open_form

_HERO = """
<div class="maivn-hero">
  <img class="maivn-logo" src="_/theme/maivn_logo_light_mode.svg" alt="mAIvn"
       onerror="this.style.display='none'"/>
  <h1 class="maivn-hero-title">mAIvn for Anvil</h1>
  <p class="maivn-hero-sub">
    Drop a streaming AI agent into any Anvil app. Install the mAIvn SDK in your
    server, add this app as a dependency, and wire your agent to a chat UI.
  </p>
</div>
""".strip()


class Home(ColumnPanel):
    def __init__(self, **properties):
        self.role = "maivn-chat"
        self.init_components(**properties)
        self.add_component(HtmlTemplate(html=_HERO))

        self.add_component(Label(text="Live examples", role="maivn-interrupt-prompt"))
        self.add_component(
            Button(text="Basic chat", click=lambda **e: open_form("Example_BasicChat"))
        )
        self.add_component(
            Button(
                text="Approval gate (interrupts)",
                click=lambda **e: open_form("Example_InterruptApproval"),
            )
        )
        self.add_component(
            Button(text="Research swarm", click=lambda **e: open_form("Example_SwarmResearch"))
        )

        self.add_component(Label(text="Learn", role="maivn-interrupt-prompt"))
        self.add_component(Button(text="Anvil + mAIvn guide", click=lambda **e: open_form("Docs")))
        self.add_component(
            Button(
                text="SDK reference (developer.maivn.io) ->",
                click=lambda **e: anvil_open_url("https://developer.maivn.io/docs"),
            )
        )


def anvil_open_url(url):
    from anvil.js.window import open as _open

    _open(url, "_blank")
