"""cachingtoolstestsuite.py
Specialized test suite for cache classes in the baseobjects package.

This module contains the specialized test suite for cache classes in the baseobjects package.
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
import time
from abc import abstractmethod
from collections.abc import Callable
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...cachingtools import BaseTimedCache
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class PicklableConcrete:
    """A picklable callable for testing."""

    def __init__(self) -> None:
        """Initializes the _TestFunc."""
        self.count = 0
        self.__name__ = "example_func"

    def __call__(self, x: int) -> int:
        """Calls the method.

        Returns:
            The result of x * 2.
        """
        self.count += 1
        return x * 2


class BaseCacheTestSuite(BaseObjectTestSuite):
    """Base test suite for cache classes.

    This class provides common test functionality for cache classes, including tests for caching, retrieval, and
    clearing. Subclasses should set the UnitTestClass attribute and may override or extend the test methods.

    Attributes:
        UnitTestClass: The cache class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[Any]

    # Helper Methods #
    def create_example_functions(self) -> tuple[Callable[..., Any], Callable[..., Any]]:
        """Creates a test function for testing caching behavior.

        Returns:
            A tuple containing:
            - A function that can be cached
            - A function that returns the number of times the cached function has been called
        """
        example = PicklableConcrete()

        def get_call_count() -> int:
            return example.count

        return example, get_call_count

    def create_test_caching_function(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[Any, Callable[..., Any], Callable[..., Any]]:
        """Creates a cache with a cached function for testing.

        Returns:
            A tuple containing:
            - A cache with a cached function
            - The cached function
            - A function that returns the number of times the cached function has been called
        """
        test_function, get_call_count = self.create_example_functions()
        return self.UnitTestClass(*args, func=test_function, **kwargs), test_function, get_call_count

    # Fixtures #
    @pytest.fixture
    def example_functions(self) -> tuple[Callable[..., Any], Callable[..., Any]]:
        """Creates a test function for testing caching behavior.

        Returns:
            A tuple containing:
            - A function that can be cached
            - A function that returns the number of times the cached function has been called
        """
        return self.create_example_functions()

    @pytest.fixture
    def caching_function(
        self,
        example_functions: tuple[Callable[..., Any], Callable[..., Any]],
    ) -> tuple[Any, Callable[..., Any], Callable[..., Any]]:
        """Creates a cache with a cached function for testing.

        Args:
            example_functions: A tuple containing a function to cache and a call counter.

        Returns:
            A tuple containing:
            - A cache with a cached function
            - The cached function
            - A function that returns the number of times the cached function has been called
        """
        test_function, get_call_count = example_functions
        return self.UnitTestClass(func=test_function), test_function, get_call_count

    @pytest.fixture
    def test_object(self, caching_function: tuple[Any, Callable[..., Any], Callable[..., Any]]) -> Any:
        """Creates a test object.

        Args:
            caching_function: A tuple containing a cache with a cached function and a call counter.

        Returns:
            A test object.
        """
        return caching_function[0]

    # Tests #
    # Instantiation #
    def test_instance_creation(
        self,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests that instances of the class can be created.

        This method can be overridden by subclasses to perform additional tests on the instance.

        Args:
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            instanced: Determines if the cache exists in the main function or in the method instances.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Creates Object
        caching_func, _, _ = self.create_test_caching_function(
            *args,
            lifetime=lifetime,
            typed=typed,
            call_method=call_method,
            instanced=instanced,
            **kwargs,
        )

        # Validate
        assert isinstance(caching_func, self.UnitTestClass)

    # Copying #
    def test_copy(self, test_object: Any) -> None:
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Cache Object
        cache_copy = copy.copy(test_object)

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is test_object.__func__
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__

    def test_copy_method(self, test_object: Any) -> None:
        """Tests the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Cache Object
        cache_copy = test_object.copy()

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is test_object.__func__
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__

    def test_deepcopy(self, test_object: Any, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        cache_copy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is test_object.__func__
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__

    def test_deepcopy_method(self, test_object: Any, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        cache_copy = test_object.deepcopy(memo=memo)

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is test_object.__func__
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Cache Object
        cache_copy = pickle.loads(pickle.dumps(test_object))

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is test_object.__func__
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__

    # Functionality #
    def test_no_cache(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests the no caching behavior.

        This test verifies that if no_cache is set, the wrapped function is called without caching.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        caching_func, _, get_call_count = self.create_test_caching_function(*args, **kwargs)
        caching_func.cache_method = "no_cache"

        # Calls the function multiple times with the same argument
        result1 = caching_func(2)
        result2 = caching_func(2)

        assert result1 == 4
        assert result2 == 4
        assert get_call_count() == 2  # The function should be called each time with no_cache

    def test_caching(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests the caching behavior of the cache class.

        This test verifies that the cache correctly caches function results and returns cached results on subsequent
        calls with the same arguments.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        caching_func, _, get_call_count = self.create_test_caching_function(*args, **kwargs)

        # Calls the function multiple times with the same argument
        result1 = caching_func(2)
        result2 = caching_func(2)

        # Verifies that the function returns the correct result
        assert result1 == 4
        assert result2 == 4

        # Verifies that the function was only called once
        assert get_call_count() == 1

        # Calls the function with a different argument
        result3 = caching_func(3)

        # Verifies that the function returns the correct result
        assert result3 == 6

        # Verifies that the function was called again
        assert get_call_count() == 2

    def test_cache_clearing(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests clearing the cache.

        This test verifies that the cache can be cleared and that subsequent calls to cached functions result in new
        function calls.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        caching_func, _, get_call_count = self.create_test_caching_function(*args, **kwargs)

        # Calls the function to cache the result
        result1 = caching_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Calls the function again with the same argument to verify caching
        result2 = caching_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Call count should not increase

        # Clear the cache
        caching_func.clear_cache()

        # Calls the function again with the same argument
        result3 = caching_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Call count should increase after clearing cache


class TimedCacheTestSuite(BaseCacheTestSuite):
    """Base test suite for timed cache classes.

    This class provides common test functionality for timed cache classes, including tests for cache expiration.
    Subclasses should set the UnitTestClass attribute and may override or extend the test methods.

    Attributes:
        UnitTestClass: The timed cache class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[BaseTimedCache]

    # Tests #
    # Instantiation #
    @pytest.mark.parametrize("typed", [None, True, False])
    @pytest.mark.parametrize("lifetime", [None, 1, 1.0])
    @pytest.mark.parametrize("call_method", [None, "call_caching"])
    @pytest.mark.parametrize("instanced", [None, True, False])
    def test_instance_creation(
        self,
        typed: bool | None,
        lifetime: int | float | None,
        call_method: str | None,
        instanced: bool | None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests that instances of the class can be created.

        This method can be overridden by subclasses to perform additional tests on the instance.

        Args:
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            instanced: Determines if the cache exists in the main function or in the method instances.
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Creates Object
        caching_func, _, _ = self.create_test_caching_function(
            *args,
            lifetime=lifetime,
            typed=typed,
            call_method=call_method,
            instanced=instanced,
            **kwargs,
        )

        # Validate
        assert isinstance(caching_func, self.UnitTestClass)
        assert caching_func.lifetime == lifetime

    # Copying #
    def test_copy(self, test_object: Any) -> None:
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Cache Object
        cache_copy = copy.copy(test_object)

        # Validate
        assert cache_copy is not test_object
        # For function wrappers, the func might be copied if it's an object, or shared if it's a function.
        # We just verify it's present and correct type.
        assert cache_copy.__func__ is not None
        assert type(cache_copy.__func__) is type(test_object.__func__)
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__
        assert cache_copy.is_timed == test_object.is_timed
        assert cache_copy.lifetime == test_object.lifetime
        assert cache_copy.expiration == test_object.expiration

    def test_copy_method(self, test_object: Any) -> None:
        """Tests the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Cache Object
        cache_copy = test_object.copy()

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is not None
        assert type(cache_copy.__func__) is type(test_object.__func__)
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__
        assert cache_copy.is_timed == test_object.is_timed
        assert cache_copy.lifetime == test_object.lifetime
        assert cache_copy.expiration == test_object.expiration

    def test_deepcopy(self, test_object: Any, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        cache_copy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is not None
        assert type(cache_copy.__func__) is type(test_object.__func__)
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__
        assert cache_copy.is_timed == test_object.is_timed
        assert cache_copy.lifetime == test_object.lifetime
        assert cache_copy.expiration == test_object.expiration

    def test_deepcopy_method(self, test_object: Any, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        cache_copy = test_object.deepcopy(memo=memo)

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is not None
        assert type(cache_copy.__func__) is type(test_object.__func__)
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__
        assert cache_copy.is_timed == test_object.is_timed
        assert cache_copy.lifetime == test_object.lifetime
        assert cache_copy.expiration == test_object.expiration

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Cache Object
        cache_copy = pickle.loads(pickle.dumps(test_object))

        # Validate
        assert cache_copy is not test_object
        assert cache_copy.__func__ is not None
        assert type(cache_copy.__func__) is type(test_object.__func__)
        assert cache_copy.clear_condition.__func__ is test_object.clear_condition.__func__
        assert cache_copy.is_timed == test_object.is_timed
        assert cache_copy.lifetime == test_object.lifetime
        assert cache_copy.expiration == test_object.expiration

    # Functionality #
    def test_cache_expiration(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests the expiration of cached items.

        This test verifies that cached items expire after the specified lifetime and that subsequent calls
        to cached functions result in new function calls.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        kwargs.setdefault("lifetime", 0.05)
        caching_func, _, get_call_count = self.create_test_caching_function(*args, **kwargs)

        # Calls the function to cache the result
        result1 = caching_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Calls the function again with the same argument to verify caching
        result2 = caching_func(2)
        assert result2 == 4
        assert get_call_count() == 1  # Call count should not increase

        # Waits for the cache to expire
        time.sleep(caching_func.lifetime + 0.1)

        # Calls the function again with the same argument
        result3 = caching_func(2)
        assert result3 == 4
        assert get_call_count() == 2  # Call count should increase after cache expiration

    def test_clear_condition(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests the clear condition of the cache.

        This test verifies that the cache correctly determines when to clear cached items based on their
        expiration time.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        kwargs.setdefault("lifetime", 1.0)
        caching_func, _, _get_call_count = self.create_test_caching_function(*args, **kwargs)

        # Verifies that clear_condition returns False when the cache is not expired
        caching_func.is_timed = True
        caching_func.expiration = time.perf_counter() + 2
        assert not caching_func.clear_condition()

        # Verifies that clear_condition returns True when the cache is expired
        caching_func.expiration = time.perf_counter() - 2
        assert caching_func.clear_condition()

        # Verifies that clear_condition returns False when is_timed is False
        caching_func.is_timed = False
        assert not caching_func.clear_condition()

        # Verifies that clear_condition returns False when lifetime is None
        caching_func.is_timed = True
        caching_func.lifetime = None
        assert not caching_func.clear_condition()

    @abstractmethod
    def test_pause_timer(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests pausing the cache timer.

        This test verifies that the cache timer can be paused and that cached items do not expire while
        the timer is paused.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        _caching_func, _, _get_call_count = self.create_test_caching_function(*args, **kwargs)

    @pytest.mark.parametrize("instanced", [True, False])
    def test_instanced_cache_property(self, instanced: bool, *args: Any, **kwargs: Any) -> None:
        """Tests the instanced_cache property.

        This test verifies that the instanced_cache property correctly gets and sets the instanced cache flag.
        """
        # Creates an instance directly or use helper
        # We need an instance of the class being tested.
        # create_test_caching_function creates a wrapper (TimedSingleCache usually)
        caching_func, _, _ = self.create_test_caching_function(*args, **kwargs)

        # Test with instanced_cache value
        caching_func.instanced_cache = instanced
        assert caching_func.instanced_cache is instanced

    @pytest.mark.parametrize("name", [None, "custom_name"])
    def test_bind_to_attribute(self, name: str | None, *args: Any, **kwargs: Any) -> None:
        """Tests bind_to_attribute with default and explicit names."""
        cache, _, _ = self.create_test_caching_function(*args, **kwargs)

        class A:
            pass

        a = A()
        cache.bind_to_attribute(instance=a, name=name)

        expected_name = name if name is not None else cache.__wrapped__.__name__
        assert hasattr(a, expected_name)

    @pytest.mark.parametrize("instanced", [True, False])
    def test_instanced_cache_setter(self, instanced: bool, *args: Any, **kwargs: Any) -> None:
        """Tests instanced_cache setter toggles binding mechanism."""
        cache, _, _ = self.create_test_caching_function(*args, **kwargs)
        cache.instanced_cache = instanced

        expected_binding = "bind_to_attribute" if instanced else "bind_builtin"
        assert cache.bind_multiplexer.selected == expected_binding, f"Failed: {cache.bind_multiplexer.selected} != {expected_binding}"
