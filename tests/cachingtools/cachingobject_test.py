#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" cachingobject_test.py
Tests for the cachingtools module in the baseobjects package.
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
import datetime
import pickle
import time
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools import CachingObject, timed_keyless_cache, timed_lru_cache
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestCachingObject(ClassTest):
    """Test the CachingObject class.

    This class tests the functionality of the CachingObject class, which provides caching capabilities for methods and
    functions.
    """

    # Class Definitions #
    class CachingTestObject(CachingObject):
        """A test class that inherits from CachingObject for testing caching functionality.

        This class implements various methods to test different aspects of caching.
        """
        # Attributes #
        a: int

        # Properties #
        @property
        def now_alias(self) -> datetime.datetime:
            """A property that returns the cached result of get_now.

            Returns:
                The cached datetime from get_proxy.
            """
            return self.get_now.call_caching()

        # Magic Methods #
        # Construction/Destruction
        def __init__(self, a: int = 1, init: bool = True) -> None:
            """Initialize with a value and init flag.

            Args:
                a: A value to store in the object.
                init: Whether to initialize the object.
            """
            super().__init__()
            self.a = a

        # Instance Methods #
        @timed_keyless_cache(lifetime=2, call_method="call_clearing", instanced=True)
        def get_now(self) -> datetime.datetime:
            """A method decorated with timed_keyless_cache that returns the current datetime.

            Returns:
                The current datetime.
            """
            return datetime.datetime.now()

        def normal(self) -> datetime.datetime:
            """A normal method that returns the current datetime.

            Returns:
                The current datetime.
            """
            return datetime.datetime.now()

        def printer(self) -> None:
            """Print the value of a.

            This method is used for testing purposes.
            """
            print(self.a)

    # Attributes #
    class_: Type[CachingObject] = CachingObject
    zero_time: datetime.timedelta = datetime.timedelta(0)

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of CachingObject can be created.

        This test verifies that CachingObject instances can be created with various parameters.
        """
        # Create a basic instance
        cacher = self.class_()
        assert cacher is not None
        assert hasattr(cacher, "_is_cache")
        assert hasattr(cacher, "_caches")

        # Create a test object instance
        test_obj = self.CachingTestObject()
        assert test_obj is not None
        assert hasattr(test_obj, "a")
        assert hasattr(test_obj, "now_alias")

    def test_pickling(self) -> None:
        """Test pickling and unpickling of CachingObject instances.

        This test verifies that CachingObject instances can be pickled and unpickled correctly.
        """
        cacher = self.CachingTestObject()

        pickle_jar = pickle.dumps(cacher)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(cacher))

    def test_object_timed_cache(self) -> None:
        """Test the timed caching behavior of a CachingObject method.

        This test verifies that cached values expire after the specified lifetime.
        """
        cacher = self.CachingTestObject()

        first = cacher.now_alias
        time.sleep(1)
        second = cacher.now_alias  # Should still be cached
        time.sleep(2)
        third = cacher.now_alias   # Cache should have expired

        assert second == first  # Verify the value was cached
        assert third > first    # Verify the cache expired and a new value was generated

    def test_object_cache_reset(self) -> None:
        """Test resetting the cache of a CachingObject method.

        This test verifies that calling the original method directly resets the cache.
        """
        cacher = self.CachingTestObject()

        first = cacher.now_alias
        time.sleep(1)
        second = cacher.get_now()  # Direct call resets the cache
        time.sleep(1)
        third = cacher.now_alias         # Should use the new cached value

        assert second > first    # Verify a new value was generated
        assert third == second   # Verify the new value was cached

    def test_object_cache_instances(self) -> None:
        """Test that different instances have separate caches.

        This test verifies that caching is instance-specific and not shared between instances.
        """
        cacher = self.CachingTestObject()
        cacher2 = self.CachingTestObject()

        first = cacher.now_alias
        _ = cacher.now_alias  # Access the cache again
        time.sleep(1)
        second = cacher2.now_alias  # Different instance should have a different cache

        assert second - first != self.zero_time  # Verify the timestamps are different


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
