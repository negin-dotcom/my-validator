from typing import Union


def _require_int(value, name: str = "value") -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be of type int, got {type(value).__name__}")


def _require_number(value, name: str = "value") -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")


def _require_type(value, expected: Union[type, tuple[type, ...]], name: str = "value") -> None:
    if not isinstance(value, expected):
        if isinstance(expected, tuple):
            names = " or ".join(t.__name__ for t in expected)
        else:
            names = expected.__name__
        raise TypeError(f"{name} must be of type {names}, got {type(value).__name__}")


def _require_callables(validators: tuple) -> None:
    for v in validators:
        if not callable(v):
            raise TypeError(f"validator must be callable, got {type(v).__name__}")