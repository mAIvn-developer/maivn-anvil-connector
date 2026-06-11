# pyright: basic, reportMissingModuleSource=false
"""In-app Anvil + mAIvn integration guide.

Covers the Anvil-specific wiring only. The SDK reference (agents, tools,
swarms, structured output) lives at developer.maivn.io/docs and is linked, not
duplicated here. Skulpt-safe (no annotations/typing).
"""

from anvil import FlowPanel, HtmlTemplate, open_form

from ..shell import PageShell
from ..ui import button
from ._anvil_designer import DocsTemplate

_GUIDE = """
<div class="maivn-doc">
  <h1>Use mAIvn in your Anvil app</h1>
  <ol>
    <li><strong>Prerequisite:</strong> a paid Anvil plan (background tasks) with a
      Python 3.10+ server environment.</li>
    <li><strong>Install the SDK</strong> in your server packages: <code>maivn</code>.</li>
    <li><strong>Add this app as a dependency</strong> in your app's Dependencies.</li>
    <li><strong>Set the secret</strong> <code>MAIVN_API_KEY</code> (Anvil &rarr; Secrets).</li>
    <li><strong>Register your agent</strong> at server-module import time:
      <pre class="maivn-code"><code>from maivn import Agent
from maivn_anvil_connector import registry

agent = Agent(name="support", api_key=resolve_api_key(), system_prompt="...")
registry.register_agent("support", agent)</code></pre>
    </li>
    <li><strong>Drop in the UI</strong> on a client form:
      <pre class="maivn-code"><code>
from maivn_anvil_connector.components.MaivnChatPanel import MaivnChatPanel
self.add_component(MaivnChatPanel(agent_key="support"))</code></pre>
    </li>
  </ol>
  <p><strong>Security:</strong> events stream through a frontend-safe boundary, so
  injected <code>private_data</code> and PII are never persisted or sent to the
  browser. Your <code>@depends_on_private_data</code> tools work unchanged.</p>
</div>
""".strip()


class Docs(DocsTemplate, PageShell):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.add_component(HtmlTemplate(html=_GUIDE))
        row = FlowPanel()
        row.add_component(
            button("<- Back to home", lambda **e: open_form("Home"), role="maivn-btn-ghost")
        )
        row.add_component(
            button(
                "Full SDK reference ->",
                lambda **e: _open_url("https://developer.maivn.io/docs"),
                role="maivn-btn-secondary",
            )
        )
        self.add_component(row)


def _open_url(url):
    from anvil.js.window import open as _open

    _open(url, "_blank")
