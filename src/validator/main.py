from validator.combinators import all_of, check_length
from validator.numbers import in_range_of
from validator.schema import Schema, validate
from validator.strings import is_str, min_length

fields = {
    "username": all_of(is_str, check_length(min_length, 3)),
    "age": in_range_of(18, 35),
    "password": all_of(is_str, check_length(min_length, 8)),
}

schema = Schema(fields)
data = {"username": "ab", "age": 12}

print(validate(data, schema))