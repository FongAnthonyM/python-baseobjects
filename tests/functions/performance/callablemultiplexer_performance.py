#!/usr/bin/env python
"""callablemultiplexer_performance.py
Performance tests for the CallableMultiplexer and MethodMultiplexer classes in the baseobjects.functions package.
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
from baseobjects.functions.callablemultiplexer import CallableMultiplexer, MethodMultiplexer
from baseobjects.testsuite import BasePerformanceTestSuite

# from typing import


# Definitions #
# Classes #
class TestCallableMultiplexerPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the CallableMultiplexer class.

    This test suite measures the performance of various operations on CallableMultiplexer objects and compares them
    with standard Python implementations.

    Attributes:
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
        UnitTestClass: The class being tested.
    """

    # Class Definitions #
    class ConcreteClass:
        """A class to test method binding."""

        def method1(self, x: int) -> int:
            """First test method.

            Returns:
                int: The result.
            """
            return x * 2

        def method2(self, x: int) -> int:
            """Second test method.

            Returns:
                int: The result.
            """
            return x * 3

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    UnitTestClass: type[CallableMultiplexer] = CallableMultiplexer

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_multiplexer(self) -> CallableMultiplexer:
        """Create a test multiplexer instance for use in tests.

        Returns:
            CallableMultiplexer: An instance of the test class.
        """
        multiplexer = self.UnitTestClass()
        multiplexer.add_function("func1", lambda x: x * 2)
        multiplexer.add_function("func2", lambda x: x * 3)
        multiplexer.select("func1")
        return multiplexer

    @pytest.fixture
    def test_class_instance(self) -> TestCallableMultiplexerPerformance.ConcreteClass:
        """Create a test class instance for use in tests.

        Returns:
            ConcreteClass: An instance of the test class.
        """
        return self.ConcreteClass()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of CallableMultiplexer can be created efficiently.

        This test compares the speed of creating CallableMultiplexer instances with creating standard Python
        dictionaries.
        """

        # Define the performance test functions
        def create_multiplexer() -> None:
            self.UnitTestClass()

        def create_dict() -> None:
            {"func1": lambda x: x * 2, "func2": lambda x: x * 3}

        # Calculate the mean time in microseconds for the multiplexer creation
        new_time = timeit.timeit(create_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dictionary creation
        old_time = timeit.timeit(create_dict, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nDictionary creation: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"CallableMultiplexer creation: {mean_new:.3f} μs ({percent:.3f}% of dictionary creation time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test the performance of the __call__ method of CallableMultiplexer.

        This test compares the speed of CallableMultiplexer.__call__() with a direct function call.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """

        # Create a normal function to compare against
        def normal(x: int) -> int:
            return x * 2

        arg = 5

        # Define the performance test functions
        def call_multiplexer() -> None:
            test_multiplexer(arg)

        def call_normal() -> None:
            normal(arg)

        # Calculate the mean time in microseconds for the multiplexer call
        new_time = timeit.timeit(call_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function call
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal function call: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"CallableMultiplexer call: {mean_new:.3f} μs ({percent:.3f}% of normal function call time)")
        assert percent < self.speed_tolerance

    def test_add_function_speed(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test the performance of the add_function method of CallableMultiplexer.

        This test compares the speed of CallableMultiplexer.add_function() with a dictionary update.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # Create a dictionary to compare against
        funcs = {"func1": lambda x: x * 2, "func2": lambda x: x * 3}

        # Define a new function to add
        def new_func(x: int) -> int:
            return x * 4

        # Define the performance test functions
        def add_to_multiplexer() -> None:
            test_multiplexer.add_function("func3", new_func)

        def add_to_dict() -> None:
            funcs["func3"] = new_func

        # Calculate the mean time in microseconds for the multiplexer add
        new_time = timeit.timeit(add_to_multiplexer, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the dictionary update
        old_time = timeit.timeit(add_to_dict, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nDictionary update: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"CallableMultiplexer add_function: {mean_new:.3f} μs ({percent:.3f}% of dictionary update time)")
        assert percent < self.speed_tolerance


class TestMethodMultiplexerPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the MethodMultiplexer class.

    This test suite measures the performance of various operations on MethodMultiplexer objects and compares them with
    standard Python implementations.

    Attributes:
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
        UnitTestClass: The class being tested.
    """

    # Class Definitions #
    class ConcreteInstanceClass:
        """A class to test method binding."""

        def method1(self, x: int) -> int:
            """First test method.

            Returns:
                int: The result.
            """
            return x * 2

        def method2(self, x: int) -> int:
            """Second test method.

            Returns:
                int: The result.
            """
            return x * 3

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    UnitTestClass: type[MethodMultiplexer] = MethodMultiplexer

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> TestMethodMultiplexerPerformance.ConcreteInstanceClass:
        """Create a test class instance for use in tests.

        Returns:
            UnitTestClass: An instance of the test class.
        """
        return self.ConcreteInstanceClass()

    @pytest.fixture
    def test_multiplexer(
        self,
        test_class_instance: TestMethodMultiplexerPerformance.ConcreteInstanceClass,
    ) -> MethodMultiplexer:
        """Create a test multiplexer instance for use in tests.

        Args:
            test_class_instance: A fixture providing a UnitTestClass instance.

        Returns:
            MethodMultiplexer: An instance of the test class.
        """
        multiplexer = self.UnitTestClass(instance=test_class_instance)
        multiplexer.select("method1")
        return multiplexer

    # Tests
    def test_instance_creation(
        self,
        test_class_instance: TestMethodMultiplexerPerformance.ConcreteInstanceClass,
    ) -> None:
        """Test that instances of MethodMultiplexer can be created efficiently.

        This test compares the speed of creating MethodMultiplexer instances with creating standard Python dictionaries
        of methods.

        Args:
            test_class_instance: A fixture providing a UnitTestClass instance.
        """

        # Define the performance test functions
        def create_multiplexer() -> None:
            self.UnitTestClass(instance=test_class_instance)

        def create_dict() -> None:
            _ = {"method1": test_class_instance.method1, "method2": test_class_instance.method2}

        # Calculate the mean time in microseconds for the multiplexer creation
        new_time = timeit.timeit(create_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dictionary creation
        old_time = timeit.timeit(create_dict, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nDictionary of methods creation: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"MethodMultiplexer creation: {mean_new:.3f} μs ({percent:.3f}% of dictionary creation time)")
        assert percent < self.speed_tolerance

    def test_call_speed(
        self,
        test_multiplexer: MethodMultiplexer,
        test_class_instance: TestMethodMultiplexerPerformance.ConcreteInstanceClass,
    ) -> None:
        """Test the performance of the __call__ method of MethodMultiplexer.

        This test compares the speed of MethodMultiplexer.__call__() with a direct method call.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
            test_class_instance: A fixture providing a UnitTestClass instance.
        """
        arg = 5

        # Define the performance test functions
        def call_multiplexer() -> None:
            test_multiplexer(arg)

        def call_normal() -> None:
            test_class_instance.method1(arg)

        # Calculate the mean time in microseconds for the multiplexer call
        new_time = timeit.timeit(call_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the direct method call
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nDirect method call: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"MethodMultiplexer call: {mean_new:.3f} μs ({percent:.3f}% of direct method call time)")
        assert percent < self.speed_tolerance

    def test_edge_case_method_switching(self, test_multiplexer: MethodMultiplexer) -> None:
        """Test the performance of rapidly switching between methods.

        This test measures the performance overhead when frequently switching between methods.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
        """

        # Define the performance test functions
        def switch_and_call() -> None:
            test_multiplexer.select("method1")
            test_multiplexer(5)
            test_multiplexer.select("method2")
            test_multiplexer(5)

        # Calculate the mean time in microseconds
        time = timeit.timeit(switch_and_call, number=self.timeit_runs // 10)
        mean_time = time / (self.timeit_runs // 10) * 1000000

        # Print the performance result
        print(f"\nMethod switching and calling: {mean_time:.3f} μs")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_time < 200  # 200 microseconds is a reasonable threshold


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
