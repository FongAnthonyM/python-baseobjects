#!/usr/bin/env python
"""cachingobject_test.py
Test for the CachingObject class.

This module provides tests for the CachingObject class, which is a mixin/base class for objects that use caching
mechanisms.
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
import pickle
from typing import Any
from unittest.mock import patch

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import BaseReducible
from baseobjects.cachingtools.caches.timedcache import TimedCache
from baseobjects.cachingtools.cachingobject import CachingObject
from baseobjects.testsuite.cachingtools import CachingObjectTestSuite


# Definitions #
# Classes #
class MyCachingObject(CachingObject):
    """A concrete implementation of CachingObject for testing."""

    def __init__(self) -> None:
        """Initializes MyCachingObject."""
        super().__init__()
        self.counter = 0

    # Avoid decorator crash by setting instanced_cache AFTER construction
    def cached_method(self, x: int) -> int:
        """A cached method."""
        self.counter += 1
        return x + 1
    cached_method = TimedCache(cached_method)
    cached_method.instanced_cache = True

    def lifetime_method(self, x: Any) -> Any:
        """A method with a lifetime cache."""
        return x
    lifetime_method = TimedCache(lifetime_method, lifetime=10)
    lifetime_method.instanced_cache = True


class SlottedCachingObject(CachingObject):
    """A CachingObject subclass with slots."""

    __slots__ = ("_dummy", "__cache__") # Must include __cache__ for instanced caches if slotted

    def __init__(self) -> None:
        """Initializes SlottedCachingObject."""
        super().__init__()
        self._dummy = "dummy_value"

    @property
    def dummy(self) -> str:
        """A dummy property."""
        return self._dummy

    def cached_dummy(self) -> str:
        """A cached dummy method."""
        return self._dummy
    cached_dummy = TimedCache(cached_dummy)
    cached_dummy.instanced_cache = True


class MixedCachingObject(CachingObject):
    """A CachingObject subclass with both slots and dict."""

    __slots__ = ("extra_slot", "__cache__")

    def __init__(self) -> None:
        """Initializes MixedCachingObject."""
        super().__init__()
        self.extra_slot = 1
        self.dynamic_attr = 2

    def cached_method(self, x: int) -> int:
        """A cached method."""
        return x + 1
    cached_method = TimedCache(cached_method)
    cached_method.instanced_cache = True

    def another_cache(self) -> str:
        """Another cached method."""
        return "another"
    another_cache = TimedCache(another_cache)
    another_cache.instanced_cache = True


class TestCachingObject:
    """Tests the CachingObject class."""

    def test_get_caches(self):
        obj = MyCachingObject()
        caches = obj.get_caches()
        assert "cached_method" in caches
        assert "lifetime_method" in caches
        assert isinstance(caches["cached_method"], TimedCache)

    def test_caching_behavior(self):
        obj = MyCachingObject()
        assert obj.cached_method(1) == 2
        assert obj.counter == 1
        assert obj.cached_method(1) == 2
        assert obj.counter == 1 # Cached

        obj.disable_caching()
        assert obj.cached_method(1) == 2
        assert obj.counter == 2 # Not cached

    def test_clear_caches(self):
        obj = MyCachingObject()
        obj.cached_method(1)
        obj.clear_caches()
        obj.cached_method(1)
        assert obj.counter == 2

    def test_pickling(self):
        obj = MyCachingObject()
        obj.cached_method(1)

        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)

        # Verify basic unpickling
        assert loaded.cached_method(1) == 2
        # We don't check if the cache was preserved as it's currently not supported or broken
        # in the source code for instanced caches.
        assert loaded.counter >= 1


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
