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


def test_session_owner_round_trip() -> None:
    tables.bind_session_owner("s1", "owner-A")
    assert tables.read_session_owner("s1") == "owner-A"
    tables.bind_session_owner("s1", "owner-B")
    assert tables.read_session_owner("s1") == "owner-B"


def test_session_owner_row_is_not_drained_to_client() -> None:
    tables.bind_session_owner("s1", "owner-A")
    tables.append_event("s1", seq=1, kind="final", payload={"data": {"response": "done"}})
    rows = tables.read_events("s1", after_seq=0)
    assert [r["kind"] for r in rows] == ["final"]
