from __future__ import annotations

from maivn.messages import AIMessage, HumanMessage
from maivn_anvil_connector.messages import to_sdk_messages


def test_user_and_assistant_roles_map() -> None:
    out = to_sdk_messages(
        [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ]
    )
    assert isinstance(out[0], HumanMessage)
    assert isinstance(out[1], AIMessage)
    assert out[0].content == "hi"


def test_unknown_role_defaults_to_human() -> None:
    out = to_sdk_messages([{"role": "system-ish", "content": "x"}])
    assert isinstance(out[0], HumanMessage)


def test_media_attachment_is_converted_onto_message() -> None:
    from anvil.media import Media

    media = Media(b"%PDF fake", "application/pdf", "doc.pdf")
    out = to_sdk_messages([{"role": "user", "content": "see attached", "attachments": [media]}])
    assert isinstance(out[0], HumanMessage)
    attached = out[0].additional_kwargs.get("attachments")
    assert attached and attached[0]["name"] == "doc.pdf"
