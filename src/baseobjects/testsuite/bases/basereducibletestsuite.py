"""basereducibletestsuite.py
Base class for test suites which test BaseReducible and its subclasses.

This module provides a base test suite for testing the BaseReducible class and its subclasses. It includes tests for
object reduction and pickling, ensuring that __getstate__ and __setstate__ work correctly with both __dict__ and
__slots__.
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
from ...bases import BaseReducible
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseReducibleTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test BaseReducible and its subclasses.

    This class provides common functionality for test suites that test reducible objects, including tests for
    __getstate__ and __setstate__.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be BaseReducible or a subclass.
    """

    # Attributes #
    UnitTestClass: type[BaseReducible] | None = None  # type: ignore[assignment]

    # Tests #
    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: BaseReducible, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes (state).

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for copying ('copy' or 'method').
        """
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)  # type: ignore[arg-type]
        assert obj_copy.__getstate__() == test_object.__getstate__()

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        test_object: BaseReducible,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with the same attributes (state).

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        else:
            obj_deepcopy = test_object.deepcopy(memo=memo)

        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)  # type: ignore[arg-type]
        assert obj_deepcopy.__getstate__() == test_object.__getstate__()

    # Pickling #
    def test_pickling(self, test_object: BaseReducible) -> None:
        """Tests pickling and unpickling of the object."""
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)  # type: ignore[arg-type]
        assert unpickled.__getstate__() == test_object.__getstate__()

    # Functionality #
    def test_getstate(self, test_object: BaseReducible) -> None:
        """Tests the __getstate__ method of BaseReducible.

        This test verifies that __getstate__ correctly captures both __dict__ and __slots__ attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Ensure object has values
        if hasattr(test_object, "normal_value"):
            test_object.normal_value = "normal"
        if hasattr(test_object, "slot_value"):
            test_object.slot_value = "slot"

        # Get state
        state = test_object.__getstate__()

        # Validate
        if hasattr(test_object, "__dict__") and hasattr(test_object, "__slots__") and test_object.__slots__:
            assert isinstance(state, tuple)  # type: ignore[unreachable]
            assert len(state) == 2
            assert isinstance(state[0], dict)
            assert isinstance(state[1], dict)
        elif hasattr(test_object, "__dict__"):
            assert isinstance(state, dict)
        elif hasattr(test_object, "__slots__") and test_object.__slots__:
            assert isinstance(state, tuple)  # type: ignore[unreachable]
            assert state[0] is None
            assert isinstance(state[1], dict)
        else:
            assert state is None

    def test_setstate(self, test_object: BaseReducible) -> None:
        """Tests the __setstate__ method of BaseReducible.

        This test verifies that __setstate__ correctly restores attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Get original state
        state = test_object.__getstate__()

        # Modify object
        if hasattr(test_object, "normal_value"):
            test_object.normal_value = "modified"
        if hasattr(test_object, "slot_value"):
            test_object.slot_value = "modified"

        # Restore state
        test_object.__setstate__(state)

        # Validate
        if hasattr(test_object, "normal_value"):
            # Assuming original was "normal" or whatever was in state
            pass

    def test_setstate_none(self, test_object: BaseReducible) -> None:
        """Tests the __setstate__ method with None."""
        # Should not raise
        test_object.__setstate__(None)

    def test_setstate_invalid(self, test_object: BaseReducible) -> None:
        """Tests the __setstate__ method with an invalid state type."""
        with pytest.raises(TypeError):
            test_object.__setstate__(123)
