#!/usr/bin/env python
"""filetimetodatetime_performance.py
Performance tests for the filetime_to_datetime function in the baseobjects.operations package.
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
from typing import Any, Union

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.operations.filetimetodatetime import FILETIME_INIT_DATE, filetime_to_datetime
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Functions #
def standard_filetime_to_datetime_int(timestamp: int, tzinfo=None) -> datetime:
    """Standard implementation of filetime_to_datetime for integer timestamps.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(microseconds=timestamp)
    else:
        return (FILETIME_INIT_DATE + timedelta(microseconds=timestamp)).astimezone(tz=tzinfo)


def standard_filetime_to_datetime_float(timestamp: float, tzinfo=None) -> datetime:
    """Standard implementation of filetime_to_datetime for float timestamps.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(microseconds=int(timestamp) / 10)
    else:
        return (FILETIME_INIT_DATE + timedelta(microseconds=int(timestamp) / 10)).astimezone(tz=tzinfo)


def standard_filetime_to_datetime_str(timestamp: str, tzinfo=None) -> datetime:
    """Standard implementation of filetime_to_datetime for string timestamps.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(microseconds=int(timestamp) / 10)
    else:
        return (FILETIME_INIT_DATE + timedelta(microseconds=int(timestamp) / 10)).astimezone(tz=tzinfo)


def standard_filetime_to_datetime_bytes(timestamp: bytes, tzinfo=None) -> datetime:
    """Standard implementation of filetime_to_datetime for bytes timestamps.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    delta = timedelta(microseconds=int.from_bytes(timestamp, "little") / 10)
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + delta
    else:
        return (FILETIME_INIT_DATE + delta).astimezone(tz=tzinfo)


def standard_filetime_to_datetime_bytearray(timestamp: bytearray, tzinfo=None) -> datetime:
    """Standard implementation of filetime_to_datetime for bytearray timestamps.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    delta = timedelta(microseconds=int.from_bytes(timestamp, "little") / 10)
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + delta
    else:
        return (FILETIME_INIT_DATE + delta).astimezone(tz=tzinfo)


