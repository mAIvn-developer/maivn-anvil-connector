# pyright: basic, reportMissingModuleSource=false
from ..showcase import build_example
from ._anvil_designer import Example_InterruptApprovalTemplate

_SOURCE = """
from maivn import Agent, depends_on_interrupt
from maivn_anvil_connector import registry
from maivn_anvil_connector.interrupts import make_anvil_interrupt_handler

agent = Agent(name="interrupt_approval", api_key=API_KEY,
              system_prompt="Call delete_record before deleting anything.")

@agent.toolify(description="Delete a record after explicit approval")
@depends_on_interrupt(
    arg_name="confirmation",
    input_handler=make_anvil_interrupt_handler(input_type="boolean",
                                               prompt="Approve deleting this record?"),
)
def delete_record(confirmation: bool) -> dict:
    # Boolean interrupt: Anvil sends "yes"/"no"; the SDK coerces to bool.
    return {"deleted": confirmation}

registry.register_agent("interrupt_approval", agent)
""".strip()


class Example_InterruptApproval(Example_InterruptApprovalTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        build_example(
            self,
            agent_key="interrupt_approval",
            example="interrupt_approval",
            title="Human-in-the-loop approval",
            description="Ask it to delete a record; the run pauses for your yes/no, then resumes.",
            source=_SOURCE,
        )
