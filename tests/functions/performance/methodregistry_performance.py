#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" methodregistry_performance.py
Performance tests for the BaseMethodRegistry, BoundMethodRegistry, and MethodRegistry classes in the baseobjects package.
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
from src.baseobjects.functions.methodregistry import BaseMethodRegistry, BoundMethodRegistry, MethodRegistry
from tests.bases.performance.base_performance import ClassPerformanceTest


# Definitions #
# Base Method Register
class TestBaseMethodRegistry(ClassPerformanceTest):
    """Test the performance of the BaseMethodRegistry class.

    This class tests the performance of the BaseMethodRegistry class, which is an abstract registry
    that holds methods.
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

    class_: Type[BaseMethodRegistry] = BaseMethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_register(self) -> BaseMethodRegistry:
        """Create a test registry instance for use in tests.

        Returns:
            BaseMethodRegistry: An instance of the test class.
        """
        register = self.class_()
        register["method1"] = lambda x: x * 2
        register["method2"] = lambda x: x * 3
        return register

    @pytest.fixture
    def test_class_instance(self) -> "TestBaseMethodRegistry.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseMethodRegistry can be created efficiently."""
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

    def test_update_speed(self, test_register: BaseMethodRegistry) -> None:
        """Test the performance of the update method of BaseMethodRegistry.

        This test compares the speed of BaseMethodRegistry.update() with a dictionary update.

        Args:
            test_register: A fixture providing a BaseMethodRegistry instance.
        """
        # Create a dictionary to compare against
        methods = {"method1": lambda x: x * 2, "method2": lambda x: x * 3}
        
        # Define new methods to add
        new_methods = {"method3": lambda x: x * 4, "method4": lambda x: x * 5}
        
        # Define the performance test functions
        def update_register() -> None:
            test_register.update(new_methods)

        def update_dict() -> None:
            methods.update(new_methods)

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


# Bound Method Register
class TestBoundMethodRegistry(ClassPerformanceTest):
    """Test the performance of the BoundMethodRegistry class.

    This class tests the performance of the BoundMethodRegistry class, which is a BaseMethodRegistry
    that is bound to another object.
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

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[BoundMethodRegistry] = BoundMethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> "TestBoundMethodRegistry.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    @pytest.fixture
    def base_register(self) -> BaseMethodRegistry:
        """Create a base registry instance for use in tests.

        Returns:
            BaseMethodRegistry: An instance of the BaseMethodRegister class.
        """
        register = BaseMethodRegistry()
        register["method1"] = lambda self, x: x * 2
        register["method2"] = lambda self, x: x * 3
        return register

    @pytest.fixture
    def test_register(self, base_register: BaseMethodRegistry, test_class_instance: "TestBoundMethodRegistry.TestClass") -> BoundMethodRegistry:
        """Create a test registry instance for use in tests.

        Args:
            base_register: A fixture providing a BaseMethodRegistry instance.
            test_class_instance: A fixture providing a TestClass instance.

        Returns:
            BoundMethodRegistry: An instance of the test class.
        """
        return self.class_(registry=base_register, instance=test_class_instance)

    # Tests
    def test_instance_creation(self, base_register: BaseMethodRegistry, test_class_instance: "TestBoundMethodRegistry.TestClass") -> None:
        """Test that instances of BoundMethodRegistry can be created efficiently.

        Args:
            base_register: A fixture providing a BaseMethodRegistry instance.
            test_class_instance: A fixture providing a TestClass instance.
        """
        # Define the performance test functions
        def create_bound_register() -> None:
            self.class_(registry=base_register, instance=test_class_instance)

        def create_dict_with_methods() -> None:
            {
                "method1": lambda x: test_class_instance.method1(x),
                "method2": lambda x: test_class_instance.method2(x)
            }

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_bound_register, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_dict_with_methods, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Method Register
class TestMethodRegistry(ClassPerformanceTest):
    """Test the performance of the MethodRegistry class.

    This class tests the performance of the MethodRegistry class, which is a registry
    that holds functions and binds appropriately.
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

    class TestDescriptorClass:
        """A class to test descriptor protocol."""
        
        register = None  # Will be set in the fixture

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[MethodRegistry] = MethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_register(self) -> MethodRegistry:
        """Create a test registry instance for use in tests.

        Returns:
            MethodRegistry: An instance of the test class.
        """
        register = self.class_()
        register["method1"] = lambda self, x: x * 2
        register["method2"] = lambda self, x: x * 3
        return register

    @pytest.fixture
    def test_class_instance(self) -> "TestMethodRegistry.TestClass":
        """Create a test class instance for use in tests.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    @pytest.fixture
    def test_descriptor_class(self, test_register: MethodRegistry) -> Type["TestMethodRegistry.TestDescriptorClass"]:
        """Create a test descriptor class for use in tests.

        Args:
            test_register: A fixture providing a MethodRegistry instance.

        Returns:
            Type[TestDescriptorClass]: The test descriptor class.
        """
        self.TestDescriptorClass.register = test_register
        return self.TestDescriptorClass

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of MethodRegistry can be created efficiently."""
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

    def test_get_descriptor_speed(self, test_descriptor_class: Type["TestMethodRegistry.TestDescriptorClass"], test_class_instance: "TestMethodRegistry.TestClass") -> None:
        """Test the performance of the __get__ method of MethodRegistry.

        This test compares the speed of MethodRegistry.__get__() with a normal method binding.

        Args:
            test_descriptor_class: A fixture providing the TestDescriptorClass.
            test_class_instance: A fixture providing a TestClass instance.
        """
        # Create an instance of the descriptor class
        test_descriptor_instance = test_descriptor_class()
        
        # Define the performance test functions
        def get_method_register() -> None:
            test_descriptor_instance.register

        def get_normal_method() -> None:
            test_class_instance.method1

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(get_method_register, number=self.timeit_runs)
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