from typing import Any, Protocol, cast

from validator._helpers import (
    Validator,
    _describe,
    _require_callable,
    _require_callables,
)
from validator.strings import max_length, min_length


class Rule(Protocol):
    code: str
    message: str

    def __call__(self, value: Any, /) -> bool: ...


class ParamRule(Protocol):
    code: str
    message: str

    def __call__(self, value: Any, /, *args: Any) -> bool: ...


def check_length(length_func: ParamRule, n: int) -> Validator:
    if length_func not in (min_length, max_length):
        raise ValueError(f"expected min_length or max_length, got {repr(length_func)}")

    
    def check(value: Any) -> bool:
        return length_func(value, n)

    rule = cast(Rule, check)
    rule.code = length_func.code
    rule.message = length_func.message.format(n=n)

    return rule


def all_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if not v(value):
                return False
        return True

    rule = cast(Rule, check)
    rule.code = "all_of"
    rule.message = "must satisfy all of: " + "; ".join(_describe(v) for v in validators)

    return rule


def any_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if v(value):
                return True
        return False

    rule = cast(Rule, check)
    rule.code = "any_of"
    rule.message = "must satisfy at least one of: " + "; ".join(
        _describe(v) for v in validators
    )
    
    return rule


def not_(validator: Validator) -> Validator:
    _require_callable(validator)

    def check(value: Any) -> bool:
        return not validator(value)

    rule = cast(Rule, check)
    rule.code = "not_"
    rule.message = "must not satisfy: " + _describe(validator)

    return rule


def none_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if v(value):
                return False
        return True

    rule = cast(Rule, check)
    rule.code = "none_of"
    rule.message = "must satisfy none of: " + "; ".join(
        _describe(v) for v in validators
    )

    return rule
