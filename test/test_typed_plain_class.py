import pytest
from typing import Optional, Union
from typed import Typed

class PlainSimple(Typed):
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

class PlainWithPostInit(Typed):
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.__post_init__()

class PlainOptional(Typed):
    name: str
    value: Optional[int] = None

    def __init__(self, name: str, value: Optional[int] = None):
        self.name = name
        self.value = value

class PlainUnion(Typed):
    data: Union[int, str]

    def __init__(self, data: Union[int, str]):
        self.data = data

class PlainWithList(Typed):
    items: list[int]

    def __init__(self, items: list[int]):
        self.items = items

class TestPlainClassInstantiation:
    def test_plain_valid(self):
        p = PlainSimple("Alice", 30)
        assert p.name == "Alice"
        assert p.age == 30

    def test_plain_invalid_name(self):
        with pytest.raises(TypeError, match="'name' must be"):
            PlainSimple(42, 30)

    def test_plain_invalid_age(self):
        with pytest.raises(TypeError, match="'age' must be"):
            PlainSimple("Alice", "old")

class TestPlainClassSetattr:
    def test_plain_setattr_valid(self):
        p = PlainSimple("Alice", 30)
        p.name = "Bob"
        assert p.name == "Bob"

    def test_plain_setattr_invalid(self):
        p = PlainSimple("Alice", 30)
        with pytest.raises(TypeError, match="'name' must be"):
            p.name = 123

    def test_plain_setattr_dynamic_attr_no_hint(self):
        p = PlainSimple("Alice", 30)
        p.extra = "anything"
        assert p.extra == "anything"

class TestPlainClassPostInit:
    def test_post_init_valid(self):
        p = PlainWithPostInit("Alice", 30)
        assert p.name == "Alice"

    def test_post_init_invalid_bypassing_setattr(self):
        p = object.__new__(PlainWithPostInit)
        object.__setattr__(p, 'name', 42)
        object.__setattr__(p, 'age', "not_int")
        with pytest.raises(TypeError, match="'name' must be"):
            p.__post_init__()

    def test_post_init_missing_attr(self):
        p = object.__new__(PlainWithPostInit)
        p.__post_init__()

class TestPlainClassOptional:
    def test_plain_optional_with_value(self):
        p = PlainOptional("Alice", 42)
        assert p.value == 42

    def test_plain_optional_with_none(self):
        p = PlainOptional("Alice", None)
        assert p.value is None

    def test_plain_optional_invalid(self):
        with pytest.raises(TypeError, match="'value' must be"):
            PlainOptional("Alice", "not_int")

class TestPlainClassUnion:
    def test_plain_union_int(self):
        p = PlainUnion(42)
        assert p.data == 42

    def test_plain_union_str(self):
        p = PlainUnion("hello")
        assert p.data == "hello"

    def test_plain_union_invalid(self):
        with pytest.raises(TypeError, match="'data' must be"):
            PlainUnion(3.14)

class TestPlainClassList:
    def test_plain_list_valid(self):
        p = PlainWithList([1, 2, 3])
        assert p.items == [1, 2, 3]

    def test_plain_list_invalid(self):
        with pytest.raises(TypeError, match="'items' must be"):
            PlainWithList([1, "two"])
