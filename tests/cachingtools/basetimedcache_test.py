#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basetimedcache_test.py
Tests for the basetimedcache module in the baseobjects.cachingtools.caches package.
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
from typing import Type, Callable

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools.caches.basetimedcache import (
    _HashedSeq,
    CacheItem,
    BaseTimedCacheCallable,
    BaseTimedCacheMethod,
    BaseTimedCache,
)
from tests.bases.base_test import ClassTest



# Definitions #
# Data Classes #
class TestHashedSeq(ClassTest):
    """Test the _HashedSeq class.

    This class tests the functionality of the _HashedSeq class, which creates a hash value based on an iterable.
    """

    # Attributes #
    class_: Type[_HashedSeq] = _HashedSeq

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of _HashedSeq can be created.

        This test verifies that _HashedSeq instances can be created with various parameters.
        """
        # Create a basic instance
        hashed_seq = self.class_((1, 2, 3))
        assert hashed_seq is not None
        assert hasattr(hashed_seq, "hashvalue")
        assert hashed_seq.hashvalue == hash((1, 2, 3))

        # Create an instance with a custom hash function
        custom_hash = lambda x: sum(x)
        hashed_seq = self.class_((1, 2, 3), hash_=custom_hash)
        assert hashed_seq.hashvalue == 6

    def test_hash_method(self) -> None:
        """Test the __hash__ method of _HashedSeq.

        This test verifies that the __hash__ method returns the hashvalue attribute.
        """
        hashed_seq = self.class_((1, 2, 3))
        assert hash(hashed_seq) == hashed_seq.hashvalue


class TestCacheItem(ClassTest):
    """Test the CacheItem class.

    This class tests the functionality of the CacheItem class, which represents an item in a cache.
    """

    # Attributes #
    class_: Type[CacheItem] = CacheItem

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of CacheItem can be created.

        This test verifies that CacheItem instances can be created with various parameters.
        """
        # Create a basic instance
        cache_item = self.class_()
        assert cache_item is not None
        assert hasattr(cache_item, "priority_link")
        assert hasattr(cache_item, "key")
        assert hasattr(cache_item, "result")
        assert cache_item.priority_link is None
        assert cache_item.key is None
        assert cache_item.result is None

        # Create an instance with parameters
        cache_item = self.class_(key="test_key", result="test_result", priority_link="test_link")
        assert cache_item.key == "test_key"
        assert cache_item.result == "test_result"
        assert cache_item.priority_link == "test_link"


# Classes #
class BaseCacheTest(ClassTest):
    """Base test class for cache types.

    This class defines a generic common set of tests which all cache types must pass.
    Specific cache type test classes should inherit from this class and may extend it
    with additional test methods specific to that cache type.
    """

    # Attributes #
    class_: Type = None  # To be defined by subclasses

    # Instance Methods #
    # Fixtures
    def create_test_function(self) -> tuple[Callable, Callable]:
        """Create a test function for use in cache tests.

        This method creates a function that can be used to test caching behavior. The function includes a call counter
        to track how many times it's called.

        Returns:
            A tuple containing the test function and a reference to the call counter.
        """
        call_count = 0

        def test_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        def get_call_count():
            nonlocal call_count
            return call_count

        return test_func, get_call_count

    def create_function_cache(self, *args, **kwargs) -> tuple[Callable, Callable]:
        """Create an instance of the cache class being tested.

        This method should be implemented by subclasses to create an instance
        of the specific cache type being tested.

        Args:
            *args: Positional arguments to pass to the cache class constructor.
            **kwargs: Keyword arguments to pass to the cache class constructor.

        Returns:
            An instance of the cache class being tested.
        """
        test_function, get_call_count = self.create_test_function()
        return self.class_(*args, func=test_function, **kwargs), get_call_count

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseTimedCacheCallable can be created.

        This test verifies that BaseTimedCacheCallable instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func = self.create_function_cache()
        assert cache_func is not None

    def test_no_cache(self) -> None:
        """Test the no caching behavior.

        This test verifies that if no_cache is set, the wrapped function is called without caching.
        """
        cache_func, get_call_count = self.create_function_cache()
        cache_func.cache_method = "no_cache"

        # Call the function multiple times with the same argument
        result1 = cache_func(2)
        result2 = cache_func(2)

        assert result1 == 4
        assert result2 == 4
        assert get_call_count() == 2  # The function should be called each time with no_cache

    def test_cache_clearing(self) -> None:
        """Test clearing the cache.

        This test verifies that the clear_cache method clears the cache.
        """
        cache_func, _ = self.create_function_cache()
        cache_func.clear_cache()
        assert cache_func.expiration == 0  # The expiration should be reset to 0 after clearing

    def test_instanced_cache_property(self) -> None:
        """Test the instanced_cache property of BaseTimedCache.

        This test verifies that setting the instanced_cache property changes the bind method.
        """
        cache_func, _ = self.create_function_cache()

        # Test with instanced_cache=True
        cache_func.instanced_cache = True
        assert cache_func.instanced_cache
        assert cache_func.bind_multiplexer.selected == "bind_to_attribute"

        # Test with instanced_cache=False
        cache_func.instanced_cache = False
        assert not cache_func.instanced_cache
        assert cache_func.bind_multiplexer.selected == "bind_builtin"


