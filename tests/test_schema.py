from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parents[1]


def _load_anvil_yaml() -> dict[str, Any]:
    return yaml.safe_load((_ROOT / "anvil.yaml").read_text(encoding="utf-8"))


def _schema() -> dict[str, Any]:
    return _load_anvil_yaml()["db_schema"]


def _column_names(table: dict[str, Any]) -> set[str]:
    cols = table["columns"]
    if isinstance(cols, list):
        return {c["name"] for c in cols}
    return {c["name"] for c in cols.values()}


def test_events_table_columns() -> None:
    cols = _column_names(_schema()["maivn_events"])
    assert {"session_id", "seq", "kind", "payload", "created"} <= cols


def test_io_table_columns() -> None:
    cols = _column_names(_schema()["maivn_io"])
    assert {"session_id", "interrupt_id", "prompt", "response", "status", "is_private"} <= cols


def test_tables_are_server_only() -> None:
    schema = _schema()
    for name in ("maivn_events", "maivn_io"):
        assert schema[name]["client"] == "none"
        assert schema[name]["server"] == "full"


def test_tables_service_is_enabled() -> None:
    services = _load_anvil_yaml()["services"]
    sources = {entry["source"] for entry in services}
    assert "/runtime/services/tables.yml" in sources


def test_secrets_service_is_enabled() -> None:
    services = _load_anvil_yaml()["services"]
    sources = {entry["source"] for entry in services}
    assert "/runtime/services/anvil/secrets.yml" in sources
