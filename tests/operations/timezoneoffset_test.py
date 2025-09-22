#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""timezoneoffset_test.py
Tests for the timezone_offset function in the baseobjects package.
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
from datetime import timedelta, timezone, tzinfo
import zoneinfo

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.operations.timezoneoffset import timezone_offset, INIT_DATE


# Definitions #
# Classes #
class TestTimezoneOffset:
    """Test the timezone_offset function.

    This class tests_old_ the functionality of the timezone_offset function, which gets the offset of a given timezone.
    """

    # Instance Methods #
    # Tests
    def test_timezone_offset_utc(self) -> None:
        """Test getting the offset of UTC timezone.

        This test verifies that the timezone_offset function correctly returns a zero timedelta for the UTC timezone.
        """
        # Test with UTC timezone
        result = timezone_offset(timezone.utc)
        expected = timedelta(0)
        assert result == expected

    def test_timezone_offset_positive(self) -> None:
        """Test getting the offset of a positive timezone.

        This test verifies that the timezone_offset function correctly returns a positive timedelta for a timezone east
        of UTC.
        """
        # Test with a positive timezone offset (UTC+5)
        tz = timezone(timedelta(hours=5))
        result = timezone_offset(tz)
        expected = timedelta(hours=5)
        assert result == expected

        # Test with another positive timezone offset (UTC+9:30)
        tz = timezone(timedelta(hours=9, minutes=30))
        result = timezone_offset(tz)
        expected = timedelta(hours=9, minutes=30)
        assert result == expected

    def test_timezone_offset_negative(self) -> None:
        """Test getting the offset of a negative timezone.

        This test verifies that the timezone_offset function correctly returns a negative timedelta for a timezone west
        of UTC.
        """
        # Test with a negative timezone offset (UTC-5)
        tz = timezone(timedelta(hours=-5))
        result = timezone_offset(tz)
        expected = timedelta(hours=-5)
        assert result == expected

        # Test with another negative timezone offset (UTC-3:30)
        tz = timezone(timedelta(hours=-3, minutes=-30))
        result = timezone_offset(tz)
        expected = timedelta(hours=-3, minutes=-30)
        assert result == expected

    def test_timezone_offset_zoneinfo(self) -> None:
        """Test getting the offset of zoneinfo timezones.

        This test verifies that the timezone_offset function correctly returns the expected timedelta for zoneinfo
        timezones.
        """
        try:
            # Test with America/New_York timezone
            tz = zoneinfo.ZoneInfo("America/New_York")
            result = timezone_offset(tz)
            # The offset depends on whether DST is in effect at INIT_DATE
            # January 1, 1970 is not in DST, so it should be UTC-5
            expected = timedelta(hours=-5)
            assert result == expected

            # Test with Asia/Tokyo timezone
            tz = zoneinfo.ZoneInfo("Asia/Tokyo")
            result = timezone_offset(tz)
            expected = timedelta(hours=9)
            assert result == expected
        except ImportError:
            # Skip if zoneinfo is not available
            pytest.skip("zoneinfo module not available")

    def test_timezone_offset_init_date(self) -> None:
        """Test that the timezone_offset function uses the correct reference date.

        This test verifies that the timezone_offset function uses the INIT_DATE constant as the reference date for
        calculating the offset.
        """

        # Create a custom timezone class that returns different offsets for different dates
        class CustomTimezone(tzinfo):
            def utcoffset(self, dt):
                if dt and dt.year == 1970 and dt.month == 1 and dt.day == 1:
                    return timedelta(hours=2)
                return timedelta(hours=1)

            def dst(self, dt):
                return timedelta(0)

            def tzname(self, dt):
                return "CustomTZ"

        # Test with the custom timezone
        tz = CustomTimezone()
        result = timezone_offset(tz)
        # Should use the offset for INIT_DATE (1970-01-01)
        expected = timedelta(hours=2)
        assert result == expected

    def test_timezone_offset_none(self) -> None:
        """Test getting the offset of None timezone.

        This test verifies that the timezone_offset function raises an AttributeError when None is provided as the
        timezone.
        """
        # Test with None timezone
        with pytest.raises(AttributeError):
            timezone_offset(None)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
