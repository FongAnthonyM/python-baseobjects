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

        obj = MyCachingObject()
        obj.get_caches()
        return obj

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
        assert isinstance(caches["cached_method"], TimedCache)

    def test_is_caching_property(self, test_object: CachingObject) -> None:
        """Tests the is_caching property and new state methods."""
        assert test_object._is_caching is True
        assert test_object.get_any_caching() is True
        assert test_object.any_caching is True
        assert test_object.all_caches_active is True
        assert test_object.any_caches_timed is True
        assert test_object.all_caches_timed is True

        test_object.disable_caching()
        assert test_object._is_caching is False
        assert test_object.any_caching is False  # global toggle off
        assert test_object.all_caches_active is False

        test_object.stop_caching(caches=True)
        assert test_object.any_caching is False
        assert test_object.all_caches_active is False

        # Verifies caching is actually disabled
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 2  # type: ignore[attr-defined]

        test_object.enable_caching()
        assert test_object._is_caching is True
        assert test_object.any_caching is True

    def test_timed_state_methods(self, test_object: CachingObject) -> None:
        """Tests any_cache_timed and all_caches_timed."""
        test_object.timeless_caching()
        assert test_object.any_caches_timed is False
        assert test_object.all_caches_timed is False

        test_object.timed_caching(exclude={"lifetime_method"})
        assert test_object.any_caches_timed is True
        assert test_object.all_caches_timed is False

        # Verifies caching is enabled
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]

    def test_clear_caches(self, test_object: CachingObject) -> None:
        """Tests clearing all caches."""
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]

        # Calls again, should use cache
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]

        # Clear caches
        test_object.clear_caches(caches=True)

        # Calls again, should re-execute
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 2  # type: ignore[attr-defined]

    def test_clear_caches_exclude(self, test_object: CachingObject) -> None:
        """Tests clearing caches with exclusion."""
        test_object.cached_method(1)  # type: ignore[attr-defined]
        test_object.lifetime_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 1  # type: ignore[attr-defined]

        test_object.clear_caches(exclude={"lifetime_method"}, caches=True)

        # cached_method should be cleared (counter increments)
        test_object.cached_method(1)  # type: ignore[attr-defined]
        assert test_object.counter == 2  # type: ignore[attr-defined]

    def test_is_caching_idempotent(self, test_object: CachingObject) -> None:
        """Tests setting is_caching to the same value."""
        assert test_object._is_caching is True
        test_object.enable_caching()
        assert test_object._is_caching is True

        test_object.disable_caching()
        assert test_object._is_caching is False
        test_object.disable_caching()
        assert test_object._is_caching is False

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
        test_object.stop_caching(exclude={"cached_method"}, caches=True)

        # cached_method should still cache
        test_object.cached_method(1)
        assert test_object.counter == 1
        test_object.cached_method(1)
        assert test_object.counter == 1

        # Checks internal state of lifetime_method
        assert test_object.cached_method.get_cache_info(test_object).is_caching is True
        assert test_object.lifetime_method.get_cache_info(test_object).cache_method == "no_cache"

        # Enable caching, excluding lifetime_method
        test_object.resume_caching(exclude={"lifetime_method"}, caches=True)

        assert test_object.cached_method.get_cache_info(test_object).cache_method != "no_cache"
        assert test_object.lifetime_method.get_cache_info(test_object).cache_method == "no_cache"

    def test_set_lifetimes_args(self, test_object: Any) -> None:
        """Tests setting lifetimes of caches."""
        test_object.set_lifetimes(100, exclude={"lifetime_method"}, caches=True)
        assert test_object.cached_method.get_cache_info(test_object).lifetime == 100
        assert test_object.lifetime_method.get_cache_info(test_object).lifetime == 10  # Original value

    def test_timeless_and_timed_caching_args(self, test_object: Any) -> None:
        """Tests timeless and timed caching toggle."""
        test_object.timeless_caching(exclude={"lifetime_method"}, caches=True)
        assert test_object.cached_method.get_cache_info(test_object).is_timed is False
        assert test_object.lifetime_method.get_cache_info(test_object).is_timed is True

        test_object.timed_caching(exclude={"lifetime_method"}, caches=True)
        assert test_object.cached_method.get_cache_info(test_object).is_timed is True
        assert test_object.lifetime_method.get_cache_info(test_object).is_timed is True

    def test_clear_caches_all(self, test_object: Any) -> None:
        """Tests clearing all caches without exclusion."""
        test_object.cached_method(1)
        test_object.clear_caches(caches=True)
        test_object.cached_method(1)
        assert test_object.counter == 2

    def test_timeless_and_timed_caching_all(self, test_object: Any) -> None:
        """Tests timeless and timed caching on all caches."""
        test_object.timeless_caching(caches=True)
        assert test_object.any_caches_timed is False

        test_object.timed_caching(caches=True)
        assert test_object.all_caches_timed is True

    def test_set_lifetimes_all(self, test_object: Any) -> None:
        """Tests setting lifetimes of all caches."""
        test_object.set_lifetimes(50, caches=True)
        assert test_object.cached_method.get_cache_info(test_object).lifetime == 50
        assert test_object.lifetime_method.get_cache_info(test_object).lifetime == 50

    def test_defaults(self, test_object: Any) -> None:
        """Tests default arguments (caches=False, exclude=None)."""
        # Ensure caches are discovered first
        test_object.get_caches()

        # clear_caches
        test_object.cached_method(1)
        test_object.clear_caches()
        test_object.cached_method(1)
        assert test_object.counter == 2

        # disable_caching -> stop_caching
        test_object.stop_caching()
        assert test_object.any_caching is False  # global toggle off
        test_object.cached_method(1)
        assert test_object.counter == 3  # global toggle off, so it doesn't cache

        # resume_caching
        test_object.resume_caching()
        test_object.cached_method(1)
        assert test_object.counter == 3  # back to caching, uses value from call 2

        # enable_caching(caches=True) -> resume_caching(caches=True)
        test_object.resume_caching(caches=True)
        test_object.cached_method(1)
        assert test_object.counter == 3  # back to caching

        # stop_caching / resume_caching
        test_object.stop_caching()
        assert test_object.any_caching is False  # global toggle off
        test_object.cached_method(1)
        assert test_object.counter == 4  # counter was 3, +1 = 4

        test_object.resume_caching()
        assert test_object.any_caching is True
        test_object.cached_method(1)
        assert test_object.counter == 4  # cached

        # timeless_caching
        test_object.timeless_caching()
        assert test_object.any_caches_timed is False

        # timed_caching
        test_object.timed_caching()
        assert test_object.any_caches_timed is True

        # set_lifetimes
        test_object.set_lifetimes(33)
        assert test_object.cached_method.get_cache_info(test_object).lifetime == 33
