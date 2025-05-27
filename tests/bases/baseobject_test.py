#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" baseobject_test.py
Tests for the BaseObject class in the baseobjects package.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseObject
from .base_test import BaseBaseObjectTest


# Classes #
class TestBaseObject(BaseBaseObjectTest):
    """Test the BaseObject class.

    This class tests the functionality of the BaseObject class, which is the base class for all objects in the
    baseobjects package. It creates a test subclass of BaseObject to test with.
    """

    # Class Definitions #
    class BaseTestObject(BaseObject):
        """A subclass of BaseObject for testing purposes.

        This class has both mutable and immutable attributes to test copying behavior.
        """
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with immutable and mutable attributes."""
            self.immutable: int = 0
            self.mutable: dict = {}

    class NormalObject(object):
        """A normal Python object for comparison with BaseObject.

        This class has the same attributes as BaseTestObject but inherits from object.
        """
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with immutable and mutable attributes."""
            self.immutable: int = 0
            self.mutable: dict = {}

    # Attributes #
    class_: Type[BaseTestObject] = BaseTestObject

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> 'TestBaseObject.BaseTestObject':
        """Create a test object instance for use in tests.

        Returns:
            BaseTestObject: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self, test_object: 'TestBaseObject.BaseTestObject') -> None:
        """Test that instances of BaseTestObject can be created.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        assert test_object is not None

    def test_copy(self, test_object: 'TestBaseObject.BaseTestObject') -> None:
        """Test the copy method of BaseObject.

        This test verifies that the copy method creates a new object with references to the same attributes
        (shallow copy).

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        new: 'TestBaseObject.BaseTestObject' = test_object.copy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) == id(test_object.mutable)

    def test_deepcopy(self, test_object: 'TestBaseObject.BaseTestObject') -> None:
        """Test the deepcopy method of BaseObject.

        This test verifies that the deepcopy method creates a new object with new copies of mutable attributes but
        references to the same immutable attributes.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        new: 'TestBaseObject.BaseTestObject' = test_object.deepcopy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) != id(test_object.mutable)

    def test_deepcopy_with_memo(self, test_object: 'TestBaseObject.BaseTestObject') -> None:
        """Test the deepcopy method of BaseObject with a memo dictionary.

        This test verifies that the deepcopy method correctly uses the memo dictionary to avoid
        copying the same object twice.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        memo = {}
        new: 'TestBaseObject.BaseTestObject' = test_object.deepcopy(memo=memo)

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
        outer = self.BaseTestObject()
        inner = self.BaseTestObject()
        outer.mutable["inner"] = inner

        # Deepcopy the outer object
        outer_copy = outer.deepcopy()

        # The inner object should also be copied
        assert outer_copy.mutable["inner"] is not inner
        assert isinstance(outer_copy.mutable["inner"], self.BaseTestObject)

    def test_pickle(self, test_object: 'TestBaseObject.BaseTestObject') -> None:
        """Test pickling and unpickling of BaseObject instances.

        This test verifies that BaseObject instances can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
        """
        import pickle

        # Modify the test object
        test_object.immutable = 42
        test_object.mutable["key"] = "value"

        # Pickle and unpickle
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Verify the unpickled object has the same attributes
        assert unpickled.immutable == test_object.immutable
        assert unpickled.mutable == test_object.mutable

        # Verify the unpickled object is a different instance
        assert unpickled is not test_object

    def test_with_slots(self) -> None:
        """Test BaseObject with __slots__.

        This test verifies that BaseObject works correctly with classes that use __slots__.
        """
        class SlottedBaseObject(BaseObject):
            """A BaseObject subclass with __slots__."""
            __slots__ = ("slot1", "slot2")

            def __init__(self) -> None:
                """Initialize with slot attributes."""
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

            def __get__(self, instance: Any, owner: Type) -> Any:
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
                self.regular = "regular"

        # Create and copy an object with a descriptor
        desc_obj = DescriptorBaseObject()
        desc_obj.desc = "modified"
        desc_copy = desc_obj.copy()

        # Verify the copy has the same descriptor value
        assert desc_copy.desc == desc_obj.desc

        # Verify the copy is a different instance
        assert desc_copy is not desc_obj

    def test_dict_modifications(self, test_object: 'TestBaseObject.BaseTestObject') -> None:
        """Test BaseObject with __dict__ modifications.

        This test verifies that BaseObject works correctly when __dict__ is modified directly.

        Args:
            test_object: A fixture providing a BaseTestObject instance.
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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
