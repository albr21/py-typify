import pytest
from conftest import (
    SimpleModel, WithDefaults, WithOptional, WithUnion, WithAny
)

class TestTypedInstantiationValid:
    def test_typed_instantiation_simple_model(self):
        m = SimpleModel(name="Alice", age=30, active=True)
        assert m.name == "Alice"
        assert m.age == 30
        assert m.active is True

    def test_typed_instantiation_with_defaults(self):
        m = WithDefaults()
        assert m.host == "localhost"
        assert m.port == 8080
        assert m.debug is False

    def test_typed_instantiation_defaults_overridden(self):
        m = WithDefaults(host="0.0.0.0", port=3000, debug=True)
        assert m.host == "0.0.0.0"
        assert m.port == 3000
        assert m.debug is True

    def test_typed_instantiation_optional_with_value(self):
        m = WithOptional(name="Alice", nickname="Ali")
        assert m.nickname == "Ali"

    def test_typed_instantiation_optional_with_none(self):
        m = WithOptional(name="Alice", nickname=None)
        assert m.nickname is None

    def test_typed_instantiation_optional_default_none(self):
        m = WithOptional(name="Alice")
        assert m.nickname is None

    def test_typed_instantiation_union_int(self):
        m = WithUnion(value=42)
        assert m.value == 42

    def test_typed_instantiation_union_float(self):
        m = WithUnion(value=3.14)
        assert m.value == 3.14

    def test_typed_instantiation_union_none_label(self):
        m = WithUnion(value=1, label=None)
        assert m.label is None

    def test_typed_instantiation_union_str_label(self):
        m = WithUnion(value=1, label="test")
        assert m.label == "test"

    def test_typed_instantiation_any_str(self):
        m = WithAny(data="hello")
        assert m.data == "hello"

    def test_typed_instantiation_any_int(self):
        m = WithAny(data=42)
        assert m.data == 42

    def test_typed_instantiation_any_list(self):
        m = WithAny(data=[1, "mixed", None])
        assert m.data == [1, "mixed", None]

    def test_typed_instantiation_any_none(self):
        m = WithAny(data=None, meta=None)
        assert m.data is None

class TestTypedInstantiationInvalid:
    def test_typed_instantiation_str_instead_of_int(self):
        with pytest.raises(TypeError, match="'age'"):
            SimpleModel(name="Alice", age="thirty", active=True)

    def test_typed_instantiation_int_instead_of_str(self):
        with pytest.raises(TypeError, match="'name'"):
            SimpleModel(name=123, age=30, active=True)

    def test_typed_instantiation_str_instead_of_bool(self):
        with pytest.raises(TypeError, match="'active'"):
            SimpleModel(name="Alice", age=30, active="yes")

    def test_typed_instantiation_none_for_required_str(self):
        with pytest.raises(TypeError, match="'name'"):
            SimpleModel(name=None, age=30, active=True)

    def test_typed_instantiation_optional_wrong_type(self):
        with pytest.raises(TypeError, match="'nickname'"):
            WithOptional(name="Alice", nickname=123)

    def test_typed_instantiation_union_wrong_type(self):
        with pytest.raises(TypeError, match="'value'"):
            WithUnion(value="not a number")

    def test_typed_instantiation_defaults_wrong_override(self):
        with pytest.raises(TypeError, match="'port'"):
            WithDefaults(port="not_a_port")
