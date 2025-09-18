#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" bytestobin_test.py
Tests for the bytes_to_bin function in the baseobjects package.
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

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.operations import bytes_to_bin


# Definitions #
# Classes #
class TestBytesToBin:
    """Test the bytes_to_bin function.

    This class tests_old_ the functionality of the bytes_to_bin function, which converts bytes to a tuple of binary values.
    """

    # Instance Methods #
    # Tests
    def test_bytes_to_bin_big_endian(self) -> None:
        """Test converting bytes to binary values with big endian byte order.

        This test verifies that the bytes_to_bin function correctly converts bytes to binary values using big endian
        byte order.
        """
        # Test with a simple byte
        result = bytes_to_bin(b'\x01', byteorder="big")
        expected = (0, 0, 0, 0, 0, 0, 0, 1)
        assert result == expected

        # Test with multiple bytes
        result = bytes_to_bin(b'\x01\x02', byteorder="big")
        expected = (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0)
        assert result == expected

        # Test with all bits set
        result = bytes_to_bin(b'\xff', byteorder="big")
        expected = (1, 1, 1, 1, 1, 1, 1, 1)
        assert result == expected

    def test_bytes_to_bin_little_endian(self) -> None:
        """Test converting bytes to binary values with little endian byte order.

        This test verifies that the bytes_to_bin function correctly converts bytes to binary values using little endian
        byte order.
        """
        # Test with a simple byte
        result = bytes_to_bin(b'\x01', byteorder="little")
        expected = (0, 0, 0, 1, 0, 0, 0, 0)
        assert result == expected

        # Test with multiple bytes
        result = bytes_to_bin(b'\x01\x02', byteorder="little")
        expected = (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
        assert result == expected

        # Test with all bits set
        result = bytes_to_bin(b'\xff', byteorder="little")
        expected = (1, 1, 1, 1, 1, 1, 1, 1)
        assert result == expected

    def test_bytes_to_bin_different_output_types(self) -> None:
        """Test converting bytes to binary values with different output types.

        This test verifies that the bytes_to_bin function correctly converts bytes to binary values using different
        output types.
        """
        # Test with bool output type
        result = bytes_to_bin(b'\x01', byteorder="big", out_type=bool)
        expected = (False, False, False, False, False, False, False, True)
        assert result == expected

        # Test with str output type
        result = bytes_to_bin(b'\x01', byteorder="big", out_type=str)
        expected = ('False', 'False', 'False', 'False', 'False', 'False', 'False', 'True')
        assert result == expected

        # Custom output type function
        def custom_type(value: bool) -> str:
            return "1" if value else "0"

        result = bytes_to_bin(b'\x01', byteorder="big", out_type=custom_type)
        expected = ('0', '0', '0', '0', '0', '0', '0', '1')
        assert result == expected

    def test_bytes_to_bin_empty_bytes(self) -> None:
        """Test converting empty bytes to binary values.

        This test verifies that the bytes_to_bin function correctly handles empty bytes.
        """
        result = bytes_to_bin(b'', byteorder="big")
        assert result == ()

        result = bytes_to_bin(b'', byteorder="little")
        assert result == ()

    def test_bytes_to_bin_invalid_byteorder(self) -> None:
        """Test converting bytes with an invalid byte order.

        This test verifies that the bytes_to_bin function raises a ValueError when an invalid byte order is provided.
        """
        with pytest.raises(ValueError, match="byteorder must be either 'little' or 'big'"):
            bytes_to_bin(b'\x01', byteorder="invalid")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])