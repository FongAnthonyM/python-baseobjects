#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedkeylesscache_test.py
Tests for the timedkeylesscache module in the baseobjects.cachingtools.caches package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools.caches.timedkeylesscache import (
    TimedKeylessCacheCallable,
    TimedKeylessCacheMethod,
    TimedKeylessCache,
    timed_keyless_cache,
)
from tests.cachingtools.basetimedcache_test import BaseCacheTest


# Definitions #
# Classes #
class TestTimedKeylessCache(BaseCacheTest):
    """Test the TimedKeylessCacheCallable class.

    This class tests the functionality of the TimedKeylessCacheCallable class, which is a periodically clearing
    cache wrapper object for a function that only has one result and doesn't create a key from arguments.
    """

    # Attributes #
    class_: Type[TimedKeylessCacheCallable] = TimedKeylessCache

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TimedKeylessCacheCallable can be created.

        This test verifies that TimedKeylessCacheCallable instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func, _ = self.create_function_cache()
        assert cache_func is not None
        assert isinstance(cache_func, TimedKeylessCacheCallable)
        assert cache_func.args_key is None
        assert cache_func.cache_container is None

    def test_function_instance_creation(self) -> None:
        """Test that instances of TimedKeylessCache can be created.

        This test verifies that TimedKeylessCache instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func, _ = self.create_function_cache()
        assert cache_func is not None
        assert isinstance(cache_func, TimedKeylessCache)
        assert cache_func.method_type == TimedKeylessCacheMethod

    def test_caching(self) -> None:
        """Test the caching method.

        This test verifies that the caching method caches a single result without using keys from arguments.
        """
        cache_func, get_call_count = self.create_function_cache()
        
        # Call the function with an argument
        result1 = cache_func(2)
        assert result1 == 4
        assert get_call_count() == 1
        assert cache_func.args_key is True  # Should be set to True, not a key
        assert cache_func.cache_container == 4
        
        # Call again with the same argument
        result2 = cache_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # No new call
        
        # Call with a different argument
        result3 = cache_func(3)
        assert result3 == 4  # Should return the cached result, not 6
        assert get_call_count() == 1  # No new call
        assert cache_func.cache_container == 4
        
        # Clear the cache and call again
        cache_func.clear_cache()
        result4 = cache_func(3)
        assert result4 == 6
        assert get_call_count() == 2  # New call after clearing
        assert cache_func.args_key is True
        assert cache_func.cache_container == 6
        
        # Call with the first argument again
        result5 = cache_func(2)
        assert result5 == 6  # Should return the cached result, not 4
        assert get_call_count() == 2  # No new call

    def test_method(self) -> None:
        """Test the bind method.

        This test verifies that the bind method creates a method bound to another object.
        """

        class CachedClass:
            call_count = 0

            @timed_keyless_cache
            def cached_method(self):
                self.call_count += 1
                return 10 * 2

        instance_1 = CachedClass()
        instance_2 = CachedClass()

        instance_1.cached_method()

        assert instance_1.call_count == 1
        assert instance_2.call_count == 0
        assert instance_1.cached_method.cache_container == 20
        assert instance_2.cached_method.cache_container == 20

        instance_2.cached_method()

        assert instance_1.call_count == 1
        assert instance_2.call_count == 0
        assert instance_1.cached_method.cache_container == 20
        assert instance_2.cached_method.cache_container == 20

    def test_instanced_method(self) -> None:
        """Test the bind method.

        This test verifies that the bind method creates a method bound to another object.
        """

        class CachedClass:
            call_count = 0

            @timed_keyless_cache(instanced=True)
            def cached_method(self):
                self.call_count += 1
                return 10 * 2

        instance = CachedClass()
        bound_method = instance.cached_method

        assert bound_method is not None
        assert isinstance(bound_method, TimedKeylessCacheMethod)
        assert bound_method.__self__ is instance
        assert bound_method.__owner__ is CachedClass

        instance_1 = CachedClass()
        instance_2 = CachedClass()

        instance_1.cached_method()

        assert instance_1.call_count == 1
        assert instance_2.call_count == 0
        assert instance_1.cached_method.cache_container == 20
        assert instance_2.cached_method.cache_container == None

        instance_2.cached_method()

        assert instance_1.call_count == 1
        assert instance_2.call_count == 1
        assert instance_1.cached_method.cache_container == 20
        assert instance_2.cached_method.cache_container == 20
        assert instance_1.cached_method != instance_2.cached_method


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])