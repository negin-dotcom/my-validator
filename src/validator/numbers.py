from typing import Any, TypeGuard

from validator._helpers import _require_bounds, _require_number
from validator.combinators import Validator
from validator.decorators import rule, rule_factory


@rule("in_range", "{value} must be between {low} and {high}")
def in_range(value: float, low: float, high: float) -> bool:
    _require_number(value)
    _require_bounds(low, high)

    return low <= value <= high


@rule_factory("in_range_of", "must be between {low} and {high}")
def in_range_of(low: float, high: float) -> Validator:
    _require_bounds(low, high)

    def check(value: Any) -> bool:
        return in_range(value, low, high)

    return check


@rule("positive", "must be positive")
def is_positive(value: float) -> bool:
    _require_number(value)
    return value > 0


@rule("negative", "must be negative")
def is_negative(value: float) -> bool:
    _require_number(value)
    return value < 0


@rule("non_positive", "must be equal to or less than zero")
def is_non_positive(value: float) -> bool:
    _require_number(value)
    return value <= 0


@rule("non_negative", "must be equal to or greater than zero")
def is_non_negative(value: float) -> bool:
    _require_number(value)
    return value >= 0


@rule("integer", "must be an integer")
def is_int(value: Any) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool)


@rule("float", "must be a float")
def is_float(value: Any) -> TypeGuard[float]:
    return isinstance(value, float)


@rule("number", "must be a number")
def is_number(value: Any) -> TypeGuard[int | float]:
    return isinstance(value, (int, float)) and not isinstance(value, bool) 


@rule("boolean", "must be a boolean")
def is_bool(value: Any) -> TypeGuard[bool]:
    return isinstance(value, bool)