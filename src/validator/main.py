from validator.combinators import all_of, check_length
from validator.numbers import in_range_of, is_int
from validator.schema import validate
from validator.strings import is_str, max_length

if __name__ == "__main__":
    schema = {
        "username": all_of(is_str, check_length(max_length, 4)),
        "age": all_of(is_int, in_range_of(3, 18))
    }

    data = {
        "username": "nen",
        "age": 12
    }

    print(validate(data, schema))