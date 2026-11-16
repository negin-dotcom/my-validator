from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from validator._helpers import _require_callables, _require_type
from validator.combinators import Validator


@dataclass(frozen=True)
class Schema:
    fields: Mapping[str, Validator]

    def __post_init__(self) -> None:
        if not isinstance(self.fields, Mapping):
            raise TypeError(f"fields must be of type Mapping, " 
                            f"got {type(self.fields).__name__}")
        
        for key in self.fields:
            _require_type(key, str)
        _require_callables(tuple(self.fields.values()))


def validate(data: dict[str, Any], schema: Schema) -> dict[str, str]:
    errors: dict[str, str] = {}

    for field, validator in schema.fields.items():
        if field not in data:
            errors[field] = "is required"
        elif not validator(data[field]):
            errors[field] = getattr(validator, "message", "failed validation")

    return errors