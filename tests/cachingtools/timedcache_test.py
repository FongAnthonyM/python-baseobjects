#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedcache_test.py
Tests for the timedcache module in the baseobjects.cachingtools.caches package.
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
from typing import Type, Callable, Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools.caches.timedcache import (
    TimedCacheCallable,
    TimedCacheMethod,
    TimedCache,
    timed_cache,
)
from tests.cachingtools.basetimedcache_test import BaseCacheTest


# Definitions #
# Classes #
class TestTimedCache(BaseCacheTest):
    """Test the TimedCacheCallable class.

    This class tests the functionality of the TimedCacheCallable class, which is a periodically clearing
    multiple item cache wrapper object for a function.
    """

    # Attributes #
    class_: Type[TimedCacheCallable] = TimedCache

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TimedCacheCallable can be created.

        This test verifies that TimedCacheCallable instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func, _ = self.create_function_cache()
        assert cache_func is not None
        assert isinstance(cache_func, TimedCacheCallable)
        
        # Create an instance with maxsize
        cache_func, _ = self.create_function_cache(maxsize=10)
        assert cache_func.maxsize == 10
        assert cache_func.cache_method == "limited_cache"
        
        # Create an instance with no maxsize
        cache_func, _ = self.create_function_cache(maxsize=None)
        assert cache_func.maxsize is None
        assert cache_func.cache_method == "unlimited_cache"
        
        # Create an instance with maxsize=0
        cache_func, _ = self.create_function_cache(maxsize=0)
        assert cache_func.maxsize == 0
        assert cache_func.cache_method == "no_cache"

    def test_function_instance_creation(self) -> None:
        """Test that instances of TimedCache can be created.

        This test verifies that TimedCache instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func, _ = self.create_function_cache()
        assert cache_func is not None
        assert isinstance(cache_func, TimedCache)

    def test_unlimited_cache(self) -> None:
        """Test the unlimited_cache method.

        This test verifies that the unlimited_cache method caches results without a limit.
        """
        cache_func, get_call_count = self.create_function_cache()
        cache_func.cache_method = "unlimited_cache"
        
        # Call the function multiple times with the same argument
        result1 = cache_func(2)
        result2 = cache_func(2)
        
        assert result1 == 4
        assert result2 == 4
        assert get_call_count() == 1  # The function should be called only once
        
        # Call with a different argument
        result3 = cache_func(3)
        assert result3 == 6
        assert get_call_count() == 2  # The function should be called again for a new argument

    def test_limited_cache(self) -> None:
        """Test the limited_cache method.

        This test verifies that the limited_cache method doesn't cache new results when the cache is full.
        """
        cache_func, get_call_count = self.create_function_cache(maxsize=2)
        cache_func.cache_method = "limited_cache"
        
        # Fill the cache
        cache_func(1)
        cache_func(2)
        assert get_call_count() == 2
        
        # Call with cached arguments
        cache_func(1)
        cache_func(2)
        assert get_call_count() == 2  # No new calls
        
        # Call with a new argument
        cache_func(3)
        assert get_call_count() == 3  # One new call
        
        # Call with the same new argument
        cache_func(3)
        assert get_call_count() == 3  # No new calls

    def test_set_maxsize(self) -> None:
        """Test the set_maxsize method.

        This test verifies that the set_maxsize method changes the cache's max size and updates the cache method.
        """
        cache_func, _ = self.create_function_cache()
        
        # Test with None
        cache_func.set_maxsize(None)
        assert cache_func.maxsize is None
        assert cache_func.cache_method == "unlimited_cache"
        
        # Test with 0
        cache_func.set_maxsize(0)
        assert cache_func.maxsize == 0
        assert cache_func.cache_method == "no_cache"
        
        # Test with a positive value
        cache_func.set_maxsize(10)
        assert cache_func.maxsize == 10
        assert cache_func.cache_method == "limited_cache"

    def test_poll(self) -> None:
        """Test the poll method.

        This test verifies that the poll method correctly checks if the cache has reached its max size.
        """
        cache_func, _ = self.create_function_cache(maxsize=2)
        
        # Empty cache
        assert cache_func.poll() is True
        
        # Add one item
        cache_func(1)
        assert cache_func.poll() is True
        
        # Add another item to reach maxsize
        cache_func(2)
        assert cache_func.poll() is True
        
        # Try to add one more item (should not be cached due to maxsize)
        cache_func(3)
        assert cache_func.poll() is False

    def test_get_length(self) -> None:
        """Test the get_length method.

        This test verifies that the get_length method returns the correct length of the cache.
        """
        cache_func, _ = self.create_function_cache()
        
        # Empty cache
        assert cache_func.get_length() == 0
        
        # Add items
        cache_func(1)
        assert cache_func.get_length() == 1
        
        cache_func(2)
        assert cache_func.get_length() == 2
        
        # Add duplicate (should not increase length)
        cache_func(1)
        assert cache_func.get_length() == 2

    def test_len_method(self) -> None:
        """Test the __len__ method.

        This test verifies that the __len__ method returns the correct length of the cache.
        """
        cache_func, _ = self.create_function_cache()
        
        # Empty cache
        assert len(cache_func) == 0
        
        # Add items
        cache_func(1)
        assert len(cache_func) == 1
        
        cache_func(2)
        assert len(cache_func) == 2

    def test_method(self) -> None:
        """Test the bind method.

        This test verifies that the bind method creates a method bound to another object.
        """

        class CachedClass:
            call_count = 0

            @timed_cache
            def cached_method(self, x):
                self.call_count += 1
                return x * 2

        instance_1 = CachedClass()
        instance_2 = CachedClass()

        instance_1.cached_method(1)
        instance_2.cached_method(2)

        assert instance_1.call_count == 1
        assert instance_2.call_count == 1
        assert len(instance_1.cached_method.__func__) == 2

    def test_instanced_method(self) -> None:
        """Test the bind method.

        This test verifies that the bind method creates a method bound to another object.
        """
        class CachedClass:
            call_count = 0

            @timed_cache(instanced=True)
            def cached_method(self, x):
                self.call_count += 1
                return x * 2
        
        instance = CachedClass()
        bound_method = instance.cached_method

        assert bound_method is not None
        assert isinstance(bound_method, TimedCacheMethod)
        assert bound_method.__self__ is instance
        assert bound_method.__owner__ is CachedClass

        instance_1 = CachedClass()
        instance_2 = CachedClass()

        instance_1.cached_method(1)
        instance_2.cached_method(2)

        assert instance_1.call_count == 1
        assert instance_2.call_count == 1
        assert len(instance_1.cached_method) == 1
        assert len(instance_2.cached_method) == 1
        assert instance_1.cached_method != instance_2.cached_method


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])