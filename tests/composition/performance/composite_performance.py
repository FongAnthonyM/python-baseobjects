#!/usr/bin/env python
"""composite_performance.py
Performance tests for the BaseComposite class in the baseobjects.composition package.
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
from baseobjects.composition import BaseComponent, BaseComposite
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class ExampleComponent(BaseComponent):
    """An example component."""


class ExampleComposite(BaseComposite):
    """An example composite."""


class TestCompositePerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseComposite class.

    This test suite measures the performance of component management.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def composite(self) -> BaseComposite:
        """Create a test BaseComposite for use in tests.

        Returns:
            BaseComposite: An instance of the test class.
        """
        return ExampleComposite()

    @pytest.fixture
    def component(self) -> BaseComponent:
        """Create a test BaseComponent for use in tests.

        Returns:
            BaseComponent: An instance of the test class.
        """
        return ExampleComponent()

    # Tests
    def test_instantiation_performance(self) -> None:
        """Test the performance of creating BaseComposite instances.

        This test measures the speed of creating a BaseComposite.
        """

        def create_composite() -> None:
            ExampleComposite()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(create_composite, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nBaseComposite creation: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_add_component_performance(self, composite: BaseComposite, component: BaseComponent) -> None:
        """Test the performance of adding a component.

        This test measures the speed of adding a component to the composite.
        """

        def add_component() -> None:
            composite.add_component("test", component)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(add_component, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nBaseComposite add_component: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_component_access_performance(self, composite: BaseComposite, component: BaseComponent) -> None:
        """Test the performance of accessing a component.

        This test measures the speed of accessing a component from the composite.
        """
        composite.add_component("test", component)

        def access_component() -> None:
            _ = composite.components["test"]

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(access_component, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nBaseComposite component access: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
