"""Coalescing event writer. Anvil-runtime-safe (no annotations)."""

_CHUNK_KIND = "assistant_chunk"


class EventsWriter:
    """Persist drained UIEvents as ordered rows, coalescing assistant chunks."""

    def __init__(self, session_id, *, append):
        self._session_id = session_id
        self._append = append
        self._seq = 0
        self._pending_text = []

    @property
    def seq(self):
        return self._seq

    def write(self, kind, payload):
        if kind == _CHUNK_KIND:
            self._pending_text.append(self._chunk_text(payload))
            return
        self._flush_chunks()
        self._emit(kind, payload)

    def flush(self):
        self._flush_chunks()

    def _flush_chunks(self):
        if not self._pending_text:
            return
        text = "".join(self._pending_text)
        self._pending_text = []
        self._emit(_CHUNK_KIND, {"data": {"text": text}})

    def _emit(self, kind, payload):
        self._seq += 1
        self._append(seq=self._seq, kind=kind, payload=payload)

    @staticmethod
    def _chunk_text(payload):
        data = payload.get("data")
        if isinstance(data, dict):
            text = data.get("text")
            if isinstance(text, str):
                return text
        return ""
