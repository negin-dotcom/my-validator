from validator.containers import is_dict, is_list, is_none
from validator.numbers import is_bool, is_int, is_number
from validator.schema import ExtraFields, Schema
from validator.strings import is_str

_TYPES = {
    "string": is_str, 
    "integer": is_int,
    "number": is_number,
    "boolean": is_bool,
    "array": is_list,
    "object": is_dict,
    "null": is_none,
}

_EXTRA_FIELDS = ("ignore", "forbid")


def from_json_schema(spec, extra_fields: ExtraFields | None = None) -> Schema:
    if extra_fields is None:
        extra_fields = ("forbid" if spec.get("additionalProperties") is False 
                        else "ignore")
    elif extra_fields not in _EXTRA_FIELDS:
        raise ValueError(f"unsupported extra_fields {repr(extra_fields)}")
    
    fields = {}
    for name, values in spec.get("properties", {}).items():
        if "type" in values:
            type_name = values["type"]
            if type_name not in _TYPES:
                raise ValueError(f"unsupported type {repr(type_name)}")
            fields[name] = _TYPES[values["type"]]
        else:
            fields[name] = lambda value: True
        

    return Schema(fields, extra_fields=extra_fields)
