# pyright: basic
"""Client-side event objects parsed from drained event rows.

Skulpt-safe: no type annotations, no typing/dataclasses imports. The Anvil
client runtime evaluates annotations and does not ship `typing`/`dataclasses`,
so this module is written in plain Python. Static typing is preserved for the
checker via inference and the typed test double, not via runtime annotations.
"""

_TERMINAL = frozenset({"final", "error"})


class MaivnEvent:
    """A single event parsed from a drained row."""

    def __init__(self, seq, kind, text, result, payload):
        self.seq = seq
        self.kind = kind
        self.text = text
        self.result = result
        self.payload = payload


def parse_row(row):
    payload = dict(row.get("payload") or {})
    raw_data = payload.get("data")
    data = raw_data if isinstance(raw_data, dict) else {}
    text = str(data.get("text") or data.get("response") or data.get("message") or "")
    return MaivnEvent(
        seq=int(row["seq"]),
        kind=str(row["kind"]),
        text=text,
        result=data.get("result"),
        payload=payload,
    )


def is_terminal(kind):
    return kind in _TERMINAL
