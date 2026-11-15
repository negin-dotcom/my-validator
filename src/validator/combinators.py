from typing import Any

from validator._helpers import (
    Validator,
    _describe, 
    _require_callable, 
    _require_callables
)

from validator.strings import max_length, min_length



def check_length(length_func: callable, n: int) -> Validator:
    if length_func not in (min_length, max_length):
        raise ValueError(f"expected min_length or max_length, got {repr(length_func)}")
    
    def check(value: Any) -> bool:
        return length_func(value, n)

    check.code = length_func.code 
    check.message = length_func.message.format(n=n)

    return check

def all_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if not v(value):
                return False 
        return True

    check.code = "all_of"
    check.message = "must satisfy all of: " + "; ".join(_describe(v) for v in validators)

    return check

def any_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if v(value):
                return True 
        return False

    check.code = "any_of"
    check.message = "must satisfy at least one of: " + "; ".join(_describe(v) for v in validators)
    
    return check

def not_(validator: Validator) -> Validator:
    _require_callable(validator)

    def check(value: Any) -> bool:
        return not validator(value)

    check.code = "not_"
    check.message = "must not satisfy: " + _describe(validator)

    return check

def none_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if v(value):
                return False 
        return True 

    check.code = "none_of"
    check.message = "must satisfy none of: " + "; ".join(_describe(v) for v in validators)

    return check