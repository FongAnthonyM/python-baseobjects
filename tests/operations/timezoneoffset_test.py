#!/usr/bin/env python
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
import zoneinfo
from datetime import datetime, timedelta, timezone, tzinfo

# Third-Party Packages #
import pytest

try:
    # Third-Party Packages #
    from typeguard import TypeCheckError
except ImportError:
    TypeCheckError = TypeError  # type: ignore

# Source Packages #
from baseobjects.operations.timezoneoffset import timezone_offset


# Definitions #
# Classes #
class TestTimezoneOffset:
    """Tests the timezone_offset function.

    This class tests the functionality of the timezone_offset function, which gets the offset of a given timezone.
    """

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("offset", "expected"),
        [
            (timedelta(0), timedelta(0)),
            (timedelta(hours=5), timedelta(hours=5)),
            (timedelta(hours=9, minutes=30), timedelta(hours=9, minutes=30)),
            (timedelta(hours=-5), timedelta(hours=-5)),
            (timedelta(hours=-3, minutes=-30), timedelta(hours=-3, minutes=-30)),
        ],
    )
    def test_timezone_offset_fixed(self, offset: timedelta, expected: timedelta) -> None:
        """Tests getting the offset of fixed timezones.

        This test verifies that the timezone_offset function correctly returns the expected timedelta for fixed
        timezones.
        """
        tz = timezone(offset)
        result = timezone_offset(tz)
        assert result == expected

    @pytest.mark.parametrize(
        ("zone_name", "expected_hours"),
        [
            ("America/New_York", -5),
            ("Asia/Tokyo", 9),
        ],
    )
    def test_timezone_offset_zoneinfo(self, zone_name: str, expected_hours: int) -> None:
        """Tests getting the offset of zoneinfo timezones.

        This test verifies that the timezone_offset function correctly returns the expected timedelta for zoneinfo
        timezones.
        """
        # Test with timezone
        try:
            tz = zoneinfo.ZoneInfo(zone_name)
        except zoneinfo.ZoneInfoNotFoundError:
            # Skip if zoneinfo is not available
            pytest.skip("Time Zone Info not available [Windows must have 'tzdata' installed for zoneinfo]")
        else:
            result = timezone_offset(tz)
            expected = timedelta(hours=expected_hours)
            assert result == expected

    def test_timezone_offset_init_date(self) -> None:
        """Tests that the timezone_offset function uses the correct reference date.

        This test verifies that the timezone_offset function uses the INIT_DATE constant as the reference date for
        calculating the offset.
        """

        # Create a custom timezone class that returns different offsets for different dates
        class CustomTimezone(tzinfo):
            def utcoffset(self, dt: datetime | None) -> timedelta | None:
                if dt and dt.year == 1970 and dt.month == 1 and dt.day == 1:
                    return timedelta(hours=2)
                return timedelta(hours=1)

            def dst(self, dt: datetime | None) -> timedelta | None:
                return timedelta(0)

            def tzname(self, dt: datetime | None) -> str:
                return "CustomTZ"

        # Test with the custom timezone
        tz = CustomTimezone()
        result = timezone_offset(tz)
        # Should use the offset for INIT_DATE (1970-01-01)
        expected = timedelta(hours=2)
        assert result == expected

    def test_timezone_offset_none(self) -> None:
        """Tests getting the offset of None timezone.

        This test verifies that the timezone_offset function raises an AttributeError when None is provided as the
        timezone.
        """
        # Test with None timezone
        with pytest.raises((AttributeError, TypeCheckError)):
            timezone_offset(None)  # type: ignore[arg-type]


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
