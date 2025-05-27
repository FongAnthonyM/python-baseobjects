#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basereducible_test.py
Tests for the BaseReducible class in the baseobjects package.
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
from src.baseobjects.bases import BaseReducible
from .base_test import BaseBaseObjectTest


# Classes #
class TestBaseReducible(BaseBaseObjectTest):
    """Test the BaseReducible class.

    This class tests the functionality of the BaseReducible class, which is a base class for objects that need to be
    pickled/reduced in the baseobjects package.
    """

    # Class Definitions #
    class ReducibleTestObject(BaseReducible):
        """A subclass of BaseReducible for testing purposes.

        This class has both normal attributes and slot attributes to test pickling behavior.
        """
        __slots__ = ("slot_value",)

        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with normal and slot attributes."""
            super().__init__()
            self.normal_value: str = "normal"
            self.slot_value: str = "slot"

    # Attributes #
    class_: Type[BaseReducible] = BaseReducible

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestBaseReducible.ReducibleTestObject":
        """Create a test object instance for use in tests.

        Returns:
            ReducibleTestObject: An instance of the test class.
        """
        return self.ReducibleTestObject()

    # Tests
    def test_instance_creation(self, test_object: "TestBaseReducible.ReducibleTestObject") -> None:
        """Test that instances of ReducibleTestObject can be created.

        Args:
            test_object: A fixture providing a ReducibleTestObject instance.
        """
        assert test_object is not None
        assert test_object.normal_value == "normal"
        assert test_object.slot_value == "slot"

    def test_getstate(self, test_object: "TestBaseReducible.ReducibleTestObject") -> None:
        """Test the __getstate__ method of BaseReducible.

        This test verifies that __getstate__ correctly captures both __dict__ and __slots__ attributes.

        Args:
            test_object: A fixture providing a ReducibleTestObject instance.
        """
        state = test_object.__getstate__()
        assert isinstance(state, tuple)
        assert len(state) == 2
        assert isinstance(state[0], dict)
        assert isinstance(state[1], dict)
        assert "normal_value" in state[0]
        assert state[0]["normal_value"] == "normal"
        assert "slot_value" in state[1]
        assert state[1]["slot_value"] == "slot"

    def test_setstate(self, test_object: "TestBaseReducible.ReducibleTestObject") -> None:
        """Test the __setstate__ method of BaseReducible.

        This test verifies that __setstate__ correctly restores both __dict__ and __slots__ attributes.

        Args:
            test_object: A fixture providing a ReducibleTestObject instance.
        """
        # Create a modified state
        state = ({"normal_value": "modified"}, {"slot_value": "modified_slot"})

        # Apply the state
        test_object.__setstate__(state)

        # Verify the state was applied
        assert test_object.normal_value == "modified"
        assert test_object.slot_value == "modified_slot"

    def test_setstate_dict_only(self, test_object: "TestBaseReducible.ReducibleTestObject") -> None:
        """Test the __setstate__ method with only a dict.

        This test verifies that __setstate__ correctly handles a state that is just a dict.

        Args:
            test_object: A fixture providing a ReducibleTestObject instance.
        """
        # Create a modified state with only dict
        state = {"normal_value": "dict_only"}

        # Apply the state
        test_object.__setstate__(state)

        # Verify the state was applied
        assert test_object.normal_value == "dict_only"
        assert test_object.slot_value == "slot"  # Should remain unchanged

    def test_setstate_none(self, test_object: "TestBaseReducible.ReducibleTestObject") -> None:
        """Test the __setstate__ method with None.

        This test verifies that __setstate__ correctly handles a None state.

        Args:
            test_object: A fixture providing a ReducibleTestObject instance.
        """
        # Apply None state
        test_object.__setstate__(None)

        # Verify the state remains unchanged
        assert test_object.normal_value == "normal"
        assert test_object.slot_value == "slot"

    def test_setstate_invalid(self, test_object: "TestBaseReducible.ReducibleTestObject") -> None:
        """Test the __setstate__ method with an invalid state type.

        This test verifies that __setstate__ raises TypeError for invalid state types.

        Args:
            test_object: A fixture providing a ReducibleTestObject instance.
        """
        # Try to apply an invalid state
        with pytest.raises(TypeError):
            test_object.__setstate__(123)  # Integer is not a valid state type

    def test_getstate_empty_dict(self) -> None:
        """Test __getstate__ with an object that has an empty __dict__.

        This test verifies that __getstate__ returns an empty dict when the object has an empty __dict__.
        """
        # Create a class with an empty __dict__
        class EmptyDictReducible(BaseReducible):
            def __init__(self) -> None:
                super().__init__()

        # Create an instance
        obj = EmptyDictReducible()

        # Get state
        state = obj.__getstate__()

        # Verify state is an empty dict
        assert isinstance(state, dict)
        assert len(state) == 0

    def test_getstate_only_dict(self) -> None:
        """Test __getstate__ with an object that has only __dict__.

        This test verifies that __getstate__ returns a dict when the object has only __dict__.
        """
        # Create a class with only __dict__
        class DictOnlyReducible(BaseReducible):
            def __init__(self) -> None:
                super().__init__()
                self.dict_attr = "dict value"

        # Create an instance
        obj = DictOnlyReducible()

        # Get state
        state = obj.__getstate__()

        # Verify state is a dict
        assert isinstance(state, dict)
        assert "dict_attr" in state
        assert state["dict_attr"] == "dict value"

    def test_getstate_with_slots(self) -> None:
        """Test __getstate__ with an object that has both __dict__ and __slots__.

        This test verifies that __getstate__ returns a tuple with (dict, slots_dict) when the object has both.
        """
        # Create a class with both __dict__ and __slots__
        class SlottedReducible(BaseReducible):
            __slots__ = ("slot_attr",)

            def __init__(self) -> None:
                super().__init__()
                self.dict_attr = "dict value"  # Goes in __dict__
                self.slot_attr = "slot value"  # Goes in __slots__

        # Create an instance
        obj = SlottedReducible()

        # Get state
        state = obj.__getstate__()

        # Verify state is a tuple with (dict, slots_dict)
        assert isinstance(state, tuple)
        assert len(state) == 2
        assert isinstance(state[0], dict)
        assert isinstance(state[1], dict)
        assert "dict_attr" in state[0]
        assert state[0]["dict_attr"] == "dict value"
        assert "slot_attr" in state[1]
        assert state[1]["slot_attr"] == "slot value"

    def test_pickling(self, test_object: "TestBaseReducible.ReducibleTestObject") -> None:
        """Test that a BaseReducible can be pickled and unpickled.

        This test verifies the complete pickling and unpickling process.

        Args:
            test_object: A fixture providing a ReducibleTestObject instance.
        """
        # Modify the object
        test_object.normal_value = "pickled normal"
        test_object.slot_value = "pickled slot"

        # Pickle and unpickle
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Verify the unpickled object has the same values
        assert test_object is not unpickled
        assert isinstance(unpickled, TestBaseReducible.ReducibleTestObject)
        assert unpickled.normal_value == "pickled normal"
        assert unpickled.slot_value == "pickled slot"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])