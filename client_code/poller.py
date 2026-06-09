# pyright: basic
"""Adaptive poll-cadence controller. Skulpt-safe (no annotations/typing)."""


class CadenceController:
    """Decides the next poll interval based on recent activity."""

    def __init__(self, active=0.2, idle=1.0, idle_after=5):
        self._active = active
        self._idle = idle
        self._idle_after = idle_after
        self._empty_streak = 0

    @property
    def active(self):
        return self._active

    def next_interval(self, got_events):
        if got_events:
            self._empty_streak = 0
            return self._active
        self._empty_streak += 1
        return self._idle if self._empty_streak >= self._idle_after else self._active
