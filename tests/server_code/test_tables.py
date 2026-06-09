from __future__ import annotations

from maivn_anvil_connector import tables


def test_append_event_assigns_increasing_seq() -> None:
    tables.append_event("s1", seq=1, kind="status_message", payload={"text": "hi"})
    tables.append_event("s1", seq=2, kind="final", payload={"response": "done"})
    rows = tables.read_events("s1", after_seq=0)
    assert [r["seq"] for r in rows] == [1, 2]


def test_read_events_respects_cursor() -> None:
    tables.append_event("s1", seq=1, kind="a", payload={})
    tables.append_event("s1", seq=2, kind="b", payload={})
    rows = tables.read_events("s1", after_seq=1)
    assert [r["kind"] for r in rows] == ["b"]


def test_events_scoped_by_session() -> None:
    tables.append_event("s1", seq=1, kind="a", payload={})
    tables.append_event("s2", seq=1, kind="b", payload={})
    assert [r["kind"] for r in tables.read_events("s2", after_seq=0)] == ["b"]
