"""cachingobjecttestsuite.py
Test suite for the CachingObject class.

This module contains the test suite for the CachingObject class.
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

# Third-Party Packages #
import pytest

# Local Packages #
from ...cachingtools.caches.timedcache import TimedCache
from ...cachingtools.cachingobject import CachingObject
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class CachingObjectTestSuite(BaseObjectTestSuite):
    """Base test suite for CachingObject classes.

    This class provides common test functionality for objects that use caching mechanisms.
    """

    # Attributes #
    UnitTestClass: type[CachingObject] = CachingObject

    # Fixtures #
    @pytest.fixture
    def test_object(self) -> CachingObject:
        """Creates a test object.

        Returns:
            CachingObject: A test object instance.
        """

        class MyCachingObject(self.UnitTestClass):  # type: ignore[misc, name-defined]
            def __init__(self) -> None:
                super().__init__()
                self.counter = 0

            @TimedCache(instanced=True)
            def cached_method(self, x: int) -> int:
                self.counter += 1
                return x + 1

            @TimedCache(lifetime=10, instanced=True)
            def lifetime_method(self, x: Any) -> Any:
                return x

        return MyCachingObject()

    # Tests #
    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling of CachingObject."""
        test_object.cached_method(1)
        assert test_object.counter == 1

        # Pickle and unpickle
        dump = pickle.dumps(test_object)
        loaded = pickle.loads(dump)

        assert loaded is not test_object
        assert loaded.counter == 1

        # Verifies caching still works on loaded object
        loaded.cached_method(1)
        # CachingObject clears caches on pickle, so cache is empty and method executes again.
        assert loaded.counter == 2

        # Verifies method calls on new object don't affect old object
        loaded.cached_method(2)
        assert loaded.counter == 3
        assert test_object.counter == 1

    # Functionality #
    def test_get_caches(self, test_object: CachingObject) -> None:
        """Tests retrieving caches from the object."""
        caches = test_object.get_caches()
        assert "cached_method" in caches
        assert "lifetime_method" in caches
        assert isinstance(vars(type(test_object))["cached_method"], TimedCache)

    def test_is_cache_property(self, test_object: CachingObject) -> None:
        """Tests the is_cache property."""
        assert test_object.is_cache is True

        test_object.is_cache = False
        assert test_object.is_cache is False

        # Verifies caching is actually disabled
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 2  # type: ignore[attr-defined]

        test_object.is_cache = True
        assert test_object.is_cache is True

        # Verifies caching is enabled
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 3  # type: ignore[attr-defined]
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 3  # type: ignore[attr-defined]

    def test_clear_caches(self, test_object: CachingObject) -> None:
        """Tests clearing all caches."""
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]

        # Calls again, should use cache
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]

        # Clear caches
        test_object.clear_caches(get_caches=True)

        # Calls again, should re-execute
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 2  # type: ignore[attr-defined]

    def test_clear_caches_exclude(self, test_object: CachingObject) -> None:
        """Tests clearing caches with exclusion."""
        test_object.cached_method(1)  # type: ignore[attr-defined]
        test_object.lifetime_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]

        test_object.clear_caches(exclude={"lifetime_method"}, get_caches=True)

        # cached_method should be cleared (counter increments)
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 2  # type: ignore[attr-defined]

    def test_is_cache_idempotent(self, test_object: CachingObject) -> None:
        """Tests setting is_cache to the same value."""
        assert test_object.is_cache is True
        test_object.is_cache = True
        assert test_object.is_cache is True

        test_object.is_cache = False
        assert test_object.is_cache is False
        test_object.is_cache = False
        assert test_object.is_cache is False

    def test_dynamic_cache(self, test_object: Any) -> None:
        """Tests adding a cache dynamically to the instance."""
        # Adds a cache to the instance, not the class
        cache = TimedCache(lambda x: x)
        test_object.dynamic_cache = cache

        # This relies on get_caches finding it in dir(obj)
        caches = test_object.get_caches()
        assert "dynamic_cache" in caches
        assert "cached_method" in caches

    def test_disable_enable_caching_args(self, test_object: Any) -> None:
        """Tests disabling and enabling caching with arguments."""
        # Disable caching, excluding cached_method
        test_object.disable_caching(exclude={"cached_method"}, get_caches=True)

        # cached_method should still cache
        test_object.cached_method(1)
        assert test_object.counter == 1
        test_object.cached_method(1)
        assert test_object.counter == 1

        # Checks internal state of lifetime_method
        assert test_object.cached_method.cache_method != "no_cache"
        assert test_object.lifetime_method.cache_method == "no_cache"

        # Enable caching, excluding lifetime_method
        test_object.enable_caching(exclude={"lifetime_method"}, get_caches=True)

        assert test_object.cached_method.cache_method != "no_cache"
        assert test_object.lifetime_method.cache_method == "no_cache"

    def test_set_lifetimes_args(self, test_object: Any) -> None:
        """Tests setting lifetimes of caches."""
        test_object.set_lifetimes(100, exclude={"lifetime_method"}, get_caches=True)
        assert test_object.cached_method.lifetime == 100
        assert test_object.lifetime_method.lifetime == 10  # Original value

    def test_timeless_and_timed_caching_args(self, test_object: Any) -> None:
        """Tests timeless and timed caching toggle."""
        test_object.timeless_caching(exclude={"lifetime_method"}, get_caches=True)
        assert test_object.cached_method.is_timed is False
        assert test_object.lifetime_method.is_timed is True

        test_object.timed_caching(exclude={"cached_method"}, get_caches=True)
        assert test_object.cached_method.is_timed is False
        assert test_object.lifetime_method.is_timed is True

    def test_clear_caches_all(self, test_object: Any) -> None:
        """Tests clearing all caches without exclusion."""
        test_object.cached_method(1)
        test_object.clear_caches(get_caches=True)
        test_object.cached_method(1)
        assert test_object.counter == 2

    def test_timeless_and_timed_caching_all(self, test_object: Any) -> None:
        """Tests timeless and timed caching on all caches."""
        test_object.timeless_caching(get_caches=True)
        assert test_object.cached_method.is_timed is False
        assert test_object.lifetime_method.is_timed is False

        test_object.timed_caching(get_caches=True)
        assert test_object.cached_method.is_timed is True
        assert test_object.lifetime_method.is_timed is True  # type: ignore[unreachable]

    def test_set_lifetimes_all(self, test_object: Any) -> None:
        """Tests setting lifetimes of all caches."""
        test_object.set_lifetimes(50, get_caches=True)
        assert test_object.cached_method.lifetime == 50
        assert test_object.lifetime_method.lifetime == 50

    def test_defaults(self, test_object: Any) -> None:
        """Tests default arguments (get_caches=False, exclude=None)."""
        # Ensure caches are discovered first
        test_object.get_caches()

        # clear_caches
        test_object.cached_method(1)
        test_object.clear_caches()
        test_object.cached_method(1)
        assert test_object.counter == 2

        # disable_caching
        test_object.disable_caching()
        test_object.cached_method(1)
        assert test_object.counter == 3

        # enable_caching
        test_object.enable_caching()
        # Cache was not updated while disabled, so it uses the old cached value
        test_object.cached_method(1)
        assert test_object.counter == 3

        # timeless_caching
        test_object.timeless_caching()
        assert test_object.cached_method.is_timed is False

        # timed_caching
        test_object.timed_caching()
        assert test_object.cached_method.is_timed is True

        # set_lifetimes
        test_object.set_lifetimes(33)  # type: ignore[unreachable]
        assert test_object.cached_method.lifetime == 33
