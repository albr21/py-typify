import pytest
from typing import Any, Optional, Union
from validation import is_valid_type

class TestTypedIsValidTypeSimple:
    @pytest.mark.parametrize("value,expected", [
        ("hello", str),
        (42, int),
        (3.14, float),
        (True, bool),
        (b"bytes", bytes),
        (None, type(None)),
    ])
    def test_validation_is_valid_type_simple_valid(self, value, expected):
        assert is_valid_type(value, expected) is True

    @pytest.mark.parametrize("value,expected", [
        (42, str),
        ("hello", int),
        (None, str),
        (3.14, int),
        ("true", bool),
    ])
    def test_validation_is_valid_type_simple_invalid(self, value, expected):
        assert is_valid_type(value, expected) is False


class TestTypedIsValidTypeAny:
    @pytest.mark.parametrize("value", ["hello", 42, None, [], {}, object()])
    def test_validation_is_valid_type_any_always_valid(self, value):
        assert is_valid_type(value, Any) is True


class TestTypedIsValidTypeOptional:
    def test_validation_is_valid_type_optional_with_value(self):
        assert is_valid_type("hello", Optional[str]) is True

    def test_validation_is_valid_type_optional_with_none(self):
        assert is_valid_type(None, Optional[str]) is True

    def test_validation_is_valid_type_optional_wrong_type(self):
        assert is_valid_type(42, Optional[str]) is False


class TestTypedIsValidTypeUnion:
    def test_validation_is_valid_type_union_first(self):
        assert is_valid_type(42, Union[int, str]) is True

    def test_validation_is_valid_type_union_second(self):
        assert is_valid_type("hi", Union[int, str]) is True

    def test_validation_is_valid_type_union_none(self):
        assert is_valid_type(None, Union[int, str]) is False

    def test_validation_is_valid_type_union_no_match(self):
        assert is_valid_type(3.14, Union[int, str]) is False


class TestTypedIsValidTypeList:
    def test_validation_is_valid_type_list_valid(self):
        assert is_valid_type([1, 2, 3], list[int]) is True

    def test_validation_is_valid_type_list_empty(self):
        assert is_valid_type([], list[int]) is True

    def test_validation_is_valid_type_list_invalid_item(self):
        assert is_valid_type([1, "2"], list[int]) is False

    def test_validation_is_valid_type_list_wrong_container(self):
        assert is_valid_type((1, 2), list[int]) is False


class TestTypedIsValidTypeSet:
    def test_validation_is_valid_type_set_valid(self):
        assert is_valid_type({1, 2}, set[int]) is True

    def test_validation_is_valid_type_set_invalid_item(self):
        assert is_valid_type({1, "2"}, set[int]) is False


class TestTypedIsValidTypeFrozenSet:
    def test_validation_is_valid_type_frozenset_valid(self):
        assert is_valid_type(frozenset(["a"]), frozenset[str]) is True

    def test_validation_is_valid_type_frozenset_invalid_item(self):
        assert is_valid_type(frozenset([1]), frozenset[str]) is False


class TestTypedIsValidTypeDict:
    def test_validation_is_valid_type_dict_valid(self):
        assert is_valid_type({"a": 1}, dict[str, int]) is True

    def test_validation_is_valid_type_dict_empty(self):
        assert is_valid_type({}, dict[str, int]) is True

    def test_validation_is_valid_type_dict_invalid_key(self):
        assert is_valid_type({1: 1}, dict[str, int]) is False

    def test_validation_is_valid_type_dict_invalid_value(self):
        assert is_valid_type({"a": "b"}, dict[str, int]) is False


class TestTypedIsValidTypeTupleFixed:
    def test_validation_is_valid_type_tuple_fixed_valid(self):
        assert is_valid_type((1, "a"), tuple[int, str]) is True

    def test_validation_is_valid_type_tuple_fixed_wrong_type(self):
        assert is_valid_type(("a", 1), tuple[int, str]) is False

    def test_validation_is_valid_type_tuple_fixed_too_long(self):
        assert is_valid_type((1, "a", True), tuple[int, str]) is False

    def test_validation_is_valid_type_tuple_fixed_too_short(self):
        assert is_valid_type((1,), tuple[int, str]) is False

    def test_validation_is_valid_type_tuple_fixed_empty(self):
        assert is_valid_type((), tuple[int, str]) is False


class TestTypedIsValidTypeTupleVariable:
    def test_validation_is_valid_type_var_tuple_valid(self):
        assert is_valid_type((1, 2, 3), tuple[int, ...]) is True

    def test_validation_is_valid_type_var_tuple_empty(self):
        assert is_valid_type((), tuple[int, ...]) is True

    def test_validation_is_valid_type_var_tuple_invalid_item(self):
        assert is_valid_type((1, "2"), tuple[int, ...]) is False


class TestTypedIsValidTypeNested:
    def test_validation_is_valid_type_nested_list(self):
        assert is_valid_type([[1, 2], [3]], list[list[int]]) is True

    def test_validation_is_valid_type_nested_list_invalid(self):
        assert is_valid_type([[1, "2"]], list[list[int]]) is False

    def test_validation_is_valid_type_nested_dict(self):
        assert is_valid_type({"a": [1, 2]}, dict[str, list[int]]) is True

    def test_validation_is_valid_type_nested_dict_invalid(self):
        assert is_valid_type({"a": [1, "2"]}, dict[str, list[int]]) is False
