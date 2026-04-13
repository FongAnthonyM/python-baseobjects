"""sentinelobjecttestsuite.py
Base class for test suites which test SentinelObject and its subclasses.

This module provides a base test suite for testing the SentinelObject class and its subclasses. It includes tests for
singleton behavior, copying, and pickling.
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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import SentinelObject
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Classes #
class SentinelObjectTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test SentinelObject and its subclasses.

    This class provides common functionality for test suites that test sentinel objects, including ensuring
    singleton behavior and correct copying/pickling.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be SentinelObject or a subclass.
    """

    # Attributes #
    UnitTestClass: type[SentinelObject]

    # Fixtures #
    @pytest.fixture
    def test_object(self) -> SentinelObject:
        """Creates a test object instance for use in tests.

        Returns:
            SentinelObject: An instance of the SentinelObject class with a test identifier.
        """
        return self.UnitTestClass("TEST_SENTINEL")

    @pytest.fixture
    def test_object_same_id(self) -> SentinelObject:
        """Creates a test object with the same ID as test_object.

        Returns:
            SentinelObject: An instance of the SentinelObject class with the same identifier as test_object.
        """
        return self.UnitTestClass("TEST_SENTINEL")

    @pytest.fixture
    def test_object_different_id(self) -> SentinelObject:
        """Creates a test object with a different ID than test_object.

        Returns:
            SentinelObject: An instance of the SentinelObject class with a different identifier than test_object.
        """
        return self.UnitTestClass("DIFFERENT_TEST_SENTINEL")

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of SentinelObject can be created."""
        # Creates Object
        obj = self.UnitTestClass("TEST_SENTINEL_CREATION")

        # Validate
        assert isinstance(obj, self.UnitTestClass)
        assert obj.identity == "TEST_SENTINEL_CREATION"

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: SentinelObject, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of SentinelObject.

        This test verifies that copy returns the original object, preserving the singleton pattern.

        Args:
            test_object: A fixture providing a SentinelObject instance.
            method: The method to use for copying ('copy' or 'method').
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        # Validate
        assert obj_copy is test_object
        assert id(obj_copy) == id(test_object)

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        test_object: SentinelObject,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:
        """Tests the deep copy behavior of SentinelObject.

        This test verifies that deepcopy returns the original object, preserving the singleton pattern.

        Args:
            test_object: A fixture providing a SentinelObject instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        else:
            obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is test_object
        assert id(obj_deepcopy) == id(test_object)

    def test_deepcopy_with_memo(self, test_object: SentinelObject) -> None:  # type: ignore[override]
        """Tests the deepcopy method of BaseObject with a memo dictionary.

        This test verifies that the deepcopy method correctly uses the memo dictionary to avoid
        copying the same object twice.

        Args:
            test_object: A fixture providing a test object instance.
        """
        memo: dict[Any, Any] = {}
        new = test_object.deepcopy(memo=memo)

        # The object should be in the memo dictionary
        # assert id(test_object) in memo
        # assert memo[id(test_object)] is new

        # A second deepcopy with the same memo should return the same object
        second_new = test_object.deepcopy(memo=memo)
        assert second_new is new

        # For SentinelObject, new and test_object are the same
        assert new is test_object

    # Pickling #
    def test_pickling(self, test_object: SentinelObject) -> None:
        """Tests pickling and unpickling of SentinelObject.

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

    # Tests #
    def test_dict_modifications(self, test_object: SentinelObject) -> None:
        """Tests BaseObject with __dict__ modifications.

        This test verifies that SentinelObject works correctly when __dict__ is modified directly.
        Since SentinelObject is a singleton, the copy is the same object.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Modify __dict__ directly
        test_object.__dict__["new_attr"] = "new value"

        # Verifies the attribute is accessible
        if hasattr(test_object, "new_attr"):
            assert test_object.new_attr == "new value"

        # Copy the object
        copy_obj = test_object.copy()

        # Verifies the copy is the same instance
        assert copy_obj is test_object

        # Verifies the copy has the same attribute (since it's the same object)
        if hasattr(copy_obj, "new_attr"):
            assert copy_obj.new_attr == "new value"

    def test_singleton_behavior_same_id(self, test_object: SentinelObject, test_object_same_id: SentinelObject) -> None:
        """Tests that SentinelObject implements the singleton pattern for the same ID.

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
        self,
        test_object: SentinelObject,
        test_object_different_id: SentinelObject,
    ) -> None:
        """Tests that SentinelObject creates different objects for different IDs.

        This test verifies that two SentinelObject instances created with different IDs are different objects.

        Args:
            test_object: A fixture providing a SentinelObject instance.
            test_object_different_id: A fixture providing another SentinelObject instance with a different ID.
        """
        # Validate
        assert test_object is not test_object_different_id
        assert test_object.identity != test_object_different_id.identity
        assert id(test_object) != id(test_object_different_id)

    @pytest.mark.parametrize("sentinel_id", [b"BYTES_TEST_SENTINEL", 42])
    def test_id_types(self, sentinel_id: Any) -> None:
        """Tests that SentinelObject supports different ID types.

        This test verifies that SentinelObject can be created with different ID types (bytes, int).

        Args:
            sentinel_id: The ID to use for the sentinel object.
        """
        # Creates Object
        obj = self.UnitTestClass(sentinel_id)

        # Validate
        assert obj.identity == sentinel_id
        assert isinstance(obj.identity, sentinel_id.__class__)

    def test_registry(self) -> None:
        """Tests that the sentinel registry correctly tracks sentinel objects."""
        # Clear registry before test (for isolation)
        original_registry = self.UnitTestClass.sentinel_registry.copy()
        self.UnitTestClass.sentinel_registry.clear()

        try:
            # Creates sentinel objects
            sentinel1 = self.UnitTestClass("REGISTRY_TEST_1")
            sentinel2 = self.UnitTestClass("REGISTRY_TEST_2")

            # Validate registry
            assert len(self.UnitTestClass.sentinel_registry) == 2
            assert "REGISTRY_TEST_1" in self.UnitTestClass.sentinel_registry
            assert "REGISTRY_TEST_2" in self.UnitTestClass.sentinel_registry
            assert self.UnitTestClass.sentinel_registry["REGISTRY_TEST_1"] is sentinel1
            assert self.UnitTestClass.sentinel_registry["REGISTRY_TEST_2"] is sentinel2

            # Creates another sentinel with existing ID
            sentinel1_again = self.UnitTestClass("REGISTRY_TEST_1")

            # Validate registry didn't change
            assert len(self.UnitTestClass.sentinel_registry) == 2
            assert sentinel1_again is sentinel1
        finally:
            # Restore original registry
            self.UnitTestClass.sentinel_registry.clear()
            self.UnitTestClass.sentinel_registry.update(original_registry)
