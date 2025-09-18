"""basetimedcachecallabletestsuite.py
Base test suite for BaseTimedCacheCallable and its subclasses.

This module provides a base test suite for testing the BaseTimedCacheCallable class and its subclasses. It defines
methods for testing the core functionality of timed cache callable objects, including caching behavior, cache
expiration, and cache clearing.
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
import pickle
import time
from typing import Any, Type, Callable

# Third-Party Packages #
import pytest

# Local Packages #
from ...cachingtools.caches.basetimedcache import _HashedSeq, BaseTimedCacheCallable
from ..functions.dynamiccallabletestsuite import DynamicCallableTestSuite


# Definitions #
# Classes #
class MethodCallCounter:
    """A simple class for counting method calls."""

    def __init__(self) -> None:
        """Initialize the instance."""
        self.count = 0

    def example_method(self, x: int) -> int:
        self.count += 1
        return x * 2

    def get_count(self) -> int:
        return self.count


class BaseTimedCacheCallableTestSuite(DynamicCallableTestSuite):
    """Base test suite for BaseTimedCacheCallable and its subclasses.
    
    This class provides common test functionality for timed cache callables, including tests for caching behavior,
    cache expiration, and cache clearing. Subclasses should set the TestClass attribute and may override or extend
    the test methods.
    
    Attributes:
        TestClass: The class that the test suite is testing, which should be BaseTimedCacheCallable or a subclass.
    """
    
    # Attributes #
    TestClass: Type[BaseTimedCacheCallable]
    
    # Instance Methods #
    def create_test_function(self) -> tuple[Callable, Callable]:
        """Create a test function for use in cache tests.
        
        This method creates a function that can be used to test caching behavior. The function includes a call counter
        to track how many times it's called.
        
        Returns:
            A tuple containing the test function and a reference to the call counter.
        """
        call_count = 0

        def test_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        def get_call_count() -> int:
            nonlocal call_count
            return call_count

        return test_func, get_call_count

    # Fixtures
    @pytest.fixture
    def test_function(self) -> tuple[Callable, Callable]:
        """Create a test function with a call counter.

        Returns:
            A tuple containing the test function and a function to get the call count.
        """
        return self.create_test_function()
    
    # Tests
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.
        
        This test verifies that instances of the TestClass can be created with various parameters.
        
        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """

    @abstractmethod
    def test_call(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.
        
        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test that the callable object can be converted to a standard Python function.
        
        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test that the wrapped function can be called directly.
        
        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """
    
    def test_call_multiplexer(self) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method."""
        # Create a test function object
        def test_func(x: int) -> int:
            return x * 2
        
        function_object = self.TestClass(func=test_func)
        
        # Test call_wrapped
        function_object.call_method = "call_wrapped"
        
        # Test no_cache
        function_object.call_method = "call_caching"

    def test_lifetime_setting(self) -> None:
        """Test that the lifetime can be set during construction and affects expiration."""
        # Create a cache with a specific lifetime
        func, get_call_count = self.create_test_function()
        cache_func = self.TestClass(func=func, lifetime=5)

        # Verify the lifetime was set correctly
        assert cache_func.lifetime == 5

        # Call the function to set the expiration
        cache_func.clear_cache()

        # Verify the expiration is in the future
        assert cache_func.expiration is not None
        assert cache_func.expiration > time.perf_counter()

        # Verify the expiration is approximately lifetime seconds in the future
        expected_expiration = time.perf_counter() + 5
        assert abs(cache_func.expiration - expected_expiration) < 0.1

    @abstractmethod
    def test_call_caching(self, test_function: tuple[Callable, Callable]) -> None:
        """Test the call_caching method.

        This test verifies that the call_caching method correctly caches results and clears the cache when needed.

        Args:
            test_function: A fixture providing a test function and call counter.
        """

    @abstractmethod
    def test_typed_caching(self, test_function: tuple[Callable, Callable]) -> None:
        """Test typed caching behavior.

        This test verifies that when typed=True, arguments of different types are cached separately.

        Args:
            test_function: A fixture providing a test function and call counter.
        """

    @abstractmethod
    def test_call_clearing(self, test_function: tuple[Callable, Callable]) -> None:
        """Test the call_clearing method.

        This test verifies that the call_clearing method clears the cache before each call.

        Args:
            test_function: A fixture providing a test function and call counter.
        """
    
    def test_no_cache(self, test_function: tuple[Callable, Callable]) -> None:
        """Test the no caching behavior.
        
        This test verifies that if no_cache is set, the wrapped function is called without caching.
        
        Args:
            test_function: A fixture providing a test function and call counter.
        """
        func, get_call_count = test_function
        cache_func = self.TestClass(func=func)
        cache_func.cache_method = "no_cache"

    @abstractmethod
    def test_cache_clearing(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test clearing the cache.
        
        This test verifies that the clear_cache method clears the cache.
        
        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """
    
    def test_clear_condition(self) -> None:
        """Test the clear_condition method of BaseTimedCacheCallable.
        
        This test verifies that the clear_condition method returns True when the cache should be cleared.
        """
        def test_func(x: int) -> int:
            return x * 2
        
        # Test with is_timed=True and lifetime=None
        cache_func = self.TestClass(func=test_func, lifetime=None)
        cache_func.is_timed = True
        assert not cache_func.clear_condition()
        
        # Test with is_timed=False and lifetime=1
        cache_func = self.TestClass(func=test_func, lifetime=1)
        cache_func.is_timed = False
        assert not cache_func.clear_condition()
        
        # Test with is_timed=True, lifetime=1, and expiration in the past
        cache_func = self.TestClass(func=test_func, lifetime=1)
        cache_func.is_timed = True
        cache_func.expiration = time.perf_counter() - 2
        assert cache_func.clear_condition()
        
        # Test with is_timed=True, lifetime=1, and expiration in the future
        cache_func = self.TestClass(func=test_func, lifetime=1)
        cache_func.is_timed = True
        cache_func.expiration = time.perf_counter() + 2
        assert not cache_func.clear_condition()
    
    def test_cache_method_property(self, test_function_object: BaseTimedCacheCallable) -> None:
        """Test the cache_method property.
        
        This test verifies that the cache_method property correctly gets and sets the caching method.
        
        Args:
            test_function_object: A fixture providing a BaseTimedCacheCallable instance that wraps a function.
        """
        # Set the cache_method property
        test_function_object.cache_method = "no_cache"
        
        # Verify the property was set correctly
        assert test_function_object.cache_method == "no_cache"
        assert test_function_object.cache.selected == "no_cache"
    
    def test_instanced_cache_property(self) -> None:
        """Test the instanced_cache property.
        
        This test verifies that the instanced_cache property correctly gets and sets the instanced cache flag.
        """
        def test_func(x: int) -> int:
            return x * 2
        
        cache_func = self.TestClass(func=test_func)
        
        # Test with instanced_cache=True
        cache_func.instanced_cache = True
        assert cache_func.instanced_cache
        
        # Test with instanced_cache=False
        cache_func.instanced_cache = False
        assert not cache_func.instanced_cache

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
        active_method = cache_func.cache.selected

        # Use the context manager to temporarily disable caching
        with cache_func.pause_caching():
            assert cache_func.cache.selected == "no_cache"

        assert cache_func.cache.selected == active_method
    
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
        active_method = cache_func.cache.selected
        
        # Stop caching
        cache_func.stop_caching()
        assert cache_func.cache.selected == "no_cache"
        
        # Resume caching
        cache_func.resume_caching()
        assert cache_func.cache.selected == active_method

