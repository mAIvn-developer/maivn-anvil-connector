from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

_registry: dict[str, Callable[..., Any]] = {}
_background: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []


def callable(name_or_fn=None):  # noqa: A001
    """Mirror Anvil's @anvil.server.callable and @anvil.server.callable('name')."""

    def register(fn: Callable[..., Any], name: str) -> Callable[..., Any]:
        _registry[name] = fn
        return fn

    if inspect.isfunction(name_or_fn) or inspect.ismethod(name_or_fn):
        return register(name_or_fn, name_or_fn.__name__)

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        rpc_name = name_or_fn if isinstance(name_or_fn, str) else fn.__name__
        return register(fn, rpc_name)

    return decorator


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


session: dict[str, Any] = {}


class AnvilWrappedError(Exception):
    pass


class _NoLoadingIndicator:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


no_loading_indicator = _NoLoadingIndicator()


def reset() -> None:
    _registry.clear()
    _background.clear()
    session.clear()
