#!/usr/bin/env python
"""timedcache_test.py
Test for the TimedCache class.
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
from collections.abc import Callable
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools.caches.timedcache import TimedCache
from baseobjects.testsuite.cachingtools import TimedCacheTestSuite


# Definitions #
# Classes #
class TestTimedCache(TimedCacheTestSuite):
    """Test the TimedCache class.

    This class tests the functionality of the TimedCache class, utilizing the TimedCacheTestSuite.
    """

    # Attributes #
    UnitTestClass = TimedCache

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize("maxsize", [2, 0])
    def test_maxsize_behavior(
        self,
        maxsize: int,
        example_functions: tuple[Callable[..., Any], Callable[[], int]],
    ) -> None:
        """Tests the maxsize behavior of TimedCache."""
        test_function, get_call_count = example_functions
        cache = self.UnitTestClass(func=test_function, maxsize=maxsize)

        calls_made = 0

        # 1. First call
        assert cache(1) == 2
        calls_made += 1
        assert get_call_count() == calls_made

        if maxsize > 0:
            assert len(cache) == 1
            # 2. Second call same arg -> HIT
            assert cache(1) == 2
            assert get_call_count() == calls_made  # No increment
        else:
            assert len(cache) == 0
            # 2. Second call same arg -> MISS
            assert cache(1) == 2
            calls_made += 1
            assert get_call_count() == calls_made

        # If maxsize is 2, fill it
        if maxsize == 2:
            # Add second item
            assert cache(2) == 4
            calls_made += 1
            assert len(cache) == 2

            # Add third item (overflow)
            assert cache(3) == 6
            calls_made += 1
            assert len(cache) == 2

            # Check overflow item is not cached
            assert cache(3) == 6
            calls_made += 1
            assert get_call_count() == calls_made

            # Check first item is still cached
            assert cache(1) == 2
            assert get_call_count() == calls_made  # Unchanged

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        # Provide func so we get an instance, but init=False prevents construction
        cache = self.UnitTestClass(func=lambda x: x, init=False)
        assert isinstance(cache, self.UnitTestClass)
        # construct was skipped, so no maxsize in __dict__?
        # Use __dict__ check to avoid class attributes or properties masking
        assert "_maxsize" not in cache.__dict__

        # Manually construct
        cache.construct(func=lambda x: x)
        assert cache(1) == 1

    def test_bind_explicit(self) -> None:
        """Tests bind method explicitly."""
        cache = self.UnitTestClass(func=lambda: None)

        class Target:
            pass

        instance = Target()
        bound = cache.bind(instance=instance, owner=Target)
        assert bound is not None

    def test_set_maxsize_none(self) -> None:
        """Tests setting maxsize to None (unlimited)."""
        cache = self.UnitTestClass(func=lambda x: x, maxsize=10)
        assert cache._maxsize == 10
        cache.maxsize = None
        assert cache._maxsize is None
        assert cache.cache_method == "unlimited_cache"  # type: ignore[unreachable]

    def test_poll(self) -> None:
        """Tests poll method."""
        cache = self.UnitTestClass(func=lambda x: x, maxsize=1)
        assert cache.poll() is True
        cache(1)
        assert cache.poll() is False

        cache.maxsize = None
        # poll returns False if maxsize is None?
        # Code: return self._maxsize is not None and len < self._maxsize
        assert cache.poll() is False

    def test_method_binding(self) -> None:
        """Tests method binding behavior."""

        class A:
            def __init__(self) -> None:
                self.val = 10

            @TimedCache(instanced=True)
            def method(self, x: int) -> int:
                return self.val + x

        a = A()
        b = A()

        assert a.method(1) == 11
        assert b.method(1) == 11

        a.val = 20
        # If cached, it might return 11?
        # But wait, TimedCache usually caches based on arguments.
        # If 'self' is part of the key or if instanced cache is separate.
        # instanced=True means cache is stored on instance 'a'.

        # Calling method(1) again on 'a' should use cache.
        assert a.method(1) == 11

        # 'b' should be independent.
        b.val = 30
        assert b.method(1) == 11  # cached for b

    def test_pause_timer(self) -> None:
        """Tests pausing the timer (abstract in suite, needs implementation if supported)."""


class PickleTestClass:
    """A helper class for testing pickling of TimedCache methods."""

    def __init__(self) -> None:
        """Initializes the test class with a value."""
        self.value = 1

    @TimedCache(instanced=True)
    def method(self) -> int:
        """A method decorated with TimedCache.

        Returns:
            int: The value.
        """
        return self.value


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
