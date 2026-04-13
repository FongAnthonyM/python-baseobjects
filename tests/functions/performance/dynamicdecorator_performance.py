#!/usr/bin/env python
"""dynamicdecoractor_performance.py
Performance tests for the DynamicDecorator class in the baseobjects.functions package.
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
from collections.abc import Callable
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.functions.basedecorator import BaseDecorator
from baseobjects.functions.dynamicdecorator import DynamicDecorator
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestDynamicDecoratorPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the DynamicDecorator class.

    This test suite measures the performance of various operations on DynamicDecorator objects and compares them with
    standard Python implementations and BaseDecorator.

    Attributes:
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
        UnitTestClass: The class being tested.
    """

    # Class Definitions #
    class TestDynamicDecorator(DynamicDecorator):
        """A subclass of DynamicDecorator for testing purposes."""

        # Magic Methods #
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation.

            Returns:
                Any: The result.
            """
            return self.call_wrapped(*args, **kwargs)

        def construct_call(self, func: Callable[..., Any] | None = None, *args: Any, **kwargs: Any) -> Any:
            """Construct the call.

            Returns:
                Any: The result.
            """
            self.construct(func, *args, **kwargs)
            return self

    class TestBaseDecorator(BaseDecorator):
        """A subclass of BaseDecorator for testing purposes."""

        # Magic Methods #
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation.

            Returns:
                Any: The result.
            """
            return self.call_wrapped(*args, **kwargs)

        def construct_call(self, func: Callable[..., Any] | None = None, *args: Any, **kwargs: Any) -> Any:
            """Construct the call.

            Returns:
                Any: The result.
            """
            self.construct(func, *args, **kwargs)
            return self

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: int = 1000000

    UnitTestClass: type[TestDynamicDecorator] = TestDynamicDecorator

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dynamic_decorator(self) -> TestDynamicDecoratorPerformance.TestDynamicDecorator:
        """Create a test dynamic decorator instance for use in tests.

        Returns:
            TestDynamicDecorator: An instance of the test class.
        """
        return self.UnitTestClass(_return_partial=False)

    @pytest.fixture
    def test_base_decorator(self) -> TestDynamicDecoratorPerformance.TestBaseDecorator:
        """Create a test base decorator instance for use in tests.

        Returns:
            TestBaseDecorator: An instance of the BaseDecorator test class.
        """
        return self.TestBaseDecorator(_return_partial=False)

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of DynamicDecorator can be created efficiently.

        This test compares the speed of creating DynamicDecorator instances with creating BaseDecorator instances and
        standard Python functions.
        """

        # Define the performance test functions
        def create_dynamic_decorator() -> None:
            self.UnitTestClass(_return_partial=False)

        def create_base_decorator() -> None:
            self.TestBaseDecorator(_return_partial=False)

        def create_normal_function() -> None:
            lambda x: x * 2

        # Calculate the mean time in microseconds for the dynamic decorator creation
        dynamic_time = timeit.timeit(create_dynamic_decorator, number=self.timeit_runs)
        mean_dynamic = dynamic_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the base decorator creation
        base_time = timeit.timeit(create_base_decorator, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function creation
        normal_time = timeit.timeit(create_normal_function, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000

        # Calculate percentages
        dynamic_to_normal_percent = (mean_dynamic / mean_normal) * 100
        dynamic_to_base_percent = (mean_dynamic / mean_base) * 100

        # Print the performance comparison
        print(
            f"\nNormal function creation: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"BaseDecorator creation: {mean_base:.3f} μs "
            f"({(mean_base / mean_normal):.3f}% of normal function creation time)",
        )
        print(
            f"DynamicDecorator creation: {mean_dynamic:.3f} μs "
            f"({dynamic_to_normal_percent:.3f}% of normal function creation time, "
            f"{dynamic_to_base_percent:.3f}% of BaseDecorator creation time)",
        )

        # Assert that the performance is within acceptable limits
        assert dynamic_to_normal_percent < self.speed_tolerance
        assert dynamic_to_base_percent < self.speed_tolerance * 1.5  # Allow more overhead compared to BaseDecorator

    def test_call_speed(
        self,
        test_dynamic_decorator: TestDynamicDecoratorPerformance.TestDynamicDecorator,
        test_base_decorator: TestDynamicDecoratorPerformance.TestBaseDecorator,
    ) -> None:
        """Test the performance of the __call__ method of DynamicDecorator.

        This test compares the speed of DynamicDecorator.__call__() with BaseDecorator.__call__() and a normal function
        call.

        Args:
            test_dynamic_decorator: A fixture providing a TestDynamicDecorator instance.
            test_base_decorator: A fixture providing a TestBaseDecorator instance.
        """

        # Create a normal function to compare against
        def normal(x: int) -> int:
            return x * 2

        arg = 5

        # Define the performance test functions
        def call_dynamic_decorator() -> None:
            test_dynamic_decorator(arg)

        def call_base_decorator() -> None:
            test_base_decorator(arg)

        def call_normal() -> None:
            normal(arg)

        # Calculate the mean time in microseconds for the dynamic decorator call
        dynamic_time = timeit.timeit(call_dynamic_decorator, number=self.timeit_runs)
        mean_dynamic = dynamic_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the base decorator call
        base_time = timeit.timeit(call_base_decorator, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function call
        normal_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000

        # Calculate percentages
        dynamic_to_normal_percent = (mean_dynamic / mean_normal) * 100
        dynamic_to_base_percent = (mean_dynamic / mean_base) * 100

        # Print the performance comparison
        print(
            f"\nNormal function call: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(f"BaseDecorator call: {mean_base:.3f} μs ({(mean_base / mean_normal):.3f}% of normal function call time)")
        print(
            f"DynamicDecorator call: {mean_dynamic:.3f} μs "
            f"({dynamic_to_normal_percent:.3f}% of normal function call time, "
            f"{dynamic_to_base_percent:.3f}% of BaseDecorator call time)",
        )

        # Assert that the performance is within acceptable limits
        assert dynamic_to_normal_percent < self.speed_tolerance
        assert dynamic_to_base_percent < self.speed_tolerance * 1.5  # Allow more overhead compared to BaseDecorator

    def test_construct_call_speed(self) -> None:
        """Test the performance of the construct_call method of DynamicDecorator.

        This test compares the speed of DynamicDecorator.construct_call() with BaseDecorator.construct_call() and a
        normal decorator.
        """

        # Create a normal decorator to compare against
        def normal_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)

            return wrapper

        def test_func(x: int) -> int:
            return x * 2

        # Define the performance test functions
        def construct_dynamic_decorator() -> None:
            decorator = self.UnitTestClass(_return_partial=False)
            decorator.construct_call(test_func)

        def construct_base_decorator() -> None:
            decorator = self.TestBaseDecorator(_return_partial=False)
            decorator.construct_call(test_func)

        def construct_normal_decorator() -> None:
            normal_decorator(test_func)

        # Calculate the mean time in microseconds for the dynamic decorator construction
        dynamic_time = timeit.timeit(construct_dynamic_decorator, number=self.timeit_runs // 10)
        mean_dynamic = dynamic_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the base decorator construction
        base_time = timeit.timeit(construct_base_decorator, number=self.timeit_runs // 10)
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the normal decorator construction
        normal_time = timeit.timeit(construct_normal_decorator, number=self.timeit_runs // 10)
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000

        # Calculate percentages
        dynamic_to_normal_percent = (mean_dynamic / mean_normal) * 100
        dynamic_to_base_percent = (mean_dynamic / mean_base) * 100

        # Print the performance comparison
        print(
            f"\nNormal decorator construction: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"BaseDecorator.construct_call: {mean_base:.3f} μs ({(mean_base / mean_normal):.3f}% "
            f"of normal decorator construction time)",
        )
        print(
            f"DynamicDecorator.construct_call: {mean_dynamic:.3f} μs "
            f"({dynamic_to_normal_percent:.3f}% of normal decorator construction time, "
            f"{dynamic_to_base_percent:.3f}% of BaseDecorator construction time)",
        )

        # Assert that the performance is within acceptable limits
        assert dynamic_to_normal_percent < self.speed_tolerance
        assert dynamic_to_base_percent < self.speed_tolerance * 1.5  # Allow more overhead compared to BaseDecorator

    def test_multiplexed_callback(self) -> None:
        """Test the performance of switching between different callback functions.

        This test measures the performance of the DynamicDecorator when switching between different callback functions,
        which is its main advantage over BaseDecorator.
        """
        # Create a dynamic decorator with multiple callback functions
        decorator = self.UnitTestClass(_return_partial=False)

        # Define different callback functions
        def wrapper1(instance: Any, *args: Any, **kwargs: Any) -> Any:
            # Add 1 to the result
            return instance.call_wrapped(*args, **kwargs) + 1

        def wrapper2(instance: Any, *args: Any, **kwargs: Any) -> Any:
            # Multiply the result by 2
            return instance.call_wrapped(*args, **kwargs) * 2

        # Define a test function
        def test_func(x: int) -> int:
            return x

        # Select the call method
        decorator.call_multiplexer.select("call")

        # Define the performance test functions
        def switch_callbacks() -> None:
            decorator.call = wrapper1  # type: ignore[method-assign]
            decorator.call_multiplexer.select("call")
            decorated1 = decorator.construct_call(test_func)
            result1 = decorated1(5)  # Should be 6 (5 + 1)

            decorator.call = wrapper2  # type: ignore[method-assign]
            decorator.call_multiplexer.select("call")
            decorated2 = decorator.construct_call(test_func)
            result2 = decorated2(5)  # Should be 10 (5 * 2)

            assert result1 == 6
            assert result2 == 10

        # Calculate the mean time in microseconds
        time = timeit.timeit(switch_callbacks, number=self.timeit_runs // 100)
        mean_time = time / (self.timeit_runs // 100) * 1000000

        # Print the performance result
        print(f"\nSwitching between callbacks: {mean_time:.3f} μs")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_time < 500  # 500 microseconds is a reasonable threshold

    def test_edge_case_complex_decorator(self) -> None:
        """Test the performance with an edge case of a complex decorator.

        This test measures the performance overhead when using a more complex decorator with multiple layers of
        wrapping.
        """

        # Create a more complex decorator function
        def complex_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            def outer_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Do some pre-processing
                args_list = list(args)
                if args_list:
                    args_list[0] += 1

                # Call the function
                result = func(*args_list, **kwargs)

                # Do some post-processing
                return result * 2

            return outer_wrapper

        # Create a dynamic decorator with similar functionality
        class ComplexDynamicDecorator(DynamicDecorator):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(lambda x: x)

            def call(self, *args: Any, **kwargs: Any) -> Any:
                """The call implementation.

                Returns:
                    Any: The result.
                """
                # Do some pre-processing
                args_list = list(args)
                if args_list:
                    args_list[0] += 1

                # Call the function
                result = self.call_wrapped(*args_list, **kwargs)

                # Do some post-processing
                return result * 2

            def construct_call(self, func: Callable[..., Any] | None = None, *args: Any, **kwargs: Any) -> Any:
                """Construct the call.

                Returns:
                    Any: The result.
                """
                self.construct(func, *args, **kwargs)
                return self

        # Create a base decorator with similar functionality
        class ComplexBaseDecorator(BaseDecorator):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(lambda x: x)

            def call(self, *args: Any, **kwargs: Any) -> Any:
                """The call implementation.

                Returns:
                    Any: The result.
                """
                # Do some pre-processing
                args_list = list(args)
                if args_list:
                    args_list[0] += 1

                # Call the function
                result = self.call_wrapped(*args_list, **kwargs)

                # Do some post-processing
                return result * 2

            def construct_call(self, func: Callable[..., Any] | None = None, *args: Any, **kwargs: Any) -> Any:
                """Construct the call.

                Returns:
                    Any: The result.
                """
                self.construct(func, *args, **kwargs)
                return self

        # Create instances
        dynamic_decorator = ComplexDynamicDecorator(_return_partial=False)
        base_decorator = ComplexBaseDecorator(_return_partial=False)

        # Define a test function
        def test_func(x: int) -> int:
            return x

        # Define the performance test functions
        def use_dynamic_decorator() -> Any:
            decorated = dynamic_decorator.construct_call(test_func)
            return decorated(5)

        def use_base_decorator() -> Any:
            decorated = base_decorator.construct_call(test_func)
            return decorated(5)

        def use_normal_decorator() -> Any:
            decorated = complex_decorator(test_func)
            return decorated(5)

        # Calculate the mean time in microseconds
        dynamic_time = timeit.timeit(use_dynamic_decorator, number=self.timeit_runs // 10)
        mean_dynamic = dynamic_time / (self.timeit_runs // 10) * 1000000

        base_time = timeit.timeit(use_base_decorator, number=self.timeit_runs // 10)
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        normal_time = timeit.timeit(use_normal_decorator, number=self.timeit_runs // 10)
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000

        # Calculate percentages
        dynamic_to_normal_percent = (mean_dynamic / mean_normal) * 100
        dynamic_to_base_percent = (mean_dynamic / mean_base) * 100

        # Print the performance comparison
        print(f"\nComplex normal decorator: {mean_normal:.3f} μs")
        print(
            f"Complex BaseDecorator: {mean_base:.3f} μs "
            f"({(mean_base / mean_normal):.3f}% of normal decorator time)",
        )
        print(
            f"Complex DynamicDecorator: {mean_dynamic:.3f} μs "
            f"({dynamic_to_normal_percent:.3f}% of normal decorator time, "
            f"{dynamic_to_base_percent:.3f}% of BaseDecorator time)",
        )

        # Assert that the performance is within acceptable limits
        assert dynamic_to_normal_percent < self.speed_tolerance * 2  # Allow more overhead for complex operations
        assert dynamic_to_base_percent < self.speed_tolerance * 1.5  # Allow more overhead compared to BaseDecorator


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
