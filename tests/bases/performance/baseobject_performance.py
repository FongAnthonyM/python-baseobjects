#!/usr/bin/env python
"""baseobject_performance.py
Performance tests for the BaseObject class in the baseobjects.bases package.
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
from typing import Any, Dict, List

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases import BaseObject
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class NormalObject:
    """A normal Python object for comparison with BaseObject."""

    def __init__(self, value: Any = None, mutable: list[int] | None = None, mapping: dict[str, int] | None = None) -> None:
        """Initialize with some attributes."""
        self.value = value
        self.mutable = mutable or [1, 2, 3]
        self.mapping = mapping or {"a": 1, "b": 2, "c": 3}


class TestBaseObjectPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseObject class.

    This test suite measures the performance of various operations on BaseObject objects
    and compares them with standard Python implementations.
    """

    # Class Definitions #
    class TestObject(BaseObject):
        """A concrete subclass of BaseObject for testing purposes."""

        def __init__(self, value: Any = None, mutable: list[int] | None = None, mapping: dict[str, int] | None = None) -> None:
            """Initialize with some attributes."""
            super().__init__()
            self.value = value
            self.mutable = mutable or [1, 2, 3]
            self.mapping = mapping or {"a": 1, "b": 2, "c": 3}

    # Attributes #
    timeit_runs: int = 100000

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestBaseObjectPerformance.TestObject":
        """Create a test object instance for use in tests.

        Returns:
            TestObject: An instance of the test class.
        """
        return self.TestObject("test")

    @pytest.fixture
    def test_normal_object(self) -> NormalObject:
        """Create a normal object instance for comparison.

        Returns:
            NormalObject: A standard Python object.
        """
        return NormalObject("test")

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating instances of the BaseObject subclass.

        This test compares the speed of creating BaseObject subclass instances with creating
        standard Python objects.
        """

        def create_base_object() -> None:
            self.TestObject("test")

        def create_normal_object() -> None:
            NormalObject("test")

        # Calculate the mean time in microseconds for BaseObject
        base_time = timeit.timeit(create_base_object, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object
        normal_time = timeit.timeit(create_normal_object, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object creation: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseObject subclass creation: {mean_base:.3f} μs ({percent:.3f}% of normal object creation time)")
        assert percent < self.speed_tolerance * 1.5  # Allow some overhead for BaseObject initialization

    def test_copy_performance(
        self, test_object: "TestBaseObjectPerformance.TestObject", test_normal_object: NormalObject,
    ) -> None:
        """Test the performance of the __copy__ method of BaseObject.

        This test compares the speed of BaseObject.__copy__() with copy.copy() on a normal object.

        Args:
            test_object: A fixture providing a TestObject instance.
            test_normal_object: A fixture providing a NormalObject instance.
        """

        def copy_base_object() -> None:
            test_object.copy()

        def copy_normal_object() -> None:
            copy.copy(test_normal_object)

        # Calculate the mean time in microseconds for BaseObject.copy
        base_time = timeit.timeit(copy_base_object, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for copy.copy on normal object
        normal_time = timeit.timeit(copy_normal_object, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object copy: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseObject.copy: {mean_base:.3f} μs ({percent:.3f}% of normal object copy time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for copy operations

    def test_deepcopy_performance(
        self, test_object: "TestBaseObjectPerformance.TestObject", test_normal_object: NormalObject,
    ) -> None:
        """Test the performance of the __deepcopy__ method of BaseObject.

        This test compares the speed of BaseObject.__deepcopy__() with copy.deepcopy() on a normal object.

        Args:
            test_object: A fixture providing a TestObject instance.
            test_normal_object: A fixture providing a NormalObject instance.
        """

        def deepcopy_base_object() -> None:
            test_object.deepcopy()

        def deepcopy_normal_object() -> None:
            copy.deepcopy(test_normal_object)

        # Calculate the mean time in microseconds for BaseObject.deepcopy
        base_time = timeit.timeit(deepcopy_base_object, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for copy.deepcopy on normal object
        normal_time = timeit.timeit(deepcopy_normal_object, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object deepcopy: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseObject.deepcopy: {mean_base:.3f} μs ({percent:.3f}% of normal object deepcopy time)")
        assert percent < self.speed_tolerance * 3  # Allow more overhead for deepcopy operations

    def test_attribute_access_performance(
        self, test_object: "TestBaseObjectPerformance.TestObject", test_normal_object: NormalObject,
    ) -> None:
        """Test the performance of accessing attributes of BaseObject vs normal object.

        This test compares the speed of accessing attributes of a BaseObject subclass vs a normal object.

        Args:
            test_object: A fixture providing a TestObject instance.
            test_normal_object: A fixture providing a NormalObject instance.
        """

        def access_base_object_attr() -> None:
            _ = test_object.value
            _ = test_object.mutable
            _ = test_object.mapping

        def access_normal_object_attr() -> None:
            _ = test_normal_object.value
            _ = test_normal_object.mutable
            _ = test_normal_object.mapping

        # Calculate the mean time in microseconds for BaseObject attribute access
        base_time = timeit.timeit(access_base_object_attr, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object attribute access
        normal_time = timeit.timeit(access_normal_object_attr, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object attribute access: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"BaseObject attribute access: {mean_base:.3f} μs ({percent:.3f}% of normal object attribute access time)",
        )
        assert percent < self.speed_tolerance  # Should be very similar to normal attribute access

    def test_attribute_modification_performance(
        self, test_object: "TestBaseObjectPerformance.TestObject", test_normal_object: NormalObject,
    ) -> None:
        """Test the performance of modifying attributes of BaseObject vs normal object.

        This test compares the speed of modifying attributes of a BaseObject subclass vs a normal object.

        Args:
            test_object: A fixture providing a TestObject instance.
            test_normal_object: A fixture providing a NormalObject instance.
        """

        def modify_base_object_attr() -> None:
            test_object.value = "modified"
            test_object.mutable.append(4)
            test_object.mapping["d"] = 4

        def modify_normal_object_attr() -> None:
            test_normal_object.value = "modified"
            test_normal_object.mutable.append(4)
            test_normal_object.mapping["d"] = 4

        # Calculate the mean time in microseconds for BaseObject attribute modification
        base_time = timeit.timeit(modify_base_object_attr, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal object attribute modification
        normal_time = timeit.timeit(modify_normal_object_attr, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal object attribute modification: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"BaseObject attribute modification: {mean_base:.3f} μs ({percent:.3f}% of normal object attribute modification time)",
        )
        assert percent < self.speed_tolerance  # Should be very similar to normal attribute modification

    def test_construct_performance(self) -> None:
        """Test the performance of the construct method of BaseObject.

        This test measures the time it takes to call the construct method on a BaseObject subclass.
        """

        class ConstructTestObject(BaseObject):
            """A subclass of BaseObject that implements the construct method."""

            def __init__(self) -> None:
                """Initialize without setting attributes."""
                super().__init__()
                self.value = None
                self.mutable = None
                self.mapping = None

            def construct(self, value: Any = None, mutable: list[int] | None = None, mapping: dict[str, int] | None = None) -> None:
                """Construct the object with the given attributes."""
                super().construct()
                self.value = value
                self.mutable = mutable or [1, 2, 3]
                self.mapping = mapping or {"a": 1, "b": 2, "c": 3}

        test_object = ConstructTestObject()

        def call_construct() -> None:
            test_object.construct("test")

        # Calculate the mean time in microseconds for BaseObject.construct
        construct_time = timeit.timeit(call_construct, number=self.timeit_runs)
        mean_construct = construct_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nBaseObject.construct: {mean_construct:.3f} μs or {mean_construct / self.call_speed:.3f} cu")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_construct < 200  # 200 microseconds is a reasonable threshold

    def test_complex_object_copy_performance(self) -> None:
        """Test the performance of copying complex objects with nested structures.

        This test compares the speed of copying complex objects with BaseObject vs normal objects.
        """
        TestObject = self.TestObject

        # Create complex objects with nested structures
        class ComplexBaseObject(BaseObject):
            """A complex BaseObject subclass with nested structures."""

            def __init__(self) -> None:
                """Initialize with nested structures."""
                super().__init__()
                self.nested = TestObject("nested")
                self.nested_list = [TestObject(f"list_{i}") for i in range(5)]
                self.nested_dict = {f"key_{i}": TestObject(f"dict_{i}") for i in range(5)}

        class ComplexNormalObject:
            """A complex normal object with nested structures."""

            def __init__(self) -> None:
                """Initialize with nested structures."""
                self.nested = NormalObject("nested")
                self.nested_list = [NormalObject(f"list_{i}") for i in range(5)]
                self.nested_dict = {f"key_{i}": NormalObject(f"dict_{i}") for i in range(5)}

        complex_base = ComplexBaseObject()
        complex_normal = ComplexNormalObject()

        def copy_complex_base() -> None:
            complex_base.copy()

        def copy_complex_normal() -> None:
            copy.copy(complex_normal)

        # Calculate the mean time in microseconds for complex BaseObject copy
        base_time = timeit.timeit(copy_complex_base, number=self.timeit_runs // 10)  # Reduce runs for complex objects
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for complex normal object copy
        normal_time = timeit.timeit(
            copy_complex_normal, number=self.timeit_runs // 10,
        )  # Reduce runs for complex objects
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nComplex normal object copy: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Complex BaseObject copy: {mean_base:.3f} μs ({percent:.3f}% of complex normal object copy time)")
        assert percent < self.speed_tolerance * 3  # Allow more overhead for complex object copying


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
