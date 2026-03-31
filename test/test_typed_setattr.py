import pytest
from conftest import (
    SimpleModel, WithOptional, WithUnion, WithAny, WithList, WithDict
)

class TestTypedSetattrValid:
    def test_typed_setattr_reassignment_simple(self):
        m = SimpleModel(name="Alice", age=30, active=True)
        m.name = "Bob"
        m.age = 25
        m.active = False
        assert m.name == "Bob"
        assert m.age == 25
        assert m.active is False

    def test_typed_setattr_optional_to_none(self):
        m = WithOptional(name="Alice", nickname="Ali")
        m.nickname = None
        assert m.nickname is None

    def test_typed_setattr_optional_to_value(self):
        m = WithOptional(name="Alice")
        m.nickname = "Ali"
        assert m.nickname == "Ali"

    def test_typed_setattr_list(self):
        m = WithList(tags=["a"], scores=[1])
        m.tags = ["x", "y"]
        assert m.tags == ["x", "y"]

    def test_typed_setattr_dict(self):
        m = WithDict(config={"a": 1})
        m.config = {"b": 2}
        assert m.config == {"b": 2}

    def test_typed_setattr_any(self):
        m = WithAny(data="hello")
        m.data = 42
        m.data = [1, 2, 3]
        m.data = None
        assert m.data is None

    def test_typed_setattr_union(self):
        m = WithUnion(value=42)
        m.value = 3.14
        assert m.value == 3.14

class TestTypedSetattrInvalid:
    def test_typed_setattr_invalid_str(self):
        m = SimpleModel(name="Alice", age=30, active=True)
        with pytest.raises(TypeError, match="'name'"):
            m.name = 123

    def test_typed_setattr_invalid_int(self):
        m = SimpleModel(name="Alice", age=30, active=True)
        with pytest.raises(TypeError, match="'age'"):
            m.age = "old"

    def test_typed_setattr_invalid_bool(self):
        m = SimpleModel(name="Alice", age=30, active=True)
        with pytest.raises(TypeError, match="'active'"):
            m.active = "yes"

    def test_typed_setattr_invalid_optional(self):
        m = WithOptional(name="Alice")
        with pytest.raises(TypeError, match="'nickname'"):
            m.nickname = 42

    def test_typed_setattr_invalid_list_items(self):
        m = WithList(tags=["a"], scores=[1])
        with pytest.raises(TypeError, match="'tags'"):
            m.tags = [1, 2]

    def test_typed_setattr_invalid_dict(self):
        m = WithDict(config={"a": 1})
        with pytest.raises(TypeError, match="'config'"):
            m.config = {"a": "not_int"}

    def test_typed_setattr_invalid_union(self):
        m = WithUnion(value=42)
        with pytest.raises(TypeError, match="'value'"):
            m.value = "not_a_number"

    def test_typed_setattr_preserves_value_on_error(self):
        m = SimpleModel(name="Alice", age=30, active=True)
        with pytest.raises(TypeError):
            m.age = "invalid"
        assert m.age == 30
