import base64
from typing import Any

from anvil.media import Media


def media_to_attachment(media: Media) -> dict[str, Any]:
    """Convert an Anvil Media object into a maivn SDK attachment payload.

    The result plugs directly into ``HumanMessage(attachments=[...])``. PDFs and
    images are carried as base64 so the platform receives them natively.
    """
    return {
        "name": media.name,
        "mime_type": media.get_content_type(),
        "content_base64": base64.b64encode(media.get_bytes()).decode("ascii"),
    }


def media_list_to_attachments(items: list[Media]) -> list[dict[str, Any]]:
    return [media_to_attachment(m) for m in items]
