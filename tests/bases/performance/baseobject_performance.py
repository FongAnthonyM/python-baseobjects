#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" base_performance.py
Performance tests for the BaseObject class in the baseobjects package.
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
import copy
import timeit
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseObject
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base Object
class TestBaseObject(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseObject class.

    This class tests the performance of the BaseObject class, which is the base class for all objects in the baseobjects
    package. It creates a test subclass of BaseObject to test with.
    """
    # Class Definitions #
    class BaseTestObject(BaseObject):
        """A subclass of BaseObject for testing purposes.

        This class has both mutable and immutable attributes to test copying behavior.
        """
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with immutable and mutable attributes."""
            self.immutable: int = 0
            self.mutable: dict = {}

    class NormalObject(object):
        """A normal Python object for comparison with BaseObject.

        This class has the same attributes as BaseTestObject but inherits from object.
        """
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with immutable and mutable attributes."""
            self.immutable: int = 0
            self.mutable: dict = {}

    # Attributes #
    class_: Type[BaseTestObject] = BaseTestObject

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestBaseObject.BaseTestObject":
        """Create a test object instance for use in tests.

        Returns:
            BaseTestObject: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test that instances of BaseTestObject can be created efficiently.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        assert test_object is not None

    def test_copy_speed(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test the performance of the copy method of BaseObject.

        This test compares the speed of BaseObject.copy() with the standard copy.copy() function.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        normal = self.NormalObject()

        def normal_copy() -> None:
            copy.copy(normal)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(test_object.copy, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(normal_copy, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_deepcopy_speed(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test the performance of the deepcopy method of BaseObject.

        This test compares the speed of BaseObject.deepcopy() with the standard copy.deepcopy() function.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        normal = self.NormalObject()

        def normal_deepcopy() -> None:
            copy.deepcopy(normal)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(test_object.deepcopy, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(normal_deepcopy, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_construct_speed(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test the performance of the construct method of BaseObject.

        This test compares the speed of BaseObject.construct() with a direct attribute assignment.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        normal = self.NormalObject()

        def normal_construct() -> None:
            # Simulate construct by setting attributes directly
            normal.immutable = 0
            normal.mutable = {}

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(test_object.construct, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(normal_construct, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_copy_vs_dunder_copy(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test the performance difference between copy() and __copy__() methods.

        This test compares the speed of BaseObject.copy() with BaseObject.__copy__().

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        # Calculate the mean time in microseconds for copy method
        copy_time = timeit.timeit(test_object.copy, number=self.timeit_runs)
        mean_copy = copy_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for __copy__ method
        dunder_time = timeit.timeit(test_object.__copy__, number=self.timeit_runs)
        mean_dunder = dunder_time / self.timeit_runs * 1000000
        percent = (mean_copy / mean_dunder) * 100

        # Print the performance comparison
        print(f"\ncopy(): {mean_copy:.3f} μs, __copy__(): {mean_dunder:.3f} μs ({percent:.3f}% ratio)")
        # The wrapper should not add significant overhead
        assert percent < 115  # Allow up to 15% overhead

    def test_deepcopy_vs_dunder_deepcopy(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test the performance difference between deepcopy() and __deepcopy__() methods.

        This test compares the speed of BaseObject.deepcopy() with BaseObject.__deepcopy__().

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        # Calculate the mean time in microseconds for deepcopy method
        deepcopy_time = timeit.timeit(test_object.deepcopy, number=self.timeit_runs)
        mean_deepcopy = deepcopy_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for __deepcopy__ method
        dunder_time = timeit.timeit(lambda: test_object.__deepcopy__({}), number=self.timeit_runs)
        mean_dunder = dunder_time / self.timeit_runs * 1000000
        percent = (mean_deepcopy / mean_dunder) * 100

        # Print the performance comparison
        print(f"\ndeepcopy(): {mean_deepcopy:.3f} μs, __deepcopy__(): {mean_dunder:.3f} μs ({percent:.3f}% ratio)")
        # The wrapper should not add significant overhead
        assert percent < 110  # Allow up to 10% overhead

    def test_attribute_access_speed(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test the performance of attribute access in BaseObject.

        This test compares the speed of attribute access in BaseObject with a normal Python object.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        normal = self.NormalObject()

        def access_base_attr() -> None:
            # Access both immutable and mutable attributes
            _ = test_object.immutable
            _ = test_object.mutable

        def access_normal_attr() -> None:
            # Access both immutable and mutable attributes
            _ = normal.immutable
            _ = normal.mutable

        # Calculate the mean time in microseconds for BaseObject attribute access
        base_time = timeit.timeit(access_base_attr, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object attribute access
        normal_time = timeit.timeit(access_normal_attr, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(f"\nBaseObject attr access: {mean_base:.3f} μs ({percent:.3f}% of normal object time)")
        assert percent < self.speed_tolerance

    def test_attribute_modification_speed(self, test_object: "TestBaseObject.BaseTestObject") -> None:
        """Test the performance of attribute modification in BaseObject.

        This test compares the speed of attribute modification in BaseObject with a normal Python object.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        normal = self.NormalObject()

        def modify_base_attr() -> None:
            # Modify both immutable and mutable attributes
            test_object.immutable = 1
            test_object.mutable = {"key": "value"}

        def modify_normal_attr() -> None:
            # Modify both immutable and mutable attributes
            normal.immutable = 1
            normal.mutable = {"key": "value"}

        # Calculate the mean time in microseconds for BaseObject attribute modification
        base_time = timeit.timeit(modify_base_attr, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object attribute modification
        normal_time = timeit.timeit(modify_normal_attr, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(f"\nBaseObject attr modification: {mean_base:.3f} μs ({percent:.3f}% of normal object time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