def standard_filetime_to_datetime(timestamp: Union[int, float, str, bytes, bytearray], tzinfo=None) -> datetime:
    """Standard implementation of filetime_to_datetime using type checking.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if isinstance(timestamp, int):
        return standard_filetime_to_datetime_int(timestamp, tzinfo)
    elif isinstance(timestamp, float):
        return standard_filetime_to_datetime_float(timestamp, tzinfo)
    elif isinstance(timestamp, str):
        return standard_filetime_to_datetime_str(timestamp, tzinfo)
    elif isinstance(timestamp, bytes):
        return standard_filetime_to_datetime_bytes(timestamp, tzinfo)
    elif isinstance(timestamp, bytearray):
        return standard_filetime_to_datetime_bytearray(timestamp, tzinfo)
    else:
        raise TypeError(f"{timestamp.__class__} cannot be converted to a datetime")


# Classes #
class TestFiletimeToDatetime(BasePerformanceTestSuite):
    """Test the performance of the filetime_to_datetime function.

    This class tests the performance of the filetime_to_datetime function, which converts a Windows filetime to a datetime.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: int = 150

    # Instance Methods #
    # Tests
    def test_filetime_to_datetime_int_speed(self) -> None:
        """Test the performance of filetime_to_datetime with integer input.

        This test compares the speed of filetime_to_datetime with a standard implementation for integer input.
        """
        timestamp = 10000000000

        def custom_implementation() -> None:
            filetime_to_datetime(timestamp, None)

        def standard_implementation() -> None:
            standard_filetime_to_datetime_int(timestamp, None)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (filetime_to_datetime int): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_filetime_to_datetime_float_speed(self) -> None:
        """Test the performance of filetime_to_datetime with float input.

        This test compares the speed of filetime_to_datetime with a standard implementation for float input.
        """
        timestamp = 10000000.0

        def custom_implementation() -> None:
            filetime_to_datetime(timestamp, None)

        def standard_implementation() -> None:
            standard_filetime_to_datetime_float(timestamp, None)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (filetime_to_datetime float): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_filetime_to_datetime_str_speed(self) -> None:
        """Test the performance of filetime_to_datetime with string input.

        This test compares the speed of filetime_to_datetime with a standard implementation for string input.
        """
        timestamp = "10000000"

        def custom_implementation() -> None:
            filetime_to_datetime(timestamp, None)

        def standard_implementation() -> None:
            standard_filetime_to_datetime_str(timestamp, None)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (filetime_to_datetime str): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_filetime_to_datetime_bytes_speed(self) -> None:
        """Test the performance of filetime_to_datetime with bytes input.

        This test compares the speed of filetime_to_datetime with a standard implementation for bytes input.
        """
        # 10000000 in little-endian bytes
        timestamp = b"\x80\x96\x98\x00\x00\x00\x00\x00"

        def custom_implementation() -> None:
            filetime_to_datetime(timestamp, None)

        def standard_implementation() -> None:
            standard_filetime_to_datetime_bytes(timestamp, None)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (filetime_to_datetime bytes): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_filetime_to_datetime_bytearray_speed(self) -> None:
        """Test the performance of filetime_to_datetime with bytearray input.

        This test compares the speed of filetime_to_datetime with a standard implementation for bytearray input.
        """
        # 10000000 in little-endian bytearray
        timestamp = bytearray(b"\x80\x96\x98\x00\x00\x00\x00\x00")

        def custom_implementation() -> None:
            filetime_to_datetime(timestamp, None)

        def standard_implementation() -> None:
            standard_filetime_to_datetime_bytearray(timestamp, None)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (filetime_to_datetime bytearray): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)"
        )
        assert percent < self.speed_tolerance

    def test_filetime_to_datetime_timezone_speed(self) -> None:
        """Test the performance of filetime_to_datetime with different timezones.

        This test measures the speed of filetime_to_datetime with different timezone specifications.
        """
        timestamp = 10000000000
        utc_tz = timezone.utc
        est_tz = timezone(timedelta(hours=-5))

        def none_timezone() -> None:
            filetime_to_datetime(timestamp, None)

        def utc_timezone() -> None:
            filetime_to_datetime(timestamp, utc_tz)

        def est_timezone() -> None:
            filetime_to_datetime(timestamp, est_tz)

        # Calculate the mean time in microseconds for None timezone
        none_time = timeit.timeit(none_timezone, number=self.timeit_runs)
        mean_none = none_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UTC timezone
        utc_time = timeit.timeit(utc_timezone, number=self.timeit_runs)
        mean_utc = utc_time / self.timeit_runs * 1000000
        utc_percent = (mean_utc / mean_none) * 100

        # Calculate the mean time in microseconds for EST timezone
        est_time = timeit.timeit(est_timezone, number=self.timeit_runs)
        mean_est = est_time / self.timeit_runs * 1000000
        est_percent = (mean_est / mean_none) * 100

        # Print the performance comparison
        print(f"\nNone timezone: {mean_none:.3f} μs (baseline)")
        print(f"UTC timezone: {mean_utc:.3f} μs ({utc_percent:.3f}% of None timezone time)")
        print(f"EST timezone: {mean_est:.3f} μs ({est_percent:.3f}% of None timezone time)")
        # No assertion here, just measuring relative performance

    def test_filetime_to_datetime_dispatch_speed(self) -> None:
        """Test the performance of filetime_to_datetime's dispatch mechanism.

        This test compares the speed of filetime_to_datetime with a standard implementation using type checking.
        """
        # Test with different types of input
        int_timestamp = 10000000000
        float_timestamp = 10000000.0
        str_timestamp = "10000000"
        bytes_timestamp = b"\x80\x96\x98\x00\x00\x00\x00\x00"
        bytearray_timestamp = bytearray(b"\x80\x96\x98\x00\x00\x00\x00\x00")

        def custom_implementation_int() -> None:
            filetime_to_datetime(int_timestamp, None)

        def custom_implementation_float() -> None:
            filetime_to_datetime(float_timestamp, None)

        def custom_implementation_str() -> None:
            filetime_to_datetime(str_timestamp, None)

        def custom_implementation_bytes() -> None:
            filetime_to_datetime(bytes_timestamp, None)

        def custom_implementation_bytearray() -> None:
            filetime_to_datetime(bytearray_timestamp, None)

        def standard_implementation_int() -> None:
            standard_filetime_to_datetime(int_timestamp, None)

        def standard_implementation_float() -> None:
            standard_filetime_to_datetime(float_timestamp, None)

        def standard_implementation_str() -> None:
            standard_filetime_to_datetime(str_timestamp, None)

        def standard_implementation_bytes() -> None:
            standard_filetime_to_datetime(bytes_timestamp, None)

        def standard_implementation_bytearray() -> None:
            standard_filetime_to_datetime(bytearray_timestamp, None)

        # Calculate the mean time for each type with the custom implementation
        int_new_time = timeit.timeit(custom_implementation_int, number=self.timeit_runs)
        float_new_time = timeit.timeit(custom_implementation_float, number=self.timeit_runs)
        str_new_time = timeit.timeit(custom_implementation_str, number=self.timeit_runs)
        bytes_new_time = timeit.timeit(custom_implementation_bytes, number=self.timeit_runs)
        bytearray_new_time = timeit.timeit(custom_implementation_bytearray, number=self.timeit_runs)

        # Calculate the mean time for each type with the standard implementation
        int_old_time = timeit.timeit(standard_implementation_int, number=self.timeit_runs)
        float_old_time = timeit.timeit(standard_implementation_float, number=self.timeit_runs)
        str_old_time = timeit.timeit(standard_implementation_str, number=self.timeit_runs)
        bytes_old_time = timeit.timeit(standard_implementation_bytes, number=self.timeit_runs)
        bytearray_old_time = timeit.timeit(standard_implementation_bytearray, number=self.timeit_runs)

        # Calculate the average time for all types
        new_avg_time = (int_new_time + float_new_time + str_new_time + bytes_new_time + bytearray_new_time) / 5
        old_avg_time = (int_old_time + float_old_time + str_old_time + bytes_old_time + bytearray_old_time) / 5

        # Convert to microseconds
        mean_new = new_avg_time / self.timeit_runs * 1000000
        mean_old = old_avg_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (filetime_to_datetime dispatch): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)"
        )
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
