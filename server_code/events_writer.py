from typing import Any, Callable

AppendRow = Callable[..., None]
_CHUNK_KIND = "assistant_chunk"


class EventsWriter:
    """Persist drained UIEvents as ordered rows, coalescing assistant chunks."""

    def __init__(self, session_id: str, *, append: AppendRow) -> None:
        self._session_id = session_id
        self._append = append
        self._seq = 0
        self._pending_text: list[str] = []

    @property
    def seq(self) -> int:
        return self._seq

    def write(self, kind: str, payload: dict[str, Any]) -> None:
        if kind == _CHUNK_KIND:
            self._pending_text.append(self._chunk_text(payload))
            return
        self._flush_chunks()
        self._emit(kind, payload)

    def flush(self) -> None:
        self._flush_chunks()

    def _flush_chunks(self) -> None:
        if not self._pending_text:
            return
        text = "".join(self._pending_text)
        self._pending_text = []
        self._emit(_CHUNK_KIND, {"data": {"text": text}})

    def _emit(self, kind: str, payload: dict[str, Any]) -> None:
        self._seq += 1
        self._append(seq=self._seq, kind=kind, payload=payload)

    @staticmethod
    def _chunk_text(payload: dict[str, Any]) -> str:
        data = payload.get("data")
        if isinstance(data, dict):
            text = data.get("text")
            if isinstance(text, str):
                return text
        return ""
