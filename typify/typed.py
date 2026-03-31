from typing import get_type_hints, Any
from validation import is_valid_type

class Typed:
    """
    A base class that enforces type checking on its attributes.
    When a class inherits from `Typed`, it will automatically check the types of
    its attributes against the type hints defined in the class.
    If an attribute is assigned a value that does not match its expected type,
    a `TypeError` will be raised.
    """

    def __post_init__(self):
        hints = get_type_hints(self.__class__)
        for name, expected in hints.items():
            if not hasattr(self, name):
                continue
            value = getattr(self, name)
            if not is_valid_type(value, expected):
                raise TypeError(f"'{name}' must be {expected}, got {type(value).__name__} ({value!r})")

    def __setattr__(self, name: str, value: Any) -> None:
        hints = get_type_hints(self.__class__)
        expected = hints.get(name)

        if expected is not None and not is_valid_type(value, expected):
            raise TypeError(
                f"'{name}' must be {expected}, got {type(value).__name__} ({value!r})"
            )

        super().__setattr__(name, value)
