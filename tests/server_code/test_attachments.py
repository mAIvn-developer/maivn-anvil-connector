from __future__ import annotations

import base64

from anvil.media import Media
from maivn_anvil_connector.attachments import media_list_to_attachments, media_to_attachment


def test_pdf_media_becomes_base64_attachment() -> None:
    raw = b"%PDF-1.4 fake"
    media = Media(raw, "application/pdf", "doc.pdf")
    att = media_to_attachment(media)
    assert att["name"] == "doc.pdf"
    assert att["mime_type"] == "application/pdf"
    assert base64.b64decode(att["content_base64"]) == raw


def test_image_media_carries_mime_type() -> None:
    media = Media(b"\x89PNG fake", "image/png", "pic.png")
    att = media_to_attachment(media)
    assert att["mime_type"] == "image/png"


def test_media_list_maps_all() -> None:
    items = [Media(b"a", "text/plain", "a.txt"), Media(b"b", "text/plain", "b.txt")]
    out = media_list_to_attachments(items)
    assert [a["name"] for a in out] == ["a.txt", "b.txt"]
