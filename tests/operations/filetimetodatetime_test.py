#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""filetimetodatetime_test.py
Tests for the filetime_to_datetime function in the baseobjects package.

This module contains tests for the filetime_to_datetime function, which converts Windows FILETIME values to Python
datetime objects. It tests various input types (int, float, str, bytes, bytearray) and timezone handling, as well as
error cases for invalid inputs.

Typical usage example:

  # Run all tests in this module
  pytest tests/operations/filetimetodatetime_test.py

  # Run a specific test
  pytest tests/operations/filetimetodatetime_test.py::TestFiletimeToDatetime::test_filetime_to_datetime_int
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
from src.baseobjects.operations.filetimetodatetime import filetime_to_datetime, FILETIME_INIT_DATE


# Definitions #
# Classes #
class TestFiletimeToDatetime:
    """Test the filetime_to_datetime function.

    This class tests the functionality of the filetime_to_datetime function, which converts a Windows filetime to a
    datetime object.
    """

    # Instance Methods #
    # Tests
    def test_filetime_to_datetime_int(self) -> None:
        """Test converting an integer filetime to a datetime.

        This test verifies that the filetime_to_datetime function correctly converts an integer filetime to a datetime
        object.
        """
        # Test with a simple integer
        result = filetime_to_datetime(1000000, None)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=1000000)
        assert result == expected
        assert result.tzinfo is None

        # Test with zero (should be the FILETIME_INIT_DATE)
        result = filetime_to_datetime(0, None)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None)
        assert result == expected

        # Test with a larger integer
        result = filetime_to_datetime(10000000000, None)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=10000000000)
        assert result == expected

    def test_filetime_to_datetime_float(self) -> None:
        """Test converting a float filetime to a datetime.

        This test verifies that the filetime_to_datetime function correctly converts a float filetime to a datetime
        object, including division by 10.
        """
        # Test with a simple float
        result = filetime_to_datetime(10000.0, None)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=1000.0)
        assert result == expected

        # Test with a larger float
        result = filetime_to_datetime(100000000.0, None)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=10000000.0)
        assert result == expected

    def test_filetime_to_datetime_str(self) -> None:
        """Test converting a string filetime to a datetime.

        This test verifies that the filetime_to_datetime function correctly converts a string representation of a
        filetime to a datetime object.
        """
        # Test with a simple string
        result = filetime_to_datetime("10000", None)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=1000.0)
        assert result == expected

        # Test with a larger string
        result = filetime_to_datetime("100000000", None)
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=10000000.0)
        assert result == expected

    def test_filetime_to_datetime_bytes(self) -> None:
        """Test converting a bytes filetime to a datetime.

        This test verifies that the filetime_to_datetime function correctly converts a bytes representation of a
        filetime to a datetime object.
        """
        # Test with a simple bytes (10000 in little-endian)
        result = filetime_to_datetime(b"\x10\x27\x00\x00\x00\x00\x00\x00", None)
        # 0x2710 = 10000, divided by 10 = 1000 microseconds
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=1000.0)
        assert result == expected

        # Test with a different bytes value
        result = filetime_to_datetime(b"\x40\x42\x0f\x00\x00\x00\x00\x00", None)
        # 0x0f4240 = 1000000, divided by 10 = 100000 microseconds
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=100000.0)
        assert result == expected

    def test_filetime_to_datetime_bytearray(self) -> None:
        """Test converting a bytearray filetime to a datetime.

        This test verifies that the filetime_to_datetime function correctly converts a bytearray representation of a
        filetime to a datetime object.
        """
        # Test with a simple bytearray (10000 in little-endian)
        result = filetime_to_datetime(bytearray(b"\x10\x27\x00\x00\x00\x00\x00\x00"), None)
        # 0x2710 = 10000, divided by 10 = 1000 microseconds
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=1000.0)
        assert result == expected

        # Test with a different bytearray value
        result = filetime_to_datetime(bytearray(b"\x40\x42\x0f\x00\x00\x00\x00\x00"), None)
        # 0x0f4240 = 1000000, divided by 10 = 100000 microseconds
        expected = FILETIME_INIT_DATE.replace(tzinfo=None) + timedelta(microseconds=100000.0)
        assert result == expected

    def test_filetime_to_datetime_timezone(self) -> None:
        """Test converting a filetime with different timezones.

        This test verifies that the filetime_to_datetime function correctly handles different timezone specifications.
        """
        # Test with None timezone (default)
        result = filetime_to_datetime(1000000)
        assert result.tzinfo is None

        # Test with UTC timezone
        result = filetime_to_datetime(1000000, timezone.utc)
        assert result.tzinfo == timezone.utc

        # Test with a specific timezone
        est = timezone(timedelta(hours=-5))
        result = filetime_to_datetime(1000000, est)
        assert result.tzinfo == est
        assert result.utcoffset() == timedelta(hours=-5)

    def test_filetime_to_datetime_invalid_type(self) -> None:
        """Test converting an invalid type to a datetime.

        This test verifies that the filetime_to_datetime function raises a TypeError when an unsupported type is
        provided.
        """
        # Test with a list (unsupported type)
        with pytest.raises(TypeError):
            filetime_to_datetime([1, 2, 3])

        # Test with a dict (unsupported type)
        with pytest.raises(TypeError):
            filetime_to_datetime({"value": 1})

        # Test with None (unsupported type)
        with pytest.raises(TypeError):
            filetime_to_datetime(None)

    def test_filetime_to_datetime_invalid_string(self) -> None:
        """Test converting an invalid string to a datetime.

        This test verifies that the filetime_to_datetime function raises a ValueError when an invalid string that cannot
        be converted to an integer is provided.
        """
        # Test with a non-numeric string
        with pytest.raises(ValueError):
            filetime_to_datetime("not a number")

        # Test with a partially numeric string
        with pytest.raises(ValueError):
            filetime_to_datetime("123abc")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
