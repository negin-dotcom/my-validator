from typing import Any, TypeGuard

from validator._helpers import _require_number


def in_range(value: float, low: float, high: float) -> bool:
    _require_number(value)
    _require_number(low, "low")
    _require_number(high, "high")

    if low > high:
        raise ValueError("low must be <= high")

    return low <= value <= high


def is_positive(value: float) -> bool:
    _require_number(value)
    return value > 0


def is_negative(value: float) -> bool:
    _require_number(value)
    return value < 0


def is_non_positive(value: float) -> bool:
    _require_number(value)
    return value <= 0


def is_non_negative(value: float) -> bool:
    _require_number(value)
    return value >= 0


def is_int(value: Any) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool)


def is_float(value: Any) -> TypeGuard[float]:
    return isinstance(value, float)


def is_number(value: Any) -> TypeGuard[int | float]:
    return isinstance(value, (int, float)) and not isinstance(value, bool) 


def is_str(value: Any) -> TypeGuard[str]:
    return isinstance(value, str)


def is_bool(value: Any) -> TypeGuard[bool]:
    return isinstance(value, bool)
