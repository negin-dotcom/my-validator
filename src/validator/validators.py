class Int:
    pass 


class Str:
    pass 


def _require_number(value, name: str = "value") -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")


def _require_type(value, expected: type) -> None:
    if not isinstance(value, expected):
        if isinstance(expected, tuple):
            names = " or ".join(t.__name__ for t in expected)
        else:
            names = expected.__name__
        raise TypeError(f"value must be of type {names}, got {type(value).__name__}")


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


def in_range(value: float, low: float, high: float) -> bool:
    _require_type(value, (int, float))
    _require_type(low, (int, float))
    _require_type(high, (int, float))

    if low > high:
        raise TypeError(f"{high} must be equal to or greater than {low}")

    return low <= value <= high


def is_positive(value: float) -> bool:
    _require_number(value)
    return value > 0


def is_negative(value: float) -> bool:
    _require_number(value)
    return value < 0


def is_non_positive(value: float) -> bool:
    _require_number(value)
    return value <= 0


def is_non_negative(value: float) -> bool:
    _require_number(value)
    return value >= 0
