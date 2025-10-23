"""basetimedcachecallable_test.py
Tests for the BaseTimedCacheCallable class in the baseobjects package.

This module provides tests for the BaseTimedCacheCallable class, which is a base cache wrapper object for a function
that resets its cache periodically. It tests the core functionality of BaseTimedCacheCallable, including instance
creation, caching behavior, cache expiration, and cache clearing.
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
import time
from collections.abc import Callable
from typing import Any, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.cachingtools.caches.basetimedcache import BaseTimedCacheCallable, _HashedSeq
from src.baseobjects.testsuite.cachingtools.basetimedcachecallabletestsuite import BaseTimedCacheCallableTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers."""
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers."""
    return x * y


# Helper Classes #
class ConcreteTimedCacheCallable(BaseTimedCacheCallable):
    """A concrete implementation of BaseTimedCacheCallable for testing.

    This class implements the abstract clear_cache method required by BaseTimedCacheCallable
    and provides a basic caching implementation.
    """

    _cache_method: str = "cache_dict"

    def __init__(
        self,
        func: Callable | None = None,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Initialize the cache container
        self.cache_container = {}

        # Parent initialization
        super().__init__(
            func=func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            instanced=instanced,
            *args,
            init=init,
            **kwargs,
        )

        # Add caching methods to the cache multiplexer
        self.cache.add_function("cache_dict", self.cache_dict)

        # Set the default cache method if none was specified
        if call_method is None:
            self.cache_method = "cache_dict"

    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        # Call the parent method to update the expiration
        super().clear_cache()

        # Clear the cache container
        self.cache_container = {}

    def cache_dict(self, *args: Any, **kwargs: Any) -> Any:
        """Cache the result of the wrapped function in a dictionary.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The cached result or the result of calling the wrapped function.
        """
        # Create a key for the cache
        key = self.create_key(args, kwargs, self.typed)

        # Check if the key is in the cache
        if key in self.cache_container:
            return self.cache_container[key]

        # Call the wrapped function and cache the result
        result = self.__wrapped__(*args, **kwargs)
        self.cache_container[key] = result

        return result


class TimedCacheTestObject:
    """A test class for testing method binding and caching."""

    def __init__(self, value: int = 10) -> None:
        """Initialize with a value."""
        self.value = value

    def method1(self, x: int) -> int:
        """A test method that adds x to the value."""
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x."""
        return self.value * x


