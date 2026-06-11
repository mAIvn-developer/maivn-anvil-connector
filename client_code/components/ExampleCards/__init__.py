# pyright: basic, reportMissingModuleSource=false
"""Clickable glass cards linking to the live example forms.

Skulpt-safe (no annotations/typing). Each card calls back into ``launch`` via
``anvil.call``; targets are validated against the card list because the call
originates from the DOM.
"""

from anvil import open_form

from ._anvil_designer import ExampleCardsTemplate

_CARDS = [
    {
        "form": "Example_BasicChat",
        "tag": "Agent",
        "title": "Basic streaming chat",
        "body": "A single agent answering with live token streaming.",
    },
    {
        "form": "Example_InterruptApproval",
        "tag": "Interrupts",
        "title": "Human-in-the-loop approval",
        "body": "The run pauses for your yes/no before a tool acts, then resumes.",
    },
    {
        "form": "Example_SwarmResearch",
        "tag": "Swarm",
        "title": "Multi-agent research swarm",
        "body": "A researcher and a writer collaborate; watch the activity feed.",
    },
]

_CARD = (
    "<button class=\"maivn-card\" onclick=\"anvil.call(this, 'launch', '{form}')\">"
    '<span class="maivn-card-tag">{tag}</span>'
    "<h3>{title}</h3>"
    "<p>{body}</p>"
    '<span class="maivn-card-link">Open example -&gt;</span>'
    "</button>"
)


class ExampleCards(ExampleCardsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        cards = "".join(_CARD.format(**card) for card in _CARDS)
        self.html = f'<div class="maivn-cards">{cards}</div>'

    def launch(self, form_name="", **event_args):
        if any(card["form"] == form_name for card in _CARDS):
            open_form(form_name)
