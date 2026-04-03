#!/usr/bin/env python
"""dispatchableclass_performance.py
Performance tests for the DispatchableClass class in the baseobjects.classregistration package.
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
import timeit
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.classregistration import DispatchableClass, NamespaceClassRegistry
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class ConcreteDispatchableClass(DispatchableClass):
    """An example dispatchable class."""
    class_registry = NamespaceClassRegistry()

    @classmethod
    def get_registered_class(cls, name: str) -> Any:
        """Gets the registered class.

        Args:
            name: The name of the class to retrieve.

        Returns:
            The registered class.
        """
        return cls.class_registry.get_class("example", name)

    @classmethod
    def get_class_information(cls, *args: Any, **kwargs: Any) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        """Gets the class information.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The keyword arguments for class lookup and the keyword arguments to pass to the class constructor or None
            if not found.
        """
        return {"name": kwargs.get("name")}, None


class SubClass(ConcreteDispatchableClass):
    """A subclass for dispatch testing."""


# Register the subclass
ConcreteDispatchableClass.class_registry.register_class(SubClass, "example", "SubClass")


class TestDispatchableClassPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the DispatchableClass class.

    This test suite measures the performance of dispatching during instantiation.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Tests
    def test_dispatch_performance(self) -> None:
        """Test the performance of dispatching to a subclass.

        This test measures the speed of instantiating the base class and dispatching to a subclass.
        """

        def dispatch() -> None:
            ConcreteDispatchableClass(name="SubClass")

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(dispatch, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nDispatchableClass dispatch: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_no_dispatch_performance(self) -> None:
        """Test the performance of instantiation without dispatch (direct instantiation).

        This test measures the overhead of the __new__ method when no dispatch occurs.
        """

        def no_dispatch() -> None:
            SubClass()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(no_dispatch, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nDispatchableClass direct instantiation: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
