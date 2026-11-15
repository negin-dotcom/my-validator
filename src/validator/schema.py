from typing import Any

from validator.combinators import Validator


def validate(data: dict[str, Any], schema: dict[str, Validator]) -> dict[str, str]:
    errors = {}

    for field, validator in schema.items():
        if field not in data:
            errors[field] = "is required"
        elif not validator(data[field]):
            errors[field] = getattr(validator, "message", "failed validation")

    return errors