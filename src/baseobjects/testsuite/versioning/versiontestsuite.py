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
from typing import Any

# Third-Party Packages #
import pytest

try:
    # Third-Party Packages #
    from typeguard import TypeCheckError
except ImportError:
    TypeCheckError = TypeError  # type: ignore

# Local Packages #
from ...versioning.version import Version
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class VersionTestSuite(BaseObjectTestSuite):
    """Base test suite for version classes.

    This class provides common test functionality for version classes, including tests for comparison operations,
    type conversions, and serialization. Subclasses should set the UnitTestClass attribute and may override or extend
    the test methods.

    Attributes:
        UnitTestClass: The version class that the test suite is testing.
    """

    UnitTestClass: type[Version]

    # Tests #
    # Magic Methods #
    def test_hash(self, test_object: Version) -> None:
        """Tests the __hash__ method of Version.

        This test verifies that the __hash__ method returns the id of the object.

        Args:
            test_object: A fixture providing a ConcreteVersion instance.
        """
        assert hash(test_object) == id(test_object)

    def test_str_representation(self, test_object: Version) -> None:
        """Tests the string representation of the version object.

        This test verifies that the __str__ method returns the correct string representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert isinstance(str(test_object), str)
        assert isinstance(test_object.str(), str)
        assert str(test_object) == test_object.str()

    # Instantiation #
    def test_instance_creation(self) -> None:
        """Tests that instances of the class can be created.

        This test verifies that instances of the UnitTestClass can be created.
        """
        instance = self.UnitTestClass()
        assert instance is not None
        assert isinstance(instance, self.UnitTestClass)

    # Copying #
    def test_copy(self, test_object: Version) -> None:
        """Tests the copy behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert obj_copy == test_object

    def test_copy_method(self, test_object: Version) -> None:
        """Tests the copy method behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert obj_copy == test_object

    def test_deepcopy(self, test_object: Version, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of a version object.

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
        assert obj_deepcopy == test_object

    def test_deepcopy_method(self, test_object: Version, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deepcopy method behavior of a version object.

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
        assert obj_deepcopy == test_object

    # Pickling #
    def test_pickling(self, test_object: Version) -> None:
        """Tests pickling and unpickling of a version object.

        This test verifies that the version object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Pickle and Unpickle Version Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert unpickled == test_object

    # Functionality #
    def test_cast_method_valid(self, test_object: Version) -> None:
        """Tests the cast class method with a valid object.

        Args:
             test_object: A fixture providing a test version object instance.
        """
        result = self.UnitTestClass.cast(test_object)
        assert isinstance(result, self.UnitTestClass)
        assert result == test_object

    @pytest.mark.parametrize("pass_", [True, False])
    def test_cast_method_invalid(self, pass_: bool) -> None:
        """Tests the cast class method with an incompatible object.

        Args:
            pass_: Whether to pass the object if casting fails.
        """
        obj = object()
        if pass_:
            result = self.UnitTestClass.cast(obj, pass_=True)
            assert isinstance(result, object)
            assert not isinstance(result, self.UnitTestClass)
        else:
            with pytest.raises((TypeError, TypeCheckError)):
                self.UnitTestClass.cast(obj, pass_=False)

    def test_list_representation(self, test_object: Version) -> None:
        """Tests the list representation of the version object.

        This test verifies that the list method returns the correct list representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert isinstance(test_object.list(), list)

    def test_tuple_representation(self, test_object: Version) -> None:
        """Tests the tuple representation of the version object.

        This test verifies that the tuple method returns the correct tuple representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert isinstance(test_object.tuple(), tuple)

    @abstractmethod
    def test_equality(self) -> None:
        """Tests the __eq__ method of the version class.

        This test verifies that the __eq__ method correctly compares version instances.
        """

    @abstractmethod
    def test_inequality(self) -> None:
        """Tests the __ne__ method of the version class.

        This test verifies that the __ne__ method correctly compares version instances.
        """

    @abstractmethod
    def test_less_than(self) -> None:
        """Tests the __lt__ method of the version class.

        This test verifies that the __lt__ method correctly compares version instances.
        """

    @abstractmethod
    def test_greater_than(self) -> None:
        """Tests the __gt__ method of the version class.

        This test verifies that the __gt__ method correctly compares version instances.
        """

    @abstractmethod
    def test_less_than_or_equal(self) -> None:
        """Tests the __le__ method of the version class.

        This test verifies that the __le__ method correctly compares version instances.
        """

    @abstractmethod
    def test_greater_than_or_equal(self) -> None:
        """Tests the __ge__ method of the version class.

        This test verifies that the __ge__ method correctly compares version instances.
        """
