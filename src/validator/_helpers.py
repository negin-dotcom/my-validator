from typing import Any, Callable, Union


Validator = Callable[[Any], bool]


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
        _require_callable(v)


def _require_callable(validator: callable) -> None:
    if not callable(validator):
        raise TypeError(f"validator must be callable, got {type(validator).__name__}")


def _require_bounds(low: float, high: float) -> None:
    _require_number(low, "low")
    _require_number(high, "high")
    
    if low > high:
        raise ValueError("low must be <= high")


def _describe(v: Validator) -> str:
    return getattr(v, "message", getattr(v, "__name__", "a custom rule"))