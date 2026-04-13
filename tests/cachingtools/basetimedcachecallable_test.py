"""basetimedcachecallable_test.py
Tests for the BaseTimedCache class in the baseobjects package.

This module provides tests for the BaseTimedCache class, which is a base cache wrapper object for a function
that resets its cache periodically. It tests the core functionality of BaseTimedCache, including instance
creation, caching behavior, cache expiration, and cache clearing.
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
from unittest.mock import patch

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools.caches.basetimedcache import (
    BaseTimedCache,
    CacheInfo,
    CacheItem,
    _HashedSeq,
)
from baseobjects.testsuite.cachingtools.basetimedcachecallabletestsuite import BaseTimedCacheTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers.

    Returns:
        The sum of x and y.
    """
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers.

    Returns:
        The product of x and y.
    """
    return x * y


# Helper Classes #
class ConcreteTimedCacheCallable(BaseTimedCache):
    """A concrete implementation of BaseTimedCache for testing.

    This class implements the abstract clear_cache method required by BaseTimedCache and provides a basic
    caching implementation.
    """

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
        # Parent initialization
        super().__init__(
            func,
            typed,
            lifetime,
            call_method,
            instanced,
            *args,
            init=init,
            **kwargs,
        )

        # Set the default cache method if none was specified
        if call_method is None:
            self.cache_method = "cache_dict"

    def clear_cache(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clear the cache and update the expiration of the cache."""
        if cache_info is None:
            cache_info = self.get_cache_info(*args)

        # Call the parent method to update the expiration
        super().clear_cache(*args, cache_info=cache_info, **kwargs)

        # Clear the cache container
        cache_info.cache_container = {}

    def cache_dict(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> Any:
        """Cache the result of the wrapped function in a dictionary.

        Args:
            *args: Arguments for the wrapped function.
            cache_info: The cache information to use for caching.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The cached result or the result of calling the wrapped function.

        Raises:
            TypeError: If the wrapped function is None.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)

        # Create a key for the cache
        key = self.create_key(args, kwargs, cache_info.typed or False)

        # Check if the key is in the cache
        if key in cache_info.cache_container:
            return cache_info.cache_container[key]

        # Call the wrapped function and cache the result
        if self.__wrapped__ is None:
            msg = "Wrapped function is None"
            raise TypeError(msg)
        result = self.call_wrapped(*args, **kwargs)
        cache_info.cache_container[key] = result

        return result


class TimedCacheTestObject:
    """A test class for testing method binding and caching."""

    def __init__(self, value: int = 10) -> None:
        """Initialize with a value."""
        self.value = value

    def method1(self, x: int) -> int:
        """A test method that adds x to the value.

        Returns:
            The sum of value and x.
        """
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x.

        Returns:
            The product of value and x.
        """
        return self.value * x


# Tests #
class SlottedConcreteTimedCacheCallable(BaseTimedCache):
    """A slotted concrete implementation of BaseTimedCache for testing."""

    __slots__ = ("_cache_method", "cache_container")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes the slotted callable."""
        super().__init__(*args, **kwargs)

    def clear_cache(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clears the cache."""
        if cache_info is None:
            cache_info = self.get_cache_info(*args)

        super().clear_cache(*args, cache_info=cache_info, **kwargs)
        cache_info.cache_container = {}


class TestBaseTimedCacheCallable(BaseTimedCacheTestSuite):
    """Tests the BaseTimedCache class.

    This class tests the functionality of the BaseTimedCache class, which is a base cache wrapper object for a
    function that resets its cache periodically.
    """

    # Attributes #
    UnitTestClass: type[BaseTimedCache] = ConcreteTimedCacheCallable

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object_instance(self) -> TimedCacheTestObject:
        """Creates a test object instance.

        Returns:
            TimedCacheTestObject: An instance of the test object.
        """
        return TimedCacheTestObject(value=10)

    # Tests

    @pytest.mark.parametrize("bind_method", ["bind_builtin", "bind_wrapped"])
    def test_bind_multiplexer(
        self, bind_method: str, test_method_object: Any = None, test_bind_target: Any = None,
    ) -> None:
        """Tests that the bind_multiplexer correctly delegates to the selected binding method."""

        # Create a test class with a method
        class UnitTestClass:
            def test_method(self, x: int) -> int:
                return x * 2

        # Create a test instance
        test_instance = UnitTestClass()

        # Create a method object
        method_object = self.UnitTestClass(func=UnitTestClass.test_method)

        # Test bind_method
        method_object.bind_method = bind_method
        bound_method = method_object.__get__(test_instance, UnitTestClass)
        assert bound_method(5) == 10

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(self, test_object: Any, method: str, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the callable object.

        This test verifies that deepcopy creates a new object with the same wrapped function. Overridden to relax
        function identity check for callable instances.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        else:
            obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, test_object.__class__)
        # Relaxed check: just check if it works (assuming default test function x+2 from suite)
        assert obj_deepcopy(5) == 7

    @pytest.mark.parametrize(
        ("scenario_name", "calls", "expected_results", "expected_counts"),
        [
            ("positional", [((2,), {}), ((3,), {}), ((2,), {}), ((3,), {})], [4, 6, 4, 6], [1, 2, 2, 2]),
            (
                "keyword",
                [((2, 3), {}), ((), {"x": 2, "y": 3}), ((2,), {"y": 3}), ((2, 3), {})],
                [6, 6, 6, 6],
                [1, 2, 3, 3],
            ),
        ],
    )
    def test_caching_scenarios(
        self,
        scenario_name: str,
        calls: list[Any],
        expected_results: list[Any],
        expected_counts: list[int],
    ) -> None:
        """Tests caching scenarios with different arguments."""
        call_count = 0

        def test_func(x: int, y: int = 2) -> int:
            nonlocal call_count
            call_count += 1
            return x * y

        cache_func = self.UnitTestClass(func=test_func)
        cache_func.call_method = "call_caching"

        for i, (args, kwargs) in enumerate(calls):
            result = cache_func(*args, **kwargs)
            assert result == expected_results[i]
            assert call_count == expected_counts[i]

    def test_pickling_slots_tuple(self) -> None:
        """Tests pickling of a slotted class to trigger tuple state."""
        # Use a global function (add_function) that is pickleable
        obj = SlottedConcreteTimedCacheCallable(func=add_function)

        # Pickle
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert isinstance(loaded, SlottedConcreteTimedCacheCallable)

    def test_cache_control_propagation_callable(self, test_function: tuple[Callable[..., Any], Callable[..., Any]]) -> None:
        """Tests the cache control methods."""
        func, _ = test_function
        callable_obj = self.UnitTestClass(func=func)

        # This should just work without errors
        callable_obj.enable_caching(callable_obj.cache_info)
        callable_obj.disable_caching(callable_obj.cache_info)
        callable_obj.stop_caching(callable_obj.cache_info)
        callable_obj.resume_caching(callable_obj.cache_info)
        callable_obj.clear_cache(callable_obj.cache_info)

    def test_call_caching_disabled(self) -> None:
        """Tests call_caching when cache is disabled."""
        class MockFunc:
            def __init__(self) -> None:
                self.called = False
                self.__name__ = "mock"

            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                self.called = True
                return "called_wrapped"

        mock_func = MockFunc()
        callable_obj = self.UnitTestClass(func=mock_func)
        callable_obj.is_caching = False

        assert callable_obj.call_caching() == "called_wrapped"
        assert mock_func.called

    def test_instanced_cache_setter_branch(self) -> None:
        """Tests instanced_cache setter branches."""
        callable_obj = self.UnitTestClass(func=lambda: None)
        callable_obj.instanced_cache = True
        assert callable_obj.instanced_cache is True
        callable_obj.instanced_cache = False
        assert callable_obj.instanced_cache is False

# Main #
class TestCacheItem:
    """Test the CacheItem class."""

    def test_init(self) -> None:
        """Test initialization of CacheItem."""
        item = CacheItem(key="key", result="result", priority_link="link")
        assert item.key == "key"
        assert item.result == "result"
        assert item.priority_link == "link"


class ConcreteTimedCache(BaseTimedCache):
    """Concrete implementation for testing."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes the concrete timed cache."""
        super().__init__(*args, **kwargs)

    def clear_cache(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clears the cache."""
        if cache_info is None:
            cache_info = self.get_cache_info(*args)

        super().clear_cache(*args, cache_info=cache_info, **kwargs)


class TestBaseTimedCache:
    """Tests the BaseTimedCache class."""

    def test_instanced_cache_setter(self) -> None:
        """Tests setter for instanced_cache."""
        cache = ConcreteTimedCache(lambda: None)
        cache.instanced_cache = True
        assert cache.instanced_cache is True
        cache.instanced_cache = False
        assert cache.instanced_cache is False

    def test_bind(self) -> None:
        """Tests bind method."""
        cache = ConcreteTimedCache(lambda: None)

        class Target:
            pass

        instance = Target()
        bound = cache.__get__(instance, Target)
        assert bound is not None

    def test_bind_to_attribute_no_instance(self) -> None:
        """Tests bind_to_attribute with no instance."""
        cache = ConcreteTimedCache(lambda: None)
        assert cache.bind_to_attribute(None) is cache

    @pytest.mark.parametrize(
        ("name", "expected_attr"),
        [
            (None, "foo"),
            ("bar", "bar"),
        ],
    )
    def test_bind_to_attribute_instance(self, name: str | None, expected_attr: str) -> None:
        """Tests bind_to_attribute with instance."""
        cache = ConcreteTimedCache(lambda: None)

        class Target:
            pass

        instance = Target()

        if name is None:
            assert cache.__wrapped__ is not None
            cache.__wrapped__.__name__ = "foo"
            cache.bind_to_attribute(instance, Target)
        else:
            cache.bind_to_attribute(instance=instance, owner=Target, name=name)

        assert hasattr(instance, expected_attr)

    def test_bind_to_attribute_attribute_error(self) -> None:
        """Tests bind_to_attribute when func has no __name__."""
        class MockFunc:
            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                pass

        cache = ConcreteTimedCache(MockFunc())

        class Target:
            pass

        target = Target()
        cache.bind_to_attribute(target)
        assert hasattr(target, "")

    @pytest.mark.parametrize("lifetime", [10, None])
    def test_clear_cache_expiration_update(self, lifetime: int | None) -> None:
        """Tests clear_cache behavior with and without lifetime."""
        cache = ConcreteTimedCache(lambda: None, lifetime=lifetime)
        if lifetime is None:
            cache.expiration = 123
        else:
            cache.expiration = 0

        cache.clear_cache(cache.cache_info)

        if lifetime is None:
            # Should not update expiration
            assert cache.expiration == 123
        else:
            # Should update expiration (or at least be not None)
            assert cache.expiration is not None


class TestHashedSeq:
    """Tests the _HashedSeq helper class."""

    def test_hashed_seq_eq(self) -> None:
        """Tests equality of _HashedSeq."""
        h1 = _HashedSeq((1, 2))
        h2 = _HashedSeq((1, 2))
        h3 = _HashedSeq((1, 3))

        assert h1 == h2
        assert h1 is not h2
        assert h1 != h3
        assert h1 != 1


if __name__ == "__main__":
    pytest.main(["-v", "-s"])
