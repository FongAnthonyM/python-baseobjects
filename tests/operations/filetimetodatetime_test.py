#!/usr/bin/env python
"""filetimetodatetime_test.py
Tests for the filetime_to_datetime function in the baseobjects package.

This module contains tests for the filetime_to_datetime function, which converts Windows FILETIME values to Python
datetime objects. It tests various input types (int, float, str, bytes, bytearray) and timezone handling, as well as
error cases for invalid inputs.
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
from datetime import timedelta, timezone
from typing import Any

# Third-Party Packages #
import pytest

try:
    # Third-Party Packages #
    from typeguard import TypeCheckError
except ImportError:
    TypeCheckError = TypeError  # type: ignore

# Source Packages #
from baseobjects.operations.filetimetodatetime import FILETIME_INIT_DATE, filetime_to_datetime


# Definitions #
# Classes #
class TestFiletimeToDatetime:
    """Tests the filetime_to_datetime function.

    This class tests the functionality of the filetime_to_datetime function, which converts a Windows filetime to a
    datetime object.
    """

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("filetime_input", "microseconds_offset", "byte_order"),
        [
            (1000000, 100000.0, None),
            (0, 0.0, None),
            (10000000000, 1000000000.0, None),
            (10000.0, 1000.0, None),
            (100000000.0, 10000000.0, None),
            ("10000", 1000.0, None),
            ("100000000", 10000000.0, None),
            (b"\x10\x27\x00\x00\x00\x00\x00\x00", 1000.0, "little"),
            (b"\x40\x42\x0f\x00\x00\x00\x00\x00", 100000.0, "little"),
            (bytearray(b"\x10\x27\x00\x00\x00\x00\x00\x00"), 1000.0, "little"),
            (bytearray(b"\x40\x42\x0f\x00\x00\x00\x00\x00"), 100000.0, "little"),
            (b"\x00\x00\x00\x00\x00\x0f\x42\x40", 100000.0, "big"),
        ],
    )
    def test_filetime_to_datetime_types(
        self,
        filetime_input: Any,
        microseconds_offset: float,
        byte_order: str | None,
    ) -> None:
        """Tests converting various types of filetime to datetime.

        This test verifies that the filetime_to_datetime function correctly converts integer, float, string, bytes, and
        bytearray representations of filetime to datetime objects.
        """
        kwargs = {}
        if byte_order:
            kwargs["byteorder"] = byte_order

        result = filetime_to_datetime(filetime_input, None, **kwargs)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=microseconds_offset)
        assert result == expected
        assert result.tzinfo is None

    @pytest.mark.parametrize(
        ("input_val", "tz", "expected_tz"),
        [
            (1000000, None, None),
            (1000000, timezone.utc, timezone.utc),
            (1000000, timezone(timedelta(hours=-5)), timezone(timedelta(hours=-5))),
            (1000000.0, timezone(timedelta(hours=-5)), timezone(timedelta(hours=-5))),
            ("1000000", timezone(timedelta(hours=-5)), timezone(timedelta(hours=-5))),
            (b"\x40\x42\x0f\x00\x00\x00\x00\x00", timezone(timedelta(hours=-5)), timezone(timedelta(hours=-5))),
        ],
    )
    def test_filetime_to_datetime_timezone(self, input_val: Any, tz: Any, expected_tz: Any) -> None:
        """Tests converting a filetime with different timezones.

        This test verifies that the filetime_to_datetime function correctly handles different timezone specifications
        and various input types.
        """
        result = filetime_to_datetime(input_val, tz)
        assert result.tzinfo == expected_tz
        base_expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=100000.0)

        if expected_tz is None:
            assert result == base_expected
        else:
            expected = base_expected.replace(tzinfo=timezone.utc).astimezone(expected_tz)
            assert result == expected

    @pytest.mark.parametrize(
        ("invalid_input", "error_type"),
        [
            ([1, 2, 3], TypeError),
            ({"value": 1}, TypeError),
            (None, TypeError),
            ("not a number", ValueError),
            ("123abc", ValueError),
        ],
    )
    def test_filetime_to_datetime_invalid(self, invalid_input: Any, error_type: type[Exception]) -> None:
        """Tests converting invalid inputs to datetime.

        This test verifies that the filetime_to_datetime function raises the appropriate exceptions for invalid
        inputs.
        """
        exceptions: type[Exception] | tuple[type[Exception], ...]
        if error_type is TypeError:
            exceptions = (error_type, TypeCheckError)
        else:
            exceptions = error_type

        with pytest.raises(exceptions):
            filetime_to_datetime(invalid_input)

    def test_timezone_conversion(self) -> None:
        """Tests timezone conversion consistency."""
        ft = 116444736000000000  # 116444736000000000 is 1970-01-01 00:00:00 UTC
        dt_utc = filetime_to_datetime(ft)
        assert dt_utc.year == 1970
        assert dt_utc.month == 1
        assert dt_utc.day == 1


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
