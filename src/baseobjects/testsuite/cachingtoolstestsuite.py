""" cachetestsuite.py
Specialized test suite for cache classes in the baseobjects package.
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
from abc import abstractmethod
import copy
import pickle
import time
from typing import Any, Type, Callable

# Third-Party Packages #
import pytest

# Local Packages #
from ..cachingtools import BaseTimedCache
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Classes #
class TimedCacheTestSuite(BaseObjectTestSuite):
    """Base test suite for cache classes.

    This class provides common test functionality for cache classes, including tests for caching, retrieval,
    and clearing. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The cache class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[BaseTimedCache]

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def create_test_function(self) -> tuple[Callable, Callable]:
        """Create a test function for testing caching behavior.

        Returns:
            A tuple containing:
            - A function that can be cached
            - A function that returns the number of times the cached function has been called
        """
        call_count = 0

        def example_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        def get_call_count():
            nonlocal call_count
            return call_count

        return example_func, get_call_count

    @pytest.fixture
    def function_cache(self, create_test_function: tuple[Callable, Callable]) -> tuple[Any, Callable, Callable]:
        """Create a cache with a cached function for testing.

        Args:
            create_test_function: A tuple containing a function to cache and a call counter.

        Returns:
            A tuple containing:
            - A cache with a cached function
            - The cached function
            - A function that returns the number of times the cached function has been called
        """
        test_function, get_call_count = create_test_function
        return self.TestClass(func=test_function), test_function, get_call_count

    @pytest.fixture
    def test_object(self, function_cache: tuple[Any, Callable, Callable]) -> Any:
        """Create a test object.

        Returns:
            A test object.
        """
        return function_cache[0]

    def create_test_function_cache(
        self,
        create_test_function: tuple[Callable, Callable],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[Any, Callable, Callable]:
        """Create a cache with a cached function for testing.

        Args:
            create_test_function: A tuple containing a function to cache and a call counter.

        Returns:
            A tuple containing:
            - A cache with a cached function
            - The cached function
            - A function that returns the number of times the cached function has been called
        """
        test_function, get_call_count = create_test_function
        return self.TestClass(func=test_function, *args, **kwargs), test_function, get_call_count

    # Tests
    @pytest.mark.parametrize("typed", [None, True, False])
    @pytest.mark.parametrize("lifetime", [None, 1, 1.0])
    @pytest.mark.parametrize("call_method", [None, "cache", "call"])
    @pytest.mark.parametrize("instanced", [None, True, False])
    def test_instance_creation(
        self,
        create_test_function: tuple[Callable, Callable],
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Test that instances of the class can be created.

        This method can be overridden by subclasses to perform additional tests on the instance.

        Args:
            create_test_function: A tuple containing a function to cache and a call counter.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            instanced: Determines if the cache exists in the main function or in the method instances.
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        caching_func, _, _ = self.create_test_function_cache(
            create_test_function,
            lifetime=lifetime,
            typed=typed,
            call_method=call_method,
            instanced=instanced,
            *args,
            **kwargs
        )

        # Validate
        assert isinstance(caching_func, self.TestClass)
        assert caching_func.lifetime == lifetime

    def test_copy(self, test_object: Any) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Cache Object
        cache_copy = copy.copy(test_object)

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.func is test_object.func
        assert cache_copy.clear_condition is test_object.clear_condition
        assert cache_copy.is_timed is test_object.is_timed
        assert cache_copy.lifetime is test_object.lifetime
        assert cache_copy.expiration is test_object.expiration
        assert cache_copy.cache is test_object.cache
        assert cache_copy.call_counter is test_object.call_counter
        assert cache_copy.cache_lock is test_object.cache_lock

    def test_copy_method(self, test_object: Any) -> None:
        """Test the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Cache Object
        cache_copy = test_object.copy()

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.func is test_object.func
        assert cache_copy.clear_condition is test_object.clear_condition
        assert cache_copy.is_timed is test_object.is_timed
        assert cache_copy.lifetime is test_object.lifetime
        assert cache_copy.expiration is test_object.expiration
        assert cache_copy.cache is test_object.cache
        assert cache_copy.call_counter is test_object.call_counter

    def test_deepcopy(self, test_object: Any) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        cache_copy = copy.deepcopy(test_object)
        assert cache_copy is not test_object
        assert cache_copy.func is test_object.func
        assert cache_copy.clear_condition is test_object.clear_condition
        assert cache_copy.is_timed is test_object.is_timed
        assert cache_copy.lifetime is test_object.lifetime
        assert cache_copy.expiration is test_object.expiration
        assert cache_copy.cache is not test_object.cache
        assert cache_copy.call_counter is not test_object.call_counter

    def test_deepcopy_method(self, test_object: Any) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        cache_copy = test_object.deepcopy()
        assert cache_copy is not test_object
        assert cache_copy.func is test_object.func
        assert cache_copy.clear_condition is test_object.clear_condition
        assert cache_copy.is_timed is test_object.is_timed
        assert cache_copy.lifetime is test_object.lifetime
        assert cache_copy.expiration is test_object.expiration
        assert cache_copy.cache is not test_object.cache
        assert cache_copy.call_counter is not test_object.call_counter

    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        cache_copy = pickle.loads(pickle.dumps(test_object))
        assert cache_copy is not test_object
        assert cache_copy.func is test_object.func
        assert cache_copy.clear_condition is test_object.clear_condition
        assert cache_copy.is_timed is test_object.is_timed
        assert cache_copy.lifetime is test_object.lifetime
        assert cache_copy.expiration is test_object.expiration
        assert cache_copy.cache is not test_object.cache
        assert cache_copy.call_counter is not test_object.call_counter

    def test_caching(self, function_cache: tuple[Any, Callable, Callable]) -> None:
        """Test the caching behavior of the cache class.

        This test verifies that the cache correctly caches function results and returns cached results
        on subsequent calls with the same arguments.

        Args:
            function_cache: A tuple containing a cache, a cached function, and a call counter.
        """
        cache_func, test_function, get_call_count = function_cache

        # Call the function multiple times with the same argument
        result1 = cache_func(2)
        result2 = cache_func(2)

        # Verify that the function returns the correct result
        assert result1 == 4
        assert result2 == 4

        # Verify that the function was only called once
        assert get_call_count() == 1

        # Call the function with a different argument
        result3 = cache_func(3)

        # Verify that the function returns the correct result
        assert result3 == 6

        # Verify that the function was called again
        assert get_call_count() == 2

    def test_cache_clearing(self, function_cache: tuple[Any, Callable, Callable]) -> None:
        """Test clearing the cache.

        This test verifies that the cache can be cleared and that subsequent calls to cached functions
        result in new function calls.

        Args:
            function_cache: A tuple containing a cache, a cached function, and a call counter.
        """
        cache_func, test_function, get_call_count = function_cache

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call the function again with the same argument to verify caching
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Call count should not increase

        # Clear the cache
        cache_func.clear_cache()

        # Call the function again with the same argument
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Call count should increase after clearing cache


class TimedCacheTestSuite(CacheTestSuite):
    """Base test suite for timed cache classes.

    This class provides common test functionality for timed cache classes, including tests for cache expiration.
    Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The timed cache class that the test suite is testing.
    """

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def function_cache(self, create_test_function: tuple[Callable, Callable]) -> tuple[Any, Callable, Callable]:
        """Create a cache with a cached function for testing.

        Args:
            create_test_function: A tuple containing a function to cache and a call counter.

        Returns:
            A tuple containing:
            - A cache with a cached function
            - The cached function
            - A function that returns the number of times the cached function has been called
        """
        test_function, get_call_count = create_test_function
        return self.TestClass(func=test_function, lifetime=1), test_function, get_call_count

    # Tests
    def test_cache_expiration(self, function_cache: tuple[Any, Callable, Callable]) -> None:
        """Test the expiration of cached items.

        This test verifies that cached items expire after the specified lifetime and that subsequent calls
        to cached functions result in new function calls.

        Args:
            function_cache: A tuple containing a cache with a short lifetime, a cached function, and a call counter.
        """
        cache_func, test_function, get_call_count = function_cache

        # Call the function to cache the result
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call the function again with the same argument to verify caching
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Call count should not increase

        # Wait for the cache to expire
        time.sleep(cache_func.lifetime + 0.1)

        # Call the function again with the same argument
        result3 = cache_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Call count should increase after cache expiration

    def test_clear_condition(self, function_cache: tuple[Any, Callable, Callable]) -> None:
        """Test the clear condition of the cache.

        This test verifies that the cache correctly determines when to clear cached items based on their
        expiration time.

        Args:
            function_cache: A tuple containing a cache with a short lifetime, a cached function, and a call counter.
        """
        cache_func, test_function, get_call_count = function_cache

        # Verify that clear_condition returns False when the cache is not expired
        cache_func.is_timed = True
        cache_func.expiration = time.perf_counter() + 2
        assert not cache_func.clear_condition()

        # Verify that clear_condition returns True when the cache is expired
        cache_func.expiration = time.perf_counter() - 2
        assert cache_func.clear_condition()

        # Verify that clear_condition returns False when is_timed is False
        cache_func.is_timed = False
        assert not cache_func.clear_condition()

        # Verify that clear_condition returns False when lifetime is None
        cache_func.is_timed = True
        cache_func.lifetime = None
        assert not cache_func.clear_condition()

    @abstractmethod
    def test_pause_timer(self, short_lived_cache: tuple[Any, Callable, Callable]) -> None:
        """Test pausing the cache timer.

        This test verifies that the cache timer can be paused and that cached items do not expire while
        the timer is paused.

        Args:
            short_lived_cache: A tuple containing a cache with a short lifetime, a cached function, and a call counter.
        """
