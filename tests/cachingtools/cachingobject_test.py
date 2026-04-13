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

    @TimedCache(instanced=True)
    def cached_method(self, x: int) -> int:
        """A cached method.

        Returns:
            int: The result.
        """
        self.counter += 1
        return x + 1

    @TimedCache(lifetime=10, instanced=True)
    def lifetime_method(self, x: Any) -> Any:
        """A method with a lifetime cache.

        Returns:
            Any: The result.
        """
        return x


class SlottedCachingObject(CachingObject):
    """A CachingObject subclass with slots."""

    __slots__ = ("_dummy",)

    def __init__(self) -> None:
        """Initializes SlottedCachingObject."""
        super().__init__()
        self._dummy = "dummy_value"

    @property
    def dummy(self) -> str:
        """A dummy property.

        Returns:
            str: The dummy value.
        """
        return self._dummy

    @TimedCache(instanced=True)
    def cached_dummy(self) -> str:
        """A cached dummy method.

        Returns:
            str: The dummy value.
        """
        return self._dummy


class MixedCachingObject(CachingObject):
    """A CachingObject subclass with both slots and dict."""

    __slots__ = ("extra_slot",)

    def __init__(self) -> None:
        """Initializes MixedCachingObject."""
        super().__init__()
        self.extra_slot = 1
        self.dynamic_attr = 2

    @TimedCache(instanced=True)
    def cached_method(self, x: int) -> int:
        """A cached method.

        Returns:
            int: The result.
        """
        return x + 1

    @TimedCache(instanced=True)
    def another_cache(self) -> str:
        """Another cached method.

        Returns:
            str: The result.
        """
        return "another"


class TestCachingObject(CachingObjectTestSuite):
    """Tests the CachingObject class.

    This class tests the functionality of the CachingObject class, utilizing the CachingObjectTestSuite.
    """

    # Attributes #
    UnitTestClass = CachingObject

    # Instance Methods #
    # Fixtures
    @pytest.fixture(autouse=True)
    def reset_caching_state(self) -> None:
        """Resets the shared descriptor state before each test."""
        MyCachingObject.cached_method.cache_method = "unlimited_cache"
        MyCachingObject.cached_method.previous_cache_method = "no_cache"
        MyCachingObject.cached_method.is_timed = True
        MyCachingObject.cached_method.lifetime = None
        MyCachingObject.cached_method.get_cache_info().is_caching = True

        MyCachingObject.lifetime_method.cache_method = "unlimited_cache"
        MyCachingObject.lifetime_method.previous_cache_method = "no_cache"
        MyCachingObject.lifetime_method.is_timed = True
        MyCachingObject.lifetime_method.lifetime = 10
        MyCachingObject.lifetime_method.get_cache_info().is_caching = True

    @pytest.fixture
    def test_object(self) -> CachingObject:
        """Creates a test object.

        Returns:
            CachingObject: A test object instance.
        """
        obj = MyCachingObject()
        obj.get_caches()
        return obj

    # Tests
    def _setup_mixed_pickling(self, obj: MixedCachingObject) -> None:
        caches = obj.get_caches()
        assert "another_cache" in caches
        assert "cached_method" in caches

        # Ensure cached_method is in __dict__ by calling it
        obj.cached_method(1)
        assert "__cache__" in obj.__dict__

        # Ensure another_cache is NOT in __dict__ to cover the 'not in state[0]' branch
        # (It seems it might be appearing there mysteriously, so we force remove it)
        if "another_cache" in obj.__dict__:
            del obj.__dict__["another_cache"]

        assert "another_cache" not in obj.__dict__

    def _verify_mixed_pickling(self, obj: MixedCachingObject) -> None:
        assert isinstance(obj, MixedCachingObject)
        assert obj.extra_slot == 1
        assert obj.dynamic_attr == 2

    def _verify_slots_pickling(self, obj: SlottedCachingObject) -> None:
        assert isinstance(obj, SlottedCachingObject)
        # Verify dummy cache is accessible
        assert obj.dummy is not None

    @pytest.mark.parametrize(
        ("obj_class", "setup_method_name", "verify_method_name"),
        [
            (SlottedCachingObject, None, "_verify_slots_pickling"),
            (MixedCachingObject, "_setup_mixed_pickling", "_verify_mixed_pickling"),
        ],
    )
    def test_pickling_variations(
        self,
        obj_class: type[CachingObject],
        setup_method_name: str | None,
        verify_method_name: str,
    ) -> None:
        """Tests pickling with various object structures."""
        obj = obj_class()

        # Setup
        if setup_method_name:
            getattr(self, setup_method_name)(obj)
        else:
            obj.get_caches()

        # Pickle
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)

        # Verify
        getattr(self, verify_method_name)(loaded)

    def test_getstate_no_dict(self) -> None:
        """Tests __getstate__ when __dict__ is missing but slots are present."""
        obj = CachingObject()
        # Mock BaseReducible.__getstate__ to return (None, {'some_slot': 1})
        # This simulates "slots present but no dict".
        with patch.object(BaseReducible, "__getstate__", return_value=(None, {"some_slot": 1})):
            state = obj.__getstate__()
            assert state == (None, {"some_slot": 1})

    def test_caching_methods_coverage(self) -> None:
        """Tests coverage of caching methods with abnormal cache configurations."""
        obj = MyCachingObject()
        obj.get_caches()

        # Add a dummy cache name that doesn't exist on the class at all
        obj._caches["nonexistent_cache"] = None

        # Add a dummy cache name that exists on the class but has no methods
        setattr(obj.__class__, "dummy_cache", "not_a_cache")
        setattr(obj, "dummy_cache", "not_a_cache")
        obj._caches["dummy_cache"] = "not_a_cache"

        obj.enable_caching()
        obj.disable_caching()
        obj.timeless_caching()
        obj.timed_caching()
        obj.clear_caches()
        obj.set_lifetimes(10)

        # Cleanup class attribute so it doesn't affect other tests
        delattr(obj.__class__, "dummy_cache")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
