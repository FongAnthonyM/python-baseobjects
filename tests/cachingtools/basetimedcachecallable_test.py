"""basetimedcachecallable_test.py
Tests for the BaseTimedCache class in the baseobjects package.
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
import copy
import pickle
from collections.abc import Callable
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools.caches.basetimedcache import (
    BaseTimedCache,
    CacheInfo,
    CacheItem,
    _HashedSeq,
)


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers."""
    return x + y


# Helper Classes #
class ConcreteTimedCacheCallable(BaseTimedCache):
    """A concrete implementation of BaseTimedCache for testing."""

    def __init__(
        self,
        func: Callable[..., Any] | None = None,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the timed cache callable."""
        super().__init__(
            func=func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            instanced=instanced,
            *args,
            init=init,
            **kwargs,
        )

        if call_method is None:
            self.cache_method = "cache_dict"

    def clear_cache(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clear the cache."""
        if cache_info is None:
            # Check if we should get instance cache or global cache
            instance = args[0] if args else None
            if instance is not None:
                cache_info = self.get_instance_cache_info(instance)
            else:
                cache_info = self.get_cache_info()

        super().clear_cache(*args, cache_info=cache_info, **kwargs)
        cache_info.cache_container = {}

    def cache_dict(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> Any:
        """Cache the result in a dictionary."""
        instance = args[0]
        original_args = args[1:]

        if cache_info is None:
            if instance is not None:
                cache_info = self.get_instance_cache_info(instance)
            else:
                cache_info = self.get_cache_info()

        key = self.create_key(original_args, kwargs, cache_info.typed or False)

        if key in cache_info.cache_container:
            return cache_info.cache_container[key]

        if instance is not None:
            result = self.call_wrapped(instance, *original_args, **kwargs)
        else:
            result = self.call_wrapped(*original_args, **kwargs)

        cache_info.cache_container[key] = result
        return result


class TestBaseTimedCacheCallable:
    """Tests the BaseTimedCache class."""

    UnitTestClass = ConcreteTimedCacheCallable

    def test_basic_caching(self):
        """Tests basic caching functionality of the concrete class."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = self.UnitTestClass(func=func)
        assert cache(1) == 1
        assert count[0] == 1
        assert cache(1) == 1
        assert count[0] == 1
        assert cache(2) == 2
        assert count[0] == 2

    def test_no_cache(self):
        """Tests that no_cache works when caching is disabled."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = self.UnitTestClass(func=func)
        cache.disable_caching()
        assert cache(1) == 1
        assert count[0] == 1
        assert cache(1) == 1
        assert count[0] == 2

    def test_clear_cache(self):
        """Tests clear_cache."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = self.UnitTestClass(func=func)
        assert cache(1) == 1
        cache.clear_cache()
        assert cache(1) == 1
        assert count[0] == 2

    def test_copy(self):
        """Tests copying the cache object."""
        cache = self.UnitTestClass(func=add_function)
        cache_copy = copy.copy(cache)
        assert cache_copy is not cache
        assert cache_copy.__wrapped__ == cache.__wrapped__
        assert cache_copy(1, 2) == 3

    def test_pickling(self):
        """Tests pickling the cache object."""
        # Use top-level function for pickling
        cache = self.UnitTestClass(func=add_function)
        pickled = pickle.dumps(cache)
        unpickled = pickle.loads(pickled)
        assert unpickled(1, 2) == 3

    def test_cache_control_methods(self):
        """Tests cache control methods existence and basic call."""
        cache = self.UnitTestClass(func=add_function)
        cache.enable_caching()
        cache.disable_caching()
        cache.clear_cache()
        # Ensure they don't crash

    def test_hashed_seq(self):
        """Tests _HashedSeq helper."""
        h1 = _HashedSeq((1, 2))
        h2 = _HashedSeq((1, 2))
        assert h1 == h2
        assert hash(h1) == hash(h2)


class TestCacheItem:
    """Test the CacheItem class."""

    def test_init(self) -> None:
        """Test initialization of CacheItem."""
        item = CacheItem(key="key", result="result", priority_link="link")
        assert item.key == "key"
        assert item.result == "result"
        assert item.priority_link == "link"


if __name__ == "__main__":
    # Third-Party Packages #
    import pytest
    pytest.main(["-v", "-s"])
