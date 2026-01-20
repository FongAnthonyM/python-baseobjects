#!/usr/bin/env python
"""dynamiccallable_performance.py
Performance tests for the DynamicCallable, DynamicMethod, and DynamicFunction classes in the baseobjects.functions
package.
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
from baseobjects.functions.dynamiccallable import DynamicCallable, DynamicFunction, DynamicMethod
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestDynamicCallablePerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the DynamicCallable class.

    This test suite measures the performance of various operations on DynamicCallable objects and compares them with
    standard Python implementations.

    Attributes:
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
        UnitTestClass: The class being tested.
    """

    # Class Definitions #
    class TestDynamicCallable(DynamicCallable):
        """A subclass of DynamicCallable for testing purposes."""

        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation.

            Returns:
                Any: The result.
            """
            return self.call_wrapped(*args, **kwargs)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    UnitTestClass: type[TestDynamicCallable] = TestDynamicCallable

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_callable(self) -> "TestDynamicCallablePerformance.TestDynamicCallable":
        """Create a test callable instance for use in tests.

        Returns:
            TestDynamicCallable: An instance of the test class.
        """
        return self.UnitTestClass()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TestDynamicCallable can be created efficiently.

        This test compares the speed of creating DynamicCallable instances with creating standard Python functions.
        """

        # Define the performance test functions
        def create_dynamic_callable() -> None:
            self.UnitTestClass()

        def create_normal_function() -> None:
            lambda x: x * 2

        # Calculate the mean time in microseconds for the dynamic callable creation
        new_time = timeit.timeit(create_dynamic_callable, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function creation
        old_time = timeit.timeit(create_normal_function, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal function creation: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"DynamicCallable creation: {mean_new:.3f} μs ({percent:.3f}% of normal function creation time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_callable: "TestDynamicCallablePerformance.TestDynamicCallable") -> None:
        """Test the performance of the __call__ method of DynamicCallable.

        This test compares the speed of DynamicCallable.__call__() with a normal function.

        Args:
            test_callable: A fixture providing a TestDynamicCallable instance.
        """

        # Create a normal function to compare against
        def normal(x: int) -> int:
            return x * 2

        arg = 5

        # Define the performance test functions
        def call_dynamic_callable() -> None:
            test_callable(arg)

        def call_normal() -> None:
            normal(arg)

        # Calculate the mean time in microseconds for the dynamic callable call
        new_time = timeit.timeit(call_dynamic_callable, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function call
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal function call: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"DynamicCallable call: {mean_new:.3f} μs ({percent:.3f}% of normal function call time)")
        assert percent < self.speed_tolerance

    def test_edge_case_complex_function(self) -> None:
        """Test the performance with an edge case of a complex function.

        This test measures the performance overhead when using a more complex function.
        """

        # Create a more complex function
        def complex_func(x: Any, y: int = 1, z: int = 2, *args: Any, **kwargs: Any) -> Any:
            result = x * y + z
            for arg in args:
                result += arg
            for _key, value in kwargs.items():
                result += value
            return result

        # Create a dynamic callable with the complex function
        complex_callable = DynamicCallable(complex_func)
        complex_callable.call = lambda *args, **kwargs: complex_callable.call_wrapped(*args, **kwargs)  # type: ignore[attr-defined]

        # Define the performance test functions
        def call_dynamic_callable() -> None:
            complex_callable(5, 2, 3, 4, 5, a=6, b=7)

        def call_normal() -> None:
            complex_func(5, 2, 3, 4, 5, a=6, b=7)

        # Calculate the mean time in microseconds for the dynamic callable call
        new_time = timeit.timeit(call_dynamic_callable, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the normal function call
        old_time = timeit.timeit(call_normal, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nComplex function call: {mean_old:.3f} μs")
        print(
            f"DynamicCallable with complex function: {mean_new:.3f} μs ({percent:.3f}% of complex function call time)",
        )
        assert percent < self.speed_tolerance * 1.5  # Allow more overhead for complex functions


class TestDynamicMethodPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the DynamicMethod class.

    This test suite measures the performance of various operations on DynamicMethod objects and compares them with
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
            """Test method.

            Returns:
                int: The result.
            """
            return x * 2

    class TestDynamicMethod(DynamicMethod):
        """A subclass of DynamicMethod for testing purposes."""

        # Magic Methods #
        def __init__(self, instance: Any = None) -> None:
            """Initialize with a simple function and instance."""
            super().__init__(lambda self, x: x * 2, instance=instance)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation.

            Returns:
                Any: The result.
            """
            # Use __func__ to get the unbound function and __self__ to get the instance
            assert self.__func__ is not None
            return self.__func__(self.__self__, *args, **kwargs)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    UnitTestClass: type[TestDynamicMethod] = TestDynamicMethod

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> "TestDynamicMethodPerformance.ConcreteInstanceClass":
        """Create a test class instance for use in tests.

        Returns:
            UnitTestClass: An instance of the test class.
        """
        return self.ConcreteInstanceClass()

    @pytest.fixture
    def test_method(
        self,
        test_class_instance: "TestDynamicMethodPerformance.ConcreteInstanceClass",
    ) -> "TestDynamicMethodPerformance.TestDynamicMethod":
        """Create a test method instance for use in tests.

        Args:
            test_class_instance: A fixture providing a UnitTestClass instance.

        Returns:
            TestDynamicMethod: An instance of the test class.
        """
        return self.UnitTestClass(instance=test_class_instance)

    # Tests
    def test_instance_creation(self, test_class_instance: "TestDynamicMethodPerformance.ConcreteInstanceClass") -> None:
        """Test that instances of TestDynamicMethod can be created efficiently.

        This test compares the speed of creating DynamicMethod instances with accessing
        standard Python methods.

        Args:
            test_class_instance: A fixture providing a UnitTestClass instance.
        """

        # Define the performance test functions
        def create_dynamic_method() -> None:
            self.UnitTestClass(instance=test_class_instance)

        def create_normal_method() -> None:
            _ = test_class_instance.method1

        # Calculate the mean time in microseconds for the dynamic method creation
        new_time = timeit.timeit(create_dynamic_method, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal method access
        old_time = timeit.timeit(create_normal_method, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal method access: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"DynamicMethod creation: {mean_new:.3f} μs ({percent:.3f}% of normal method access time)")
        assert percent < self.speed_tolerance

    def test_call_speed(
        self,
        test_method: "TestDynamicMethodPerformance.TestDynamicMethod",
        test_class_instance: "TestDynamicMethodPerformance.ConcreteInstanceClass",
    ) -> None:
        """Test the performance of the __call__ method of DynamicMethod.

        This test compares the speed of DynamicMethod.__call__() with a normal method call.

        Args:
            test_method: A fixture providing a TestDynamicMethod instance.
            test_class_instance: A fixture providing a UnitTestClass instance.
        """
        arg = 5

        # Define the performance test functions
        def call_dynamic_method() -> None:
            test_method(arg)

        def call_normal_method() -> None:
            test_class_instance.method1(arg)

        # Calculate the mean time in microseconds for the dynamic method call
        new_time = timeit.timeit(call_dynamic_method, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal method call
        old_time = timeit.timeit(call_normal_method, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal method call: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"DynamicMethod call: {mean_new:.3f} μs ({percent:.3f}% of normal method call time)")
        assert percent < self.speed_tolerance

    def test_edge_case_instance_change(self, test_method: "TestDynamicMethodPerformance.TestDynamicMethod") -> None:
        """Test the performance of changing the instance of a DynamicMethod.

        This test measures the performance overhead when changing the instance of a DynamicMethod.

        Args:
            test_method: A fixture providing a TestDynamicMethod instance.
        """
        # Create new instances
        instance1 = self.ConcreteInstanceClass()
        instance2 = self.ConcreteInstanceClass()

        # Define the performance test functions
        def change_instance() -> None:
            test_method.bind_self(instance1)
            test_method.bind_self(instance2)

        # Calculate the mean time in microseconds
        time = timeit.timeit(change_instance, number=self.timeit_runs // 10)
        mean_time = time / (self.timeit_runs // 10) * 1000000

        # Print the performance result
        print(f"\nChanging DynamicMethod instance: {mean_time:.3f} μs")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_time < 200  # 200 microseconds is a reasonable threshold


class TestDynamicFunctionPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the DynamicFunction class.

    This test suite measures the performance of various operations on DynamicFunction objects and compares them with
    standard Python implementations.

    Attributes:
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
        UnitTestClass: The class being tested.
    """

    # Class Definitions #
    class BindingTarget:
        """A class to test method binding."""

        def method1(self, x: int) -> int:
            """Test method.

            Returns:
                int: The result.
            """
            return x * 2

    class TestDynamicFunction(DynamicFunction):
        """A subclass of DynamicFunction for testing purposes."""

        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation.

            Returns:
                Any: The result.
            """
            return self.call_wrapped(*args, **kwargs)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    UnitTestClass: type[TestDynamicFunction] = TestDynamicFunction

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_function(self) -> "TestDynamicFunctionPerformance.TestDynamicFunction":
        """Create a test function instance for use in tests.

        Returns:
            TestDynamicFunction: An instance of the test class.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def test_class_instance(self) -> "TestDynamicFunctionPerformance.BindingTarget":
        """Create a test class instance for use in tests.

        Returns:
            BindingTarget: An instance of the test class.
        """
        return self.BindingTarget()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TestDynamicFunction can be created efficiently.

        This test compares the speed of creating DynamicFunction instances with creating standard Python functions.
        """

        # Define the performance test functions
        def create_dynamic_function() -> None:
            self.UnitTestClass()

        def create_normal_function() -> None:
            lambda x: x * 2

        # Calculate the mean time in microseconds for the dynamic function creation
        new_time = timeit.timeit(create_dynamic_function, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function creation
        old_time = timeit.timeit(create_normal_function, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal function creation: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"DynamicFunction creation: {mean_new:.3f} μs ({percent:.3f}% of normal function creation time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_function: "TestDynamicFunctionPerformance.TestDynamicFunction") -> None:
        """Test the performance of the __call__ method of DynamicFunction.

        This test compares the speed of DynamicFunction.__call__() with a normal function call.

        Args:
            test_function: A fixture providing a TestDynamicFunction instance.
        """

        # Create a normal function to compare against
        def normal(x: int) -> int:
            return x * 2

        arg = 5

        # Define the performance test functions
        def call_dynamic_function() -> None:
            test_function(arg)

        def call_normal() -> None:
            normal(arg)

        # Calculate the mean time in microseconds for the dynamic function call
        new_time = timeit.timeit(call_dynamic_function, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function call
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal function call: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"DynamicFunction call: {mean_new:.3f} μs ({percent:.3f}% of normal function call time)")
        assert percent < self.speed_tolerance

    def test_get_descriptor_speed(
        self,
        test_function: "TestDynamicFunctionPerformance.TestDynamicFunction",
        test_class_instance: "TestDynamicFunctionPerformance.BindingTarget",
    ) -> None:
        """Test the performance of the __get__ method of DynamicFunction.

        This test compares the speed of DynamicFunction.__get__() with a normal method binding.

        Args:
            test_function: A fixture providing a TestDynamicFunction instance.
            test_class_instance: A fixture providing a UnitTestClass instance.
        """

        # Create a class with the dynamic function as a class attribute
        class TestDescriptorClass:
            dynamic_func = test_function

            def normal_method(self, x: int) -> int:
                """A normal method.

                Returns:
                    int: The result.
                """
                return x * 2

        test_descriptor_instance = TestDescriptorClass()

        # Define the performance test functions
        def get_dynamic_function() -> None:
            _ = test_descriptor_instance.dynamic_func

        def get_normal_method() -> None:
            _ = test_descriptor_instance.normal_method

        # Calculate the mean time in microseconds for the dynamic function descriptor
        new_time = timeit.timeit(get_dynamic_function, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal method descriptor
        old_time = timeit.timeit(get_normal_method, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal method descriptor: {mean_old:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"DynamicFunction descriptor: {mean_new:.3f} μs ({percent:.3f}% of normal method descriptor time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
