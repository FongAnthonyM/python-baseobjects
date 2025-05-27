#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basemethod_test.py
Tests for the BaseMethod class in the baseobjects package.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"

from types import MethodType
# Imports #
# Standard Libraries #
from typing import Any, Optional, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseObject, BaseMethod
from .base_test import BaseBaseObjectTest


# Classes #
class TestBaseMethod(BaseBaseObjectTest):
    """Test the BaseMethod class.

    This class tests the functionality of the BaseMethod class, which is a base class for method objects in the 
    baseobjects package.
    """
    # Attributes #
    class_: Type[BaseMethod] = BaseMethod

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def generate_method(self, request: Optional[Any] = None) -> BaseMethod:
        """Create a BaseMethod instance with a generic function.

        The generic function returns the first argument passed to it, which will be the instance the method is bound to.

        Args:
            request: A pytest request object that may contain parameters. If provided, the get_method parameter is 
                passed to BaseMethod.

        Returns:
            BaseMethod: An instance of BaseMethod wrapping the generic function and bound to self.
        """
        def generic(*args: Any, **kwargs: Any) -> Any:
            return args[0]

        if request is None:
            return self.class_(func=generic, instance=self)
        else:
            return self.class_(func=generic, instance=self, get_method=request.param)

    # Tests
    def test_method_call(self, generate_method: BaseMethod) -> None:
        """Test that a BaseMethod instance can be called like a normal method.

        When called, the method should pass the bound instance (self) as the first argument to the wrapped function.

        Args:
            generate_method: A fixture providing a BaseMethod instance.
        """
        assert self == generate_method()

    def test_binding(self, generate_method: BaseMethod) -> None:
        """Test the bind_self method of BaseMethod.

        This test verifies that a BaseMethod can be rebound to a different object instance, changing which instance is 
        passed as the first argument when called.

        Args:
            generate_method: A fixture providing a BaseMethod instance.
        """
        obj = BaseObject()
        bound_method = generate_method.bind_self(instance=obj)
        assert bound_method is generate_method
        assert obj == generate_method()

    def test_bind_wrapped(self, generate_method: BaseMethod) -> None:
        """Test the bind_wrapped method of BaseMethod.

        This test verifies that a BaseMethod can be rebound to a different object instance, changing which instance is
        passed as the first argument when called.

        Args:
            generate_method: A fixture providing a BaseMethod instance.
        """
        obj = BaseObject()
        bound_method = generate_method.bind_wrapped(instance=obj)
        assert isinstance(bound_method, MethodType)
        assert obj == bound_method()

    def test_binding_to_attribute(self, generate_method: BaseMethod) -> None:
        """Test the bind_to_attribute method of BaseMethod.

        This test verifies that a BaseMethod can be bound to an attribute of an object, making it accessible as an 
        attribute while maintaining its binding to the original instance.

        Args:
            generate_method: A fixture providing a BaseMethod instance.
        """
        obj = BaseObject()
        generate_method.bind_to_attribute(instance=obj)
        assert hasattr(obj, "generic")
        assert obj.generic == generate_method

    def test_binding_to_attribute_with_name(self, generate_method: BaseMethod) -> None:
        """Test the bind_to_attribute method of BaseMethod with a custom name.

        This test verifies that a BaseMethod can be bound to an attribute with a custom name.

        Args:
            generate_method: A fixture providing a BaseMethod instance.
        """
        obj = BaseObject()
        generate_method.bind_to_attribute(instance=obj, name="custom_name")
        assert hasattr(obj, "custom_name")
        assert obj.custom_name == generate_method

    def test_descriptor_behavior(self) -> None:
        """Test the descriptor behavior of BaseMethod.

        This test verifies that a BaseMethod can be accessed as a descriptor.
        """
        # Create a simple test class
        class TestClass:
            def test_method(self, *args: Any, **kwargs: Any) -> Any:
                return self

        # Create an instance
        instance = TestClass()

        # Create a BaseMethod from the instance method
        method = BaseMethod(func=instance.test_method.__func__, instance=instance)

        # Verify the method returns the instance
        assert method() is instance

    def test_state_methods(self) -> None:
        """Test the __getstate__ and __setstate__ methods of BaseMethod.

        This test verifies that the state can be extracted and restored.
        """
        # Create a method that returns a fixed value
        def test_method(instance: Any) -> str:
            return "test_value"

        # Create a BaseMethod
        method = BaseMethod(func=test_method, instance=self)

        # Get the state
        state = method.__getstate__()

        # Create a new method and set its state
        new_method = BaseMethod()
        new_method.__setstate__(state)

        # Verify the new method has the same behavior
        assert new_method() == "test_value"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])