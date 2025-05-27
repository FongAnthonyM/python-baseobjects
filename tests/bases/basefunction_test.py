#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basefunction_test.py
Tests for the BaseFunction class in the baseobjects package.
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
from types import MethodType
from typing import Any, Optional, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseObject, BaseFunction, BaseMethod
from .base_test import BaseBaseObjectTest


# Classes #
class TestBaseFunction(BaseBaseObjectTest):
    """Test the BaseFunction class.

    This class tests the functionality of the BaseFunction class, which is a base class for function objects in the
    baseobjects package.
    """
    # Attributes #
    class_: Type[BaseFunction] = BaseFunction

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def generic_function(self) -> callable:
        """Create a simple generic function that always returns True.

        Returns:
            function: A function that returns True regardless of arguments.
        """
        def generic(*args: Any, **kwargs: Any) -> bool:
            return True

        return generic

    @pytest.fixture
    def generate_function(self, request: Optional[Any] = None) -> BaseFunction:
        """Create a BaseFunction instance with a generic function.

        The generic function returns the first argument passed to it.

        Args:
            request: A pytest request object that may contain parameters. If provided, the get_function parameter is
                passed to BaseFunction.

        Returns:
            BaseFunction: An instance of BaseFunction wrapping the generic function.
        """
        def generic(*args: Any, **kwargs: Any) -> Any:
            return args[0]

        return self.class_(func=generic) if generic else self.class_(func=generic, get_function=request.param)

    # Tests
    def test_function_call(self, generate_function: BaseFunction) -> None:
        """Test that a BaseFunction instance can be called like a normal function.

        Args:
            generate_function: A fixture providing a BaseFunction instance.
        """
        assert generate_function(5) == 5

    def test_binding(self, generate_function: BaseFunction) -> None:
        """Test the bind method of BaseFunction.

        This test verifies that a BaseFunction can be bound to an object instance, creating a method that passes the
        instance as the first argument.

        Args:
            generate_function: A fixture providing a BaseFunction instance.
        """
        obj = BaseObject()
        method = generate_function.bind(instance=obj)
        assert isinstance(method, BaseMethod)
        assert method() == obj

    def test_binding_to_attribute(self, generate_function: BaseFunction) -> None:
        """Test the bind_to_attribute method of BaseFunction.

        This test verifies that a BaseFunction can be bound to an attribute of an object, creating a BaseMethod instance
        accessible as an attribute.

        Args:
            generate_function: A fixture providing a BaseFunction instance.
        """
        obj = BaseObject()
        generate_function.bind_to_attribute(instance=obj)
        assert isinstance(obj.generic, BaseMethod)

    def test_binding_to_attribute_with_name(self, generate_function: BaseFunction) -> None:
        """Test the bind_to_attribute method of BaseFunction with a custom name.

        This test verifies that a BaseFunction can be bound to an attribute with a custom name.

        Args:
            generate_function: A fixture providing a BaseFunction instance.
        """
        obj = BaseObject()
        generate_function.bind_to_attribute(instance=obj, name="custom_name")
        assert hasattr(obj, "custom_name")
        assert isinstance(obj.custom_name, BaseMethod)

    def test_bind_builtin(self, generate_function: BaseFunction) -> None:
        """Test the bind_builtin method of BaseFunction.

        This test verifies that a BaseFunction can be bound to an object using the builtin method type.

        Args:
            generate_function: A fixture providing a BaseFunction instance.
        """
        obj = BaseObject()
        method = generate_function.bind_builtin(instance=obj)
        assert isinstance(method, MethodType)
        assert method() == obj

    def test_get_descriptor(self, generate_function: BaseFunction) -> None:
        """Test the __get__ descriptor method of BaseFunction.

        This test verifies that a BaseFunction can be used as a descriptor to create bound methods.

        Args:
            generate_function: A fixture providing a BaseFunction instance.
        """
        # Create a class with the function as a class attribute
        class TestClass:
            method = generate_function

        # Create an instance
        instance = TestClass()

        # Access the method (should trigger __get__)
        method = instance.method

        # Verify it's a bound method
        assert isinstance(method, MethodType)
        assert method() == instance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])