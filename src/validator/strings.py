import re
from typing import Any, Callable, TypeGuard

from validator._helpers import _require_callables, _require_int, _require_type


_NUMERIC = re.compile(r"[+-]?[0-9]+(\.[0-9]+)?")

_LOCAL_CHAR = r"[A-Za-z0-9_%+-]+"
_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"

_EMAIL = re.compile(
    rf"{_LOCAL_CHAR}(?:\.{_LOCAL_CHAR})*"
    rf"@"
    rf"{_LABEL}(?:\.{_LABEL})+"
)


def min_length(value: str, minimum: int) -> bool:
    _require_type(value, str)
    _require_int(minimum, "minimum")
    
    if minimum < 0:
        raise ValueError("minimum must be >= 0")
    
    return len(value) >= minimum


def max_length(value: str, maximum: int) -> bool:
    _require_type(value, str)
    _require_int(maximum, "maximum")
        
    if maximum < 0:
        raise ValueError("maximum must be >= 0")

    return len(value) <= maximum


def not_empty(value: str) -> bool:
    """Return True if value has at least one non-whitespace character."""
    _require_type(value, str)

    return bool(value.strip())


def is_alpha(value: str) -> bool:
    _require_type(value, str)

    return value.isalpha()


def is_numeric(value: str) -> bool:
    _require_type(value, str)
    return _NUMERIC.fullmatch(value) is not None


def _compile(pattern) -> re.Pattern:
    if isinstance(pattern, re.Pattern):
        return pattern 
    if isinstance(pattern, str):
        try:
            return re.compile(pattern)
        except re.error as e:
            raise ValueError(f"invalid regex pattern: {e}") from e 
    raise TypeError(
        f"pattern must be of type str or re.Pattern, got {type(pattern).__name__}"
    )


def matches(value: str, pattern) -> bool:
    _require_type(value, str)
    return _compile(pattern).fullmatch(value) is not None


def is_email(email: str) -> bool:
    _require_type(email, str, "Email")

    return _EMAIL.fullmatch(email) is not None


def is_str(value: Any) -> TypeGuard[str]:
    return isinstance(value, str)


# ---------------------------------------------------------------

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