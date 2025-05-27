#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basecallable_test.py
Tests for the BaseCallable class in the baseobjects package.
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
from asyncio.coroutines import iscoroutinefunction
from types import FunctionType
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseCallable
from .base_test import BaseBaseObjectTest


# Classes #
class TestBaseCallable(BaseBaseObjectTest):
    """Test the BaseCallable class.

    This class tests the functionality of the BaseCallable class, which is a base class for callable objects
    in the baseobjects package.
    """
    # Attributes #
    class_: Type[BaseCallable] = BaseCallable

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_function(self) -> callable:
        """Create a simple test function that returns its arguments.

        Returns:
            function: A function that returns a tuple of its args and kwargs.
        """
        def test_func(*args: Any, **kwargs: Any) -> tuple[tuple[Any, ...], dict[str, Any]]:
            return args, kwargs

        return test_func

    @pytest.fixture
    def test_callable(self, test_function: callable) -> BaseCallable:
        """Create a BaseCallable instance wrapping the test function.

        Args:
            test_function: A fixture providing a test function.

        Returns:
            BaseCallable: An instance of BaseCallable wrapping the test function.
        """
        return self.class_(func=test_function)

    # Tests
    def test_instance_creation(self, test_callable: BaseCallable) -> None:
        """Test that instances of BaseCallable can be created.

        Args:
            test_callable: A fixture providing a BaseCallable instance.
        """
        assert test_callable is not None
        assert test_callable.__wrapped__ is not None

    def test_call(self, test_callable: BaseCallable) -> None:
        """Test that a BaseCallable instance can be called like a normal function.

        Args:
            test_callable: A fixture providing a BaseCallable instance.
        """
        args, kwargs = test_callable(1, 2, a=3, b=4)
        assert args == (1, 2)
        assert kwargs == {"a": 3, "b": 4}

    def test_func_property(self, test_callable: BaseCallable, test_function: callable) -> None:
        """Test the __func__ property of BaseCallable.

        This test verifies that the __func__ property returns the wrapped function.

        Args:
            test_callable: A fixture providing a BaseCallable instance.
            test_function: A fixture providing the test function.
        """
        assert test_callable.__func__ is test_function

    def test_name_property(self, test_callable: BaseCallable, test_function: callable) -> None:
        """Test the __name__ property of BaseCallable.

        This test verifies that the __name__ property returns the name of the wrapped function.

        Args:
            test_callable: A fixture providing a BaseCallable instance.
            test_function: A fixture providing the test function.
        """
        assert test_callable.__name__ == test_function.__name__

    def test_as_function(self, test_callable: BaseCallable) -> None:
        """Test the as_function method of BaseCallable.

        This test verifies that as_function creates a function that behaves like the original.

        Args:
            test_callable: A fixture providing a BaseCallable instance.
        """
        func = test_callable.as_function()
        assert callable(func)
        assert isinstance(func, FunctionType)

        # Test that the function works like the original
        args, kwargs = func(1, 2, a=3, b=4)
        assert args == (1, 2)
        assert kwargs == {"a": 3, "b": 4}

    def test_coroutine_handling(self) -> None:
        """Test that BaseCallable correctly identifies and handles coroutine functions."""
        # Create an async function
        async def async_func(*args: Any, **kwargs: Any) -> tuple[tuple[Any, ...], dict[str, Any]]:
            return args, kwargs

        # Create a BaseCallable with the async function
        callable_obj = self.class_(func=async_func)

        # Test that it's identified as a coroutine
        assert callable_obj.is_coroutine

        # Test that as_function creates an async function
        func = callable_obj.as_function()
        assert iscoroutinefunction(func)

    def test_func_setter(self, test_callable: BaseCallable, test_function: callable) -> None:
        """Test setting the __func__ property of BaseCallable.

        This test verifies that the __func__ property setter correctly updates the wrapped function.

        Args:
            test_callable: A fixture providing a BaseCallable instance.
            test_function: A fixture providing the test function.
        """
        # Create a new function
        def new_func(*args: Any, **kwargs: Any) -> str:
            return "new function"

        # Set the __func__ property
        test_callable.__func__ = new_func

        # Verify the function was updated
        assert test_callable.__wrapped__ is new_func
        assert test_callable() == "new function"

    def test_func_setter_invalid(self, test_callable: BaseCallable) -> None:
        """Test setting the __func__ property with an invalid value.

        This test verifies that the __func__ property setter raises TypeError for non-callable values.

        Args:
            test_callable: A fixture providing a BaseCallable instance.
        """
        # Try to set a non-callable value
        with pytest.raises(TypeError):
            test_callable.__func__ = "not callable"

    def test_construct_with_func(self) -> None:
        """Test constructing a BaseCallable with a function.

        This test verifies that the construct method correctly sets the wrapped function.
        """
        # Create a function
        def test_func(*args: Any, **kwargs: Any) -> str:
            return "constructed"

        # Create a BaseCallable without a function
        callable_obj = self.class_()

        # Construct with the function
        callable_obj.construct(func=test_func)

        # Verify the function was set
        assert callable_obj.__wrapped__ is test_func
        assert callable_obj() == "constructed"

    def test_custom_attributes(self) -> None:
        """Test that custom attributes from the wrapped function are copied to the BaseCallable.

        This test verifies that custom attributes from the wrapped function are
        copied to the BaseCallable instance.
        """
        # Create a function with custom attributes
        def test_func(*args: Any, **kwargs: Any) -> None:
            pass

        test_func.custom_attr = "custom value"

        # Create a BaseCallable with the function
        callable_obj = self.class_(func=test_func)

        # Verify custom attributes were copied
        assert hasattr(callable_obj, "custom_attr")
        assert callable_obj.custom_attr == "custom value"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])