# pyright: basic, reportMissingModuleSource=false
from ..shell import PageShell
from ..showcase import build_example
from ._anvil_designer import Example_SwarmResearchTemplate

_SOURCE = """
from maivn import Agent, Swarm
from maivn_anvil_connector import registry

researcher = Agent(name="researcher", api_key=API_KEY,
                   system_prompt="List the 3 most important points on a topic.")
writer = Agent(name="writer", api_key=API_KEY,
               system_prompt="Turn bullet points into one tight paragraph.")
registry.register_agent("swarm_research", Swarm(name="swarm_research",
                                                agents=[researcher, writer]))
""".strip()


class Example_SwarmResearch(Example_SwarmResearchTemplate, PageShell):
    def __init__(self, **properties):
        self.init_components(**properties)
        build_example(
            self,
            agent_key="swarm_research",
            example="swarm_research",
            title="Multi-agent research swarm",
            description="A researcher and a writer collaborate; watch the activity feed for "
            "agent assignments.",
            source=_SOURCE,
        )
