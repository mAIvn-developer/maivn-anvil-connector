from __future__ import annotations

from maivn_anvil_connector.poller import CadenceController


def test_active_cadence_when_events_arrive() -> None:
    c = CadenceController(active=0.2, idle=1.0, idle_after=3)
    assert c.next_interval(got_events=True) == 0.2


def test_backs_off_to_idle_after_empty_polls() -> None:
    c = CadenceController(active=0.2, idle=1.0, idle_after=3)
    for _ in range(3):
        c.next_interval(got_events=False)
    assert c.next_interval(got_events=False) == 1.0


def test_resets_to_active_on_new_events() -> None:
    c = CadenceController(active=0.2, idle=1.0, idle_after=2)
    c.next_interval(got_events=False)
    c.next_interval(got_events=False)
    assert c.next_interval(got_events=False) == 1.0
    assert c.next_interval(got_events=True) == 0.2
