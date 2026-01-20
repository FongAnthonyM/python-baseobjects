#!/usr/bin/env python
"""exceldatetodatetime_test.py
Tests for the excel_date_to_datetime function in the baseobjects package.
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
from baseobjects.operations.exceldatetodatetime import EXCEL_INIT_DATE, excel_date_to_datetime


# Definitions #
# Classes #
class TestExcelDateToDatetime:
    """Tests the excel_date_to_datetime function.

    This class tests the functionality of the excel_date_to_datetime function, which converts an Excel date to a
    datetime object.
    """

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("excel_date", "days_offset"),
        [
            (1, 1),
            (0, 0),
            (10000, 10000),
            (1.5, 1.5),
            (0.25, 0.25),
            (-1.5, -1.5),
            ("1", 1),
            ("1.5", 1.5),
            ("-1", -1),
            (b"1", 1),
            (b"1.5", 1.5),
            (b"-1", -1),
        ],
    )
    def test_excel_date_to_datetime_types(self, excel_date: Any, days_offset: float) -> None:
        """Tests converting various types of Excel dates to datetime.

        This test verifies that the excel_date_to_datetime function correctly converts integer, float, string, and bytes
        representations of Excel dates to datetime objects.
        """
        result = excel_date_to_datetime(excel_date, timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=days_offset)
        assert result == expected
        assert result.tzinfo == timezone.utc

    @pytest.mark.parametrize(
        ("tz", "expected_offset"),
        [
            (timezone.utc, timedelta(0)),
            (None, None),
            (timezone(timedelta(hours=-5)), timedelta(hours=-5)),
        ],
    )
    def test_excel_date_to_datetime_timezone(self, tz: Any, expected_offset: timedelta | None) -> None:
        """Tests converting an Excel date with different timezones.

        This test verifies that the excel_date_to_datetime function correctly handles different timezone specifications.
        """
        result = excel_date_to_datetime(1, tz)
        assert result.tzinfo == tz
        if expected_offset is not None:
            assert result.utcoffset() == expected_offset

    @pytest.mark.parametrize(
        ("invalid_input", "error_type"),
        [
            ([1, 2, 3], TypeError),
            ({"value": 1}, TypeError),
            (None, TypeError),
            ("not a number", ValueError),
            ("1.5abc", ValueError),
        ],
    )
    def test_excel_date_to_datetime_invalid(self, invalid_input: Any, error_type: type[Exception]) -> None:
        """Tests converting invalid inputs to datetime.

        This test verifies that the excel_date_to_datetime function raises the appropriate exceptions for invalid
        inputs.
        """
        exceptions: type[Exception] | tuple[type[Exception], ...]
        if error_type is TypeError:
            exceptions = (error_type, TypeCheckError)
        else:
            exceptions = error_type

        with pytest.raises(exceptions):
            excel_date_to_datetime(invalid_input)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