# Tests #
class TestBaseTimedCacheCallable(BaseTimedCacheCallableTestSuite):
    """Test the BaseTimedCacheCallable class.

    This class tests the functionality of the BaseTimedCacheCallable class, which is a base cache wrapper object
    for a function that resets its cache periodically.
    """

    # Attributes #
    TestClass: type[BaseTimedCacheCallable] = ConcreteTimedCacheCallable

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object_instance(self) -> TimedCacheTestObject:
        """Create a test object instance.

        Returns:
            TimedCacheTestObject: An instance of the test object.
        """
        return TimedCacheTestObject(value=10)

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This test verifies that instances of the TestClass can be created with various parameters.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create a basic instance
        instance = self.TestClass(*args, **kwargs)
        assert instance is not None
        assert isinstance(instance, self.TestClass)

        # Create an instance with a function
        def test_func(x: int) -> int:
            return x * 2

        instance = self.TestClass(func=test_func, typed=True, lifetime=60)
        assert instance is not None
        assert instance.__wrapped__ is test_func
        assert instance.typed is True
        assert instance.lifetime == 60

    def test_call(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """
        # Call the function and verify the result
        result = test_function_object(5)
        assert result == 7

    def test_as_function(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """
        # Convert to a function and call it
        func = test_function_object.as_function()
        result = func(5)
        assert result == 7

    def test_call_wrapped(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(5)
        assert result == 7

    def test_bind_multiplexer(self) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method."""

        # Create a test class with a method
        class TestClass:
            def test_method(self, x: int) -> int:
                return x * 2

        # Create a test instance
        test_instance = TestClass()

        # Create a method object
        method_object = self.TestClass(func=TestClass.test_method)

        # Test bind_builtin
        method_object.bind_method = "bind_builtin"
        bound_method = method_object.__get__(test_instance, TestClass)
        assert bound_method(5) == 10

        # Test bind_wrapper
        method_object.bind_method = "bind_wrapped"
        bound_method = method_object.__get__(test_instance, TestClass)
        assert bound_method(5) == 10

    def test_call_multiplexer(self) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method."""

        # Create a test function object
        def test_func(x: int) -> int:
            return x * 2

        function_object = self.TestClass(func=test_func)

        # Test call_wrapped
        function_object.call_method = "call_wrapped"
        assert function_object(5) == 10

        # Test no_cache
        function_object.call_method = "call_caching"
        assert function_object(5) == 10

    def test_cache_clearing(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test clearing the cache.

        This test verifies that the clear_cache method clears the cache.

        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """
        test_function_object.clear_cache()
        assert test_function_object.expiration is not None

        # If the class has a cache_container, verify it's empty
        if hasattr(test_function_object, "cache_container") and test_function_object.cache_container is not None:
            assert not test_function_object.cache_container

    def test_create_key(self) -> None:
        """Test the create_key method of BaseTimedCacheCallable.

        This test verifies that the create_key method creates appropriate keys for different arguments.
        """

        def test_func(x: int, y: int | None = None) -> int:
            return x * 2

        cache_func = self.TestClass(func=test_func)

        # Test with a single argument
        key1 = cache_func.create_key((1,), {}, False)
        assert key1 == 1  # For a single argument of a simple type, the key is the argument itself

        # Test with multiple arguments
        key2 = cache_func.create_key((1, 2), {}, False)
        assert isinstance(key2, _HashedSeq)
        assert list(key2) == [1, 2]

        # Test with keyword arguments
        key3 = cache_func.create_key((1,), {"y": 2}, False)
        assert isinstance(key3, _HashedSeq)
        assert len(key3) > 2  # The key includes the argument, a marker, and the keyword argument

        # Test with typed=True and multiple arguments
        key4 = cache_func.create_key((1, 2), {}, True)
        assert isinstance(key4, _HashedSeq)
        assert len(key4) > 2  # The key includes the arguments and their types

    def test_call_caching(self, test_function: tuple[Callable, Callable]) -> None:
        """Test the call_caching method.

        This test verifies that the call_caching method correctly caches results and clears the cache when needed.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        cache_func = self.TestClass(func=func, lifetime=1)

        # Set up caching
        cache_func.call_method = "call_caching"

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call again to use the cache
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Count shouldn't increase if caching works

        # Set expiration to the past to trigger cache clearing
        cache_func.expiration = time.perf_counter() - 2

        # Call again, should clear cache and call function again
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Count should increase

    def test_typed_caching(self, test_function: tuple[Callable, Callable]) -> None:
        """Test typed caching behavior.

        This test verifies that when typed=True, arguments of different types are cached separately.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        cache_func = self.TestClass(func=func, typed=True)

        # Set up caching
        cache_func.call_method = "call_caching"

        # Call with int
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call with same value as float
        result2 = cache_func(2.0)
        assert result2 == 4
        assert get_call_count() == 2  # Count should increase because types are different

        # Call with int again
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Count shouldn't increase, using cache

        # Call with float again
        result4 = cache_func(2.0)
        assert result4 == 4
        assert get_call_count() == 2  # Count shouldn't increase, using cache

    def test_call_clearing(self, test_function: tuple[Callable, Callable]) -> None:
        """Test the call_clearing method.

        This test verifies that the call_clearing method clears the cache before each call.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        cache_func = self.TestClass(func=func)

        # Set up clearing
        cache_func.call_method = "call_clearing"

        # Call the function
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call again, should clear cache and call function again
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 2  # Count should increase

    def test_no_cache(self, test_function: tuple[Callable, Callable]) -> None:
        """Test the no caching behavior.

        This test verifies that if no_cache is set, the wrapped function is called without caching.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        cache_func = self.TestClass(func=func)
        cache_func.cache_method = "no_cache"

        # Call the function multiple times with the same argument
        result1 = cache_func(2)
        result2 = cache_func(2)

        assert result1 == 4
        assert result2 == 4
        assert get_call_count() == 2  # The function should be called each time with no_cache

    def test_cache_expiration(self, test_function: tuple[Callable, Callable]) -> None:
        """Test that the cache expires after the lifetime has elapsed.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        # Use a very short lifetime for testing
        cache_func = self.TestClass(func=func, lifetime=0.1)
        cache_func.cache_method = "cache_dict"

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call again immediately, should use cache
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Count shouldn't increase if caching works

        # Wait for the cache to expire
        time.sleep(0.2)

        # Call again, should call the function again
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Count should increase

    def test_is_timed_property(self) -> None:
        """Test the is_timed property.

        This test verifies that the is_timed property correctly controls whether the cache expires.
        """
        func, get_call_count = self.create_test_function()
        cache_func = self.TestClass(func=func, lifetime=0.1)
        cache_func.cache_method = "cache_dict"

        # Set is_timed to False
        cache_func.is_timed = False

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Wait for what would be the cache expiration time
        time.sleep(0.2)

        # Call again, should still use cache because is_timed is False
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Count shouldn't increase

        # Set is_timed to True
        cache_func.is_timed = True

        # Call again, should call the function again because the cache has expired
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Count should increase

    def test_pause_caching_context(self, test_function: tuple[Callable, Callable]) -> None:
        """Test the pause_caching context manager.

        This test verifies that the pause_caching context manager temporarily disables caching.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        cache_func = self.TestClass(func=func)

        # Set up caching
        cache_func.call_method = "call_caching"

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Use the context manager to temporarily disable caching
        with cache_func.pause_caching():
            # Call again, should not use cache
            result2 = cache_func(2)
            assert result2 == 4
            assert get_call_count() == 2  # Count should increase

            # Call again, still no cache
            result3 = cache_func(2)
            assert result3 == 4
            assert get_call_count() == 3  # Count should increase again

        # After the context, caching should be restored
        # Call again, should use cache again
        result4 = cache_func(2)
        assert result4 == 4
        assert get_call_count() == 4  # Count should increase because cache was cleared

    def test_stop_resume_caching(self, test_function: tuple[Callable, Callable]) -> None:
        """Test stopping and resuming caching.

        This test verifies that the stop_caching and resume_caching methods correctly control caching behavior.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        cache_func = self.TestClass(func=func)

        # Set up caching
        cache_func.call_method = "call_caching"

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call again to use the cache
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Count shouldn't increase if caching works

        # Stop caching
        cache_func.stop_caching()
        assert cache_func.cache.selected == "no_cache"

        # Call again, should not use cache
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Count should increase

        # Resume caching
        cache_func.resume_caching()
        assert cache_func.cache.selected == "cache_dict"

        # Call again, should use cache again
        result4 = cache_func(2)
        assert result4 == 4
        assert get_call_count() == 3  # Count should increase because cache was cleared

    def test_zero_lifetime(self) -> None:
        """Test the edge case where lifetime is set to zero."""
        func, get_call_count = self.create_test_function()
        cache_func = self.TestClass(func=func, lifetime=0)
        cache_func.cache_method = "cache_dict"

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call again immediately, should call the function again because lifetime is 0
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 2  # Count should increase

    def test_negative_lifetime(self) -> None:
        """Test the edge case where lifetime is set to a negative value."""
        func, get_call_count = self.create_test_function()
        cache_func = self.TestClass(func=func, lifetime=-1)
        cache_func.cache_method = "cache_dict"

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call again immediately, should call the function again because lifetime is negative
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 2  # Count should increase

    def test_multiple_cache_clears(self) -> None:
        """Test that the cache can be cleared multiple times."""
        func, get_call_count = self.create_test_function()
        cache_func = self.TestClass(func=func)
        cache_func.call_method = "call_caching"

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Clear the cache
        cache_func.clear_cache()

        # Call again, should call the function again
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 2  # Count should increase

        # Clear the cache again
        cache_func.clear_cache()

        # Call again, should call the function again
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 3  # Count should increase again

    def test_cache_with_different_arguments(self) -> None:
        """Test that different arguments are cached separately."""
        func, get_call_count = self.create_test_function()
        cache_func = self.TestClass(func=func)
        cache_func.call_method = "call_caching"

        # Call with argument 2
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call with argument 3
        result2 = cache_func(3)
        assert result2 == 6
        assert get_call_count() == 2  # Count should increase for different argument

        # Call with argument 2 again
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Count shouldn't increase, using cache

        # Call with argument 3 again
        result4 = cache_func(3)
        assert result4 == 6
        assert get_call_count() == 2  # Count shouldn't increase, using cache

    def test_cache_with_keyword_arguments(self) -> None:
        """Test that keyword arguments are properly handled in caching."""

        def test_func(x: int, y: int = 2) -> int:
            nonlocal call_count
            call_count += 1
            return x * y

        call_count = 0
        cache_func = self.TestClass(func=test_func)
        cache_func.call_method = "call_caching"

        # Call with positional arguments
        result1 = cache_func(2, 3)
        assert result1 == 6
        assert call_count == 1

        # Call with keyword arguments
        result2 = cache_func(x=2, y=3)
        assert result2 == 6
        assert call_count == 2  # Count should increase for different argument form

        # Call with mixed arguments
        result3 = cache_func(2, y=3)
        assert result3 == 6
        assert call_count == 3  # Count should increase for different argument form

        # Call with positional arguments again
        result4 = cache_func(2, 3)
        assert result4 == 6
        assert call_count == 3  # Count shouldn't increase, using cache


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
