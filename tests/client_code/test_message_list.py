# pyright: strict
from __future__ import annotations

from maivn_anvil_connector.components.MessageList import MessageList


def test_processing_indicator_is_rendered_and_cleared() -> None:
    transcript = MessageList()
    transcript.show_processing()
    assert "maivn-msg-processing" in transcript.html
    transcript.hide_processing()
    assert "maivn-msg-processing" not in transcript.html
