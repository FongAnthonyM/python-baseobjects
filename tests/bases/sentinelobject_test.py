"""sentinelobject_test.py
Tests for the SentinelObject class in the baseobjects package.

This module provides tests for the SentinelObject class, which implements a singleton pattern through a registry
mechanism, ensuring that only one instance exists for each unique identifier.
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
import copy
import pickle
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import SentinelObject
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Classes #
class TestSentinelObject(BaseObjectTestSuite):
    """Test the SentinelObject class.

    This class tests the functionality of the SentinelObject class, which implements a singleton pattern through a
    registry mechanism, ensuring that only one instance exists for each unique identifier.
    """

    # Attributes #
    TestClass: Type[SentinelObject] = SentinelObject

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> SentinelObject:
        """Create a test object instance for use in tests.

        Returns:
            SentinelObject: An instance of the SentinelObject class with a test identifier.
        """
        return self.TestClass("TEST_SENTINEL")

    @pytest.fixture
    def test_object_same_id(self) -> SentinelObject:
        """Create a test object with the same ID as test_object.

        Returns:
            SentinelObject: An instance of the SentinelObject class with the same identifier as test_object.
        """
        return self.TestClass("TEST_SENTINEL")

    @pytest.fixture
    def test_object_different_id(self) -> SentinelObject:
        """Create a test object with a different ID than test_object.

        Returns:
            SentinelObject: An instance of the SentinelObject class with a different identifier than test_object.
        """
        return self.TestClass("DIFFERENT_TEST_SENTINEL")

    @pytest.fixture
    def test_object_bytes_id(self) -> SentinelObject:
        """Create a test object with a bytes ID.

        Returns:
            SentinelObject: An instance of the SentinelObject class with a bytes identifier.
        """
        return self.TestClass(b"BYTES_TEST_SENTINEL")

    @pytest.fixture
    def test_object_int_id(self) -> SentinelObject:
        """Create a test object with an integer ID.

        Returns:
            SentinelObject: An instance of the SentinelObject class with an integer identifier.
        """
        return self.TestClass(42)

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of SentinelObject can be created."""
        # Create Object
        obj = self.TestClass("TEST_SENTINEL_CREATION")

        # Validate
        assert isinstance(obj, self.TestClass)
        assert obj.identity == "TEST_SENTINEL_CREATION"

    def test_singleton_behavior_same_id(self, test_object: SentinelObject, test_object_same_id: SentinelObject) -> None:
        """Test that SentinelObject implements the singleton pattern for the same ID.

        This test verifies that two SentinelObject instances created with the same ID are the same object.

        Args:
            test_object: A fixture providing a SentinelObject instance.
            test_object_same_id: A fixture providing another SentinelObject instance with the same ID.
        """
        # Validate
        assert test_object is test_object_same_id
        assert test_object.identity == test_object_same_id.identity
        assert id(test_object) == id(test_object_same_id)

    def test_different_objects_different_ids(
        self, test_object: SentinelObject, test_object_different_id: SentinelObject
    ) -> None:
        """Test that SentinelObject creates different objects for different IDs.

        This test verifies that two SentinelObject instances created with different IDs are different objects.

        Args:
            test_object: A fixture providing a SentinelObject instance.
            test_object_different_id: A fixture providing another SentinelObject instance with a different ID.
        """
        # Validate
        assert test_object is not test_object_different_id
        assert test_object.identity != test_object_different_id.identity
        assert id(test_object) != id(test_object_different_id)

    def test_different_id_types(self, test_object_bytes_id: SentinelObject, test_object_int_id: SentinelObject) -> None:
        """Test that SentinelObject supports different ID types.

        This test verifies that SentinelObject can be created with different ID types (bytes, int).

        Args:
            test_object_bytes_id: A fixture providing a SentinelObject instance with a bytes ID.
            test_object_int_id: A fixture providing a SentinelObject instance with an integer ID.
        """
        # Validate
        assert isinstance(test_object_bytes_id.identity, bytes)
        assert test_object_bytes_id.identity == b"BYTES_TEST_SENTINEL"

        assert isinstance(test_object_int_id.identity, int)
        assert test_object_int_id.identity == 42

        assert test_object_bytes_id is not test_object_int_id

    def test_registry(self) -> None:
        """Test that the sentinel registry correctly tracks sentinel objects."""
        # Clear registry before test (for isolation)
        original_registry = self.TestClass.sentinel_registry.copy()
        self.TestClass.sentinel_registry.clear()

        try:
            # Create sentinel objects
            sentinel1 = self.TestClass("REGISTRY_TEST_1")
            sentinel2 = self.TestClass("REGISTRY_TEST_2")

            # Validate registry
            assert len(self.TestClass.sentinel_registry) == 2
            assert "REGISTRY_TEST_1" in self.TestClass.sentinel_registry
            assert "REGISTRY_TEST_2" in self.TestClass.sentinel_registry
            assert self.TestClass.sentinel_registry["REGISTRY_TEST_1"] is sentinel1
            assert self.TestClass.sentinel_registry["REGISTRY_TEST_2"] is sentinel2

            # Create another sentinel with existing ID
            sentinel1_again = self.TestClass("REGISTRY_TEST_1")

            # Validate registry didn't change
            assert len(self.TestClass.sentinel_registry) == 2
            assert sentinel1_again is sentinel1
        finally:
            # Restore original registry
            self.TestClass.sentinel_registry.clear()
            self.TestClass.sentinel_registry.update(original_registry)

    def test_copy(self, test_object: SentinelObject) -> None:
        """Test the copy behavior of SentinelObject.

        This test verifies that copy returns the original object, preserving the singleton pattern.

        Args:
            test_object: A fixture providing a SentinelObject instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is test_object
        assert id(obj_copy) == id(test_object)

    def test_copy_method(self, test_object: SentinelObject) -> None:
        """Test the copy method behavior of SentinelObject.

        This test verifies that the copy method returns the original object, preserving the singleton pattern.

        Args:
            test_object: A fixture providing a SentinelObject instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is test_object
        assert id(obj_copy) == id(test_object)

    def test_deepcopy(self, test_object: SentinelObject, memo: dict | None = None) -> None:
        """Test the deep copy behavior of SentinelObject.

        This test verifies that deepcopy returns the original object, preserving the singleton pattern.

        Args:
            test_object: A fixture providing a SentinelObject instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is test_object
        assert id(obj_deepcopy) == id(test_object)

    def test_deepcopy_method(self, test_object: SentinelObject, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of SentinelObject.

        This test verifies that the deepcopy method returns the original object, preserving the singleton pattern.

        Args:
            test_object: A fixture providing a SentinelObject instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is test_object
        assert id(obj_deepcopy) == id(test_object)

    def test_pickling(self, test_object: SentinelObject) -> None:
        """Test pickling and unpickling of SentinelObject.

        This test verifies that the object can be pickled and unpickled correctly, and that the unpickled object
        is the same object as the original due to the singleton pattern.

        Args:
            test_object: A fixture providing a SentinelObject instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is test_object
        assert id(unpickled) == id(test_object)
        assert unpickled.identity == test_object.identity

    def test_predefined_constants(self) -> None:
        """Test the predefined sentinel constants.

        This test verifies that the predefined sentinel constants DEFAULTSENTINEL and SEARCHSENTINEL
        are instances of SentinelObject with the correct identities.
        """
        from src.baseobjects.bases.sentinelobject import DEFAULTSENTINEL, SEARCHSENTINEL

        # Validate DEFAULTSENTINEL
        assert isinstance(DEFAULTSENTINEL, SentinelObject)
        assert DEFAULTSENTINEL.identity == "DEFAULTSENTINEL"
        assert DEFAULTSENTINEL is SentinelObject("DEFAULTSENTINEL")

        # Validate SEARCHSENTINEL
        assert isinstance(SEARCHSENTINEL, SentinelObject)
        assert SEARCHSENTINEL.identity == "SEARCHSENTINEL"
        assert SEARCHSENTINEL is SentinelObject("SEARCHSENTINEL")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
