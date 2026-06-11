"""Data Table helpers. Anvil-runtime-safe (no annotations)."""

from datetime import datetime, timezone

from anvil.tables import app_tables


def append_event(session_id, *, seq, kind, payload):
    app_tables.maivn_events.add_row(
        session_id=session_id,
        seq=seq,
        kind=kind,
        payload=payload,
        created=datetime.now(timezone.utc),
    )


def read_events(session_id, *, after_seq, limit=500):
    rows = [
        {"seq": r["seq"], "kind": r["kind"], "payload": r["payload"]}
        for r in app_tables.maivn_events.search(session_id=session_id)
        if r["seq"] > after_seq
    ]
    rows.sort(key=lambda r: r["seq"])
    return rows[:limit]


def delete_session(session_id):
    for r in list(app_tables.maivn_events.search(session_id=session_id)):
        r.delete()
    for r in list(app_tables.maivn_io.search(session_id=session_id)):
        r.delete()
    for r in list(app_tables.maivn_sessions.search(session_id=session_id)):
        r.delete()


# MARK: Session ownership


def bind_session_owner(session_id, owner_id):
    for r in list(app_tables.maivn_sessions.search(session_id=session_id)):
        r.delete()
    app_tables.maivn_sessions.add_row(
        session_id=session_id,
        owner_id=owner_id,
        created=datetime.now(timezone.utc),
    )


def read_session_owner(session_id):
    for r in app_tables.maivn_sessions.search(session_id=session_id):
        return r["owner_id"]
    return None


def reset_session_owners():
    for r in list(app_tables.maivn_sessions.search()):
        r.delete()


# MARK: Interrupt I/O helpers


def put_interrupt(
    session_id,
    *,
    interrupt_id,
    prompt,
    input_type,
    choices,
    is_private=False,
):
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


def _io_row(session_id, interrupt_id):
    for r in app_tables.maivn_io.search(session_id=session_id):
        if r["interrupt_id"] == interrupt_id:
            return r
    return None


def interrupt_exists(session_id, interrupt_id):
    return _io_row(session_id, interrupt_id) is not None


def write_interrupt_response(session_id, interrupt_id, response):
    row = _io_row(session_id, interrupt_id)
    if row is not None:
        row["response"] = response
        row["status"] = "answered"


def read_interrupt_response(session_id, interrupt_id):
    row = _io_row(session_id, interrupt_id)
    if row is None:
        return None
    return row["response"]


def is_interrupt_private(session_id, interrupt_id):
    row = _io_row(session_id, interrupt_id)
    return bool(row["is_private"]) if row is not None else False


def clear_interrupt(session_id, interrupt_id):
    row = _io_row(session_id, interrupt_id)
    if row is not None:
        row.delete()
