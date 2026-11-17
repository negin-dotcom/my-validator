import functools
from typing import Any, cast

from validator._helpers import Validator
from validator.combinators import Rule


def custom_validator(
    func: Validator,
    *,
    code: str | None = None,
    message: str | None = None,
) -> Validator:
    """Turn a user's function into a validator the library understands.
    
    Example:

    from validator import Schema, validate

    def _is_even(x):
        return x % 2 == 0

    is_even = custom_validator(_is_even, code="even", message="must be even")

    fields = {"age": is_even}
    schema = Schema(fields)

    data = {"age": 31}
    print(validate(data, schema))

    >>> {"age": "must be even"}
    """

    if not callable(func):
        raise TypeError("func must be callable")

    name = getattr(func, "__name__", "custom")
    if code is None:
        code = name 

    if message is None:
        message = f"failed validation: {name}"

    if not isinstance(code, str) or not isinstance(message, str):
        raise TypeError("code and message must be strings")

    @functools.wraps(func)
    def validator(value: Any) -> bool:
        result = func(value)

        if not isinstance(result, bool):
            raise TypeError(
                f"{name} must return a bool, got {repr(type(result))}"
            )

        return result 

    rule_validator = cast(Rule, validator)
    rule_validator.code = code
    rule_validator.message = message

    return rule_validator