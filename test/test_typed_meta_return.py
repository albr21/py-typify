import pytest
from conftest import (
    SimpleService, BadReturnSimpleService, BadReturnGenericService,
    NoReturnHintService
)

class TestTypedMetaReturnValid:
    def test_meta_return_str(self):
        s = SimpleService()
        result = s.greet("World")
        assert result == "Hello, World"
        assert isinstance(result, str)

    def test_meta_return_int(self):
        s = SimpleService()
        result = s.add(2, 3)
        assert result == 5
        assert isinstance(result, int)

    def test_meta_return_no_hint_skips_check(self):
        s = NoReturnHintService()
        assert s.process(5) == 10

class TestTypedMetaReturnInvalid:
    def test_meta_return_wrong_simple(self):
        s = BadReturnSimpleService()
        with pytest.raises(TypeError, match="return must be"):
            s.process("hello")

    def test_meta_return_wrong_generic(self):
        s = BadReturnGenericService()
        with pytest.raises(TypeError, match="return must be"):
            s.process([1, 2, 3])
