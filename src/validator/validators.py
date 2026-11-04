from typing import Any, Union



# -------- Helper functions ------------------------
def _require_int(value, name: str = "value") -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be of type int, got {type(value).__name__}")


def _require_number(value, name: str = "value") -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")


def _require_type(value, expected: Union[type, tuple[type, ...]]) -> None:
    if not isinstance(value, expected):
        if isinstance(expected, tuple):
            names = " or ".join(t.__name__ for t in expected)
        else:
            names = expected.__name__
        raise TypeError(f"value must be of type {names}, got {type(value).__name__}")

# --------------------------------------------------


def min_length(value: str, minimum: int) -> bool:
    _require_type(value, str)
    _require_int(minimum, "minimum")
    
    if minimum < 0:
        raise ValueError("minimum must be >= 0")
    
    return len(value) >= minimum


def max_length(value: str, maximum: int) -> bool:
    _require_type(value, str)
    _require_int(maximum, "maximum")
        
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
    _require_number(value)
    _require_number(low, "low")
    _require_number(high, "high")

    if low > high:
        raise ValueError("low must be <= high")

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


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)