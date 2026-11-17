from validator.custom import custom_validator
from validator.schema import Schema, validate

if __name__ == "__main__":
    def _is_even(x):
        return x % 2 == 0

    is_even = custom_validator(_is_even, code="even", message="must be even")

    fields = {
        "age": is_even,
    }

    schema = Schema(fields)
    data = {"age": 31}

    print(validate(data, schema))