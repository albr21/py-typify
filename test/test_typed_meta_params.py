import pytest
from conftest import (
    SimpleService, DefaultService, OptionalService, UnionService, AnyService
)

class TestTypedMetaParamsValid:
    def test_meta_params_str(self):
        s = SimpleService()
        assert s.greet("World") == "Hello, World"

    def test_meta_params_int(self):
        s = SimpleService()
        assert s.add(1, 2) == 3

    def test_meta_params_defaults_used(self):
        s = DefaultService()
        assert s.with_defaults("ab") == "ab"

    def test_meta_params_defaults_overridden(self):
        s = DefaultService()
        assert s.with_defaults("ab", 3) == "ababab"

    def test_meta_params_defaults_kwarg(self):
        s = DefaultService()
        assert s.with_defaults(name="ab", count=2) == "abab"

    def test_meta_params_optional_with_value(self):
        s = OptionalService()
        assert s.process("hello") == "HELLO"

    def test_meta_params_optional_with_none(self):
        s = OptionalService()
        assert s.process(None) is None

    def test_meta_params_union_int(self):
        s = UnionService()
        assert s.process(42) == "42"

    def test_meta_params_union_str(self):
        s = UnionService()
        assert s.process("hello") == "hello"

    def test_meta_params_any_int(self):
        s = AnyService()
        assert s.process(42) == 42

    def test_meta_params_any_str(self):
        s = AnyService()
        assert s.process("hello") == "hello"

    def test_meta_params_any_none(self):
        s = AnyService()
        assert s.process(None) is None

    def test_meta_params_any_list(self):
        s = AnyService()
        assert s.process([1, 2]) == [1, 2]

class TestTypedMetaParamsInvalid:
    def test_meta_params_invalid_str(self):
        s = SimpleService()
        with pytest.raises(TypeError, match="'name' must be"):
            s.greet(123)

    def test_meta_params_invalid_int_first(self):
        s = SimpleService()
        with pytest.raises(TypeError, match="'a' must be"):
            s.add("one", 2)

    def test_meta_params_invalid_int_second(self):
        s = SimpleService()
        with pytest.raises(TypeError, match="'b' must be"):
            s.add(1, "two")

    def test_meta_params_invalid_both_raises_first(self):
        s = SimpleService()
        with pytest.raises(TypeError, match="'a' must be"):
            s.add("one", "two")

    def test_meta_params_defaults_invalid_name(self):
        s = DefaultService()
        with pytest.raises(TypeError, match="'name' must be"):
            s.with_defaults(123)

    def test_meta_params_defaults_invalid_count(self):
        s = DefaultService()
        with pytest.raises(TypeError, match="'count' must be"):
            s.with_defaults("ab", "three")

    def test_meta_params_optional_invalid(self):
        s = OptionalService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process(42)

    def test_meta_params_union_invalid(self):
        s = UnionService()
        with pytest.raises(TypeError, match="'value' must be"):
            s.process(3.14)
