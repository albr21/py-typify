# py-typify

A Python module for runtime type checking based on type annotations.

## Usage

```python
from typify import Typed, TypedMeta
from dataclasses import dataclass

# Example of using Typed to create a class with type-checked attributes

@dataclass
class MyClass(Typed):
    x: int
    y: str

obj = MyClass(x=10, y="hello")  # This will work
obj = MyClass(x="not an int", y="hello")  # This will raise a TypeError


# Example of using TypedMeta to create a class with type-checked attributes

class MyMetaClass(metaclass=TypedMeta):
    def method_1(self, a: int) -> str:
        return "Hello"

MetaObj = MyMetaClass()
MetaObj.method_1(10)  # This will work
MetaObj.method_1("not an int")  # This will raise a TypeError
```

## Contributing

Check out the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
