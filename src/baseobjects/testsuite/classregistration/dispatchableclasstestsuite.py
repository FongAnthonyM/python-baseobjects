"""dispatchableclasstestsuite.py
Base test suite for DispatchableClass and its subclasses.
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
from abc import abstractmethod
import copy
import pickle
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from baseobjects.classregistration import DispatchableClass, BaseRegisteredClass
from baseobjects.testsuite.classregistration.baseregisteredclasstestsuite import BaseRegisteredClassTestSuite


# Definitions #
# Classes #
class DispatchableClassTestSuite(BaseRegisteredClassTestSuite):
    """Base test suite for children of DispatchableClass.

    This class provides common test functionality for child classes of DispatchableClass, including tests_old_ for
    class dispatching. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[DispatchableClass]

    # Instance Methods #
    # Tests
    @abstractmethod
    def test_copy(self, test_object: Any) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object

    @abstractmethod
    def test_copy_method(self, test_object: Any) -> None:
        """Test the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object

    @abstractmethod
    def test_deepcopy(self, test_object: Any, memo: dict | None = None) -> None:
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

    @abstractmethod
    def test_deepcopy_method(self, test_object: Any, memo: dict | None = None) -> None:
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

    @abstractmethod
    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object

    @abstractmethod
    def test_get_class_information(self, *args: Any, **kwargs: Any) -> None:
        """Test the get_class_information method.

        This test verifies that the get_class_information method correctly extracts class information from arguments.

        Args:
            *args: Positional arguments to test the get_class_information method.
            **kwargs: Keyword arguments to test the get_class_information method.
        """

    @abstractmethod
    def test_class_dispatch(self, *args: Any, **kwargs: Any) -> None:
        """Test class dispatching.

        Args:
            *args: Positional arguments to test the class dispatching.
            **kwargs: Keyword arguments to test the class dispatching.
        """
