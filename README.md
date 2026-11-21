[![CI](https://github.com/negin-dotcom/validator/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/negin-dotcom/validator/actions/workflows/ci.yml)
# validator 

A small validator library written in Python.
<br>
Use it instead of writing validations by hand.

> Status: early development. The API may still change.

This library is:
- Simple and dependency-free.
- Explicit about bad inputs.

## Why
Hand-written checks like "is this long enough?" or "is this a valid email?" are easy to get wrong, and every project ends up repeating them.
<br>
All validators are plain functions that return `True` or `False`. 
<br>
Passing the wrong type to a validator raises `TypeError` instead of simply returning False.


## How it works
- **Validators** are functions that take a value and return a bool (True or False): `is_str`, `is_int`, `is_float`, `is_list`, etc.
- **Combinators** build bigger rules from small ones: `all_of`, `any_of`, etc.
- **Schema + validate** apply a validator to each field and return a dictionary of `field -> message`. An empty dict means the data is valid.


# Installation
```bash
git clone https://github.com/negin-dotcom/validator.git
cd validator
uv sync
```

Requires Python 3.12 or newer.
<br>
Auto completion is added.
<br>
Custom validator is added.
<br>
Json schema support is added.


## Sample Usage 
```python
from validator import validate, all_of, is_str, check_length, min_length, in_range_of, Schema


fields = {
    "username": all_of(is_str, check_length(min_length, 3)),
    "age": in_range_of(18, 35),
    "password": all_of(is_str, check_length(min_length, 8)),
}

schema = Schema(fields)
data = {"username": "ab", "age": 12}

print(validate(data, schema))
```

```python
{
    "username": "must satisfy all of: ...",
    "age": "must be between 18 and 35",
    "password": "is required",
}
```

Notes:
- A `missing field` is reported as `is required`.
- A value of the wrong type is reported as `has an invalid type`.
- Extra fields (keys in the data that are not in the schema) are ignored by
default. Use `Schema(fields, extra_fields="forbid")` to report each of them
as `is not allowed`.
