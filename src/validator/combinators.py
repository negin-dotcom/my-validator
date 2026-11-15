from typing import Any, Callable

from validator._helpers import _require_callable, _require_callables
from validator.strings import max_length, min_length


Validator = Callable[[Any], bool]


def check_length(length_func: callable, n: int) -> Validator:
    if length_func not in (min_length, max_length):
        raise ValueError(f"expected min_length or max_length, got {repr(length_func)}")
    
    def check(value: Any) -> bool:
        return length_func(value, n)

    return check

def all_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if not v(value):
                return False 
        return True

    return check

def any_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if v(value):
                return True 
        return False

    return check

def not_(validator: Validator) -> Validator:
    _require_callable(validator)

    def check(value: Any) -> bool:
        return not validator(value)

    return check

def none_of(*validators: Validator) -> Validator:
    _require_callables(validators)

    def check(value: Any) -> bool:
        for v in validators:
            if v(value):
                return False 
        return True 

    return check