from dataclasses import dataclass
from collections import deque
from typing import Deque
from typify.typed import Typed
from typify.validation import is_valid_type
from conftest import WithList

class TestTypedEdgeCases:
    def test_validation_is_valid_type_edge_bool_is_int_subclass(self):
        assert is_valid_type(True, int) is True

    def test_validation_is_valid_type_edge_int_is_not_bool(self):
        assert is_valid_type(1, bool) is False

    def test_validation_is_valid_type_edge_untyped_attr_no_check(self):
        @dataclass
        class Flexible(Typed):
            name: str

        m = Flexible(name="test")
        m.extra = 42
        assert m.extra == 42

    def test_validation_is_valid_type_edge_large_collection(self):
        m = WithList(tags=["tag"] * 10000, scores=[1] * 10000)
        assert len(m.tags) == 10000

    def test_validation_is_valid_type_edge_deeply_nested_valid(self):
        assert is_valid_type(
            {"a": {"b": [1, 2]}},
            dict[str, dict[str, list[int]]]
        ) is True

    def test_validation_is_valid_type_edge_deeply_nested_invalid(self):
        assert is_valid_type(
            {"a": {"b": [1, "2"]}},
            dict[str, dict[str, list[int]]]
        ) is False

    def test_validation_is_valid_type_edge_generic_without_args(self):
        assert is_valid_type([1, "a"], list) is True

    def test_validation_is_valid_type_edge_tuple_single_element(self):
        assert is_valid_type(("hello",), tuple[str]) is True

    def test_validation_is_valid_type_edge_tuple_single_wrong(self):
        assert is_valid_type((42,), tuple[str]) is False

    def test_validation_is_valid_type_edge_unknown_generic_origin_returns_true(self):
        # Deque[int] has origin=deque, which is not handled by any branch
        d = deque([1, 2, 3])
        assert is_valid_type(d, Deque[int]) is True
