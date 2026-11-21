import re
from typing import Any, TypeGuard

from validator._helpers import _require_int, _require_type
from validator.decorators import rule, rule_factory

_NUMERIC = re.compile(r"[+-]?[0-9]+(\.[0-9]+)?")

_LOCAL_CHAR = r"[A-Za-z0-9_%+-]+"
_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"

_EMAIL = re.compile(
    rf"{_LOCAL_CHAR}(?:\.{_LOCAL_CHAR})*"
    rf"@"
    rf"{_LABEL}(?:\.{_LABEL})+"
)


@rule("min_length", "must be equal to or greater than {n}")
def min_length(value: str, minimum: int) -> bool:
    _require_type(value, str)
    _require_int(minimum, "minimum")
    
    if minimum < 0:
        raise ValueError("minimum must be >= 0")
    
    return len(value) >= minimum


@rule("max_length", "must be equal to or less than {n}")
def max_length(value: str, maximum: int) -> bool:
    _require_type(value, str)
    _require_int(maximum, "maximum")
        
    if maximum < 0:
        raise ValueError("maximum must be >= 0")

    return len(value) <= maximum


@rule("not_empty", "must not be empty")
def not_empty(value: str) -> bool:
    """Return True if value has at least one non-whitespace character."""
    _require_type(value, str)

    return bool(value.strip())


@rule("alpha", "must be alphabetic")
def is_alpha(value: str) -> bool:
    _require_type(value, str)

    return value.isalpha()


@rule("numeric", "must be numeric")
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


@rule("match", "must exactly match the required pattern")
def matches(value: str, pattern) -> bool:
    _require_type(value, str)
    return _compile(pattern).fullmatch(value) is not None


@rule_factory("match", "must match exactly the pattern {pattern}")
def matches_of(pattern):
    def check(value: str) -> bool:
        return matches(value, pattern)

    return check


@rule("email", "must be an Email")
def is_email(email: str) -> bool:
    _require_type(email, str, "Email")

    return _EMAIL.fullmatch(email) is not None


@rule("string", "must be a string")
def is_str(value: Any) -> TypeGuard[str]:
    return isinstance(value, str)