from typing import Any

from validator.combinators import Validator


def validate(data: dict[str, Any], schema: dict[str, Validator]) -> list[str]:
    failed = []

    for field, validator in schema.items():
        if field not in data:
            failed.append(field)
        elif not validator(data[field]):
            failed.append(field)

    return failed