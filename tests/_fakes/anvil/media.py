from __future__ import annotations


class Media:
    def __init__(self, content: bytes, content_type: str, name: str) -> None:
        self._content = content
        self.content_type = content_type
        self.name = name

    def get_bytes(self) -> bytes:
        return self._content

    def get_content_type(self) -> str:
        return self.content_type
