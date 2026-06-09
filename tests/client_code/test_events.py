from __future__ import annotations

from maivn_anvil_connector.events import is_terminal, parse_row


def test_parse_assistant_chunk() -> None:
    ev = parse_row({"seq": 3, "kind": "assistant_chunk", "payload": {"data": {"text": "hi"}}})
    assert ev.seq == 3
    assert ev.kind == "assistant_chunk"
    assert ev.text == "hi"


def test_parse_final_carries_result() -> None:
    ev = parse_row(
        {"seq": 9, "kind": "final", "payload": {"data": {"response": "done", "result": {"x": 1}}}}
    )
    assert ev.kind == "final"
    assert ev.text == "done"
    assert ev.result == {"x": 1}


def test_is_terminal() -> None:
    assert is_terminal("final")
    assert is_terminal("error")
    assert not is_terminal("assistant_chunk")
