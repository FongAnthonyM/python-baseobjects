#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" dynamiccallable_performance.py
Performance tests for the DynamicCallable, DynamicMethod, and DynamicFunction classes in the baseobjects package.
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
from typing import Type, Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions.dynamiccallable import DynamicCallable, DynamicMethod, DynamicFunction
from tests.bases.performance.base_performance import ClassPerformanceTest


# Definitions #
# Dynamic Callable
class TestDynamicCallable(ClassPerformanceTest):
    """Test the performance of the DynamicCallable class.

    This class tests the performance of the DynamicCallable class, which is a subclass of BaseCallable
    that provides dynamic calling capabilities.
    """
    # Class Definitions #
    class TestDynamicCallable(DynamicCallable):
        """A subclass of DynamicCallable for testing purposes."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation."""
            return self.func(*args, **kwargs)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[TestDynamicCallable] = TestDynamicCallable

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_callable(self) -> "TestDynamicCallable.TestDynamicCallable":
        """Create a test callable instance for use in tests.

        Returns:
            TestDynamicCallable: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TestDynamicCallable can be created efficiently."""
        # Define the performance test functions
        def create_dynamic_callable() -> None:
            self.class_()

        def create_normal_function() -> None:
            lambda x: x * 2

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_dynamic_callable, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal_function, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_callable: "TestDynamicCallable.TestDynamicCallable") -> None:
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

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_dynamic_callable, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Dynamic Method
class TestDynamicMethod(ClassPerformanceTest):
    """Test the performance of the DynamicMethod class.

    This class tests the performance of the DynamicMethod class, which is a subclass of DynamicCallable
    and BaseMethod for method-specific functionality.
    """
    # Class Definitions #
    class TestClass:
        """A class to test method binding."""
        
        def method1(self, x: int) -> int:
            """Test method."""
            return x * 2

    class TestDynamicMethod(DynamicMethod):
        """A subclass of DynamicMethod for testing purposes."""
        # Magic Methods #
        def __init__(self, instance: Any = None) -> None:
            """Initialize with a simple function and instance."""
            super().__init__(lambda self, x: x * 2, instance=instance)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation."""
            return self.func(self.instance, *args, **kwargs)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[TestDynamicMethod] = TestDynamicMethod

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> "TestDynamicMethod.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    @pytest.fixture
    def test_method(self, test_class_instance: "TestDynamicMethod.TestClass") -> "TestDynamicMethod.TestDynamicMethod":
        """Create a test method instance for use in tests.

        Args:
            test_class_instance: A fixture providing a TestClass instance.

        Returns:
            TestDynamicMethod: An instance of the test class.
        """
        return self.class_(instance=test_class_instance)

    # Tests
    def test_instance_creation(self, test_class_instance: "TestDynamicMethod.TestClass") -> None:
        """Test that instances of TestDynamicMethod can be created efficiently.

        Args:
            test_class_instance: A fixture providing a TestClass instance.
        """
        # Define the performance test functions
        def create_dynamic_method() -> None:
            self.class_(instance=test_class_instance)

        def create_normal_method() -> None:
            test_class_instance.method1

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_dynamic_method, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal_method, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_method: "TestDynamicMethod.TestDynamicMethod", test_class_instance: "TestDynamicMethod.TestClass") -> None:
        """Test the performance of the __call__ method of DynamicMethod.

        This test compares the speed of DynamicMethod.__call__() with a normal method call.

        Args:
            test_method: A fixture providing a TestDynamicMethod instance.
            test_class_instance: A fixture providing a TestClass instance.
        """
        arg = 5

        # Define the performance test functions
        def call_dynamic_method() -> None:
            test_method(arg)

        def call_normal_method() -> None:
            test_class_instance.method1(arg)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_dynamic_method, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_normal_method, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Dynamic Function
class TestDynamicFunction(ClassPerformanceTest):
    """Test the performance of the DynamicFunction class.

    This class tests the performance of the DynamicFunction class, which is a subclass of DynamicCallable
    and BaseFunction for function-specific functionality.
    """
    # Class Definitions #
    class TestClass:
        """A class to test method binding."""
        
        def method1(self, x: int) -> int:
            """Test method."""
            return x * 2

    class TestDynamicFunction(DynamicFunction):
        """A subclass of DynamicFunction for testing purposes."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The call implementation."""
            return self.func(*args, **kwargs)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[TestDynamicFunction] = TestDynamicFunction

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_function(self) -> "TestDynamicFunction.TestDynamicFunction":
        """Create a test function instance for use in tests.

        Returns:
            TestDynamicFunction: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def test_class_instance(self) -> "TestDynamicFunction.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TestDynamicFunction can be created efficiently."""
        # Define the performance test functions
        def create_dynamic_function() -> None:
            self.class_()

        def create_normal_function() -> None:
            lambda x: x * 2

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_dynamic_function, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal_function, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_function: "TestDynamicFunction.TestDynamicFunction") -> None:
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

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_dynamic_function, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_get_descriptor_speed(self, test_function: "TestDynamicFunction.TestDynamicFunction", test_class_instance: "TestDynamicFunction.TestClass") -> None:
        """Test the performance of the __get__ method of DynamicFunction.

        This test compares the speed of DynamicFunction.__get__() with a normal method binding.

        Args:
            test_function: A fixture providing a TestDynamicFunction instance.
            test_class_instance: A fixture providing a TestClass instance.
        """
        # Create a class with the dynamic function as a class attribute
        class TestDescriptorClass:
            dynamic_func = test_function
            
            def normal_method(self, x: int) -> int:
                return x * 2
        
        test_descriptor_instance = TestDescriptorClass()
        
        # Define the performance test functions
        def get_dynamic_function() -> None:
            test_descriptor_instance.dynamic_func

        def get_normal_method() -> None:
            test_descriptor_instance.normal_method

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(get_dynamic_function, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(get_normal_method, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])