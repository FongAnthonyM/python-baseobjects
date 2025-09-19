"""baseobjecttestsuite.py
Specialized test suite classes for different types of tests_old_ in the baseobjects package.

This module provides the BaseObjectTestSuite class which serves as a foundation for testing classes that inherit from
BaseObject. It includes common test functionality such as tests for copying and pickling. Subclasses should set the
TestClass attribute and may override or extend the test methods.

Typical usage example:

  class MyObjectTestSuite(BaseObjectTestSuite):
      TestClass = MyObject

      def test_specific_functionality(self):
          # Test specific functionality of MyObject
          pass
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
from ...bases import BaseObject
from ..bases import BaseClassTestSuite


# Definitions #
# Classes #
class BaseObjectTestSuite(BaseClassTestSuite):
    """Base test suite for children of BaseObject.

    This class provides common test functionality for child class of BaseObject, including tests_old_ for copying and
    pickling. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[BaseObject]

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self, *args: Any, **kwargs: Any) -> BaseObject:
        """Create a test object.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            BaseObject: A test object instance.
        """
        return self.TestClass(*args, **kwargs)

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This method can be overridden by subclasses to perform additional tests_old_ on the instance.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.TestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.TestClass)

    @abstractmethod
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

    @abstractmethod
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


    @abstractmethod
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

    @abstractmethod
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
