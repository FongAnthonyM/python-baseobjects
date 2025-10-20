"""baseobject_test.py
Tests for the BaseObject class in the baseobjects package.

This module provides tests for the BaseObject class, which is an abstract base class that implements fundamental
functionality that should be available in all objects, such as copying and deep copying.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases import BaseObject
from src.baseobjects.testsuite import BaseObjectTestSuite


# Classes #
class BaseTestObject(BaseObject):
    """A subclass of BaseObject for testing purposes.

    This class has both mutable and immutable attributes to test copying behavior.
    """

    # Magic Methods #
    def __init__(self) -> None:
        """Initialize with immutable and mutable attributes."""
        super().__init__()
        self.immutable: int = 0
        self.mutable: dict = {}


# Tests #
class TestBaseObject(BaseObjectTestSuite):
    """Test the BaseObject class.

    This class tests the functionality of the BaseObject class, which is the base class for all objects in the
    baseobjects package. It creates a test subclass of BaseObject to test with.
    """

    # Attributes #
    TestClass: type[BaseObject] = BaseTestObject

    # Instance Methods #
    # Tests
    def test_copy(self, test_object: BaseObject) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.immutable == test_object.immutable
        assert obj_copy.mutable == test_object.mutable
        assert id(obj_copy.mutable) == id(test_object.mutable)  # Shallow copy, same reference

    def test_copy_method(self, test_object: BaseObject) -> None:
        """Test the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.immutable == test_object.immutable
        assert obj_copy.mutable == test_object.mutable
        assert id(obj_copy.mutable) == id(test_object.mutable)  # Shallow copy, same reference

    def test_deepcopy(self, test_object: BaseObject, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.immutable == test_object.immutable
        assert obj_deepcopy.mutable == test_object.mutable
        assert id(obj_deepcopy.mutable) != id(test_object.mutable)  # Deep copy, different reference

    def test_deepcopy_method(self, test_object: BaseObject, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.immutable == test_object.immutable
        assert obj_deepcopy.mutable == test_object.mutable
        assert id(obj_deepcopy.mutable) != id(test_object.mutable)  # Deep copy, different reference

    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Modify the test object
        test_object.immutable = 42
        test_object.mutable["key"] = "value"

        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.TestClass)
        assert unpickled.immutable == test_object.immutable
        assert unpickled.mutable == test_object.mutable

    def test_with_slots(self) -> None:
        """Test BaseObject with __slots__.

        This test verifies that BaseObject works correctly with classes that use __slots__.
        """

        class SlottedBaseObject(BaseObject):
            """A BaseObject subclass with __slots__."""

            __slots__ = ("slot1", "slot2")

            def __init__(self) -> None:
                """Initialize with slot attributes."""
                super().__init__()
                self.slot1 = "value1"
                self.slot2 = "value2"

        # Create and copy a slotted object
        slotted = SlottedBaseObject()
        slotted_copy = slotted.copy()

        # Verify the copy has the same slot values
        assert slotted_copy.slot1 == slotted.slot1
        assert slotted_copy.slot2 == slotted.slot2

        # Verify the copy is a different instance
        assert slotted_copy is not slotted

    def test_with_properties(self) -> None:
        """Test BaseObject with properties.

        This test verifies that BaseObject works correctly with classes that use properties.
        """

        class PropertyBaseObject(BaseObject):
            """A BaseObject subclass with properties."""

            def __init__(self) -> None:
                """Initialize with a private attribute."""
                super().__init__()
                self._value = "initial"

            @property
            def value(self) -> str:
                """Get the value."""
                return self._value

            @value.setter
            def value(self, new_value: str) -> None:
                """Set the value."""
                self._value = new_value

        # Create and copy an object with properties
        prop_obj = PropertyBaseObject()
        prop_obj.value = "modified"
        prop_copy = prop_obj.copy()

        # Verify the copy has the same property value
        assert prop_copy.value == prop_obj.value

        # Verify the copy is a different instance
        assert prop_copy is not prop_obj

        # Verify changing the property in one doesn't affect the other
        prop_obj.value = "changed again"
        assert prop_copy.value != prop_obj.value

    def test_with_descriptors(self) -> None:
        """Test BaseObject with descriptors.

        This test verifies that BaseObject works correctly with classes that use descriptors.
        """

        class MyDescriptor:
            """A simple descriptor class."""

            def __init__(self, initial_value: Any = None) -> None:
                """Initialize with an initial value."""
                self.value = initial_value

            def __get__(self, instance: Any, owner: type) -> Any:
                """Get the descriptor value."""
                if instance is None:
                    return self
                return self.value

            def __set__(self, instance: Any, value: Any) -> None:
                """Set the descriptor value."""
                self.value = value

        class DescriptorBaseObject(BaseObject):
            """A BaseObject subclass with a descriptor."""

            desc = MyDescriptor("initial")

            def __init__(self) -> None:
                """Initialize with a regular attribute."""
                super().__init__()
                self.regular = "regular"

        # Create and copy an object with a descriptor
        desc_obj = DescriptorBaseObject()
        desc_obj.desc = "modified"
        desc_copy = desc_obj.copy()

        # Verify the copy has the same descriptor value
        assert desc_copy.desc == desc_obj.desc

        # Verify the copy is a different instance
        assert desc_copy is not desc_obj

    def test_dict_modifications(self, test_object: BaseObject) -> None:
        """Test BaseObject with __dict__ modifications.

        This test verifies that BaseObject works correctly when __dict__ is modified directly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Modify __dict__ directly
        test_object.__dict__["new_attr"] = "new value"

        # Verify the attribute is accessible
        assert test_object.new_attr == "new value"

        # Copy the object
        copy_obj = test_object.copy()

        # Verify the copy has the same attribute
        assert copy_obj.new_attr == test_object.new_attr

        # Verify the copy is a different instance
        assert copy_obj is not test_object

    def test_deepcopy_with_memo(self, test_object: BaseObject) -> None:
        """Test the deepcopy method of BaseObject with a memo dictionary.

        This test verifies that the deepcopy method correctly uses the memo dictionary to avoid
        copying the same object twice.

        Args:
            test_object: A fixture providing a test object instance.
        """
        memo = {}
        new = test_object.deepcopy(memo=memo)

        # The object should be in the memo dictionary
        assert id(test_object) in memo
        assert memo[id(test_object)] is new

        # A second deepcopy with the same memo should return the same object
        second_new = test_object.deepcopy(memo=memo)
        assert second_new is new

    def test_deepcopy_nested(self) -> None:
        """Test deepcopy with nested BaseObject instances.

        This test verifies that deepcopy correctly handles nested BaseObject instances.
        """
        # Create a BaseObject with a nested BaseObject
        outer = self.TestClass()
        inner = self.TestClass()
        outer.mutable["inner"] = inner

        # Deepcopy the outer object
        outer_copy = outer.deepcopy()

        # The inner object should also be copied
        assert outer_copy.mutable["inner"] is not inner
        assert isinstance(outer_copy.mutable["inner"], self.TestClass)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
