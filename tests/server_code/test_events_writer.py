from __future__ import annotations

from typing import Any

from maivn_anvil_connector.events_writer import EventsWriter


class _Sink:
    def __init__(self) -> None:
        self.rows: list[tuple[int, str, dict[str, Any]]] = []

    def __call__(self, *, seq: int, kind: str, payload: dict[str, Any]) -> None:
        self.rows.append((seq, kind, payload))


def _chunk(text: str) -> tuple[str, dict[str, Any]]:
    return ("assistant_chunk", {"data": {"text": text}})


def test_non_chunk_events_pass_through_with_seq() -> None:
    sink = _Sink()
    w = EventsWriter("s1", append=sink)
    w.write("status_message", {"data": {"text": "working"}})
    w.write("final", {"data": {"response": "done"}})
    w.flush()
    assert [(s, k) for s, k, _ in sink.rows] == [(1, "status_message"), (2, "final")]


def test_consecutive_chunks_coalesce_into_one_row() -> None:
    sink = _Sink()
    w = EventsWriter("s1", append=sink)
    for part in ("He", "llo", " world"):
        kind, payload = _chunk(part)
        w.write(kind, payload)
    w.flush()
    assert len(sink.rows) == 1
    _seq, kind, payload = sink.rows[0]
    assert kind == "assistant_chunk"
    assert payload["data"]["text"] == "Hello world"


def test_chunk_run_is_flushed_before_a_following_event() -> None:
    sink = _Sink()
    w = EventsWriter("s1", append=sink)
    for part in ("a", "b"):
        kind, payload = _chunk(part)
        w.write(kind, payload)
    w.write("final", {"data": {"response": "done"}})
    w.flush()
    assert [
        (k, p.get("data", {}).get("text") or p.get("data", {}).get("response"))
        for _, k, p in sink.rows
    ] == [("assistant_chunk", "ab"), ("final", "done")]
