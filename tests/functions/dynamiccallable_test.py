#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" dynamiccallable_test.py
Tests for the dynamiccallable.py module in the baseobjects package.
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
from typing import Any, Callable, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions.dynamiccallable import DynamicCallable, DynamicMethod, DynamicFunction
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class ConcreteDynamicCallable(DynamicCallable):
    """A concrete implementation of DynamicCallable for testing purposes."""

    def __init__(self, func: Callable | None = None, *args: Any, bind_method: str | None = None, call_method: str | None = None, **kwargs: Any) -> None:
        super().__init__(func=func, *args, bind_method=bind_method, call_method=call_method, **kwargs)

    def bind_builtin(self, instance: Any = None, owner: Type[Any] | None = None) -> Any:
        """Creates a method of this function which is bound to another object using the builtin method.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        from types import MethodType
        return MethodType(self, instance)

    def custom_bind(self, instance: Any = None, owner: Type[Any] | None = None) -> Any:
        """A custom bind method for testing."""
        # Just return a tuple of the arguments
        return (instance, owner)

    def custom_call(self, *args: Any, **kwargs: Any) -> Any:
        """A custom call method for testing."""
        # Add a prefix to the result
        result = self.__wrapped__(*args, **kwargs)
        if isinstance(result, str):
            return f"Custom: {result}"
        return result


class ConcreteDynamicMethod(DynamicMethod):
    """A concrete implementation of DynamicMethod for testing purposes."""

    def __init__(self, func: Callable | None = None, instance: Any = None, owner: Type[Any] | None = None, *args: Any, bind_method: str | None = None, call_method: str | None = None, **kwargs: Any) -> None:
        super().__init__(func=func, instance=instance, owner=owner, *args, bind_method=bind_method, call_method=call_method, **kwargs)

    def bind_builtin(self, instance: Any = None, owner: Type[Any] | None = None) -> Any:
        """Creates a method of this function which is bound to another object using the builtin method.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        from types import MethodType
        return MethodType(self, instance)

    def custom_call(self, *args: Any, **kwargs: Any) -> Any:
        """A custom call method for testing."""
        # Add a prefix to the result
        result = self.__wrapped__(*args, **kwargs)
        if isinstance(result, str):
            return f"Method: {result}"
        return result


class ConcreteDynamicFunction(DynamicFunction):
    """A concrete implementation of DynamicFunction for testing purposes."""

    def __init__(self, func: Callable | None = None, *args: Any, bind_method: str | None = None, call_method: str | None = None, **kwargs: Any) -> None:
        super().__init__(func=func, *args, bind_method=bind_method, call_method=call_method, **kwargs)

    def custom_call(self, *args: Any, **kwargs: Any) -> Any:
        """A custom call method for testing."""
        # Add a prefix to the result
        result = self.__wrapped__(*args, **kwargs)
        if isinstance(result, str):
            return f"Function: {result}"
        return result


