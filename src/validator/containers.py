from typing import Any, TypeGuard


# For `mypy --strict`, type parameters are declared.
def is_list(value: Any) -> TypeGuard[list[Any]]:
    return isinstance(value, list)


def is_tuple(value: Any) -> TypeGuard[tuple[Any, ...]]:
    return isinstance(value, tuple)


def is_dict(value: Any) -> TypeGuard[dict[Any, Any]]:
    return isinstance(value, dict)


def is_set(value: Any) -> TypeGuard[set[Any]]:
    return isinstance(value, set)


def is_none(value: Any) -> TypeGuard[None]:
    return value is None