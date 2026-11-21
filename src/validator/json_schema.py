from validator.containers import is_dict, is_list, is_none
from validator.numbers import is_bool, is_int, is_number
from validator.schema import Schema
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

def from_json_schema(spec) -> Schema:
    fields = {}
    for name, values in spec.get("properties", {}).items():
        if "type" in values:
            type_name = values["type"]
            if type_name not in _TYPES:
                raise ValueError(f"unsupported type {repr(type_name)}")
            fields[name] = _TYPES[values["type"]]
        else:
            fields[name] = lambda value: True
        

    return Schema(fields)
