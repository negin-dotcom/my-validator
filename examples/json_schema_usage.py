from validator.json_schema import from_json_schema
from validator.schema import validate

json_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "age": {"type": "integer"},
    },
}
data = {"username": "negin", "age": "20"}

print(validate(data, from_json_schema(json_schema)))  # {'age': 'must be a string'}