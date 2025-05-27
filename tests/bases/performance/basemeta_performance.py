#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basemeta_performance.py
Performance tests for the BaseMeta metaclass in the baseobjects package.
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
from src.baseobjects.bases import BaseMeta
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base Meta
class TestBaseMeta(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseMeta metaclass.

    This class tests the performance of the BaseMeta metaclass, which is the base metaclass for all metaclasses in the
    baseobjects package. It creates test classes with this metaclass to test with.
    """
    # Class Definitions #
    class BaseTestMeta(metaclass=BaseMeta):
        """A class using BaseMeta as its metaclass for testing purposes."""
        # Class Attributes #
        class_attr = "test"
        
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple attribute."""
            self.instance_attr = "test"

    class NormalMeta(type):
        """A normal Python metaclass for comparison with BaseMeta."""
        # Magic Methods #
        def __copy__(cls):
            """Create a shallow copy of the class."""
            return type(cls.__name__, cls.__bases__, dict(cls.__dict__))
            
        def __deepcopy__(cls, memo=None):
            """Create a deep copy of the class."""
            if memo is None:
                memo = {}
            result = type(cls.__name__, cls.__bases__, {})
            memo[id(cls)] = result
            for key, value in cls.__dict__.items():
                if key != "__dict__":
                    setattr(result, key, copy.deepcopy(value, memo))
            return result

    class NormalTestClass(metaclass=NormalMeta):
        """A class using NormalMeta as its metaclass for comparison."""
        # Class Attributes #
        class_attr = "test"
        
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple attribute."""
            self.instance_attr = "test"

    # Attributes #
    class_: Type = BaseTestMeta

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class(self) -> Type:
        """Create a test class for use in tests.

        Returns:
            Type: A class using BaseMeta as its metaclass.
        """
        return self.class_

    @pytest.fixture
    def normal_class(self) -> Type:
        """Create a normal test class for comparison.

        Returns:
            Type: A class using NormalMeta as its metaclass.
        """
        return self.NormalTestClass

    # Tests
    def test_instance_creation(self, test_class: Type) -> None:
        """Test that instances of classes with BaseMeta can be created efficiently.

        Args:
            test_class: A fixture providing a class with BaseMeta.
        """
        instance = test_class()
        assert instance is not None

    def test_copy_speed(self, test_class: Type, normal_class: Type) -> None:
        """Test the performance of the __copy__ method of BaseMeta.

        This test compares the speed of copying a class with BaseMeta with a normal metaclass.

        Args:
            test_class: A fixture providing a class with BaseMeta.
            normal_class: A fixture providing a class with a normal metaclass.
        """
        def copy_base() -> None:
            copy.copy(test_class)

        def copy_normal() -> None:
            copy.copy(normal_class)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(copy_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(copy_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_deepcopy_speed(self, test_class: Type, normal_class: Type) -> None:
        """Test the performance of the __deepcopy__ method of BaseMeta.

        This test compares the speed of deep copying a class with BaseMeta with a normal metaclass.

        Args:
            test_class: A fixture providing a class with BaseMeta.
            normal_class: A fixture providing a class with a normal metaclass.
        """
        def deepcopy_base() -> None:
            copy.deepcopy(test_class)

        def deepcopy_normal() -> None:
            copy.deepcopy(normal_class)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(deepcopy_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(deepcopy_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_class_creation_speed(self) -> None:
        """Test the performance of creating a class with BaseMeta.

        This test compares the speed of creating a class with BaseMeta with a normal metaclass.
        """
        def create_base_class() -> None:
            class TestClass(metaclass=BaseMeta):
                class_attr = "test"
                
                def __init__(self) -> None:
                    self.instance_attr = "test"

        def create_normal_class() -> None:
            class TestClass(metaclass=self.NormalMeta):
                class_attr = "test"
                
                def __init__(self) -> None:
                    self.instance_attr = "test"

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_base_class, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal_class, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])