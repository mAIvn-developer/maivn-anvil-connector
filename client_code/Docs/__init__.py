# pyright: basic, reportMissingModuleSource=false
"""In-app Anvil + mAIvn integration guide.

Covers the Anvil-specific wiring only. The SDK reference (agents, tools,
swarms, structured output) lives at developer.maivn.io/docs and is linked, not
duplicated here. Skulpt-safe (no annotations/typing).
"""

from anvil import Button, HtmlTemplate, open_form

from ._anvil_designer import DocsTemplate

_GUIDE = """
<div class="maivn-chat">
  <h1>Use mAIvn in your Anvil app</h1>
  <ol>
    <li><strong>Prerequisite:</strong> a paid Anvil plan (background tasks).</li>
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


class Docs(DocsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.add_component(HtmlTemplate(html=_GUIDE))
        self.add_component(
            Button(
                text="Full SDK reference (developer.maivn.io) ->",
                click=lambda **e: _open_url("https://developer.maivn.io/docs"),
            )
        )
        self.add_component(Button(text="<- Home", click=lambda **e: open_form("Home")))


def _open_url(url):
    from anvil.js.window import open as _open

    _open(url, "_blank")
