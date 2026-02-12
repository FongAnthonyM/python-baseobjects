"""basecallable_test.py
Tests for the BaseCallable class in the baseobjects package.

This module provides tests for the BaseCallable class, which is an abstract base class that implements the core
functionality for creating callable objects in Python. It wraps an existing function or callable and implements the
necessary protocols to make the wrapper behave like the wrapped function.
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
from types import MethodType
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import BaseCallable
from baseobjects.testsuite.bases import BaseCallableTestSuite


# Classes #
class SlotCallable(BaseCallable):
    """A subclass with slots for testing."""

    __slots__ = ("_extra",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes the SlotCallable."""
        super().__init__(*args, **kwargs)
        self._extra = 1


class TestBaseCallable(BaseCallableTestSuite):
    """Tests the BaseCallable class.

    This class tests the functionality of the BaseCallable class, which is the base class for all callable
    objects in the baseobjects package.
    """

    # Attributes #
    UnitTestClass: type[BaseCallable] = BaseCallable

    # Instance Methods #
    # Tests

    def test_with_custom_function(self) -> None:
        """Tests BaseCallable with a custom function."""

        # Create a custom function with attributes
        def custom_func(a: int, b: int) -> int:
            """Custom function docstring.

            Returns:
                int: The product of a and b.
            """
            return a * b

        custom_func.custom_attr = "custom value"  # type: ignore[attr-defined]

        # Create a callable object with the custom function
        callable_obj = self.UnitTestClass(custom_func)

        # Verify it has the correct wrapped function
        assert callable_obj.__func__ is custom_func

        # Verify it has the correct attributes
        assert callable_obj.__name__ == "custom_func"  # type: ignore[attr-defined]
        assert callable_obj.__doc__ == """Custom function docstring.\n\nReturns:\n    int: The product of a and b.\n"""
        assert callable_obj.custom_attr == "custom value"  # type: ignore[attr-defined]

        # Verify it returns the expected result when called
        assert callable_obj(3, 4) == 12  # 3 * 4

    def test_pickling_slots(self) -> None:
        """Tests pickling of a subclass with slots."""
        # Must use a picklable function. Builtin functions like len are picklable.
        obj = SlotCallable(len)

        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert loaded([1]) == 1
        assert loaded._extra == 1

    def test_descriptor_protocol(self, test_method_object: BaseCallable) -> None:
        """Tests that the callable implements the descriptor protocol for method binding.

        This test only varifies that the descriptor returns a bound method. This method may be overwritten to include
        validation that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        if not hasattr(test_method_object, "__get__"):
            pytest.skip("Test object does not implement descriptor protocol")

        class BindTarget:
            new_method: Any = test_method_object

        instance = BindTarget()
        assert isinstance(instance.new_method, MethodType)
        assert instance.new_method.__self__ is instance

    def test_attribute_copying(self) -> None:
        """Tests that attributes from the wrapped function are correctly copied to the callable object."""

        # Create a temporary function
        def temp_func(x: int, y: int = 2) -> int:
            return x + y

        # Create an attribute in the function
        temp_func.new_attribute = "test"  # type: ignore[attr-defined]

        # Create a callable object
        test_object = self.UnitTestClass(temp_func)

        # Validate the new attribute is present and the same
        assert test_object.new_attribute == temp_func.new_attribute  # type: ignore[attr-defined]

    def test_as_function_missing_attrs(self) -> None:
        """Tests as_function with a callable missing standard attributes."""

        class IncompleteCallable:
            def __call__(self, x: Any) -> Any:
                return x

        func = IncompleteCallable()
        obj = self.UnitTestClass(func)
        wrapped_func = obj.as_function()
        assert wrapped_func(1) == 1
        assert wrapped_func.__name__ == "wrapper_function"

    def test_as_function_cast_excluded(self) -> None:
        """Tests that excluded attributes are not copied by as_function."""
        obj = self.UnitTestClass(lambda: None)
        # Mock __call__ in __dict__
        obj.__dict__["__call__"] = lambda: "fail"
        wrapper = obj.as_function()
        assert "__call__" not in wrapper.__dict__

    def test_func_setter_attributes_cleanup(self) -> None:
        """Tests that attributes are cleaned up when __func__ is set to None."""

        def func() -> None:
            """Docstring."""

        obj = self.UnitTestClass(func)
        assert obj.__doc__ == "Docstring."
        assert obj.__name__ == "func"  # type: ignore[attr-defined]

        obj.__func__ = None

        # Should revert to class docstring or raise AttributeError if not on class
        assert obj.__doc__ == self.UnitTestClass.__doc__
        # __name__ is not on BaseCallable class, so it might raise AttributeError or be missing
        assert not hasattr(obj, "__name__")

    def test_attribute_copying_exclusion(self) -> None:
        """Tests that attributes existing in dir(self) are not overwritten."""

        def func() -> None:
            pass

        func.construct = "overwrite"  # type: ignore[attr-defined]

        obj = self.UnitTestClass(func)

        assert callable(obj.construct)
        assert obj.construct != "overwrite"  # type: ignore[comparison-overlap]

    def test_exclude_attributes(self) -> None:
        """Tests that attributes in _exclude_attributes are not copied."""

        class ExcludeDoc(BaseCallable):
            _exclude_attributes: set[str] = {"__doc__"}

        def func() -> None:
            """Func Docstring."""

        obj = ExcludeDoc(func)
        assert obj.__doc__ == ExcludeDoc.__doc__
        assert obj.__doc__ != "Func Docstring."


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
