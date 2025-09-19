"""basedecorator_test.py
Tests for the BaseDecorator class in the baseobjects package.

This module provides tests for the BaseDecorator class, which extends BaseFunction to create decorator-like callable 
objects. It provides utilities for creating decorators with and without arguments, and for applying decorators to 
functions and methods.
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
import asyncio
import copy
import pickle
from functools import partial
from typing import Any, Callable, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions import BaseDecorator
from src.baseobjects.testsuite.functions import BaseDecoratorTestSuite
from src.baseobjects.testsuite.bases import example_function, example_coroutine


# Definitions #
# Classes #
class ConcreteDecorator(BaseDecorator):
    """A concrete implementation of BaseDecorator for testing purposes."""

    def __init__(self, func: Callable | None = None, prefix: str = "Decorated: ", *args: Any,
                 **kwargs: Any) -> None:
        """Initialize the decorator with a prefix.

        Args:
            func: The function to decorate.
            prefix: The prefix to add to string results.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.prefix = prefix
        super().__init__(func=func, *args, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Add a prefix to the result of the wrapped function.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of the wrapped function, with a prefix added if it's a string.
        """
        result = self.__wrapped__(*args, **kwargs)
        if isinstance(result, str):
            return f"{self.prefix}{result}"
        return result


# Tests #
class TestBaseDecorator(BaseDecoratorTestSuite):
    """Test the BaseDecorator class.

    This class tests the functionality of the BaseDecorator class, which extends BaseFunction to create
    decorator-like callable objects.
    """

    # Attributes #
    TestClass: Type[BaseDecorator] = BaseDecorator

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

    def test_call(self, test_function_object: BaseDecorator) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """
        # Call the callable object
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_as_function(self, test_function_object: BaseDecorator) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
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

    def test_call_wrapped(self, test_function_object: BaseDecorator) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_coroutine(self, test_coroutine_object: BaseDecorator) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a BaseDecorator instance that wraps a coroutine function.
        """
        # Call the coroutine
        coro = test_coroutine_object(3)

        # Verify it's a coroutine
        assert asyncio.iscoroutine(coro)

        # Run the coroutine and verify the result
        result = asyncio.run(coro)
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        coro = test_coroutine_object(3, 4)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_as_function_coroutine(self, test_coroutine_object: BaseDecorator) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a BaseDecorator instance that wraps a coroutine function.
        """
        # Convert to a standard Python function
        func = test_coroutine_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Call the function and verify it returns a coroutine
        coro = func(3)
        assert asyncio.iscoroutine(coro)

        # Run the coroutine and verify the result
        result = asyncio.run(coro)
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        coro = func(3, 4)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_decorator_usage(self) -> None:
        """Test using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """
        # Define a function to be decorated
        @self.TestClass
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(test_func, self.TestClass)

        # Verify the decorated function can be called
        result = test_func(3)
        assert result == 5  # 3 + 2 (default y)

        # Verify the decorated function can be called with different arguments
        result = test_func(3, 4)
        assert result == 7  # 3 + 4

    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Test using the decorator with arguments.

        This test verifies that the decorator can be used with arguments.

        Args:
            *args: Positional arguments to pass to the decorator.
            **kwargs: Keyword arguments to pass to the decorator.
        """
        # Define a function to be decorated with arguments
        @self.TestClass(*args, **kwargs)
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(test_func, self.TestClass)

        # Verify the decorated function can be called
        result = test_func(3)
        assert result == 5  # 3 + 2 (default y)

        # Verify the decorated function can be called with different arguments
        result = test_func(3, 4)
        assert result == 7  # 3 + 4

    def test_concrete_decorator(self) -> None:
        """Test a concrete implementation of BaseDecorator.

        This test verifies that a concrete implementation of BaseDecorator works correctly.
        """
        # Create a concrete decorator
        decorator = ConcreteDecorator()

        # Define a function to be decorated
        def test_func() -> str:
            return "test"

        # Apply the decorator
        decorated = decorator(test_func)

        # Verify the decorated function works correctly
        assert decorated() == "Decorated: test"

        # Create a concrete decorator with a custom prefix
        custom_decorator = ConcreteDecorator(prefix="Custom: ")

        # Apply the decorator
        custom_decorated = custom_decorator(test_func)

        # Verify the decorated function works correctly
        assert custom_decorated() == "Custom: test"

    def test_concrete_decorator_usage(self) -> None:
        """Test using a concrete decorator in the standard Python way.

        This test verifies that a concrete decorator can be used in the standard Python way.
        """
        # Use the decorator directly
        @ConcreteDecorator
        def direct_func() -> str:
            return "direct"

        # Verify the decorator works correctly
        assert direct_func() == "Decorated: direct"

        # Use the decorator with arguments
        @ConcreteDecorator(prefix="Custom: ")
        def custom_func() -> str:
            return "custom"

        # Verify the decorator with arguments works correctly
        assert custom_func() == "Custom: custom"

    def test_pickle(self, test_function_object: BaseDecorator) -> None:
        """Test that the decorator can be pickled and unpickled.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """
        # Pickle the decorator
        pickled = pickle.dumps(test_function_object)

        # Unpickle the decorator
        unpickled = pickle.loads(pickled)

        # Verify the unpickled decorator is an instance of the correct class
        assert isinstance(unpickled, self.TestClass)

        # Verify the unpickled decorator has the correct wrapped function
        assert unpickled.__func__.__name__ == test_function_object.__func__.__name__

        # Verify the unpickled decorator can be called
        result = unpickled(3)
        assert result == 5  # 3 + 2 (default y)

    def test_copy(self, test_function_object: BaseDecorator) -> None:
        """Test that the decorator can be copied.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """
        # Copy the decorator
        copied = copy.copy(test_function_object)

        # Verify the copied decorator is an instance of the correct class
        assert isinstance(copied, self.TestClass)

        # Verify the copied decorator has the correct wrapped function
        assert copied.__func__ is test_function_object.__func__

        # Verify the copied decorator can be called
        result = copied(3)
        assert result == 5  # 3 + 2 (default y)

    def test_deepcopy(self, test_function_object: BaseDecorator) -> None:
        """Test that the decorator can be deep copied.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """
        # Deep copy the decorator
        deepcopied = copy.deepcopy(test_function_object)

        # Verify the deep copied decorator is an instance of the correct class
        assert isinstance(deepcopied, self.TestClass)

        # Verify the deep copied decorator has the correct wrapped function
        assert deepcopied.__func__.__name__ == test_function_object.__func__.__name__

        # Verify the deep copied decorator can be called
        result = deepcopied(3)
        assert result == 5  # 3 + 2 (default y)

    def test_no_function(self) -> None:
        """Test the edge case where no function is provided to the decorator."""
        # Create a decorator without a function
        decorator = self.TestClass()

        # Verify it's a partial function
        assert isinstance(decorator, partial)

        # Apply the decorator to a function
        decorated = decorator(example_function)

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(decorated, self.TestClass)

        # Verify the decorated function can be called
        result = decorated(3)
        assert result == 5  # 3 + 2 (default y)

    def test_none_function(self) -> None:
        """Test the edge case where None is provided as the function to the decorator."""
        # Create a decorator with None as the function
        decorator = self.TestClass(func=None)

        # Verify it's a partial function
        assert isinstance(decorator, partial)

        # Apply the decorator to a function
        decorated = decorator(example_function)

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(decorated, self.TestClass)

        # Verify the decorated function can be called
        result = decorated(3)
        assert result == 5  # 3 + 2 (default y)

    def test_coroutine_decorator(self) -> None:
        """Test the edge case where the decorator is applied to a coroutine function."""
        # Define a coroutine to be decorated
        @self.TestClass
        async def test_coro(x: int, y: int = 2) -> int:
            await asyncio.sleep(0.001)  # Simulate some async work
            return x + y

        # Verify the decorated coroutine is an instance of the decorator class
        assert isinstance(test_coro, self.TestClass)

        # Call the decorated coroutine
        coro = test_coro(3)

        # Verify it's a coroutine
        assert asyncio.iscoroutine(coro)

        # Run the coroutine and verify the result
        result = asyncio.run(coro)
        assert result == 5  # 3 + 2 (default y)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])