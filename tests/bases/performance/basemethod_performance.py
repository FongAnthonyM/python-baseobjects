#!/usr/bin/env python
"""basemethod_performance.py
Performance tests for the BaseMethod class in the baseobjects.bases package.
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
from types import MethodType
from typing import Any
from weakref import ReferenceType

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases import BaseMethod
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Functions #
def simple_method(self, x: int) -> int:
    """A simple function that doubles its input."""
    return x * 2, self


class NormalMethod:
    """A normal Python method-like object for comparison with BaseMethod."""

    def __init__(self, func: Callable | None = None, instance: Any = None, owner: type | None = None) -> None:
        """Initialize with a function, instance, and owner."""
        self.func = func or simple_method
        self._self = None if instance is None else ReferenceType(instance)
        self.__owner__ = owner

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the wrapped function with the bound instance."""
        if self._self is not None:
            instance = self._self()
            if instance is not None:
                return self.func(instance, *args, **kwargs)
        return self.func(*args, **kwargs)


class TestBaseMethodPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseMethod class.

    This test suite measures the performance of various operations on BaseMethod objects
    and compares them with standard Python implementations.
    """

    # Class Definitions #
    class TestMethod(BaseMethod):
        """A subclass of BaseMethod for testing purposes."""

        def __init__(self, func: Callable | None = None, instance: Any = None, owner: type | None = None) -> None:
            """Initialize with a function, instance, and owner."""
            super().__init__(func or simple_method, instance, owner)

    class ExampleClass:
        """A class to own methods for testing."""

        def normal_method(self, x: int) -> int:
            """A normal method."""
            return x * 2

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def example_instance(self) -> "TestBaseMethodPerformance.ExampleClass":
        """Create an instance of the example class for testing.

        Returns:
            ExampleClass: An instance of the example class.
        """
        return self.ExampleClass()

    @pytest.fixture
    def test_method(
        self,
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> "TestBaseMethodPerformance.TestMethod":
        """Create a test method instance for use in tests.

        Returns:
            TestMethod: An instance of the test class.
        """
        return self.TestMethod(instance=example_instance)

    @pytest.fixture
    def test_normal_method(self, example_instance: "TestBaseMethodPerformance.ExampleClass") -> NormalMethod:
        """Create a normal method instance for comparison.

        Returns:
            NormalMethod: A standard Python method-like object.
        """
        return NormalMethod(instance=example_instance)

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating instances of the BaseMethod class.

        This test compares the speed of creating BaseMethod instances with creating
        standard Python method-like objects.
        """

        def create_base_method() -> None:
            self.TestMethod(simple_method)

        # Calculate the mean time in microseconds for BaseMethod
        base_time = timeit.timeit(create_base_method, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Print the performance comparison
        print(f"\nBaseMethod instance creation: {mean_base:.3f} μs or {mean_base / self.call_speed:.3f} cu")

    def test_call_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        test_normal_method: NormalMethod,
    ) -> None:
        """Test the performance of the __call__ method of BaseMethod.

        This test compares the speed of BaseMethod.__call__() with a normal method-like object.

        Args:
            test_method: A fixture providing a TestMethod instance.
            test_normal_method: A fixture providing a NormalMethod instance.
        """
        arg = 5

        def call_base() -> None:
            test_method(arg)

        def call_normal() -> None:
            test_normal_method(arg)

        # Calculate the mean time in microseconds for BaseMethod
        base_time = timeit.timeit(call_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for NormalMethod
        normal_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal method call: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseMethod.__call__: {mean_base:.3f} μs ({percent:.3f}% of normal method call time)")
        assert percent < self.speed_tolerance

    def test_bind_self_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> None:
        """Test the performance of the bind_self method of BaseMethod.

        This test compares the speed of BaseMethod.bind_self() with creating a method using MethodType.

        Args:
            test_method: A fixture providing a TestMethod instance.
            example_instance: A fixture providing an instance of the example class.
        """

        def bind_base() -> None:
            test_method.bind_self(example_instance)

        def bind_standard() -> None:
            MethodType(simple_method, example_instance)

        # Calculate the mean time in microseconds for BaseMethod.bind_self
        base_time = timeit.timeit(bind_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for standard method binding
        standard_time = timeit.timeit(bind_standard, number=self.timeit_runs)
        mean_standard = standard_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_standard) * 100

        # Print the performance comparison
        print(
            f"\nStandard method binding: {mean_standard:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseMethod.bind_self: {mean_base:.3f} μs ({percent:.3f}% of standard method binding time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for method creation

    def test_bind_to_attribute_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> None:
        """Test the performance of the bind_to_attribute method of BaseMethod.

        This test measures the time it takes to bind a method to an instance and set it as an attribute.

        Args:
            test_method: A fixture providing a TestMethod instance.
            example_instance: A fixture providing an instance of the example class.
        """

        def bind_to_attribute() -> None:
            # Create a new instance each time to avoid attribute already existing
            obj = self.ExampleClass()
            test_method.bind_to_attribute(obj, name="test_method")

        # Calculate the mean time in microseconds for BaseMethod.bind_to_attribute
        bind_time = timeit.timeit(bind_to_attribute, number=self.timeit_runs)
        mean_bind = bind_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nBaseMethod.bind_to_attribute: {mean_bind:.3f} μs or {mean_bind / self.call_speed:.3f} cu")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_bind < 200  # 200 microseconds is a reasonable threshold

    def test_bound_method_call_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> None:
        """Test the performance of calling a bound BaseMethod.

        This test compares the speed of calling a bound BaseMethod with a normal method.

        Args:
            test_method: A fixture providing a TestMethod instance.
            example_instance: A fixture providing an instance of the example class.
        """
        bound_method = test_method.bind_self(example_instance)
        arg = 5

        def call_bound() -> None:
            bound_method(arg)

        def call_normal() -> None:
            example_instance.normal_method(arg)

        # Calculate the mean time in microseconds for bound method call
        bound_time = timeit.timeit(call_bound, number=self.timeit_runs)
        mean_bound = bound_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal method call
        normal_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_bound / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal method call: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Bound BaseMethod call: {mean_bound:.3f} μs ({percent:.3f}% of normal method call time)")
        assert percent < self.speed_tolerance * 1.5  # Allow some overhead for method call

    def test_descriptor_protocol_performance(self, test_method: "TestBaseMethodPerformance.TestMethod") -> None:
        """Test the performance of the descriptor protocol (__get__) of BaseMethod.

        This test measures the time it takes to get a method from an instance using the descriptor protocol.

        Args:
            test_method: A fixture providing a TestMethod instance.
        """

        class TestObject:
            pass

        obj = TestObject()
        obj.method = test_method

        def get_descriptor() -> None:
            obj.method  # This calls __get__

        # Calculate the mean time in microseconds for descriptor protocol
        descriptor_time = timeit.timeit(get_descriptor, number=self.timeit_runs)
        mean_descriptor = descriptor_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nBaseMethod.__get__: {mean_descriptor:.3f} μs or {mean_descriptor / self.call_speed:.3f} cu")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_descriptor < 100  # 100 microseconds is a reasonable threshold

    def test_call_binding_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> None:
        """Test the performance of the call_binding method of BaseMethod.

        This test measures the time it takes to call a method with binding.

        Args:
            test_method: A fixture providing a TestMethod instance.
            example_instance: A fixture providing an instance of the example class.
        """
        bound_method = test_method.bind_self(example_instance)
        arg = 5

        def call_binding() -> None:
            bound_method.call_binding(arg)

        def call_normal() -> None:
            bound_method(arg)

        # Calculate the mean time in microseconds for call_binding
        binding_time = timeit.timeit(call_binding, number=self.timeit_runs)
        mean_binding = binding_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal call
        normal_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_binding / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal bound method call: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseMethod.call_binding: {mean_binding:.3f} μs ({percent:.3f}% of normal bound method call time)")
        assert percent < self.speed_tolerance * 1.5  # Allow some overhead for binding call

    def test_pickling_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> None:
        """Test the performance of pickling and unpickling BaseMethod objects.

        This test measures the time it takes to get and set the state of a BaseMethod object.

        Args:
            test_method: A fixture providing a TestMethod instance.
            example_instance: A fixture providing an instance of the example class.
        """
        bound_method = test_method.bind_self(example_instance)

        def get_state() -> None:
            bound_method.__getstate__()

        def set_state() -> None:
            state = bound_method.__getstate__()
            bound_method.__setstate__(state)

        # Calculate the mean time in microseconds for __getstate__
        get_time = timeit.timeit(get_state, number=self.timeit_runs)
        mean_get = get_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for __setstate__
        set_time = timeit.timeit(set_state, number=self.timeit_runs)
        mean_set = set_time / self.timeit_runs * 1000000

        # Print the performance results
        print(f"\nBaseMethod.__getstate__: {mean_get:.3f} μs or {mean_get / self.call_speed:.3f} cu")
        print(f"BaseMethod.__setstate__: {mean_set:.3f} μs or {mean_set / self.call_speed:.3f} cu")

        # No direct comparison, just ensure they're reasonably fast
        assert mean_get < 100  # 100 microseconds is a reasonable threshold
        assert mean_set < 100  # 100 microseconds is a reasonable threshold

    def test_is_binding_flag_performance(self) -> None:
        """Test the performance impact of the is_binding flag.

        This test compares the speed of binding with is_binding=True versus is_binding=False.
        """
        # Create methods with different is_binding flags
        binding_method = self.TestMethod()
        binding_method.is_binding = True

        non_binding_method = self.TestMethod()
        non_binding_method.is_binding = False

        obj = self.ExampleClass()

        def bind_with_binding() -> None:
            binding_method.bind_self(obj)

        def bind_without_binding() -> None:
            non_binding_method.bind_self(obj)

        # Calculate the mean time in microseconds for binding with is_binding=True
        binding_time = timeit.timeit(bind_with_binding, number=self.timeit_runs)
        mean_binding = binding_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for binding with is_binding=False
        non_binding_time = timeit.timeit(bind_without_binding, number=self.timeit_runs)
        mean_non_binding = non_binding_time / self.timeit_runs * 1000000
        percent = (mean_binding / mean_non_binding) * 100

        # Print the performance comparison
        print(
            f"\nBinding with is_binding=False: {mean_non_binding:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Binding with is_binding=True: {mean_binding:.3f} μs ({percent:.3f}% of non-binding time)")
        # The performance should be similar or binding might be slightly slower due to extra operations
        assert percent < 150  # Allow up to 50% overhead for binding operations

    def test_large_argument_list_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> None:
        """Test the performance of BaseMethod with large argument lists.

        This test compares the speed of BaseMethod.__call__() with a normal method
        when passing a large number of arguments.

        Args:
            test_method: A fixture providing a TestMethod instance.
            example_instance: A fixture providing an instance of the example class.
        """

        # Create a function that accepts many arguments
        def many_args_function(self, *args: Any, **kwargs: Any) -> int:
            return len(args) + len(kwargs)

        # Create a class with a normal method that accepts many arguments
        class ManyArgsClass:
            def many_args_method(self, *args: Any, **kwargs: Any) -> int:
                return len(args) + len(kwargs)

        # Create instances for testing
        many_args_instance = ManyArgsClass()
        base_method = self.TestMethod(many_args_function, example_instance)

        # Create a large list of arguments and a large dict of keyword arguments
        args = list(range(50))
        kwargs = {f"key_{i}": i for i in range(50)}

        def call_normal_large_args() -> None:
            many_args_instance.many_args_method(*args, **kwargs)

        def call_base_large_args() -> None:
            base_method(*args, **kwargs)

        # Calculate the mean time in microseconds for normal method with large args
        normal_time = timeit.timeit(call_normal_large_args, number=self.timeit_runs // 10)  # Reduce runs for large args
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for BaseMethod with large args
        base_time = timeit.timeit(call_base_large_args, number=self.timeit_runs // 10)  # Reduce runs for large args
        mean_base = base_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal method with large args: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseMethod with large args: {mean_base:.3f} μs ({percent:.3f}% of normal method with large args time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for large argument processing

    def test_nested_method_calls_performance(
        self,
        test_method: "TestBaseMethodPerformance.TestMethod",
        example_instance: "TestBaseMethodPerformance.ExampleClass",
    ) -> None:
        """Test the performance of BaseMethod with deeply nested method calls.

        This test measures the performance impact of calling a BaseMethod that calls another BaseMethod,
        and compares it with nested normal method calls.

        Args:
            test_method: A fixture providing a TestMethod instance.
            example_instance: A fixture providing an instance of the example class.
        """

        # Create a chain of nested methods
        class NestedMethodsClass:
            def inner_method(self, x: int) -> int:
                return x * 2

            def outer_method(self, x: int) -> int:
                return self.inner_method(x)

        # Create instances for testing
        nested_instance = NestedMethodsClass()

        # Create BaseMethod instances
        inner_method = self.TestMethod(NestedMethodsClass.inner_method, nested_instance)

        # Create a BaseMethod that will call the inner BaseMethod
        def outer_function(self, x: int) -> int:
            return inner_method(x)

        outer_method = self.TestMethod(outer_function, nested_instance)

        arg = 5

        def call_nested_normal() -> None:
            nested_instance.outer_method(arg)

        def call_nested_base() -> None:
            outer_method(arg)

        # Calculate the mean time in microseconds for nested normal method calls
        normal_time = timeit.timeit(call_nested_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for nested BaseMethod calls
        base_time = timeit.timeit(call_nested_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNested normal method calls: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Nested BaseMethod calls: {mean_base:.3f} μs ({percent:.3f}% of nested normal method calls time)")
        assert percent < self.speed_tolerance * 1.5  # Allow some overhead for nested calls

    def test_rebinding_performance(self, test_method: "TestBaseMethodPerformance.TestMethod") -> None:
        """Test the performance of rebinding a BaseMethod to different instances.

        This test measures the time it takes to rebind a BaseMethod to different instances
        and compares it with creating new method bindings.

        Args:
            test_method: A fixture providing a TestMethod instance.
        """
        # Create multiple instances for rebinding
        instance1 = self.ExampleClass()
        instance2 = self.ExampleClass()
        instance3 = self.ExampleClass()

        # Bind initially to instance1
        bound_method = test_method.bind_self(instance1)

        def rebind_method() -> None:
            # Rebind to instance2, then instance3, then back to instance1
            bound_method.bind_self(instance2)
            bound_method.bind_self(instance3)
            bound_method.bind_self(instance1)

        def create_new_bindings() -> None:
            # Create new bindings each time
            test_method.bind_self(instance2)
            test_method.bind_self(instance3)
            test_method.bind_self(instance1)

        # Calculate the mean time in microseconds for rebinding
        rebind_time = timeit.timeit(rebind_method, number=self.timeit_runs)
        mean_rebind = rebind_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for creating new bindings
        new_binding_time = timeit.timeit(create_new_bindings, number=self.timeit_runs)
        mean_new_binding = new_binding_time / self.timeit_runs * 1000000
        percent = (mean_rebind / mean_new_binding) * 100

        # Print the performance comparison
        print(
            f"\nCreating new bindings: {mean_new_binding:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Rebinding existing method: {mean_rebind:.3f} μs ({percent:.3f}% of new binding creation time)")
        # Rebinding should be faster than creating new bindings
        assert percent < 100  # Rebinding should be less than 100% of the time to create new bindings


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
