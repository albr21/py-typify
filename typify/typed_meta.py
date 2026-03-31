from typing import get_type_hints
from validation import is_valid_type
import functools
import inspect

class TypedMeta(type):
    """
    Metaclass that automatically applies runtime type checking
    to all public methods. Supports generic types (Optional, Union,
    list[int], dict[str, int], etc.) via the shared validation module.
    """

    def __new__(mcs, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith("_"):
                namespace[attr_name] = mcs._typecheck(attr_value)
        return super().__new__(mcs, name, bases, namespace)

    @staticmethod
    def _typecheck(func):
        """Decorator that enforces type hints at runtime."""
        hints = get_type_hints(func)
        sig = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for param_name, value in bound.arguments.items():
                if param_name in ("self", "cls"):
                    continue
                expected = hints.get(param_name)
                if expected is not None and not is_valid_type(value, expected):
                    raise TypeError(
                        f"{func.__qualname__}: '{param_name}' must be {expected}, "
                        f"got {type(value).__name__} ({value!r})"
                    )

            result = func(*args, **kwargs)

            expected_return = hints.get("return")
            if expected_return is not None and not is_valid_type(result, expected_return):
                raise TypeError(
                    f"{func.__qualname__}: return must be {expected_return}, "
                    f"got {type(result).__name__} ({result!r})"
                )

            return result
        return wrapper
