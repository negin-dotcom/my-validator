from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal, get_args

from validator._helpers import _require_callables, _require_type
from validator.combinators import Validator

ExtraFields = Literal["ignore", "forbid"]


@dataclass(frozen=True)
class Schema:
    """Maps field names to the validator, each field must pass.
    
    Example:
        Schema({"age": in_range_of(18, 35), "name": check_length(min_length, 2)})
    """
    fields: Mapping[str, Validator]
    extra_fields: ExtraFields = "ignore"

    def __post_init__(self) -> None:
        if not isinstance(self.fields, Mapping):
            raise TypeError(f"fields must be of type Mapping, " 
                            f"got {type(self.fields).__name__}")
        
        for key in self.fields:
            _require_type(key, str)
        _require_callables(tuple(self.fields.values()))

        if self.extra_fields not in get_args(ExtraFields):
            raise ValueError("extra_fields expected ignore or forbid, "
                             f"got {repr(self.extra_fields)}")


def validate(data: dict[str, Any], schema: Schema) -> dict[str, str]:
    """Check data against schema and return field -> error message.
    
    An empty dict means everything is ok.
    Missing fields are reported as "is required".
    Extra fields are ignored or reported depending on `schema.extra_fields`.
    """
    errors: dict[str, str] = {}

    for field, validator in schema.fields.items():
        if field not in data:
            errors[field] = "is required"
            continue 

        try:
            passed = validator(data[field])
        except TypeError:
            errors[field] = "has an invalid type"
            continue

        if not passed:
            errors[field] = getattr(validator, "message", "failed validation")

    if schema.extra_fields == "forbid":
        for key in data:
            if key not in schema.fields:
                errors[key] = "is not allowed"

    return errors