class TestDynamicCallable(ClassTest):
    """Test the DynamicCallable class.

    This class tests the functionality of the DynamicCallable class, which is an abstract
    callable class that has multiplexed binding and callback.
    """

    # Class Attributes #
    class_: Type[DynamicCallable] = DynamicCallable

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_func(self) -> Callable:
        """Create a test function for use in tests.

        Returns:
            A simple test function that returns a string.
        """
        def func() -> str:
            return "test"
        return func

    @pytest.fixture
    def dynamic_callable(self, test_func: Callable) -> ConcreteDynamicCallable:
        """Create a ConcreteDynamicCallable instance for testing.

        Args:
            test_func: A fixture providing a test function.

        Returns:
            A ConcreteDynamicCallable instance wrapping the test function.
        """
        return ConcreteDynamicCallable(test_func)

    # Tests
    def test_init(self, test_func: Callable) -> None:
        """Test the initialization of DynamicCallable.

        This test verifies that DynamicCallable can be initialized with a function.

        Args:
            test_func: A fixture providing a test function.
        """
        # Create a dynamic callable with a function
        dynamic_callable = ConcreteDynamicCallable(test_func)

        # Verify the dynamic callable was created correctly
        assert dynamic_callable.__wrapped__ == test_func
        assert dynamic_callable.bind_method == "bind_builtin"
        assert dynamic_callable.call_method == "call_wrapped"

    def test_bind_method_property(self, dynamic_callable: ConcreteDynamicCallable) -> None:
        """Test the bind_method property.

        This test verifies that the bind_method property correctly gets and sets the bind method.

        Args:
            dynamic_callable: A fixture providing a ConcreteDynamicCallable instance.
        """
        # Verify the default bind method
        assert dynamic_callable.bind_method == "bind_builtin"

        # Set a custom bind method
        dynamic_callable.bind_method = "custom_bind"

        # Verify the bind method was set correctly
        assert dynamic_callable.bind_method == "custom_bind"
        assert dynamic_callable.default_bind_method == "custom_bind"

    def test_call_method_property(self, dynamic_callable: ConcreteDynamicCallable) -> None:
        """Test the call_method property.

        This test verifies that the call_method property correctly gets and sets the call method.

        Args:
            dynamic_callable: A fixture providing a ConcreteDynamicCallable instance.
        """
        # Verify the default call method
        assert dynamic_callable.call_method == "call_wrapped"

        # Set a custom call method
        dynamic_callable.call_method = "custom_call"

        # Verify the call method was set correctly
        assert dynamic_callable.call_method == "custom_call"
        assert dynamic_callable.default_call_method == "custom_call"

    def test_get(self, dynamic_callable: ConcreteDynamicCallable) -> None:
        """Test the __get__ method.

        This test verifies that the __get__ method correctly delegates to the bind multiplexer.

        Args:
            dynamic_callable: A fixture providing a ConcreteDynamicCallable instance.
        """
        # Set a custom bind method
        dynamic_callable.bind_method = "custom_bind"

        # Create a test instance and class
        class TestClass:
            pass

        test_instance = TestClass()

        # Call __get__ through descriptor protocol
        result = dynamic_callable.__get__(test_instance, TestClass)

        # Verify the result
        assert result == (test_instance, TestClass)

    def test_call(self, dynamic_callable: ConcreteDynamicCallable) -> None:
        """Test the __call__ method.

        This test verifies that the __call__ method correctly delegates to the call multiplexer.

        Args:
            dynamic_callable: A fixture providing a ConcreteDynamicCallable instance.
        """
        # Verify the default call behavior
        assert dynamic_callable() == "test"

        # Set a custom call method
        dynamic_callable.call_method = "custom_call"

        # Verify the custom call behavior
        assert dynamic_callable() == "Custom: test"

    def test_construct(self, test_func: Callable) -> None:
        """Test the construct method.

        This test verifies that the construct method correctly sets up the dynamic callable.

        Args:
            test_func: A fixture providing a test function.
        """
        # Create a dynamic callable without initialization
        dynamic_callable = ConcreteDynamicCallable(init=False)

        # Construct the dynamic callable
        dynamic_callable.construct(test_func, bind_method="custom_bind", call_method="custom_call")

        # Verify the dynamic callable was constructed correctly
        assert dynamic_callable.__wrapped__ == test_func
        assert dynamic_callable.bind_method == "custom_bind"
        assert dynamic_callable.call_method == "custom_call"

    def test_call_multiplexer(self, dynamic_callable: ConcreteDynamicCallable) -> None:
        """Test the call multiplexer.

        This test verifies that the call multiplexer correctly calls the wrapped function.

        Args:
            dynamic_callable: A fixture providing a ConcreteDynamicCallable instance.
        """
        # Call the call method
        result = dynamic_callable.call_multiplexer()

        # Verify the result
        assert result == "test"


class TestDynamicMethod(ClassTest):
    """Test the DynamicMethod class.

    This class tests the functionality of the DynamicMethod class, which is an abstract
    method class that has multiplexed binding and callback.
    """

    # Class Attributes #
    class_: Type[DynamicMethod] = DynamicMethod

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_func(self) -> Callable:
        """Create a test function for use in tests.

        Returns:
            A simple test function that returns a string.
        """
        def func(self) -> str:
            return "test"
        return func

    @pytest.fixture
    def dynamic_method(self, test_func: Callable) -> ConcreteDynamicMethod:
        """Create a ConcreteDynamicMethod instance for testing.

        Args:
            test_func: A fixture providing a test function.

        Returns:
            A ConcreteDynamicMethod instance wrapping the test function.
        """
        return ConcreteDynamicMethod(test_func)

    # Tests
    def test_init(self, test_func: Callable) -> None:
        """Test the initialization of DynamicMethod.

        This test verifies that DynamicMethod can be initialized with a function.

        Args:
            test_func: A fixture providing a test function.
        """
        # Create a dynamic method with a function
        dynamic_method = ConcreteDynamicMethod(test_func)

        # Verify the dynamic method was created correctly
        assert dynamic_method.__wrapped__ == test_func
        assert dynamic_method.call_method == "call_binding"


class TestDynamicFunction(ClassTest):
    """Test the DynamicFunction class.

    This class tests the functionality of the DynamicFunction class, which is an abstract
    function class that has multiplexed bind and callback.
    """

    # Class Attributes #
    class_: Type[DynamicFunction] = DynamicFunction

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_func(self) -> Callable:
        """Create a test function for use in tests.

        Returns:
            A simple test function that returns a string.
        """
        def func() -> str:
            return "test"
        return func

    @pytest.fixture
    def dynamic_function(self, test_func: Callable) -> ConcreteDynamicFunction:
        """Create a ConcreteDynamicFunction instance for testing.

        Args:
            test_func: A fixture providing a test function.

        Returns:
            A ConcreteDynamicFunction instance wrapping the test function.
        """
        return ConcreteDynamicFunction(test_func)

    # Tests
    def test_init(self, test_func: Callable) -> None:
        """Test the initialization of DynamicFunction.

        This test verifies that DynamicFunction can be initialized with a function.

        Args:
            test_func: A fixture providing a test function.
        """
        # Create a dynamic function with a function
        dynamic_function = ConcreteDynamicFunction(test_func)

        # Verify the dynamic function was created correctly
        assert dynamic_function.__wrapped__ == test_func
        assert dynamic_function.method_type == DynamicMethod


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
