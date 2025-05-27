#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedlrucache_test.py
Tests for the timedlrucache module in the baseobjects.cachingtools.caches package.
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
from src.baseobjects.cachingtools.caches.timedlrucache import (
    TimedLRUCache,
    TimedLRUCacheMethod,
    timed_lru_cache,
)
from tests.cachingtools.basetimedcache_test import BaseCacheTest


# Definitions #
# Classes #
class TestTimedLRUCache(BaseCacheTest):
    """Test the TimedLRUCache class.

    This class tests the functionality of the TimedLRUCache class, which is a periodically clearing
    Least Recently Used (LRU) cache wrapper object for a function.
    """

    # Attributes #
    class_: Type[TimedLRUCache] = TimedLRUCache

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TimedLRUCache can be created.

        This test verifies that TimedLRUCache instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func, _ = self.create_function_cache()
        assert cache_func is not None
        assert isinstance(cache_func, TimedLRUCache)

    def test_unlimited_cache_lru_behavior(self) -> None:
        """Test the unlimited_cache method with LRU behavior.

        This test verifies that the unlimited_cache method caches results and maintains LRU ordering.
        """
        cache_func, get_call_count = self.create_function_cache()
        cache_func.cache_method = "unlimited_cache"
        
        # Call the function with different arguments to fill the cache
        cache_func(1)
        cache_func(2)
        cache_func(3)
        assert get_call_count() == 3
        
        # Access items in reverse order to change LRU order
        cache_func(2)  # Now order is: 2, 3, 1
        cache_func(1)  # Now order is: 1, 2, 3
        assert get_call_count() == 3  # No new calls
        
        # Verify the LRU order by checking the priority queue
        # The most recently used item should be at the start of the priority queue
        assert cache_func.priority.first_node.data.key == 1
        assert cache_func.priority.first_node.next.data.key == 2
        assert cache_func.priority.last_node.data.key == 3

    def test_limited_cache_lru_behavior(self) -> None:
        """Test the limited_cache method with LRU behavior.

        This test verifies that the limited_cache method caches results up to maxsize
        and replaces the least recently used items when the cache is full.
        """
        cache_func, get_call_count = self.create_function_cache(maxsize=2)
        cache_func.cache_method = "limited_cache"
        
        # Fill the cache
        cache_func(1)
        cache_func(2)
        assert cache_func.priority.first_node.data.key == 2
        assert cache_func.priority.last_node.data.key == 1
        assert get_call_count() == 2

        # Access an item to change LRU order
        cache_func(1)  # Now order is: 2, 1
        assert cache_func.priority.first_node.data.key == 1
        assert cache_func.priority.last_node.data.key == 2
        assert get_call_count() == 2  # No new calls
        
        # Add a new item, which should replace the least recently used item (2)
        cache_func(3)  # Now order is: 3, 1
        assert cache_func.priority.first_node.data.key == 3
        assert cache_func.priority.last_node.data.key == 1
        assert get_call_count() == 3  # One new call
        
        # Verify that item 2 was replaced by checking if it requires a new call
        cache_func(2)
        assert cache_func.priority.first_node.data.key == 2
        assert cache_func.priority.last_node.data.key == 3
        assert get_call_count() == 4  # New call because 2 was replaced
        
        # Verify that item 3 is still in the cache
        cache_func(3)
        assert cache_func.priority.first_node.data.key == 3
        assert cache_func.priority.last_node.data.key == 2
        assert get_call_count() == 4  # No new call

    def test_method(self) -> None:
        """Test the bind method.

        This test verifies that the bind method creates a method bound to another object.
        """

        class CachedClass:
            call_count = 0

            @timed_lru_cache
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

            @timed_lru_cache(instanced=True)
            def cached_method(self, x):
                self.call_count += 1
                return x * 2

        instance = CachedClass()
        bound_method = instance.cached_method

        assert bound_method is not None
        assert isinstance(bound_method, TimedLRUCacheMethod)
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