import pytest
from conftest import (
    WithList, WithSet, WithFrozenSet, WithDict, WithTuple, WithVarTuple, WithMixedTuple
)

class TestTypedCollectionsValid:
    def test_typed_collections_list_of_str(self):
        m = WithList(tags=["a", "b", "c"], scores=[1, 2, 3])
        assert m.tags == ["a", "b", "c"]

    def test_typed_collections_list_empty(self):
        m = WithList(tags=[], scores=[])
        assert m.tags == []

    def test_typed_collections_set_of_int(self):
        m = WithSet(ids={1, 2, 3})
        assert m.ids == {1, 2, 3}

    def test_typed_collections_set_empty(self):
        m = WithSet(ids=set())
        assert m.ids == set()

    def test_typed_collections_frozenset_of_str(self):
        m = WithFrozenSet(codes=frozenset(["a", "b"]))
        assert m.codes == frozenset(["a", "b"])

    def test_typed_collections_dict_str_int(self):
        m = WithDict(config={"port": 80, "timeout": 30})
        assert m.config["port"] == 80

    def test_typed_collections_dict_empty(self):
        m = WithDict(config={})
        assert m.config == {}

    def test_typed_collections_tuple_fixed(self):
        m = WithTuple(point=(10, 20))
        assert m.point == (10, 20)

    def test_typed_collections_tuple_variable(self):
        m = WithVarTuple(values=(1, 2, 3, 4, 5))
        assert m.values == (1, 2, 3, 4, 5)

    def test_typed_collections_tuple_variable_empty(self):
        m = WithVarTuple(values=())
        assert m.values == ()

    def test_typed_collections_mixed_tuple(self):
        m = WithMixedTuple(record=("hello", 42, True))
        assert m.record == ("hello", 42, True)

class TestTypedCollectionsInvalid:
    def test_typed_collections_list_wrong_item_type(self):
        with pytest.raises(TypeError, match="'tags'"):
            WithList(tags=["a", 2, "c"], scores=[1])

    def test_typed_collections_list_wrong_container_type(self):
        with pytest.raises(TypeError, match="'tags'"):
            WithList(tags="not_a_list", scores=[1])

    def test_typed_collections_set_wrong_item_type(self):
        with pytest.raises(TypeError, match="'ids'"):
            WithSet(ids={1, "two", 3})

    def test_typed_collections_set_wrong_container(self):
        with pytest.raises(TypeError, match="'ids'"):
            WithSet(ids=[1, 2, 3])

    def test_typed_collections_frozenset_wrong_item_type(self):
        with pytest.raises(TypeError, match="'codes'"):
            WithFrozenSet(codes=frozenset([1, 2]))

    def test_typed_collections_dict_wrong_key_type(self):
        with pytest.raises(TypeError, match="'config'"):
            WithDict(config={1: 100})

    def test_typed_collections_dict_wrong_value_type(self):
        with pytest.raises(TypeError, match="'config'"):
            WithDict(config={"port": "eighty"})

    def test_typed_collections_dict_wrong_container(self):
        with pytest.raises(TypeError, match="'config'"):
            WithDict(config=[("port", 80)])

    def test_typed_collections_tuple_wrong_length(self):
        with pytest.raises(TypeError, match="'point'"):
            WithTuple(point=(1, 2, 3))

    def test_typed_collections_tuple_wrong_item_type(self):
        with pytest.raises(TypeError, match="'point'"):
            WithTuple(point=("x", "y"))

    def test_typed_collections_tuple_too_short(self):
        with pytest.raises(TypeError, match="'point'"):
            WithTuple(point=(1,))

    def test_typed_collections_var_tuple_wrong_item(self):
        with pytest.raises(TypeError, match="'values'"):
            WithVarTuple(values=(1, "two", 3))

    def test_typed_collections_mixed_tuple_wrong_types(self):
        with pytest.raises(TypeError, match="'record'"):
            WithMixedTuple(record=(42, "hello", True))

    def test_typed_collections_mixed_tuple_wrong_length(self):
        with pytest.raises(TypeError, match="'record'"):
            WithMixedTuple(record=("hello", 42))
