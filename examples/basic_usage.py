from validator import (
    Schema,
    all_of,
    check_length,
    in_range_of,
    is_str,
    min_length,
    validate,
)

fields = {
    "username": all_of(is_str, check_length(min_length, 3)),
    "age": in_range_of(18, 35),
    "password": all_of(is_str, check_length(min_length, 8)),
}

schema = Schema(fields)
data = {"username": "ab", "age": 12}


print(validate(data, schema))   # {'username': 'must satisfy all of: must be a string; 
                                # must be equal to or greater than 3', 
                                # 'age': 'must be between 18 and 35', 
                                # 'password': 'is required'}