from __future__ import annotations

from collections.abc import Callable
from typing import Any

_registry: dict[str, Callable[..., Any]] = {}
_background: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []


def callable(fn: Callable[..., Any]) -> Callable[..., Any]:  # noqa: A001
    _registry[fn.__name__] = fn
    return fn


def background_task(fn: Callable[..., Any]) -> Callable[..., Any]:
    _registry[fn.__name__] = fn
    return fn


class _Task:
    def __init__(self, task_id: str) -> None:
        self.id = task_id


def launch_background_task(name: str, *args: Any, **kwargs: Any) -> _Task:
    _background.append((name, args, kwargs))
    return _Task(task_id=f"task-{len(_background)}")


def call(fn_name: str, *args: Any, **kwargs: Any) -> Any:
    """Client -> server RPC. Never invoked in tests (callers inject a fake)."""
    return _registry[fn_name](*args, **kwargs)


# Anvil's per-session store; a dict-like. Tests always set an owner provider, so
# this branch is not exercised, but it must exist for the double to be complete.
session: dict[str, Any] = {}


class AnvilWrappedError(Exception):
    pass


def reset() -> None:
    _registry.clear()
    _background.clear()
    session.clear()
