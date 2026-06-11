"""Media attachment helpers. Anvil-runtime-safe (no annotations)."""

import base64


def media_to_attachment(media):
    """Convert an Anvil Media object into a maivn SDK attachment payload.

    The result plugs directly into ``HumanMessage(attachments=[...])``. PDFs and
    images are carried as base64 so the platform receives them natively.
    """
    return {
        "name": media.name,
        "mime_type": media.get_content_type(),
        "content_base64": base64.b64encode(media.get_bytes()).decode("ascii"),
    }


def media_list_to_attachments(items):
    return [media_to_attachment(m) for m in items]
