class Int:
    pass 


class Str:
    pass

def _require_type(value, expected: type) -> None:
    if not isinstance(value, expected):
        raise TypeError(f"value must be of type {expected.__name__}, got {type(value).__name__}")


def min_length(value: str, minimum: int) -> bool:
    _require_type(value, str)
    
    if minimum < 0:
        raise ValueError("minimum must be >= 0")
    
    return len(value) >= minimum


def max_length(value: str, maximum: int) -> bool:
    _require_type(value, str)
        
    if maximum < 0:
        raise ValueError("maximum must be >= 0")

    return len(value) <= maximum


def not_empty(value: str) -> bool:
    _require_type(value, str)

    return bool(value.strip())


def is_alpha(value: str) -> bool:
    _require_type(value, str)

    return value.isalpha()


def is_numeric(value: str) -> bool:
    _require_type(value, str)

    return value.isdecimal()
            