#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedsinglecache_test.py
Tests for the timedsinglecache module in the baseobjects.cachingtools.caches package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools.caches.timedsinglecache import (
    TimedSingleCacheCallable,
    TimedSingleCacheMethod,
    TimedSingleCache,
    timed_single_cache,
)
from tests.cachingtools.basetimedcache_test import BaseCacheTest


# Definitions #
# Classes #
class TestTimedSingleCache(BaseCacheTest):
    """Test the TimedSingleCacheCallable class.

    This class tests the functionality of the TimedSingleCacheCallable class, which is a periodically clearing single
    item cache wrapper for a function.
    """

    # Attributes #
    class_: Type[TimedSingleCacheCallable] = TimedSingleCache

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TimedSingleCacheCallable can be created.

        This test verifies that TimedSingleCacheCallable instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func, _ = self.create_function_cache()
        assert cache_func is not None
        assert isinstance(cache_func, TimedSingleCacheCallable)
        assert cache_func.args_key is None
        assert cache_func.cache_container is None

    def test_function_instance_creation(self) -> None:
        """Test that instances of TimedSingleCache can be created.

        This test verifies that TimedSingleCache instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func, _ = self.create_function_cache()
        assert cache_func is not None
        assert isinstance(cache_func, TimedSingleCache)
        assert cache_func.method_type == TimedSingleCacheMethod

    def test_caching(self) -> None:
        """Test the caching method.

        This test verifies that the caching method caches a single result based on argument keys.
        """
        cache_func, get_call_count = self.create_function_cache()
        
        # Call the function with an argument
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1
        assert cache_func.args_key is not None
        assert cache_func.cache_container == 4
        
        # Call again with the same argument
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # No new call
        
        # Call with a different argument
        result3 = cache_func(3)
        assert result3 == 6
        assert get_call_count() == 2  # New call
        assert cache_func.cache_container == 6
        
        # Call again with the first argument
        result4 = cache_func(2)
        assert result4 == 4
        assert get_call_count() == 3  # New call because the cache only holds one item

    def test_refresh_expiration(self) -> None:
        """Test the refresh_expiration method.

        This test verifies that the refresh_expiration method refreshes the expiration time.
        """
        # Test with lifetime=None
        cache_func, _ = self.create_function_cache(lifetime=None)
        initial_expiration = cache_func.expiration
        time.sleep(0.1)
        cache_func.refresh_expiration()
        assert cache_func.expiration == initial_expiration  # Should not change
        
        # Test with lifetime=1
        cache_func, _ = self.create_function_cache(lifetime=1)
        initial_expiration = cache_func.expiration
        time.sleep(0.1)
        cache_func.refresh_expiration()
        assert cache_func.expiration > initial_expiration  # Should be updated

    def test_clear_cache(self) -> None:
        """Test the clear_cache method.

        This test verifies that the clear_cache method clears the cache and updates expiration.
        """
        cache_func, _ = self.create_function_cache(lifetime=1)
        
        # Fill the cache
        cache_func(2)
        assert cache_func.args_key is not None
        assert cache_func.cache_container == 4
        
        # Clear the cache
        initial_expiration = cache_func.expiration
        time.sleep(0.1)
        cache_func.clear_cache()
        
        assert cache_func.args_key is None
        assert cache_func.cache_container is None
        assert cache_func.expiration > initial_expiration  # Should be updated

    def test_method(self) -> None:
        """Test the bind method.

        This test verifies that the bind method creates a method bound to another object.
        """

        class CachedClass:
            call_count = 0

            @timed_single_cache
            def cached_method(self, x):
                self.call_count += 1
                return x * 2

        instance_1 = CachedClass()
        instance_2 = CachedClass()

        instance_1.cached_method(1)
        instance_2.cached_method(2)

        assert instance_1.call_count == 1
        assert instance_2.call_count == 1
        assert instance_1.cached_method.cache_container == 4

    def test_instanced_method(self) -> None:
        """Test the bind method.

        This test verifies that the bind method creates a method bound to another object.
        """

        class CachedClass:
            call_count = 0

            @timed_single_cache(instanced=True)
            def cached_method(self, x):
                self.call_count += 1
                return x * 2

        instance = CachedClass()
        bound_method = instance.cached_method

        assert bound_method is not None
        assert isinstance(bound_method, TimedSingleCacheMethod)
        assert bound_method.__self__ is instance
        assert bound_method.__owner__ is CachedClass

        instance_1 = CachedClass()
        instance_2 = CachedClass()

        instance_1.cached_method(1)
        instance_2.cached_method(2)

        assert instance_1.call_count == 1
        assert instance_2.call_count == 1
        assert instance_1.cached_method.cache_container == 2
        assert instance_2.cached_method.cache_container == 4
        assert instance_1.cached_method != instance_2.cached_method


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])