from datetime import datetime, timezone
from typing import Any

from anvil.tables import app_tables


def append_event(session_id: str, *, seq: int, kind: str, payload: dict[str, Any]) -> None:
    app_tables.maivn_events.add_row(
        session_id=session_id,
        seq=seq,
        kind=kind,
        payload=payload,
        created=datetime.now(timezone.utc),
    )


def read_events(session_id: str, *, after_seq: int, limit: int = 500) -> list[dict[str, Any]]:
    rows = [
        {"seq": r["seq"], "kind": r["kind"], "payload": r["payload"]}
        for r in app_tables.maivn_events.search(session_id=session_id)
        if r["seq"] > after_seq
    ]
    rows.sort(key=lambda r: r["seq"])
    return rows[:limit]


def delete_session(session_id: str) -> None:
    for r in list(app_tables.maivn_events.search(session_id=session_id)):
        r.delete()
    for r in list(app_tables.maivn_io.search(session_id=session_id)):
        r.delete()


# MARK: Interrupt I/O helpers


def put_interrupt(
    session_id: str,
    *,
    interrupt_id: str,
    prompt: str,
    input_type: str,
    choices: list[str] | None,
    is_private: bool = False,
) -> None:
    app_tables.maivn_io.add_row(
        session_id=session_id,
        interrupt_id=interrupt_id,
        prompt=prompt,
        input_type=input_type,
        choices=choices,
        response=None,
        status="pending",
        is_private=is_private,
    )


def _io_row(session_id: str, interrupt_id: str) -> Any:
    for r in app_tables.maivn_io.search(session_id=session_id):
        if r["interrupt_id"] == interrupt_id:
            return r
    return None


def interrupt_exists(session_id: str, interrupt_id: str) -> bool:
    return _io_row(session_id, interrupt_id) is not None


def write_interrupt_response(session_id: str, interrupt_id: str, response: str) -> None:
    row = _io_row(session_id, interrupt_id)
    if row is not None:
        row["response"] = response
        row["status"] = "answered"


def read_interrupt_response(session_id: str, interrupt_id: str) -> str | None:
    row = _io_row(session_id, interrupt_id)
    if row is None:
        return None
    return row["response"]


def is_interrupt_private(session_id: str, interrupt_id: str) -> bool:
    row = _io_row(session_id, interrupt_id)
    return bool(row["is_private"]) if row is not None else False


def clear_interrupt(session_id: str, interrupt_id: str) -> None:
    row = _io_row(session_id, interrupt_id)
    if row is not None:
        row.delete()
