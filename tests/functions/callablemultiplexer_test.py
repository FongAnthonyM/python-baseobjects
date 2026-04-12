"""callablemultiplexer_test.py
Tests for the CallableMultiplexer class in the baseobjects package.

This module provides tests for the CallableMultiplexer class, which is a callable that selects between different
functions or methods to be used as the call method. It has a registry to store functions/methods and can also use
methods from a wrapped object.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
# from typing import

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.functions import CallableMultiplexer, FunctionMultiplexer, MethodMultiplexer
from baseobjects.testsuite.functions import (
    CallableMultiplexerTestSuite,
    FunctionMultiplexerTestSuite,
    MethodMultiplexerTestSuite,
)


# Tests #
class TestCallableMultiplexer(CallableMultiplexerTestSuite):
    """Test the CallableMultiplexer class.

    This class tests the functionality of the CallableMultiplexer class, which is a callable that selects between
    different functions or methods to be used as the call method.
    """

    # Attributes #
    UnitTestClass: type[CallableMultiplexer] = CallableMultiplexer

    def test_construct_with_registry_as_func(self) -> None:
        """Test constructing with a FunctionRegistry as the first argument."""
        # Source Packages #
        from baseobjects.functions import FunctionRegistry
        registry = FunctionRegistry()
        obj = self.UnitTestClass(registry)
        assert obj.registry is registry
        assert obj.__func__ is None

    def test_construct_with_func_and_registry(self) -> None:
        """Test constructing with both func as registry and explicit registry."""
        # Source Packages #
        from baseobjects.functions import FunctionRegistry
        registry1 = FunctionRegistry()
        registry2 = FunctionRegistry()
        obj = self.UnitTestClass(func=registry1, registry=registry2)
        assert obj.registry is registry2
        assert obj.__func__ is None

    def test_add_select_function_no_get(self) -> None:
        """Test adding a function that doesn't have __get__."""
        class MockFunc:
            def __call__(self, *args, **kwargs):
                return True

        mock_func = MockFunc()
        obj = self.UnitTestClass()
        obj.add_select_function("mock", mock_func)
        assert obj._selected == "mock"
        assert getattr(obj, "_selected_bind_method", None) is None

    def test_add_select_method_no_func_no_get(self) -> None:
        """Test adding a method that has neither __func__ nor __get__."""
        class MockMethod:
            def __call__(self, *args, **kwargs):
                return True

        mock_method = MockMethod()
        obj = self.UnitTestClass()
        obj.add_select_method("mock", mock_method)
        assert obj._selected == "mock"
        assert obj.registry["mock"] is mock_method


class TestFunctionMultiplexer(FunctionMultiplexerTestSuite):
    """Test the FunctionMultiplexer class.

    This class tests the functionality of the FunctionMultiplexer class.
    """

    # Attributes #
    UnitTestClass: type[FunctionMultiplexer] = FunctionMultiplexer


class TestMethodMultiplexer(MethodMultiplexerTestSuite):
    """Test the MethodMultiplexer class.

    This class tests the functionality of the MethodMultiplexer class.
    """

    # Attributes #
    UnitTestClass: type[MethodMultiplexer] = MethodMultiplexer

    def test_call_wrapped_present(self) -> None:
        """Test calling when the selected function has call_wrapped."""
        class MockWrapped:
            def call_wrapped(self, instance, *args, **kwargs):
                return "wrapped_called"

        class MockInstance:
            pass

        obj = self.UnitTestClass()
        obj.add_select_function("wrapped", MockWrapped())
        obj.__self__ = MockInstance()

        assert obj() == "wrapped_called"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
