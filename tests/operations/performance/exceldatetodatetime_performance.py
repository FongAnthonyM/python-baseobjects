#!/usr/bin/env python
"""exceldatetodatetime_performance.py
Performance tests for the excel_date_to_datetime function in the baseobjects.operations package.
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
from datetime import datetime, timedelta, timezone
from typing import Union

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.operations.exceldatetodatetime import EXCEL_INIT_DATE, excel_date_to_datetime
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Functions #
def standard_excel_date_to_datetime_int(timestamp: int, tzinfo=timezone.utc) -> datetime:
    """Standard implementation of excel_date_to_datetime for integer timestamps.

    Args:
        timestamp: The Excel date to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the Excel date.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=timestamp)


def standard_excel_date_to_datetime_float(timestamp: float, tzinfo=timezone.utc) -> datetime:
    """Standard implementation of excel_date_to_datetime for float timestamps.

    Args:
        timestamp: The Excel date to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the Excel date.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=timestamp)


def standard_excel_date_to_datetime_str(timestamp: str, tzinfo=timezone.utc) -> datetime:
    """Standard implementation of excel_date_to_datetime for string timestamps.

    Args:
        timestamp: The Excel date to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the Excel date.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=float(timestamp))


def standard_excel_date_to_datetime_bytes(timestamp: bytes, tzinfo=timezone.utc) -> datetime:
    """Standard implementation of excel_date_to_datetime for bytes timestamps.

    Args:
        timestamp: The Excel date to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the Excel date.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=float(timestamp))


def standard_excel_date_to_datetime(timestamp: Union[int, float, str, bytes], tzinfo=timezone.utc) -> datetime:
    """Standard implementation of excel_date_to_datetime using type checking.

    Args:
        timestamp: The Excel date to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the Excel date.
    """
    if isinstance(timestamp, int):
        return standard_excel_date_to_datetime_int(timestamp, tzinfo)
    elif isinstance(timestamp, float):
        return standard_excel_date_to_datetime_float(timestamp, tzinfo)
    elif isinstance(timestamp, str):
        return standard_excel_date_to_datetime_str(timestamp, tzinfo)
    elif isinstance(timestamp, bytes):
        return standard_excel_date_to_datetime_bytes(timestamp, tzinfo)
    else:
        raise TypeError(f"{timestamp.__class__} cannot be converted to a datetime")


# Classes #
class TestExcelDateToDatetime(BasePerformanceTestSuite):
    """Test the performance of the excel_date_to_datetime function.

    This class tests the performance of the excel_date_to_datetime function, which converts an Excel date to a datetime.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: int = 150

    # Instance Methods #
    # Tests
    def test_excel_date_to_datetime_int_speed(self) -> None:
        """Test the performance of excel_date_to_datetime with integer input.

        This test compares the speed of excel_date_to_datetime with a standard implementation for integer input.
        """
        timestamp = 10000

        def custom_implementation() -> None:
            excel_date_to_datetime(timestamp, timezone.utc)

        def standard_implementation() -> None:
            standard_excel_date_to_datetime_int(timestamp, timezone.utc)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (excel_date_to_datetime int): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_excel_date_to_datetime_float_speed(self) -> None:
        """Test the performance of excel_date_to_datetime with float input.

        This test compares the speed of excel_date_to_datetime with a standard implementation for float input.
        """
        timestamp = 10000.5

        def custom_implementation() -> None:
            excel_date_to_datetime(timestamp, timezone.utc)

        def standard_implementation() -> None:
            standard_excel_date_to_datetime_float(timestamp, timezone.utc)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (excel_date_to_datetime float): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)"
        )
        assert percent < self.speed_tolerance

    def test_excel_date_to_datetime_str_speed(self) -> None:
        """Test the performance of excel_date_to_datetime with string input.

        This test compares the speed of excel_date_to_datetime with a standard implementation for string input.
        """
        timestamp = "10000.5"

        def custom_implementation() -> None:
            excel_date_to_datetime(timestamp, timezone.utc)

        def standard_implementation() -> None:
            standard_excel_date_to_datetime_str(timestamp, timezone.utc)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (excel_date_to_datetime str): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_excel_date_to_datetime_bytes_speed(self) -> None:
        """Test the performance of excel_date_to_datetime with bytes input.

        This test compares the speed of excel_date_to_datetime with a standard implementation for bytes input.
        """
        timestamp = b"10000.5"

        def custom_implementation() -> None:
            excel_date_to_datetime(timestamp, timezone.utc)

        def standard_implementation() -> None:
            standard_excel_date_to_datetime_bytes(timestamp, timezone.utc)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (excel_date_to_datetime bytes): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)"
        )
        assert percent < self.speed_tolerance

    def test_excel_date_to_datetime_dispatch_speed(self) -> None:
        """Test the performance of excel_date_to_datetime's dispatch mechanism.

        This test compares the speed of excel_date_to_datetime with a standard implementation using type checking.
        """
        # Test with different types of input
        int_timestamp = 10000
        float_timestamp = 10000.5
        str_timestamp = "10000.5"
        bytes_timestamp = b"10000.5"

        def custom_implementation_int() -> None:
            excel_date_to_datetime(int_timestamp, timezone.utc)

        def custom_implementation_float() -> None:
            excel_date_to_datetime(float_timestamp, timezone.utc)

        def custom_implementation_str() -> None:
            excel_date_to_datetime(str_timestamp, timezone.utc)

        def custom_implementation_bytes() -> None:
            excel_date_to_datetime(bytes_timestamp, timezone.utc)

        def standard_implementation_int() -> None:
            standard_excel_date_to_datetime(int_timestamp, timezone.utc)

        def standard_implementation_float() -> None:
            standard_excel_date_to_datetime(float_timestamp, timezone.utc)

        def standard_implementation_str() -> None:
            standard_excel_date_to_datetime(str_timestamp, timezone.utc)

        def standard_implementation_bytes() -> None:
            standard_excel_date_to_datetime(bytes_timestamp, timezone.utc)

        # Calculate the mean time for each type with the custom implementation
        int_new_time = timeit.timeit(custom_implementation_int, number=self.timeit_runs)
        float_new_time = timeit.timeit(custom_implementation_float, number=self.timeit_runs)
        str_new_time = timeit.timeit(custom_implementation_str, number=self.timeit_runs)
        bytes_new_time = timeit.timeit(custom_implementation_bytes, number=self.timeit_runs)

        # Calculate the mean time for each type with the standard implementation
        int_old_time = timeit.timeit(standard_implementation_int, number=self.timeit_runs)
        float_old_time = timeit.timeit(standard_implementation_float, number=self.timeit_runs)
        str_old_time = timeit.timeit(standard_implementation_str, number=self.timeit_runs)
        bytes_old_time = timeit.timeit(standard_implementation_bytes, number=self.timeit_runs)

        # Calculate the average time for all types
        new_avg_time = (int_new_time + float_new_time + str_new_time + bytes_new_time) / 4
        old_avg_time = (int_old_time + float_old_time + str_old_time + bytes_old_time) / 4

        # Convert to microseconds
        mean_new = new_avg_time / self.timeit_runs * 1000000
        mean_old = old_avg_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (excel_date_to_datetime dispatch): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)"
        )
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
