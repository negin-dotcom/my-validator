from typing import Any, TypeGuard

from validator.decorators import rule


# For `mypy --strict`, type parameters are declared.
@rule("list", "{value} must be a list")
def is_list(value: Any) -> TypeGuard[list[Any]]:
    return isinstance(value, list)


@rule("tuple", "{value} must be a tuple")
def is_tuple(value: Any) -> TypeGuard[tuple[Any, ...]]:
    return isinstance(value, tuple)


@rule("dictionary", "{value} must be a dictionary")
def is_dict(value: Any) -> TypeGuard[dict[Any, Any]]:
    return isinstance(value, dict)


@rule("set", "{value} must be a set")
def is_set(value: Any) -> TypeGuard[set[Any]]:
    return isinstance(value, set)


@rule("None", "{value} must be None")
def is_none(value: Any) -> TypeGuard[None]:
    return value is None