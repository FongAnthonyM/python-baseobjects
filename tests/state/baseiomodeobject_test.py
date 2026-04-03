"""baseiomodeobject_test.py
Unit tests for the BaseIOModeObject class and staterestriction decorator.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2026, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from enum import StrEnum
from typing import Any, Self

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools import CachingObject, timed_keyless_cache
from baseobjects.state.baseiomodeobject import BaseIOModeObject, asopen, asopenasync, staterestriction
from baseobjects.testsuite.state.baseiomodeobjecttestsuite import (
    AsOpenAsyncTestSuite,
    AsOpenTestSuite,
    BaseIOModeObjectTestSuite,
    StateRestrictionTestSuite,
)


# Definitions #
# Classes #
class MockModes(StrEnum):
    """Mock modes for testing."""
    READ = "r"
    WRITE = "w"


class MockIOModeObject(BaseIOModeObject):
    """A mock I/O mode object for testing."""
    _valid_modes: type[StrEnum] = MockModes

    def __init__(self, mode: str = MockModes.READ) -> None:
        """Initializes the mock object."""
        self._mode = MockModes(mode)

    def open(self, *args: Any, **kwargs: Any) -> Self:
        """Opens the object.

        Returns:
            The opened object.
        """
        super().open(*args, **kwargs)
        return self

    def close(self) -> None:
        """Closes the object."""
        super().close()


class AsyncMockIOModeObject(MockIOModeObject):
    """An async mock I/O mode object for testing."""

    async def open_async(self, *args: Any, **kwargs: Any) -> Self:
        """Asynchronously opens the object.

        Returns:
            The opened object.
        """
        self._is_open = True
        return self

    async def close_async(self, *args: Any, **kwargs: Any) -> None:
        """Asynchronously closes the object."""
        self._is_open = False


class TestBaseIOModeObject(BaseIOModeObjectTestSuite):
    """Unit tests for the BaseIOModeObject class."""
    UnitTestClass: type[BaseIOModeObject] = MockIOModeObject

    @pytest.fixture
    def test_object(self) -> MockIOModeObject:
        """A fixture providing a MockIOModeObject instance.

        Returns:
            A MockIOModeObject instance.
        """
        return MockIOModeObject()

    def test_open_async_not_implemented(self, test_object: MockIOModeObject) -> None:
        """Tests that open_async raises NotImplementedError by default."""
        # Standard Libraries #
        import asyncio

        with pytest.raises(NotImplementedError, match="Async open is not implemented"):
            asyncio.run(test_object.open_async())

    def test_close_async_not_implemented(self, test_object: MockIOModeObject) -> None:
        """Tests that close_async raises NotImplementedError by default."""
        # Standard Libraries #
        import asyncio

        with pytest.raises(NotImplementedError, match="Async close is not implemented"):
            asyncio.run(test_object.close_async())


class TestAsyncBaseIOModeObject(BaseIOModeObjectTestSuite):
    """Unit tests for the BaseIOModeObject class with async support."""
    UnitTestClass: type[BaseIOModeObject] = AsyncMockIOModeObject

    @pytest.fixture
    def test_object(self) -> AsyncMockIOModeObject:
        """A fixture providing an AsyncMockIOModeObject instance.

        Returns:
            An AsyncMockIOModeObject instance.
        """
        return AsyncMockIOModeObject()


class TestStateRestriction(StateRestrictionTestSuite):
    """Unit tests for the staterestriction decorator."""
    UnitTestClass: type[staterestriction] = staterestriction

    @pytest.fixture
    def io_object(self) -> MockIOModeObject:
        """A fixture providing a MockIOModeObject instance.

        Returns:
            A MockIOModeObject instance.
        """
        return MockIOModeObject()

    def test_all_modes_restriction(self) -> None:
        """Tests the all_modes restriction."""
        def dummy() -> None:
            pass

        restriction = staterestriction(dummy, valid_modes=True)
        assert restriction.all_modes is True

        restriction = staterestriction(dummy, valid_modes=False)
        assert restriction.all_modes is False

    def test_single_mode_restriction(self) -> None:
        """Tests the single mode restriction."""
        def dummy() -> None:
            pass

        restriction = staterestriction(dummy, valid_modes="r")
        assert "r" in restriction.valid_modes
        assert restriction.all_modes is False

    def test_multi_mode_restriction(self) -> None:
        """Tests the multi mode restriction."""
        def dummy() -> None:
            pass

        restriction = staterestriction(dummy, valid_modes=["r", "w"])
        assert "r" in restriction.valid_modes
        assert "w" in restriction.valid_modes
        assert restriction.all_modes is False


class TestAsOpen(AsOpenTestSuite):
    """Unit tests for the asopen decorator."""
    UnitTestClass: type[asopen] = asopen

    @pytest.fixture
    def io_object(self) -> MockIOModeObject:
        """A fixture providing a MockIOModeObject instance.

        Returns:
            A MockIOModeObject instance.
        """
        return MockIOModeObject()


class TestAsOpenAsync(AsOpenAsyncTestSuite):
    """Unit tests for the asopenasync decorator."""
    UnitTestClass: type[asopenasync] = asopenasync

    @pytest.fixture
    def io_object(self) -> AsyncMockIOModeObject:
        """A fixture providing an AsyncMockIOModeObject instance.

        Returns:
            An AsyncMockIOModeObject instance.
        """
        return AsyncMockIOModeObject()


class MockIOCachingObject(MockIOModeObject, CachingObject):
    """A mock object with I/O modes and caching."""
    def __init__(self, mode: str = MockModes.READ) -> None:
        """Initializes the mock object."""
        super().__init__(mode=mode)
        CachingObject.__init__(self)
        self.call_count = 0

    @staterestriction(open_state=True, valid_modes=["r"])
    @timed_keyless_cache()
    def cached_restricted_method(self) -> int:
        """A method that is both restricted and cached."""
        self.call_count += 1
        return self.call_count

    @timed_keyless_cache()
    @staterestriction(open_state=True, valid_modes=["r"])
    def restricted_cached_method(self) -> int:
        """A method that is both cached and restricted (reversed order)."""
        self.call_count += 1
        return self.call_count


class TestStateRestrictionCaching:
    """Tests the interaction between staterestriction and timed_keyless_cache."""

    def test_staterestriction_and_caching(self) -> None:
        """Tests that staterestriction and caching work together."""
        obj = MockIOCachingObject()

        # Test case where staterestriction is outer
        method = obj.cached_restricted_method
        obj.call_count = 0
        obj.close()

        # Should fail initially because not open
        with pytest.raises(ValueError):
            method()

        # Open the object
        obj.open()

        # First call, should increment count
        assert method() == 1
        assert obj.call_count == 1

        # Second call, should be cached
        assert method() == 1
        assert obj.call_count == 1

        # Disable caching
        obj.disable_caching()

        # Third call, should not be cached
        assert method() == 2
        assert obj.call_count == 2

        # Re-enable caching
        obj.enable_caching()

        # Fourth call, should be cached (new cache because disable_caching might have cleared it)
        assert method() == 3
        assert obj.call_count == 3
        assert method() == 3
        assert obj.call_count == 3

        # Close the object
        obj.close()

        # Should fail now because staterestriction is outer and checked on every call
        with pytest.raises(ValueError):
            method()

    def test_caching_and_staterestriction_reversed(self) -> None:
        """Tests the interaction when caching is the outer decorator."""
        obj = MockIOCachingObject()

        # Test case where timed_keyless_cache is outer
        method = obj.restricted_cached_method
        obj.call_count = 0
        obj.close()

        # Should fail initially because not open (cache is empty)
        with pytest.raises(ValueError):
            method()

        # Open the object
        obj.open()

        # First call, should increment count
        assert method() == 1
        assert obj.call_count == 1

        # Second call, should be cached
        assert method() == 1
        assert obj.call_count == 1

        # Close the object
        obj.close()

        # Should NOT fail now because timed_keyless_cache is outer and hit the cache before staterestriction
        # This is expected behavior for this order of decorators.
        assert method() == 1

    def test_instance_separation(self) -> None:
        """Tests that caches are separate between instances."""
        obj1 = MockIOCachingObject()
        obj2 = MockIOCachingObject()

        obj1.open()
        obj2.open()

        assert obj1.cached_restricted_method() == 1
        assert obj2.cached_restricted_method() == 1

        assert obj1.cached_restricted_method() == 1
        assert obj2.cached_restricted_method() == 1

        assert obj1.call_count == 1
        assert obj2.call_count == 1
