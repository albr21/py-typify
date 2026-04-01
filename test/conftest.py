from dataclasses import dataclass
from typing import Any, Optional, Union

from typify.typed import Typed
from typify.typed_meta import TypedMeta

# =============================================================================
# Typed fixtures
# =============================================================================

@dataclass
class SimpleModel(Typed):
    name: str
    age: int
    active: bool

@dataclass
class WithDefaults(Typed):
    host: str = "localhost"
    port: int = 8080
    debug: bool = False

@dataclass
class WithOptional(Typed):
    name: str
    nickname: Optional[str] = None

@dataclass
class WithUnion(Typed):
    value: Union[int, float]
    label: Union[str, None] = None

@dataclass
class WithAny(Typed):
    data: Any
    meta: Any = None

@dataclass
class WithList(Typed):
    tags: list[str]
    scores: list[int]

@dataclass
class WithSet(Typed):
    ids: set[int]

@dataclass
class WithFrozenSet(Typed):
    codes: frozenset[str]

@dataclass
class WithDict(Typed):
    config: dict[str, int]

@dataclass
class WithTuple(Typed):
    point: tuple[int, int]

@dataclass
class WithVarTuple(Typed):
    values: tuple[int, ...]

@dataclass
class WithMixedTuple(Typed):
    record: tuple[str, int, bool]

@dataclass
class WithNestedList(Typed):
    matrix: list[list[int]]

@dataclass
class WithNestedDict(Typed):
    registry: dict[str, list[int]]

@dataclass
class WithComplexUnion(Typed):
    data: Union[str, list[int], dict[str, float]]

@dataclass
class Address(Typed):
    street: str
    city: str
    zip_code: str

@dataclass
class Person(Typed):
    name: str
    age: int
    address: Address

@dataclass
class Company(Typed):
    name: str
    ceo: Person
    employees: list[Person]

@dataclass
class Tag(Typed):
    label: str
    priority: int

@dataclass
class Article(Typed):
    title: str
    author: Person
    tags: list[Tag]
    metadata: dict[str, Any]

@dataclass
class OptionalNested(Typed):
    name: str
    address: Optional[Address] = None

@dataclass
class UnionNested(Typed):
    owner: Union[Person, Company]

@dataclass
class DeeplyNested(Typed):
    company: Company

# =============================================================================
# TypedMeta fixtures
# =============================================================================

class SimpleService(metaclass=TypedMeta):
    def greet(self, name: str) -> str:
        return f"Hello, {name}"

    def add(self, a: int, b: int) -> int:
        return a + b

    def _private(self, value: int):
        return value

class DefaultService(metaclass=TypedMeta):
    def with_defaults(self, name: str, count: int = 1) -> str:
        return name * count

class OptionalService(metaclass=TypedMeta):
    def process(self, value: Optional[str]) -> Optional[str]:
        return value.upper() if value else None

class UnionService(metaclass=TypedMeta):
    def process(self, value: Union[int, str]) -> str:
        return str(value)

class AnyService(metaclass=TypedMeta):
    def process(self, value: Any) -> Any:
        return value

class ListService(metaclass=TypedMeta):
    def process(self, items: list[int]) -> list[int]:
        return [x * 2 for x in items]

class SetService(metaclass=TypedMeta):
    def process(self, items: set[str]) -> set[str]:
        return items

class FrozenSetService(metaclass=TypedMeta):
    def process(self, items: frozenset[int]) -> frozenset[int]:
        return items

class DictService(metaclass=TypedMeta):
    def process(self, data: dict[str, int]) -> dict[str, int]:
        return {k: v * 2 for k, v in data.items()}

class TupleFixedService(metaclass=TypedMeta):
    def process(self, value: tuple[int, str]) -> tuple[int, str]:
        return value

class TupleVarService(metaclass=TypedMeta):
    def process(self, value: tuple[int, ...]) -> tuple[int, ...]:
        return value

class MixedTupleService(metaclass=TypedMeta):
    def process(self, value: tuple[str, int, bool]) -> tuple[str, int, bool]:
        return value

class NestedListService(metaclass=TypedMeta):
    def process(self, value: list[list[int]]) -> list[list[int]]:
        return value

class NestedDictService(metaclass=TypedMeta):
    def process(self, data: dict[str, list[int]]) -> dict[str, list[int]]:
        return data

class ComplexUnionService(metaclass=TypedMeta):
    def process(self, data: Union[str, list[int], dict[str, float]]) -> Union[str, list[int], dict[str, float]]:
        return data

class BadReturnSimpleService(metaclass=TypedMeta):
    def process(self, name: str) -> int:
        return name  # type: ignore

class BadReturnGenericService(metaclass=TypedMeta):
    def process(self, items: list[int]) -> list[str]:
        return items  # type: ignore

class NoHintsService(metaclass=TypedMeta):
    def process(self, value):
        return value

class NoReturnHintService(metaclass=TypedMeta):
    def process(self, value: int):
        return value * 2

class NonCallableAttrService(metaclass=TypedMeta):
    label = "static_value"

    def process(self, x: int) -> int:
        return x
