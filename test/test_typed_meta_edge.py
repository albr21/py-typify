import pytest
from conftest import (
    SimpleService, NoHintsService, NonCallableAttrService
)
from typify.typed_meta import TypedMeta

class TestTypedMetaPrivateSkipped:
    def test_meta_private_not_typechecked(self):
        s = SimpleService()
        assert s._private("not_an_int") == "not_an_int"

    def test_meta_private_with_valid_type(self):
        s = SimpleService()
        assert s._private(42) == 42

class TestTypedMetaNoHints:
    def test_meta_no_hints_int(self):
        s = NoHintsService()
        assert s.process(42) == 42

    def test_meta_no_hints_str(self):
        s = NoHintsService()
        assert s.process("anything") == "anything"

    def test_meta_no_hints_none(self):
        s = NoHintsService()
        assert s.process(None) is None

class TestTypedMetaNonCallableAttr:
    def test_meta_non_callable_preserved(self):
        assert NonCallableAttrService.label == "static_value"

    def test_meta_callable_still_checked(self):
        s = NonCallableAttrService()
        assert s.process(5) == 5

    def test_meta_callable_invalid(self):
        s = NonCallableAttrService()
        with pytest.raises(TypeError, match="'x' must be"):
            s.process("five")

class TestTypedMetaTypecheckStandalone:
    def test_typecheck_valid(self):
        @TypedMeta._typecheck
        def double(x: int) -> int:
            return x * 2

        assert double(5) == 10

    def test_typecheck_invalid_param(self):
        @TypedMeta._typecheck
        def double(x: int) -> int:
            return x * 2

        with pytest.raises(TypeError, match="'x' must be"):
            double("five")

    def test_typecheck_invalid_return(self):
        @TypedMeta._typecheck
        def bad(x: int) -> str:
            return x  # type: ignore

        with pytest.raises(TypeError, match="return must be"):
            bad(42)

    def test_typecheck_with_kwargs(self):
        @TypedMeta._typecheck
        def greet(name: str, excited: bool = False) -> str:
            return f"Hello, {name}{'!' if excited else '.'}"

        assert greet("Alice") == "Hello, Alice."
        assert greet("Alice", excited=True) == "Hello, Alice!"
        assert greet(name="Bob") == "Hello, Bob."

    def test_typecheck_kwargs_invalid(self):
        @TypedMeta._typecheck
        def greet(name: str, excited: bool = False) -> str:
            return f"Hello, {name}{'!' if excited else '.'}"

        with pytest.raises(TypeError, match="'excited' must be"):
            greet("Alice", excited="yes")
