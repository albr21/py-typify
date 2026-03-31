import pytest
from conftest import (
    ListService, SetService, FrozenSetService, DictService,
    TupleFixedService, TupleVarService, MixedTupleService
)

class TestTypedMetaCollectionsValid:
    def test_meta_collections_list(self):
        s = ListService()
        assert s.process([1, 2, 3]) == [2, 4, 6]

    def test_meta_collections_list_empty(self):
        s = ListService()
        assert s.process([]) == []

    def test_meta_collections_set(self):
        s = SetService()
        assert s.process({"a", "b"}) == {"a", "b"}

    def test_meta_collections_set_empty(self):
        s = SetService()
        assert s.process(set()) == set()

    def test_meta_collections_frozenset(self):
        s = FrozenSetService()
        assert s.process(frozenset([1, 2])) == frozenset([1, 2])

    def test_meta_collections_dict(self):
        s = DictService()
        assert s.process({"a": 1}) == {"a": 2}

    def test_meta_collections_dict_empty(self):
        s = DictService()
        assert s.process({}) == {}

    def test_meta_collections_tuple_fixed(self):
        s = TupleFixedService()
        assert s.process((1, "a")) == (1, "a")

    def test_meta_collections_tuple_variable(self):
        s = TupleVarService()
        assert s.process((1, 2, 3)) == (1, 2, 3)

    def test_meta_collections_tuple_variable_empty(self):
        s = TupleVarService()
        assert s.process(()) == ()

    def test_meta_collections_mixed_tuple(self):
        s = MixedTupleService()
        assert s.process(("hello", 42, True)) == ("hello", 42, True)

class TestTypedMetaCollectionsInvalid:
    def test_meta_collections_list_wrong_item(self):
        s = ListService()
        with pytest.raises(TypeError, match="'items' must be"):
            s.process([1, "two"])

    def test_meta_collections_list_wrong_container(self):
        s = ListService()
        with pytest.raises(TypeError, match="'items' must be"):
            s.process((1, 2))

    def test_meta_collections_set_wrong_item(self):
        s = SetService()
        with pytest.raises(TypeError, match="'items' must be"):
            s.process({1, 2})

    def test_meta_collections_frozenset_wrong_item(self):
        s = FrozenSetService()
        with pytest.raises(TypeError, match="'items' must be"):
            s.process(frozenset(["a", "b"]))

    def test_meta_collections_dict_wrong_key(self):
        s = DictService()
        with pytest.raises(TypeError, match="'data' must be"):
            s.process({1: 1})

    def test_meta_collections_dict_wrong_value(self):
        s = DictService()
        with pytest.raises(TypeError, match="'data' must be"):
            s.process({"a": "b"})

    def test_meta_collections_dict_wrong_container(self):
        s = DictService()
        with pytest.raises(TypeError, match="'data' must be"):
            s.process([("a", 1)])

    def test_meta_collections_tuple_fixed_wrong_types(self):
        s = TupleFixedService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process(("a", 1))

    def test_meta_collections_tuple_fixed_wrong_length(self):
        s = TupleFixedService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process((1, "a", True))

    def test_meta_collections_tuple_variable_wrong_item(self):
        s = TupleVarService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process((1, "two"))

    def test_meta_collections_mixed_tuple_wrong(self):
        s = MixedTupleService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process((42, "hello", True))
