"""wrapperperformancetestsuite.py
Base performance test suite for wrapper classes.
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
from abc import abstractmethod
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ..bases import BasePerformanceTestSuite


# Definitions #
# Classes #
class WrapperPerformanceTestSuite(BasePerformanceTestSuite):
    """A base test suite which assays the performance of wrapper classes.

    This is a base test suite that concrete subclasses should implement abstract methods and assign attributes.

    Attributes:
        _base_time: The time it takes to run a simple function call for a baseline of 10 million iterations.
        call_speed: The baseline speed of a simple function call in microseconds.
        timeit_runs: The number of runs to use for timeit measurements.
        speed_tolerance: The maximum percentage of time a new implementation can take compared to the old one.
        UnitTestClass: The main wrapper class to be assayed.
    """

    class ConcreteOne:
        """An example class for testing wrappers.

        This class has attributes and methods that can be wrapped by wrapper classes.
        """

        # Attributes #
        one: str
        two: str = "one"
        common: str = "example_one"

        def __init__(self) -> None:
            """Initializes with attributes."""
            self.one = "one"
            self.two = "one"
            self.common = "example_one"

        def __eq__(self, other: Any) -> bool:
            """Checks equality with another object.

            Args:
                other: The object to compare with.

            Returns:
                Always True.
            """
            return True

        def method(self) -> str:
            """Returns a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "one"

        def __str__(self) -> str:
            """Returns a string representation of this class."""
            return "ConcreteOne"

    class ConcreteTwo:
        """Another example class for testing wrappers.

        This class has different attributes and methods than ConcreteOne.
        """

        # Attributes #
        one: str
        three: str
        common: str

        def __init__(self) -> None:
            """Initializes with attributes."""
            self.one = "two"
            self.three = "two"
            self.common = "example_two"

        def function(self) -> str:
            """Returns a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "two"

        def __str__(self) -> str:
            """Returns a string representation of this class."""
            return "ConcreteTwo"

    timeit_runs: int = 100000

    speed_tolerance: int = 150

    UnitTestClass: type[Any]

    # Fixtures #
    @abstractmethod
    @pytest.fixture
    def test_object(self, *args: Any, **kwargs: Any) -> Any:
        """Creates a test object.

        Returns:
            A wrapper object with ConcreteOne and ConcreteTwo objects.
        """

    @pytest.fixture
    def test_example_one(self) -> ConcreteOne:
        """Creates a test ConcreteOne object.

        Returns:
            An ConcreteOne object.
        """
        return self.ConcreteOne()

    @pytest.fixture
    def test_example_two(self) -> ConcreteTwo:
        """Creates a test ConcreteTwo object.

        Returns:
            An ConcreteTwo object.
        """
        return self.ConcreteTwo()

    # Tests #
    @abstractmethod
    def test_instance_creation_performance(self) -> None:
        """Tests the performance of creating instances of the wrapper class.

        This is an abstract method that must be implemented by subclasses.
        """

    def test_attribute_access_performance(self, test_object: Any) -> None:
        """Tests the performance of attribute access through the wrapper.

        This test compares the speed of accessing attributes through the wrapper with direct attribute access.

        Args:
            test_object: A fixture providing a wrapper test object.
        """

        def wrapper_access() -> None:
            _ = test_object.one
            _ = test_object.two
            _ = test_object.common

        def direct_access() -> None:
            _ = test_object._first.one
            _ = test_object._first.two
            _ = test_object._first.common

        # Calculate the mean time in microseconds for the wrapper access
        new_time = timeit.timeit(wrapper_access, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for direct access
        old_time = timeit.timeit(direct_access, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"""
            \n{self.UnitTestClass.__name__} attribute access: {mean_new:.3f} μs ({percent:.3f}% of direct access time)
        """)
        assert percent < self.speed_tolerance

    def test_attribute_set_performance(self, test_object: Any) -> None:
        """Tests the performance of attribute setting through the wrapper.

        This test compares the speed of setting attributes through the wrapper with direct attribute setting.

        Args:
            test_object: A fixture providing a wrapper test object.
        """

        def wrapper_set() -> None:
            test_object.one = "one"
            test_object.two = "one"
            test_object.common = "example_one"

        def direct_set() -> None:
            test_object._first.one = "one"
            test_object._first.two = "one"
            test_object._first.common = "example_one"

        # Calculate the mean time in microseconds for the wrapper set
        new_time = timeit.timeit(wrapper_set, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for direct set
        old_time = timeit.timeit(direct_set, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\n{self.UnitTestClass.__name__} attribute set: {mean_new:.3f} μs ({percent:.3f}% of direct set time)")
        assert percent < self.speed_tolerance

    def test_method_call_performance(self, test_object: Any) -> None:
        """Tests the performance of method calls through the wrapper.

        This test compares the speed of calling methods through the wrapper with direct method calls.

        Args:
            test_object: A fixture providing a wrapper test object.
        """

        def wrapper_call() -> None:
            _ = test_object.method()

        def direct_call() -> None:
            _ = test_object._first.method()

        # Calculate the mean time in microseconds for the wrapper call
        new_time = timeit.timeit(wrapper_call, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for direct call
        old_time = timeit.timeit(direct_call, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\n{self.UnitTestClass.__name__} method call: {mean_new:.3f} μs ({percent:.3f}% of direct call time)")
        assert percent < self.speed_tolerance
