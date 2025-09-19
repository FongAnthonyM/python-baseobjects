#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from datetime import timezone, timedelta

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.operations.exceldatetodatetime import excel_date_to_datetime, EXCEL_INIT_DATE


# Definitions #
# Classes #
class TestExcelDateToDatetime:
    """Test the excel_date_to_datetime function.

    This class tests_old_ the functionality of the excel_date_to_datetime function, which converts an Excel date to a
    datetime object.
    """

    # Instance Methods #
    # Tests
    def test_excel_date_to_datetime_int(self) -> None:
        """Test converting an integer Excel date to a datetime.

        This test verifies that the excel_date_to_datetime function correctly converts an integer Excel date to a
        datetime object.
        """
        # Test with a simple integer
        result = excel_date_to_datetime(1, timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=1)
        assert result == expected
        assert result.tzinfo == timezone.utc

        # Test with zero (should be the EXCEL_INIT_DATE)
        result = excel_date_to_datetime(0, timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc)
        assert result == expected

        # Test with a larger integer
        result = excel_date_to_datetime(10000, timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=10000)
        assert result == expected

    def test_excel_date_to_datetime_float(self) -> None:
        """Test converting a float Excel date to a datetime.

        This test verifies that the excel_date_to_datetime function correctly converts a float Excel date to a datetime
        object, including fractional days.
        """
        # Test with a simple float (1.5 days = 36 hours)
        result = excel_date_to_datetime(1.5, timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=1.5)
        assert result == expected

        # Test with a small fraction (0.25 days = 6 hours)
        result = excel_date_to_datetime(0.25, timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=0.25)
        assert result == expected

        # Test with a negative float (-1.5 days = -36 hours)
        result = excel_date_to_datetime(-1.5, timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=-1.5)
        assert result == expected

    def test_excel_date_to_datetime_str(self) -> None:
        """Test converting a string Excel date to a datetime.

        This test verifies that the excel_date_to_datetime function correctly converts a string representation of an
        Excel date to a datetime object.
        """
        # Test with a simple string
        result = excel_date_to_datetime("1", timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=1)
        assert result == expected

        # Test with a float string
        result = excel_date_to_datetime("1.5", timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=1.5)
        assert result == expected

        # Test with a negative string
        result = excel_date_to_datetime("-1", timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=-1)
        assert result == expected

    def test_excel_date_to_datetime_bytes(self) -> None:
        """Test converting a bytes Excel date to a datetime.

        This test verifies that the excel_date_to_datetime function correctly converts a bytes representation of an
        Excel date to a datetime object.
        """
        # Test with a simple bytes
        result = excel_date_to_datetime(b"1", timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=1)
        assert result == expected

        # Test with a float bytes
        result = excel_date_to_datetime(b"1.5", timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=1.5)
        assert result == expected

        # Test with a negative bytes
        result = excel_date_to_datetime(b"-1", timezone.utc)
        expected = EXCEL_INIT_DATE.replace(tzinfo=timezone.utc) + timedelta(days=-1)
        assert result == expected

    def test_excel_date_to_datetime_timezone(self) -> None:
        """Test converting an Excel date with different timezones.

        This test verifies that the excel_date_to_datetime function correctly handles different timezone specifications.
        """
        # Test with UTC timezone (default)
        result = excel_date_to_datetime(1)
        assert result.tzinfo == timezone.utc

        # Test with None timezone
        result = excel_date_to_datetime(1, None)
        assert result.tzinfo is None

        # Test with a specific timezone
        est = timezone(timedelta(hours=-5))
        result = excel_date_to_datetime(1, est)
        assert result.tzinfo == est
        assert result.utcoffset() == timedelta(hours=-5)

    def test_excel_date_to_datetime_invalid_type(self) -> None:
        """Test converting an invalid type to a datetime.

        This test verifies that the excel_date_to_datetime function raises a TypeError when an unsupported type is
        provided.
        """
        # Test with a list (unsupported type)
        with pytest.raises(TypeError):
            excel_date_to_datetime([1, 2, 3])

        # Test with a dict (unsupported type)
        with pytest.raises(TypeError):
            excel_date_to_datetime({"value": 1})

        # Test with None (unsupported type)
        with pytest.raises(TypeError):
            excel_date_to_datetime(None)

    def test_excel_date_to_datetime_invalid_string(self) -> None:
        """Test converting an invalid string to a datetime.

        This test verifies that the excel_date_to_datetime function raises a ValueError when an invalid string that
        cannot be converted to a float is provided.
        """
        # Test with a non-numeric string
        with pytest.raises(ValueError):
            excel_date_to_datetime("not a number")

        # Test with a partially numeric string
        with pytest.raises(ValueError):
            excel_date_to_datetime("1.5abc")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])