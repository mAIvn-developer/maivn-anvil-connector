from __future__ import annotations

import itertools
from collections.abc import Iterator
from typing import Any


class _Row:
    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def delete(self) -> None:
        _Table._deleted.append(self)  # noqa: SLF001


class _Table:
    _deleted: list[_Row] = []

    def __init__(self) -> None:
        self._rows: list[_Row] = []
        self._ids = itertools.count(1)

    def add_row(self, **data: Any) -> _Row:
        data.setdefault("_id", next(self._ids))
        row = _Row(data)
        self._rows.append(row)
        return row

    def search(self, *args: Any, **filters: Any) -> Iterator[_Row]:
        for row in self._rows:
            if row in _Table._deleted:  # noqa: SLF001
                continue
            if all(row._data.get(k) == v for k, v in filters.items()):  # noqa: SLF001
                yield row


class _AppTables:
    def __init__(self) -> None:
        self._tables: dict[str, _Table] = {}

    def __getattr__(self, name: str) -> _Table:
        if name.startswith("_"):
            raise AttributeError(name)
        return self._tables.setdefault(name, _Table())


app_tables = _AppTables()


def order_by(name: str, ascending: bool = True) -> dict[str, Any]:
    return {"__order_by__": name, "ascending": ascending}


def reset() -> None:
    app_tables._tables.clear()  # noqa: SLF001
    _Table._deleted.clear()  # noqa: SLF001
