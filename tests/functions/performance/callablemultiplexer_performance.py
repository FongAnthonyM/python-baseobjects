#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" callablemultiplexer_performance.py
Performance tests for the CallableMultiplexer and MethodMultiplexer classes in the baseobjects package.
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
from src.baseobjects.functions.callablemultiplexer import CallableMultiplexer, MethodMultiplexer
from tests.bases.performance.base_performance import ClassPerformanceTest


# Definitions #
# Callable Multiplexer
class TestCallableMultiplexer(ClassPerformanceTest):
    """Test the performance of the CallableMultiplexer class.

    This class tests the performance of the CallableMultiplexer class, which provides a way
    to multiplex between different callable objects.
    """
    # Class Definitions #
    class TestClass:
        """A class to test method binding."""
        
        def method1(self, x: int) -> int:
            """First test method."""
            return x * 2
            
        def method2(self, x: int) -> int:
            """Second test method."""
            return x * 3

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[CallableMultiplexer] = CallableMultiplexer

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_multiplexer(self) -> CallableMultiplexer:
        """Create a test multiplexer instance for use in tests.

        Returns:
            CallableMultiplexer: An instance of the test class.
        """
        multiplexer = self.class_()
        multiplexer.add_function("func1", lambda x: x * 2)
        multiplexer.add_function("func2", lambda x: x * 3)
        multiplexer.select("func1")
        return multiplexer

    @pytest.fixture
    def test_class_instance(self) -> "TestCallableMultiplexer.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of CallableMultiplexer can be created efficiently."""
        # Define the performance test functions
        def create_multiplexer() -> None:
            self.class_()

        def create_dict() -> None:
            {"func1": lambda x: x * 2, "func2": lambda x: x * 3}

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_dict, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
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

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_select_speed(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test the performance of the select method of CallableMultiplexer.

        This test compares the speed of CallableMultiplexer.select() with a dictionary lookup.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # Create a dictionary to compare against
        funcs = {"func1": lambda x: x * 2, "func2": lambda x: x * 3}
        
        # Define the performance test functions
        def select_multiplexer() -> None:
            test_multiplexer.select("func2")

        def select_dict() -> None:
            _ = funcs["func2"]

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(select_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(select_dict, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
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

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(add_to_multiplexer, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(add_to_dict, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Method Multiplexer
class TestMethodMultiplexer(ClassPerformanceTest):
    """Test the performance of the MethodMultiplexer class.

    This class tests the performance of the MethodMultiplexer class, which is a subclass of
    CallableMultiplexer that provides method-specific functionality.
    """
    # Class Definitions #
    class TestClass:
        """A class to test method binding."""
        
        def method1(self, x: int) -> int:
            """First test method."""
            return x * 2
            
        def method2(self, x: int) -> int:
            """Second test method."""
            return x * 3

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[MethodMultiplexer] = MethodMultiplexer

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> "TestMethodMultiplexer.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    @pytest.fixture
    def test_multiplexer(self, test_class_instance: "TestMethodMultiplexer.TestClass") -> MethodMultiplexer:
        """Create a test multiplexer instance for use in tests.

        Args:
            test_class_instance: A fixture providing a TestClass instance.

        Returns:
            MethodMultiplexer: An instance of the test class.
        """
        multiplexer = self.class_(instance=test_class_instance)
        multiplexer.add_method("method1", test_class_instance.method1)
        multiplexer.add_method("method2", test_class_instance.method2)
        multiplexer.select("method1")
        return multiplexer

    # Tests
    def test_instance_creation(self, test_class_instance: "TestMethodMultiplexer.TestClass") -> None:
        """Test that instances of MethodMultiplexer can be created efficiently.

        Args:
            test_class_instance: A fixture providing a TestClass instance.
        """
        # Define the performance test functions
        def create_multiplexer() -> None:
            self.class_(instance=test_class_instance)

        def create_dict() -> None:
            {"method1": test_class_instance.method1, "method2": test_class_instance.method2}

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_dict, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_multiplexer: MethodMultiplexer, test_class_instance: "TestMethodMultiplexer.TestClass") -> None:
        """Test the performance of the __call__ method of MethodMultiplexer.

        This test compares the speed of MethodMultiplexer.__call__() with a direct method call.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
            test_class_instance: A fixture providing a TestClass instance.
        """
        arg = 5

        # Define the performance test functions
        def call_multiplexer() -> None:
            test_multiplexer(arg)

        def call_normal() -> None:
            test_class_instance.method1(arg)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_multiplexer, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])