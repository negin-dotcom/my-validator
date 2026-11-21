[![CI](https://github.com/negin-dotcom/validator/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/negin-dotcom/validator/actions/workflows/ci.yml)
# A small validator library written in Python. (still being developed)
# Use it instead of writing validations by hand.


# Installation
```bash
git clone https://github.com/negin-dotcom/validator.git
cd validator
uv sync
```

Requires Python 3.12 or newer.
<br>
Autocompletion is added.
<br>
Custom validator is added.


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
- `Extra fields` in the data that are not in the schema are ignored.
