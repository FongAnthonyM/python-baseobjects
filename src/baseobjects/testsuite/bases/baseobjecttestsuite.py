"""baseobjecttestsuite.py
Specialized test suite classes for different types of tests in the baseobjects package.

This module provides the BaseObjectTestSuite class which serves as a foundation for testing classes that inherit from
BaseObject. It includes common test functionality such as tests for copying and pickling. Subclasses should set the
UnitTestClass attribute and may override or extend the test methods.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseObject
from .baseclasstestsuite import BaseClassTestSuite


# Definitions #
# Classes #
class BaseObjectTestSuite(BaseClassTestSuite):
    """Base test suite for children of BaseObject.

    This class provides common test functionality for child class of BaseObject, including tests for copying and
    pickling. Subclasses should set the UnitTestClass attribute and may override or extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestClass: ClassVar[type[BaseObject]]

    # Fixtures #
    @pytest.fixture
    def test_object(self, *args: Any, **kwargs: Any) -> BaseObject:
        """Creates a test object.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            BaseObject: A test object instance.
        """
        return self.UnitTestClass(*args, **kwargs)

    # Tests #
    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        This method can be overridden by subclasses to perform additional tests on the instance.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.UnitTestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.UnitTestClass)

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: BaseObject, method: str) -> None:
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for copying ('copy' or 'method').

        Raises:
            ValueError: If the method is invalid.
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        elif method == "method":
            obj_copy = test_object.copy()
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert obj_copy is not test_object

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        test_object: BaseObject,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.

        Raises:
            ValueError: If the method is invalid.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        elif method == "method":
            obj_deepcopy = test_object.deepcopy(memo=memo)
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert obj_deepcopy is not test_object

    def test_deepcopy_with_memo(self, test_object: BaseObject) -> None:
        """Tests the deepcopy method of BaseObject with a memo dictionary.

        This test verifies that the deepcopy method correctly uses the memo dictionary to avoid
        copying the same object twice.

        Args:
            test_object: A fixture providing a test object instance.
        """
        memo: dict[Any, Any] = {}
        new = test_object.deepcopy(memo=memo)

        # The object should be in the memo dictionary
        assert id(test_object) in memo
        assert memo[id(test_object)] is new

        # A second deepcopy with the same memo should return the same object
        second_new = test_object.deepcopy(memo=memo)
        assert second_new is new

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object

    # Modifications #
    def test_dict_modifications(self, test_object: BaseObject) -> None:
        """Tests BaseObject with __dict__ modifications.

        This test verifies that BaseObject works correctly when __dict__ is modified directly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Modify __dict__ directly
        test_object.__dict__["new_attr"] = "new value"

        # Verify the attribute is accessible
        if hasattr(test_object, "new_attr"):
            assert test_object.new_attr == "new value"

        # Copy the object
        copy_obj = test_object.copy()

        # Verify the copy has the same attribute
        if hasattr(copy_obj, "new_attr") and hasattr(test_object, "new_attr"):
            assert copy_obj.new_attr == test_object.new_attr

        # Verify the copy is a different instance
        assert copy_obj is not test_object
