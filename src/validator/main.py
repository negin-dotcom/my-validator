from validator.combinators import all_of, check_length
from validator.numbers import is_int
from validator.schema import validate
from validator.strings import is_str, max_length


schema = {
    "username": all_of(is_str, check_length(max_length, 3)),
    "age": all_of(is_int),
}


if __name__ == "__main__":
    print(validate({"username": "you", "age": 10}, schema))