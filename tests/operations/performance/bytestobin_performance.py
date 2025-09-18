#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" bytestobin_performance.py
Performance tests_old_ for the bytes_to_bin function in the baseobjects.operations package.
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
from typing import Any, Callable, Tuple

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.operations import bytes_to_bin
from tests.bases.performance.base_performance import ClassPerformanceTest


# Definitions #
# Functions #
def standard_bytes_to_bin_big(bytes_: bytes, out_type: type = int) -> tuple[Any]:
    """Standard implementation of bytes_to_bin for big endian using list comprehension.

    Args:
        bytes_: The bytes to convert to binary.
        out_type: The type to represent the binary values as.

    Returns:
        The tuple of binary values from the bytes.
    """
    result = []
    for byte in bytes_:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            result.append(out_type(bool(bit)))
    return tuple(result)


def standard_bytes_to_bin_little(bytes_: bytes, out_type: type = int) -> tuple[Any]:
    """Standard implementation of bytes_to_bin for little endian using list comprehension.

    Args:
        bytes_: The bytes to convert to binary.
        out_type: The type to represent the binary values as.

    Returns:
        The tuple of binary values from the bytes.
    """
    result = []
    for byte in bytes_:
        for i in range(4):
            bit = (byte >> i) & 1
            result.append(out_type(bool(bit)))
        for i in range(4):
            bit = (byte >> (i + 4)) & 1
            result.append(out_type(bool(bit)))
    return tuple(result)


# Classes #
class TestBytesToBin(ClassPerformanceTest):
    """Test the performance of the bytes_to_bin function.

    This class tests_old_ the performance of the bytes_to_bin function, which converts bytes to a tuple of binary values.
    """
    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: int = 150

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_bytes(self) -> bytes:
        """Create test bytes for use in tests_old_.

        Returns:
            bytes: Test bytes.
        """
        return b'\x01\x02\x03\x04\x05'

    # Tests
    def test_bytes_to_bin_big_endian_speed(self, test_bytes: bytes) -> None:
        """Test the performance of bytes_to_bin with big endian byte order.

        This test compares the speed of bytes_to_bin with a standard implementation for big endian byte order.

        Args:
            test_bytes: A fixture providing test bytes.
        """
        def custom_implementation() -> None:
            bytes_to_bin(test_bytes, byteorder="big")

        def standard_implementation() -> None:
            standard_bytes_to_bin_big(test_bytes)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (bytes_to_bin big endian): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_bytes_to_bin_little_endian_speed(self, test_bytes: bytes) -> None:
        """Test the performance of bytes_to_bin with little endian byte order.

        This test compares the speed of bytes_to_bin with a standard implementation for little endian byte order.

        Args:
            test_bytes: A fixture providing test bytes.
        """
        def custom_implementation() -> None:
            bytes_to_bin(test_bytes, byteorder="little")

        def standard_implementation() -> None:
            standard_bytes_to_bin_little(test_bytes)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (bytes_to_bin little endian): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_bytes_to_bin_different_output_types_speed(self, test_bytes: bytes) -> None:
        """Test the performance of bytes_to_bin with different output types.

        This test measures the speed of bytes_to_bin with different output types.

        Args:
            test_bytes: A fixture providing test bytes.
        """
        def int_output_type() -> None:
            bytes_to_bin(test_bytes, out_type=int)

        def bool_output_type() -> None:
            bytes_to_bin(test_bytes, out_type=bool)

        def str_output_type() -> None:
            bytes_to_bin(test_bytes, out_type=str)

        # Calculate the mean time in microseconds for int output type
        int_time = timeit.timeit(int_output_type, number=self.timeit_runs)
        mean_int = int_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for bool output type
        bool_time = timeit.timeit(bool_output_type, number=self.timeit_runs)
        mean_bool = bool_time / self.timeit_runs * 1000000
        bool_percent = (mean_bool / mean_int) * 100

        # Calculate the mean time in microseconds for str output type
        str_time = timeit.timeit(str_output_type, number=self.timeit_runs)
        mean_str = str_time / self.timeit_runs * 1000000
        str_percent = (mean_str / mean_int) * 100

        # Print the performance comparison
        print(f"\nInt output type: {mean_int:.3f} μs (baseline)")
        print(f"Bool output type: {mean_bool:.3f} μs ({bool_percent:.3f}% of int output type time)")
        print(f"Str output type: {mean_str:.3f} μs ({str_percent:.3f}% of int output type time)")
        # No assertion here, just measuring relative performance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])