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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseCallable
from src.baseobjects.testsuite.bases import BaseCallableTestSuite, example_function


# Classes #
class TestBaseCallable(BaseCallableTestSuite):
    """Test the BaseCallable class.

    This class tests the functionality of the BaseCallable class, which is the base class for all callable
    objects in the baseobjects package.
    """

    # Attributes #
    TestClass: Type[BaseCallable] = BaseCallable

    # Instance Methods #
    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a test function
        instance = self.TestClass(example_function)
        
        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)
        
        # Verify it has the correct wrapped function
        assert instance.__func__ is example_function

    def test_call(self, test_function_object: BaseCallable) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Call the callable object
        result = test_function_object(3)
        
        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        
        # Call with different arguments
        result = test_function_object(3, 4)
        
        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_as_function(self, test_function_object: BaseCallable) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()
        
        # Verify it's a function
        assert callable(func)
        
        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4
        
        # Verify it has the correct attributes
        assert func.__name__ == test_function_object.__name__
        assert func.__doc__ == test_function_object.__doc__
        assert func.__wrapped__ is test_function_object

    def test_call_wrapped(self, test_function_object: BaseCallable) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)
        
        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        
        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)
        
        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_with_custom_function(self) -> None:
        """Test BaseCallable with a custom function."""
        # Create a custom function with attributes
        def custom_func(a: int, b: int) -> int:
            """Custom function docstring."""
            return a * b
        
        custom_func.custom_attr = "custom value"
        
        # Create a callable object with the custom function
        callable_obj = self.TestClass(custom_func)
        
        # Verify it has the correct wrapped function
        assert callable_obj.__func__ is custom_func
        
        # Verify it has the correct attributes
        assert callable_obj.__name__ == "custom_func"
        assert callable_obj.__doc__ == "Custom function docstring."
        assert callable_obj.custom_attr == "custom value"
        
        # Verify it returns the expected result when called
        assert callable_obj(3, 4) == 12  # 3 * 4


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])