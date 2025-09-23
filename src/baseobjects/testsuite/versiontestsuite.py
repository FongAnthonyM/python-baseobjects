"""versiontestsuite.py
Specialized test suite for version classes in the Versions package.
"""

# Header #
__package_name__ = "Versions"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
import copy
import pickle
from abc import abstractmethod
from typing import Any, Type

# Third-Party Packages #

# Local Packages #
from ..versioning.version import Version
from .bases import BaseObjectTestSuite


# Definitions #
# Classes #
class VersionTestSuite(BaseObjectTestSuite):
    """Base test suite for version classes.

    This class provides common test functionality for version classes, including tests for comparison operations,
    type conversions, and serialization. Subclasses should set the TestClass attribute and may override or extend
    the test methods.

    Attributes:
        TestClass: The version class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[Version]

    # Instance Methods #
    # Tests
    @abstractmethod
    def test_copy(self, test_object: Version) -> None:
        """Test the copy behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object

    @abstractmethod
    def test_copy_method(self, test_object: Version) -> None:
        """Test the copy method behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object

    @abstractmethod
    def test_deepcopy(self, test_object: Version, memo: dict | None = None) -> None:
        """Test the deep copy behavior of a version object.

        This test verifies that deepcopy creates a new version object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test version object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Version Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object

    @abstractmethod
    def test_deepcopy_method(self, test_object: Version, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of a version object.

        This test verifies that deepcopy creates a new version object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test version object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Version Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object

    @abstractmethod
    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of a version object.

        This test verifies that the version object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Pickle and Unpickle Version Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object

    def test_hash(self, test_object: Version) -> None:
        """Test the __hash__ method of Version.

        This test verifies that the __hash__ method returns the id of the object.

        Args:
            test_object: A fixture providing a TestVersion instance.
        """
        assert hash(test_object) == id(test_object)

    @abstractmethod
    def test_equality(self) -> None:
        """Test the __eq__ method of the version class.

        This test verifies that the __eq__ method correctly compares version instances.
        """

    @abstractmethod
    def test_inequality(self) -> None:
        """Test the __ne__ method of the version class.

        This test verifies that the __ne__ method correctly compares version instances.
        """

    @abstractmethod
    def test_less_than(self) -> None:
        """Test the __lt__ method of the version class.

        This test verifies that the __lt__ method correctly compares version instances.
        """

    @abstractmethod
    def test_greater_than(self) -> None:
        """Test the __gt__ method of the version class.

        This test verifies that the __gt__ method correctly compares version instances.
        """

    @abstractmethod
    def test_less_than_or_equal(self) -> None:
        """Test the __le__ method of the version class.

        This test verifies that the __le__ method correctly compares version instances.
        """

    @abstractmethod
    def test_greater_than_or_equal(self) -> None:
        """Test the __ge__ method of the version class.

        This test verifies that the __ge__ method correctly compares version instances.
        """
