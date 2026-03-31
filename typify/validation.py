from typing import Any, get_origin, get_args, Union

def is_valid_type(value: Any, expected: type) -> bool:
    """
    Verify if the value is of the expected type, including support for
    generic types like List[int] or Dict[str, int].
    """

    if expected is Any: return True

    origin = get_origin(expected)

    if origin is None: return isinstance(value, expected)

    if origin is Union: return any(is_valid_type(value, arg) for arg in get_args(expected))

    if not isinstance(value, origin): return False

    type_args = get_args(expected)
    if not type_args: return True

    if origin in (list, set, frozenset): return all(is_valid_type(item, type_args[0]) for item in value)

    if origin is dict:
        return all(
            is_valid_type(k, type_args[0]) and is_valid_type(v, type_args[1])
            for k, v in value.items()
        )

    if origin is tuple:
        if len(type_args) == 2 and type_args[1] is Ellipsis:
            return all(is_valid_type(item, type_args[0]) for item in value)
        if len(type_args) != len(value):
            return False
        return all(is_valid_type(item, arg) for item, arg in zip(value, type_args))

    return True
