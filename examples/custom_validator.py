from validator import Schema, custom_validator, validate


def _is_even(x: int) -> bool:
    return x % 2 == 0

is_even = custom_validator(_is_even, code="even", message="must be even")

fields = {
    "age": is_even,
}

schema = Schema(fields)

print(validate({"age": 31}, schema))   # {'age': 'must be even'}
print(validate({"age": 30}, schema))   # {}