class ConcreteTimedCacheCallable(BaseTimedCacheCallable):
    """A concrete implementation of BaseTimedCacheCallable for testing."""
    # Instance Methods #
    # Cache Control
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        super().clear_cache()
        self.cache_container = {}


class ConcreteTimedCacheMethod(ConcreteTimedCacheCallable, BaseTimedCacheMethod):
    """A concrete implementation of BaseTimedCacheMethod for testing."""


class ConcreteTimedCache(ConcreteTimedCacheCallable, BaseTimedCache):
    """A concrete implementation of BaseTimedCacheCallable for testing."""
    # Attributes #
    method_type = ConcreteTimedCacheMethod


class TestBaseTimedCacheCallable(BaseCacheTest):
    """Test the BaseTimedCacheCallable class.

    This class tests the functionality of the BaseTimedCacheCallable class, which is an abstract base class for timed
    cache callables.
    """
    # Attributes #
    class_: Type[BaseTimedCache] = ConcreteTimedCache

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseTimedCacheCallable can be created.

        This test verifies that BaseTimedCacheCallable instances can be created with various parameters.
        """
        # Create a basic instance
        cache_func = self.create_function_cache()
        assert cache_func is not None

    def test_cache_clearing(self) -> None:
        """Test clearing the cache.

        This test verifies that the clear_cache method clears the cache.
        """
        cache_func, _ = self.create_function_cache()
        cache_func.clear_cache()
        assert not cache_func.cache_container
        assert cache_func.expiration == 0  # The expiration should be reset to 0 after clearing

    def test_cache_expiration(self) -> None:
        """Test cache expiration.

        This test verifies that cached values expire after the specified lifetime.
        """
        # Test with is_timed=True, lifetime=1, and expiration in the past
        cache_func, _ = self.create_function_cache(lifetime=1)
        cache_func.is_timed = True
        cache_func.expiration = time.perf_counter() - 2
        assert cache_func.clear_condition()

        # Test with is_timed=True, lifetime=1, and expiration in the future
        cache_func, _ = self.create_function_cache(lifetime=1)
        cache_func.is_timed = True
        cache_func.expiration = time.perf_counter() + 2
        assert not cache_func.clear_condition()

    def test_create_key(self) -> None:
        """Test the create_key method of BaseTimedCacheCallable.

        This test verifies that the create_key method creates appropriate keys for different arguments.
        """
        def t_func(x, y=None):
            return x * 2

        cache_func = self.class_(func=t_func)

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

    def test_clear_condition(self) -> None:
        """Test the clear_condition method of BaseTimedCacheCallable.

        This test verifies that the clear_condition method returns True when the cache should be cleared.
        """
        def t_func(x):
            return x * 2

        # Test with is_timed=True and lifetime=None
        cache_func = self.class_(func=t_func, lifetime=None)
        cache_func.is_timed = True
        assert not cache_func.clear_condition()

        # Test with is_timed=False and lifetime=1
        cache_func = self.class_(func=t_func, lifetime=1)
        cache_func.is_timed = False
        assert not cache_func.clear_condition()

        # Test with is_timed=True, lifetime=1, and expiration in the past
        cache_func = self.class_(func=t_func, lifetime=1)
        cache_func.is_timed = True
        cache_func.expiration = time.perf_counter() - 2
        assert cache_func.clear_condition()

        # Test with is_timed=True, lifetime=1, and expiration in the future
        cache_func = self.class_(func=t_func, lifetime=1)
        cache_func.is_timed = True
        cache_func.expiration = time.perf_counter() + 2
        assert not cache_func.clear_condition()


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
