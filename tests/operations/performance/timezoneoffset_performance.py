#!/usr/bin/env python
"""timezoneoffset_performance.py
Performance tests for the timezone_offset function in the baseobjects.operations package.
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
import zoneinfo
from datetime import datetime, timedelta, timezone, tzinfo

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.operations.timezoneoffset import INIT_DATE, timezone_offset
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Functions #
def standard_timezone_offset(tz: tzinfo) -> timedelta:
    """Standard implementation of timezone_offset that directly calls utcoffset.

    Args:
        tz: The timezone to get the offset from.

    Returns:
        The time delta offset of the given timezone.
    """
    return tz.utcoffset(datetime(1970, 1, 1))


# Classes #
class CustomTimezone(tzinfo):
    """A custom timezone class for testing purposes.

    This class returns different offsets based on the date provided.
    """

    def __init__(self, hours: int = 1, complex_calculation: bool = False):
        self.hours = hours
        self.complex_calculation = complex_calculation

    def utcoffset(self, dt):
        if self.complex_calculation and dt:
            # Simulate a more complex calculation
            if dt.year == 1970 and dt.month == 1 and dt.day == 1:
                return timedelta(hours=self.hours + 1)
            elif dt.month in [4, 5, 6, 7, 8, 9]:
                return timedelta(hours=self.hours + 2)
            else:
                return timedelta(hours=self.hours)
        return timedelta(hours=self.hours)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return f"CustomTZ({self.hours})"


class TestTimezoneOffset(BasePerformanceTestSuite):
    """Test the performance of the timezone_offset function.

    This class tests the performance of the timezone_offset function, which gets the offset of a given timezone.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: int = 150

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def utc_timezone(self) -> timezone:
        """Create a UTC timezone for use in tests.

        Returns:
            timezone: The UTC timezone.
        """
        return timezone.utc

    @pytest.fixture
    def positive_timezone(self) -> timezone:
        """Create a positive timezone for use in tests.

        Returns:
            timezone: A timezone with a positive offset.
        """
        return timezone(timedelta(hours=5, minutes=30))

    @pytest.fixture
    def negative_timezone(self) -> timezone:
        """Create a negative timezone for use in tests.

        Returns:
            timezone: A timezone with a negative offset.
        """
        return timezone(timedelta(hours=-3, minutes=-45))

    @pytest.fixture
    def custom_timezone(self) -> CustomTimezone:
        """Create a custom timezone for use in tests.

        Returns:
            CustomTimezone: A custom timezone.
        """
        return CustomTimezone(hours=2)

    @pytest.fixture
    def complex_custom_timezone(self) -> CustomTimezone:
        """Create a complex custom timezone for use in tests.

        Returns:
            CustomTimezone: A custom timezone with complex calculations.
        """
        return CustomTimezone(hours=2, complex_calculation=True)

    @pytest.fixture
    def zoneinfo_timezone(self) -> tzinfo:
        """Create a zoneinfo timezone for use in tests.

        Returns:
            tzinfo: A zoneinfo timezone.
        """
        try:
            return zoneinfo.ZoneInfo("America/New_York")
        except (ImportError, zoneinfo.ZoneInfoNotFoundError):
            pytest.skip("zoneinfo module not available or timezone not found")

    # Tests
    def test_timezone_offset_utc_speed(self, utc_timezone: timezone) -> None:
        """Test the performance of timezone_offset with UTC timezone.

        This test compares the speed of timezone_offset with a standard implementation for UTC timezone.

        Args:
            utc_timezone: A fixture providing the UTC timezone.
        """

        def custom_implementation() -> None:
            timezone_offset(utc_timezone)

        def standard_implementation() -> None:
            standard_timezone_offset(utc_timezone)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (timezone_offset UTC): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_timezone_offset_positive_speed(self, positive_timezone: timezone) -> None:
        """Test the performance of timezone_offset with a positive timezone.

        This test compares the speed of timezone_offset with a standard implementation for a positive timezone.

        Args:
            positive_timezone: A fixture providing a positive timezone.
        """

        def custom_implementation() -> None:
            timezone_offset(positive_timezone)

        def standard_implementation() -> None:
            standard_timezone_offset(positive_timezone)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (timezone_offset positive): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_timezone_offset_negative_speed(self, negative_timezone: timezone) -> None:
        """Test the performance of timezone_offset with a negative timezone.

        This test compares the speed of timezone_offset with a standard implementation for a negative timezone.

        Args:
            negative_timezone: A fixture providing a negative timezone.
        """

        def custom_implementation() -> None:
            timezone_offset(negative_timezone)

        def standard_implementation() -> None:
            standard_timezone_offset(negative_timezone)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (timezone_offset negative): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_timezone_offset_custom_speed(self, custom_timezone: CustomTimezone) -> None:
        """Test the performance of timezone_offset with a custom timezone.

        This test compares the speed of timezone_offset with a standard implementation for a custom timezone.

        Args:
            custom_timezone: A fixture providing a custom timezone.
        """

        def custom_implementation() -> None:
            timezone_offset(custom_timezone)

        def standard_implementation() -> None:
            standard_timezone_offset(custom_timezone)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (timezone_offset custom): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_timezone_offset_complex_custom_speed(self, complex_custom_timezone: CustomTimezone) -> None:
        """Test the performance of timezone_offset with a complex custom timezone.

        This test compares the speed of timezone_offset with a standard implementation for a complex custom timezone.

        Args:
            complex_custom_timezone: A fixture providing a complex custom timezone.
        """

        def custom_implementation() -> None:
            timezone_offset(complex_custom_timezone)

        def standard_implementation() -> None:
            standard_timezone_offset(complex_custom_timezone)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (timezone_offset complex custom): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)"
        )
        assert percent < self.speed_tolerance

    def test_timezone_offset_zoneinfo_speed(self, zoneinfo_timezone: tzinfo) -> None:
        """Test the performance of timezone_offset with a zoneinfo timezone.

        This test compares the speed of timezone_offset with a standard implementation for a zoneinfo timezone.

        Args:
            zoneinfo_timezone: A fixture providing a zoneinfo timezone.
        """

        def custom_implementation() -> None:
            timezone_offset(zoneinfo_timezone)

        def standard_implementation() -> None:
            standard_timezone_offset(zoneinfo_timezone)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (timezone_offset zoneinfo): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
