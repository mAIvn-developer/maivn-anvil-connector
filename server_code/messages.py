"""SDK message conversion. Anvil-runtime-safe (no annotations)."""

from maivn.messages import AIMessage, HumanMessage

from . import _py310_compat  # noqa: F401
from .attachments import media_to_attachment


def _coerce_attachments(raw):
    """Normalize a message's attachments into SDK attachment payloads.

    Accepts already-built payload dicts or Anvil ``Media`` objects (converted
    server-side to base64).
    """
    if not isinstance(raw, list):
        return []
    out = []
    for item in raw:
        if isinstance(item, dict):
            out.append(item)
        elif hasattr(item, "get_bytes"):
            out.append(media_to_attachment(item))
    return out


def to_sdk_messages(messages):
    """Convert client-side role/content dicts into SDK message objects."""
    out = []
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
