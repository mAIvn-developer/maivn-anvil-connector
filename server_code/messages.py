from __future__ import annotations

from typing import Any

from maivn.messages import AIMessage, BaseMessage, HumanMessage

from .attachments import media_to_attachment


def _coerce_attachments(raw: Any) -> list[dict[str, Any]]:
    """Normalize a message's attachments into SDK attachment payloads.

    Accepts already-built payload dicts or Anvil ``Media`` objects (converted
    server-side to base64).
    """
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:  # type: ignore[misc]
        if isinstance(item, dict):
            out.append(item)
        elif hasattr(item, "get_bytes"):
            out.append(media_to_attachment(item))
    return out


def to_sdk_messages(messages: list[dict[str, Any]]) -> list[BaseMessage]:
    """Convert client-side role/content dicts into SDK message objects."""
    out: list[BaseMessage] = []
    for m in messages:
        content = str(m.get("content", ""))
        attachments = _coerce_attachments(m.get("attachments"))
        if m.get("role") == "assistant":
            out.append(AIMessage(content=content))
        elif attachments:
            out.append(
                HumanMessage(
                    content=content, attachments=attachments, allow_attachment_file_paths=False
                )
            )
        else:
            out.append(HumanMessage(content=content))
    return out
