from __future__ import annotations

from maivn_anvil_connector.interrupt_controls import control_kind


def test_text_is_default() -> None:
    assert control_kind("text", None) == "text"
    assert control_kind(None, None) == "text"


def test_boolean_variants() -> None:
    assert control_kind("boolean", None) == "boolean"
    assert control_kind("yes_no", None) == "boolean"


def test_choice_from_input_type() -> None:
    assert control_kind("choice", None) == "choice"
    assert control_kind("select", ["a", "b"]) == "choice"


def test_choices_present_implies_choice() -> None:
    assert control_kind("text", ["a", "b"]) == "choice"


def test_boolean_wins_over_choices() -> None:
    assert control_kind("boolean", ["a", "b"]) == "boolean"
