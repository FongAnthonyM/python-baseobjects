#!/usr/bin/env python
"""basereducible_performance.py
Performance tests for the BaseReducible class in the baseobjects.bases package.
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
import timeit
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import BaseReducible
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class NormalReducible:
    """A normal Python object with pickle support for comparison with BaseReducible."""

    def __init__(
        self,
        value: Any = None,
        mutable: list[int] | None = None,
        mapping: dict[str, int] | None = None,
    ) -> None:
        """Initialize with some attributes."""
        self.value = value
        self.mutable = mutable or [1, 2, 3]
        self.mapping = mapping or {"a": 1, "b": 2, "c": 3}

    def __getstate__(self) -> dict[str, Any]:
        """Get the state.

        Returns:
            dict[str, Any]: The state.
        """
        return self.__dict__.copy()

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Set the object's state from a pickled state."""
        self.__dict__.update(state)


class SlottedNormalReducible:
    """A normal Python object with __slots__ and pickle support for comparison."""

    __slots__ = ["mapping", "mutable", "value"]

    def __init__(
        self,
        value: Any = None,
        mutable: list[int] | None = None,
        mapping: dict[str, int] | None = None,
    ) -> None:
        """Initialize with some attributes."""
        self.value = value
        self.mutable = mutable or [1, 2, 3]
        self.mapping = mapping or {"a": 1, "b": 2, "c": 3}

    def __getstate__(self) -> dict[str, Any]:
        """Get the object's state for pickling.

        Returns:
            dict[str, Any]: The state.
        """
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Set the object's state from a pickled state."""
        for slot, value in state.items():
            setattr(self, slot, value)


class TestBaseReduciblePerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseReducible class.

    This test suite measures the performance of various operations on BaseReducible objects
    and compares them with standard Python implementations.
    """

    # Class Definitions #
    class TestReducible(BaseReducible):
        """A concrete subclass of BaseReducible for testing purposes."""

        def __init__(
            self,
            value: Any = None,
            mutable: list[int] | None = None,
            mapping: dict[str, int] | None = None,
        ) -> None:
            """Initialize with some attributes."""
            super().__init__()
            self.value = value
            self.mutable = mutable or [1, 2, 3]
            self.mapping = mapping or {"a": 1, "b": 2, "c": 3}

    class TestSlottedReducible(BaseReducible):
        """A concrete subclass of BaseReducible with __slots__ for testing purposes."""

        __slots__ = ["mapping", "mutable", "value"]

        def __init__(
            self,
            value: Any = None,
            mutable: list[int] | None = None,
            mapping: dict[str, int] | None = None,
        ) -> None:
            """Initialize with some attributes."""
            super().__init__()
            self.value = value
            self.mutable = mutable or [1, 2, 3]
            self.mapping = mapping or {"a": 1, "b": 2, "c": 3}

    class TestMixedReducible(BaseReducible):
        """A concrete subclass of BaseReducible with both __dict__ and __slots__ for testing purposes."""

        __slots__ = ["value"]

        def __init__(
            self,
            value: Any = None,
            mutable: list[int] | None = None,
            mapping: dict[str, int] | None = None,
        ) -> None:
            """Initialize with some attributes."""
            super().__init__()
            self.value = value
            self.mutable = mutable or [1, 2, 3]
            self.mapping = mapping or {"a": 1, "b": 2, "c": 3}

    # Attributes #
    timeit_runs: int = 10000  # Reduced runs for pickling operations which can be slower

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_reducible(self) -> "TestBaseReduciblePerformance.TestReducible":
        """Create a test reducible instance for use in tests.

        Returns:
            TestReducible: An instance of the test class.
        """
        return self.TestReducible("test")

    @pytest.fixture
    def test_slotted_reducible(self) -> "TestBaseReduciblePerformance.TestSlottedReducible":
        """Create a test slotted reducible instance for use in tests.

        Returns:
            TestSlottedReducible: An instance of the test class with __slots__.
        """
        return self.TestSlottedReducible("test")

    @pytest.fixture
    def test_mixed_reducible(self) -> "TestBaseReduciblePerformance.TestMixedReducible":
        """Create a test mixed reducible instance for use in tests.

        Returns:
            TestMixedReducible: An instance of the test class with both __dict__ and __slots__.
        """
        return self.TestMixedReducible("test")

    @pytest.fixture
    def test_normal_reducible(self) -> NormalReducible:
        """Create a normal reducible instance for comparison.

        Returns:
            NormalReducible: A standard Python object with pickle support.
        """
        return NormalReducible("test")

    @pytest.fixture
    def test_slotted_normal_reducible(self) -> SlottedNormalReducible:
        """Create a normal slotted reducible instance for comparison.

        Returns:
            SlottedNormalReducible: A standard Python object with __slots__ and pickle support.
        """
        return SlottedNormalReducible("test")

    # Tests
    def test_getstate_performance(
        self,
        test_reducible: "TestBaseReduciblePerformance.TestReducible",
        test_normal_reducible: NormalReducible,
    ) -> None:
        """Test the performance of the __getstate__ method of BaseReducible.

        This test compares the speed of BaseReducible.__getstate__() with a normal object's __getstate__().

        Args:
            test_reducible: A fixture providing a TestReducible instance.
            test_normal_reducible: A fixture providing a NormalReducible instance.
        """

        def getstate_base_reducible() -> None:
            test_reducible.__getstate__()

        def getstate_normal_reducible() -> None:
            test_normal_reducible.__getstate__()

        # Calculate the mean time in microseconds for BaseReducible.__getstate__
        base_time = timeit.timeit(getstate_base_reducible, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object's __getstate__
        normal_time = timeit.timeit(getstate_normal_reducible, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object __getstate__: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseReducible.__getstate__: {mean_base:.3f} μs ({percent:.3f}% of normal object __getstate__ time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for state extraction

    def test_slotted_getstate_performance(
        self,
        test_slotted_reducible: "TestBaseReduciblePerformance.TestSlottedReducible",
        test_slotted_normal_reducible: SlottedNormalReducible,
    ) -> None:
        """Test the performance of the __getstate__ method of BaseReducible with __slots__.

        This test compares the speed of BaseReducible.__getstate__() with a normal slotted object's __getstate__().

        Args:
            test_slotted_reducible: A fixture providing a TestSlottedReducible instance.
            test_slotted_normal_reducible: A fixture providing a SlottedNormalReducible instance.
        """

        def getstate_base_reducible() -> None:
            test_slotted_reducible.__getstate__()

        def getstate_normal_reducible() -> None:
            test_slotted_normal_reducible.__getstate__()

        # Calculate the mean time in microseconds for BaseReducible.__getstate__
        base_time = timeit.timeit(getstate_base_reducible, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object's __getstate__
        normal_time = timeit.timeit(getstate_normal_reducible, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal slotted object __getstate__: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"BaseReducible with __slots__ __getstate__: {mean_base:.3f} μs "
            f"({percent:.3f}% of normal slotted object __getstate__ time)",
        )
        assert percent < self.speed_tolerance * 2  # Allow more overhead for state extraction

    def test_mixed_getstate_performance(
        self,
        test_mixed_reducible: "TestBaseReduciblePerformance.TestMixedReducible",
    ) -> None:
        """Test the performance of the __getstate__ method of BaseReducible with both __dict__ and __slots__.

        This test measures the time it takes to get the state of a BaseReducible object with both __dict__ and
        __slots__.

        Args:
            test_mixed_reducible: A fixture providing a TestMixedReducible instance.
        """

        def getstate_mixed_reducible() -> None:
            test_mixed_reducible.__getstate__()

        # Calculate the mean time in microseconds for BaseReducible.__getstate__
        mixed_time = timeit.timeit(getstate_mixed_reducible, number=self.timeit_runs)
        mean_mixed = mixed_time / self.timeit_runs * 1000000

        # Print the performance result
        print((
            "\nBaseReducible with mixed __dict__ and __slots__ __getstate__:",
            f"{mean_mixed:.3f} μs or {mean_mixed / self.call_speed:.3f} cu",
        ))
        # No direct comparison, just ensure it's reasonably fast
        assert mean_mixed < 200  # 200 microseconds is a reasonable threshold

    def test_setstate_performance(
        self,
        test_reducible: "TestBaseReduciblePerformance.TestReducible",
        test_normal_reducible: NormalReducible,
    ) -> None:
        """Test the performance of the __setstate__ method of BaseReducible.

        This test compares the speed of BaseReducible.__setstate__() with a normal object's __setstate__().

        Args:
            test_reducible: A fixture providing a TestReducible instance.
            test_normal_reducible: A fixture providing a NormalReducible instance.
        """
        # Get states to restore
        base_state = test_reducible.__getstate__()
        normal_state = test_normal_reducible.__getstate__()

        def setstate_base_reducible() -> None:
            test_reducible.__setstate__(base_state)

        def setstate_normal_reducible() -> None:
            test_normal_reducible.__setstate__(normal_state)

        # Calculate the mean time in microseconds for BaseReducible.__setstate__
        base_time = timeit.timeit(setstate_base_reducible, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object's __setstate__
        normal_time = timeit.timeit(setstate_normal_reducible, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object __setstate__: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseReducible.__setstate__: {mean_base:.3f} μs ({percent:.3f}% of normal object __setstate__ time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for state restoration

    def test_slotted_setstate_performance(
        self,
        test_slotted_reducible: "TestBaseReduciblePerformance.TestSlottedReducible",
        test_slotted_normal_reducible: SlottedNormalReducible,
    ) -> None:
        """Test the performance of the __setstate__ method of BaseReducible with __slots__.

        This test compares the speed of BaseReducible.__setstate__() with a normal slotted object's __setstate__().

        Args:
            test_slotted_reducible: A fixture providing a TestSlottedReducible instance.
            test_slotted_normal_reducible: A fixture providing a SlottedNormalReducible instance.
        """
        # Get states to restore
        base_state = test_slotted_reducible.__getstate__()
        normal_state = test_slotted_normal_reducible.__getstate__()

        def setstate_base_reducible() -> None:
            test_slotted_reducible.__setstate__(base_state)

        def setstate_normal_reducible() -> None:
            test_slotted_normal_reducible.__setstate__(normal_state)

        # Calculate the mean time in microseconds for BaseReducible.__setstate__
        base_time = timeit.timeit(setstate_base_reducible, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object's __setstate__
        normal_time = timeit.timeit(setstate_normal_reducible, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal slotted object __setstate__: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"BaseReducible with __slots__ __setstate__: {mean_base:.3f} μs "
            f"({percent:.3f}% of normal slotted object __setstate__ time)",
        )
        assert percent < self.speed_tolerance * 2  # Allow more overhead for state restoration

    def test_mixed_setstate_performance(
        self,
        test_mixed_reducible: "TestBaseReduciblePerformance.TestMixedReducible",
    ) -> None:
        """Test the performance of the __setstate__ method of BaseReducible with both __dict__ and __slots__.

        This test measures the time it takes to set the state of a BaseReducible object with both __dict__ and
        __slots__.

        Args:
            test_mixed_reducible: A fixture providing a TestMixedReducible instance.
        """
        # Get state to restore
        mixed_state = test_mixed_reducible.__getstate__()

        def setstate_mixed_reducible() -> None:
            test_mixed_reducible.__setstate__(mixed_state)

        # Calculate the mean time in microseconds for BaseReducible.__setstate__
        mixed_time = timeit.timeit(setstate_mixed_reducible, number=self.timeit_runs)
        mean_mixed = mixed_time / self.timeit_runs * 1000000

        # Print the performance result
        print((
            "\nBaseReducible with mixed __dict__ and __slots__ __setstate__:",
            f"{mean_mixed:.3f} μs or {mean_mixed / self.call_speed:.3f} cu",
        ))
        # No direct comparison, just ensure it's reasonably fast
        assert mean_mixed < 200  # 200 microseconds is a reasonable threshold

    def test_pickle_performance(
        self,
        test_reducible: "TestBaseReduciblePerformance.TestReducible",
        test_normal_reducible: NormalReducible,
    ) -> None:
        """Test the performance of pickling and unpickling BaseReducible objects.

        This test compares the speed of pickling and unpickling BaseReducible objects with normal objects.

        Args:
            test_reducible: A fixture providing a TestReducible instance.
            test_normal_reducible: A fixture providing a NormalReducible instance.
        """

        def pickle_base_reducible() -> None:
            pickle.dumps(test_reducible)

        def pickle_normal_reducible() -> None:
            pickle.dumps(test_normal_reducible)

        # Calculate the mean time in microseconds for pickling BaseReducible
        base_time = timeit.timeit(pickle_base_reducible, number=self.timeit_runs // 10)  # Reduce runs for pickling
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for pickling normal object
        normal_time = timeit.timeit(pickle_normal_reducible, number=self.timeit_runs // 10)  # Reduce runs for pickling
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object pickling: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseReducible pickling: {mean_base:.3f} μs ({percent:.3f}% of normal object pickling time)")
        assert percent < self.speed_tolerance * 3  # Allow more overhead for pickling operations

        # Now test unpickling
        base_pickle = pickle.dumps(test_reducible)
        normal_pickle = pickle.dumps(test_normal_reducible)

        def unpickle_base_reducible() -> None:
            pickle.loads(base_pickle)

        def unpickle_normal_reducible() -> None:
            pickle.loads(normal_pickle)

        # Calculate the mean time in microseconds for unpickling BaseReducible
        base_time = timeit.timeit(unpickle_base_reducible, number=self.timeit_runs // 10)  # Reduce runs for unpickling
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for unpickling normal object
        normal_time = timeit.timeit(
            unpickle_normal_reducible,
            number=self.timeit_runs // 10,
        )  # Reduce runs for unpickling
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object unpickling: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseReducible unpickling: {mean_base:.3f} μs ({percent:.3f}% of normal object unpickling time)")
        assert percent < self.speed_tolerance * 3  # Allow more overhead for unpickling operations


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
