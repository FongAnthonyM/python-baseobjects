"""basereducible_test.py
Tests for the BaseReducible class in the baseobjects package.

This module provides tests for the BaseReducible class, which extends BaseObject to add functionality for object
reduction and pickling.
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
import pickle
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import BaseReducible
from baseobjects.testsuite.bases import BaseReducibleTestSuite


# Classes #
class ReducibleTestObject(BaseReducible):
    """A subclass of BaseReducible for testing purposes.

    This class has both normal attributes and slot attributes to test pickling behavior.
    """

    __slots__ = ("slot_value",)
    __test__ = False

    # Magic Methods #
    def __init__(self) -> None:
        """Initialize with normal and slot attributes."""
        super().__init__()
        self.normal_value: str = "normal"
        self.slot_value: str = "slot"
        self.mutable_attr: Any = None


class ConcreteReducible(BaseReducible):
    """A simple BaseReducible subclass for testing."""

    __slots__ = ("slot_value",)

    def __init__(self) -> None:
        """Initializes the ConcreteReducible."""
        super().__init__()
        self.normal_value = "normal"
        self.slot_value = "slot"


class SlottedReducible(BaseReducible):
    """A BaseReducible subclass with only slots."""

    __slots__ = ("x",)

    def __init__(self) -> None:
        """Initializes the SlottedReducible."""
        super().__init__()
        self.x = 1


class MixedReducible(BaseReducible):
    """A BaseReducible subclass with both slots and dict."""

    __slots__ = ("y",)

    def __init__(self) -> None:
        """Initializes the MixedReducible."""
        super().__init__()
        self.y = 2
        self.z = 3  # in __dict__


class EmptyDictReducible(BaseReducible):
    """A BaseReducible subclass with an empty dict."""

    def __init__(self) -> None:
        """Initializes the EmptyDictReducible."""
        super().__init__()


class DictOnlyReducible(BaseReducible):
    """A BaseReducible subclass with only dict attributes."""

    def __init__(self) -> None:
        """Initializes the DictOnlyReducible."""
        super().__init__()
        self.dict_attr = "dict value"


class SlottedDictReducible(BaseReducible):
    """A BaseReducible subclass with both slots and dict attributes."""

    __slots__ = ("slot_attr",)

    def __init__(self) -> None:
        """Initializes the SlottedDictReducible."""
        super().__init__()
        self.dict_attr = "dict value"
        self.slot_attr = "slot value"


# Tests #
class TestBaseReducible(BaseReducibleTestSuite):
    """Tests the BaseReducible class.

    This class tests the functionality of the BaseReducible class, which is a base class for objects that need to be
    pickled/reduced in the baseobjects package.
    """

    # Attributes #
    UnitTestClass: type[ReducibleTestObject] = ReducibleTestObject

    def test_getstate_missing_slot(self) -> None:
        """Tests getstate when a slot is missing (deleted)."""
        obj = self.UnitTestClass()
        del obj.slot_value
        state = obj.__getstate__()

        # Check that slot_value is not in the state
        if isinstance(state, tuple):
            # state is (dict, slots_dict) or (None, slots_dict)
            slots = state[1]
            assert "slot_value" not in slots

    @pytest.mark.parametrize(
        ("cls", "validator"),
        [
            (EmptyDictReducible, lambda state: state is None or (isinstance(state, dict) and len(state) == 0)),
            (DictOnlyReducible, lambda state: isinstance(state, dict) and state.get("dict_attr") == "dict value"),
            (
                SlottedDictReducible,
                lambda state: isinstance(state, tuple)
                and state[0]["dict_attr"] == "dict value"
                and state[1]["slot_attr"] == "slot value",
            ),
        ],
    )
    def test_getstate_structure(self, cls: type, validator: Any) -> None:
        """Tests __getstate__ with different object structures.

        Args:
            cls: The class to instantiate and test.
            validator: A function to validate the state.
        """
        obj = cls()
        state = obj.__getstate__()
        assert validator(state)

    def test_setstate_dict_only(self) -> None:
        """Tests the __setstate__ method with only a dict."""

        class DictOnlyReducible(BaseReducible):
            def __init__(self) -> None:
                super().__init__()
                self.dict_attr = "original"

        obj = DictOnlyReducible()
        state = {"dict_attr": "new"}
        obj.__setstate__(state)
        assert obj.dict_attr == "new"

    @pytest.mark.parametrize(
        ("cls", "validator"),
        [
            (
                SlottedReducible,
                lambda obj: obj.x == 1 and (getattr(obj, "__dict__", None) is None or len(obj.__dict__) == 0),
            ),
            (MixedReducible, lambda obj: obj.y == 2 and obj.z == 3 and hasattr(obj, "__dict__")),
        ],
    )
    def test_pickling_scenarios(self, cls: type, validator: Any) -> None:
        """Tests pickling of different object structures.

        Args:
            cls: The class to instantiate and test.
            validator: A function to validate the unpickled object.
        """
        obj = cls()
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert validator(loaded)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
