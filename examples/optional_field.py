from validator.combinators import optional
from validator.schema import Schema, validate
from validator.strings import is_str

fields = {"name": is_str, "nickname": optional(is_str)}
schema = Schema(fields)
data: dict = {}

print(validate(data, schema))   # {'name': 'is required'}