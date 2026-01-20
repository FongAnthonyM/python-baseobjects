#!/usr/bin/env python
"""bytestobin_test.py
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
from collections.abc import Callable
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.operations import bytes_to_bin


# Definitions #
# Classes #
class TestBytesToBin:
    """Tests the bytes_to_bin function.

    This class tests the functionality of the bytes_to_bin function, which converts bytes to a tuple of binary values.
    """

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("byte_order", "expected_single", "expected_multiple", "expected_all"),
        [
            (
                "big",
                (0, 0, 0, 0, 0, 0, 0, 1),
                (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0),
                (1, 1, 1, 1, 1, 1, 1, 1),
            ),
            (
                "little",
                (0, 0, 0, 1, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
                (1, 1, 1, 1, 1, 1, 1, 1),
            ),
        ],
    )
    def test_bytes_to_bin_endian(
        self,
        byte_order: str,
        expected_single: tuple[int, ...],
        expected_multiple: tuple[int, ...],
        expected_all: tuple[int, ...],
    ) -> None:
        """Tests converting bytes to binary values with different byte orders.

        This test verifies that the bytes_to_bin function correctly converts bytes to binary values using both big and
        little endian byte orders.
        """
        # Test with a simple byte
        result = bytes_to_bin(b"\x01", byteorder=byte_order)
        assert result == expected_single

        # Test with multiple bytes
        result = bytes_to_bin(b"\x01\x02", byteorder=byte_order)
        assert result == expected_multiple

        # Test with all bits set
        result = bytes_to_bin(b"\xff", byteorder=byte_order)
        assert result == expected_all

    @staticmethod
    def custom_type(val: bool) -> str:
        """A custom type conversion function.

        Returns:
            The converted string.
        """
        return "1" if val else "0"

    @pytest.mark.parametrize(
        ("out_type", "expected"),
        [
            (bool, (False, False, False, False, False, False, False, True)),
            (str, ("False", "False", "False", "False", "False", "False", "False", "True")),
            (custom_type, ("0", "0", "0", "0", "0", "0", "0", "1")),
        ],
    )
    def test_bytes_to_bin_different_output_types(
        self,
        out_type: type | Callable[[bool], Any],
        expected: tuple[Any, ...],
    ) -> None:
        """Tests converting bytes to binary values with different output types.

        This test verifies that the bytes_to_bin function correctly converts bytes to binary values using different
        output types.
        """
        # Test with specified output type
        result = bytes_to_bin(b"\x01", byteorder="big", out_type=out_type)
        assert result == expected

    @pytest.mark.parametrize("byte_order", ["big", "little"])
    def test_bytes_to_bin_empty_bytes(self, byte_order: str) -> None:
        """Tests converting empty bytes to binary values.

        This test verifies that the bytes_to_bin function correctly handles empty bytes.
        """
        result = bytes_to_bin(b"", byteorder=byte_order)
        assert result == ()

    def test_bytes_to_bin_invalid_byteorder(self) -> None:
        """Tests converting bytes with an invalid byte order.

        This test verifies that the bytes_to_bin function raises a ValueError when an invalid byte order is provided.
        """
        with pytest.raises(ValueError, match="byteorder must be either 'little' or 'big'"):
            bytes_to_bin(b"\x01", byteorder="invalid")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
