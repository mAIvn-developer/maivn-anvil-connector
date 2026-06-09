from __future__ import annotations

import pytest
from maivn_anvil_connector import limits


def test_non_example_session_is_unlimited() -> None:
    limits.reset()
    for _ in range(100):
        limits.enforce_start(example=None, messages=[{"role": "user", "content": "x"}])


def test_example_session_capped_per_owner() -> None:
    limits.reset()
    limits.set_owner_provider(lambda: "owner-A")
    for _ in range(limits.EXAMPLE_DAILY_CAP):
        limits.enforce_start(example="basic_chat", messages=[])
    with pytest.raises(limits.UsageLimitError):
        limits.enforce_start(example="basic_chat", messages=[])


def test_example_message_length_capped() -> None:
    limits.reset()
    limits.set_owner_provider(lambda: "owner-A")
    with pytest.raises(limits.UsageLimitError):
        limits.enforce_start(
            example="basic_chat", messages=[{"role": "user", "content": "x" * 10_000}]
        )
