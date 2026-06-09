from __future__ import annotations

_store: dict[str, str] = {}


def get_secret(name: str) -> str:
    return _store[name]


def _set(name: str, value: str) -> None:
    _store[name] = value


def reset() -> None:
    _store.clear()
