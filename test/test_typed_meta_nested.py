import pytest
from conftest import (
    NestedListService, NestedDictService, ComplexUnionService
)

class TestTypedMetaNestedValid:
    def test_meta_nested_list(self):
        s = NestedListService()
        assert s.process([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]

    def test_meta_nested_list_empty_inner(self):
        s = NestedListService()
        assert s.process([[], []]) == [[], []]

    def test_meta_nested_list_empty_outer(self):
        s = NestedListService()
        assert s.process([]) == []

    def test_meta_nested_dict(self):
        s = NestedDictService()
        assert s.process({"g1": [1, 2], "g2": [3]}) == {"g1": [1, 2], "g2": [3]}

    def test_meta_nested_dict_empty(self):
        s = NestedDictService()
        assert s.process({}) == {}

    def test_meta_nested_complex_union_str(self):
        s = ComplexUnionService()
        assert s.process("hello") == "hello"

    def test_meta_nested_complex_union_list(self):
        s = ComplexUnionService()
        assert s.process([1, 2, 3]) == [1, 2, 3]

    def test_meta_nested_complex_union_dict(self):
        s = ComplexUnionService()
        assert s.process({"pi": 3.14}) == {"pi": 3.14}

class TestTypedMetaNestedInvalid:
    def test_meta_nested_list_wrong_inner(self):
        s = NestedListService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process([[1, "two"]])

    def test_meta_nested_list_wrong_structure(self):
        s = NestedListService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process([1, 2, 3])

    def test_meta_nested_dict_wrong_inner(self):
        s = NestedDictService()
        with pytest.raises(TypeError, match="'data' must be"):
            s.process({"group": [1, "two"]})

    def test_meta_nested_complex_union_no_match(self):
        s = ComplexUnionService()
        with pytest.raises(TypeError, match="'data' must be"):
            s.process(42)

    def test_meta_nested_complex_union_list_wrong_item(self):
        s = ComplexUnionService()
        with pytest.raises(TypeError, match="'data' must be"):
            s.process([1, "two"])

    def test_meta_nested_complex_union_dict_wrong_value(self):
        s = ComplexUnionService()
        with pytest.raises(TypeError, match="'data' must be"):
            s.process({"pi": "not_float"})
