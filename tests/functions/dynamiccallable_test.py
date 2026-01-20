"""dynamiccallable_test.py
Tests for the DynamicCallable class in the baseobjects package.

This module provides tests for the DynamicCallable class, which is an abstract callable class that has multiplexed
binding and callback functionality. It tests the core functionality of DynamicCallable, including instance creation,
function calling, binding, and multiplexed callback.
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
import pickle
from typing import Any, ClassVar, cast
from unittest.mock import patch

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.functions import DynamicCallable, DynamicFunction, DynamicMethod
from baseobjects.testsuite.functions import (
    DynamicCallableTestSuite,
    DynamicFunctionTestSuite,
    DynamicMethodTestSuite,
)


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers.

    Returns:
        The sum of x and y.
    """
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers.

    Returns:
        The product of x and y.
    """
    return x * y


# Helper Classes #
class DynamicCallableTestObject:
    """A test class for testing method binding and selection."""

    def __init__(self, value: int = 10) -> None:
        """Initialize with a value."""
        self.value = value

    def method1(self, x: int) -> int:
        """A test method that adds x to the value.

        Returns:
            The sum of value and x.
        """
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x.

        Returns:
            The product of value and x.
        """
        return self.value * x


# Tests #
class TestDynamicCallable(DynamicCallableTestSuite):
    """Test the DynamicCallable class.

    This class tests the functionality of the DynamicCallable class, which is an abstract callable class that has
    multiplexed binding and callback functionality.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[DynamicCallable]] = DynamicCallable

    # Instance Methods #
    def create_test_method_object(self) -> DynamicCallable:
        """Create a test method object for testing.

        Returns:
            DynamicCallable: An instance of DynamicCallable that wraps a method.
        """
        return cast(DynamicCallable, self.create_method_object())

    # Fixtures
    @pytest.fixture
    def test_object_instance(self) -> DynamicCallableTestObject:
        """Create a test object instance.

        Returns:
            DynamicCallableTestObject: An instance of the test object.
        """
        return DynamicCallableTestObject(value=10)

    @pytest.fixture
    def test_function_object(self) -> DynamicCallable:
        """Create a test callable object that wraps a function.

        Returns:
            DynamicCallable: An instance of DynamicCallable that wraps a function.
        """
        return cast(DynamicCallable, self.create_function_object(add_function))

    @pytest.fixture
    def test_method_object(self) -> DynamicCallable:
        """Create a test callable object that wraps a method.

        Returns:
            DynamicCallable: An instance of DynamicCallable that wraps a method.
        """
        return cast(DynamicCallable, self.create_method_object())


class TestDynamicFunction(DynamicFunctionTestSuite):
    """Test the DynamicFunction class.

    This class tests the functionality of the DynamicFunction class.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[DynamicFunction]] = DynamicFunction


class TestDynamicMethod(DynamicMethodTestSuite):
    """Test the DynamicMethod class.

    This class tests the functionality of the DynamicMethod class.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[DynamicMethod]] = DynamicMethod

    def test_call_without_self(self) -> None:
        """Test calling when _self_ attribute causes AttributeError."""
        class MockDynamicMethod(DynamicMethod):
            @property
            def _self_(self) -> Any:
                raise AttributeError("Mocked AttributeError")

            @_self_.setter
            def _self_(self, value: Any) -> None:
                pass

        def func() -> int:
            return 1

        obj = MockDynamicMethod(func)
        assert obj() == 1


# Classes #
class SlotDynamicCallable(DynamicCallable):
    """A DynamicCallable subclass with slots for testing."""

    __slots__ = ("extra",)

    def __init__(self, func: Any, **kwargs: Any) -> None:
        """Initializes the SlotDynamicCallable."""
        self.extra = 1
        super().__init__(func, **kwargs)


class TestDynamicCallableCoverage:
    """Tests coverage for DynamicCallable."""

    def test_call_wrapped(self) -> None:
        """Tests calling the wrapped function directly."""
        dc = DynamicCallable(lambda x: x + 1)
        assert dc.call_wrapped(1) == 2

    def test_as_function(self) -> None:
        """Tests as_function method."""
        dc = DynamicCallable(lambda x: x + 1)
        func = dc.as_function()
        assert func(1) == 2
        assert func.__name__ == "<lambda>"

    def _setup_slots(self) -> SlotDynamicCallable:
        return SlotDynamicCallable(len)

    def _setup_dict(self) -> DynamicCallable:
        dc = DynamicCallable(len)
        dc.foo = "bar"  # type: ignore[attr-defined]
        return dc

    @pytest.mark.parametrize(
        ("setup_method", "verify_attr", "expected_val"),
        [
            ("_setup_slots", "extra", 1),
            ("_setup_dict", "foo", "bar"),
        ],
    )
    def test_pickling_variants(self, setup_method: str, verify_attr: str, expected_val: Any) -> None:
        """Tests pickling with various object structures."""
        dc = getattr(self, setup_method)()
        dump = pickle.dumps(dc)
        loaded = pickle.loads(dump)
        assert loaded([1]) == 1
        assert getattr(loaded, verify_attr) == expected_val

    @pytest.mark.parametrize(
        ("state", "verifier"),
        [
            ((None, {"extra": 2}), lambda dc: dc.extra == 2),
            (None, lambda dc: dc.bind_multiplexer.selected == dc.default_bind_method),
        ],
    )
    def test_setstate_variants(self, state: Any, verifier: Any) -> None:
        """Tests setstate with different state types."""
        dc = SlotDynamicCallable(len)
        dc.__setstate__(state)
        assert verifier(dc)

    def test_getstate_none_return(self) -> None:
        """Tests getstate when super class returns None."""
        dc = DynamicCallable(len)
        with patch.object(DynamicCallable.__base__, "__getstate__", return_value=None):
            state = dc.__getstate__()
            assert state is None or state == {}

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        dc = DynamicCallable(init=False)
        assert dc.__wrapped__ is None

    def test_setstate_unknown(self) -> None:
        """Tests setstate with unknown state type."""
        dc = DynamicCallable(len)
        # baseobjects.bases.basereducible.BaseReducible raises TypeError for invalid state
        with pytest.raises(TypeError):
            dc.__setstate__("invalid_state")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
