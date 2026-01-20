#!/usr/bin/env python
"""classregistry_performance.py
Performance tests for the ClassRegistry class in the baseobjects.classregistration package.
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

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.classregistration import NamespaceClassRegistry
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class ExampleClass:
    """An example class for registration."""


class TestClassRegistryPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the NamespaceClassRegistry class.

    This test suite measures the performance of registering and retrieving classes.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def registry(self) -> NamespaceClassRegistry:
        """Create a test NamespaceClassRegistry for use in tests.

        Returns:
            NamespaceClassRegistry: An instance of the test class.
        """
        registry = NamespaceClassRegistry()
        registry.register_class(ExampleClass, "example", "ExampleClass")
        return registry

    # Tests
    def test_get_class_performance(self, registry: NamespaceClassRegistry) -> None:
        """Test the performance of getting a class from the registry.

        This test measures the speed of retrieving a registered class.
        """

        def get_class() -> None:
            registry.get_class("example", "ExampleClass")

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(get_class, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nNamespaceClassRegistry get_class: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_register_class_performance(self) -> None:
        """Test the performance of registering a class.

        This test measures the speed of registering a class.
        """
        registry = NamespaceClassRegistry()

        def register_class() -> None:
            registry.register_class(ExampleClass, "example", "ExampleClass")

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(register_class, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nNamespaceClassRegistry register_class: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
