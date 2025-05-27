#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" functionregistry_performance.py
Performance tests for the FunctionRegistry class in the baseobjects package.
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
from src.baseobjects.functions.functionregistry import FunctionRegistry
from tests.bases.performance.base_performance import ClassPerformanceTest


# Definitions #
# Function Register
class TestFunctionRegistry(ClassPerformanceTest):
    """Test the performance of the FunctionRegistry class.

    This class tests the performance of the FunctionRegistry class, which is a registry
    that holds functions.
    """
    # Class Definitions #
    class TestClass:
        """A class with methods for testing."""
        
        def method1(self, x: int) -> int:
            """First test method."""
            return x * 2
            
        def method2(self, x: int) -> int:
            """Second test method."""
            return x * 3
            
        def method3(self, x: int) -> int:
            """Third test method."""
            return x * 4

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[FunctionRegistry] = FunctionRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_register(self) -> FunctionRegistry:
        """Create a test registry instance for use in tests.

        Returns:
            FunctionRegistry: An instance of the test class.
        """
        register = self.class_()
        register["func1"] = lambda x: x * 2
        register["func2"] = lambda x: x * 3
        return register

    @pytest.fixture
    def test_class_instance(self) -> "TestFunctionRegistry.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of FunctionRegistry can be created efficiently."""
        # Define the performance test functions
        def create_register() -> None:
            self.class_()

        def create_dict() -> None:
            {}

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_register, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_dict, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_update_speed(self, test_register: FunctionRegistry) -> None:
        """Test the performance of the update method of FunctionRegistry.

        This test compares the speed of FunctionRegistry.update() with a dictionary update.

        Args:
            test_register: A fixture providing a FunctionRegistry instance.
        """
        # Create a dictionary to compare against
        funcs = {"func1": lambda x: x * 2, "func2": lambda x: x * 3}
        
        # Define new functions to add
        new_funcs = {"func3": lambda x: x * 4, "func4": lambda x: x * 5}
        
        # Define the performance test functions
        def update_register() -> None:
            test_register.update(new_funcs)

        def update_dict() -> None:
            funcs.update(new_funcs)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(update_register, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(update_dict, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_update_from_object_speed(self, test_register: FunctionRegistry, test_class_instance: "TestFunctionRegistry.TestClass") -> None:
        """Test the performance of the update_from_object method of FunctionRegistry.

        This test compares the speed of FunctionRegistry.update_from_object() with a manual dictionary update.

        Args:
            test_register: A fixture providing a FunctionRegistry instance.
            test_class_instance: A fixture providing a TestClass instance.
        """
        # Create a dictionary to compare against
        funcs = {"func1": lambda x: x * 2, "func2": lambda x: x * 3}
        
        # Define the performance test functions
        def update_from_object() -> None:
            test_register.update_from_object(test_class_instance)

        def manual_update() -> None:
            for name in dir(test_class_instance):
                attr = getattr(test_class_instance, name, None)
                if callable(attr) and not name.startswith("__"):
                    funcs[name] = attr

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(update_from_object, number=self.timeit_runs // 100)
        mean_new = new_time / (self.timeit_runs // 100) * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(manual_update, number=self.timeit_runs // 100)
        mean_old = old_time / (self.timeit_runs // 100) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_update_from_objects_speed(self, test_register: FunctionRegistry, test_class_instance: "TestFunctionRegistry.TestClass") -> None:
        """Test the performance of the update_from_objects method of FunctionRegistry.

        This test compares the speed of FunctionRegistry.update_from_objects() with multiple manual dictionary updates.

        Args:
            test_register: A fixture providing a FunctionRegistry instance.
            test_class_instance: A fixture providing a TestClass instance.
        """
        # Create a second test class instance
        test_class_instance2 = self.TestClass()
        
        # Create a dictionary to compare against
        funcs = {"func1": lambda x: x * 2, "func2": lambda x: x * 3}
        
        # Define the performance test functions
        def update_from_objects() -> None:
            test_register.update_from_objects(test_class_instance, test_class_instance2)

        def manual_updates() -> None:
            for obj in [test_class_instance, test_class_instance2]:
                for name in dir(obj):
                    attr = getattr(obj, name, None)
                    if callable(attr) and not name.startswith("__"):
                        funcs[name] = attr

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(update_from_objects, number=self.timeit_runs // 100)
        mean_new = new_time / (self.timeit_runs // 100) * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(manual_updates, number=self.timeit_runs // 100)
        mean_old = old_time / (self.timeit_runs // 100) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])