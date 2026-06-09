# pyright: basic
from anvil import ColumnPanel

from ..showcase import build_example

_SOURCE = """
from maivn import Agent
from maivn_anvil_connector import registry

agent = Agent(name="basic_chat", description="A friendly assistant.",
              system_prompt="You are concise and friendly.", api_key=API_KEY)
registry.register_agent("basic_chat", agent)

# In a form:
from maivn_anvil_connector.components.MaivnChatPanel import MaivnChatPanel
self.add_component(MaivnChatPanel(agent_key="basic_chat"))
""".strip()


class Example_BasicChat(ColumnPanel):
    def __init__(self, **properties):
        self.init_components(**properties)
        build_example(
            self,
            agent_key="basic_chat",
            example="basic_chat",
            title="Basic streaming chat",
            description="A single agent answering with live token streaming.",
            source=_SOURCE,
        )
