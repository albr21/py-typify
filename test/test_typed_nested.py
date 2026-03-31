import pytest
from conftest import (
    WithNestedList, WithNestedDict, WithComplexUnion
)

class TestTypedNestedValid:
    def test_typed_nested_list(self):
        m = WithNestedList(matrix=[[1, 2], [3, 4]])
        assert m.matrix == [[1, 2], [3, 4]]

    def test_typed_nested_list_empty_inner(self):
        m = WithNestedList(matrix=[[], []])
        assert m.matrix == [[], []]

    def test_typed_nested_dict(self):
        m = WithNestedDict(registry={"group1": [1, 2], "group2": [3]})
        assert m.registry == {"group1": [1, 2], "group2": [3]}

    def test_typed_nested_complex_union_str(self):
        m = WithComplexUnion(data="hello")
        assert m.data == "hello"

    def test_typed_nested_complex_union_list_int(self):
        m = WithComplexUnion(data=[1, 2, 3])
        assert m.data == [1, 2, 3]

    def test_typed_nested_complex_union_dict(self):
        m = WithComplexUnion(data={"pi": 3.14})
        assert m.data == {"pi": 3.14}

class TestTypedNestedInvalid:
    def test_typed_nested_list_wrong_inner_type(self):
        with pytest.raises(TypeError, match="'matrix'"):
            WithNestedList(matrix=[[1, "two"], [3, 4]])

    def test_typed_nested_list_wrong_structure(self):
        with pytest.raises(TypeError, match="'matrix'"):
            WithNestedList(matrix=[1, 2, 3])

    def test_typed_nested_dict_wrong_inner_type(self):
        with pytest.raises(TypeError, match="'registry'"):
            WithNestedDict(registry={"group": [1, "two"]})

    def test_typed_nested_complex_union_no_match(self):
        with pytest.raises(TypeError, match="'data'"):
            WithComplexUnion(data=42)

    def test_typed_nested_complex_union_list_wrong_item(self):
        with pytest.raises(TypeError, match="'data'"):
            WithComplexUnion(data=[1, "two"])

    def test_typed_nested_complex_union_dict_wrong_value(self):
        with pytest.raises(TypeError, match="'data'"):
            WithComplexUnion(data={"pi": "not_float"})
