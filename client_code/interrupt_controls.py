# pyright: basic
"""Pure logic for choosing an interrupt input control. Skulpt-safe."""

_BOOLEAN = frozenset({"boolean", "bool", "yes_no", "confirm"})
_CHOICE = frozenset({"choice", "select", "enum"})


def control_kind(input_type, choices):
    """Return one of 'text' | 'boolean' | 'choice' for the given interrupt spec."""
    normalized = str(input_type or "").strip().lower()
    if normalized in _CHOICE or (choices and normalized not in _BOOLEAN):
        return "choice"
    if normalized in _BOOLEAN:
        return "boolean"
    return "text"
