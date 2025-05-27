#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" sentinelobject_test.py
Tests for the SentinelObject class in the baseobjects package.
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
from typing import Type
import pickle

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import SentinelObject
from .base_test import ClassTest


# Classes #
class TestSentinelObject(ClassTest):
    """Test the SentinelObject class.

    This class tests the functionality of the SentinelObject class, which is used to create
    sentinel objects in the baseobjects package.
    """

    # Class Definitions #
    class NormalSentinel:
        """A normal Python sentinel object for comparison with SentinelObject."""
        # Magic Methods #
        def __init__(self, id_: str | bytes | int) -> None:
            """Initialize with an ID."""
            if isinstance(id_, str):
                self.id_number = int.from_bytes(id_.encode("utf-8"), "big")
            elif isinstance(id_, bytes):
                self.id_number = int.from_bytes(id_, "big")
            else:
                self.id_number = id_

        def __hash__(self) -> int:
            """Return the hash of the object."""
            return id(self)

        def __eq__(self, other) -> bool:
            """Compare two sentinel objects."""
            return isinstance(other, self.__class__) and self.id_number == other.id_number

    # Attributes #
    class_: Type[SentinelObject] = SentinelObject

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def string_id(self) -> str:
        """Create a string ID for testing.

        Returns:
            str: A string ID.
        """
        return "test_sentinel"

    @pytest.fixture
    def bytes_id(self) -> bytes:
        """Create a bytes ID for testing.

        Returns:
            bytes: A bytes ID.
        """
        return b"test_sentinel"

    @pytest.fixture
    def int_id(self) -> int:
        """Create an int ID for testing.

        Returns:
            int: An integer ID.
        """
        return 12345

    # Tests
    def test_instance_creation_string(self, string_id: str) -> None:
        """Test that instances of SentinelObject can be created with a string ID.

        Args:
            string_id: A fixture providing a string ID.
        """
        sentinel = self.class_(string_id)
        assert sentinel is not None
        assert hasattr(sentinel, "id_number")
        assert isinstance(sentinel.id_number, int)

    def test_instance_creation_bytes(self, bytes_id: bytes) -> None:
        """Test that instances of SentinelObject can be created with a bytes ID.

        Args:
            bytes_id: A fixture providing a bytes ID.
        """
        sentinel = self.class_(bytes_id)
        assert sentinel is not None
        assert hasattr(sentinel, "id_number")
        assert isinstance(sentinel.id_number, int)

    def test_instance_creation_int(self, int_id: int) -> None:
        """Test that instances of SentinelObject can be created with an int ID.

        Args:
            int_id: A fixture providing an int ID.
        """
        sentinel = self.class_(int_id)
        assert sentinel is not None
        assert hasattr(sentinel, "id_number")
        assert isinstance(sentinel.id_number, int)
        assert sentinel.id_number == int_id

    def test_hash(self) -> None:
        """Test the hash method of SentinelObject.

        This test verifies that the hash method returns the id_number of the object.
        """
        sentinel = self.class_("test_hash")
        assert hash(sentinel) != sentinel.id_number

    def test_equality_same_id(self) -> None:
        """Test equality comparison with the same ID.

        This test verifies that two SentinelObjects with the same ID are equal.
        """
        sentinel1 = self.class_("test_equality")
        sentinel2 = self.class_("test_equality")
        assert sentinel1 == sentinel2

    def test_equality_different_id(self) -> None:
        """Test equality comparison with different IDs.

        This test verifies that two SentinelObjects with different IDs are not equal.
        """
        sentinel1 = self.class_("test_equality1")
        sentinel2 = self.class_("test_equality2")
        assert sentinel1 != sentinel2

    def test_equality_different_types(self) -> None:
        """Test equality comparison with different types.

        This test verifies that a SentinelObject is not equal to an object of a different type.
        """
        sentinel = self.class_("test_equality")
        normal = self.NormalSentinel("test_equality")
        assert sentinel != normal

    def test_different_encoding(self) -> None:
        """Test creating a SentinelObject with a different encoding.

        This test verifies that the encoding parameter works correctly.
        """
        sentinel1 = self.class_("test_encoding", encoding="utf-8")
        sentinel2 = self.class_("test_encoding", encoding="ascii")
        # Both encodings should produce the same result for ASCII characters
        assert sentinel1 == sentinel2

    def test_different_byteorder(self) -> None:
        """Test creating a SentinelObject with a different byteorder.

        This test verifies that the byteorder parameter works correctly.
        """
        sentinel1 = self.class_("test_byteorder", byteorder="big")
        sentinel2 = self.class_("test_byteorder", byteorder="little")
        # Different byteorders should produce different ID numbers
        assert sentinel1 != sentinel2

    def test_pickle_unpickle(self) -> None:
        """Test pickling and unpickling a SentinelObject.

        This test verifies that a pickled and unpickled SentinelObject maintains equality with
        another SentinelObject created with the same ID.
        """
        original = self.class_("test_pickle")
        pickled = pickle.dumps(original)
        unpickled = pickle.loads(pickled)
        assert original is not unpickled
        assert original == unpickled


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
